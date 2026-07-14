"""One-off ECOS statistic-table lookup helper.

This sandbox's outbound network can't reach ecos.bok.or.kr at all, so
verifying a stat_code/item_code from here isn't possible. This script is
meant to run somewhere that *does* have network access (a developer's own
machine, or the `ECOS Table Lookup` GitHub Actions workflow) using the
already-registered ECOS_API_KEY, and prints every statistic table whose
name contains a keyword — e.g. "경제성장률" — so the right STAT_CODE can be
read off directly instead of guessed.

Usage:
    ECOS_API_KEY=... python -m scripts.ecos_lookup 경제성장률
    ECOS_API_KEY=... python -m scripts.ecos_lookup --items 902Y015 한국
"""
from __future__ import annotations

import os
import sys

import requests

ECOS_BASE_URL = "https://ecos.bok.or.kr/api"


def list_statistic_tables(api_key: str, start: int = 1, end: int = 3000) -> list[dict]:
    url = f"{ECOS_BASE_URL}/StatisticTableList/{api_key}/json/kr/{start}/{end}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if "StatisticTableList" not in payload:
        raise RuntimeError(payload.get("RESULT", {}).get("MESSAGE", "ECOS error response"))
    return payload["StatisticTableList"].get("row", [])


def list_statistic_items(api_key: str, stat_code: str, start: int = 1, end: int = 1000) -> list[dict]:
    url = f"{ECOS_BASE_URL}/StatisticItemList/{api_key}/json/kr/{start}/{end}/{stat_code}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if "StatisticItemList" not in payload:
        raise RuntimeError(payload.get("RESULT", {}).get("MESSAGE", "ECOS error response"))
    return payload["StatisticItemList"].get("row", [])


def main() -> None:
    api_key = os.environ.get("ECOS_API_KEY")
    if not api_key:
        print("ECOS_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "--items":
        stat_code = sys.argv[2]
        keyword = sys.argv[3] if len(sys.argv) > 3 else ""
        rows = list_statistic_items(api_key, stat_code)
        matches = [r for r in rows if keyword in r.get("ITEM_NAME", "")] if keyword else rows
        print(f"{len(matches)} item match(es) for stat_code={stat_code} keyword='{keyword}' "
              f"out of {len(rows)} total items\n")
        for r in matches:
            print(f"ITEM_CODE={r.get('ITEM_CODE')}  ITEM_NAME={r.get('ITEM_NAME')}  "
                  f"CYCLE={r.get('CYCLE')}  START_TIME={r.get('START_TIME')}  END_TIME={r.get('END_TIME')}")
        return

    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    rows = list_statistic_tables(api_key)
    matches = [r for r in rows if keyword in r.get("STAT_NAME", "")]

    print(f"{len(matches)} match(es) for '{keyword}' out of {len(rows)} total tables\n")
    for r in matches:
        print(f"STAT_CODE={r.get('STAT_CODE')}  STAT_NAME={r.get('STAT_NAME')}  CYCLE={r.get('CYCLE')}  "
              f"SRCH_YN={r.get('SRCH_YN')}  P_STAT_CODE={r.get('P_STAT_CODE')}")


if __name__ == "__main__":
    main()
