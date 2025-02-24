# AI Chatbot Application

このプロジェクトは、OpenAIのAPIを使用した生成AIチャットボットアプリケーションです。ユーザーは自然言語、画像、音声の3つのモードでチャットボットと対話できます。

## プロジェクト構成

```
ai-chatbot-app
├── src
│   ├── app.py                  # アプリケーションのメインエントリポイント
│   ├── modes
│   │   ├── natural_language_mode.py  # 自然言語モードの実装
│   │   ├── image_mode.py           # 画像モードの実装
│   │   └── audio_mode.py           # 音声モードの実装
│   └── config
│       └── openai_config.py        # OpenAI APIの設定
├── Dockerfile                      # Dockerイメージのビルド指示
├── requirements.txt                # プロジェクトの依存関係
└── README.md                       # プロジェクトのドキュメント
```

## セットアップ

1. リポジトリをクローンします。
   ```
   git clone <repository-url>
   cd ai-chatbot-app
   ```

2. 必要な依存関係をインストールします。
   ```
   pip install -r requirements.txt
   ```

3. OpenAI APIの設定を行います。`src/config/openai_config.py`にAPIキーを追加してください。

## 使用方法

アプリケーションを起動するには、以下のコマンドを実行します。

```
streamlit run src/app.py
```

## モードの説明

- **自然言語モード**: シンプルな自然言語でのチャットボットと対話できます。
- **画像モード**: 画像と自然言語の質問を入力し、複合的な回答を得ることができます。
- **音声モード**: 音声入力を使用して質問し、回答を得ることができます。

このアプリケーションを通じて、さまざまな形式での対話を楽しんでください。