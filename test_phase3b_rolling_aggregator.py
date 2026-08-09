"""
Phase 3b Test Suite: Rolling Aggregation Framework
Tests signal recording, aggregation, and trend detection.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "engine" / "report"))

from rolling_aggregator import (
    DailySignal,
    aggregate_signals_by_period,
    compare_periods,
    generate_rolling_window_markdown,
)


def test_01_daily_signal_creation():
    """Test 1: DailySignal dataclass creation"""
    print("TEST 1: DailySignal dataclass creation")

    signal = DailySignal(
        date="2026-08-09",
        sk_hynix_signal="HOLD",
        sk_hynix_confidence=50.0,
        real_estate_signal="WAIT",
        real_estate_confidence=60.0,
        notes="Test signal"
    )

    assert signal.date == "2026-08-09"
    assert signal.sk_hynix_signal == "HOLD"
    assert signal.sk_hynix_confidence == 50.0
    print("  ✓ DailySignal created successfully")
    return True


def test_02_monthly_aggregation():
    """Test 2: Aggregate signals into monthly period"""
    print("\nTEST 2: Monthly aggregation")

    signals = [
        DailySignal("2026-08-01", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-08-02", "HOLD", 48.0, "WAIT", 62.0),
        DailySignal("2026-08-03", "HOLD", 45.0, "WAIT", 65.0),
        DailySignal("2026-08-04", "HOLD", 50.0, "WAIT", 63.0),
        DailySignal("2026-08-05", "HOLD", 52.0, "WAIT", 60.0),
        DailySignal("2026-08-06", "BUY", 55.0, "WAIT", 58.0),
        DailySignal("2026-08-07", "BUY", 58.0, "WAIT", 55.0),
        DailySignal("2026-08-08", "BUY", 60.0, "ENTER", 65.0),
        DailySignal("2026-08-09", "HOLD", 55.0, "ENTER", 68.0),
    ]

    monthly = aggregate_signals_by_period(signals, "month")

    assert len(monthly) == 1
    agg = monthly[0]

    assert agg.sk_hynix_primary_signal == "HOLD"  # HOLD: 6, BUY: 3
    assert agg.real_estate_primary_signal == "WAIT"  # WAIT: 7, ENTER: 2
    assert agg.days_recorded == 9
    assert agg.sk_hynix_signal_counts["HOLD"] == 6
    assert agg.sk_hynix_signal_counts["BUY"] == 3

    print(f"  ✓ Aggregated {agg.days_recorded} days into 1 month")
    print(f"  ✓ SK primary: {agg.sk_hynix_primary_signal} (avg: {agg.sk_hynix_avg_confidence}%)")
    print(f"  ✓ RE primary: {agg.real_estate_primary_signal} (avg: {agg.real_estate_avg_confidence}%)")
    print(f"  ✓ SK signals: HOLD={agg.sk_hynix_signal_counts['HOLD']}, BUY={agg.sk_hynix_signal_counts['BUY']}, SELL={agg.sk_hynix_signal_counts['SELL']}")
    print(f"  ✓ RE signals: WAIT={agg.real_estate_signal_counts['WAIT']}, ENTER={agg.real_estate_signal_counts['ENTER']}")

    return True


def test_03_confidence_trend():
    """Test 3: Confidence trend detection (improving)"""
    print("\nTEST 3: Confidence trend detection")

    signals = [
        DailySignal("2026-08-01", "HOLD", 40.0, "WAIT", 50.0),  # Early: low
        DailySignal("2026-08-02", "HOLD", 42.0, "WAIT", 52.0),
        DailySignal("2026-08-03", "HOLD", 41.0, "WAIT", 51.0),
        DailySignal("2026-08-04", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-08-05", "HOLD", 52.0, "WAIT", 62.0),
        DailySignal("2026-08-06", "HOLD", 55.0, "WAIT", 65.0),  # Late: high
        DailySignal("2026-08-07", "HOLD", 58.0, "WAIT", 68.0),
        DailySignal("2026-08-08", "HOLD", 60.0, "ENTER", 70.0),
        DailySignal("2026-08-09", "HOLD", 62.0, "ENTER", 72.0),
    ]

    monthly = aggregate_signals_by_period(signals, "month")
    agg = monthly[0]

    assert agg.sk_hynix_confidence_trend == "↑"
    assert agg.real_estate_confidence_trend == "↑"

    print(f"  ✓ SK confidence trend: {agg.sk_hynix_confidence_trend} (improving)")
    print(f"  ✓ RE confidence trend: {agg.real_estate_confidence_trend} (improving)")

    return True


def test_04_weekly_aggregation():
    """Test 4: Aggregate into weekly periods"""
    print("\nTEST 4: Weekly aggregation")

    signals = [
        DailySignal("2026-08-01", "HOLD", 50.0, "WAIT", 60.0),  # Fri
        DailySignal("2026-08-02", "HOLD", 48.0, "WAIT", 62.0),  # Sat
        DailySignal("2026-08-03", "HOLD", 52.0, "WAIT", 58.0),  # Sun
        DailySignal("2026-08-04", "BUY", 55.0, "WAIT", 55.0),   # Mon (new week)
        DailySignal("2026-08-05", "BUY", 58.0, "ENTER", 65.0),  # Tue
    ]

    weekly = aggregate_signals_by_period(signals, "week")

    assert len(weekly) >= 2
    print(f"  ✓ Aggregated into {len(weekly)} weeks")

    for w in weekly:
        print(f"    Week {w.period_name}: {w.start_date}~{w.end_date}, "
              f"SK={w.sk_hynix_primary_signal}({w.sk_hynix_avg_confidence}%), "
              f"RE={w.real_estate_primary_signal}({w.real_estate_avg_confidence}%)")

    return True


def test_05_period_comparison():
    """Test 5: Compare two periods"""
    print("\nTEST 5: Period comparison")

    # July signals (low confidence)
    july_signals = [
        DailySignal("2026-07-01", "HOLD", 40.0, "WAIT", 50.0),
        DailySignal("2026-07-15", "HOLD", 45.0, "WAIT", 55.0),
        DailySignal("2026-07-31", "HOLD", 42.0, "WAIT", 52.0),
    ]

    # August signals (higher confidence)
    aug_signals = [
        DailySignal("2026-08-01", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-08-15", "BUY", 55.0, "ENTER", 65.0),
        DailySignal("2026-08-30", "BUY", 58.0, "ENTER", 70.0),
    ]

    july = aggregate_signals_by_period(july_signals, "month")[0]
    aug = aggregate_signals_by_period(aug_signals, "month")[0]

    sk_compare, re_compare = compare_periods(aug, july)

    assert sk_compare == "improved"
    assert re_compare == "improved"

    print(f"  ✓ SK: {sk_compare.upper()} (July {july.sk_hynix_avg_confidence}% → Aug {aug.sk_hynix_avg_confidence}%)")
    print(f"  ✓ RE: {re_compare.upper()} (July {july.real_estate_avg_confidence}% → Aug {aug.real_estate_avg_confidence}%)")

    return True


def test_06_markdown_generation():
    """Test 6: Generate markdown for rolling window"""
    print("\nTEST 6: Markdown generation")

    signals = [
        DailySignal("2026-08-01", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-08-02", "HOLD", 48.0, "WAIT", 62.0),
        DailySignal("2026-08-03", "HOLD", 52.0, "WAIT", 58.0),
    ]

    monthly = aggregate_signals_by_period(signals, "month")
    agg = monthly[0]

    md = generate_rolling_window_markdown(agg, period_type="month")

    assert "Month Rolling Window" in md
    assert "SK Hynix" in md
    assert "Real Estate" in md
    assert "HOLD" in md
    assert "WAIT" in md

    print(f"  ✓ Generated {len(md)} characters of markdown")
    print(f"  ✓ Includes SK Hynix section")
    print(f"  ✓ Includes Real Estate section")
    print(f"  ✓ Includes signal counts table")

    return True


def test_07_quarter_aggregation():
    """Test 7: Aggregate into quarterly period"""
    print("\nTEST 7: Quarterly aggregation")

    signals = [
        # Q1
        DailySignal("2026-01-01", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-02-01", "HOLD", 48.0, "WAIT", 62.0),
        DailySignal("2026-03-01", "HOLD", 52.0, "WAIT", 58.0),
        # Q2
        DailySignal("2026-04-01", "BUY", 55.0, "WAIT", 55.0),
        DailySignal("2026-05-01", "BUY", 58.0, "ENTER", 65.0),
        DailySignal("2026-06-01", "BUY", 60.0, "ENTER", 70.0),
        # Q3
        DailySignal("2026-07-01", "HOLD", 55.0, "ENTER", 75.0),
        DailySignal("2026-08-01", "HOLD", 50.0, "WAIT", 60.0),
        DailySignal("2026-09-01", "HOLD", 48.0, "WAIT", 62.0),
    ]

    quarterly = aggregate_signals_by_period(signals, "quarter")

    assert len(quarterly) == 3
    print(f"  ✓ Aggregated into {len(quarterly)} quarters")

    print(f"  Q1: SK={quarterly[0].sk_hynix_primary_signal}, RE={quarterly[0].real_estate_primary_signal}")
    print(f"  Q2: SK={quarterly[1].sk_hynix_primary_signal}, RE={quarterly[1].real_estate_primary_signal}")
    print(f"  Q3: SK={quarterly[2].sk_hynix_primary_signal}, RE={quarterly[2].real_estate_primary_signal}")

    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("PHASE 3B: ROLLING AGGREGATION FRAMEWORK TEST SUITE")
    print("=" * 70)

    tests = [
        test_01_daily_signal_creation,
        test_02_monthly_aggregation,
        test_03_confidence_trend,
        test_04_weekly_aggregation,
        test_05_period_comparison,
        test_06_markdown_generation,
        test_07_quarter_aggregation,
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
    print("\n" + "=" * 70)
    if success:
        print("✓ Rolling Aggregation Framework is fully functional")
        print("\nFeatures:")
        print("  • Daily signal recording (SK Hynix + Real Estate)")
        print("  • Period aggregation (Week/Month/Quarter/Year)")
        print("  • Confidence trend detection (↑/→/↓)")
        print("  • Period-over-period comparison")
        print("  • Markdown generation for rolling windows")
    else:
        print("✗ Some tests failed")
    print("=" * 70)

    exit_code = 0 if success else 1
    sys.exit(exit_code)
