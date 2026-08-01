"""Tests for collectors/base.py's shared plumbing — specifically the API-key
redaction helper, since a leak here means a real secret ends up committed to a
public report/<month>.md file (see collectors/molit.py's fetch_and_store)."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import requests

from collectors import base


def test_redact_url_masks_service_key():
    url = (
        "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
        "?serviceKey=751fd46ea503be38c38d3b466987abf162c356f40a2e060ef7fb7953fb5ca078"
        "&LAWD_CD=11110&DEAL_YMD=202607&pageNo=1&numOfRows=1000&type=json"
    )
    redacted = base.redact_url(url)
    assert "751fd46ea503be38c38d3b466987abf162c356f40a2e060ef7fb7953fb5ca078" not in redacted
    assert "serviceKey=***" in redacted
    assert "LAWD_CD=11110" in redacted  # non-secret params survive untouched


def test_redact_url_masks_fred_and_kosis_style_keys():
    assert "api_key=***" in base.redact_url("https://x/y?series_id=Z&api_key=abcdef123&file_type=json")
    assert "apiKey=***" in base.redact_url("https://x/y?apiKey=XYZ789&itmId=ALL")


def test_redact_url_leaves_key_free_urls_untouched():
    url = "https://x/y?page=1&perPage=200"
    assert base.redact_url(url) == url


def test_raise_for_status_redacts_key_in_exception_message():
    resp = MagicMock()
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "401 Client Error: Unauthorized for url: https://apis.data.go.kr/x?serviceKey=SECRET123&a=1"
    )
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        base.raise_for_status(resp)
    assert "SECRET123" not in str(excinfo.value)
    assert "serviceKey=***" in str(excinfo.value)


def test_raise_for_status_noop_on_success():
    resp = MagicMock()
    resp.raise_for_status.return_value = None
    base.raise_for_status(resp)  # must not raise
