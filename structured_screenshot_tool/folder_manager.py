from __future__ import annotations

from pathlib import Path


class FolderError(ValueError):
    pass


def validate_save_folder(path_text: str) -> Path:
    path_text = path_text.strip().strip('"')
    if not path_text:
        raise FolderError("保存先フォルダを選択してください。")

    path = Path(path_text).expanduser()
    if not path.exists():
        raise FolderError("指定されたフォルダが存在しません。")
    if not path.is_dir():
        raise FolderError("指定されたパスはフォルダではありません。")

    try:
        next(path.iterdir(), None)
    except OSError:
        raise FolderError("指定されたフォルダを読み取れません。")

    return path.resolve()
