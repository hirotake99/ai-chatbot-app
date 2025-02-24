def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--image', type=str,)
    parser.add_argument('-p', '--prompt', type=str)
    return parser.parse_args()

# Function to encode the image
def encode_image(image):
    import base64
    # ファイルオブジェクトの場合は直接読み込む
    if hasattr(image, "read"):
        return base64.b64encode(image.read()).decode('utf-8')
    else:
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_and_query(image, query):
    import openai
    import os
    from dotenv import load_dotenv

    # 現在のスクリプトと同じディレクトリにある .env ファイルのパスを取得
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    # .env ファイルから環境変数をロード
    load_dotenv(dotenv_path=env_path)

    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Getting the base64 string
    base64_image = encode_image(image)

    # ユーザーからのメッセージと画像を設定
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]

    # APIリクエストを送信
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=500
    )
    print(response)
    answer = response['choices'][0]['message']['content']
    return answer