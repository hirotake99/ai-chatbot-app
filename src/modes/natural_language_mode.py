def chat_with_bot(user_input, conversation_history):
    import openai
    import os
    from dotenv import load_dotenv

    # 現在のスクリプトと同じディレクトリにある .env ファイルのパスを取得
    env_path = os.path.join(os.path.dirname(__file__), '.env')

    # .env ファイルから環境変数をロード
    load_dotenv(dotenv_path=env_path)

    # openai.api_key = OPENAI_API_KEY
    openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = []
    # 会話履歴をメッセージリストに追加
    for entry in conversation_history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["bot"]})
    # 現在のユーザー入力を追加
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )


    return response.choices[0].message['content']