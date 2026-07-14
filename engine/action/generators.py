"""Action candidate generators (Master Instruction 15.1-15.5).

Each function inspects one engine's output and yields zero or more action
candidates: {title, reason, invalid_condition, recheck, category,
factors: {user_relevance, risk_level, time_urgency, portfolio_impact,
event_significance}}. engine/action/engine.py scores and ranks the
combined list; engine/action/conflict.py resolves cross-category tension.

`category` must be one of config/rules.yaml `conflict_resolver_priority`.
"""
from __future__ import annotations


def _candidate(title, reason, invalid_condition, recheck, category,
                user_relevance=50, risk_level=50, time_urgency=50,
                portfolio_impact=50, event_significance=50) -> dict:
    return {
        "title": title,
        "reason": reason,
        "invalid_condition": invalid_condition,
        "recheck": recheck,
        "category": category,
        "factors": {
            "user_relevance": user_relevance,
            "risk_level": risk_level,
            "time_urgency": time_urgency,
            "portfolio_impact": portfolio_impact,
            "event_significance": event_significance,
        },
    }


def from_macro_warnings(macro_payload: dict) -> list[dict]:
    out = []
    for label in macro_payload.get("warnings_kr", []):
        out.append(_candidate(
            title=f"{label} 관련 지표 재확인",
            reason=f"11.9 즉시 경고 규칙에 해당하는 신호({label})가 감지되었다.",
            invalid_condition="다음 달 지표에서 해당 신호가 해소되면 경고 해제.",
            recheck="다음 정기 리포트(익월) 또는 관련 지표 발표 직후.",
            category="macro_risk",
            user_relevance=70, risk_level=90, time_urgency=75, portfolio_impact=60, event_significance=55,
        ))
    if macro_payload.get("transition") == "downgrade":
        out.append(_candidate(
            title=f"경기 국면 강등 배경 점검 ({macro_payload.get('previous_regime')} → {macro_payload.get('regime')})",
            reason="11.8 강등 규칙 조건이 2개 이상 충족되어 국면이 한 단계 하향되었다.",
            invalid_condition="다음 달 상향 조건(11.10) 충족 시 판단 재검토.",
            recheck="다음 정기 리포트.",
            category="macro_risk",
            user_relevance=75, risk_level=85, time_urgency=70, portfolio_impact=70, event_significance=60,
        ))
    return out


def from_semiconductor(semiconductor: dict) -> list[dict]:
    if semiconductor.get("data_status") != "ok":
        return []
    band = semiconductor.get("status_band")
    label = semiconductor.get("status_label_kr")
    if band in ("strong_positive", "positive"):
        return [_candidate(
            title="메모리/AI 인프라 비중 유지 또는 확대 검토",
            reason=f"반도체 종합 점수 {semiconductor['semiconductor_score']}점({label}) — 메모리 사이클과 AI 인프라 투자 모두 순풍.",
            invalid_condition="DRAM/NAND 가격 추세 반전 또는 CSP CapEx 가이던스 하향 시 보류.",
            recheck="Micron/SK hynix/TSMC 분기 실적 발표 직후.",
            category="industry_cycle",
            user_relevance=95, risk_level=40, time_urgency=45, portfolio_impact=85, event_significance=70,
        )]
    if band in ("cautious", "weak_risk"):
        return [_candidate(
            title="반도체 비중 축소/헤지 필요성 점검",
            reason=f"반도체 종합 점수 {semiconductor['semiconductor_score']}점({label}) — 업황 둔화 시그널 우세.",
            invalid_condition="메모리 가격/가이던스 반등 확인 시 보류.",
            recheck="다음 달 반도체 수출 및 주요 기업 실적 발표.",
            category="macro_risk",
            user_relevance=90, risk_level=75, time_urgency=55, portfolio_impact=85, event_significance=65,
        )]
    return []


def from_investment(investment: dict) -> list[dict]:
    if investment.get("data_status") != "ok" or not investment.get("biases"):
        return []
    biases = investment["biases"]
    env_score = investment["investment_environment_score"]
    out = []
    if biases["stock_bias"] in ("확대", "소폭 확대"):
        out.append(_candidate(
            title="주식/ETF 비중 확대 검토",
            reason=f"Investment Environment Score {env_score}점 — 거시/반도체 환경이 우호적.",
            invalid_condition="Investment Environment Score가 20점 이상 하락하면 보류.",
            recheck="다음 정기 리포트.",
            category="investment_opportunity",
            user_relevance=85, risk_level=45, time_urgency=40, portfolio_impact=80, event_significance=50,
        ))
    else:
        out.append(_candidate(
            title="주식/ETF 비중 축소 또는 방어적 재배분 검토",
            reason=f"Investment Environment Score {env_score}점 — 거시/반도체 환경이 비우호적.",
            invalid_condition="Investment Environment Score 반등 시 보류.",
            recheck="다음 정기 리포트.",
            category="macro_risk",
            user_relevance=85, risk_level=70, time_urgency=50, portfolio_impact=80, event_significance=50,
        ))
    return out


def from_bond(bond: dict) -> list[dict]:
    if bond.get("data_status") != "ok":
        return []
    score = bond["bond_score"]
    if score >= 55:
        return [_candidate(
            title="채권 비중 추가 확대 여부를 검토한다",
            reason="금리 완화 기대가 형성되고 있으나 물가 둔화 확인이 추가로 필요하다.",
            invalid_condition="CPI 재가속 또는 장기금리 급등 시 보류.",
            recheck="미국 CPI 및 한국은행 금통위 이후 재검토.",
            category="investment_opportunity",
            user_relevance=70, risk_level=35, time_urgency=45, portfolio_impact=60, event_significance=55,
        )]
    if score <= 40:
        return [_candidate(
            title="채권 신규 매수 보류 및 만기 재투자 방식 재검토",
            reason=f"Bond Score {score}점 — 금리/실질금리 매력도가 낮은 국면.",
            invalid_condition="실질금리 매력도 회복 또는 성장 둔화 신호 확산 시 재검토.",
            recheck="다음 금통위/FOMC 이후.",
            category="investment_opportunity",
            user_relevance=60, risk_level=35, time_urgency=30, portfolio_impact=50, event_significance=45,
        )]
    return []


def from_fx_and_travel(fx: dict, travel: dict) -> list[dict]:
    out = []
    for trip in travel.get("trips", []):
        if trip.get("data_status") != "ok":
            continue
        favorable = trip["score"] >= 60
        fx_known = fx.get("fx_score") is not None
        if favorable:
            reason = f"{trip['name']}: 환전 유리도 {trip['score']}점 — 현재 환율/시점이 상대적으로 유리."
            action_title = f"{trip['name']} 환전 실행 검토"
        else:
            # 15.6 conflict example: unfavorable FX doesn't cancel a confirmed trip — split conversion instead.
            reason = (f"{trip['name']}: 환전 유리도 {trip['score']}점으로 낮지만 일정이 확정되어 있어 "
                      "환전을 전면 보류하기보다 분할 환전으로 리스크를 분산하는 것이 합리적이다.")
            action_title = f"{trip['name']} 분할 환전 검토"
        out.append(_candidate(
            title=action_title, reason=reason,
            invalid_condition="출국일 이전 환율이 추가로 5% 이상 불리하게 움직이면 재검토.",
            recheck=f"{trip.get('departure_date', '출국')} 2주 전.",
            category="travel_discretionary" if trip.get("type") == "leisure" else "liquidity_survival",
            user_relevance=65 if fx_known else 45, risk_level=40, time_urgency=70, portfolio_impact=35,
            event_significance=40,
        ))
    return out


def from_housing(housing: dict) -> list[dict]:
    out = []
    for notice in housing.get("notices", []):
        if notice.get("data_status") != "ok":
            continue
        out.append(_candidate(
            title=f"{notice['name']} 청약 자격/자금 점검",
            reason=f"청약 준비도 {notice['readiness_score']}점 — 신청 전 자격/자금 요건 재확인 필요.",
            invalid_condition="공고가 취소되거나 자격 요건 미충족이 확인되면 보류.",
            recheck=f"{notice.get('application_start', '접수 시작일')} 1주 전.",
            category="liquidity_survival",
            user_relevance=90, risk_level=55, time_urgency=65, portfolio_impact=75, event_significance=60,
        ))
        pc = notice.get("platform_city_analysis")
        if pc and pc.get("funding_gap_krw") and pc["funding_gap_krw"] > 0:
            out.append(_candidate(
                title=f"{notice['name']} 자금 갭 {pc['funding_gap_krw']:,.0f}원 확보 계획 수립",
                reason="목표 자금 대비 현재 청약저축/현금 잔액이 부족하다.",
                invalid_condition="공고가 취소되거나 자금 목표가 조정되면 보류.",
                recheck=f"{notice.get('application_start', '접수 시작일')} 1개월 전.",
                category="liquidity_survival",
                user_relevance=95, risk_level=70, time_urgency=75, portfolio_impact=90, event_significance=60,
            ))
    return out


def from_calendar(calendar_events: list[dict], top_n: int = 5) -> list[dict]:
    out = []
    for ev in calendar_events[:top_n]:
        out.append(_candidate(
            title=f"{ev['name']} 확인 ({ev['date']})",
            reason=f"우선순위 점수 {ev['priority_score']}점, {ev['importance_label']} — D-{ev['days_until']}.",
            invalid_condition="일정이 연기되면 재점검 시점도 함께 조정.",
            recheck=f"{ev['date']} 당일 또는 직후.",
            category="macro_risk" if ev.get("category", "").startswith(("us_", "kr_")) else "industry_cycle",
            user_relevance=ev.get("priority_score", 50), risk_level=40,
            time_urgency=max(0, 100 - ev["days_until"] * 2.5), portfolio_impact=ev.get("priority_score", 50),
            event_significance=ev.get("priority_score", 50),
        ))
    return out
