# storage.py
import json
import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _path(name: str) -> str:
    p = Path(name)
    if p.is_absolute():
        return str(p)
    return str(DATA_DIR / name)

def read_json(name: str, default: Any = None) -> Any:
    path = _path(name)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(name: str, data: Any) -> None:
    path = _path(name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_text(name: str, default: str = "") -> str:
    path = _path(name)
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(name: str, text: str) -> None:
    path = _path(name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
