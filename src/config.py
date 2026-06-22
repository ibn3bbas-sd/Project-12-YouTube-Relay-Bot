import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_ALLOWED_CHAT_ID = int(os.environ["TELEGRAM_ALLOWED_CHAT_ID"])

SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID", "UC8semOV-MqT3enT4M0mS1ow")
TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "UCCKQxDfs0eIVsLmnc4JVtpQ")
YOUTUBE_CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "config/client_secret.json")
YOUTUBE_TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "config/token.json")

SCHEDULE_MORNING = os.getenv("SCHEDULE_MORNING", "06:00")
SCHEDULE_EVENING = os.getenv("SCHEDULE_EVENING", "18:00")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Riyadh")

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
MAX_VIDEO_AGE_DAYS = int(os.getenv("MAX_VIDEO_AGE_DAYS", "7"))
VIDEO_QUALITY = os.getenv("VIDEO_QUALITY", "best[height<=1080]")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_ENABLED = os.getenv("GEMINI_ENABLED", "false").lower() == "true"

DATA_DIR = "data"
PROCESSED_FILE = f"{DATA_DIR}/processed_videos.json"
