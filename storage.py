import json
from pathlib import Path
from typing import Any
from utils import DATA_DIR

def _path(name: str) -> Path:
    return DATA_DIR / name

def read_json(name: str, default: Any):
    p = _path(name)
    if not p.exists():
        write_json(name, default)
        return default
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def write_json(name: str, data: Any):
    p = _path(name)
    with p.open("w", encoding="utf-8") as f:
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
