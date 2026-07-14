"""Structured logging for PEOS.

Master Instruction 19.1 requires every stage (collection success/failure,
API retry, cache hit, revision detected, rule applied, score computed,
report generated, user input changed) to be logged. We emit both a normal
console line and a JSON-lines record to `logs/peos.jsonl` so the trail is
machine-parseable later without adding a dependency on a logging backend.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = REPO_ROOT / "logs"
LOG_FILE = LOG_DIR / "peos.jsonl"

_configured = False


def _configure_root() -> None:
    global _configured
    if _configured:
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
    _configured = True


def get_logger(name: str) -> logging.Logger:
    _configure_root()
    return logging.getLogger(name)


def log_event(event: str, level: str = "info", **fields: Any) -> None:
    """Record a structured pipeline event (collection, validation, rule, score, report...).

    Always appends a JSON line to logs/peos.jsonl and mirrors a short
    message to the standard logger so it's visible in console output too.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "level": level,
        **fields,
    }
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except OSError:
        pass  # logging must never crash the pipeline

    logger = get_logger("peos")
    msg = f"{event} :: " + ", ".join(f"{k}={v}" for k, v in fields.items())
    getattr(logger, level, logger.info)(msg)
