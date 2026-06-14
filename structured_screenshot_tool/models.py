from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    save_folder: str | None = None


@dataclass
class AppState:
    config: AppConfig
    current_save_path: Path | None = None
