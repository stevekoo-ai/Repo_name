"""Collect the Core-10 macro series. Data only — no report, no email, no push.

WHY THIS EXISTS
───────────────
Core-10 collection (KOSIS + ECOS + FRED) only ever ran as a side effect of
`python -m engine.report.run`, i.e. inside daily-peos-report.yml. That workflow
was deleted from main on 2026-08-11 under the "remove push/email code" policy —
correctly, for the publishing half of what it did. But it was doing two jobs,
and only one of them was the reason for removal:

    리포트 생성 · 푸시 · 이메일   ← the policy target
    Core-10 지표 수집             ← collateral damage

Since then nothing refreshes the Core-10 indicators. macro-data-sync.yml covers
the market-data layer (rates, FX, oil) via scripts/macro_data.py and does not
touch KOSIS at all, so KOSIS_API_KEY reaches only kosis-lookup.yml, a manual
diagnostic. Result: zero kosis_*.csv files on disk, four Core-10 indicators
(산업생산·소매판매·CPI·실업률) falling back to OECD mirrors, two of which are
themselves dead — which is why every report since has shown most indicators as
carried forward.

This restores the collection half alone. It imports no report code and writes
nothing but normalized series, so it fits the surviving collection workflows
rather than reviving the publishing one.

    python -m scripts.collect_core10           # collect, report outcome
    python -m scripts.collect_core10 --strict  # exit 1 if any source fails
"""
from __future__ import annotations

import argparse
import sys

from collectors import ecos, fred, kosis
from core.models import DataStatus

# KOSIS keys used by engine/macro/indicators.py (build_core10_readings).
KOSIS_KEYS = ["industrial_production_index", "retail_sales_index",
              "cpi_index", "unemployment_rate",
              # 2026-09-15 추가. 원래 collectors/kosis.py 자체 docstring이
              # "Core-10 4개 지표 전용이라 얹지 않기로" 했던 것들이다 —
              # 대신 engine/crisis_analysis/scoring.py::score_semiconductor_cycle()
              # 안에서 직접 fetch_series()를 부르는 방식으로 설계됐는데, 그
              # 함수를 실제로 호출하는 유일한 경로였던 daily-peos-report.yml이
              # 2026-08-11 정책으로 main에서 제거되면서 이 두 시리즈는 아무
              # 스케줄에도 안 걸리는 고아가 됐다 — Core-10 4개 지표가 겪었던
              # 것과 정확히 같은 "collateral damage" 패턴. 그때 수집이
              # 이 파일로 옮겨온 것과 같은 이유로 여기 재사용한다.
              "semiconductor_shipment_index", "semiconductor_inventory_index"]

# ECOS keys backing Core-10. base_rate/usdkrw/yields are already covered by
# macro-data-sync, but re-fetching is cheap and keeps this entry point complete.
ECOS_KEYS = ["gdp_growth_qoq", "ppi_yoy_level", "current_account",
             "base_rate", "usdkrw", "kr_3y_yield", "kr_10y_yield"]


def _run_one(label: str, fn) -> tuple[str, bool, str]:
    try:
        dp = fn()
    except Exception as exc:
        return label, False, f"예외: {exc}"

    status = getattr(dp, "status", None)
    if status == DataStatus.OK:
        return label, True, f"OK (value={getattr(dp, 'value', '?')})"
    note = getattr(dp, "note", None) or getattr(dp, "detail", "") or str(status)
    return label, False, f"{status}: {note}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when any source fails (default: report and continue)")
    args = ap.parse_args()

    results: list[tuple[str, bool, str]] = []

    for key in KOSIS_KEYS:
        results.append(_run_one(f"kosis:{key}", lambda k=key: kosis.fetch_series(k)))
    for key in ECOS_KEYS:
        results.append(_run_one(f"ecos:{key}", lambda k=key: ecos.fetch_series(k)))

    # FRED exposes a bulk fetch. A non-empty return is NOT success — a blocked
    # network still yields a full list of failed DataPoints, which would report
    # "22 series ✅" while collecting nothing. Count OK statuses instead.
    try:
        got = fred.fetch_all()
        points = list(got.values()) if isinstance(got, dict) else list(got or [])
        ok_n = sum(1 for p in points if getattr(p, "status", None) == DataStatus.OK)
        results.append(("fred:fetch_all", ok_n > 0,
                        f"{ok_n}/{len(points)} series OK"))
    except Exception as exc:
        results.append(("fred:fetch_all", False, f"예외: {exc}"))

    width = max(len(r[0]) for r in results)
    print(f"{'source':<{width}}  result")
    print("-" * (width + 40))
    for label, ok, detail in results:
        print(f"{label:<{width}}  {'✅' if ok else '❌'} {detail[:70]}")
    print("-" * (width + 40))

    failed = [r for r in results if not r[1]]
    print(f"{len(results) - len(failed)}/{len(results)} succeeded")

    if failed:
        print("\nFailures here mean the report will carry those indicators forward.")
        print("Check the API key is present in the environment, then the series spec.")

    return 1 if (args.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())
