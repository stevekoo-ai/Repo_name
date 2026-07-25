"""Shared collector plumbing: retry, raw-tier storage, normalized-tier storage.

Storage layout (Master Instruction 7.4, 7.5):
  data/raw/<source>/<series_id>__<fetched_at>.json   -- immutable, one file per fetch
  data/normalized/<series_id>.csv                     -- tidy (date, value) rows, deduped by date

Raw files are never edited or overwritten — each fetch writes a new
timestamped file, so initial/revised/final releases are all preserved
(7.5's revision requirement).
"""
from __future__ import annotations

import json
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, TypeVar

import pandas as pd

from core.logger import log_event

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
NORMALIZED_DIR = REPO_ROOT / "data" / "normalized"

T = TypeVar("T")


def retry(fn: Callable[[], T], attempts: int = 3, backoff_seconds: float = 1.5, label: str = "") -> T | None:
    """Retry `fn` with linear backoff. Returns None (does not raise) after exhausting attempts.

    Every attempt and the final outcome are logged per 19.1 (API Retry).
    """
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            result = fn()
            if attempt > 1:
                log_event("collector.retry_succeeded", label=label, attempt=attempt)
            return result
        except Exception as exc:  # collectors must never crash the pipeline
            last_exc = exc
            log_event(
                "collector.fetch_failed",
                level="warning",
                label=label,
                attempt=attempt,
                error=str(exc),
            )
            if attempt < attempts:
                time.sleep(backoff_seconds * attempt)
    log_event("collector.fetch_exhausted", level="error", label=label, error=str(last_exc))
    return None


def write_raw(source: str, series_id: str, payload: Any) -> Path:
    """Persist an immutable raw snapshot. Returns the path written."""
    source_dir = RAW_DIR / source
    source_dir.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = source_dir / f"{series_id}__{fetched_at}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
    log_event("collector.raw_saved", source=source, series_id=series_id, path=str(path))
    return path


def latest_raw(source: str, series_id: str) -> Any | None:
    """Read back the most recent raw snapshot for a series, if any."""
    source_dir = RAW_DIR / source
    if not source_dir.exists():
        return None
    candidates = sorted(source_dir.glob(f"{series_id}__*.json"))
    if not candidates:
        return None
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def append_normalized(series_id: str, rows: list[dict]) -> pd.DataFrame:
    """Append (date, value) rows to the normalized-tier CSV for a series, deduped by date.

    `rows` items must have at least {"date": iso-date-str, "value": float}.
    """
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)
    path = NORMALIZED_DIR / f"{series_id}.csv"
    new_df = pd.DataFrame(rows)
    if new_df.empty:
        return new_df
    new_df["date"] = pd.to_datetime(new_df["date"]).dt.date.astype(str)

    if path.exists() and path.stat().st_size > 0:
        existing = pd.read_csv(path)
        existing["date"] = existing["date"].astype(str)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    combined = combined.drop_duplicates(subset=["date"], keep="last").sort_values("date").reset_index(drop=True)
    combined.to_csv(path, index=False)
    log_event("collector.normalized_saved", series_id=series_id, rows=len(combined))
    return combined


def read_normalized(series_id: str) -> pd.DataFrame:
    path = NORMALIZED_DIR / f"{series_id}.csv"
    if not path.exists():
        return pd.DataFrame(columns=["date", "value"])
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def as_date_value_tuples(df: pd.DataFrame) -> list[tuple[date, float]]:
    return [(row.date, float(row.value)) for row in df.itertuples() if pd.notna(row.value)]


def series_change_over_rows(series_id: str, offset_rows: int) -> tuple[float, float] | tuple[None, None]:
    """(latest, value `offset_rows` rows earlier) for a normalized series.

    Used for daily/irregular-cadence series (FX, yields) where a fixed row
    offset approximates a calendar window better than the monthly-cadence
    assumption in core.utils.compute_trend.
    """
    df = read_normalized(series_id)
    if df.empty or len(df) <= offset_rows:
        return None, None
    s = df.sort_values("date")["value"]
    return float(s.iloc[-1]), float(s.iloc[-1 - offset_rows])
