# スクショ保存ツール

保存先フォルダを事前に指定してから範囲選択でスクリーンショットを撮れる、Windows向けデスクトップアプリ。

---

## 概要

通常のスクショは保存場所が固定されがちで、後から整理が手間になる。このツールは「どのフォルダに保存するか」を先に決めてから撮影するため、授業・勉強・作業ごとにフォルダを分けて即整理できる。

---

## 機能

- **フォルダ指定** — 撮影前に保存先フォルダを選択、次回起動時も復元
- **範囲選択撮影** — 画面全体を暗転させてドラッグで範囲を選択
- **自動命名保存** — `screenshot_YYYYMMDD_HHMMSS.png` で自動保存
- **常時最前面** — 小さなウィンドウが常に最前面に表示

---

## 技術スタック

| 領域 | 技術 |
|------|------|
| GUI | PyQt6 |
| スクリーンショット | PyQt6 QScreen |

---

## セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r structured_screenshot_tool/requirements.txt
```

または `run_screenshot_tool.bat` をダブルクリック（初回のみ `setup` が必要な場合あり）。

---

## 起動

```bash
python structured_screenshot_tool/main.py
```

または `run_screenshot_tool.bat` をダブルクリック。

---

## 使い方

1. 「参照」で保存先フォルダを選択
2. 「範囲を選択して撮影」をクリック
3. 画面上でドラッグして範囲を選択
4. 選択した範囲が指定フォルダに自動保存される

`Esc` キーで撮影をキャンセルできる。

---

## 必要環境

- Windows 10/11
- Python 3.10+

---

## ライセンス

MIT
