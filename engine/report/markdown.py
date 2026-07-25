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
    DataStatus.STALE.value: "이전 값 유지",
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


def _macro_dashboard_rows(rows_data: list[dict]) -> list[str]:
    lines = ["| 지표 | 현재 | 이전 | 추세 | 점수 | 출처 |", "|---|---|---|---|---|---|"]
    for row in rows_data:
        current = _fmt(row["current"]) + (" ‡" if row.get("status") == "stale" else "")
        lines.append(
            f"| {row['indicator']} | {current} | {_fmt(row['previous'])} | "
            f"{row['trend']} | {_fmt(row['score'])} | {row['source'] or STATUS_KR.get(row['status'], row['status'])} |"
        )
    if any(r.get("status") == "stale" for r in rows_data):
        lines.append("")
        lines.append("‡ 오늘 실시간 조회에 실패한 지표 — 마지막으로 확인된 값을 그대로 유지해 표시 (추측/대체 데이터 아님).")
    return lines


def _us_macro_dashboard(payload: dict) -> str:
    lines = ["## 1. Macro Dashboard — 미국 (큰 그림)", ""] + _macro_dashboard_rows(payload["us_macro_dashboard"])
    return "\n".join(lines)


def _us_regime_judgement(payload: dict) -> str:
    macro_us = payload["macro_us"]
    lines = [
        "## 2. 미국 경기 판정",
        f"- 총점: {macro_us['score']} (가중 점수 {macro_us['weighted_score']})",
        f"- Regime: {macro_us['regime']}",
        f"- Confidence: {macro_us['confidence']}점",
        "- Warning: " + (", ".join(macro_us["warnings"]) if macro_us["warnings"] else "없음"),
    ]
    return "\n".join(lines)


def _kr_us_comparison(payload: dict) -> str:
    cmp_ = payload["kr_us_comparison"]
    lines = [
        "## 5. 한국은 미국의 흐름에 실려 있는가",
        f"- 미국 국면: **{cmp_['us_regime']}** / 한국 국면: **{cmp_['kr_regime']}**",
        f"- [해석] {cmp_['narrative']}",
        "", "| 지표 | 한국 점수 | 미국 점수 | 관계 |", "|---|---|---|---|",
    ]
    for p in cmp_["indicator_pairs"]:
        relationship_kr = {"sync": "동조", "diverge": "디커플링", "data_unavailable": "데이터 부족"}.get(p["relationship"], p["relationship"])
        lines.append(f"| {p['label']} | {_fmt(p['kr_score'])} | {_fmt(p['us_score'])} | {relationship_kr} |")
    return "\n".join(lines)


def _executive_summary(payload: dict) -> str:
    macro = payload["macro"]
    brief = payload["personal_executive_brief"]
    top_action = payload["actions"][0] if payload["actions"] else None
    daily_history = payload.get("daily_history_summary", {})

    lines = [
        "## 6. Executive Summary",
        f"- 현재 경기 국면: **{macro['regime']}** ({macro['score_band_label']}, 총점 {macro['score']})",
        f"- 지난달 대비 변화: {macro['previous_regime']} → {macro['regime']}"
        + (f" ({macro['transition']})" if macro["transition"] else " (변동 없음)"),
        "- 핵심 원인: " + ("; ".join(c["message"] for c in macro["changes"][:3]) if macro["changes"] else "데이터 부족"),
        f"- 사용자에게 중요한 의미: {brief['one_line_diagnosis']}",
        "- 이번 달 핵심 행동: " + (f"[행동] {top_action['title']}" if top_action else "[행동] 핵심 지표 확보 후 재평가 필요"),
        f"- 리포트 충족도: **{payload['report_readiness']}** (Confidence {macro['confidence']}점)",
    ]

    # 일일 이력 요약 추가
    if daily_history.get("status") == "ok":
        trend = daily_history.get("trend_summary", {})
        trend_notes = []
        if not trend.get("kr_regime_stable"):
            trend_notes.append("한국 국면 변화")
        kr_conf_change = trend.get("kr_confidence_change")
        if kr_conf_change and abs(kr_conf_change) > 5:
            direction = "상승" if kr_conf_change > 0 else "하락"
            trend_notes.append(f"신뢰도 {direction} ({kr_conf_change:+.1f}%p)")
        investment_trend = trend.get("investment_env_trend", 0)
        if investment_trend and abs(investment_trend) > 2:
            direction = "개선" if investment_trend > 0 else "악화"
            trend_notes.append(f"투자환경 {direction}")
        if trend_notes:
            lines.append(f"- **월간 일일 추이**: {', '.join(trend_notes)}")

    return "\n".join(lines)


def _monthly_key_changes(payload: dict) -> str:
    lines = ["## 7. 이번 달 핵심 변화"]
    for c in payload["macro"]["changes"]:
        lines.append(f"- [사실] {c['message']}")
    return "\n".join(lines)


def _macro_dashboard(payload: dict) -> str:
    lines = ["## 3. Macro Dashboard — 한국", ""] + _macro_dashboard_rows(payload["macro_dashboard"])
    return "\n".join(lines)


def _regime_judgement(payload: dict) -> str:
    macro = payload["macro"]
    lines = [
        "## 4. 한국 경기 판정",
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
    lines = ["## 8. 지표별 분석"]
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
        lines.append("- [행동] Action Plan 항목 참고 — 관련 조치가 있으면 13절에 반영됨.")
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
        "## 9. 사용자 맞춤 분석",
        f"- 직업 관점: 반도체/AI 인프라 종사자 — 반도체 점수 {_fmt(p['semiconductor_score'], '점')}"
        f"({p['semiconductor_band']})은 업황과 성과급 사이클에 직접 연결된다.",
        f"- 투자 관점: Investment Environment {_fmt(p['investment_environment_score'], '점')}{bias_text}",
        f"- 채권 관점: Bond Score {_fmt(p['bond_score'], '점')}.",
        f"- 환율 관점: FX Score {_fmt(p['fx_score'], '점')}.",
        f"- 공공분양 관점: Housing Readiness {_fmt(p['housing_readiness_score'], '점')}.",
        "- 출장/여행 관점: 14절 경제 캘린더 및 Action Plan의 환전 관련 항목 참고.",
    ]
    return "\n".join(lines)


def _asset_impact(payload: dict) -> str:
    labels = {"stocks": "주식", "etf": "ETF", "bond": "채권", "cash": "현금",
              "subscription_fund": "청약 자금", "fx_exposure": "환율"}
    lines = ["## 10. 자산별 영향 분석"]
    for key, label in labels.items():
        a = payload["assets"].get(key, {})
        if a.get("score") is None:
            lines.append(f"- {label}: Pending (데이터 부족)")
            continue
        lines.append(f"- {label}: {a['stars']} ({a['score']}점)")
    return "\n".join(lines)


def _scenario_analysis(payload: dict) -> str:
    s = payload["scenarios"]
    lines = ["## 11. 시나리오 분석"]
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
    lines = ["## 12. 논의가 필요한 결정 사항"]
    if not points:
        lines.append("- 이번 달은 별도로 논의가 필요한 항목이 없습니다.")
        return "\n".join(lines)
    for p in points:
        lines.append(f"### {p['topic']}")
        lines.append(f"- [사실] {p['context']}")
        lines.append(f"- [질문] {p['question']}")
    return "\n".join(lines)


def _action_plan(payload: dict) -> str:
    lines = ["## 13. 이번 달 Action Plan"]
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
    lines = ["## 14. 경제 캘린더", "", "| 날짜 | 이벤트 | 중요도 | 사용자 영향 |", "|---|---|---|---|"]
    for ev in payload["calendar"]:
        lines.append(f"| {ev['date']} | {ev['name']} | {ev['importance_label']} | {ev['priority_score']}점 |")
    if not payload["calendar"]:
        lines.append("| - | 확정된 일정 없음 (data/manual_inputs/calendar.yaml 갱신 필요) | - | - |")
    return "\n".join(lines)


def _personal_brief(payload: dict) -> str:
    b = payload["personal_executive_brief"]
    lines = [
        "## 15. Personal Executive Brief",
        f"- 이번 달 한 줄 진단: {b['one_line_diagnosis']}",
        "- 자산별 영향 요약: " + ", ".join(f"{k}={v}" for k, v in b["asset_summary"].items() if v),
        "- 중요한 이벤트 TOP 5: " + ("; ".join(b["top_events"]) if b["top_events"] else "없음"),
        f"- 최종 제안: [행동] {b['final_suggestion']}",
    ]
    return "\n".join(lines)


def _rate_analysis(payload: dict) -> str:
    """Render interest rate analysis section (US/KR yield comparison and portfolio strategy)."""
    if "rate_analysis" not in payload or not payload["rate_analysis"]:
        return ""

    ra = payload["rate_analysis"]
    score = ra.get("total_score", 0)

    # Determine score interpretation
    if score >= 85:
        interpretation = "극도 완화 (Extreme easing) — 공격적 성장 전략"
    elif score >= 70:
        interpretation = "완화 사이클 (Easing) — 성장 지향"
    elif score >= 55:
        interpretation = "중립~약한 완화 (Neutral-Accommodative) — 균형 배분"
    elif score >= 40:
        interpretation = "긴축 사이클 (Tightening) — 방어적 전략"
    else:
        interpretation = "극도 긴축 (Extreme tightening) — 극도 방어적"

    rates = ra.get("current_rates", {})
    trends = ra.get("trends", {})
    portfolio = ra.get("portfolio_recommendation", {})
    hynix = ra.get("sk_hynix_outlook", {})

    lines = [
        "## 금리 분석 (Interest Rate Environment)",
        "",
        f"**금리 점수: {score}/100 ({interpretation})**",
        "",
        "### 점수 구성",
        f"| 항목 | 점수 | 만점 |",
        "|------|------|------|",
        f"| 절대 금리 수준 | {ra['score_components'].get('absolute_rates', 0)} | 30 |",
        f"| 추이 분석 | {ra['score_components'].get('trend_analysis', 0)} | 30 |",
        f"| Yield Spread | {ra['score_components'].get('spread', 0)} | 25 |",
        f"| 시장 신호 | {ra['score_components'].get('market_signals', 0)} | 15 |",
        "",
        "### 현재 금리 상황",
        f"- **미국 10Y Treasury**: {_fmt(rates.get('us_10y'), '%')}",
        f"- **한국 10Y 국고채**: {_fmt(rates.get('kr_10y'), '%')}",
        f"- **Spread (US-KR)**: {_fmt(rates.get('spread_bp'), 'bp')}",
        f"  - 기준: 200~250bp | 현재: {('**정상 범위**' if rates.get('spread_bp') is not None and 150 <= rates['spread_bp'] <= 300 else '**주의 필요**')}",
        "",
        "### 추이 신호",
        f"- **미국 10Y 1개월 변화**: {_fmt(trends.get('us_10y_1m_change_bp'), 'bp')}",
        f"- **3개월 추세**: {'상승 (긴축)' if trends.get('us_10y_3m_trend') == 'up' else '하강 (완화)'}",
        "",
        "### 시장 신호",
        f"- **역수익 곡선 (10Y-2Y)**: {_fmt(ra.get('market_signal', {}).get('us_10y_2y_spread'), '%')}",
        f"- **상태**: {'**정상** (경기순환 양호)' if ra.get('market_signal', {}).get('yield_curve_status') == 'normal' else '⚠️ **역수익** (경기약세 경고)'}",
        "",
        "### 포트폴리오 전략",
        f"**권장 자산 배분**: 주식 {portfolio.get('stocks', 50)}% + 채권 {portfolio.get('bonds', 30)}% + 현금 {portfolio.get('cash', 20)}%",
        f"**기본 원칙**: {portfolio.get('condition', 'N/A')}",
        f"**리밸런싱 트리거**: 점수 {portfolio.get('rebalance_trigger', 0)}점 이상/이하 변화",
        "",
        "### SK Hynix 관점",
        f"- **3개월 상승 가능성**: {hynix.get('3m_upside_probability', 50)}%",
        f"- **6개월 상승 가능성**: {hynix.get('6m_upside_probability', 50)}%",
        f"- **12개월 상승 가능성**: {hynix.get('12m_upside_probability', 50)}%",
        f"- **근거**: {hynix.get('rationale', 'N/A')}",
        "",
    ]

    return "\n".join(lines)


def _appendix(payload: dict) -> str:
    a = payload["appendix"]
    lines = ["## 16. Appendix", "- 데이터 출처: " + (", ".join(a["sources"]) if a["sources"] else "N/A"),
              f"- 지난달 Regime: {a['previous_month_regime'] or 'N/A'}", "- 용어 설명:"]
    for term, desc in a["glossary"].items():
        lines.append(f"  - **{term}**: {desc}")
    return "\n".join(lines)


def _cci_analysis(payload: dict) -> str:
    """Comprehensive Crisis Index analysis with SK Hynix trading signals."""
    if "cci_analysis" not in payload:
        return ""

    cci = payload["cci_analysis"]
    state_emoji = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}
    state = cci["state"]
    score = cci["total_score"]

    lines = [
        f"## 위기지수 분석 (Comprehensive Crisis Index)",
        f"**상태: {state_emoji.get(state, '?')} {state}** | **점수: {score}/100**",
        "",
        "| 지표 | 점수 | 해석 |",
        "|------|------|------|",
        f"| Sahm Rule (고용 모멘텀) | {cci['score_components']['sahm']}/20 | US 실업률 3개월 MA 추이 |",
        f"| Yield Curve (수익률곡선) | {cci['score_components']['yield_curve']}/15 | 10Y-2Y, 10Y-3M 스프레드 |",
        f"| Harvey Filter (3개월 검증) | {cci['score_components']['harvey']}/15 | 장기 수익률곡선 역전 신호 |",
        f"| Copper-Gold Ratio | {cci['score_components']['copper_gold']}/10 | 산업 수요 vs 안전자산 선호 |",
        f"| HY Credit OAS | {cci['score_components']['credit_oas']}/15 | 신용 긴축 및 유동성 지수 |",
        f"| Buffett Indicator | {cci['score_components']['buffett']}/5 | 거시 가치평가 지표 |",
        f"| Rule of 20 | {cci['score_components']['rule_of_20']}/5 | PER + 인플레이션 조정 |",
        f"| K-Sahm Rule (한국 고용) | {cci['score_components']['k_sahm']}/5 | 국내 일자리 악화 신호 |",
        f"| 반도체 산업사이클 | {cci['score_components']['semiconductor']}/10 | 출하-재고 사이클 추이 |",
        "",
    ]

    if cci["raw_values"]["ur_ma3"] is not None:
        lines.append(f"**주요 지표 현황:**")
        lines.append(f"- 미국 실업률 3M MA: {cci['raw_values']['ur_ma3']}%")
        lines.append(f"- 10Y-2Y 스프레드: {cci['raw_values']['spread_10y2y']}%p")
        lines.append(f"- HY OAS: {cci['raw_values']['hy_oas']}%")
        lines.append("")

    # 각 법칙별 상세 해석
    lines.append("### 각 리스크 신호별 해석")
    lines.append("")

    # Sahm Rule
    sahm_score = cci['score_components']['sahm']
    lines.append(f"**1. Sahm Rule (고용 모멘텀)** — {sahm_score}/20")
    if sahm_score >= 15:
        lines.append("- ⚠️ **경고 신호**: 미국 실업률 3개월 이동평균이 최근 12개월 최저치에서 0.5%p 이상 상승했으며, 고용이 급격히 악화 중")
        lines.append("- **경제 의미**: 금리 인상 효과가 고용 시장에까지 파급. 경기 침체 초기 신호")
        lines.append("- **사용자 영향**: SK하이닉스 매출 감소 가능성, 보유 ETF 수익률 악화 우려")
    elif sahm_score >= 8:
        lines.append("- ⚡ **주의 신호**: 실업률이 소폭 상승 추세. 고용 시장의 약화 신호 but 아직 심각하지 않음")
        lines.append("- **경제 의미**: 경기 둔화 국면으로 진입하는 중")
        lines.append("- **사용자 영향**: 대기 자금 확충 검토")
    else:
        lines.append("- ✅ **안전 신호**: 실업률이 안정적이거나 하락 중. 고용 시장이 건강함")
        lines.append("- **경제 의미**: 경기 확장 또는 회복 국면 유지")
        lines.append("- **사용자 영향**: 공격적 포지션 유지 가능")
    lines.append("")

    # Yield Curve
    yc_score = cci['score_components']['yield_curve']
    lines.append(f"**2. Yield Curve (수익률곡선)** — {yc_score}/15")
    if yc_score >= 12:
        lines.append("- 🔴 **극도 경고**: 10Y-2Y 스프레드가 음수(역전)이며, 10Y-3M도 역전. 경기 침체 신호 강함")
        lines.append("- **경제 의미**: 시장이 향후 경기 침체를 선반영. 장기 금리가 단기보다 낮다는 것은 안전자산 선호 신호")
        lines.append("- **사용자 영향**: 채권 비중 확대, 공격성 자산 축소 시점. 청약 기회 관찰")
    elif yc_score >= 6:
        lines.append("- ⚡ **주의**: 스프레드가 200bp 이하로 축소. 금리 인상 효과가 곡선을 누르는 중")
        lines.append("- **경제 의미**: 경기 둔화 신호. 통상 6~12개월 후 경기 약세 우려")
        lines.append("- **사용자 영향**: 리스크 자산 비중 조절 시작")
    else:
        lines.append("- ✅ **정상**: 스프레드가 충분히 양수. 곡선이 건강한 상승 구조")
        lines.append("- **경제 의미**: 경기 확장 신호. 투자심리 양호")
        lines.append("- **사용자 영향**: 포지션 유지 또는 확대 검토")
    lines.append("")

    # Harvey Filter
    hf_score = cci['score_components']['harvey']
    lines.append(f"**3. Harvey Filter (장기 수익률곡선 역전 신호)** — {hf_score}/15")
    if hf_score >= 12:
        lines.append("- 🔴 **경기 침체 신호**: 지난 3개월 이상 장기 곡선이 역전 상태 지속. Sahm Rule보다 선행성 강함")
        lines.append("- **경제 의미**: 시장 전문가들이 1년 후 경기 침체를 확신하는 신호")
        lines.append("- **사용자 영향**: 방어 포지션 강화 단계")
    elif hf_score >= 6:
        lines.append("- ⚡ **추적 필요**: 최근 역전 신호. 지속 여부 모니터링")
        lines.append("- **경제 의미**: 곧 경기 둔화 가능성. 하지만 일시적일 수도")
        lines.append("- **사용자 영향**: 변동성 높은 자산 비중 축소 검토")
    else:
        lines.append("- ✅ **안전**: 곡선 역전 신호 없음. 경기 침체 임박 신호 약함")
        lines.append("- **경제 의미**: 시장의 경기 전망이 중립~긍정적")
        lines.append("- **사용자 영향**: 현재 포지션 유지")
    lines.append("")

    # Credit OAS
    coas_score = cci['score_components']['credit_oas']
    lines.append(f"**4. HY Credit OAS (신용 스프레드)** — {coas_score}/15")
    if coas_score >= 12:
        lines.append("- 🔴 **유동성 위기 신호**: 신용 스프레드 500bp 이상. 시장 불안 극고조")
        lines.append("- **경제 의미**: 기업 신용 리스크 급증. 기업 부도 우려. 금융 시스템 스트레스")
        lines.append("- **사용자 영향**: 긴급 현금화 단계. 채권 수익률 급락 우려하며 장기채 매수 기회 동시 주시")
    elif coas_score >= 6:
        lines.append("- ⚡ **경고**: 스프레드 300~500bp. 신용 리스크 높아짐")
        lines.append("- **경제 의미**: 경기 둔화에 따른 기업 부실화 우려")
        lines.append("- **사용자 영향**: 고수익률 채권 회피. 안전자산 비중 확대")
    else:
        lines.append("- ✅ **정상**: 스프레드가 300bp 이하. 신용 시장 양호")
        lines.append("- **경제 의미**: 기업 신용 환경 건강. 시장 유동성 충분")
        lines.append("- **사용자 영향**: 신용 자산 비중 유지 가능")
    lines.append("")

    # Semiconductor Cycle
    semi_score = cci['score_components']['semiconductor']
    lines.append(f"**5. 반도체 산업사이클** — {semi_score}/10")
    if semi_score >= 8:
        lines.append("- 📈 **긍정 신호**: 출하/재고 비율 정상화, 가격 안정화. 업황 회복 단계")
        lines.append("- **경제 의미**: AI/DC 인프라 투자 재개. 메모리 공급 부족 심화. 가격 인상 가능성")
        lines.append("- **사용자 영향 (SK하이닉스 직원)**: 매출 개선 → 보너스 사이클 상향. ETF 수익률 개선")
    elif semi_score >= 4:
        lines.append("- ⚡ **회복 중**: 약간의 과잉 공급 남아있으나 개선 추세")
        lines.append("- **경제 의미**: 시장 정리 진행 중. 향후 2~3개월이 중요")
        lines.append("- **사용자 영향**: SK하이닉스 지켜보기. 실적 발표 주의")
    else:
        lines.append("- 📉 **침체**: 공급 과잉, 가격 하락. 구조조정 우려")
        lines.append("- **경제 의미**: 산업 사이클 저점. 정부 지원 정책 추적")
        lines.append("- **사용자 영향**: 현금 확충. 저점 매수 기회 포착 준비")
    lines.append("")

    action = cci["sk_hynix_action"]
    lines.append(f"### SK Hynix 포지션 관리")
    lines.append(f"- **Action**: {action['action']}")
    lines.append(f"- **Max Weight**: {action['max_weight']}%")
    lines.append(f"- **Context**: {action['description']}")
    lines.append(f"- **Signal**: {action['signal']}")
    lines.append("")
    lines.append(f"### 상태 해석")
    lines.append(f"> {cci['interpretation'][state]}")

    return "\n".join(lines)


def _real_estate_trend(payload: dict) -> str:
    """국토교통부 실거래가 기반 서울/수도권/전국 가격 추세 + 청약 타겟 지역 하이라이트."""
    re_data = payload.get("real_estate")
    if not re_data:
        return ""

    lines = ["## 부동산 실거래가 동향 (국토교통부 실거래가 공개시스템)", ""]

    is_pending = re_data["fetch_status"] == "pending"
    is_dead_source_error = re_data["fetch_status"] == "source_error" and not any(
        t.get("data_status") == "ok" for t in re_data.get("tiers", {}).values()
    )
    if is_pending or is_dead_source_error:
        if is_pending:
            lines.append(f"- [사실] 데이터 상태: Pending — {re_data.get('fetch_note', 'DATA_GO_KR_KEY 미설정')}")
        else:
            lines.append(f"- [사실] 데이터 상태: Source Error — {re_data.get('fetch_note', '국토교통부 API 응답 없음')}")
        lines.append("")
        lines.append("**데이터 준비 중:** 다음 리포트에서 재시도됩니다. 아래는 채워질 정보의 형식입니다.")
        lines.append("")
        lines.append("| 지역군 | 기준월 | 평당가(만원) | MoM | 3개월 추세 | 거래량 | 시장 온도 |")
        lines.append("|---|---|---|---|---|---|---|")
        lines.append("| 서울 | - | - | - | - | - | - |")
        lines.append("| 수도권 | - | - | - | - | - | - |")
        lines.append("| 전국(대표표본) | - | - | - | - | - | - |")
        lines.append("")
        lines.append("### 청약 타겟 지역 하이라이트 — 용인 기흥구")
        lines.append("- [사실] 플랫폼시티 인근 지역의 월간 실거래가 추세")
        lines.append("- 기준: 평당가(만원), 전월비 변화율, 월간 거래량, 시장 온도(과열/보합/냉각)")
        lines.append("")
        lines.append("### 서울 구별 순위")
        lines.append("- [분석] 25개 자치구를 실거래가 상승률로 순위화")
        lines.append("- 상승 TOP 3 (Gainers)")
        lines.append("- 하락 TOP 3 (Decliners)")
        return "\n".join(lines)

    coverage = re_data.get("regions_covered")
    total = re_data.get("regions_total")
    if coverage is not None and total:
        lines.append(f"- [사실] 조회 지역 커버리지: {coverage}/{total}개 지역")
        lines.append("")

    lines += ["| 지역군 | 기준월 | 평당가(만원) | MoM | 3개월 추세 | 거래량 | 시장 온도 |",
              "|---|---|---|---|---|---|---|"]
    for tier in ("seoul", "capital_area", "nationwide"):
        t = re_data["tiers"][tier]
        if t.get("data_status") != "ok":
            lines.append(f"| {_tier_label(tier)} | - | Pending | - | - | - | - |")
            continue
        lines.append(
            f"| {t['label']} | {t['reference_month']} | {_fmt(t['price_per_pyeong_manwon'])} | "
            f"{_fmt(t['mom_change_pct'], '%')} | {_fmt(t['trend_3m_pct'], '%')} | "
            f"{_fmt(t['transaction_count'])}건 | {t['market_heat']} |"
        )
    lines.append("")
    lines.append("- [해석] '전국'은 250여개 시군구 전수조사가 아니라 8개 특·광역시 + 주요 도청소재지 대표 도시 표본 기준 추정치.")
    lines.append("")

    hl = re_data["highlight"]
    lines.append(f"### 청약 타겟 지역 하이라이트 — {hl['region_name']}")
    if hl.get("note"):
        lines.append(f"- [사실] {hl['note']}")
    if hl.get("data_status") == "ok":
        lines.append(
            f"- [사실] {hl['reference_month']} 기준 평당가 {_fmt(hl['price_per_pyeong_manwon'])}만원 "
            f"(MoM {_fmt(hl.get('mom_change_pct'), '%')}), 거래 {_fmt(hl.get('transaction_count'))}건, "
            f"시장 온도 {hl.get('market_heat', 'N/A')}"
        )
    else:
        lines.append("- [사실] 데이터 상태: Pending — 최근 조회 기간 내 확인된 실거래 없음")
    lines.append("")

    movers = re_data.get("seoul_district_movers", {})
    if movers.get("data_status") == "ok":
        lines.append("### 서울 자치구 MoM 상승/하락 TOP")
        gainers = ", ".join(f"{g['name']} ({_fmt(g['mom_change_pct'], '%')})" for g in movers["gainers"])
        decliners = ", ".join(f"{d['name']} ({_fmt(d['mom_change_pct'], '%')})" for d in movers["decliners"])
        lines.append(f"- 상승 TOP: {gainers or '데이터 부족'}")
        lines.append(f"- 하락 TOP: {decliners or '데이터 부족'}")

    return "\n".join(lines)


def _tier_label(tier: str) -> str:
    return {"seoul": "서울", "capital_area": "수도권", "nationwide": "전국(대표표본)"}.get(tier, tier)


def render_markdown(payload: dict) -> str:
    header = f"# 월간 PEOS 리포트 - {payload['report_month']}\n"
    sections = [
        _us_macro_dashboard(payload), _us_regime_judgement(payload),
        _macro_dashboard(payload), _regime_judgement(payload), _kr_us_comparison(payload),
        _executive_summary(payload), _monthly_key_changes(payload),
        _rate_analysis(payload), _cci_analysis(payload), _real_estate_trend(payload),
        _indicator_deep_dive(payload), _personal_analysis(payload),
        _asset_impact(payload), _scenario_analysis(payload), _discussion_points(payload),
        _action_plan(payload), _calendar(payload), _personal_brief(payload), _appendix(payload),
    ]
    return header + "\n\n" + "\n\n".join(sections) + "\n"
