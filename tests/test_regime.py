import pandas as pd
import pytest

from core.models import DataStatus, IndicatorReading
from engine.macro import regime as regime_mod


def _reading(name, score, fields=None, value=1.0):
    return IndicatorReading(name=name, value=value, status=DataStatus.OK, score=score,
                             detail={"fields": fields or {}})


def _base_readings(**overrides):
    readings = {
        "gdp": _reading("gdp", 0, {"qoq": 0.5}),
        "industrial_production": _reading("industrial_production", 0, {"mom": 0.0}),
        "retail_sales": _reading("retail_sales", 0, {"mom": 0.0}),
        "exports": _reading("exports", 0, {"yoy": 5.0}),
        "semiconductor_exports": _reading("semiconductor_exports", 0, {"yoy": 10.0}),
        "current_account": _reading("current_account", 0, {"avg_3m": 10.0}),
        "cpi": _reading("cpi", 0, {"yoy": 2.0}),
        "ppi": _reading("ppi", 0, {"yoy": 2.0}),
        "unemployment": _reading("unemployment", 0, {"avg_3m_change": 0.0}),
        "us_global": _reading("us_global", 0, value=0.0),
    }
    readings.update(overrides)
    return readings


def test_downgrade_when_two_or_more_negative_signals(monkeypatch):
    monkeypatch.setattr(regime_mod, "_compute_signals", lambda readings: {
        "export_slump": True, "semiconductor_export_slump": True,
        "industrial_production_decline_2m": False, "cpi_reaccelerating": False,
        "ppi_sustained_high": False, "fx_surge": False, "rates_rising": False,
        "exports_negative": False, "semiconductor_exports_negative": False,
        "unemployment_surge": False, "current_account_deficit": False,
        "us_employment_cooling": False, "yield_curve_inversion_deepening": False,
        "gdp_strong": False, "exports_strong": False, "semiconductor_strong": False,
        "cpi_stable": False, "ppi_easing": False, "rates_easing": False, "us_employment_improving": False,
    })
    result = regime_mod.determine_regime(_base_readings(), raw_score=2, history=[
        {"macro": {"regime": "Expansion", "scores": {"raw_score": 2}}},
    ])
    assert result["transition"] == "downgrade"
    assert result["regime"] == "Late Expansion"  # Expansion -> next stage in the cycle


def test_upgrade_when_three_or_more_positive_signals(monkeypatch):
    monkeypatch.setattr(regime_mod, "_compute_signals", lambda readings: {
        "gdp_strong": True, "exports_strong": True, "semiconductor_strong": True,
        "cpi_stable": False, "ppi_easing": False, "rates_easing": False, "us_employment_improving": False,
        "export_slump": False, "semiconductor_export_slump": False, "industrial_production_decline_2m": False,
        "cpi_reaccelerating": False, "ppi_sustained_high": False, "fx_surge": False, "rates_rising": False,
        "exports_negative": False, "semiconductor_exports_negative": False, "unemployment_surge": False,
        "current_account_deficit": False, "us_employment_cooling": False, "yield_curve_inversion_deepening": False,
    })
    result = regime_mod.determine_regime(_base_readings(), raw_score=5, history=[
        {"macro": {"regime": "Expansion", "scores": {"raw_score": 3}}},
    ])
    assert result["transition"] == "upgrade"
    assert result["regime"] == "Early Expansion"  # Expansion -> previous stage (upgraded/promoted)


def test_warning_flag_needs_only_one_signal(monkeypatch):
    monkeypatch.setattr(regime_mod, "_compute_signals", lambda readings: {
        "exports_negative": True, "semiconductor_exports_negative": False, "unemployment_surge": False,
        "current_account_deficit": False, "us_employment_cooling": False, "yield_curve_inversion_deepening": False,
        "export_slump": False, "semiconductor_export_slump": False, "industrial_production_decline_2m": False,
        "cpi_reaccelerating": False, "ppi_sustained_high": False, "fx_surge": False, "rates_rising": False,
        "gdp_strong": False, "exports_strong": False, "semiconductor_strong": False,
        "cpi_stable": False, "ppi_easing": False, "rates_easing": False, "us_employment_improving": False,
    })
    result = regime_mod.determine_regime(_base_readings(), raw_score=1, history=[])
    assert result["warning_active"] is True
    assert "수출 감소 전환" in result["warnings_kr"]


def test_no_signals_holds_regime_steady(monkeypatch):
    monkeypatch.setattr(regime_mod, "_compute_signals", lambda readings: {k: False for k in [
        "export_slump", "semiconductor_export_slump", "industrial_production_decline_2m",
        "cpi_reaccelerating", "ppi_sustained_high", "fx_surge", "rates_rising",
        "exports_negative", "semiconductor_exports_negative", "unemployment_surge",
        "current_account_deficit", "us_employment_cooling", "yield_curve_inversion_deepening",
        "gdp_strong", "exports_strong", "semiconductor_strong", "cpi_stable", "ppi_easing",
        "rates_easing", "us_employment_improving",
    ]})
    result = regime_mod.determine_regime(_base_readings(), raw_score=1, history=[
        {"macro": {"regime": "Early Expansion", "scores": {"raw_score": 1}}},
    ])
    assert result["transition"] is None
    assert result["regime"] == "Early Expansion"


def test_export_slump_signal_from_normalized_series(monkeypatch):
    """21.4 case 2 ingredient: a sharp MoM drop in export YoY growth trips export_slump."""
    def fake_read_normalized(series_id):
        if series_id == "motie_total_exports_yoy":
            return pd.DataFrame({"date": ["2026-05-01", "2026-06-01"], "value": [15.0, 2.0]})
        return pd.DataFrame(columns=["date", "value"])

    import collectors.base as collector_base
    monkeypatch.setattr(collector_base, "read_normalized", fake_read_normalized)

    signals = regime_mod._compute_signals(_base_readings(exports=_reading("exports", -1, {"yoy": 2.0})))
    assert signals["export_slump"] is True
