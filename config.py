import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

FORUM_CHAT_ID: int = int(os.getenv("FORUM_CHAT_ID"))

FORUM_THREAD_ID: int = int(os.getenv("FORUM_THREAD_ID"))

DAILY_SCHEDULE_TIME: str = os.getenv("DAILY_SCHEDULE_TIME")

TIMEZONE: str = os.getenv("TIMEZONE")
