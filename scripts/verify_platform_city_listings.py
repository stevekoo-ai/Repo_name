#!/usr/bin/env python3
"""Smart verification of Yongin Platform City subscription listings.

This script queries the 청약Home API (via data.go.kr) to check for current
and historical "플랫폼시티" listings, including their housing types
(국민주택 vs 민영) to understand the notification scope needed.

Run: python3 scripts/verify_platform_city_listings.py <DATA_GO_KR_KEY>

📚 Lesson Learned Reference:
   See docs/LESSON_LEARNED_API_DEBUGGING.md for:
   - CJK character encoding (한글 URL encoding)
   - API authentication (Authorization header format)
   - 3-tier validation query strategy
   - Type mismatch handling
   - Error diagnosis patterns
"""
from __future__ import annotations

import json
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def query_applyhome(
    service_key: str,
    keyword: str,
    search_field: str = "HOUSE_NM",
    page: int = 1,
    per_page: int = 100,
) -> dict:
    """Query the 청약Home API via data.go.kr."""
    params = {
        "serviceKey": service_key,
        "pageNo": page,
        "numOfRows": per_page,
        f"cond[{search_field}::LIKE]": keyword,
    }
    url = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail?" + urlencode(params)

    try:
        req = Request(url, headers={"Authorization": f"Infuser {service_key}"})
        with urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "data": []}


def categorize_housing_type(row: dict) -> str:
    """Infer housing type from the API response row."""
    house_type_code = row.get("HOUSE_DTL_SECD_NM", "").upper()
    if any(x in house_type_code for x in ["국민", "공공", "임대"]):
        return "국민주택 (Public)"
    elif any(x in house_type_code for x in ["민영", "Private", "분양"]):
        return "민영 (Private)"
    else:
        return f"Unknown ({house_type_code})"


def analyze_listings(results: dict) -> None:
    """Analyze and display listing results."""
    data = results.get("data", [])
    total = results.get("totalCount", 0)

    if results.get("error"):
        print(f"❌ Error: {results['error']}")
        return

    print(f"📊 Total matches: {total} (displayed: {len(data)})")
    print()

    if not data:
        print("No listings found.")
        return

    housing_types = {}
    for row in data:
        house_name = row.get("HOUSE_NM", "N/A")
        house_type = categorize_housing_type(row)
        supply_addr = row.get("HSSPLY_ADRES", "N/A")
        announce_date = row.get("RCRIT_PBLANC_DE", "N/A")

        if house_type not in housing_types:
            housing_types[house_type] = []
        housing_types[house_type].append({
            "name": house_name,
            "address": supply_addr,
            "date": announce_date,
            "raw_type": row.get("HOUSE_DTL_SECD_NM", "N/A"),
        })

        print(f"  🏢 {house_name}")
        print(f"     Type: {house_type}")
        print(f"     Address: {supply_addr}")
        print(f"     Announce: {announce_date}")
        print()

    print("📈 Summary by Housing Type:")
    for htype, listings in housing_types.items():
        print(f"  • {htype}: {len(listings)} listings")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_platform_city_listings.py <DATA_GO_KR_KEY>")
        print()
        print("This verifies Yongin Platform City listings on 청약Home by checking:")
        print("  1. Direct search for '플랫폼시티' in house name")
        print("  2. Search for '용인' (Yongin) by address")
        print("  3. Search for '기흥구' (Giheung district) where Platform City is located")
        print()
        print("Sets the DATA_GO_KR_KEY env var and re-run to execute queries.")
        sys.exit(1)

    service_key = sys.argv[1]

    print("=" * 70)
    print("🔍 YONGIN PLATFORM CITY SUBSCRIPTION LISTING VERIFICATION")
    print("=" * 70)
    print()

    print("1️⃣ Search: 플랫폼시티 (exact house name match)")
    print("-" * 70)
    results_1 = query_applyhome(service_key, "플랫폼시티", search_field="HOUSE_NM")
    analyze_listings(results_1)

    print("\n2️⃣ Search: 용인 (Yongin city address match)")
    print("-" * 70)
    results_2 = query_applyhome(service_key, "용인", search_field="HSSPLY_ADRES")
    analyze_listings(results_2)

    print("\n3️⃣ Search: 기흥구 (Giheung district - Platform City's actual location)")
    print("-" * 70)
    results_3 = query_applyhome(service_key, "기흥구", search_field="HSSPLY_ADRES")
    analyze_listings(results_3)

    print("\n" + "=" * 70)
    print("📋 FINDINGS & RECOMMENDATIONS")
    print("=" * 70)

    all_data = (results_1.get("data", []) +
                results_2.get("data", []) +
                results_3.get("data", []))
    unique_listings = {}
    for row in all_data:
        key = row.get("HOUSE_NM", "")
        if key and key not in unique_listings:
            unique_listings[key] = row

    housing_type_dist = {}
    for row in unique_listings.values():
        htype = categorize_housing_type(row)
        housing_type_dist[htype] = housing_type_dist.get(htype, 0) + 1

    print()
    print("🏗️ Housing Type Distribution (historical + current):")
    for htype, count in housing_type_dist.items():
        print(f"   • {htype}: {count} listings")

    print()
    print("💡 NOTIFICATION SYSTEM SCOPE:")
    if any("민영" in k for k in housing_type_dist.keys()):
        print("   ⚠️  Yongin Platform City historical data shows PRIVATE (민영) housing.")
        print("   ❌ Current system: Tracks 국민주택 (public housing) ONLY")
        print("   ✅ RECOMMENDATION: Expand scope to include BOTH 국민주택 & 민영 types")
        print("      to catch the actual Platform City announcement when released.")
    else:
        print("   ✓ All Platform City projects found: 국민주택 (public housing)")
        print("   ✓ Current system scope is appropriate.")


if __name__ == "__main__":
    main()
