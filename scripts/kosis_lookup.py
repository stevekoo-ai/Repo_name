"""One-off KOSIS statisticsParameterData.do candidate-table verifier.

collectors/kosis.py's four table IDs were guessed at build time (never
verified — see the "통계표 ID 확인 필요" notes) and all four now fail live
(either "해당 통계표가 존재하지 않습니다" or "잘못된 요청 변수를 호출 하였습니다").
Unlike ECOS, KOSIS has no simple keyword-search API reachable from outside
Korea, so this script instead takes a short list of *candidate* (orgId,
tblId) pairs per indicator — gathered from public references — and queries
each with itmId=ALL&objL1=ALL&objL2=ALL over a short recent window. A
candidate that responds with real rows is confirmed correct; the printed
ITM_ID/ITM_NM/C1/C1_NM values are exactly what collectors/kosis.py's
KOSIS_SERIES needs for itm_id/obj_l1 (a specific item, not "ALL", so the
collector keeps returning one number as before).

Usage:
    KOSIS_API_KEY=... python -m scripts.kosis_lookup
    KOSIS_API_KEY=... python -m scripts.kosis_lookup cpi_index
"""
from __future__ import annotations

import os
import sys
from datetime import datetime

import requests

KOSIS_BASE_URL = "https://kosis.kr/openapi"

# A few plausible (orgId, tblId) candidates per indicator, gathered from
# public references (KOSIS itself has no reachable-from-here keyword search).
CANDIDATES: dict[str, list[tuple[str, str]]] = {
    "cpi_index": [("101", "DT_1J22003"), ("101", "DT_1J17009")],
    "industrial_production_index": [("101", "DT_1JH20151")],
    "retail_sales_index": [("101", "DT_1K41002"), ("101", "DT_1K31009")],
    "unemployment_rate": [("101", "DT_1DA7004S")],
}


def _try_candidate(api_key: str, org_id: str, tbl_id: str, start: str, end: str, prd_se: str) -> dict:
    url = f"{KOSIS_BASE_URL}/Param/statisticsParameterData.do"
    params = {
        "method": "getList", "apiKey": api_key, "itmId": "ALL",
        "objL1": "ALL", "objL2": "ALL", "format": "json", "jsonVD": "Y",
        "prdSe": prd_se, "startPrdDe": start, "endPrdDe": end,
        "orgId": org_id, "tblId": tbl_id,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:  # network/JSON errors reported as-is, not raised
        return {"ok": False, "error": str(exc)}
    if isinstance(payload, dict) and payload.get("err"):
        return {"ok": False, "error": payload.get("errMsg", "unknown error"), "err_code": payload.get("err")}
    if not isinstance(payload, list) or not payload:
        return {"ok": False, "error": "empty response"}
    return {"ok": True, "rows": payload}


def main() -> None:
    api_key = os.environ.get("KOSIS_API_KEY")
    if not api_key:
        print("KOSIS_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    today = datetime.utcnow()
    end_m = today.strftime("%Y%m")
    start_m = today.replace(year=today.year - 1).strftime("%Y%m")

    only = sys.argv[1] if len(sys.argv) > 1 else None
    series_keys = [only] if only else list(CANDIDATES)

    for key in series_keys:
        print(f"\n=== {key} ===")
        for org_id, tbl_id in CANDIDATES[key]:
            print(f"-- orgId={org_id} tblId={tbl_id} (prdSe=M, {start_m}-{end_m})")
            result = _try_candidate(api_key, org_id, tbl_id, start_m, end_m, "M")
            if not result["ok"]:
                print(f"   FAILED: {result['error']}")
                continue
            rows = result["rows"]
            seen: set[tuple[str, str]] = set()
            print(f"   OK — {len(rows)} rows returned. Distinct ITM_ID/C1 combos:")
            for r in rows:
                combo = (r.get("ITM_ID"), r.get("C1"))
                if combo in seen:
                    continue
                seen.add(combo)
                print(f"     ITM_ID={r.get('ITM_ID')} ITM_NM={r.get('ITM_NM')} "
                      f"C1={r.get('C1')} C1_NM={r.get('C1_NM')} "
                      f"(sample: PRD_DE={r.get('PRD_DE')} DT={r.get('DT')})")


if __name__ == "__main__":
    main()
