"""Folds the existing Macro Investment Clock project in as a supplementary
US/global context signal (per user decision: absorb src/clock as a PEOS
input source rather than maintaining two disconnected systems).

This reuses src/clock's own growth/inflation momentum model as-is — it is
not re-derived here — and is attached to the macro payload as
`macro.us_investment_clock` context (favored asset class per the
Merrill Lynch clock framework), separate from and complementary to the
Core-10 `us_global` composite indicator in engine/macro/indicators.py.
Failures degrade to None rather than breaking the macro engine run.
"""
from __future__ import annotations

from core.logger import log_event


def get_investment_clock_context() -> dict | None:
    try:
        from src.clock import data_sources as clock_data_sources
        from src.clock.model import read_clock
    except Exception as exc:  # pragma: no cover - import wiring issue, not a data failure
        log_event("us_clock.import_failed", level="warning", error=str(exc))
        return None

    try:
        series = clock_data_sources.fetch_all()
        reading = read_clock(series)
    except Exception as exc:
        log_event("us_clock.fetch_failed", level="warning", error=str(exc))
        return None

    return {
        "phase": reading.phase["name"],
        "phase_kr": reading.phase["name_kr"],
        "favored_asset": reading.phase["asset"],
        "favored_asset_kr": reading.phase["asset_kr"],
        "growth_signal": reading.growth.label,
        "inflation_signal": reading.inflation.label,
        "as_of": max(reading.growth.as_of, reading.inflation.as_of).date().isoformat(),
    }
