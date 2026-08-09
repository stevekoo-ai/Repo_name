"""SK Hynix investment decision engine.

Converts HBM Cycle Score + macro trust level + external signals
into a HOLD/BUY/SELL decision with conditional price triggers.

Decision Logic:
- HOLD: Default position when macro regime is stable and HBM score is neutral
- BUY: Score ↑ + Confidence ↑ + Macro support (상승/조정) + Price pullback
- SELL: Score ↓ or Macro warning (약세/위기) + Foreign outflows detected + Price target hit

Triggers are conditional — they only activate when their preconditions are met.
"""
from __future__ import annotations

from dataclasses import dataclass

from engine.valuation.hynix_band import compute_valuation_band


@dataclass
class SKHynixDecision:
    """SK Hynix investment decision with conditional triggers."""
    signal: str  # "HOLD" | "BUY" | "SELL"
    confidence: float  # 0-100
    rationale: str  # one-line reason
    triggers: list[dict]  # conditional actions, e.g. [{"condition": "price < 1400K", "action": "매수 고려"}]
    macro_linkage: str  # how macro signals connect to this decision
    risk_flags: list[str]  # current risk indicators
    next_check: str  # when to re-evaluate
    valuation_band: dict | None = None  # Layer 0 — P/E Z-score(근사) + ERP, see engine/valuation/hynix_band.py


def compute_sk_hynix_decision(payload: dict) -> SKHynixDecision:
    """Compute SK Hynix decision based on macro + semiconductor data.

    Args:
        payload: Full report payload with macro, semiconductor, rate analysis data

    Returns:
        SKHynixDecision with signal, confidence, rationale, triggers, etc.
    """
    macro = payload["macro"]
    personal = payload["personal"]
    rate_analysis = payload.get("rate_analysis", {})
    cci_analysis = payload.get("cci_analysis", {})

    # Extract key signals
    kr_regime = macro["regime"]  # 상승|조정|약세|위기
    kr_confidence = macro["confidence"]
    kr_changes = macro.get("changes", [])
    semiconductor_score = personal.get("semiconductor_score")
    semiconductor_band = personal.get("semiconductor_band")  # 양호|정상|부진|극악
    rate_score = rate_analysis.get("total_score", 50)
    cci_state = cci_analysis.get("state", "YELLOW")  # GREEN|YELLOW|RED

    # Base signal logic
    signal = "HOLD"
    confidence = 50
    triggers = []
    risk_flags = []

    # --- LAYER 0: VALUATION BAND (added 2026-08-09) ---
    # P/E Z-score(근사, divergence 기반) + ERP. 극단치일 때만 modifier로
    # 작용 — 밸류에이션 신호가 다른 계층의 결론을 뒤집지는 않고, 확신도만
    # 조정한다(Gemini 원안의 "score += ..." 직접가산 대신 완충 방식 채택 —
    # 이미 4계층이 확립된 엔진에 다섯 번째 계층을 얹으면서 기존 로직의
    # 우선순위를 존중). 상세: engine/valuation/hynix_band.py
    valuation = compute_valuation_band()
    valuation_band_dict = {
        "pe_zscore": valuation.pe_zscore,
        "band_label": valuation.band_label,
        "latest_quarter": valuation.latest_quarter,
        "latest_divergence": valuation.latest_divergence,
        "erp_pct": valuation.erp_pct,
        "erp_note": valuation.erp_note,
        "caveats": valuation.caveats,
    }
    if valuation.pe_zscore is not None:
        if valuation.pe_zscore <= -1.5:
            risk_flags.append(f"밸류에이션 저평가 극단(P/E Z {valuation.pe_zscore:.2f})")
            triggers.append({
                "condition": f"P/E Z-score {valuation.pe_zscore:.2f} ≤ -1.5 (저평가 극단)",
                "action": "밸류에이션 관점 매수 매력 — 다른 계층과 함께 재검토",
                "price_level": None,
            })
        elif valuation.pe_zscore >= 1.5:
            risk_flags.append(f"밸류에이션 고평가 극단(P/E Z {valuation.pe_zscore:.2f})")
            triggers.append({
                "condition": f"P/E Z-score {valuation.pe_zscore:.2f} ≥ 1.5 (고평가 극단)",
                "action": "밸류에이션 관점 수익실현 검토 — 다른 계층과 함께 재검토",
                "price_level": None,
            })

    # --- MACRO-LEVEL REGIME CHECK ---
    # 약세/위기: default to SELL unless strong counterarguments
    if kr_regime in ("약세", "위기"):
        signal = "SELL"
        confidence = 75
        risk_flags.append(f"거시 국면 {kr_regime}")
        if kr_regime == "위기":
            triggers.append({
                "condition": "방어 필수",
                "action": "50% 감량 검토 (1,200주 → 600주)",
                "price_level": None,
            })

    # 조정: cautious HOLD with buy opportunities on dips
    elif kr_regime == "조정":
        signal = "HOLD"
        confidence = 60
        if kr_confidence >= 70:
            triggers.append({
                "condition": "신뢰도 70%↑ 유지",
                "action": "매수 기회 window (1,400K 이하)",
                "price_level": 1400,
            })
        else:
            risk_flags.append("신뢰도 약세")

    # 상승: HOLD by default, consider buying on weakness
    elif kr_regime == "상승":
        signal = "HOLD"
        confidence = 70
        if kr_confidence >= 75:
            triggers.append({
                "condition": "신뢰도 75%↑ + 상승 국면",
                "action": "추가 매수 고려 (1,400K 이하, 200주 단위)",
                "price_level": 1400,
            })

    # --- SEMICONDUCTOR-SPECIFIC CHECKS ---
    if semiconductor_score is not None:
        if semiconductor_band in ("부진", "극악"):
            signal = "SELL"
            confidence = max(confidence, 70)
            risk_flags.append(f"반도체 밴드 {semiconductor_band}")
            triggers.append({
                "condition": f"반도체 {semiconductor_band}",
                "action": "수익실현 고려 (300-500주 매도)",
                "price_level": None,
            })
        elif semiconductor_band == "양호" and kr_regime == "상승":
            if signal == "HOLD":
                signal = "BUY"
                confidence = 75
            triggers.append({
                "condition": "반도체 양호 + 거시 상승",
                "action": "포지션 확대 (1,400K 이하, 100-200주)",
                "price_level": 1400,
            })

    # --- RATE ENVIRONMENT CHECK ---
    # High rates (긴축) reduce semiconductor margin outlook
    if rate_score < 40:
        risk_flags.append(f"긴축 사이클 (점수 {rate_score})")
        if signal == "BUY":
            signal = "HOLD"
            confidence -= 15
    # Low rates (완화) support upside
    elif rate_score >= 70:
        if signal == "HOLD" and kr_regime == "상승":
            signal = "BUY"
            confidence = min(100, confidence + 10)

    # --- CCI STATE CHECK ---
    if cci_state == "RED":
        risk_flags.append("위기지수 RED")
        if signal in ("HOLD", "BUY"):
            signal = "SELL"
            confidence = 80
            triggers.append({
                "condition": "CCI RED (위험신호)",
                "action": "방어 우선 (25% 감량)",
                "price_level": None,
            })
    elif cci_state == "YELLOW":
        risk_flags.append("위기지수 YELLOW (경고)")

    # --- MACRO LINKAGE ANALYSIS ---
    macro_linkage = _analyze_macro_linkage(macro, semiconductor_score)

    # --- GENERATE RATIONALE ---
    rationale = _generate_rationale(signal, kr_regime, semiconductor_band, kr_confidence, rate_score)

    # --- NEXT CHECK TIMING ---
    # Re-evaluate when macro regime changes or rate/cci signals flip
    next_check = _next_check_timing(kr_regime, cci_state, rate_score)

    return SKHynixDecision(
        signal=signal,
        confidence=confidence,
        rationale=rationale,
        triggers=triggers,
        macro_linkage=macro_linkage,
        risk_flags=risk_flags,
        next_check=next_check,
        valuation_band=valuation_band_dict,
    )


def _analyze_macro_linkage(macro: dict, semiconductor_score: float | None) -> str:
    """Analyze how macro signals affect SK Hynix outlook."""
    changes = macro.get("changes", [])
    kr_regime = macro.get("regime")

    linkages = []
    for change in changes[:3]:  # Top 3 changes
        msg = change.get("message", "")
        # Map common macro changes to semiconductor impact
        if "수출" in msg or "수요" in msg:
            linkages.append("미국 CapEx ↑ → 메모리 수요 지속 → HBM ASP 강세")
        elif "금리" in msg or "긴축" in msg:
            linkages.append("금리 상향 → 반도체 설비투자 둔화 우려 → 공급감소기대")
        elif "신뢰도" in msg:
            linkages.append("거시 신뢰도 ↑ → 외국인 복귀 기대 → 메모리 선물물 수요 ↑")

    if not linkages:
        if kr_regime == "상승":
            linkages.append("거시 상승 국면 → 반도체 성장 기대 → SK하이닉스 실적 개선 기대")
        elif kr_regime == "약세":
            linkages.append("거시 약세 → 메모리 수요 위축 → SK하이닉스 ASP 하향 압력")

    return " | ".join(linkages[:2]) if linkages else "거시-반도체 연결고리 미확인"


def _generate_rationale(
    signal: str, kr_regime: str, semiconductor_band: str, kr_confidence: float, rate_score: float
) -> str:
    """Generate one-line rationale for decision."""
    if signal == "SELL":
        if kr_regime == "위기":
            return "거시 위기 신호 → 방어 모드 필수"
        elif kr_regime == "약세":
            return "거시 약세 → 반도체 수요 위축 우려"
        elif semiconductor_band in ("부진", "극악"):
            return f"반도체 밴드 {semiconductor_band} → 수익 실현 시점"
        else:
            return "누적된 위험 신호 → 포지션 축소"

    elif signal == "BUY":
        if kr_regime == "상승" and kr_confidence >= 75:
            return f"거시 상승 + 반도체 {semiconductor_band} → 확대 기회"
        elif rate_score >= 70:
            return "완화 사이클 + 반도체 수요 회복 → 매수 기회"
        else:
            return "거시-반도체 신호 정렬 → 추가 매수 고려"

    else:  # HOLD
        if kr_confidence >= 70:
            return f"거시 {kr_regime} + 신뢰도 {kr_confidence:.0f}% → 현 포지션 유지, 매수기 대기"
        else:
            return f"거시 {kr_regime} + 신뢰도 낮음 → 보수 보유"


def _next_check_timing(kr_regime: str, cci_state: str, rate_score: float) -> str:
    """Determine when to re-evaluate decision."""
    checks = []

    if kr_regime in ("약세", "위기"):
        checks.append("거시 국면 전환 신호")
    else:
        checks.append("1-2주 후 거시 신뢰도 변화")

    if cci_state == "RED":
        checks.append("CCI → YELLOW 전환")
    elif cci_state == "YELLOW":
        checks.append("CCI → RED 또는 GREEN 전환")

    if 40 <= rate_score <= 60:
        checks.append("금리 신호 상향/하향 이동 시")

    return "; ".join(checks) if checks else "주간 정기 점검"
