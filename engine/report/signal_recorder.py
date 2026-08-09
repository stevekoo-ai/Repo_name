"""
Signal Recorder — Persistent Storage of Daily SK Hynix & Real Estate Signals

Records each day's decision signals (SK Hynix HOLD/BUY/SELL + confidence,
Real Estate WAIT/ENTER + confidence) to enable rolling aggregation.

Storage: CSV file under data/daily_signals/ with append-only pattern.
"""
import sys
import csv
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional

# Import DailySignal dataclass
from rolling_aggregator import DailySignal


DATA_DIR = Path(__file__).parent.parent.parent / "data" / "daily_signals"


def ensure_signal_directory():
    """Create data/daily_signals directory if it doesn't exist"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_signal_file_path(date: Optional[str] = None) -> Path:
    """
    Get path to signal CSV file.

    Args:
        date: YYYY-MM-DD format, defaults to current date

    Returns:
        Path to signal_YYYYMM.csv (monthly file for easy archiving)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    year_month = date[:7]  # YYYY-MM
    return DATA_DIR / f"signal_{year_month}.csv"


def record_daily_signal(
    date: str,  # YYYY-MM-DD
    sk_hynix_signal: str,  # HOLD, BUY, SELL
    sk_hynix_confidence: float,  # 0-100
    real_estate_signal: str,  # WAIT, ENTER
    real_estate_confidence: float,  # 0-100
    notes: Optional[str] = None
) -> bool:
    """
    Record a single day's decision signals.

    Args:
        date: Date of the signal (YYYY-MM-DD)
        sk_hynix_signal: HOLD, BUY, or SELL
        sk_hynix_confidence: 0-100
        real_estate_signal: WAIT or ENTER
        real_estate_confidence: 0-100
        notes: Optional notes about this day

    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_signal_directory()

        signal_file = get_signal_file_path(date)
        file_exists = signal_file.exists()

        with open(signal_file, "a", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "date",
                    "sk_hynix_signal",
                    "sk_hynix_confidence",
                    "real_estate_signal",
                    "real_estate_confidence",
                    "notes",
                ]
            )

            # Write header if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "date": date,
                "sk_hynix_signal": sk_hynix_signal,
                "sk_hynix_confidence": sk_hynix_confidence,
                "real_estate_signal": real_estate_signal,
                "real_estate_confidence": real_estate_confidence,
                "notes": notes or "",
            })

        return True
    except Exception as e:
        print(f"Error recording signal: {e}")
        return False


def load_signals(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[DailySignal]:
    """
    Load signals from CSV files in date range.

    Args:
        start_date: YYYY-MM-DD, defaults to 90 days ago
        end_date: YYYY-MM-DD, defaults to today

    Returns:
        List of DailySignal objects sorted by date
    """
    try:
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if start_date is None:
            start_days_ago = datetime.now() - timedelta(days=90)
            start_date = start_days_ago.strftime("%Y-%m-%d")

        signals: List[DailySignal] = []

        # Determine which monthly files to read
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        current_dt = start_dt

        while current_dt <= end_dt:
            signal_file = get_signal_file_path(current_dt.strftime("%Y-%m-%d"))

            if signal_file.exists():
                with open(signal_file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row_date = row["date"]
                        if start_date <= row_date <= end_date:
                            signal = DailySignal(
                                date=row_date,
                                sk_hynix_signal=row["sk_hynix_signal"],
                                sk_hynix_confidence=float(row["sk_hynix_confidence"]),
                                real_estate_signal=row["real_estate_signal"],
                                real_estate_confidence=float(row["real_estate_confidence"]),
                                notes=row.get("notes") or None,
                            )
                            signals.append(signal)

            # Move to next month
            if current_dt.month == 12:
                current_dt = current_dt.replace(year=current_dt.year + 1, month=1)
            else:
                current_dt = current_dt.replace(month=current_dt.month + 1)

        # Sort by date
        signals.sort(key=lambda s: s.date)
        return signals

    except Exception as e:
        print(f"Error loading signals: {e}")
        return []


# Example usage
if __name__ == "__main__":
    print("Signal Recorder Example")
    print("=" * 60)

    # Record sample signals
    print("\nRecording sample signals...")
    record_daily_signal(
        date="2026-08-01",
        sk_hynix_signal="HOLD",
        sk_hynix_confidence=50.0,
        real_estate_signal="WAIT",
        real_estate_confidence=60.0,
        notes="Market opening"
    )
    print("✓ Recorded 2026-08-01")

    record_daily_signal(
        date="2026-08-02",
        sk_hynix_signal="HOLD",
        sk_hynix_confidence=48.0,
        real_estate_signal="WAIT",
        real_estate_confidence=62.0,
        notes="Slight decline"
    )
    print("✓ Recorded 2026-08-02")

    # Load signals
    print("\nLoading signals for past 30 days...")
    signals = load_signals()
    print(f"✓ Loaded {len(signals)} signals")

    for sig in signals[-5:]:  # Show last 5
        print(f"  {sig.date}: SK={sig.sk_hynix_signal}({sig.sk_hynix_confidence}%), "
              f"RE={sig.real_estate_signal}({sig.real_estate_confidence}%)")

    print("\nSignal files stored in: data/daily_signals/")
