from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import AppConfig


CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


def load_config(config_path: Path = CONFIG_PATH) -> AppConfig:
    if not config_path.exists():
        return AppConfig()

    try:
        data: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AppConfig()

    save_folder = data.get("save_folder")
    legacy_parent_folder = data.get("parent_folder")
    folder = save_folder if isinstance(save_folder, str) else legacy_parent_folder

    return AppConfig(save_folder=folder if isinstance(folder, str) else None)


def save_config(config: AppConfig, config_path: Path = CONFIG_PATH) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    data = {"save_folder": config.save_folder}
    config_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
