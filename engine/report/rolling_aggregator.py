"""
Rolling Aggregator — Monthly/Quarterly/Annual Signal Trending
Part of Phase 3b: PEOS 5-Section Report Enhancement

Aggregates daily SK Hynix and Real Estate decision signals over rolling windows
(Week, Month, Quarter, Year) to identify trends and compare periods.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict


@dataclass
class DailySignal:
    """Single day's recorded decision signals"""
    date: str  # YYYY-MM-DD
    sk_hynix_signal: str  # HOLD, BUY, SELL
    sk_hynix_confidence: float  # 0-100
    real_estate_signal: str  # WAIT, ENTER
    real_estate_confidence: float  # 0-100
    notes: Optional[str] = None


@dataclass
class AggregatedPeriod:
    """Aggregated metrics for a time period"""
    period_name: str  # "Week", "Month", "Quarter", "Year"
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    days_recorded: int

    # SK Hynix aggregates
    sk_hynix_primary_signal: str  # Most common signal
    sk_hynix_avg_confidence: float
    sk_hynix_signal_counts: Dict[str, int]  # {"HOLD": 15, "BUY": 5, "SELL": 0}
    sk_hynix_confidence_trend: str  # "↑", "→", "↓"

    # Real Estate aggregates
    real_estate_primary_signal: str
    real_estate_avg_confidence: float
    real_estate_signal_counts: Dict[str, int]  # {"WAIT": 18, "ENTER": 2}
    real_estate_confidence_trend: str  # "↑", "→", "↓"

    # Comparisons
    sk_hynix_vs_prev: Optional[str] = None  # "improved", "same", "declined"
    real_estate_vs_prev: Optional[str] = None


def aggregate_signals_by_period(
    signals: List[DailySignal],
    period_type: str  # "week", "month", "quarter", "year"
) -> List[AggregatedPeriod]:
    """
    Aggregate daily signals into time periods.

    Args:
        signals: List of DailySignal records (sorted by date)
        period_type: One of "week", "month", "quarter", "year"

    Returns:
        List of AggregatedPeriod objects, one per period
    """
    if not signals:
        return []

    periods: Dict[str, Dict] = defaultdict(lambda: {
        "dates": [],
        "sk_signals": [],
        "sk_confidences": [],
        "re_signals": [],
        "re_confidences": [],
    })

    for signal in signals:
        date_obj = datetime.strptime(signal.date, "%Y-%m-%d")

        if period_type == "week":
            # ISO week (Mon-Sun)
            year, week, _ = date_obj.isocalendar()
            period_key = f"{year}-W{week:02d}"
        elif period_type == "month":
            period_key = date_obj.strftime("%Y-%m")
        elif period_type == "quarter":
            quarter = (date_obj.month - 1) // 3 + 1
            period_key = f"{date_obj.year}-Q{quarter}"
        elif period_type == "year":
            period_key = str(date_obj.year)
        else:
            raise ValueError(f"Unknown period type: {period_type}")

        periods[period_key]["dates"].append(signal.date)
        periods[period_key]["sk_signals"].append(signal.sk_hynix_signal)
        periods[period_key]["sk_confidences"].append(signal.sk_hynix_confidence)
        periods[period_key]["re_signals"].append(signal.real_estate_signal)
        periods[period_key]["re_confidences"].append(signal.real_estate_confidence)

    # Build aggregated results
    results: List[AggregatedPeriod] = []

    for period_key, data in sorted(periods.items()):
        if not data["dates"]:
            continue

        dates = data["dates"]
        start_date = min(dates)
        end_date = max(dates)

        # SK Hynix aggregates
        sk_signals = data["sk_signals"]
        sk_confidences = data["sk_confidences"]
        sk_counts = {}
        for sig in ["HOLD", "BUY", "SELL"]:
            sk_counts[sig] = sk_signals.count(sig)
        sk_primary = max(sk_counts, key=sk_counts.get)
        sk_avg_conf = sum(sk_confidences) / len(sk_confidences) if sk_confidences else 0

        # Determine SK confidence trend (first vs last 1/3 of period)
        third = len(sk_confidences) // 3
        if third > 0:
            first_avg = sum(sk_confidences[:third]) / third
            last_avg = sum(sk_confidences[-third:]) / third
            if last_avg > first_avg + 2:
                sk_trend = "↑"
            elif last_avg < first_avg - 2:
                sk_trend = "↓"
            else:
                sk_trend = "→"
        else:
            sk_trend = "→"

        # Real Estate aggregates
        re_signals = data["re_signals"]
        re_confidences = data["re_confidences"]
        re_counts = {}
        for sig in ["WAIT", "ENTER"]:
            re_counts[sig] = re_signals.count(sig)
        re_primary = max(re_counts, key=re_counts.get)
        re_avg_conf = sum(re_confidences) / len(re_confidences) if re_confidences else 0

        # Determine RE confidence trend
        if third > 0:
            first_avg = sum(re_confidences[:third]) / third
            last_avg = sum(re_confidences[-third:]) / third
            if last_avg > first_avg + 2:
                re_trend = "↑"
            elif last_avg < first_avg - 2:
                re_trend = "↓"
            else:
                re_trend = "→"
        else:
            re_trend = "→"

        agg = AggregatedPeriod(
            period_name=period_type.capitalize(),
            start_date=start_date,
            end_date=end_date,
            days_recorded=len(dates),
            sk_hynix_primary_signal=sk_primary,
            sk_hynix_avg_confidence=round(sk_avg_conf, 1),
            sk_hynix_signal_counts=sk_counts,
            sk_hynix_confidence_trend=sk_trend,
            real_estate_primary_signal=re_primary,
            real_estate_avg_confidence=round(re_avg_conf, 1),
            real_estate_signal_counts=re_counts,
            real_estate_confidence_trend=re_trend,
        )
        results.append(agg)

    return results


def compare_periods(
    current: AggregatedPeriod,
    previous: AggregatedPeriod
) -> tuple[str, str]:
    """
    Compare current period vs previous period.

    Returns:
        (sk_comparison, re_comparison) — each is "improved", "same", or "declined"
    """
    # SK Hynix comparison
    sk_signal_strength = {"SELL": 0, "HOLD": 1, "BUY": 2}
    current_sk_strength = sk_signal_strength.get(current.sk_hynix_primary_signal, 1)
    previous_sk_strength = sk_signal_strength.get(previous.sk_hynix_primary_signal, 1)

    if current.sk_hynix_avg_confidence > previous.sk_hynix_avg_confidence + 5:
        sk_compare = "improved"
    elif current.sk_hynix_avg_confidence < previous.sk_hynix_avg_confidence - 5:
        sk_compare = "declined"
    else:
        sk_compare = "same"

    # Real Estate comparison
    re_signal_strength = {"WAIT": 0, "ENTER": 1}
    current_re_strength = re_signal_strength.get(current.real_estate_primary_signal, 0)
    previous_re_strength = re_signal_strength.get(previous.real_estate_primary_signal, 0)

    if current.real_estate_avg_confidence > previous.real_estate_avg_confidence + 5:
        re_compare = "improved"
    elif current.real_estate_avg_confidence < previous.real_estate_avg_confidence - 5:
        re_compare = "declined"
    else:
        re_compare = "same"

    return sk_compare, re_compare


def generate_rolling_window_markdown(
    current_period: AggregatedPeriod,
    previous_period: Optional[AggregatedPeriod] = None,
    period_type: str = "month"
) -> str:
    """
    Generate markdown for rolling window summary.

    Args:
        current_period: Current period's aggregated data
        previous_period: Previous period for comparison
        period_type: "week", "month", "quarter", "year"

    Returns:
        Markdown string for rolling window section
    """
    md = f"\n## 📊 {period_type.capitalize()} Rolling Window ({current_period.start_date} ~ {current_period.end_date})\n\n"
    md += f"**기간**: {current_period.days_recorded}일 기록\n\n"

    # SK Hynix section
    md += "### SK Hynix: 보유/매도 추적\n\n"
    md += f"| 지표 | 값 |\n"
    md += f"|------|--------|\n"
    md += f"| 주요신호 | {current_period.sk_hynix_primary_signal} |\n"
    md += f"| 평균신뢰도 | {current_period.sk_hynix_avg_confidence}% {current_period.sk_hynix_confidence_trend} |\n"
    md += f"| HOLD | {current_period.sk_hynix_signal_counts.get('HOLD', 0)}일 |\n"
    md += f"| BUY | {current_period.sk_hynix_signal_counts.get('BUY', 0)}일 |\n"
    md += f"| SELL | {current_period.sk_hynix_signal_counts.get('SELL', 0)}일 |\n"
    md += "\n"

    # Real Estate section
    md += "### Real Estate: 진입/대기 추적\n\n"
    md += f"| 지표 | 값 |\n"
    md += f"|------|--------|\n"
    md += f"| 주요신호 | {current_period.real_estate_primary_signal} |\n"
    md += f"| 평균신뢰도 | {current_period.real_estate_avg_confidence}% {current_period.real_estate_confidence_trend} |\n"
    md += f"| WAIT | {current_period.real_estate_signal_counts.get('WAIT', 0)}일 |\n"
    md += f"| ENTER | {current_period.real_estate_signal_counts.get('ENTER', 0)}일 |\n"
    md += "\n"

    # Comparison section
    if previous_period:
        sk_compare, re_compare = compare_periods(current_period, previous_period)
        md += "### Period Comparison\n\n"
        md += f"- **SK Hynix**: {sk_compare.upper()} (이전 {previous_period.period_name}: {previous_period.sk_hynix_primary_signal} {previous_period.sk_hynix_avg_confidence}%)\n"
        md += f"- **Real Estate**: {re_compare.upper()} (이전 {previous_period.period_name}: {previous_period.real_estate_primary_signal} {previous_period.real_estate_avg_confidence}%)\n\n"

    return md


# Example usage and sample data for testing
if __name__ == "__main__":
    # Sample signals for August 2026 (30 days)
    sample_signals = [
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

    # Test aggregation
    monthly = aggregate_signals_by_period(sample_signals, "month")
    print("Monthly Aggregation:")
    for agg in monthly:
        print(f"  {agg.period_name} {agg.start_date}~{agg.end_date}")
        print(f"    SK: {agg.sk_hynix_primary_signal} ({agg.sk_hynix_avg_confidence}%)")
        print(f"    RE: {agg.real_estate_primary_signal} ({agg.real_estate_avg_confidence}%)")

    # Test markdown generation
    if monthly:
        md = generate_rolling_window_markdown(monthly[0], period_type="month")
        print("\nMarkdown Output:")
        print(md)
