"""Tests for engine.report.subscription_report — the daily "청약 리포트" split
out of PEOS (2026-09-02): 청약 우려사항 추적 + 매매/전세 실거래가 4종, with no
macro/CCI dependency at all.
"""
from __future__ import annotations

from engine.exporters.subscription_concern_tracker import ConcernItem, SubscriptionConcernReport
from engine.report import subscription_report as sr


def _fake_report(urgency="🟢 관망", headline="테스트 headline"):
    return SubscriptionConcernReport(
        concerns=[
            ConcernItem(name="테스트 우려", urgency=urgency, status="상태",
                       recommendation="권고", detail=["세부1"]),
        ],
        overall_urgency=urgency,
        headline=headline,
    )


def test_sale_trend_section_empty_when_no_data():
    assert sr._real_estate_trend({}) == ""
    assert sr._villa_trend({}) == ""
    assert sr._officetel_trend({}) == ""
    assert sr._rent_trend({}) == ""


def test_sale_trend_section_pending_placeholder():
    payload = {"real_estate": {"fetch_status": "pending", "fetch_note": "DATA_GO_KR_KEY 미설정"}}
    out = sr._real_estate_trend(payload)
    assert "아파트 매매" in out
    assert "Pending" in out
    assert "DATA_GO_KR_KEY 미설정" in out


def test_subscription_concerns_section_reads_precomputed_not_recompute(monkeypatch):
    """지난 버전의 버그: 이 함수가 compute_subscription_concerns()를 다시 불러서
    build_subscription_report_payload()의 try/except가 이미 잡아준 실패를 여기서
    다시 재현해 렌더링 전체를 죽일 수 있었다 — payload에 이미 계산된 값을 읽기만
    해야 한다."""
    def _boom(*a, **k):
        raise RuntimeError("이 함수는 절대 호출되면 안 됨")
    monkeypatch.setattr(sr, "compute_subscription_concerns", _boom)

    payload = {"subscription_concerns": _fake_report(headline="🟢 전부 관망")}
    out = sr._subscription_concerns_section(payload)
    assert "테스트 우려" in out
    assert "🟢 전부 관망" in out


def test_subscription_concerns_section_pending_when_none():
    out = sr._subscription_concerns_section({"subscription_concerns": None})
    assert "Pending" in out
    assert "계산 실패" in out


def test_render_skips_missing_real_estate_sections_but_keeps_intro_and_concerns():
    payload = {"subscription_concerns": _fake_report()}
    out = sr.render_subscription_report(payload, "2026-09-02")
    assert out.startswith("# 청약 리포트 — 2026-09-02")
    assert "테스트 우려" in out
    assert "아파트 매매" not in out
    assert "연립다세대" not in out
    assert "오피스텔" not in out
    assert "전월세" not in out


def test_render_includes_real_estate_sections_when_data_present():
    payload = {
        "subscription_concerns": _fake_report(),
        "real_estate": {"fetch_status": "pending", "fetch_note": "no key"},
        "real_estate_villa": {"fetch_status": "pending", "fetch_note": "no key"},
    }
    out = sr.render_subscription_report(payload, "2026-09-02")
    assert "# 2. 부동산 실거래가 동향" in out
    assert "아파트 매매" in out
    assert "연립다세대" in out
    # officetel/rent were never in payload -> still absent
    assert "오피스텔" not in out


def test_render_never_produces_bare_header_blockquote_collision():
    """이전 버전 버그: 리스트를 통째로 join하며 빈 줄만 걸러내면(list comprehension
    with `if l != \"\"`) 헤더 다음 블록쿼트 사이 빈 줄까지 사라져 마크다운이 깨졌다."""
    out = sr.render_subscription_report({"subscription_concerns": _fake_report()}, "2026-09-02")
    assert "# 청약 리포트 — 2026-09-02\n\n>" in out


def test_build_subscription_report_payload_isolated(monkeypatch, tmp_path):
    """네트워크(MOLIT)와 exposure(portfolio.yaml)를 전부 격리해 순수 배선만 검증 —
    각 단계가 독립적으로 실패해도 나머지가 죽지 않는지가 핵심."""
    monkeypatch.setattr(sr.real_estate_trend, "compute_real_estate_trend", lambda: {"fetch_status": "ok"})
    monkeypatch.setattr(sr.rent_trend, "compute_rent_trend", lambda: {"fetch_status": "ok"})

    def _boom():
        raise RuntimeError("villa collector down")
    monkeypatch.setattr(sr.villa_trend, "compute_villa_trend", _boom)
    monkeypatch.setattr(sr.officetel_trend, "compute_officetel_trend", lambda: {"fetch_status": "ok"})

    monkeypatch.setattr(
        "engine.exposure.model.build_exposure_model",
        lambda: None,
    )
    monkeypatch.setattr(
        "collectors.manual.fetch_subscription_notices", lambda: []
    )

    payload = sr.build_subscription_report_payload()

    assert payload["real_estate"] == {"fetch_status": "ok"}
    assert payload["real_estate_rent"] == {"fetch_status": "ok"}
    assert payload["real_estate_villa"] is None  # failed independently, didn't crash the rest
    assert payload["real_estate_officetel"] == {"fetch_status": "ok"}
    # subscription_concerns still computes even though exposure/villa failed
    assert payload["subscription_concerns"] is not None
