# utils.py
import os
from typing import List, Optional

def _env_str(key: str, default: str = "") -> str:
    """Return stripped environment variable or default."""
    return os.environ.get(key, default).strip()

def get_bot_token() -> str:
    """Read BOT_TOKEN from environment at call time."""
    return _env_str("BOT_TOKEN", "")

def require_bot_token() -> None:
    """Raise RuntimeError if BOT_TOKEN is not set."""
    if not get_bot_token():
        raise RuntimeError("BOT_TOKEN is not set. Please set the BOT_TOKEN environment variable.")

def get_boten_flag() -> bool:
    """Return True if BOTEN env is set to a truthy value (1, true, yes)."""
    v = _env_str("BOTEN", "0").lower()
    return v in ("1", "true", "yes", "on")

def _parse_int_list(env_value: str) -> List[int]:
    """Parse comma-separated integers from an env string, ignore invalid items."""
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
    """
    Read ADMIN_IDS from environment.
    Accepts comma-separated integers, e.g. "12345,67890".
    Returns list of ints (empty list if none).
    """
    raw = _env_str("ADMIN_IDS", "")
    return _parse_int_list(raw)

# Module-level convenience values (read-on-import but functions above are preferred)
BOT_TOKEN: str = get_bot_token()
BOTEN: bool = get_boten_flag()
ADMIN_IDS: List[int] = get_admin_ids()
