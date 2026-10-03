"""One-off: directly query 청약Home for ALL 국민주택(공공분양) listings
ANNOUNCED (RCRIT_PBLANC_DE) in the last 45 days nationwide — not filtered by
"currently open" (RCEPT_ENDDE>=today) like fetch_and_render.py's live
pipeline. This answers the user's skepticism ("한달동안 한건도?!?") directly
against the raw API, independent of our own alerted_state.json history."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))
BASE_URL = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail"


def fetch_page(service_key, page, per_page=200, extra=None):
    params = {"page": page, "perPage": per_page}
    if extra:
        params.update(extra)
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Infuser {service_key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_all(service_key, extra=None):
    rows = []
    page = 1
    while True:
        data = fetch_page(service_key, page, extra=extra)
        rows.extend(data.get("data", []))
        match_count = data.get("matchCount", 0)
        per_page = data.get("perPage", 200)
        if page * per_page >= match_count or page > 20:
            break
        page += 1
    return rows


def main():
    key = os.environ["DATA_GO_KR_KEY"]
    now_kst = datetime.now(KST)
    cutoff = (now_kst - timedelta(days=45)).strftime("%Y-%m-%d")
    today = now_kst.strftime("%Y-%m-%d")

    print(f"=== 국민주택(국민) 전국 — 공고일(RCRIT_PBLANC_DE) {cutoff} 이후 전부 (오늘: {today}) ===")
    rows = fetch_all(key, extra={"cond[HOUSE_DTL_SECD_NM::EQ]": "국민", "cond[RCRIT_PBLANC_DE::GTE]": cutoff})
    print(f"전국 국민주택 공고 건수 (최근 45일 공고일 기준): {len(rows)}\n")
    for r in sorted(rows, key=lambda r: r.get("RCRIT_PBLANC_DE") or ""):
        print(f"  {r.get('RCRIT_PBLANC_DE')} | {r.get('HOUSE_NM')} | {r.get('SUBSCRPT_AREA_CODE_NM')} | "
              f"{r.get('HSSPLY_ADRES')} | 접수 {r.get('RCEPT_BGNDE')}~{r.get('RCEPT_ENDDE')}")

    print("\n=== 전국 전체 HOUSE_DTL_SECD_NM(주택구분) 분포 — 최근 45일 공고일 기준, 필터 없이 ===")
    all_rows = fetch_all(key, extra={"cond[RCRIT_PBLANC_DE::GTE]": cutoff})
    print(f"전국 전체(모든 구분) 공고 건수: {len(all_rows)}")
    dist = {}
    for r in all_rows:
        k = r.get("HOUSE_DTL_SECD_NM") or "(없음)"
        dist[k] = dist.get(k, 0) + 1
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}건")

    print("\n=== 서울/경기 지역 전체(주택구분 무관) — 최근 45일 공고일 기준 ===")
    sg = [r for r in all_rows if r.get("SUBSCRPT_AREA_CODE_NM") in {"서울", "경기"}]
    print(f"서울/경기 전체: {len(sg)}건")
    for r in sorted(sg, key=lambda r: r.get("RCRIT_PBLANC_DE") or ""):
        print(f"  {r.get('RCRIT_PBLANC_DE')} | {r.get('HOUSE_NM')} | {r.get('SUBSCRPT_AREA_CODE_NM')} | "
              f"구분={r.get('HOUSE_DTL_SECD_NM')} | {r.get('HSSPLY_ADRES')}")


if __name__ == "__main__":
    main()
