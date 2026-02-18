# utils.py
import os
from typing import List

def _env_str(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()

def get_bot_token() -> str:
    return _env_str("BOT_TOKEN", "")

def require_bot_token() -> None:
    if not get_bot_token():
        raise RuntimeError("BOT_TOKEN is not set. Please set BOT_TOKEN in .env or environment.")

def get_boten_flag() -> bool:
    v = _env_str("BOTEN", "0").lower()
    return v in ("1", "true", "yes", "on")

def _parse_int_list(env_value: str) -> List[int]:
    out: List[int] = []
    for part in env_value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(int(part))
        except ValueError:
            continue
    return out

def get_admin_ids() -> List[int]:
    raw = _env_str("ADMIN_IDS", "")
    return _parse_int_list(raw)

BOT_TOKEN: str = get_bot_token()
BOTEN: bool = get_boten_flag()
ADMIN_IDS: List[int] = get_admin_ids()
