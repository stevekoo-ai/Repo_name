"""⑪ 경기·신용 경보 판정(2026-10-20)."""
from __future__ import annotations

from datetime import date

from engine.briefing import macro_watch as MW

LEAD = [("2026-06-01", 103.8), ("2026-07-01", 104.3), ("2026-08-01", 104.2)]
HY = [("2026-07-16", 2.73), ("2026-10-16", 3.31)]


def _state(res, wid):
    return next(r for r in res if r["id"] == wid)["state"]


def test_one_month_decline_is_yellow_and_two_is_red():
    res = MW.evaluate(date(2026, 10, 20), {"kr_leading_cycle": LEAD, "us_hy_oas": HY})
    assert _state(res, "W1").startswith("🟡")          # 8월 1개월 하락, 80일 전 자료는 정상 지연
    res = MW.evaluate(date(2026, 11, 2), {"kr_leading_cycle": LEAD + [("2026-09-01", 104.0)], "us_hy_oas": HY})
    assert _state(res, "W1").startswith("🔴")


def test_hy_threshold_and_stale_data_is_not_safe():
    res = MW.evaluate(date(2026, 10, 20), {"us_hy_oas": HY + [("2026-10-19", 3.6)]})
    assert _state(res, "W2").startswith("🔴")
    res = MW.evaluate(date(2026, 12, 1), {"us_hy_oas": HY})
    assert _state(res, "W2") == "판단 불가"               # 오래된 값은 '안전'이 아니다(R3)
    assert _state(res, "W1") == "판단 불가"               # 데이터 없음


def test_both_lit_message():
    res = MW.evaluate(date(2026, 11, 2), {"kr_leading_cycle": LEAD + [("2026-09-01", 104.0)],
                                          "us_hy_oas": HY + [("2026-10-30", 3.7)]})
    assert "경보 2개 이상 점등" in MW.render_markdown(res)


def test_triple_weakness_needs_all_three_legs(monkeypatch):
    from engine.briefing import sentiment as S
    monkeypatch.setattr(S, "_daily_price", lambda code: [("2026-09-18", 7000.0), ("2026-10-20", 5600.0)])
    m = {"kr_treasury_10y": [("2026-09-18", 4.0), ("2026-10-20", 4.3)],
         "kr_usdkrw": [("2026-09-18", 1350.0), ("2026-10-20", 1390.0)]}
    assert MW._triple(date(2026, 10, 21), m)["state"].startswith("🔴")
    m["kr_usdkrw"] = [("2026-09-18", 1380.0), ("2026-10-20", 1332.0)]     # 원화 강세면 3/3 아님
    assert MW._triple(date(2026, 10, 21), m)["state"] == "🟡 2/3"
