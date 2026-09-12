"""거래 캘린더 — 휴장·시차 인지 + 다음주 예정 일정.

## 왜 이게 필요한가

사용자 지적: "한국과 미국에 거래가 없는 날을 잘 알고, 그것이 두 시장에
서로 어떤 time delay로 작용할지가 의견에 포함돼야 한다." 그리고
"주말 보고서에는 다음주 예정된 일정을 미리 알려달라."

기존 팩(context.py)은 데이터의 **기준일**(⚠️N일 지연)만 알고, 그 지연이
**휴장 때문인지 단순 수집 지연인지**를 구분하지 못했다. 이 모듈이 그
구분을 코드로 만든다 — LLM이 "왜 이 숫자가 오래됐는지" 추측하지 않고
읽게 하기 위해서다(R1: 측정 > 추론).

## 두 데이터 등급

- `market_holidays_2026.yaml` — 확정된 휴장일. 매년 갱신 필요.
- `economic_calendar_2026.yaml` — `confirmed: true`(발표된 일정)와
  `confirmed: false`(과거 패턴 추정치)를 섞는다. 렌더링 시 후자엔 항상
  "(추정)"을 붙인다 — 추정을 확정처럼 쓰면 R1 위반이다.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
_HOLIDAY_FILE = REPO / "data" / "manual_inputs" / "market_holidays_2026.yaml"
_CALENDAR_FILE = REPO / "data" / "manual_inputs" / "economic_calendar_2026.yaml"
_HISTORY_FILE = REPO / "data" / "manual_inputs" / "event_historical_reactions.yaml"


def _load_holidays() -> dict[str, set[str]]:
    if not _HOLIDAY_FILE.exists():
        return {"KR": set(), "US": set()}
    doc = yaml.safe_load(_HOLIDAY_FILE.read_text(encoding="utf-8")) or {}
    return {
        "KR": {r["date"] for r in doc.get("KR", [])},
        "US": {r["date"] for r in doc.get("US", [])},
    }


def _load_events() -> list[dict]:
    if not _CALENDAR_FILE.exists():
        return []
    doc = yaml.safe_load(_CALENDAR_FILE.read_text(encoding="utf-8")) or {}
    return doc.get("events", [])


def is_trading_day(market: str, d: date) -> bool:
    """market: 'KR' | 'US'. 주말이거나 등록된 휴장일이면 False."""
    if d.weekday() >= 5:  # 5=토, 6=일
        return False
    holidays = _load_holidays()
    return d.isoformat() not in holidays.get(market, set())


def last_trading_day(market: str, before: date) -> date:
    """`before` 이전(당일 포함하지 않음) 가장 최근 거래일."""
    d = before - timedelta(days=1)
    for _ in range(14):
        if is_trading_day(market, d):
            return d
        d -= timedelta(days=1)
    return d  # 14일 넘게 못 찾으면(있을 수 없음) 그냥 반환


@dataclass
class TradingGapNote:
    kr_open_today: bool
    us_open_last_session: bool
    kr_last_trading: date
    us_last_trading: date
    lag_days_kr: int          # 오늘까지 한국 시장이 쉰 연속일
    lag_days_us: int
    text: str


def describe_trading_gap(as_of: date, slot: str) -> TradingGapNote:
    """오늘(as_of) 기준 두 시장의 개장 여부와 그 사이 시차를 서술한다.

    AM 슬롯: "밤사이 미국"을 다루므로 미국의 직전 거래일이 언제였는지가
    핵심(연휴로 이틀 이상 쉬었으면 그 기간 뉴스가 한꺼번에 반영된다).
    PM 슬롯: "오늘 한국"을 다루므로 한국이 오늘 열렸는지가 핵심.
    """
    kr_open = is_trading_day("KR", as_of)
    us_last = last_trading_day("US", as_of + timedelta(days=1))  # "어젯밤까지" 포함
    kr_last = last_trading_day("KR", as_of + timedelta(days=1)) if not kr_open else as_of

    us_gap = (as_of - us_last).days - 1  # 미국이 쉰 날 수(당일 제외 개념 보정)
    kr_gap = 0
    d = as_of - timedelta(days=1)
    while not is_trading_day("KR", d) and (as_of - d).days < 10:
        kr_gap += 1
        d -= timedelta(days=1)

    lines = []
    if slot == "AM":
        if us_gap >= 2:
            lines.append(f"⚠️ **미국 시장이 {us_gap}일 연속 휴장 후 재개**됐다"
                         f"(직전 거래일 {us_last.isoformat()}). "
                         "그 기간 쌓인 뉴스·이벤트가 하루치처럼 한꺼번에 가격에 반영됐을 수 있다 — "
                         "'하루 동안 무슨 일이'가 아니라 '휴장 동안 무슨 일이'로 조사할 것.")
        else:
            lines.append(f"미국 직전 거래일: {us_last.isoformat()} (정상 시차).")
        if not kr_open:
            lines.append(f"⚠️ **오늘(한국) 휴장이다.** 오늘 한국장 전망은 성립하지 않는다 — "
                         f"다음 개장일까지 누적해서 볼 것.")
    else:  # PM
        if not kr_open:
            lines.append("⚠️ **오늘(한국) 휴장이다.** 이 브리핑은 발행하지 않는 것이 맞다.")
        elif kr_gap >= 1:
            lines.append(f"오늘 한국장은 {kr_gap}일 휴장 뒤 재개였다 — "
                         "휴장 중 미국·환율 변동이 오늘 하루에 누적 반영됐을 수 있다.")
        else:
            lines.append("한국 정상 개장일.")
        us_open_tonight = is_trading_day("US", as_of)
        if not us_open_tonight:
            lines.append("⚠️ **오늘 밤 미국은 휴장이다.** '오늘 밤 미국장 전망'은 성립하지 않는다.")

    return TradingGapNote(
        kr_open_today=kr_open,
        us_open_last_session=True,
        kr_last_trading=kr_last,
        us_last_trading=us_last,
        lag_days_kr=kr_gap,
        lag_days_us=max(us_gap, 0),
        text="\n".join(f"- {ln}" for ln in lines),
    )


def upcoming_events(as_of: date, horizon_days: int = 7) -> list[dict]:
    """as_of 이후 horizon_days일 이내(당일 제외) 확정 일정만.

    패턴형(INDICATOR_PATTERN, 날짜가 'YYYY-MM-DD' 형식이 아님)은 별도로
    다뤄야 하므로 여기서는 제외한다 — `pattern_events()` 참고."""
    end = as_of + timedelta(days=horizon_days)
    out = []
    for ev in _load_events():
        try:
            d = date.fromisoformat(ev["date"])
        except (ValueError, KeyError):
            continue
        if as_of < d <= end:
            out.append(ev)
    out.sort(key=lambda e: e["date"])
    return out


def pattern_events() -> list[dict]:
    """날짜가 확정이 아니라 반복 패턴으로 적힌 항목(비농업고용 등)."""
    return [ev for ev in _load_events() if ev.get("type") == "INDICATOR_PATTERN"]


def historical_analog(event_type: str) -> dict | None:
    """이벤트 유형(FOMC/BOK/ELECTION/EARNINGS)의 과거 유사 사례 비교 노트.

    ⚠️ 회차별 정밀 수치가 아니라 위키에 이미 기록된 실제 사건에서 뽑은
    **정성적 패턴**이다(이 저장소는 "이번 FOMC 때 KOSPI가 몇 % 움직였다"는
    회차별 로그를 자동 수집하지 않는다). `confirmed`는 항상 False로
    고정돼 있고, 호출부가 이걸 확정 예측처럼 쓰면 안 된다(R1)."""
    if not _HISTORY_FILE.exists():
        return None
    doc = yaml.safe_load(_HISTORY_FILE.read_text(encoding="utf-8")) or {}
    return doc.get("patterns", {}).get(event_type)
