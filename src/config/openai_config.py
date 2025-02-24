import os
from dotenv import load_dotenv

# プロジェクトルートの .env ファイルを読み込む
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_TIMEOUT = int(os.getenv("OPENAI_API_TIMEOUT", 10))  # seconds

def get_openai_config():
    return {
        "api_key": OPENAI_API_KEY,
        "api_base": OPENAI_API_BASE,
        "api_timeout": OPENAI_API_TIMEOUT,
    }