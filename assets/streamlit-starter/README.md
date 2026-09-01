# 業務管理アプリ

病院・検査室内の業務を、担当者・期限・ステータスとともに管理する日本語アプリです。データはこのPC内の `data/app.db` に保存されます。

## 必要環境

- Python 3.11以上
- Windows 10/11（macOS・Linuxでも起動可能）

## 初回セットアップと起動

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

表示されたURLをブラウザで開きます。停止するときはPowerShellで `Ctrl+C` を押します。

## バックアップ

アプリを停止してから `data/app.db` を別の安全な場所へコピーしてください。復元するときは同じ場所へ戻します。患者情報など機微情報を扱う場合は、院内の保存・バックアップ規程を優先してください。

## 別PCへの移行

このフォルダ全体を別PCへコピーし、新しいPCで「初回セットアップと起動」を行います。データも移す場合は `data/app.db` を含めます。`.venv` はコピーせず、新しいPCで作り直してください。

## 注意

このアプリは業務管理用です。診断、治療、検査結果の医学的判断には使用しません。

