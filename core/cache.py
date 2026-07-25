"""Simple TTL file cache for collector responses.

Master Instruction 18.2 sets per-series cache windows (FX/rates 30min,
market prices 5min, monthly macro series 24h). Rather than hardcode these,
callers pass the ttl_seconds for the series they're fetching (sourced from
config/api.yaml `cache_ttl_seconds`), keeping the policy externalized.

On API failure, collectors fall back to `get_stale()` — the last cached
value regardless of TTL — per the failure-handling flow in 19.2 (Retry ->
alternate source -> cache -> Warning -> log).
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = REPO_ROOT / "data" / ".cache"


def _cache_path(key: str) -> Path:
    safe_key = key.replace("/", "__").replace(" ", "_")
    return CACHE_DIR / f"{safe_key}.json"


def get(key: str, ttl_seconds: int) -> Any | None:
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if time.time() - payload.get("cached_at", 0) > ttl_seconds:
        return None
    return payload.get("value")


def get_stale(key: str) -> Any | None:
    """Return the cached value regardless of age (last-resort fallback)."""
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return payload.get("value")


def set(key: str, value: Any) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(key)
    payload = {"cached_at": time.time(), "value": value}
    path.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")
