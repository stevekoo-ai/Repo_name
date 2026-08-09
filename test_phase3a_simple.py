"""
Phase 3a Simple Integration Test (No External APIs)
Validates economic events core functionality.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from engine.report.economic_events import (
    EconomicEvent,
    get_upcoming_events,
    calculate_event_impact,
    get_scenario_impacts,
    generate_event_section,
)


def test_economic_events_integration():
    """Test economic events integration without external APIs"""
    print("=" * 70)
    print("PHASE 3A: ECONOMIC EVENTS SIMPLE INTEGRATION TEST")
    print("=" * 70)

    # Test 1: Event dataclass
    print("\n✓ TEST 1: EconomicEvent dataclass creation")
    event = EconomicEvent(
        date="2026-08-12",
        name="미국 CPI (7월)",
        importance="🔴 Critical",
        consensus=2.8,
        actual=None,
        prior=2.9,
        sk_hynix_impact="BEARISH",
        real_estate_impact="WAIT"
    )
    assert event.date == "2026-08-12"
    print("  ✓ EconomicEvent created successfully")

    # Test 2: Get events
    print("\n✓ TEST 2: get_upcoming_events()")
    events = get_upcoming_events()
    assert len(events) >= 3
    print(f"  ✓ Retrieved {len(events)} upcoming events")

    # Test 3: CPI upside impact
    print("\n✓ TEST 3: CPI upside impact scenario")
    event_cpi = EconomicEvent(
        date="2026-08-12",
        name="미국 CPI (7월)",
        importance="🔴 Critical",
        consensus=2.8,
        actual=3.4,  # Upside: +0.6%p
        prior=2.9,
        sk_hynix_impact="BEARISH",
        real_estate_impact="WAIT"
    )
    new_signal, new_confidence, reason = calculate_event_impact(
        event_cpi, "HOLD", 50.0
    )
    assert new_signal == "HOLD"
    assert new_confidence < 50
    print(f"  ✓ Signal: {new_signal}, Confidence: {new_confidence}%, Reason: {reason}")

    # Test 4: Rate cut impact
    print("\n✓ TEST 4: Interest rate cut scenario")
    event_rate = EconomicEvent(
        date="2026-08-14",
        name="한국은행 기준금리",
        importance="🔴 Critical",
        consensus=3.50,
        actual=3.25,  # Cut
        prior=3.50,
        sk_hynix_impact="BULLISH",
        real_estate_impact="ENTER"
    )
    new_signal, new_confidence, reason = calculate_event_impact(
        event_rate, "HOLD", 50.0
    )
    assert new_signal == "BUY"
    assert new_confidence > 50
    print(f"  ✓ Signal: {new_signal}, Confidence: {new_confidence}%, Reason: {reason}")

    # Test 5: Scenario planning
    print("\n✓ TEST 5: Scenario planning for CPI")
    scenarios = get_scenario_impacts(event_cpi)
    assert "downside" in scenarios
    assert "base" in scenarios
    assert "upside" in scenarios
    print(f"  ✓ Generated {len(scenarios)-1} scenarios (downside, base, upside)")

    # Test 6: Markdown generation
    print("\n✓ TEST 6: Markdown section generation")
    payload = {"macro_indicators": {}}
    markdown = generate_event_section(payload)
    assert len(markdown) > 100
    assert "경제 일정" in markdown or "Economic" in markdown
    assert "upcoming" in markdown.lower() or "2026-08" in markdown
    print(f"  ✓ Generated {len(markdown)} characters of markdown")
    print(f"  ✓ Includes upcoming events table")
    print(f"  ✓ Includes scenario planning")
    print(f"  ✓ Includes watch list")

    # Test 7: Verify markdown structure
    print("\n✓ TEST 7: Markdown structure validation")
    lines = markdown.split("\n")
    assert "3.5 경제 일정" in markdown
    assert "Upcoming Critical Events" in markdown
    assert "Scenario Planning" in markdown
    assert "Watch List" in markdown
    print(f"  ✓ Section title: '3.5 경제 일정 & 의사결정 트리거'")
    print(f"  ✓ Events table present")
    print(f"  ✓ Scenario planning present")
    print(f"  ✓ Watch list present")

    # Test 8: Check markdown import in renderer
    print("\n✓ TEST 8: Verify integration in markdown.py")
    from engine.report import markdown as md_module
    import inspect

    source = inspect.getsource(md_module.render_markdown)
    assert "generate_event_section" in source
    print("  ✓ generate_event_section() is imported and called in render_markdown()")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
    print("\nSummary:")
    print("  • EconomicEvent dataclass: OK")
    print("  • Event retrieval: OK")
    print("  • Signal impact calculation (CPI): OK")
    print("  • Signal impact calculation (Interest rate): OK")
    print("  • Scenario planning: OK")
    print("  • Markdown generation: OK")
    print("  • Markdown structure: OK")
    print("  • Integration in render_markdown(): OK")
    print("\nEconomic events integration is fully functional and positioned")
    print("as Section 3.5 in the daily report.")

    return True


if __name__ == "__main__":
    try:
        success = test_economic_events_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
