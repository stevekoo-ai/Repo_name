"""거시 수집 신선도 탐지 — "FRED가 늦은 것"과 "우리가 안 걷은 것"의 구분.

## 왜 필요한가

팩 ①의 "⚠️N일 지연"은 **데이터 기준일**이 며칠 전인지만 잰다. 그 지연이
FRED 발표 지연(정상)인지 수집 실패(장애)인지 구분하지 못한다.

2026-09-14에 실제로 후자였다. 거시 수집(cron 22:10 UTC)이 GitHub Actions
큐 대기로 매번 약 2시간 밀려 00:00~00:15 UTC에 끝나는데 AM 브리핑은
(당시) 22:30 UTC에 돌았다. 완충이 20분뿐이라 **브리핑이 늘 먼저 돌아 그날
수집분을 못 썼다** — 9/14 브리핑이 쓴 데이터는 22시간 전 수집분이었고,
그날 수집은 브리핑 1시간 27분 뒤에 끝났다.

이후 수집 20:15 UTC / 브리핑 23:00 UTC(08:00 KST)로 완충을 2h45m으로
벌렸지만, cron 조정은 GitHub 큐 사정이 바뀌면 다시 깨진다. 그래서
**상태를 탐지하는 쪽**을 고정한다 — cron은 보조, 이 테스트가 본선이다.
"""
from datetime import date, datetime, timedelta, timezone

from engine.briefing import context as CTX


def test_freshness_reads_the_actual_collection_timestamp():
    fetched, hours = CTX.collection_freshness()
    assert fetched, "macro-series.csv에서 fetched_at을 읽지 못했다"
    assert hours is not None and hours >= 0


def test_recent_collection_is_not_flagged():
    """매일 경고가 뜨면 경고가 아니게 된다."""
    fetched, _ = CTX.collection_freshness()
    just_now = datetime.fromisoformat(fetched.replace("Z", "+00:00")) + timedelta(hours=1)
    _, hours = CTX.collection_freshness(now=just_now)
    assert hours < CTX.STALE_COLLECTION_HOURS


def test_stale_collection_crosses_the_threshold():
    fetched, _ = CTX.collection_freshness()
    much_later = (datetime.fromisoformat(fetched.replace("Z", "+00:00"))
                  + timedelta(hours=CTX.STALE_COLLECTION_HOURS + 2))
    _, hours = CTX.collection_freshness(now=much_later)
    assert hours >= CTX.STALE_COLLECTION_HOURS


def test_threshold_is_under_a_day():
    """수집은 하루 1회다. 임계가 24시간 이상이면 '하루를 통째로 건너뛴'
    경우에만 뜨게 되어 이번 사고(22시간 지연)를 못 잡는다."""
    assert CTX.STALE_COLLECTION_HOURS < 24


def test_fact_sheet_states_collection_time_either_way(monkeypatch):
    """신선하든 낡았든 **언제 걷은 것인지**는 항상 팩에 있어야 한다."""
    body = CTX.build_fact_sheet(date(2026, 9, 15)).body
    assert "거시 수집" in body


def test_fact_sheet_warns_not_to_trust_the_table_when_collection_is_stale(monkeypatch):
    monkeypatch.setattr(CTX, "collection_freshness",
                        lambda now=None: ("2026-09-14T00:08:55+00:00", 23.0))
    body = CTX.build_fact_sheet(date(2026, 9, 15)).body
    assert "오늘 수집분이 아직 없다" in body
    assert "뉴스로 확인" in body, "표를 믿지 말라는 지시가 없으면 경고가 행동으로 이어지지 않는다"


def test_fact_sheet_stays_quiet_when_collection_is_fresh(monkeypatch):
    monkeypatch.setattr(CTX, "collection_freshness",
                        lambda now=None: ("2026-09-15T00:08:55+00:00", 2.0))
    body = CTX.build_fact_sheet(date(2026, 9, 15)).body
    assert "오늘 수집분이 아직 없다" not in body
    assert "최신" in body
