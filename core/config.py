"""Config loader for PEOS.

All rules, thresholds, templates and user/portfolio data live in YAML under
`config/` (never hardcoded in engine code — see Master Instruction 24.1).
This module loads them once per process and caches the result.

Secrets (API keys) are never stored in the YAML files themselves. `api.yaml`
only records *which environment variable* holds a given source's key; the
actual value is read from the environment (or a local `.env` file, loaded
if present and `python-dotenv`-style KEY=VALUE lines exist) at call time.
"""
from __future__ import annotations

import functools
import os
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"
ENV_FILE = REPO_ROOT / ".env"

_loaded_env = False


def _load_dotenv_once() -> None:
    """Best-effort .env loader so local runs don't need to export vars manually.

    No-op if the file doesn't exist or a var is already set (env wins).
    """
    global _loaded_env
    if _loaded_env or not ENV_FILE.exists():
        _loaded_env = True
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
    _loaded_env = True


@functools.lru_cache(maxsize=None)
def load_yaml(name: str) -> dict[str, Any]:
    """Load one YAML config file by name (with or without .yaml suffix)."""
    _load_dotenv_once()
    filename = name if name.endswith((".yaml", ".yml")) else f"{name}.yaml"
    path = CONFIG_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def reload_all() -> None:
    """Clear the config cache — used by tests that swap fixture configs."""
    load_yaml.cache_clear()


def api_config() -> dict[str, Any]:
    return load_yaml("api")


def rules_config() -> dict[str, Any]:
    return load_yaml("rules")


def thresholds_config() -> dict[str, Any]:
    return load_yaml("thresholds")


def user_profile() -> dict[str, Any]:
    return load_yaml("user")


def portfolio_config() -> dict[str, Any]:
    return load_yaml("portfolio")


def schedule_config() -> dict[str, Any]:
    return load_yaml("schedule")


def report_config() -> dict[str, Any]:
    return load_yaml("report")


def get_api_key(source: str) -> str | None:
    """Resolve the API key for a data source declared in config/api.yaml.

    api.yaml declares e.g. `ecos: {env_key: ECOS_API_KEY}`. We read the
    named environment variable. Returns None (not an empty string) if unset,
    so callers can cleanly fall back to Pending/mock behavior.
    """
    _load_dotenv_once()
    source_cfg = api_config().get("sources", {}).get(source, {})
    env_key = source_cfg.get("env_key")
    if not env_key:
        return None
    value = os.environ.get(env_key)
    return value or None


def has_api_key(source: str) -> bool:
    return get_api_key(source) is not None
