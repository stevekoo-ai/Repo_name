"""docs/real-estate-daily.html generator (engine/report/real_estate_dashboard.py).

사용자 요청: "HTML보고서에 부동산 매매가 전월세에 대해서 쌓인 데이터만큼 daily
그래프로 보여줘 트렌드가 보고싶다."
"""
from __future__ import annotations

import json
import re

import pandas as pd
import pytest

from engine.report import real_estate_dashboard as red
from engine.report.real_estate_dashboard import render_real_estate_dashboard


def _fake_normalized(rows: dict[str, list[tuple[str, float]]]):
    """series_id -> [(date, value_won), ...] 를 collector_base.read_normalized가
    돌려주는 DataFrame 모양으로 흉내."""

    def _read(series_id: str) -> pd.DataFrame:
        data = rows.get(series_id)
        if not data:
            return pd.DataFrame(columns=["date", "value"])
        return pd.DataFrame(data, columns=["date", "value"])

    return _read


def test_render_smoke_with_no_data(monkeypatch):
    """DATA_GO_KR_KEY 미설정 등으로 정규화 데이터가 아예 없어도 크래시 없이,
    "데이터 없음" 안내와 함께 렌더링돼야 한다(7.9 — 값을 지어내지 않음)."""
    monkeypatch.setattr(red.collector_base, "read_normalized", _fake_normalized({}))

    html_doc = render_real_estate_dashboard()

    assert html_doc.startswith("<!doctype html>")
    assert html_doc.count("<section") == html_doc.count("</section>")
    assert "아직 수집된 실거래가 데이터가 없습니다" in html_doc
    assert "부동산 실거래가 Daily Dashboard" in html_doc


def test_render_with_accumulated_data_shows_all_six_groups(monkeypatch):
    rows = {
        "molit_seoul_price_pyeong": [("2026-05-01", 450_000_000.0), ("2026-06-01", 460_000_000.0)],
        "molit_capital_area_price_pyeong": [("2026-06-01", 300_000_000.0)],
        "molit_nationwide_price_pyeong": [("2026-06-01", 200_000_000.0)],
        "molit_highlight_price_pyeong": [("2026-06-01", 250_000_000.0)],
        "molit_rent_wolse_seoul_deposit_pyeong": [("2026-06-01", 50_000_000.0)],
        "molit_rent_wolse_seoul_rent_pyeong": [("2026-06-01", 500_000.0)],
    }
    monkeypatch.setattr(red.collector_base, "read_normalized", _fake_normalized(rows))

    html_doc = render_real_estate_dashboard()

    for title in ("아파트 매매", "연립다세대(빌라) 매매", "오피스텔 매매",
                  "아파트 전세", "아파트 월세 — 보증금", "아파트 월세 — 월세액"):
        assert title in html_doc
    # 청약 타겟 인근(kr_regions.HIGHLIGHT_REGION) 라벨이 매 그룹의 차트 카드마다 붙는다
    # (+ 상단 설명 문단에서 1회 더 언급).
    assert html_doc.count("청약 타겟 인근") == 7


def _extract_data_json(html_doc: str) -> dict:
    match = re.search(r"var RE_DAILY_DATA = (\{.*\});", html_doc)
    assert match, "RE_DAILY_DATA payload not found in rendered dashboard"
    return json.loads(match.group(1))


def test_values_are_converted_from_won_to_manwon_not_left_raw(monkeypatch):
    """render는 (원) 단위 정규화 값을 만원 단위로 나눠 보여준다 — 원 단위 그대로면
    차트 라벨이 억 단위 숫자로 깨져 보인다."""
    rows = {"molit_seoul_price_pyeong": [("2026-06-01", 45_000_000.0)]}
    monkeypatch.setattr(red.collector_base, "read_normalized", _fake_normalized(rows))

    html_doc = render_real_estate_dashboard()
    data = _extract_data_json(html_doc)

    assert data["series"]["molit_price_seoul"]["values"] == [4500.0]
    assert data["series"]["molit_price_seoul"]["dates"] == ["2026-06-01"]


def test_each_group_reads_its_own_series_not_a_shared_one(monkeypatch):
    """매매(molit)와 전세(molit_rent_jeonse) 서울 시리즈가 서로 다른 series_id를
    읽어야 한다 — 접두어 조합이 잘못되면 두 그룹이 같은 파일을 읽는 회귀가 생긴다."""
    rows = {
        "molit_seoul_price_pyeong": [("2026-06-01", 45_000_000.0)],
        "molit_rent_jeonse_seoul_price_pyeong": [("2026-06-01", 15_000_000.0)],
    }
    monkeypatch.setattr(red.collector_base, "read_normalized", _fake_normalized(rows))

    html_doc = render_real_estate_dashboard()
    data = _extract_data_json(html_doc)

    assert data["series"]["molit_price_seoul"]["values"] == [4500.0]
    assert data["series"]["molit_rent_jeonse_price_seoul"]["values"] == [1500.0]


def test_write_real_estate_dashboard_writes_to_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(red.collector_base, "read_normalized", _fake_normalized({}))
    out = tmp_path / "real-estate-daily.html"

    written = red.write_real_estate_dashboard(out_path=out)

    assert written == out
    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("<!doctype html>")
