"""US Macro Core indicator layer — the "big picture" the KR Core-10
(engine/macro/indicators.py) is read against, per the user's explicit
request: judge the US regime first, then see whether Korea is riding that
wave or diverging from it, before drawing personal conclusions.

Reuses indicators.py's generic helpers (score_indicator/series_trend_change
/series_moving_average operate on any normalized series id — nothing about
them is KR-specific) and collectors/fred.py, which has never failed in any
observed run, unlike ECOS/KOSIS.
"""
from __future__ import annotations

from collectors import fred
from core.config import rules_config
from core.models import IndicatorReading
from . import indicators as kr_indicators

US_CORE_ORDER = [
    "gdp", "industrial_production", "retail_sales", "cpi", "ppi",
    "unemployment", "trade_balance", "yield_curve",
]


def build_us_core_readings() -> dict[str, IndicatorReading]:
    """Collect + compute + score the US Core Macro set (mirrors
    build_core10_readings()'s shape, one market at a time)."""
    rules = rules_config()["macro_us"]
    readings: dict[str, IndicatorReading] = {}

    dp = fred.fetch_series("us_gdp_qoq")
    readings["gdp"] = kr_indicators.score_indicator("gdp", rules["gdp"], {"qoq": dp.value}, dp)

    dp = fred.fetch_series("us_industrial_production")
    mom = kr_indicators.series_trend_change("fred_us_industrial_production", "1m")
    readings["industrial_production"] = kr_indicators.score_indicator(
        "industrial_production", rules["industrial_production"], {"mom": mom}, dp
    )

    dp = fred.fetch_series("us_retail_sales")
    mom = kr_indicators.series_trend_change("fred_us_retail_sales", "1m")
    readings["retail_sales"] = kr_indicators.score_indicator("retail_sales", rules["retail_sales"], {"mom": mom}, dp)

    dp = fred.fetch_series("us_cpi")
    yoy = kr_indicators.series_trend_change("fred_us_cpi", "12m")
    readings["cpi"] = kr_indicators.score_indicator("cpi", rules["cpi"], {"yoy": yoy}, dp)

    dp = fred.fetch_series("us_ppi")
    yoy = kr_indicators.series_trend_change("fred_us_ppi", "12m")
    readings["ppi"] = kr_indicators.score_indicator("ppi", rules["ppi"], {"yoy": yoy}, dp)

    dp = fred.fetch_series("us_unemployment")
    avg_now = kr_indicators.series_moving_average("fred_us_unemployment", 3)
    avg_prior = kr_indicators.series_moving_average("fred_us_unemployment", 3, offset=3)
    avg_change = (avg_now - avg_prior) if (avg_now is not None and avg_prior is not None) else None
    readings["unemployment"] = kr_indicators.score_indicator(
        "unemployment", rules["unemployment"], {"avg_3m_change": avg_change}, dp
    )

    dp = fred.fetch_series("us_trade_balance")
    avg3 = kr_indicators.series_moving_average("fred_us_trade_balance", 3)
    readings["trade_balance"] = kr_indicators.score_indicator(
        "trade_balance", rules["trade_balance"], {"avg_3m": avg3}, dp
    )

    dp = fred.fetch_series("us_yield_curve_10y2y")
    readings["yield_curve"] = kr_indicators.score_indicator(
        "yield_curve", rules["yield_curve"], {"spread": dp.value}, dp
    )

    return readings
