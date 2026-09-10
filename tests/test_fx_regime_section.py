"""engine/report/fx_regime_section.py — 리포트 §1.7.

이 파일의 절반은 "무엇을 렌더하는가"가 아니라 **"무엇을 렌더하지 않는가"**를
고정한다. R4(포지션 지시는 단일 출처)와 §6.5.1(국면은 자산 선택에 정보를
주지 않는다)이 코드로 지켜지는지가 이 섹션의 핵심 계약이기 때문이다.
"""
from datetime import date

import pytest

from engine.fx.transition import TriggerKind
from engine.report.fx_regime_section import (
    build_fx_regime_payload, render_fx_regime_section,
)


@pytest.fixture(scope="module")
def payload():
    return {"fx_regime": build_fx_regime_payload(date(2026, 9, 9))}


@pytest.fixture(scope="module")
def rendered(payload):
    return render_fx_regime_section(payload)


# ── 렌더 기본 ────────────────────────────────────────────────

def test_section_renders_with_the_expected_headings(rendered):
    assert "# 1.7 환율 국면 (FRS)" in rendered
    assert "## 국면 전환 경고" in rendered
    assert "## 달러 자산 맥락" in rendered


def test_all_eight_factors_appear_with_their_weights(rendered):
    for label in ("한미 정책금리차", "미 10년물", "달러인덱스", "경상수지",
                  "수출", "지정학·위기", "유가(브렌트)", "MA36 이격"):
        assert label in rendered, label


def test_each_warning_shows_its_measured_predictive_power(rendered):
    """경고가 켜졌다는 사실만 보여주고 얼마나 믿을 만한지 안 보여주면
    독자가 네 개를 같은 무게로 읽는다."""
    assert "실측 예측력" in rendered
    assert "검증됨 — 단기 예측력 최강" in rendered        # 경과 개월
    assert "이번 표본에서 예측력 확인 안 됨" in rendered    # 모멘텀 반전


def test_missing_payload_skips_the_section_silently():
    assert render_fx_regime_section({}) == ""
    assert render_fx_regime_section({"fx_regime": None}) == ""
    assert render_fx_regime_section({"fx_regime": {"score": None}}) == ""


# ── R4 — 하지 않는 것들 ──────────────────────────────────────

FORBIDDEN = [
    "헤지하", "헤지를 ", "매수하", "매도하", "사야", "팔아야",
    "추천", "비중을 ", "목표 환율은 1", "전망치",
]

# "추천 아님", "목표 환율은 제시하지 않는다" 같은 **부인** 문구는 위반이
# 아니라 정반대다 — 이 섹션이 스스로 한계를 밝히는 문장이라 오히려 있어야
# 한다. 처음 이 테스트를 쓸 때 헤딩의 "(판단 재료 — 추천 아님)"이 걸려
# 오탐이 났고, 그래서 부정형을 명시적으로 구분한다.
NEGATIONS = ("아님", "않는다", "제시하지", "만들지", "하지 않")


def test_the_section_never_issues_an_instruction_or_recommendation(rendered):
    """R4 — 이 섹션은 근거만 제공한다. 지시·추천이 새어들면 결정 엔진과
    별개의 매매 지시가 두 개 생긴다."""
    for line in rendered.splitlines():
        if any(neg in line for neg in NEGATIONS):
            continue   # 스스로 한계를 밝히는 문장
        for phrase in FORBIDDEN:
            assert phrase not in line, f"금지 표현이 렌더됐다: {phrase!r} — {line!r}"


def test_the_disclaimer_lines_are_the_only_place_those_words_appear(rendered):
    """부인 문구 자체는 반드시 있어야 한다 — 없으면 위 테스트가 통과해도
    독자가 이 섹션의 성격을 알 수 없다."""
    assert "추천 아님" in rendered
    assert any(neg in rendered for neg in ("만들지 않는다", "제시하지 않는다"))


def test_the_section_states_its_own_limits(rendered):
    assert "R4" in rendered
    assert "목표 환율은 제시하지 않는다" in rendered or "목표 환율은 만들지 않는다" in rendered


def test_no_asset_allocation_score_is_produced(payload):
    """§6.5.1 — 국면에서 자산배분을 도출하지 않는다. dollar_context는
    사실(금리·스프레드) 뿐이고 점수나 비중 필드가 있으면 안 된다."""
    ctx = payload["fx_regime"]["dollar_context"]
    assert set(ctx) == {"cash_yield", "us_2y", "us_10y", "hy_oas", "vix"}
    for key in ctx:
        assert "weight" not in key and "score" not in key and "alloc" not in key


# ── §1.7-B 달러 맥락 ─────────────────────────────────────────

def test_cash_baseline_is_always_shown_when_available(rendered):
    """과거 국면과 지금의 결정적 차이라 반드시 보인다."""
    assert "달러 현금 기준선" in rendered
    assert "제로금리" in rendered


def test_long_bond_note_only_appears_when_a_warning_fired():
    """경고가 없으면 장기채 줄을 렌더하지 않는다 — 없는 신호를 매일 찍지 않는다."""
    quiet = {"fx_regime": {**build_fx_regime_payload(date(2026, 9, 9)),
                           "warning_count": 0}}
    assert "장기채 함의" not in render_fx_regime_section(quiet)


def test_us_tightening_and_non_us_shock_give_opposite_bond_notes():
    """§6.5.2 — 같은 종료 경고라도 원인에 따라 장기채 함의가 정반대다."""
    base = build_fx_regime_payload(date(2026, 9, 9))
    tightening = render_fx_regime_section({"fx_regime": {
        **base, "warning_count": 2, "trigger_kind": TriggerKind.US_TIGHTENING.name}})
    shock = render_fx_regime_section({"fx_regime": {
        **base, "warning_count": 2, "trigger_kind": TriggerKind.NON_US_SHOCK.name}})
    assert "−0.3%" in tightening and "무조건 진입" in tightening
    assert "+16.2%" in shock and "완화로 돌아서면" in shock
    assert tightening != shock


def test_unknown_trigger_kind_withholds_the_bond_judgement():
    """원인을 모르면 함의가 정반대일 수 있으므로 판단을 보류한다(R3)."""
    base = build_fx_regime_payload(date(2026, 9, 9))
    out = render_fx_regime_section({"fx_regime": {
        **base, "warning_count": 2, "trigger_kind": TriggerKind.UNKNOWN.name}})
    assert "판단을 보류" in out


# ── payload 계약 ─────────────────────────────────────────────

def test_payload_is_json_serialisable(payload):
    """리포트 payload는 로깅·직렬화를 타므로 Enum이나 dataclass가 새면 안 된다."""
    import json
    json.dumps(payload["fx_regime"])


def test_payload_carries_as_of_so_the_report_can_state_freshness(payload):
    assert payload["fx_regime"]["as_of"] == "2026-09-09"


# ── 두 렌더러 동등성 ─────────────────────────────────────────
#
# 2026-09-10에 실제로 난 사고 — §1.7을 markdown.py에만 연결하고 "구현 완료"
# 라고 보고했는데, **사용자가 매일 받아보는 건 HTML이다**(daily-peos-report.yml이
# report/<날짜>.html을 이메일로 보내고 docs/report.html로 게시한다).
# 마크다운은 저장소 안에만 있었다. 렌더러가 둘인 구조에선 한쪽만 붙이면
# 전달이 안 된다 — 그걸 테스트로 고정한다.

def test_the_html_renderer_also_emits_the_section():
    from engine.report.html_new import _render_fx_regime

    out = _render_fx_regime({"fx_regime": build_fx_regime_payload(date(2026, 9, 9))})
    assert "1.7 환율 국면" in out
    assert out.strip().startswith("<div class=\"card\"")


def test_both_renderers_report_the_same_score_and_label(payload):
    """두 렌더러가 각자 계산하면 같은 날 리포트가 두 얘기를 하게 된다.
    계산은 payload.py가 한 번만 하고 렌더러는 표기만 해야 한다."""
    from engine.report.html_new import _render_fx_regime

    md = render_fx_regime_section(payload)
    html = _render_fx_regime(payload)
    score = payload["fx_regime"]["score"]
    label = payload["fx_regime"]["label"]
    assert f"{score:+.0f}" in md and f"{score:+.0f}" in html
    assert label in md and label in html


def test_both_renderers_skip_together_when_data_is_missing():
    from engine.report.html_new import _render_fx_regime

    for empty in ({}, {"fx_regime": None}, {"fx_regime": {"score": None}}):
        assert render_fx_regime_section(empty) == ""
        assert _render_fx_regime(empty) == ""


def test_html_escapes_manually_entered_strings():
    """근거 문자열엔 수동 입력(fx_risk_events.yaml)에서 온 값이 섞인다 —
    그대로 HTML에 넣는 경로를 막아둔다."""
    from engine.report.html_new import _render_fx_regime

    base = build_fx_regime_payload(date(2026, 9, 9))
    poisoned = {**base, "label": "<script>alert(1)</script>"}
    out = _render_fx_regime({"fx_regime": poisoned})
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_html_section_carries_the_same_r4_disclaimer(payload):
    """R4 표기가 한쪽에만 있으면 HTML 독자는 이 섹션의 성격을 모른다."""
    from engine.report.html_new import _render_fx_regime

    html = _render_fx_regime(payload)
    assert "포지션 지시 아님" in html
    assert "추천 아님" in html
    assert "목표 환율은 제시하지 않는다" in html
