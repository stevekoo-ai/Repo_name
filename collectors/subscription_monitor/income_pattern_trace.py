"""
One-off (workflow_dispatch-only) exploratory trace: run income_analysis.py's
소득요건 classification against EVERY currently-open 서울/경기 국민주택 일반공급
listing (not just NEW_MATCH keyword hits like the live alert pipeline), to
empirically verify whether the pattern documented in
wiki/concepts/public-housing-income-requirement-framework.md
(사업유형: 신혼희망타운=전체검증 vs 국민주택=60㎡이하만검증, 배율표 전국공통)
actually holds across the live population, not just the 3 reference PDFs.

Not part of the 30-min live pipeline — deliberately manual (workflow_dispatch)
because it downloads+parses a PDF per listing, which is heavier than the
alert pipeline's "only NEW_MATCH" policy and is meant for periodic pattern
re-validation, not continuous operation. Run again whenever the framework
page needs re-checking against a fresh batch of listings.

Output goes to stdout (captured in the GitHub Actions job log) — this is an
investigative trace, not something that needs its own persisted state file.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from fetch_and_render import fetch_all, TARGET_REGIONS  # noqa: E402
import income_analysis  # noqa: E402

KST = timezone(timedelta(hours=9))
PER_LISTING_DELAY_SEC = 1.5  # be polite to 청약Home / LH / GH servers — sequential, not parallel

# SCOPE=national broadens beyond 서울/경기 to every open 국민주택 nationwide —
# useful when the 서울/경기 pool is exhausted (already traced) and more PDF
# samples are wanted to keep validating the framework. Non-LH listings
# (GH/SH/기타 지방공사) will fail at the discover stage since
# search_and_download_lh_pdf() only supports LH청약플러스 — that failure mode
# itself is useful signal for whether LH-only support needs expanding.
SCOPE = os.environ.get("SCOPE", "seoul_gyeonggi")


def main() -> None:
    service_key = os.environ["DATA_GO_KR_KEY"]
    now_kst = datetime.now(KST)
    today = now_kst.strftime("%Y-%m-%d")

    all_rows = fetch_all(service_key, today)
    if SCOPE == "national":
        rows = all_rows
        scope_label = "전국"
    else:
        rows = [r for r in all_rows if r.get("SUBSCRPT_AREA_CODE_NM") in TARGET_REGIONS]
        scope_label = "서울/경기"

    print(f"=== {scope_label} 국민주택 소득요건 패턴 트레이스 ({now_kst.strftime('%Y-%m-%d %H:%M KST')}) ===")
    print(f"전국 국민주택(접수마감 전) {len(all_rows)}건 중 {scope_label} {len(rows)}건 대상\n")

    results = []
    for i, r in enumerate(rows, 1):
        name = r.get("HOUSE_NM") or "(이름없음)"
        region = r.get("SUBSCRPT_AREA_CODE_NM") or "-"
        print(f"[{i}/{len(rows)}] {name} ({region}) ... ", end="", flush=True)
        try:
            analysis = income_analysis.analyze_listing(r)
        except Exception as e:
            analysis = {"status": "failed", "stage": "unexpected", "reason": str(e)}
        analysis["_name"] = name
        analysis["_region"] = region
        analysis["_pblanc_url"] = r.get("PBLANC_URL")
        results.append(analysis)

        if analysis["status"] == "ok":
            tag = "⚠️예외" if analysis.get("exceptions") else "✅일치"
            print(f"{tag} {analysis['business_type']}/{analysis['income_scope']}")
        else:
            print(f"❌실패({analysis.get('stage')}): {analysis.get('reason')}")

        if i < len(rows):
            time.sleep(PER_LISTING_DELAY_SEC)

    # --- Aggregate summary ---
    ok = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] != "ok"]
    with_exceptions = [r for r in ok if r.get("exceptions")]

    print("\n=== 집계 ===")
    print(f"분석 성공: {len(ok)}/{len(results)}  (실패: {len(failed)})")

    by_business_type: dict[str, int] = {}
    by_income_scope: dict[str, int] = {}
    for r in ok:
        by_business_type[r["business_type"]] = by_business_type.get(r["business_type"], 0) + 1
        by_income_scope[r["income_scope"]] = by_income_scope.get(r["income_scope"], 0) + 1
    print(f"사업유형 분포: {by_business_type}")
    print(f"소득검증범위 분포: {by_income_scope}")

    if failed:
        print(f"\n=== 분석 실패 {len(failed)}건 (자동 다운로드/파싱 불가 — 수동 확인 필요) ===")
        for r in failed:
            print(f"  - {r['_name']} ({r['_region']}): [{r.get('stage')}] {r.get('reason')}")
            print(f"    청약홈: {r.get('_pblanc_url')}")

    if with_exceptions:
        print(f"\n=== ⚠️ 프레임워크 규칙과 다른 예외 {len(with_exceptions)}건 (원문 확인 후 wiki에 기록 권장) ===")
        for r in with_exceptions:
            print(f"  - {r['_name']} ({r['_region']}) — {r['business_type']}/{r['income_scope']}")
            for exc in r["exceptions"]:
                print(f"      · {exc}")
            print(f"    공고문: {r.get('pdf_url')}")
    else:
        print("\n=== 예외 없음 — 이번 배치는 프레임워크 규칙과 전부 일치 ===")

    print("\n=== 전체 결과 (JSON, 다음 세션에서 파싱해 wiki에 반영하기 위함) ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
