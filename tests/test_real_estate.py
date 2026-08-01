"""Pure-function tests for the MOLIT real-estate collector and trend engine —
no network calls (those paths are exercised end-to-end only in CI with a real
MOLIT_API_KEY)."""
from __future__ import annotations

import pytest

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


class _FakeResponse:
    """Minimal requests.Response stand-in for exercising _fetch_region_month's error paths
    without a real network call."""

    def __init__(self, text: str, json_ok: bool = True, status_ok: bool = True, status_error: str | None = None):
        self.text = text
        self._json_ok = json_ok
        self._status_ok = status_ok
        self._status_error = status_error or "500 Server Error"

    def raise_for_status(self):
        if not self._status_ok:
            raise __import__("requests").exceptions.HTTPError(self._status_error)

    def json(self):
        if not self._json_ok:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        import json
        return json.loads(self.text)


def test_fetch_region_month_surfaces_data_go_kr_error_response(monkeypatch):
    """data.go.kr's own error envelope (resultCode != 00) must not be swallowed as an empty
    result — a wrong/unapproved service key looks exactly like "no data" otherwise."""
    body = '{"response": {"header": {"resultCode": "30", "resultMsg": "SERVICE_ACCESS_DENIED_ERROR"}}}'
    monkeypatch.setattr(molit.requests, "get", lambda *a, **k: _FakeResponse(body))

    with pytest.raises(RuntimeError, match="SERVICE_ACCESS_DENIED_ERROR"):
        molit._fetch_region_month("11110", "202601", "fake-key")


def test_fetch_region_month_surfaces_non_json_body_as_likely_auth_error(monkeypatch):
    """data.go.kr returns an XML error envelope (not JSON) when the gateway rejects a request
    before it reaches the service that would honor type=json — the classic signature of a key
    that's valid but not 활용신청-approved for *this* specific API product. This must produce a
    message pointing at that, not an opaque JSON-decode failure."""
    xml_body = "<OpenAPI_ServiceResponse><cmmMsgHeader><errMsg>SERVICE ACCESS DENIED</errMsg></cmmMsgHeader></OpenAPI_ServiceResponse>"
    monkeypatch.setattr(molit.requests, "get", lambda *a, **k: _FakeResponse(xml_body, json_ok=False))

    with pytest.raises(RuntimeError, match="non-JSON response"):
        molit._fetch_region_month("11110", "202601", "fake-key")


def test_fetch_region_month_never_leaks_the_real_key_on_http_error(monkeypatch):
    """Regression test for a real incident: a 401 from data.go.kr surfaced the raw
    DATA_GO_KR_KEY value (from requests' HTTPError embedding the full request URL) into
    fetch_and_store()'s note — which then got committed verbatim into the public
    report/<month>.md. _fetch_region_month must never let the real key value survive in
    any exception it raises, regardless of which HTTP status caused the failure."""
    real_key = "751fd46ea503be38c38d3b466987abf162c356f40a2e060ef7fb7953fb5ca078"
    status_error = (
        "401 Client Error: Unauthorized for url: "
        f"https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
        f"?serviceKey={real_key}&LAWD_CD=11110&DEAL_YMD=202607&pageNo=1&numOfRows=1000&type=json"
    )
    monkeypatch.setattr(
        molit.requests, "get",
        lambda *a, **k: _FakeResponse("", status_ok=False, status_error=status_error),
    )

    with pytest.raises(Exception) as excinfo:
        molit._fetch_region_month("11110", "202607", real_key)

    assert real_key not in str(excinfo.value)


def test_probe_with_detail_returns_error_message_instead_of_swallowing_it(monkeypatch):
    def _always_fails(*a, **k):
        raise RuntimeError("SERVICE_ACCESS_DENIED_ERROR")

    monkeypatch.setattr(molit, "_fetch_region_month", _always_fails)

    rows, error = molit._probe_with_detail("11110", "202601", "fake-key", attempts=1, backoff_seconds=0)

    assert rows is None
    assert error == "SERVICE_ACCESS_DENIED_ERROR"
