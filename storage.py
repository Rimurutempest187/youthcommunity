import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def _path(name: str) -> Path:
    return DATA_DIR / name

def read_json(name: str, default: Any):
    p = _path(name)
    if not p.exists():
        write_json(name, default)
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

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
