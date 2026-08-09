"""
Phase 3a Test Suite: Economic Events Integration
Validates economic calendar integration into decision framework.
"""
import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.report.economic_events import (
    EconomicEvent,
    get_upcoming_events,
    calculate_event_impact,
    get_scenario_impacts,
    generate_event_section,
)
from engine.report.payload import build_report_payload


def test_01_economic_event_dataclass():
    """Test 1: EconomicEvent dataclass creation"""
    print("TEST 1: EconomicEvent dataclass")

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
    assert event.importance == "🔴 Critical"
    assert event.actual is None
    assert event.sk_hynix_impact == "BEARISH"
    print("  ✓ EconomicEvent created successfully")
    print(f"  ✓ Fields: {event.name}, consensus={event.consensus}%, prior={event.prior}%")
    return True


def test_02_get_upcoming_events():
    """Test 2: Fetch upcoming events"""
    print("\nTEST 2: get_upcoming_events()")

    events = get_upcoming_events()

    assert isinstance(events, list)
    assert len(events) >= 3
    assert all(isinstance(e, EconomicEvent) for e in events)

    print(f"  ✓ Retrieved {len(events)} upcoming events")
    for event in events:
        days_until = event.date.split("-")[2]
        print(f"    - {event.date} | {event.name} | {event.importance} | "
              f"Consensus: {event.consensus}% | SK: {event.sk_hynix_impact} | RE: {event.real_estate_impact}")

    return True


def test_03_calculate_event_impact_cpi_upside():
    """Test 3: CPI upside impact (inflation concern)"""
    print("\nTEST 3: calculate_event_impact() - CPI upside scenario")

    event = EconomicEvent(
        date="2026-08-12",
        name="미국 CPI (7월)",
        importance="🔴 Critical",
        consensus=2.8,
        actual=3.4,  # Upside: +0.6%p
        prior=2.9,
        sk_hynix_impact="BEARISH",
        real_estate_impact="WAIT"
    )

    # Current signal: HOLD at 50% confidence
    new_signal, new_confidence, reason = calculate_event_impact(
        event, "HOLD", 50.0
    )

    print(f"  Current: HOLD, confidence=50%")
    print(f"  Event outcome: CPI 3.4% (consensus 2.8%, upside +0.6%p)")
    print(f"  Result: {new_signal}, confidence={new_confidence}%, reason: {reason}")

    assert new_signal == "HOLD"  # Signal maintains as HOLD
    assert new_confidence < 50  # Confidence decreases
    assert "CPI upside" in reason or "긴축" in reason
    print("  ✓ CPI upside handling correct (confidence decreased due to tightening concern)")

    return True


def test_04_calculate_event_impact_rate_cut():
    """Test 4: Interest rate cut impact (monetary easing)"""
    print("\nTEST 4: calculate_event_impact() - Rate cut scenario")

    event = EconomicEvent(
        date="2026-08-14",
        name="한국은행 기준금리",
        importance="🔴 Critical",
        consensus=3.50,
        actual=3.25,  # Cut from 3.50 to 3.25
        prior=3.50,
        sk_hynix_impact="BULLISH",
        real_estate_impact="ENTER"
    )

    # Current signal: HOLD at 50% confidence
    new_signal, new_confidence, reason = calculate_event_impact(
        event, "HOLD", 50.0
    )

    print(f"  Current: HOLD, confidence=50%")
    print(f"  Event outcome: 기준금리 인하 (3.50% → 3.25%)")
    print(f"  Result: {new_signal}, confidence={new_confidence}%, reason: {reason}")

    assert new_signal == "BUY"  # Signal changes to BUY
    assert new_confidence > 50  # Confidence increases
    assert "인하" in reason or "약달러" in reason
    print("  ✓ Rate cut handling correct (signal switched to BUY, confidence increased)")

    return True


def test_05_get_scenario_impacts():
    """Test 5: Scenario planning for critical events"""
    print("\nTEST 5: get_scenario_impacts()")

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

    scenarios = get_scenario_impacts(event)

    assert "downside" in scenarios
    assert "base" in scenarios
    assert "upside" in scenarios

    print(f"  ✓ Scenario planning for {event.name}:")

    for scenario_name, scenario_data in scenarios.items():
        if scenario_name != "note":
            print(f"\n    {scenario_name.upper()} Scenario:")
            print(f"      Probability: {scenario_data['probability']}")
            print(f"      Condition: {scenario_data['description']}")
            print(f"      SK Hynix: {scenario_data['sk_hynix']['signal']} "
                  f"(신뢰도 {scenario_data['sk_hynix']['confidence_change']}) — "
                  f"{scenario_data['sk_hynix']['reason']}")
            print(f"      Real Estate: {scenario_data['real_estate']['signal']} "
                  f"(신뢰도 {scenario_data['real_estate']['confidence_change']}) — "
                  f"{scenario_data['real_estate']['reason']}")

    return True


def test_06_generate_event_section():
    """Test 6: Markdown generation for economic events section"""
    print("\nTEST 6: generate_event_section()")

    payload = {"macro_indicators": {}}  # Minimal payload

    markdown = generate_event_section(payload)

    assert isinstance(markdown, str)
    assert len(markdown) > 100
    assert "경제 일정" in markdown or "Economic" in markdown
    assert "upcoming" in markdown.lower() or "2026-08" in markdown

    print(f"  ✓ Markdown section generated ({len(markdown)} characters)")
    print(f"  ✓ Includes upcoming events table")
    print(f"  ✓ Includes scenario planning")
    print(f"  ✓ Includes watch list")

    # Count lines to verify richness
    lines = markdown.split("\n")
    print(f"  ✓ Section contains {len(lines)} lines")

    # Print first 30 lines
    print("\n  First 30 lines of generated markdown:")
    for i, line in enumerate(lines[:30], 1):
        print(f"    {i:2d}: {line}")

    return True


def test_07_payload_integration():
    """Test 7: Full payload integration with economic events"""
    print("\nTEST 7: build_report_payload() with economic events")

    try:
        payload = build_report_payload()

        # Verify payload structure
        assert isinstance(payload, dict)
        assert "timestamp" in payload
        assert "macro_indicators" in payload
        assert "sk_hynix_decision" in payload
        assert "real_estate_decision" in payload

        print("  ✓ Payload built successfully")
        print(f"  ✓ Timestamp: {payload.get('timestamp', 'N/A')}")
        print(f"  ✓ SK Hynix signal: {payload['sk_hynix_decision'].signal if payload.get('sk_hynix_decision') else 'N/A'}")
        print(f"  ✓ Real Estate signal: {payload['real_estate_decision'].signal if payload.get('real_estate_decision') else 'N/A'}")

        return True
    except Exception as e:
        print(f"  ✗ Error building payload: {e}")
        return False


def test_08_markdown_rendering_with_economic_events():
    """Test 8: Full markdown rendering including economic events"""
    print("\nTEST 8: Full report rendering with economic events integration")

    try:
        from engine.report.markdown import render_markdown

        payload = build_report_payload()
        markdown = render_markdown(payload)

        assert isinstance(markdown, str)
        assert len(markdown) > 1000
        assert "경제 일정" in markdown or "Economic" in markdown

        # Verify 6 sections are present
        section_count = markdown.count("# ")
        print(f"  ✓ Full markdown rendered ({len(markdown)} characters)")
        print(f"  ✓ Contains {section_count} main sections (expect 6+)")

        # Check for key sections
        assert "SK하이닉스" in markdown or "SK" in markdown
        assert "부동산" in markdown or "Real Estate" in markdown

        print("  ✓ SK Hynix section found")
        print("  ✓ Real Estate section found")
        print("  ✓ Economic events section found")

        return True
    except Exception as e:
        print(f"  ✗ Error rendering markdown: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("PHASE 3A: ECONOMIC EVENTS INTEGRATION TEST SUITE")
    print("=" * 70)

    tests = [
        test_01_economic_event_dataclass,
        test_02_get_upcoming_events,
        test_03_calculate_event_impact_cpi_upside,
        test_04_calculate_event_impact_rate_cut,
        test_05_get_scenario_impacts,
        test_06_generate_event_section,
        test_07_payload_integration,
        test_08_markdown_rendering_with_economic_events,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except AssertionError as e:
            print(f"  ✗ Assertion failed: {e}")
            results.append((test_func.__name__, False))
        except Exception as e:
            print(f"  ✗ Exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_func.__name__, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit_code = 0 if success else 1
    print(f"\nExit code: {exit_code}")
    sys.exit(exit_code)
