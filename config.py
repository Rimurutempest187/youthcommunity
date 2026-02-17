
# config.py
import json
from pathlib import Path

_cfg_path = Path(__file__).parent / "config.json"
try:
    CONFIG = json.loads(_cfg_path.read_text(encoding="utf-8"))
except Exception:
    CONFIG = {"powered_by": "@Enoch_777", "language_default": "my"}
