"""Real estate market entry/wait decision engine.

Converts interest rate trajectory + 전세가 + Platform City news
into a WAIT/ENTER signal with event-based triggers.

Decision Logic:
- WAIT: Interest rates rising (긴축), 전세가 falling or volatile, Platform City news not active
- ENTER: Interest rates falling (완화), 전세가 stabilizing, key event triggers (기준금리인하, 청약공시)

Event triggers:
- 기준금리 25bp+ 인하 발표 → 전세 전환 고려
- 플랫폼시티 청약공시 발표 → 즉시 청약신청
- 강남/서초 전세가 +5% 이상 → 긴급 입장 검토
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RealEstateDecision:
    """Real estate market entry/wait decision."""
    signal: str  # "WAIT" | "ENTER"
    confidence: float  # 0-100
    rationale: str  # one-line reason
    event_triggers: list[dict]  # event-based conditions (not price-based)
    macro_linkage: str  # how macro affects real estate
    current_situation: str  # user's current housing status
    next_check: str  # when to re-evaluate
    # Funding reality from the exposure model (engine/exposure/model.py).
    # None when the exposure model did not run. See _compute_affordability().
    affordability: dict | None = None


def compute_real_estate_decision(payload: dict) -> RealEstateDecision:
    """Compute real estate market entry decision based on macro + housing data.

    Args:
        payload: Full report payload with macro, rate, housing data

    Returns:
        RealEstateDecision with signal, confidence, event triggers, etc.
    """
    macro = payload["macro"]
    rate_analysis = payload.get("rate_analysis", {})
    housing = payload.get("housing", {})
    affordability = _compute_affordability(payload)

    # Extract key signals
    kr_regime = macro["regime"]  # 상승|조정|약세|위기
    kr_confidence = macro["confidence"]
    rate_score = rate_analysis.get("total_score", 50)
    rate_trends = rate_analysis.get("trends", {})
    real_estate = payload.get("real_estate", {})
    real_estate_rent = payload.get("real_estate_rent", {})

    # User's current housing status (from housing data)
    current_situation = _get_housing_situation(housing)

    # Base signal logic
    signal = "WAIT"
    confidence = 50
    event_triggers = []
    risk_flags = []

    # --- RATE ENVIRONMENT CHECK (Primary Driver) ---
    # Low rates (완화) = entry friendly
    if rate_score >= 70:
        signal = "ENTER"
        confidence = 75
        reason = "완화 사이클 → 전세금 상승 기대 → 조기 진입 유리"
        # Add event triggers
        event_triggers.append({
            "event": "기준금리 25bp 인하 발표",
            "action": "전세 전환 고려 (기한 3개월 내)",
            "urgency": "높음",
        })
        event_triggers.append({
            "event": "플랫폼시티 청약공시",
            "action": "당첨 가능성 분석 후 즉시 청약",
            "urgency": "최고",
        })

    # Mid-range rates (중립)
    elif 55 <= rate_score < 70:
        signal = "WAIT"
        confidence = 60
        reason = "금리 중립 → 진입 판단 유보"
        event_triggers.append({
            "event": "기준금리 추가 인하 신호",
            "action": "진입 검토로 전환",
            "urgency": "중간",
        })

    # High rates (긴축) = entry caution
    else:
        signal = "WAIT"
        confidence = 80
        reason = "긴축 사이클 → 전세금 상승 우려 → 관망"
        risk_flags.append(f"긴축 사이클 (점수 {rate_score})")

    # --- MACRO REGIME CHECK (Secondary Driver) ---
    # 위기/약세: strong caution
    if kr_regime in ("위기", "약세"):
        signal = "WAIT"
        confidence = max(80, confidence)
        reason = f"거시 {kr_regime} → 고금리 장기화 가능성 → 진입 유보"
        risk_flags.append(f"거시 국면 {kr_regime}")
    # 상승: supports entry
    elif kr_regime == "상승" and signal == "ENTER":
        confidence = min(100, confidence + 10)
        reason = "거시 상승 + 완화 사이클 → 진입 기회"

    # --- REAL ESTATE TREND CHECK ---
    # Check if 전세가 is stable or rising (entry favorable)
    rent_trend = _analyze_rent_trend(real_estate_rent)
    if rent_trend == "상승":
        # 전세가 rising = urgency to enter
        if signal == "WAIT":
            confidence -= 10  # Less time to wait
        event_triggers.append({
            "event": "강남/서초 전세가 +5% 급등",
            "action": "긴급 진입 검토 (전세 대기자 순서 앞당기기)",
            "urgency": "높음",
        })
    elif rent_trend == "하강":
        # 전세가 falling = advantage to wait
        if signal == "WAIT":
            confidence += 10
        reason = f"전세가 하락세 → 조급 금지, 관망 지속"

    # --- MACRO-REAL ESTATE LINKAGE ---
    macro_linkage = _analyze_real_estate_linkage(macro, rate_score)

    # --- PLATFORM CITY TRACKING ---
    # Always add Platform City as primary event trigger
    if signal == "ENTER":
        event_triggers.insert(0, {
            "event": "플랫폼시티 공공/일반 청약공시",
            "action": "당첨 가능성 분석 → 즉시 청약신청 (경쟁률 파악 후)",
            "urgency": "최고",
        })
    else:
        event_triggers.append({
            "event": "플랫폼시티 청약공시 (대기 중)",
            "action": "공시 시 즉시 분석 후 진입 신호 재검토",
            "urgency": "관심",
        })

    # --- NEXT CHECK TIMING ---
    next_check = _next_check_timing(kr_regime, rate_score, rent_trend)

    # --- GENERATE RATIONALE (if not already set) ---
    if "reason" not in locals():
        reason = _generate_rationale(signal, kr_regime, rate_score, rent_trend)

    return RealEstateDecision(
        signal=signal,
        confidence=confidence,
        rationale=reason,
        event_triggers=event_triggers,
        macro_linkage=macro_linkage,
        current_situation=current_situation,
        next_check=next_check,
        affordability=affordability,
    )


def _compute_affordability(payload: dict) -> dict | None:
    """Join the exposure model to the housing decision.

    This is the coupling the report was missing. "Should I sell SK하이닉스?" and
    "when can I buy a home?" are not two questions for this user — the money for
    the home is inside the stock. The rate environment can say ENTER all it likes;
    if the cash is not there, ENTER is not an instruction the user can follow.

    Deliberately does NOT invent an affordability threshold: the user's target
    area and size are unknown, so a hard-coded "you need N억" would be a guess
    dressed as a rule. Instead it reports how far the deployable cash actually
    reaches at the current Seoul 평당가, and states the one fact that follows
    from the numbers — funding a purchase means liquidating semiconductors,
    which is also what reduces the concentration. Both problems share a solution.
    """
    exposure = payload.get("exposure")
    if exposure is None:
        return None

    def _pyeong_price(block: dict, key: str) -> float | None:
        seoul = (block or {}).get(key, {}).get("seoul", {})
        v = seoul.get("price_per_pyeong_manwon")
        return float(v) * 10_000 if v else None

    buy_pp = _pyeong_price(payload.get("real_estate", {}), "tiers")
    jeonse_pp = _pyeong_price(payload.get("real_estate_rent", {}), "jeonse_tiers")

    cash = exposure.deployable_cash
    out = {
        "deployable_cash": cash,
        "cash_only": exposure.cash_krw,
        "from_liquidation": exposure.liquid_valued,
        "locked": exposure.locked_valued,
        "buy_pyeong_price": buy_pp,
        "jeonse_pyeong_price": jeonse_pp,
        "buy_pyeong_equivalent": (cash / buy_pp) if buy_pp else None,
        "jeonse_pyeong_equivalent": (cash / jeonse_pp) if jeonse_pp else None,
        "semi_pct": exposure.semi_pct,
        "reference_month": ((payload.get("real_estate") or {}).get("tiers", {})
                            .get("seoul", {}).get("reference_month")),
    }

    # The only structural statement the numbers support on their own.
    out["coupling_note"] = (
        f"가용 현금 {cash/100_000_000:.2f}억 중 현금성은 "
        f"{exposure.cash_krw/100_000_000:.2f}억뿐이고 나머지는 주식 매각으로만 만들어진다. "
        f"그런데 그 매각은 반도체 집중도({exposure.semi_pct:.1f}%)를 낮추는 행위와 같다 — "
        f"주택 자금 마련과 집중도 완화는 서로 다른 문제가 아니라 같은 실행이다."
    )
    return out


def _get_housing_situation(housing: dict) -> str:
    """Get user's current housing status."""
    notices = housing.get("notices", [])
    if not notices:
        return "현재 거주 상황 미입력"

    # Summarize current notice/status
    primary = notices[0] if notices else {}
    status = primary.get("status", "확인 중")
    if primary.get("name"):
        return f"{primary['name']} ({status})"
    return status


def _analyze_rent_trend(real_estate_rent: dict) -> str:
    """Analyze 전세가 trend from real estate data."""
    if not real_estate_rent:
        return "데이터 부족"

    # Look for trend in data
    trend_data = real_estate_rent.get("trend", {})
    if trend_data.get("direction") == "상승":
        return "상승"
    elif trend_data.get("direction") == "하강":
        return "하강"
    else:
        return "보합"


def _analyze_real_estate_linkage(macro: dict, rate_score: float) -> str:
    """Analyze how macro signals affect real estate."""
    changes = macro.get("changes", [])
    kr_regime = macro.get("regime")

    linkages = []
    for change in changes[:2]:
        msg = change.get("message", "")
        if "금리" in msg or "긴축" in msg:
            linkages.append("금리 ↑ → 전세금 상승 압력 → 진입 시점 단축")
        elif "신뢰도" in msg:
            linkages.append("거시 신뢰도 ↑ → 외국인 부동산 투자 활성화 → 전세 공실 감소")

    if not linkages:
        if rate_score >= 70:
            linkages.append("완화 사이클 → 금융 유동성 ↑ → 전세금 상승기 → 조기 진입 유리")
        elif rate_score < 40:
            linkages.append("긴축 사이클 → 금융 경색 → 전세금 안정화 → 진입 타이밍 유보")
        else:
            linkages.append("금리 중립 → 전세금 추이 모니터링 필요")

    return linkages[0] if linkages else "거시-부동산 연결고리 미확인"


def _generate_rationale(signal: str, kr_regime: str, rate_score: float, rent_trend: str) -> str:
    """Generate one-line rationale for decision."""
    if signal == "ENTER":
        if rate_score >= 70:
            return "완화 사이클 + 경제 회복 기대 → 진입 기회 창"
        else:
            return "거시 개선 신호 → 조기 진입 검토"

    else:  # WAIT
        if kr_regime in ("약세", "위기"):
            return f"거시 {kr_regime} → 금리 전망 불확실 → 관망 지속"
        elif rate_score < 40:
            return "긴축 사이클 심화 → 금융경색 우려 → 진입 유보"
        elif rent_trend == "상승":
            return "전세가 상승세 → 하향세 대기"
        else:
            return "진입 기회 발생 시까지 대기"


def _next_check_timing(kr_regime: str, rate_score: float, rent_trend: str) -> str:
    """Determine when to re-evaluate real estate decision."""
    checks = []

    if kr_regime in ("약세", "위기"):
        checks.append("거시 회복신호 발생 시")
    else:
        checks.append("기준금리 발표 후 (매월 초)")

    if rate_score < 50:
        checks.append("금리 방향성 변화 시")

    if rent_trend == "상승":
        checks.append("일일 전세가 모니터링")
    else:
        checks.append("주간 전세가 체크")

    checks.append("플랫폼시티 공시 소식")

    return "; ".join(checks[:3]) if checks else "주간 정기 점검"
