from __future__ import annotations

from PyQt6.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QKeyEvent, QMouseEvent, QPainter, QPen
from PyQt6.QtWidgets import QApplication, QWidget


class OverlaySelector(QWidget):
    selection_made = pyqtSignal(QRect)
    selection_cancelled = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.start_global: QPoint | None = None
        self.current_global: QPoint | None = None
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        virtual_geometry = self._virtual_screen_geometry()
        self.setGeometry(virtual_geometry)

    def showEvent(self, event) -> None:  # type: ignore[override]
        super().showEvent(event)
        self.activateWindow()
        self.raise_()
        self.setFocus()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_global = event.globalPosition().toPoint()
            self.current_global = self.start_global
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.start_global is not None:
            self.current_global = event.globalPosition().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton or self.start_global is None:
            return

        self.current_global = event.globalPosition().toPoint()
        rect = QRect(self.start_global, self.current_global).normalized()
        self.start_global = None
        self.current_global = None
        self.close()

        if rect.width() <= 0 or rect.height() <= 0:
            self.selection_cancelled.emit()
            return

        self.selection_made.emit(rect)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            self.selection_cancelled.emit()
            return
        super().keyPressEvent(event)

    def paintEvent(self, event) -> None:  # type: ignore[override]
        del event
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 90))

        if self.start_global is None or self.current_global is None:
            self._draw_hint(painter)
            return

        rect = QRect(
            self.mapFromGlobal(self.start_global),
            self.mapFromGlobal(self.current_global),
        ).normalized()

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(rect, QColor(0, 0, 0, 0))
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setPen(QPen(QColor(0, 150, 255), 2))
        painter.drawRect(rect)

    def _draw_hint(self, painter: QPainter) -> None:
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            "ドラッグして保存する範囲を選択してください\nEscでキャンセル",
        )

    def _virtual_screen_geometry(self) -> QRect:
        screens = QApplication.screens()
        if not screens:
            return QRect(0, 0, 800, 600)

        geometry = screens[0].geometry()
        for screen in screens[1:]:
            geometry = geometry.united(screen.geometry())
        return geometry
