
# config.py
import json
from pathlib import Path
# utils.py
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# optional English flag if you used earlier
BOTEN = os.environ.get("BOTEN", "0")  # "1" for English responses if needed

_cfg_path = Path(__file__).parent / "config.json"
try:
    CONFIG = json.loads(_cfg_path.read_text(encoding="utf-8"))
except Exception:
    CONFIG = {"powered_by": "@Enoch_777", "language_default": "my"}
