from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from ui_main import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("スクショを構造的に保存できるツール")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
