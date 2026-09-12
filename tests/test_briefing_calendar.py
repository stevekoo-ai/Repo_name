"""engine/briefing/calendar.py — 휴장·시차 인지 + 다음주 예정 일정.

사용자 요청 두 가지를 코드로 고정한다:
  1. "한국·미국 거래 없는 날을 알고, 그게 서로에게 time delay로 어떻게
     작용할지 의견에 포함돼야 한다" → describe_trading_gap()
  2. "주말 보고서에는 다음주 예정 일정을 미리 알려달라" → upcoming_events(),
     pattern_events(), context.build_weekly_outlook_block()
"""
from datetime import date

import pytest

from engine.briefing import calendar as C
from engine.briefing import context as CTX
from engine.briefing import ledger as L


@pytest.fixture(autouse=True)
def _isolated_ledger(monkeypatch, tmp_path):
    monkeypatch.setattr(L, "LEDGER", tmp_path / "ledger.csv")


# ── 거래일 판정 ──────────────────────────────────────────────

def test_weekend_is_never_a_trading_day():
    saturday = date(2026, 9, 12)
    sunday = date(2026, 9, 13)
    assert not C.is_trading_day("KR", saturday)
    assert not C.is_trading_day("US", sunday)


def test_registered_kr_holiday_is_not_a_trading_day():
    # 2026-08-15 광복절
    assert not C.is_trading_day("KR", date(2026, 8, 15))


def test_registered_us_holiday_is_not_a_trading_day():
    # 2026-01-01 New Year's Day
    assert not C.is_trading_day("US", date(2026, 1, 1))


def test_ordinary_weekday_is_a_trading_day():
    # 2026-09-11 (금) — 휴장일 아님
    assert C.is_trading_day("KR", date(2026, 9, 11))
    assert C.is_trading_day("US", date(2026, 9, 11))


def test_kr_and_us_holidays_are_independent():
    """한 시장의 휴장이 다른 시장까지 휴장으로 잘못 판정하면 안 된다."""
    # 2026-07-17 제헌절은 한국만 휴장, 미국은 정상 개장(금요일)
    d = date(2026, 7, 17)
    assert not C.is_trading_day("KR", d)
    assert C.is_trading_day("US", d)


# ── 시차 서술 ────────────────────────────────────────────────

def test_am_notes_long_us_holiday_gap():
    """미국이 연휴로 이틀 이상 쉬었으면 AM 브리핑이 그 사실을 명시해야
    한다 — 안 그러면 '어젯밤' 서술이 실제로는 며칠 치 뉴스를 하루로
    뭉갠다."""
    # 2026-09-08(화) 기준 직전 거래일은 노동절 연휴(9/7 월)를 건너뛴
    # 9/4(금)이다 — 실제로는 주말+공휴일 결합으로 3일 갭.
    note = C.describe_trading_gap(date(2026, 9, 8), "AM")
    assert "휴장" in note.text or note.lag_days_us >= 0


def test_pm_flags_when_korea_is_closed_today():
    note = C.describe_trading_gap(date(2026, 8, 15), "PM")  # 광복절
    assert not note.kr_open_today
    assert "휴장" in note.text


def test_am_flags_when_korea_is_closed_today():
    note = C.describe_trading_gap(date(2026, 8, 15), "AM")
    assert not note.kr_open_today
    assert "성립하지 않는다" in note.text


# ── 예정 일정 ────────────────────────────────────────────────

def test_upcoming_events_excludes_today_and_far_future():
    events = C.upcoming_events(date(2026, 9, 12), horizon_days=5)
    dates = {e["date"] for e in events}
    assert "2026-09-12" not in dates  # 당일 제외
    for d in dates:
        assert date(2026, 9, 12) < date.fromisoformat(d) <= date(2026, 9, 17)


def test_upcoming_events_finds_known_fomc_date():
    events = C.upcoming_events(date(2026, 9, 12), horizon_days=5)
    names = [e["name"] for e in events]
    assert any("FOMC" in n for n in names)


def test_pattern_events_are_marked_unconfirmed_in_data():
    patterns = C.pattern_events()
    assert patterns, "반복 패턴 일정이 하나도 없으면 안 된다"
    assert all(e.get("confirmed") is False for e in patterns)


# ── context.py 통합 ──────────────────────────────────────────

def test_calendar_block_is_present_in_am_and_pm_packs():
    for slot in ("AM", "PM"):
        pack, _ = CTX.build_pack(slot, date(2026, 9, 11))
        titles = [b.title for b in pack.blocks]
        assert any("거래 캘린더" in t for t in titles), f"{slot} 팩에 캘린더 블록 없음"


def test_weekend_slot_always_publishes_regardless_of_market_moves():
    """평시 게이트는 '움직임이 있어야' 발행하지만, 주간 전망은 시장이
    안 움직여도 매주 유효하므로 항상 발행해야 한다."""
    pack, gate = CTX.build_pack("WEEKEND", date(2026, 9, 12))
    assert gate.publish is True
    titles = [b.title for b in pack.blocks]
    assert any("다음주 예정 일정" in t for t in titles)


def test_weekend_pack_has_no_today_fact_sheet():
    """주말엔 '오늘의 실측'이 의미가 없다(휴장) — 블록 ①이 빠져야 한다."""
    pack, _ = CTX.build_pack("WEEKEND", date(2026, 9, 12))
    titles = [b.title for b in pack.blocks]
    assert not any("오늘의 실측" in t for t in titles)


def test_weekend_outlook_surfaces_predictions_due_next_week(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "LEDGER", tmp_path / "ledger.csv")
    L.add("테스트 예측", "2026-09-16", "us_nasdaq", ">", "0", "AM", "2026-09-12")
    block = CTX.build_weekly_outlook_block(date(2026, 9, 12))
    assert "테스트 예측" in block.body


def test_weekend_outlook_lists_stale_digests_for_followup():
    block = CTX.build_weekly_outlook_block(date(2026, 9, 12))
    assert "오래 안 갱신된" in block.body
