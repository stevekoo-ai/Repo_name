"""Pure-function tests for the MOLIT 연립다세대/오피스텔 매매 collectors and trend engines.

Both reuse collectors/molit.py's _price_per_pyeong (already covered by
tests/test_real_estate.py) and collectors/kr_regions.py (already covered there too) —
these tests focus on what's specific to each module: source/series naming, error
surfacing, and pending behavior with no key.
"""
from __future__ import annotations

import pytest

from collectors import molit_officetel, molit_villa
from engine.real_estate import officetel_trend, villa_trend


@pytest.mark.parametrize("module", [molit_villa, molit_officetel])
def test_source_and_series_prefix_are_distinct_and_match(module):
    assert module.SOURCE == module.SERIES_PREFIX
    assert module.SOURCE in ("molit_villa", "molit_officetel")


@pytest.mark.parametrize("module", [molit_villa, molit_officetel])
def test_fetch_region_month_surfaces_data_go_kr_error_response(module, monkeypatch):
    body = '{"response": {"header": {"resultCode": "30", "resultMsg": "SERVICE_ACCESS_DENIED_ERROR"}}}'

    class _FakeResponse:
        text = body

        def raise_for_status(self):
            pass

        def json(self):
            import json
            return json.loads(self.text)

    monkeypatch.setattr(module.requests, "get", lambda *a, **k: _FakeResponse())

    with pytest.raises(RuntimeError, match="SERVICE_ACCESS_DENIED_ERROR"):
        module._fetch_region_month("11110", "202601", "fake-key")


@pytest.mark.parametrize("module", [molit_villa, molit_officetel])
def test_fetch_region_month_surfaces_non_json_body_as_likely_auth_error(module, monkeypatch):
    xml_body = "<OpenAPI_ServiceResponse><cmmMsgHeader><errMsg>SERVICE ACCESS DENIED</errMsg></cmmMsgHeader></OpenAPI_ServiceResponse>"

    class _FakeResponse:
        text = xml_body

        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Expecting value: line 1 column 1 (char 0)")

    monkeypatch.setattr(module.requests, "get", lambda *a, **k: _FakeResponse())

    with pytest.raises(RuntimeError, match="non-JSON response"):
        module._fetch_region_month("11110", "202601", "fake-key")


def test_compute_villa_trend_pending_when_no_key(monkeypatch):
    monkeypatch.delenv("DATA_GO_KR_KEY", raising=False)
    result = villa_trend.compute_villa_trend()
    assert result["fetch_status"] == "pending"
    assert result["fetch_note"] is not None


def test_compute_officetel_trend_pending_when_no_key(monkeypatch):
    monkeypatch.delenv("DATA_GO_KR_KEY", raising=False)
    result = officetel_trend.compute_officetel_trend()
    assert result["fetch_status"] == "pending"
    assert result["fetch_note"] is not None
