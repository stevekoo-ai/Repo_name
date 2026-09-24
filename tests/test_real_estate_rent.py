"""Pure-function tests for the MOLIT 전월세 collector and trend engine —
no network calls (mirrors tests/test_real_estate.py's approach for molit.py)."""
from __future__ import annotations

import pytest

from collectors import base, molit_rent
from engine.real_estate import rent_trend


def test_amount_per_pyeong_parses_comma_formatted_amount():
    row = {"deposit": "50,000", "excluUseAr": "84.96"}
    price = molit_rent._amount_per_pyeong(row, "deposit")
    assert price is not None
    assert price == (50_000 * 10_000) / (84.96 / 3.3058)


def test_amount_per_pyeong_handles_missing_fields():
    assert molit_rent._amount_per_pyeong({}, "deposit") is None
    assert molit_rent._amount_per_pyeong({"deposit": "1,000", "excluUseAr": "0"}, "deposit") is None


def test_is_jeonse_true_when_monthly_rent_zero_or_missing():
    assert molit_rent._is_jeonse({"monthlyRent": "0"}) is True
    assert molit_rent._is_jeonse({}) is True
    assert molit_rent._is_jeonse({"monthlyRent": ""}) is True


def test_is_jeonse_false_when_monthly_rent_positive():
    assert molit_rent._is_jeonse({"monthlyRent": "80"}) is False
    assert molit_rent._is_jeonse({"monthlyRent": "1,200"}) is False


def test_split_prices_separates_jeonse_and_wolse_and_keeps_counts_aligned():
    rows = [
        {"excluUseAr": "84.96", "deposit": "50,000", "monthlyRent": "0"},    # jeonse
        {"excluUseAr": "59.9", "deposit": "10,000", "monthlyRent": "80"},    # wolse
        {"excluUseAr": "59.9", "deposit": "10,000"},                         # wolse field missing -> jeonse (monthlyRent missing treated as 0)
        {"excluUseAr": "0", "deposit": "10,000", "monthlyRent": "50"},       # invalid area -> dropped entirely
    ]
    split = molit_rent._split_prices(rows)
    assert len(split["jeonse_deposit_pyeong"]) == 2
    assert len(split["wolse_deposit_pyeong"]) == 1
    assert len(split["wolse_rent_pyeong"]) == 1  # stays aligned with wolse_deposit_pyeong


def test_fetch_region_month_surfaces_data_go_kr_error_response(monkeypatch):
    body = '{"response": {"header": {"resultCode": "30", "resultMsg": "SERVICE_ACCESS_DENIED_ERROR"}}}'

    class _FakeResponse:
        text = body

        def raise_for_status(self):
            pass

        def json(self):
            import json
            return json.loads(self.text)

    monkeypatch.setattr(molit_rent.requests, "get", lambda *a, **k: _FakeResponse())

    with pytest.raises(RuntimeError, match="SERVICE_ACCESS_DENIED_ERROR"):
        molit_rent._fetch_region_month("11110", "202601", "fake-key")


def test_fetch_region_month_never_leaks_the_real_key_on_http_error(monkeypatch):
    """Same regression class as collectors/molit.py's — the redaction lives in
    collectors/base.raise_for_status, shared by every MOLIT-family collector."""
    real_key = "751fd46ea503be38c38d3b466987abf162c356f40a2e060ef7fb7953fb5ca078"
    status_error = (
        "401 Client Error: Unauthorized for url: "
        f"https://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent"
        f"?serviceKey={real_key}&LAWD_CD=11110&DEAL_YMD=202607&pageNo=1&numOfRows=1000&type=json"
    )

    class _FakeResponse:
        text = ""

        def raise_for_status(self):
            import requests
            raise requests.exceptions.HTTPError(status_error)

    monkeypatch.setattr(molit_rent.requests, "get", lambda *a, **k: _FakeResponse())

    with pytest.raises(Exception) as excinfo:
        molit_rent._fetch_region_month("11110", "202607", real_key)

    assert real_key not in str(excinfo.value)


def test_compute_rent_trend_pending_when_no_key(monkeypatch):
    monkeypatch.delenv("DATA_GO_KR_KEY", raising=False)
    result = rent_trend.compute_rent_trend()
    assert result["fetch_status"] == "pending"
    assert result["fetch_note"] is not None


# ── 거주지(수지구) 전월세 series — 2026-09-24 신설 ──────────────────
#
# 사용자: "용인시 수지구의 전월세 변화는 내게 아주 중요한 데이터이니
# 따로 잘 기록해놓고 판단에 반영하도록 하자." 청약 타겟(기흥구, highlight)과
# 이름이 섞이면 어느 지역 신호인지 알 수 없게 되므로, series 이름 자체가
# 분리돼 있는지 소스 검사로 고정한다(fetch_and_store는 실제 API 키가
# 있어야 끝까지 돌아가므로 여기서는 로직이 있는지만 고정).

def test_fetch_and_store_writes_dedicated_residence_series_not_reusing_highlight():
    import inspect
    src = inspect.getsource(molit_rent.fetch_and_store)
    assert "RESIDENCE_REGION" in src
    for suffix in ("jeonse_residence_price_pyeong", "jeonse_residence_volume",
                   "wolse_residence_deposit_pyeong", "wolse_residence_rent_pyeong",
                   "wolse_residence_volume"):
        assert suffix in src, f"거주지 전용 series '{suffix}'가 없다"
    # highlight(기흥구) 기존 series 이름은 그대로 남아 있어야 한다 — 이미
    # 5개월치가 쌓여 있어 이름이 바뀌면 그 이력이 끊긴다.
    for suffix in ("jeonse_highlight_price_pyeong", "wolse_highlight_deposit_pyeong"):
        assert suffix in src, f"기존 하이라이트 series '{suffix}'가 사라지면 안 된다"


# ── 장기 백필 파라미터화 — 2026-09-24 신설 ─────────────────────────
#
# 사용자: "과거 데이터를 가지고 올 수 있는데 왜 한달치만 가져와? 과거
# 10년치를 매달 가져올 수 있어?" 답: 새 지역(RESIDENCE_REGION)은 티어
# series가 이미 두꺼워서 늘 1개월만 받던 게 원인이었다(fetch_and_store의
# thinnest_history 게이트가 **티어 단위**라 개별 신규 지역의 이력 부재를
#못 본다). months/region_codes를 명시하면 그 게이트를 우회한다.

def _stub_network(monkeypatch, calls: list[tuple[str, str]]):
    """get_api_key/_probe_with_detail/_fetch_region_month를 네트워크 없이
    흉내낸다. calls에는 실제로 조회된 (region_code, deal_ymd)가 쌓인다."""
    monkeypatch.setattr(molit_rent, "get_api_key", lambda source: "dummy-key")

    def _fake_probe(lawd_cd, deal_ymd, api_key, **kw):
        return [{"deposit": "10,000", "monthlyRent": "0", "excluUseAr": "84.0"}], None
    monkeypatch.setattr(molit_rent, "_probe_with_detail", _fake_probe)

    def _fake_fetch(lawd_cd, deal_ymd, api_key):
        calls.append((lawd_cd, deal_ymd))
        return [{"deposit": "10,000", "monthlyRent": "0", "excluUseAr": "84.0"}]
    monkeypatch.setattr(molit_rent, "_fetch_region_month", _fake_fetch)


def test_months_param_overrides_the_thinnest_history_gate(monkeypatch, tmp_path):
    """기본 호출은 티어가 이미 두꺼우면 1개월만 받는다 — 그게 새 지역이
    한 달치만 받던 원인이었다. months=를 명시하면 그 판단을 건너뛴다."""
    calls: list[tuple[str, str]] = []
    _stub_network(monkeypatch, calls)
    monkeypatch.setattr(base, "NORMALIZED_DIR", tmp_path)
    # 티어 series가 이미 두껍다고 흉내(기본 호출이면 1개월로 떨어질 상황)
    monkeypatch.setattr(base, "read_normalized",
                        lambda series_id: [0] * 12 if "highlight" not in series_id else [])

    result = molit_rent.fetch_and_store(
        months=10, region_codes=[molit_rent.RESIDENCE_REGION["code"]])

    assert len(result["months_fetched"]) == 10


def test_region_codes_restricts_which_regions_are_actually_queried(monkeypatch, tmp_path):
    calls: list[tuple[str, str]] = []
    _stub_network(monkeypatch, calls)
    monkeypatch.setattr(base, "NORMALIZED_DIR", tmp_path)
    monkeypatch.setattr(base, "read_normalized", lambda series_id: [])

    target = molit_rent.RESIDENCE_REGION["code"]
    result = molit_rent.fetch_and_store(months=2, region_codes=[target])

    queried_codes = {code for code, _ in calls}
    assert queried_codes == {target}, "지정한 지역만 조회해야 한다 — 55개 전부를 부르면 안 된다"
    assert result["regions_total"] == 1


def test_scoped_backfill_never_writes_tier_aggregates(monkeypatch, tmp_path):
    """55개 중 2개 지역만 조회해놓고 티어(수도권 등) 값을 갱신하면, 그
    달의 티어가 '전체 대비 일부만 반영'된 값으로 조용히 오염된다."""
    calls: list[tuple[str, str]] = []
    _stub_network(monkeypatch, calls)
    monkeypatch.setattr(base, "NORMALIZED_DIR", tmp_path)
    monkeypatch.setattr(base, "read_normalized", lambda series_id: [])

    written: list[str] = []
    real_append = base.append_normalized
    monkeypatch.setattr(base, "append_normalized",
                        lambda series_id, rows: written.append(series_id))

    molit_rent.fetch_and_store(
        months=1, region_codes=[molit_rent.HIGHLIGHT_REGION["code"],
                                molit_rent.RESIDENCE_REGION["code"]])

    tier_series = [s for s in written if any(f"_{t}_" in s for t in ("seoul", "capital_area", "nationwide"))]
    assert tier_series == [], f"scoped 백필에서 티어 series가 쓰였다: {tier_series}"
    assert any("_residence_" in s for s in written), "residence series는 여전히 써야 한다"
    assert any("_highlight_" in s for s in written), "highlight series는 여전히 써야 한다"


def test_unscoped_call_still_writes_tier_aggregates(monkeypatch, tmp_path):
    """region_codes를 안 주는 평소 호출은 지금까지처럼 티어도 써야 한다
    — scoped 가드가 기본 동작까지 막으면 안 된다."""
    calls: list[tuple[str, str]] = []
    _stub_network(monkeypatch, calls)
    monkeypatch.setattr(base, "NORMALIZED_DIR", tmp_path)
    monkeypatch.setattr(base, "read_normalized", lambda series_id: [])

    written: list[str] = []
    monkeypatch.setattr(base, "append_normalized",
                        lambda series_id, rows: written.append(series_id))

    molit_rent.fetch_and_store(months=1)

    assert any("_capital_area_" in s for s in written), "기본 호출은 티어를 계속 써야 한다"


def test_empty_region_codes_match_is_reported_not_silently_skipped(monkeypatch):
    """존재하지 않는 코드만 넘기면 R3대로 판정불가를 명시해야 한다."""
    monkeypatch.setattr(molit_rent, "get_api_key", lambda source: "dummy-key")
    result = molit_rent.fetch_and_store(months=1, region_codes=["99999"])
    assert result["status"] == "error"
