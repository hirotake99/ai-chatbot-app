# AI Chatbot Application

このプロジェクトは、OpenAI の API を使用した生成 AI チャットボットアプリケーションです。ユーザーは自然言語、画像、音声の 3 つのモードでチャットボットと対話できます。

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

2. docker で起動

   ```
   docker build -t ai-chatbot .
   docker run -d -p 8501:8501 --name ai-chatbot-app ai-chatbot
   ```

3. OpenAI API の設定を行います。`src/models/.env を新規作成して API キーを追加してください。

## モードの説明

- **自然言語モード**: シンプルな自然言語でのチャットボットと対話できます。
- **画像モード**: 画像と自然言語の質問を入力し、複合的な回答を得ることができます。
- **音声モード**: 音声入力を使用して質問し、回答を得ることができます。

このアプリケーションを通じて、さまざまな形式での対話を楽しんでください。
