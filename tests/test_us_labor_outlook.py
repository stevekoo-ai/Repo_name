"""미국 노동시장 + IMF 전망 리포트 섹션 (engine/report/us_labor_outlook.py, 1.5절).

2026-09-07 신설. 이 섹션의 계약 두 가지가 테스트의 전부다:
1. 전망을 실측인 척 렌더하지 않는다(IMF는 이 저장소에서 유일하게 미래 값을 준다).
2. 데이터가 없으면 섹션을 통째로 생략한다 — 0이나 "N/A"로 채우지 않는다(R3).
"""
from __future__ import annotations

from engine.report.markdown import _us_labor_outlook_section


def _labor_fixture():
    return {"as_of": "2026-07-01", "items": [
        {"label": "시간당 평균임금", "unit": "달러", "digits": 2,
         "as_of": "2026-07-01", "value": 37.5, "change": 0.08},
        {"label": "실업률", "unit": "%", "digits": 1,
         "as_of": "2026-07-01", "value": 4.4, "change": -0.1},
    ]}


def _outlook_fixture():
    return {"series_key": "gdp_growth", "rows": [
        {"country": "한국", "actual_year": "2025", "actual": 1.0,
         "forecast": [{"date": "2026-01-01", "value": 1.9},
                      {"date": "2027-01-01", "value": 2.1}]},
    ]}


def test_forecast_is_labeled_as_forecast_not_presented_as_measurement():
    """IMF 전망을 실측처럼 렌더하면 R1(실측 우선)을 정면으로 어긴다."""
    out = _us_labor_outlook_section(
        {"us_labor": None, "imf_outlook": _outlook_fixture()})
    assert "전망" in out
    assert "예측이지 실측이 아니다" in out
    # 실측 연도와 전망 연도가 같은 칸에 뭉쳐 있으면 안 된다
    assert "2025년 1.0%" in out and "2026년 1.9%" in out


def test_section_is_omitted_entirely_when_nothing_was_collected():
    """미수집을 0이나 'N/A'로 채우지 않는다 — 섹션 자체가 사라져야 한다(R3)."""
    assert _us_labor_outlook_section({"us_labor": None, "imf_outlook": None}) == ""
    assert _us_labor_outlook_section({}) == ""


def test_labor_only_and_outlook_only_both_render():
    """한쪽만 수집됐어도 그쪽은 보여야 한다 — 둘 다 있어야만 렌더하면
    한 소스의 장애가 멀쩡한 다른 소스까지 가린다."""
    # 섹션 제목("1.5 미국 노동시장 & 국가별 전망")에는 두 단어가 다 들어가므로
    # 하위 헤딩(## ...)으로 어느 블록이 실제로 렌더됐는지 본다.
    labor_only = _us_labor_outlook_section(
        {"us_labor": _labor_fixture(), "imf_outlook": None})
    assert "## 미국 노동시장 (BLS" in labor_only
    assert "## 실질 GDP 성장률" not in labor_only

    outlook_only = _us_labor_outlook_section(
        {"us_labor": None, "imf_outlook": _outlook_fixture()})
    assert "## 실질 GDP 성장률" in outlook_only
    assert "## 미국 노동시장 (BLS" not in outlook_only


def test_change_direction_arrows_match_the_sign():
    out = _us_labor_outlook_section({"us_labor": _labor_fixture(), "imf_outlook": None})
    assert "▲ 0.08" in out    # 임금 상승
    assert "▼ 0.1" in out     # 실업률 하락


def test_section_states_it_is_not_a_trade_instruction():
    """R4 — 포지션 지시는 결정 엔진 단일 출처. 새 신호가 매매 지시처럼
    읽히지 않도록 문구를 강제한다(CCI 충돌 처리와 동일 패턴)."""
    out = _us_labor_outlook_section(
        {"us_labor": _labor_fixture(), "imf_outlook": _outlook_fixture()})
    assert "매매 지시가 아니다" in out
    assert "R4" in out


def test_missing_series_are_skipped_not_rendered_as_zero(monkeypatch):
    """수집 안 된 지표를 0으로 렌더하면 '임금 0달러'처럼 읽힌다."""
    import pandas as pd

    from engine.report import us_labor_outlook as mod

    def _fake_read(series_id):
        if series_id == "bls_us_unemployment":
            return pd.DataFrame([{"date": "2026-07-01", "value": 4.4}])
        return pd.DataFrame()

    monkeypatch.setattr(mod.base, "read_normalized", _fake_read)
    result = mod.build_us_labor()
    assert result is not None
    assert [i["label"] for i in result["items"]] == ["실업률"]


def test_build_returns_none_when_no_series_exist_at_all(monkeypatch):
    import pandas as pd

    from engine.report import us_labor_outlook as mod

    monkeypatch.setattr(mod.base, "read_normalized", lambda sid: pd.DataFrame())
    assert mod.build_us_labor() is None
    assert mod.build_imf_outlook() is None
