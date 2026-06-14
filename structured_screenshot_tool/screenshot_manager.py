from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication


class ScreenshotError(RuntimeError):
    pass


def make_screenshot_path(save_folder: Path, now: datetime | None = None) -> Path:
    timestamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    base_name = f"screenshot_{timestamp}"
    candidate = save_folder / f"{base_name}.png"

    counter = 1
    while candidate.exists():
        candidate = save_folder / f"{base_name}_{counter:02d}.png"
        counter += 1

    return candidate


def capture_rect_to_file(rect: QRect, save_folder: Path) -> Path:
    normalized = rect.normalized()
    width = normalized.width()
    height = normalized.height()

    if width <= 0 or height <= 0:
        raise ScreenshotError("選択範囲が小さすぎます。")
    if not save_folder.exists() or not save_folder.is_dir():
        raise ScreenshotError("保存先フォルダが存在しません。")

    target_path = make_screenshot_path(save_folder)
    screen = QApplication.screenAt(normalized.center())
    if screen is None:
        screen = QApplication.primaryScreen()
    if screen is None:
        raise ScreenshotError("スクリーンを取得できませんでした。")

    try:
        pixmap = screen.grabWindow(
            0,
            normalized.left(),
            normalized.top(),
            normalized.width(),
            normalized.height(),
        )
        if pixmap.isNull():
            raise ScreenshotError("スクリーンショットを取得できませんでした。")
        if not pixmap.save(str(target_path), "PNG"):
            raise ScreenshotError("画像ファイルを書き込めませんでした。")
    except Exception as exc:
        if isinstance(exc, ScreenshotError):
            raise
        raise ScreenshotError(f"スクリーンショットの保存に失敗しました: {exc}") from exc

    return target_path
