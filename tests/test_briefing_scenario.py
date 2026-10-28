"""⑫ 시나리오 점검(2026-10-28)."""
from __future__ import annotations

from datetime import date

from engine.briefing import scenario as SC

D = date(2026, 10, 29)
M = {"us_10y_yf": [("2026-10-28", 5.04)], "us_brent_futures": [("2026-10-28", 110.7)],
     "us_vix_yf": [("2026-10-28", 16.9)]}
CLOSES = [("2026-10-26", 1275000.0), ("2026-10-27", 1341000.0), ("2026-10-28", 1487000.0)]
FLOWS = [("2026-10-23", -5.7e11), ("2026-10-26", -4.0e11), ("2026-10-27", -0.7e11)]
BREADTH = [("2026-10-23", 173, 719), ("2026-10-26", 114, 778), ("2026-10-27", 700, 150)]


def test_today_is_between_s1_and_s2():
    r = SC.evaluate(D, M, CLOSES, FLOWS, BREADTH, [])
    assert r["dominant"] == "S1/S2"
    assert "T1 13주" in r["action"]


def test_floor_break_is_s3_and_overrides_s1():
    m = dict(M, us_10y_yf=[("2026-10-28", 4.7)], us_brent_futures=[("2026-10-28", 95.0)])
    closes = CLOSES + [("2026-10-29", 1330000.0)]
    r = SC.evaluate(D, m, closes, FLOWS, BREADTH, [])
    assert r["dominant"] == "S3"            # S1 신호 2개여도 꺾임 신호가 우선
    assert "즉시 매도" in r["action"]


def test_trailing_stop_from_post_deferral_peak():
    closes = CLOSES + [("2026-10-29", 1600000.0), ("2026-10-30", 1470000.0)]   # 1.6M × 0.92 = 1,472,000
    r = SC.evaluate(date(2026, 10, 30), M, closes, FLOWS, BREADTH, [])
    assert r["dominant"] == "S3"


def test_macro_shock_has_top_priority():
    m = dict(M, us_vix_yf=[("2026-10-28", 31.0)])
    closes = CLOSES + [("2026-10-29", 1330000.0)]
    assert SC.evaluate(D, m, closes, FLOWS, BREADTH, [])["dominant"] == "S4"


def test_two_s1_signals_make_s1():
    m = dict(M, us_10y_yf=[("2026-10-28", 4.75)], us_brent_futures=[("2026-10-28", 98.0)])
    assert SC.evaluate(D, m, CLOSES, FLOWS, BREADTH, [])["dominant"] == "S1"


def test_missing_data_is_unknown_not_safe():
    r = SC.evaluate(D, {}, [], [], [], [])
    assert r["unknown"] >= 5
    assert "판단 불가" in SC.render_markdown(r)
