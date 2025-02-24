FROM python:3.8-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なツール・ライブラリのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    portaudio19-dev

# 依存関係ファイルをコピーしインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ソースコード全体をコピー
COPY . .

# Streamlitのデフォルトポートを公開
EXPOSE 8501

# Streamlitアプリを起動
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]
