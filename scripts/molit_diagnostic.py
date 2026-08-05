"""One-off diagnostic: hit each MOLIT 실거래가 endpoint directly for one region/month and print
the raw response, so a live run makes 활용신청 propagation / wrong-endpoint / genuinely-empty-month
issues immediately distinguishable from each other — not part of the regular pipeline.

Run via .github/workflows/molit-diagnostic.yml (workflow_dispatch). This repo is public, so the
real DATA_GO_KR_KEY value is scrubbed from every printed string via a direct substring replace —
not just a query-param regex — before anything reaches stdout, since data.go.kr's own error
bodies sometimes echo the key back in free text (see collectors/molit.py's _fetch_region_month
docstring on this).
"""
from __future__ import annotations

import os
import sys

import requests

ENDPOINTS = {
    "molit (아파트 매매 상세)": "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev",
    "molit_rent (아파트 전월세)": "https://apis.data.go.kr/1613000/RTMSDataSvcAptRent/getRTMSDataSvcAptRent",
    "molit_villa (연립다세대 매매)": "https://apis.data.go.kr/1613000/RTMSDataSvcRHTrade/getRTMSDataSvcRHTrade",
    "molit_officetel (오피스텔 매매)": "https://apis.data.go.kr/1613000/RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade",
}


def _scrub(text: str, api_key: str) -> str:
    """Unconditional substring replace, not a query-param regex — catches the key wherever it
    shows up (query string, echoed-back error text, anywhere), which a pattern like
    `[?&]key=...` can miss."""
    return text.replace(api_key, "***") if api_key else text


def main() -> None:
    api_key = os.environ.get("DATA_GO_KR_KEY")
    if not api_key:
        print("DATA_GO_KR_KEY not set")
        sys.exit(1)

    lawd_cd = sys.argv[1] if len(sys.argv) > 1 else "11110"  # 종로구 — probe region for every collector
    deal_ymd = sys.argv[2] if len(sys.argv) > 2 else "202606"

    for label, url in ENDPOINTS.items():
        print(f"\n===== {label} =====")
        print(f"URL: {url}")
        try:
            resp = requests.get(url, params={
                "serviceKey": api_key, "LAWD_CD": lawd_cd, "DEAL_YMD": deal_ymd,
                "pageNo": 1, "numOfRows": 10, "type": "json",
            }, timeout=10)
            print(f"HTTP {resp.status_code}")
            print(_scrub(resp.text[:1500], api_key))
        except Exception as exc:
            print(f"EXCEPTION: {_scrub(str(exc), api_key)}")


if __name__ == "__main__":
    main()
