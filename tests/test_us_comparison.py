"""US Macro Core (engine/macro/indicators_us.py), the shared regime state
machine reused for the US market (engine/macro/regime_us.py), and the
KR-vs-US comparison synthesis (engine/macro/comparison.py) — the "big
picture first" layer the user asked for."""
from __future__ import annotations

import pandas as pd
import pytest

from core.models import DataPoint, DataStatus, Frequency, Metadata
from engine.macro import comparison, regime_us


@pytest.fixture(autouse=True)
def _isolated_storage(tmp_path, monkeypatch):
    import collectors.base as collector_base
    monkeypatch.setattr(collector_base, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(collector_base, "NORMALIZED_DIR", tmp_path / "normalized")

    import core.cache as cache_mod
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / "cache")
    yield


def _monthly_rows(start_year: int, start_month: int, count: int, base: float, step: float) -> list[dict]:
    rows, y, m = [], start_year, start_month
    for i in range(count):
        rows.append({"date": f"{y:04d}-{m:02d}-01", "value": base + step * i})
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return rows


def test_build_us_core_readings_populates_all_eight_indicators(monkeypatch):
    import collectors.base as collector_base
    from engine.macro import indicators_us

    # (base, monthly step) — steps chosen so the 12m/1m derived fields land
    # inside a defined rules.yaml macro_us band (some low-value gaps are
    # unclassified by design, mirroring the same gap in the KR `macro` rules).
    fred_keys = {
        "us_gdp_qoq": (2.8, 0.0), "us_industrial_production": (103.0, 0.103),
        "us_retail_sales": (700000.0, 700.0), "us_cpi": (315.0, 0.525),
        "us_ppi": (245.0, 0.0), "us_unemployment": (4.0, -0.02),
        "us_trade_balance": (-68000.0, 0.0), "us_yield_curve_10y2y": (0.4, 0.0),
    }

    def _fake_fetch_series(key, ttl_seconds=None):
        base, step = fred_keys[key]
        rows = _monthly_rows(2016, 7, 40, base, step)
        collector_base.append_normalized(f"fred_{key}", rows)
        metadata = Metadata(source="FRED", unit="x", frequency=Frequency.MONTHLY,
                             reliability_grade=5, official=True, confidence=90.0)
        return DataPoint(series_id=key, status=DataStatus.OK, value=rows[-1]["value"], metadata=metadata)

    monkeypatch.setattr(indicators_us.fred, "fetch_series", _fake_fetch_series)

    readings = indicators_us.build_us_core_readings()
    assert set(readings) == set(indicators_us.US_CORE_ORDER)
    for key, reading in readings.items():
        assert reading.status == DataStatus.OK, key
        assert reading.score is not None, key


def test_regime_us_downgrade_when_two_or_more_negative_signals(monkeypatch):
    monkeypatch.setattr(regime_us, "_compute_signals_us", lambda readings: {
        "retail_sales_slump": True, "industrial_production_decline_2m": True,
        "cpi_reaccelerating": False, "ppi_sustained_high": False,
        "yield_curve_inversion_deepening": False, "trade_balance_widening": False,
        "gdp_contraction": False, "gdp_negative": False, "retail_sales_negative": False,
        "unemployment_surge": False, "yield_curve_inverted": False, "trade_balance_wide_deficit": False,
        "gdp_strong": False, "retail_sales_strong": False, "industrial_production_strong": False,
        "cpi_stable": False, "ppi_easing": False, "unemployment_improving": False, "yield_curve_steepening": False,
    })
    result = regime_us.determine_regime_us({}, raw_score=2, history=[
        {"macro_us": {"regime": "Expansion", "scores": {"raw_score": 2}}},
    ])
    assert result["transition"] == "downgrade"
    assert result["regime"] == "Late Expansion"


def test_regime_us_history_key_is_independent_of_kr_snapshot():
    # A snapshot with only a KR 'macro' block (no 'macro_us') must not be
    # mistaken for US history — the two markets' regime chains are separate.
    result = regime_us.determine_regime_us({}, raw_score=0, history=[
        {"macro": {"regime": "Recession", "scores": {"raw_score": -8}}},
    ])
    assert result["previous_regime"] != "Recession"


def _macro_block(regime: str, score_band: str, readings: dict, warning: bool = False) -> dict:
    return {"regime": regime, "score_band": score_band, "readings": readings, "warning_active": warning}


def _reading(score: int, value: float = 1.0) -> dict:
    return {"score": score, "value": value}


def test_comparison_flags_sync_when_regimes_and_scores_match():
    kr = _macro_block("Expansion", "expansion", {
        "gdp": _reading(1), "industrial_production": _reading(1), "retail_sales": _reading(1),
        "cpi": _reading(0), "ppi": _reading(0), "unemployment": _reading(1), "current_account": _reading(1),
    })
    us = _macro_block("Expansion", "expansion", {
        "gdp": _reading(1), "industrial_production": _reading(1), "retail_sales": _reading(1),
        "cpi": _reading(0), "ppi": _reading(0), "unemployment": _reading(1), "trade_balance": _reading(1),
    })
    result = comparison.compare_kr_us(kr, us)
    assert result["alignment"] == "sync"
    assert result["cycle_gap"] == 0
    assert all(p["relationship"] == "sync" for p in result["indicator_pairs"] if p["key"] != "current_account")
    assert "같은 단계" in result["narrative"]


def test_comparison_flags_diverging_indicators():
    kr = _macro_block("Recovery", "unbalanced_expansion", {
        "gdp": _reading(-1), "industrial_production": _reading(0), "retail_sales": _reading(0),
        "cpi": _reading(0), "ppi": _reading(0), "unemployment": _reading(0), "current_account": _reading(0),
    })
    us = _macro_block("Expansion", "expansion", {
        "gdp": _reading(1), "industrial_production": _reading(0), "retail_sales": _reading(0),
        "cpi": _reading(0), "ppi": _reading(0), "unemployment": _reading(0), "trade_balance": _reading(0),
    })
    result = comparison.compare_kr_us(kr, us)
    gdp_pair = next(p for p in result["indicator_pairs"] if p["key"] == "gdp")
    assert gdp_pair["relationship"] == "diverge"
    assert result["alignment"] == "kr_behind"  # Recovery is earlier in the cycle than Expansion
