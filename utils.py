# utils.py
import os
from typing import Optional

# Environment variables
BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "").strip()
BOTEN: str = os.environ.get("BOTEN", "0").strip()  # "1" for English responses if needed

def require_bot_token() -> None:
    """Raise RuntimeError if BOT_TOKEN is not set."""
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Please set the BOT_TOKEN environment variable.")
