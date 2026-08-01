"""Pure-function tests for the MOLIT 전월세 collector and trend engine —
no network calls (mirrors tests/test_real_estate.py's approach for molit.py)."""
from __future__ import annotations

import pytest

from collectors import molit_rent
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
