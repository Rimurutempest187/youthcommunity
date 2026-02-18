# storage.py
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _path(name: str) -> str:
    return name if os.path.isabs(name) else str(DATA_DIR / name)

def read_json(name: str, default=None):
    path = _path(name)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(name: str, data):
    path = _path(name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_text(name: str, default=""):
    path = _path(name)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(name: str, text: str):
    path = _path(name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
