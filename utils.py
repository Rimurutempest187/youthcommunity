import os
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

def load_config():
    cfg_path = ROOT / "config.json"
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}
CONFIG = load_config()
