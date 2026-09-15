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

## 2026-09-15 fix — annual series had no bucket, so they all read as DEAD

IMF WEO series (16 of them: gdp_growth/inflation/current_account/govt_debt/
unemployment × KOR/USA/CHN/JPN) update once a year — median gap between rows
is exactly 365 days. That fell through every existing bucket (daily≤5,
monthly≤45, quarterly≤130) into "unknown" (tolerance 75/365 days), so 622
days since the last actual (2025 — 2026 hasn't closed yet, WEO publishes
actuals for a closing year the following April) read as DEAD even though the
collector was working perfectly every time it ran (verified against real
GitHub Actions job logs: `fred:fetch_all ✅ 22/22`, `28/28 succeeded` for
BLS+IMF — this was a false alarm from the audit tool, not a dead collector).
Added an `annual` bucket sized for that publication rhythm.

Also: two FRED series (`kr_cpi_oecd`, `kr_industrial_production_oecd`,
FRED codes KORCPIALLMINMEI/KORPROINDMISMEI) collect successfully every run
(confirmed in the same job logs) but the series themselves stopped updating
at the source in 2023-11/2024-03 — the same kind of upstream discontinuation
as `us_dollar_index_major`/DTWEXM (already documented in engine/health/
registry.py). They're KOSIS fallbacks (engine/macro/indicators.py only
reaches them when KOSIS itself fails), not the primary path, so keeping them
around for historical continuity is correct — but they should stop being
reported as an actionable "collector broken" DEAD every day. `KNOWN_DEAD_BY_DESIGN`
names them explicitly (not silently — still shown, just not as DEAD) so this
isn't a second silent exemption pile-up.
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
    "annual":    (450,  800),
    "unknown":   (75,   365),
}

# Series confirmed (2026-09-15, against live GitHub Actions job logs, not
# just local files) to collect successfully every run but whose *upstream*
# source has stopped publishing — collection is not the problem, so DEAD
# would be a permanent false alarm. Each entry names why and what it's a
# fallback for, so the exemption itself stays auditable rather than becoming
# another thing nobody remembers the reason for.
KNOWN_DEAD_BY_DESIGN = {
    "fred_kr_cpi_oecd": (
        "OECD MEI mirror (KORCPIALLMINMEI) discontinued upstream 2023-11 — "
        "same pattern as us_dollar_index_major/DTWEXM. KOSIS(cpi_index) is "
        "the primary source; this is only engine/macro/indicators.py's "
        "fallback when KOSIS is unreachable."
    ),
    "fred_kr_industrial_production_oecd": (
        "OECD MEI mirror (KORPROINDMISMEI) discontinued upstream 2024-03 — "
        "same pattern. KOSIS(industrial_production_index) is primary."
    ),
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
    if med <= 400:
        return "annual"
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
        known_reason = KNOWN_DEAD_BY_DESIGN.get(path.stem)
        if status == "dead" and known_reason:
            status = "dead_by_design"  # still visible, not reported as an actionable failure
        results.append({
            "series": path.stem, "last": dates[-1].isoformat(), "age_days": age,
            "frequency": freq, "status": status, "rows": len(dates),
            "known_reason": known_reason,
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="exit 1 when any series is dead")
    args = ap.parse_args()

    rows = audit()
    dead = [r for r in rows if r["status"] == "dead"]
    stale = [r for r in rows if r["status"] == "stale"]
    known = [r for r in rows if r["status"] == "dead_by_design"]

    if dead or stale or known:
        print(f"{'series':<44}{'last':>12}{'age':>7}  freq        status")
        print("-" * 82)
        for r in sorted(dead + stale + known, key=lambda r: -r["age_days"]):
            mark = {"dead": "DEAD ", "stale": "stale", "dead_by_design": "known"}[r["status"]]
            print(f"{r['series']:<44}{r['last']:>12}{r['age_days']:>6}d  "
                  f"{r['frequency']:<11} {mark}")
            if r["status"] == "dead_by_design":
                print(f"  └ {r['known_reason']}")
        print("-" * 82)

    print(f"{len(rows)} series — ok {len(rows)-len(dead)-len(stale)-len(known)} / "
          f"stale {len(stale)} / dead {len(dead)} / known-dead-by-design {len(known)}")

    if dead:
        print("\nDead series are collectors that are not collecting. Check, in order:")
        print("  1. the series spec (stat_code / item_code / cycle) against the provider")
        print("  2. response pagination — a reply that exactly fills the page limit is")
        print("     truncated, and the missing part is always the recent end")
        print("  3. whether the workflow that feeds it still exists on the default branch")

    return 1 if (args.strict and dead) else 0


if __name__ == "__main__":
    sys.exit(main())
