# config.py
import json
from pathlib import Path
from typing import Any, Dict

BASE_DIR = Path(__file__).parent
CFG_PATH = BASE_DIR / "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "powered_by": "@Enoch_777",
    "language_default": "my",
    "daily_verse_time": "08:00",   # HH:MM (server local time)
    "timezone": "Asia/Yangon"
}

def load_config() -> Dict[str, Any]:
    """
    Safely load config.json and return a dict.
    If file is missing or invalid, return DEFAULT_CONFIG.
    """
    try:
        if not CFG_PATH.exists():
            return DEFAULT_CONFIG.copy()
        text = CFG_PATH.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, dict):
            return DEFAULT_CONFIG.copy()
        # merge defaults with file values (file overrides defaults)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(data)
        return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()

# module-level CONFIG for easy import
CONFIG = load_config()

def reload_config() -> Dict[str, Any]:
    """Reload config from disk and update CONFIG value."""
    global CONFIG
    CONFIG = load_config()
    return CONFIG
