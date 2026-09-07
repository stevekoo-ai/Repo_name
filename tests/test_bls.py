"""US BLS collector (collectors/bls.py).

2026-09-07 신설. BLS_API_KEY는 두 워크플로에 주입되고 config에도 등록돼
있었지만 이를 쓰는 코드가 저장소에 없었다 — API 전수 프로브에서 발견해
채운 모듈의 테스트.
"""
from __future__ import annotations

import pytest

from collectors import bls


def test_m13_annual_average_is_excluded_from_the_monthly_series():
    """BLS의 period "M13"은 월이 아니라 **연평균**이다. 안 거르면 매년 12월
    뒤에 13번째 포인트가 끼어 시계열이 오염된다 — 이 모듈에서 가장 쉽게
    놓치는 함정이라 테스트로 고정한다."""
    assert bls._period_to_date("2026", "M07") is not None
    assert bls._period_to_date("2026", "M13") is None
    assert bls._period_to_date("2026", "A01") is None   # 연간 시리즈 표기
    assert bls._period_to_date("2026", "Q01") is None   # 분기 표기
    assert bls._period_to_date("", "M01") is None       # 빈 연도


def test_period_to_date_maps_month_to_first_of_month():
    assert bls._period_to_date("2024", "M01").isoformat() == "2024-01-01"
    assert bls._period_to_date("2024", "M12").isoformat() == "2024-12-01"


def _payload(series_id: str, data: list[dict]) -> dict:
    return {"status": "REQUEST_SUCCEEDED",
            "Results": {"series": [{"seriesID": series_id, "data": data}]}}


def test_rows_are_sorted_oldest_first_even_though_bls_returns_newest_first():
    """BLS는 최신순으로 주는데 이 저장소의 normalized CSV는 날짜 오름차순이
    관례다. 정렬을 안 하면 append_normalized가 뒤집힌 순서를 그대로 쌓는다."""
    payload = _payload("CUUR0000SA0", [
        {"year": "2026", "period": "M03", "value": "333.9"},
        {"year": "2026", "period": "M02", "value": "332.1"},
        {"year": "2026", "period": "M01", "value": "331.0"},
    ])
    rows = bls._rows_for(payload, "CUUR0000SA0")
    assert [r["date"] for r in rows] == ["2026-01-01", "2026-02-01", "2026-03-01"]
    assert rows[-1]["value"] == 333.9


def test_annual_average_row_does_not_reach_the_normalized_rows():
    payload = _payload("CUUR0000SA0", [
        {"year": "2025", "period": "M13", "value": "999.9"},   # 연평균 — 버려져야 함
        {"year": "2025", "period": "M12", "value": "330.0"},
    ])
    rows = bls._rows_for(payload, "CUUR0000SA0")
    assert len(rows) == 1
    assert rows[0]["value"] == 330.0


def test_non_numeric_values_are_skipped_not_crashed_on():
    """BLS는 미발표/정정 중인 값에 빈 문자열이나 '-'를 넣어 보내는 경우가 있다."""
    payload = _payload("LNS14000000", [
        {"year": "2026", "period": "M02", "value": ""},
        {"year": "2026", "period": "M01", "value": "4.1"},
    ])
    rows = bls._rows_for(payload, "LNS14000000")
    assert rows == [{"date": "2026-01-01", "value": 4.1}]


def test_unknown_series_id_returns_empty_not_another_series_data():
    """여러 series를 한 번에 받으므로, 요청한 id와 다른 series의 데이터를
    잘못 집어오면 지표가 통째로 뒤바뀐다."""
    payload = _payload("CUUR0000SA0", [{"year": "2026", "period": "M01", "value": "1.0"}])
    assert bls._rows_for(payload, "LNS14000000") == []


def test_failed_status_raises_instead_of_silently_returning_nothing(monkeypatch):
    """BLS는 한도 초과·잘못된 series_id를 200 OK에 실어 보낸다. status를 안 보면
    조용히 빈 결과가 되어 흘러간다 — 이 저장소가 이번에 MOLIT에서 겪은 것과
    같은 종류의 조용한 실패."""
    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return {"status": "REQUEST_NOT_PROCESSED",
                    "message": ["daily threshold reached"]}

    monkeypatch.setattr(bls.requests, "post", lambda *a, **k: _Resp())
    with pytest.raises(RuntimeError, match="daily threshold"):
        bls._fetch_raw(["CUUR0000SA0"], None)


def test_key_is_optional_because_v2_works_keyless(monkeypatch):
    """키가 없어도 PENDING으로 죽지 않고 실제로 호출해야 한다 — v2는 키리스로
    동작하고(일 25회), 2026-09-07 프로브에서 키 없이 수신 확인됐다."""
    captured = {}

    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return _payload("CUUR0000SA0", [{"year": "2026", "period": "M01", "value": "1.0"}])

    def _post(url, json=None, timeout=None):
        captured["body"] = json
        return _Resp()

    monkeypatch.setattr(bls.requests, "post", _post)
    bls._fetch_raw(["CUUR0000SA0"], None)
    assert "registrationkey" not in captured["body"]

    bls._fetch_raw(["CUUR0000SA0"], "somekey")
    assert captured["body"]["registrationkey"] == "somekey"


def test_series_catalog_has_no_duplicate_bls_ids():
    """같은 series_id를 두 key에 매핑하면 한 번에 받아 나눠 담을 때 헷갈린다."""
    ids = [sid for sid, _, _ in bls.BLS_SERIES.values()]
    assert len(ids) == len(set(ids))


def test_requested_year_span_stays_within_the_keyless_ten_year_limit():
    """BLS v2의 연도 범위 한도는 **포함 연수**로 센다(키 없이 10년). 초과하면
    BLS는 에러를 내지 않고 **조용히 앞 10년만 주면서 최신 연도를 버린다**.

    2026-09-07 첫 수집에서 실제로 그랬다: startyear=올해-10 이라 11년을
    요청했고, 8개 시리즈가 전부 2016-01~2025-12(정확히 120개월)에서 멈췄다.
    같은 날 프로브는 CPI가 2026-07까지 있음을 확인해줬으니, 최신 9개월치를
    아무 경고 없이 잃고 있었던 것이다."""
    from datetime import datetime

    this_year = datetime.utcnow().year
    start_year = this_year - bls._HISTORY_YEARS
    span = this_year - start_year + 1     # 포함 연수
    assert span <= 10, (
        f"요청 범위가 {span}년이라 키리스 한도(10년)를 넘는다 — "
        "BLS가 조용히 최신 연도를 잘라낸다"
    )


def test_fetch_raw_sends_the_year_window_it_promises(monkeypatch):
    """_HISTORY_YEARS를 고쳐도 실제 요청 본문이 따라가지 않으면 의미가 없다."""
    from datetime import datetime

    captured = {}

    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return {"status": "REQUEST_SUCCEEDED", "Results": {"series": []}}

    def _post(url, json=None, timeout=None):
        captured.update(json)
        return _Resp()

    monkeypatch.setattr(bls.requests, "post", _post)
    bls._fetch_raw(["CUUR0000SA0"], None)

    this_year = datetime.utcnow().year
    assert captured["endyear"] == str(this_year)
    span = this_year - int(captured["startyear"]) + 1
    assert span <= 10
