from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config_manager import load_config, save_config
from folder_manager import FolderError, validate_save_folder
from models import AppState
from overlay_selector import OverlaySelector
from screenshot_manager import ScreenshotError, capture_rect_to_file


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.config = load_config()
        self.state = AppState(config=self.config)
        self.overlay: OverlaySelector | None = None

        self.setWindowTitle("スクショ保存ツール")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(240, 150)
        self._build_ui()
        self._load_initial_state()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(6, 5, 6, 5)
        main_layout.setSpacing(4)

        title = QLabel("スクショ保存ツール")
        title_font = QFont()
        title_font.setPointSize(10)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)

        main_layout.addWidget(self._make_folder_section())
        main_layout.addWidget(self._make_capture_section())
        main_layout.addStretch()

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #f7f8fa;
                color: #1f2933;
                font-size: 9px;
            }
            QFrame {
                background: #ffffff;
                border: 1px solid #d9dee7;
                border-radius: 4px;
            }
            QPushButton {
                min-height: 18px;
                padding: 1px 6px;
                border: 1px solid #9aa7b7;
                border-radius: 4px;
                background: #ffffff;
            }
            QPushButton:hover {
                background: #eef4ff;
                border-color: #6d8fca;
            }
            QPushButton#captureButton {
                min-height: 23px;
                font-weight: 700;
                color: #ffffff;
                border: 1px solid #1f5d98;
                background: #256fae;
            }
            QPushButton#captureButton:hover {
                background: #1f5d98;
            }
            QLabel#sectionTitle {
                font-weight: 700;
            }
            QLabel#pathLabel, QLabel#statusLabel {
                color: #334155;
                background: transparent;
            }
            """
        )

    def _make_folder_section(self) -> QFrame:
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(6, 4, 6, 5)
        layout.setSpacing(2)

        header = QHBoxLayout()
        title = QLabel("保存先フォルダ")
        title.setObjectName("sectionTitle")
        self.browse_button = QPushButton("参照")
        self.browse_button.clicked.connect(self._browse_save_folder)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.browse_button)

        self.save_path_label = QLabel("未設定")
        self.save_path_label.setObjectName("pathLabel")
        self.save_path_label.setWordWrap(True)
        self.save_path_label.setMaximumHeight(28)

        layout.addLayout(header)
        layout.addWidget(self.save_path_label)
        return section

    def _make_capture_section(self) -> QFrame:
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(6, 4, 6, 5)
        layout.setSpacing(3)

        self.capture_button = QPushButton("範囲を選択して撮影")
        self.capture_button.setObjectName("captureButton")
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setMaximumHeight(24)

        self.capture_button.clicked.connect(self._start_capture)

        layout.addWidget(self.capture_button)
        layout.addWidget(self.status_label)
        return section

    def _load_initial_state(self) -> None:
        if self.config.save_folder:
            try:
                validated = validate_save_folder(self.config.save_folder)
                self.config.save_folder = str(validated)
                self._update_path_label()
                self._set_status("保存先を復元しました。")
                save_config(self.config)
                return
            except FolderError as exc:
                self.config.save_folder = None
                self._set_status(str(exc), error=True)

        self._update_path_label()
        if not self.config.save_folder:
            self._set_status("保存先フォルダを参照から選択してください。")

    def _browse_save_folder(self) -> None:
        start_dir = self.config.save_folder or str(Path.home())
        folder = QFileDialog.getExistingDirectory(self, "保存先フォルダを選択", start_dir)
        if not folder:
            return

        try:
            save_folder = validate_save_folder(folder)
        except FolderError as exc:
            self._set_status(str(exc), error=True)
            QMessageBox.warning(self, "保存先を設定できません", str(exc))
            return

        self.config.save_folder = str(save_folder)
        save_config(self.config)
        self._update_path_label()
        self._set_status("保存先フォルダを設定しました。")

    def _update_path_label(self) -> None:
        self.state.current_save_path = (
            Path(self.config.save_folder) if self.config.save_folder else None
        )
        path_text = str(self.state.current_save_path) if self.state.current_save_path else "未設定"
        self.save_path_label.setText(path_text)
        self.save_path_label.setToolTip(path_text)

    def _start_capture(self) -> None:
        self._update_path_label()
        save_path = self.state.current_save_path
        if save_path is None:
            self._set_status("保存先フォルダを選択してください。", error=True)
            return
        if not save_path.exists() or not save_path.is_dir():
            self._set_status("保存先フォルダが存在しません。", error=True)
            return

        self.hide()
        QTimer.singleShot(180, self._show_overlay)

    def _show_overlay(self) -> None:
        self.overlay = OverlaySelector()
        self.overlay.selection_made.connect(self._capture_selected_rect)
        self.overlay.selection_cancelled.connect(self._capture_cancelled)
        self.overlay.show()

    def _capture_selected_rect(self, rect) -> None:
        save_path = self.state.current_save_path
        if save_path is None:
            self.show()
            self._set_status("保存先フォルダを選択してください。", error=True)
            return

        QTimer.singleShot(180, lambda: self._save_selected_rect(rect, save_path))

    def _save_selected_rect(self, rect, save_path: Path) -> None:
        try:
            target_path = capture_rect_to_file(rect, save_path)
        except ScreenshotError as exc:
            self.show()
            self._set_status(str(exc), error=True)
            QMessageBox.warning(self, "保存できません", str(exc))
            return

        self.show()
        self.activateWindow()
        self._set_status(f"保存しました: {target_path.name}")

    def _capture_cancelled(self) -> None:
        self.show()
        self.activateWindow()
        self._set_status("撮影をキャンセルしました。")

    def _set_status(self, message: str, error: bool = False) -> None:
        self.status_label.setText(message)
        color = "#b42318" if error else "#334155"
        self.status_label.setStyleSheet(f"color: {color};")
