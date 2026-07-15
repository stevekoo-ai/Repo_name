"""Folds the existing Macro Investment Clock project in as a supplementary
US/global context signal (per user decision: absorb src/clock as a PEOS
input source rather than maintaining two disconnected systems).

This reuses src/clock's own growth/inflation momentum model as-is — it is
not re-derived here — and is attached to the macro payload as
`macro.us_investment_clock` context (favored asset class per the
Merrill Lynch clock framework), separate from and complementary to the
Core-10 `us_global` composite indicator in engine/macro/indicators.py.

If a live FRED fetch isn't possible (e.g. this environment's outbound
network is policy-blocked), we fall back to the last row of the daily
GitHub Actions job's own history file (data/history.csv) rather than
showing nothing — that dashboard already runs independently once a day,
so its last known reading is still meaningful context, just possibly
stale. Only if neither live data nor history is available do we return
None.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.logger import log_event

REPO_ROOT = Path(__file__).resolve().parents[2]
HISTORY_PATH = REPO_ROOT / "data" / "history.csv"
DASHBOARD_URL_HINT = "GitHub Pages 활성화 시 https://<github계정>.github.io/<저장소명>/ 에서 매일 갱신되는 대시보드로 확인 가능"


def _from_history() -> dict | None:
    if not HISTORY_PATH.exists():
        return None
    try:
        from src.clock.model import PHASES
        df = pd.read_csv(HISTORY_PATH)
        if df.empty:
            return None
        # data/history.csv holds one row per historical month (data_asof) as of
        # the backfill/time-machine upgrade, not one row per daily run — the
        # last-computed timestamp lives in `last_updated`, not `run_date`.
        latest = df.sort_values("data_asof").iloc[-1]
        phase = PHASES_BY_NAME(PHASES).get(latest["phase"])
        if phase is None:
            return None
        return {
            "phase": latest["phase"],
            "phase_kr": phase["name_kr"],
            "favored_asset": latest["asset"],
            "favored_asset_kr": phase["asset_kr"],
            "growth_signal": latest["growth_signal"],
            "inflation_signal": latest["inflation_signal"],
            "as_of": str(latest["data_asof"]),
            "source": "stale_history",
            "note": f"실시간 조회 불가 — {latest['last_updated']} 실행분(마지막 저장값) 사용. {DASHBOARD_URL_HINT}",
        }
    except Exception as exc:
        log_event("us_clock.history_fallback_failed", level="warning", error=str(exc))
        return None


def PHASES_BY_NAME(phases: dict) -> dict:
    return {p["name"]: p for p in phases.values()}


def get_investment_clock_context() -> dict | None:
    try:
        from src.clock import data_sources as clock_data_sources
        from src.clock.model import read_clock
    except Exception as exc:  # pragma: no cover - import wiring issue, not a data failure
        log_event("us_clock.import_failed", level="warning", error=str(exc))
        return _from_history()

    try:
        series = clock_data_sources.fetch_all()
        reading = read_clock(series)
    except Exception as exc:
        log_event("us_clock.fetch_failed", level="warning", error=str(exc))
        return _from_history()

    return {
        "phase": reading.phase["name"],
        "phase_kr": reading.phase["name_kr"],
        "favored_asset": reading.phase["asset"],
        "favored_asset_kr": reading.phase["asset_kr"],
        "growth_signal": reading.growth.label,
        "inflation_signal": reading.inflation.label,
        "as_of": max(reading.growth.as_of, reading.inflation.as_of).date().isoformat(),
        "source": "live",
        "note": DASHBOARD_URL_HINT,
    }
