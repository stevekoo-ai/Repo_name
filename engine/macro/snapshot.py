"""Monthly Macro Snapshot storage (Master Instruction 7.12).

Every run persists one snapshot per calendar month at
`data/snapshots/YYYY-MM.json`. Regime persistence rules (11.7's "2개월
연속" checks) and change detection (11.12, "지난달 대비") both read this
history — it is the only place PEOS looks backward in time.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = REPO_ROOT / "data" / "snapshots"


def _month_key(d: date | None = None) -> str:
    d = d or date.today()
    return f"{d.year:04d}-{d.month:02d}"


def save_snapshot(payload: dict[str, Any], month_key: str | None = None) -> Path:
    month_key = month_key or _month_key()
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{month_key}.json"
    payload = {**payload, "month": month_key, "saved_at": datetime.now(timezone.utc).isoformat()}
    path.write_text(json.dumps(payload, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    return path


def load_snapshot(month_key: str) -> dict[str, Any] | None:
    path = SNAPSHOT_DIR / f"{month_key}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_snapshot_months() -> list[str]:
    if not SNAPSHOT_DIR.exists():
        return []
    months = [p.stem for p in SNAPSHOT_DIR.glob("*.json")]
    return sorted(months)


def load_history(limit: int = 6, before_month: str | None = None) -> list[dict[str, Any]]:
    """Most recent `limit` snapshots strictly before `before_month` (defaults to the current month), oldest first."""
    before_month = before_month or _month_key()
    months = [m for m in list_snapshot_months() if m < before_month]
    months = months[-limit:]
    return [load_snapshot(m) for m in months if load_snapshot(m) is not None]


def previous_snapshot(before_month: str | None = None) -> dict[str, Any] | None:
    history = load_history(limit=1, before_month=before_month)
    return history[-1] if history else None
