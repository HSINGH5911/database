import fnmatch
import time
from typing import Any, List, Union

def glob_match(pattern: str, text: str) -> bool:
    """
    Glob-style pattern matching used by KEYS and SCAN commands.
    """
    return fnmatch.fnmatch(text, pattern)

def current_time_ms() -> int:
    """
    Returns current epoch timestamp in milliseconds.
    """
    return int(time.time() * 1000)

def format_bytes(size: int) -> str:
    """
    Formats raw byte counts into human readable string (KB, MB, GB).
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size) < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """
    Safely converts a value to integer.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    """
    Safely converts a value to float.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
