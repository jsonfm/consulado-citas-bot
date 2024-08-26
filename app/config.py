import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
    BROWSER_PLAYWRIGHT_ENDPOINT = os.environ("BROWSER_PLAYWRIGHT_ENDPOINT)", "")