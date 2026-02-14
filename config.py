import logging
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://routellm.abacus.ai/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")
if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

# Models (configurable via env)
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o")
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")
TTS_VOICE = os.getenv("TTS_VOICE", "alloy")

# Database
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///serbian_tutor.db")
# Render gives postgres://, SQLAlchemy needs postgresql+asyncpg://
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Admin
ADMIN_ID = int(os.getenv("ADMIN_ID", "485544391"))

# Promo codes: code -> days of pro access
PROMO_CODES: dict[str, int] = {
    "SHABBAT": 60,
}

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
