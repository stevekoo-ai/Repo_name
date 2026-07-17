"""Pure-function tests for the MOLIT real-estate collector and trend engine —
no network calls (those paths are exercised end-to-end only in CI with a real
MOLIT_API_KEY)."""
from __future__ import annotations

from collectors import molit
from engine.real_estate import market_trend


def test_seoul_districts_count():
    assert len(molit.SEOUL_DISTRICTS) == 25
    assert len({r["code"] for r in molit.SEOUL_DISTRICTS}) == 25  # no duplicate codes


def test_region_tiers_nest_correctly():
    seoul_codes = {r["code"] for r in molit.REGION_TIERS["seoul"]}
    capital_codes = {r["code"] for r in molit.REGION_TIERS["capital_area"]}
    nationwide_codes = {r["code"] for r in molit.REGION_TIERS["nationwide"]}
    assert seoul_codes.issubset(capital_codes)
    assert capital_codes.issubset(nationwide_codes)


def test_highlight_region_is_yongin_giheung():
    assert molit.HIGHLIGHT_REGION["name"] == "용인 기흥구"
    assert molit.HIGHLIGHT_REGION["code"] == "41463"


def test_price_per_pyeong_parses_comma_formatted_amount():
    row = {"dealAmount": "85,000", "excluUseAr": "84.96"}
    price = molit._price_per_pyeong(row)
    assert price is not None
    assert price == (85_000 * 10_000) / (84.96 / 3.3058)


def test_price_per_pyeong_handles_missing_fields():
    assert molit._price_per_pyeong({}) is None
    assert molit._price_per_pyeong({"dealAmount": "1,000", "excluUseAr": "0"}) is None


def test_trailing_deal_months_length_and_order():
    months = molit._trailing_deal_months(3)
    assert len(months) == 3
    assert months == sorted(months)  # oldest first
    assert all(len(m) == 6 for m in months)


def test_pct_change_basic():
    assert market_trend._pct_change(110, 100) == 10.0
    assert market_trend._pct_change(90, 100) == -10.0
    assert market_trend._pct_change(100, None) is None
    assert market_trend._pct_change(100, 0) is None


def test_market_heat_bands():
    assert market_trend._market_heat(None, None) == "데이터 부족"
    assert market_trend._market_heat(1.5, 5.0) == "과열"
    assert market_trend._market_heat(-1.5, None) == "냉각"
    assert market_trend._market_heat(0.2, -2.0) == "보합"
