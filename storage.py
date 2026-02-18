import json
from pathlib import Path
from typing import Any
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def read_json(name, default=None):
    path = name if os.path.isabs(name) else os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(name, data):
    path = name if os.path.isabs(name) else os.path.join(DATA_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_text(name: str, default: str = "") -> str:
    p = _path(name)
    if not p.exists():
        p.write_text(default, encoding="utf-8")
        return default
    return p.read_text(encoding="utf-8")

def write_text(name: str, text: str):
    p = _path(name)
    p.write_text(text, encoding="utf-8")
