"""
Economic Events Integration Module

Integrates macroeconomic events (CPI, interest rates, employment) into
SK Hynix and Real Estate investment decisions.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta


@dataclass
class EconomicEvent:
    """Represents a macroeconomic event"""
    date: str
    name: str
    importance: str  # 🔴 Critical, 🟡 High, 🟢 Medium
    consensus: Optional[float]
    actual: Optional[float]
    prior: Optional[float]
    sk_hynix_impact: str  # "BULLISH", "NEUTRAL", "BEARISH"
    real_estate_impact: str  # "ENTER", "NEUTRAL", "WAIT"


def get_upcoming_events() -> List[EconomicEvent]:
    """
    Get next 14 days of critical economic events.
    In production, this would query trading economics API or web scrape.

    Returns:
        List of upcoming economic events with metadata
    """
    today = datetime.now()

    # Hardcoded for Phase 3a validation; replace with API calls in Phase 3b
    events = [
        EconomicEvent(
            date="2026-08-12",
            name="미국 CPI (7월)",
            importance="🔴 Critical",
            consensus=2.8,
            actual=None,  # Not yet released
            prior=2.9,
            sk_hynix_impact="BEARISH",  # Upside inflation → hawkish
            real_estate_impact="WAIT"   # Tight money environment
        ),
        EconomicEvent(
            date="2026-08-14",
            name="한국은행 기준금리",
            importance="🔴 Critical",
            consensus=3.50,
            actual=None,
            prior=3.50,
            sk_hynix_impact="NEUTRAL",  # Expected hold
            real_estate_impact="WAIT"
        ),
        EconomicEvent(
            date="2026-08-20",
            name="미국 PPI (7월)",
            importance="🟡 High",
            consensus=2.5,
            actual=None,
            prior=2.6,
            sk_hynix_impact="NEUTRAL",
            real_estate_impact="NEUTRAL"
        ),
    ]

    return events


def calculate_event_impact(
    event: EconomicEvent,
    current_signal: str,
    current_confidence: float
) -> tuple[str, float, str]:
    """
    Calculate signal and confidence change based on economic event.

    Args:
        event: EconomicEvent with consensus and actual values
        current_signal: Current SK Hynix signal (HOLD, BUY, SELL)
        current_confidence: Current confidence level (0-100)

    Returns:
        (new_signal, new_confidence, change_reason)
    """
    if event.actual is None:
        # Event not yet released
        return current_signal, current_confidence, "Event pending"

    # Calculate consensus miss
    consensus_miss = event.actual - event.consensus

    # Apply impact rules
    new_signal = current_signal
    new_confidence = current_confidence
    change_reason = ""

    # CPI Logic
    if "CPI" in event.name and "미국" in event.name:
        if consensus_miss > 0.5:  # Upside (inflation concerns)
            new_confidence = max(0, current_confidence - 15)
            new_signal = "HOLD" if current_signal == "BUY" else current_signal
            change_reason = f"CPI upside (+{consensus_miss:.1f}%p) → 긴축 우려 ↑"
        elif consensus_miss < -0.5:  # Downside (deflation/slowdown)
            new_confidence = max(0, current_confidence - 10)
            new_signal = "SELL" if current_signal in ["HOLD", "BUY"] else current_signal
            change_reason = f"CPI downside ({consensus_miss:.1f}%p) → 경기약세 신호"

    # 기준금리 Logic
    elif "기준금리" in event.name:
        if event.actual < event.consensus:  # Rate cut
            new_signal = "BUY"
            new_confidence = min(100, current_confidence + 15)
            change_reason = "기준금리 인하 → 약달러, 유동성 확대"
        elif event.actual > event.consensus:  # Rate hike
            new_signal = "SELL"
            new_confidence = min(100, current_confidence + 10)
            change_reason = "기준금리 인상 → 긴축 심화"

    return new_signal, new_confidence, change_reason


def get_scenario_impacts(event: EconomicEvent) -> Dict[str, Dict]:
    """
    Generate SK Hynix and Real Estate signal impact scenarios.

    Args:
        event: EconomicEvent to analyze

    Returns:
        Dict with downside/base/upside scenarios and impacts
    """
    if "CPI" not in event.name:
        return {"note": "Scenario planning not configured for this event type"}

    return {
        "downside": {
            "description": f"CPI < {event.consensus - 0.5:.1f}%",
            "probability": "25%",
            "sk_hynix": {"signal": "SELL", "confidence_change": "-10%p", "reason": "경기약세"},
            "real_estate": {"signal": "WAIT", "confidence_change": "+5%p", "reason": "금리인하기대"},
        },
        "base": {
            "description": f"CPI {event.consensus - 0.3:.1f}% ~ {event.consensus + 0.3:.1f}%",
            "probability": "60%",
            "sk_hynix": {"signal": "HOLD", "confidence_change": "0%", "reason": "기대치부합"},
            "real_estate": {"signal": "WAIT", "confidence_change": "0%", "reason": "신호무변"},
        },
        "upside": {
            "description": f"CPI > {event.consensus + 0.5:.1f}%",
            "probability": "15%",
            "sk_hynix": {"signal": "HOLD", "confidence_change": "-15%p", "reason": "긴축장기화"},
            "real_estate": {"signal": "WAIT", "confidence_change": "+10%p", "reason": "실질금리압박"},
        },
    }


def generate_event_section(payload: dict) -> str:
    """
    Generate markdown section for economic events in daily report.

    Args:
        payload: PEOS report payload with macro data

    Returns:
        Markdown string for economic events section
    """
    events = get_upcoming_events()

    md = "\n# 3.5 경제 일정 & 의사결정 트리거\n\n"
    md += "**다음 14일간 SK Hynix/부동산 신호에 영향을 미칠 주요 이벤트 추적**\n\n"

    # 2026-08-27 발견 — get_upcoming_events()는 module docstring이 스스로 인정하듯
    # "Phase 3a 검증용 하드코딩, Phase 3b에서 API로 교체 예정"이었으나 교체가
    # 안 됐다. 무료 공개 경제캘린더 API가 없어(아래 get_upcoming_events 참고)
    # 이 표의 날짜가 전부 오늘보다 과거로 밀리면(교체 전까지 계속 발생) 마치
    # 최신 데이터인 것처럼 조용히 보여주지 않고 여기서 loud하게 경고한다 —
    # "값을 지어내지 않는다"는 이 저장소 전반의 원칙과 동일선상.
    if events and all(
        (datetime.strptime(e.date, "%Y-%m-%d") - datetime.now()).days < 0 for e in events
    ):
        md += (
            "**🚨 [사실] 아래 이벤트는 전부 오늘(현재 실행 시각) 기준으로 이미 지난 날짜입니다** — "
            "이 표는 Phase 3a 검증용 예시 데이터가 그대로 남아있는 것이며(무료 공개 경제캘린더 API가 "
            "없어 아직 실데이터로 교체되지 못함), 실제 다음 14일 일정이 아닙니다. "
            "실제 경제 일정은 별도로 확인하세요.\n\n"
        )

    # Upcoming events table
    md += "## 📍 Upcoming Critical Events (Next 14 Days)\n\n"
    md += "| 날짜 | 이벤트 | 중요도 | 컨센서스 | 직전값 | D-Days | SK 신호 영향 | RE 신호 영향 |\n"
    md += "|------|--------|--------|---------|--------|--------|----------|----------|\n"

    for event in events:
        days_until = (datetime.strptime(event.date, "%Y-%m-%d") - datetime.now()).days
        prior_str = f"{event.prior:.1f}" if event.prior else "-"
        consensus_str = f"{event.consensus:.1f}" if event.consensus else "-"

        md += f"| {event.date} | {event.name} | {event.importance} | {consensus_str} | {prior_str} | D-{days_until} | "
        md += f"{event.sk_hynix_impact} | {event.real_estate_impact} |\n"

    md += "\n"

    # Scenario planning for next critical event
    if events:
        next_critical = next((e for e in events if "🔴" in e.importance), None)
        if next_critical:
            md += f"## 🔮 Scenario Planning: {next_critical.name}\n\n"
            scenarios = get_scenario_impacts(next_critical)

            for scenario_name, scenario_data in scenarios.items():
                if scenario_name == "note":
                    continue

                md += f"### {scenario_name.upper()} Scenario\n"
                md += f"- **발생 확률**: {scenario_data['probability']}\n"
                md += f"- **조건**: {scenario_data['description']}\n"
                md += f"- **SK Hynix**: {scenario_data['sk_hynix']['signal']} "
                md += f"(신뢰도 {scenario_data['sk_hynix']['confidence_change']}) — "
                md += f"{scenario_data['sk_hynix']['reason']}\n"
                md += f"- **부동산**: {scenario_data['real_estate']['signal']} "
                md += f"(신뢰도 {scenario_data['real_estate']['confidence_change']}) — "
                md += f"{scenario_data['real_estate']['reason']}\n\n"

    # Risk alert
    md += "## ⚠️ Watch List\n"
    md += "- **미국 CPI (D-3)**: Upside > 3.0% 시 긴축 우려 급증 → SK 신뢰도 하락 가능\n"
    md += "- **기준금리 (D-5)**: 인하 신호 시 BUY 신호 전환 가능성 높음 (확률 30%)\n\n"

    return md


# Integration with decision engines
def apply_event_context_to_sk_hynix(payload: dict) -> dict:
    """
    Adjust SK Hynix decision based on recent/upcoming economic events.
    """
    events = get_upcoming_events()

    # Check if any recent event should trigger signal review
    # This would be called within compute_sk_hynix_decision()

    # For now, return unchanged payload
    return payload


def apply_event_context_to_real_estate(payload: dict) -> dict:
    """
    Adjust Real Estate decision based on recent/upcoming economic events.
    """
    events = get_upcoming_events()

    # Check if any recent event should trigger signal review
    # This would be called within compute_real_estate_decision()

    # For now, return unchanged payload
    return payload
