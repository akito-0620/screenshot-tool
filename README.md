# スクショを構造的に保存できるツール

スクリーンショットを撮影する前に保存先フォルダを設定しておくことで、講義・研究・就活など用途ごとに自動整理できる Windows デスクトップアプリです。

## 機能

- **2段階フォルダ管理**: 親フォルダを基準に子フォルダを選択・作成して保存先を整理
- **範囲選択スクリーンショット**: マウスドラッグで取得範囲を指定して撮影
- **ファイル名自動生成**: `screenshot_YYYYMMDD_HHMMSS.png` 形式で保存
- **設定の永続化**: `config.json` に保存し次回起動時に復元

## 必要環境

- Python 3.8+
- Windows

## インストール

```bash
pip install -r structured_screenshot_tool/requirements.txt
```

## 使い方

```bash
python structured_screenshot_tool/main.py
```

1. **親フォルダ設定**: 「参照」ボタンまたはパス直接入力でスクショ保存のルートフォルダを指定
2. **保存先フォルダ選択**: 親フォルダ内の子フォルダを一覧から選択（新規作成も可能）
3. **撮影**: 「範囲を選択して撮影」ボタンを押し、マウスでドラッグして範囲を指定
4. Escキーでキャンセル可能

## ファイル構成

```
structured_screenshot_tool/
├── main.py                # アプリ起動処理
├── ui_main.py             # メイン画面 UI
├── config_manager.py      # JSON 設定の読み書き
├── folder_manager.py      # フォルダ検証・一覧取得・新規作成
├── screenshot_manager.py  # スクリーンショット撮影と画像保存
├── overlay_selector.py    # 範囲選択オーバーレイ UI
├── models.py              # データクラス定義
└── requirements.txt       # 依存ライブラリ
```

## 技術スタック

| ライブラリ | 用途 |
|---|---|
| PyQt6 | GUI フレームワーク |
| mss | スクリーンショット取得 |
| Pillow | 画像保存 |