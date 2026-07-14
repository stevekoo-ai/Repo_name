"""Markdown report renderer (Master Instruction 16, 17, 25).

Pure rendering — every number here already comes from engine/report/payload.py.
This module only turns the payload into prose following the section order
(config/report.yaml `sections`) and the [사실]/[해석]/[시나리오]/[행동]
sentence structure required by 17.2 wherever a judgment is being stated.
"""
from __future__ import annotations

from core.models import DataStatus

STATUS_KR = {
    DataStatus.OK.value: "OK",
    DataStatus.PENDING.value: "Pending",
    DataStatus.NOT_RELEASED.value: "Not Released",
    DataStatus.SOURCE_ERROR.value: "Source Error",
}

INDICATOR_SECTIONS = [
    ("gdp", "GDP"), ("industrial_production", "산업생산"), ("retail_sales", "소매판매"),
    ("exports", "수출"), ("semiconductor_exports", "반도체"), ("current_account", "경상수지"),
    ("cpi", "CPI"), ("ppi", "PPI"), ("unemployment", "실업률"), ("us_global", "미국/글로벌"),
]


def _fmt(value, suffix: str = "") -> str:
    if value is None:
        return "Pending"
    if isinstance(value, float):
        return f"{value:.2f}{suffix}"
    return f"{value}{suffix}"


def _executive_summary(payload: dict) -> str:
    macro = payload["macro"]
    brief = payload["personal_executive_brief"]
    top_action = payload["actions"][0] if payload["actions"] else None
    lines = [
        "## 1. Executive Summary",
        f"- 현재 경기 국면: **{macro['regime']}** ({macro['score_band_label']}, 총점 {macro['score']})",
        f"- 지난달 대비 변화: {macro['previous_regime']} → {macro['regime']}"
        + (f" ({macro['transition']})" if macro["transition"] else " (변동 없음)"),
        "- 핵심 원인: " + ("; ".join(c["message"] for c in macro["changes"][:3]) if macro["changes"] else "데이터 부족"),
        f"- 사용자에게 중요한 의미: {brief['one_line_diagnosis']}",
        "- 이번 달 핵심 행동: " + (f"[행동] {top_action['title']}" if top_action else "[행동] 핵심 지표 확보 후 재평가 필요"),
        f"- 리포트 충족도: **{payload['report_readiness']}** (Confidence {macro['confidence']}점)",
    ]
    return "\n".join(lines)


def _monthly_key_changes(payload: dict) -> str:
    lines = ["## 2. 이번 달 핵심 변화"]
    for c in payload["macro"]["changes"]:
        lines.append(f"- [사실] {c['message']}")
    return "\n".join(lines)


def _macro_dashboard(payload: dict) -> str:
    lines = ["## 3. Macro Dashboard", "", "| 지표 | 현재 | 이전 | 추세 | 점수 | 출처 |", "|---|---|---|---|---|---|"]
    for row in payload["macro_dashboard"]:
        lines.append(
            f"| {row['indicator']} | {_fmt(row['current'])} | {_fmt(row['previous'])} | "
            f"{row['trend']} | {_fmt(row['score'])} | {row['source'] or STATUS_KR.get(row['status'], row['status'])} |"
        )
    return "\n".join(lines)


def _regime_judgement(payload: dict) -> str:
    macro = payload["macro"]
    lines = [
        "## 4. 경기 판정",
        f"- 총점: {macro['score']} (가중 점수 {macro['weighted_score']})",
        f"- Regime: {macro['regime']}",
        f"- Confidence: {macro['confidence']}점 "
        f"(신선도 {macro['confidence_components']['data_freshness']}, 출처품질 {macro['confidence_components']['source_quality']}, "
        f"일관성 {macro['confidence_components']['indicator_consistency']}, 안정성 {macro['confidence_components']['trend_stability']})",
        "- Warning: " + (", ".join(macro["warnings"]) if macro["warnings"] else "없음"),
    ]
    clock = macro.get("us_investment_clock")
    if clock:
        staleness = " (실시간)" if clock.get("source") == "live" else " (최근 저장값, 실시간 조회 불가)"
        lines.append(
            f"- 참고(미국 Investment Clock{staleness}): **{clock['phase_kr']}** 국면 — "
            f"유리 자산군 **{clock['favored_asset_kr']}** (기준일 {clock['as_of']}, "
            f"성장 {clock['growth_signal']} / 물가 {clock['inflation_signal']})"
        )
        if clock.get("note"):
            lines.append(f"  - {clock['note']}")
    else:
        lines.append("- 참고(미국 Investment Clock): 데이터 없음 (Pending)")
    return "\n".join(lines)


def _indicator_deep_dive(payload: dict) -> str:
    lines = ["## 5. 지표별 분석"]
    # payload["macro_dashboard"] is built from INDICATOR_ORDER, same order as INDICATOR_SECTIONS.
    readings = payload["macro_dashboard"]
    for row, (_, title) in zip(readings, INDICATOR_SECTIONS):
        lines.append(f"### {title}")
        if row["status"] != "ok":
            lines.append(f"- [사실] 데이터 상태: {STATUS_KR.get(row['status'], row['status'])} — 판단 보류.")
            continue
        trend_word = {1: "개선", 0: "보합", -1: "악화"}.get(row["score"], "N/A")
        lines.append(f"- [사실] 현재 값 {_fmt(row['current'])} (출처: {row['source']}).")
        lines.append(f"- [해석] 전월 대비 추세는 '{trend_word}'이며 규칙엔진 점수는 {row['score']}이다.")
        lines.append("- [행동] Action Plan 항목 참고 — 관련 조치가 있으면 10절에 반영됨.")
    return "\n".join(lines)


_BIAS_LABEL_KR = {"stock_bias": "주식", "etf_bias": "ETF", "bond_bias": "채권", "cash_bias": "현금"}


def _personal_analysis(payload: dict) -> str:
    p = payload["personal"]
    bias_text = ""
    if p["investment_biases"]:
        bias_text = ", 편향: " + ", ".join(
            f"{_BIAS_LABEL_KR.get(k, k)} {v}" for k, v in p["investment_biases"].items()
        )
    lines = [
        "## 6. 사용자 맞춤 분석",
        f"- 직업 관점: 반도체/AI 인프라 종사자 — 반도체 점수 {_fmt(p['semiconductor_score'], '점')}"
        f"({p['semiconductor_band']})은 업황과 성과급 사이클에 직접 연결된다.",
        f"- 투자 관점: Investment Environment {_fmt(p['investment_environment_score'], '점')}{bias_text}",
        f"- 채권 관점: Bond Score {_fmt(p['bond_score'], '점')}.",
        f"- 환율 관점: FX Score {_fmt(p['fx_score'], '점')}.",
        f"- 공공분양 관점: Housing Readiness {_fmt(p['housing_readiness_score'], '점')}.",
        "- 출장/여행 관점: 11절 경제 캘린더 및 Action Plan의 환전 관련 항목 참고.",
    ]
    return "\n".join(lines)


def _asset_impact(payload: dict) -> str:
    labels = {"stocks": "주식", "etf": "ETF", "bond": "채권", "cash": "현금",
              "subscription_fund": "청약 자금", "fx_exposure": "환율"}
    lines = ["## 7. 자산별 영향 분석"]
    for key, label in labels.items():
        a = payload["assets"].get(key, {})
        if a.get("score") is None:
            lines.append(f"- {label}: Pending (데이터 부족)")
            continue
        lines.append(f"- {label}: {a['stars']} ({a['score']}점)")
    return "\n".join(lines)


def _scenario_analysis(payload: dict) -> str:
    s = payload["scenarios"]
    lines = ["## 8. 시나리오 분석"]
    for name, label in (("base", "Base"), ("bull", "Bull"), ("bear", "Bear")):
        sc = s[name]
        lines.append(f"### {label} ({sc['probability']}%)")
        lines.append(f"- [시나리오] 전제: {sc['premise']}")
        lines.append(f"- 기대되는 변화: {sc['expected_change']}")
        lines.append(f"- 사용자 영향: {sc['user_impact']}")
    lines.append("### 깨지는 조건")
    for cond in s["invalid_conditions"]:
        lines.append(f"- {cond}")
    return "\n".join(lines)


def _discussion_points(payload: dict) -> str:
    points = payload.get("discussion_points", [])
    lines = ["## 9. 논의가 필요한 결정 사항"]
    if not points:
        lines.append("- 이번 달은 별도로 논의가 필요한 항목이 없습니다.")
        return "\n".join(lines)
    for p in points:
        lines.append(f"### {p['topic']}")
        lines.append(f"- [사실] {p['context']}")
        lines.append(f"- [질문] {p['question']}")
    return "\n".join(lines)


def _action_plan(payload: dict) -> str:
    lines = ["## 10. 이번 달 Action Plan"]
    tiers = [
        (5, "★★★★★ 반드시 확인 / 실행"), (4, "★★★★☆ 검토"), (3, "★★★☆☆ 관찰"),
        (2, "★★☆☆☆ 참고"), (1, "보류"),
    ]
    actions_by_tier = {t: [] for t, _ in tiers}
    for a in payload["actions"]:
        actions_by_tier.setdefault(a["priority"], []).append(a)

    for tier, tier_label in tiers:
        items = actions_by_tier.get(tier, [])
        if not items:
            continue
        lines.append(f"### {tier_label}")
        for a in items:
            lines.append(f"- **[행동] {a['title']}**")
            lines.append(f"  - [이유] {a['reason']}")
            lines.append(f"  - [보류 조건] {a['invalid_condition']}")
            lines.append(f"  - [재점검] {a['recheck']}")
            if a.get("conflict_note"):
                lines.append(f"  - [조정] {a['conflict_note']}")
    return "\n".join(lines)


def _calendar(payload: dict) -> str:
    lines = ["## 11. 경제 캘린더", "", "| 날짜 | 이벤트 | 중요도 | 사용자 영향 |", "|---|---|---|---|"]
    for ev in payload["calendar"]:
        lines.append(f"| {ev['date']} | {ev['name']} | {ev['importance_label']} | {ev['priority_score']}점 |")
    if not payload["calendar"]:
        lines.append("| - | 확정된 일정 없음 (data/manual_inputs/calendar.yaml 갱신 필요) | - | - |")
    return "\n".join(lines)


def _personal_brief(payload: dict) -> str:
    b = payload["personal_executive_brief"]
    lines = [
        "## 12. Personal Executive Brief",
        f"- 이번 달 한 줄 진단: {b['one_line_diagnosis']}",
        "- 자산별 영향 요약: " + ", ".join(f"{k}={v}" for k, v in b["asset_summary"].items() if v),
        "- 중요한 이벤트 TOP 5: " + ("; ".join(b["top_events"]) if b["top_events"] else "없음"),
        f"- 최종 제안: [행동] {b['final_suggestion']}",
    ]
    return "\n".join(lines)


def _appendix(payload: dict) -> str:
    a = payload["appendix"]
    lines = ["## 12. Appendix", "- 데이터 출처: " + (", ".join(a["sources"]) if a["sources"] else "N/A"),
              f"- 지난달 Regime: {a['previous_month_regime'] or 'N/A'}", "- 용어 설명:"]
    for term, desc in a["glossary"].items():
        lines.append(f"  - **{term}**: {desc}")
    return "\n".join(lines)


def render_markdown(payload: dict) -> str:
    header = f"# 월간 PEOS 리포트 - {payload['report_month']}\n"
    sections = [
        _executive_summary(payload), _monthly_key_changes(payload), _macro_dashboard(payload),
        _regime_judgement(payload), _indicator_deep_dive(payload), _personal_analysis(payload),
        _asset_impact(payload), _scenario_analysis(payload), _discussion_points(payload),
        _action_plan(payload), _calendar(payload), _personal_brief(payload), _appendix(payload),
    ]
    return header + "\n\n" + "\n\n".join(sections) + "\n"
