"""Core-10 indicator layer (Master Instruction 9, 11.3-11.4).

Turns raw collector output into the computed fields each rule needs
(QoQ/YoY/MoM/3M-avg/composite), then scores each indicator through the
generic rule engine. This is the only place that knows how to go from
"a normalized series" to "the field a rule.yaml threshold checks" —
Macro Engine scoring (engine/macro/score.py) just consumes the result.
"""
from __future__ import annotations

from collectors import base as collector_base
from collectors import ecos, fred, kosis, manual
from core.config import rules_config
from core.models import DataPoint, DataStatus, IndicatorReading
from core.utils import compute_trend, moving_average
from engine.rule.engine import evaluate_indicator_rule

CORE10_ORDER = [
    "gdp", "industrial_production", "retail_sales", "exports",
    "semiconductor_exports", "current_account", "cpi", "ppi",
    "unemployment", "us_global",
]


def _series_trend_change(series_id: str, window: str) -> float | None:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return None
    points = collector_base.as_date_value_tuples(df)
    trends = compute_trend(points)
    tp = trends.get(window)
    return tp.change if tp else None


def _series_moving_average(series_id: str, periods: int, offset: int = 0) -> float | None:
    df = collector_base.read_normalized(series_id)
    if df.empty:
        return None
    values = df.sort_values("date")["value"].tolist()
    if offset:
        values = values[: len(values) - offset] if offset < len(values) else []
    return moving_average(values, periods)


def _build_us_global_composite() -> tuple[float | None, dict]:
    """11.4 (10): NFP trend + unemployment trend + OECD CLI/industrial-production trend -> [-1, 1]."""
    detail: dict[str, int] = {}
    signals: list[int] = []

    payroll_change = _series_trend_change("fred_us_nonfarm_payroll", "3m")
    if payroll_change is not None:
        s = 1 if payroll_change > 0 else (-1 if payroll_change < 0 else 0)
        signals.append(s)
        detail["payroll_signal"] = s

    unemployment_change = _series_trend_change("fred_us_unemployment", "3m")
    if unemployment_change is not None:
        s = 1 if unemployment_change < 0 else (-1 if unemployment_change > 0 else 0)
        signals.append(s)
        detail["unemployment_signal"] = s

    cli_change = _series_trend_change("fred_us_oecd_cli", "3m")
    if cli_change is None:
        cli_change = _series_trend_change("fred_us_industrial_production", "3m")
    if cli_change is not None:
        s = 1 if cli_change > 0 else (-1 if cli_change < 0 else 0)
        signals.append(s)
        detail["global_growth_signal"] = s

    if not signals:
        return None, detail
    return sum(signals) / len(signals), detail


def _score_indicator(key: str, rule_spec: dict, fields: dict, dp: DataPoint) -> IndicatorReading:
    reading = IndicatorReading(
        name=key, value=dp.value, status=dp.status, weight=rule_spec["weight"],
        label=rule_spec["label"], source=dp.metadata.source if dp.metadata else None,
        reference_date=dp.metadata.reference_date if dp.metadata else None,
        detail={"fields": fields, "note": dp.note},
    )
    if dp.status == DataStatus.OK:
        outcome = evaluate_indicator_rule(key, rule_spec, fields)
        reading.score = outcome.score
        reading.detail["rule_outcome"] = {
            "matched_band": outcome.matched_band,
            "field_used": outcome.field_used,
            "value_used": outcome.value_used,
        }
    return reading


def build_core10_readings() -> dict[str, IndicatorReading]:
    """Collect + compute + score all 10 core macro indicators (11.3)."""
    rules = rules_config()["macro"]
    readings: dict[str, IndicatorReading] = {}

    dp = ecos.fetch_series("gdp_growth_qoq")
    readings["gdp"] = _score_indicator("gdp", rules["gdp"], {"qoq": dp.value}, dp)

    dp = kosis.fetch_series("industrial_production_index")
    mom = _series_trend_change("kosis_industrial_production_index", "1m")
    readings["industrial_production"] = _score_indicator(
        "industrial_production", rules["industrial_production"], {"mom": mom}, dp
    )

    dp = kosis.fetch_series("retail_sales_index")
    mom = _series_trend_change("kosis_retail_sales_index", "1m")
    readings["retail_sales"] = _score_indicator("retail_sales", rules["retail_sales"], {"mom": mom}, dp)

    exports_points = manual.fetch_exports()
    exp_dp = exports_points["total_exports_yoy"]
    readings["exports"] = _score_indicator("exports", rules["exports"], {"yoy": exp_dp.value}, exp_dp)

    semi_dp = exports_points["semiconductor_exports_yoy"]
    readings["semiconductor_exports"] = _score_indicator(
        "semiconductor_exports", rules["semiconductor_exports"], {"yoy": semi_dp.value}, semi_dp
    )

    dp = ecos.fetch_series("current_account")
    avg3 = _series_moving_average("ecos_current_account", 3)
    readings["current_account"] = _score_indicator("current_account", rules["current_account"], {"avg_3m": avg3}, dp)

    dp = kosis.fetch_series("cpi_index")
    yoy = _series_trend_change("kosis_cpi_index", "12m")
    readings["cpi"] = _score_indicator("cpi", rules["cpi"], {"yoy": yoy}, dp)

    dp = ecos.fetch_series("ppi_yoy_level")
    yoy = _series_trend_change("ecos_ppi_yoy_level", "12m")
    readings["ppi"] = _score_indicator("ppi", rules["ppi"], {"yoy": yoy}, dp)

    dp = kosis.fetch_series("unemployment_rate")
    avg_now = _series_moving_average("kosis_unemployment_rate", 3)
    avg_prior = _series_moving_average("kosis_unemployment_rate", 3, offset=3)
    avg_change = (avg_now - avg_prior) if (avg_now is not None and avg_prior is not None) else None
    readings["unemployment"] = _score_indicator("unemployment", rules["unemployment"], {"avg_3m_change": avg_change}, dp)

    # Supporting series for regime-signal detection (engine/macro/regime.py) and the
    # Bond/FX personal engines — not Core-10 indicators themselves, but must be
    # populated here so they're on disk before regime detection runs this same pass.
    ecos.fetch_series("usdkrw")
    ecos.fetch_series("kr_3y_yield")
    ecos.fetch_series("base_rate")

    fred.fetch_all()
    composite, detail = _build_us_global_composite()
    us_reading = IndicatorReading(
        name="us_global", value=composite,
        status=DataStatus.OK if composite is not None else DataStatus.PENDING,
        weight=rules["us_global"]["weight"], label=rules["us_global"]["label"],
        source="FRED", detail=detail,
    )
    if composite is not None:
        outcome = evaluate_indicator_rule("us_global", rules["us_global"], {"composite": composite})
        us_reading.score = outcome.score
    readings["us_global"] = us_reading

    return readings
