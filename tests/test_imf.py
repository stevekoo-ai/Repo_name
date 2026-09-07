"""IMF WEO collector (collectors/imf.py).

2026-09-07 신설. config/api.yaml에 등록만 돼 있고 구현이 없던 소스를
채우면서 만든 테스트. 이 모듈의 핵심 계약은 하나다:
**실측과 전망을 절대 섞지 않는다.**
"""
from __future__ import annotations

from datetime import datetime

import pytest

from collectors import imf


def test_actual_and_forecast_are_split_at_the_cutoff():
    """WEO는 과거 실측과 미래 전망을 한 딕셔너리에 담아 준다. 이 저장소의
    다른 소스는 전부 실측만 주므로, 섞인 채로 흘러가면 리포트가 예측을
    실측으로 제시하게 된다 — R1(실측 우선)과 같은 계열의 규칙."""
    series = {"2023": 1.4, "2024": 2.0, "2025": 1.8, "2026": 2.2, "2031": 1.9}
    actual, forecast = imf._split_actual_forecast(series, cutoff_year=2025)

    assert [r["date"] for r in actual] == ["2023-01-01", "2024-01-01", "2025-01-01"]
    assert [r["date"] for r in forecast] == ["2026-01-01", "2031-01-01"]
    assert forecast[-1]["value"] == 1.9


def test_split_is_sorted_by_year_not_dict_order():
    """API가 주는 dict 순서를 신뢰하면 시계열이 뒤섞인다."""
    series = {"2026": 3.0, "2024": 1.0, "2025": 2.0}
    actual, forecast = imf._split_actual_forecast(series, cutoff_year=2025)
    assert [r["value"] for r in actual] == [1.0, 2.0]
    assert [r["value"] for r in forecast] == [3.0]


def test_non_year_keys_are_ignored_not_crashed_on():
    series = {"2024": 1.0, "notayear": 5.0, "": 9.0}
    actual, forecast = imf._split_actual_forecast(series, cutoff_year=2025)
    assert len(actual) == 1 and forecast == []


def test_cutoff_is_last_year_so_the_current_year_counts_as_forecast():
    """올해 값은 연중이라 어차피 추정치다. 실측 계열에 넣으면 리포트가
    추정을 실측으로 말하게 된다 — 보수적으로 작년까지만 실측."""
    this_year = datetime.utcnow().year
    series = {str(this_year - 1): 1.0, str(this_year): 2.0}
    actual, forecast = imf._split_actual_forecast(series, cutoff_year=this_year - 1)
    assert [r["value"] for r in actual] == [1.0]
    assert [r["value"] for r in forecast] == [2.0]


def test_fetch_parses_the_datamapper_envelope(monkeypatch):
    """datamapper 응답은 values -> 지표코드 -> 국가코드 -> {연도: 값} 3중 중첩이다."""
    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return {"values": {"NGDP_RPCH": {"KOR": {"2024": 2.0, "2025": None, "2026": "1.9"}}}}

    monkeypatch.setattr(imf.requests, "get", lambda *a, **k: _Resp())
    series = imf._fetch("NGDP_RPCH", "KOR")
    assert series == {"2024": 2.0, "2026": 1.9}   # None은 제외, 문자열 숫자는 변환


def test_fetch_returns_empty_for_a_country_not_in_the_response(monkeypatch):
    class _Resp:
        def raise_for_status(self): pass
        def json(self):
            return {"values": {"NGDP_RPCH": {"USA": {"2024": 2.8}}}}

    monkeypatch.setattr(imf.requests, "get", lambda *a, **k: _Resp())
    assert imf._fetch("NGDP_RPCH", "KOR") == {}


def test_series_catalog_has_no_duplicate_indicator_codes():
    codes = [code for code, _, _ in imf.IMF_SERIES.values()]
    assert len(codes) == len(set(codes))


def test_timeout_is_generous_because_datamapper_is_slow():
    """프로브 실측 10.4초 — 다른 소스 기준(8~20초)으로 잡으면 종종 죽는다."""
    connect, read = imf._TIMEOUT_SECONDS
    assert read >= 30
