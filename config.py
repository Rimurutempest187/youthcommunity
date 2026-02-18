# config.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
CFG_PATH = BASE_DIR / "config.json"

def load_config() -> dict:
    """Load config.json safely and return dict. Return default if file missing or invalid."""
    default = {"powered_by": "@Enoch_777", "language_default": "my"}
    try:
        if not CFG_PATH.exists():
            return default
        text = CFG_PATH.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, dict):
            return default
        return data
    except Exception:
        return default

# module-level CONFIG for easy import
CONFIG = load_config()
