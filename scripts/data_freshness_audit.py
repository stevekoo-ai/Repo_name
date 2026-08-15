"""Which collected series have gone stale, and how badly.

WHY
───
Jobs exiting 0 is not evidence that data arrived. Three ECOS series sat at
2018-08-24 for 2,912 days while every workflow reported success, and the
report published one of them (한국 10Y 1.56%) as a current rate — inventing a
US-KR spread that never existed. A green pipeline told us nothing.

This checks the thing that actually matters: the newest observation in each
normalized series, measured against how often that series is supposed to
update. Run it any time; wire it into CI if you want staleness to be loud.

    python -m scripts.data_freshness_audit            # human-readable table
    python -m scripts.data_freshness_audit --strict   # exit 1 if anything is dead

Tolerances are per-frequency because "stale" means different things for a
daily FX quote and a quarterly GDP print. They are deliberately generous —
this is meant to catch dead collectors, not to nag about ordinary release lag.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NORMALIZED = REPO_ROOT / "data" / "normalized"

# max age in days before a series is suspect / considered dead
TOLERANCE = {
    "daily":     (10,   60),
    "monthly":   (75,   200),
    "quarterly": (150,  400),
    "unknown":   (75,   365),
}

# Frequency can't be read back from a bare (date,value) CSV, so infer it from
# the median gap between the last observations — good enough to pick a bucket.
def _infer_frequency(dates: list[date]) -> str:
    if len(dates) < 3:
        return "unknown"
    gaps = sorted((dates[i] - dates[i - 1]).days for i in range(1, min(len(dates), 30)))
    med = gaps[len(gaps) // 2]
    if med <= 5:
        return "daily"
    if med <= 45:
        return "monthly"
    if med <= 130:
        return "quarterly"
    return "unknown"


def _read_dates(path: Path) -> list[date]:
    out: list[date] = []
    try:
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row and row[0][:2] == "20":
                    try:
                        out.append(date.fromisoformat(row[0][:10]))
                    except ValueError:
                        continue
    except Exception:
        return []
    return sorted(out)


def audit(today: date | None = None) -> list[dict]:
    today = today or date.today()
    results = []
    for path in sorted(NORMALIZED.glob("*.csv")):
        dates = _read_dates(path)
        if not dates:
            continue
        freq = _infer_frequency(dates)
        age = (today - dates[-1]).days
        warn_at, dead_at = TOLERANCE[freq]
        status = "dead" if age > dead_at else ("stale" if age > warn_at else "ok")
        results.append({
            "series": path.stem, "last": dates[-1].isoformat(), "age_days": age,
            "frequency": freq, "status": status, "rows": len(dates),
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="exit 1 when any series is dead")
    args = ap.parse_args()

    rows = audit()
    dead = [r for r in rows if r["status"] == "dead"]
    stale = [r for r in rows if r["status"] == "stale"]

    if dead or stale:
        print(f"{'series':<44}{'last':>12}{'age':>7}  freq        status")
        print("-" * 82)
        for r in sorted(dead + stale, key=lambda r: -r["age_days"]):
            mark = "DEAD " if r["status"] == "dead" else "stale"
            print(f"{r['series']:<44}{r['last']:>12}{r['age_days']:>6}d  "
                  f"{r['frequency']:<11} {mark}")
        print("-" * 82)

    print(f"{len(rows)} series — ok {len(rows)-len(dead)-len(stale)} / "
          f"stale {len(stale)} / dead {len(dead)}")

    if dead:
        print("\nDead series are collectors that are not collecting. Check, in order:")
        print("  1. the series spec (stat_code / item_code / cycle) against the provider")
        print("  2. response pagination — a reply that exactly fills the page limit is")
        print("     truncated, and the missing part is always the recent end")
        print("  3. whether the workflow that feeds it still exists on the default branch")

    return 1 if (args.strict and dead) else 0


if __name__ == "__main__":
    sys.exit(main())
