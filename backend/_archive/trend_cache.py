import json
import os
import time
import hashlib
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / 'cache' / 'trends'
CACHE_TTL = 24 * 60 * 60  # 24 hours in seconds

# In-memory cache for faster access
_memory_cache = {}
MEMORY_TTL = 60 * 60  # 1 hour in seconds


def _get_cache_key(keyword: str) -> str:
    """Generate a safe filename from keyword."""
    return hashlib.md5(keyword.lower().strip().encode()).hexdigest()


def _ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_cached(keyword: str) -> dict | None:
    """
    Get cached trend data for a keyword.
    Checks memory cache first, then file cache.
    Returns None if no valid cache exists.
    """
    cache_key = _get_cache_key(keyword)
    now = time.time()

    # Check memory cache first
    if cache_key in _memory_cache:
        entry = _memory_cache[cache_key]
        if now - entry['timestamp'] < MEMORY_TTL:
            return entry['data']
        else:
            del _memory_cache[cache_key]

    # Check file cache
    _ensure_cache_dir()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                entry = json.load(f)

            if now - entry['timestamp'] < CACHE_TTL:
                # Refresh memory cache
                _memory_cache[cache_key] = entry
                return entry['data']
            else:
                # Cache expired, remove file
                cache_file.unlink()
        except (json.JSONDecodeError, KeyError):
            # Corrupted cache, remove it
            cache_file.unlink()

    return None


def set_cached(keyword: str, data: dict) -> None:
    """
    Cache trend data for a keyword.
    Stores in both memory and file cache.
    """
    cache_key = _get_cache_key(keyword)
    now = time.time()

    entry = {
        'keyword': keyword.lower().strip(),
        'timestamp': now,
        'data': data
    }

    # Store in memory
    _memory_cache[cache_key] = entry

    # Store in file
    _ensure_cache_dir()
    cache_file = CACHE_DIR / f"{cache_key}.json"

    try:
        with open(cache_file, 'w') as f:
            json.dump(entry, f)
    except IOError:
        pass  # Fail silently, memory cache still works


def clear_cache() -> int:
    """Clear all cached trend data. Returns number of entries cleared."""
    global _memory_cache
    count = len(_memory_cache)
    _memory_cache = {}

    _ensure_cache_dir()
    for cache_file in CACHE_DIR.glob('*.json'):
        try:
            cache_file.unlink()
            count += 1
        except IOError:
            pass

    return count
