"""One-off re-verification (2026-10-14, 사용자 "소득요건 자동검증 진행에
대해서 재조사해봐"): wider 90-day nationwide check + full HOUSE_DTL_SECD_NM
distribution (to catch a 공공분양 subtype our "국민" EQ filter might miss,
e.g. 뉴홈) + cross-check against our own tracked state (alerted_state.json's
10 ids, income_review_state.json's 3 reviewed) to find any discrepancy."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))
BASE_URL = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail"

TRACKED_IDS = {
    "2026000313", "2026000320", "2026820006", "2026820008", "2026000409",
    "2026000416", "2026820009", "2026000438", "2026000437", "2026820011",
}
REVIEWED_IDS = {"2026000438", "2026000437", "2026820011"}


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
        if page * per_page >= match_count or page > 30:
            break
        page += 1
    return rows


def main():
    key = os.environ["DATA_GO_KR_KEY"]
    now_kst = datetime.now(KST)
    cutoff = (now_kst - timedelta(days=90)).strftime("%Y-%m-%d")
    today = now_kst.strftime("%Y-%m-%d")

    print(f"=== 전국 전체(필터없음) — 공고일 {cutoff} 이후, 오늘 {today} ===")
    all_rows = fetch_all(key, extra={"cond[RCRIT_PBLANC_DE::GTE]": cutoff})
    print(f"전국 전체 건수: {len(all_rows)}")
    dist = {}
    for r in all_rows:
        k = r.get("HOUSE_DTL_SECD_NM") or "(없음)"
        dist[k] = dist.get(k, 0) + 1
    print("HOUSE_DTL_SECD_NM 분포:")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v}건")

    print(f"\n=== 국민주택('국민') 전국 — 90일 ===")
    gukmin_rows = [r for r in all_rows if r.get("HOUSE_DTL_SECD_NM") == "국민"]
    print(f"건수: {len(gukmin_rows)}")

    print(f"\n=== 국민주택 서울/경기 — 90일 ===")
    sg_rows = [r for r in gukmin_rows if r.get("SUBSCRPT_AREA_CODE_NM") in {"서울", "경기"}]
    print(f"건수: {len(sg_rows)}")
    found_ids = set()
    for r in sorted(sg_rows, key=lambda r: r.get("RCRIT_PBLANC_DE") or ""):
        hid = r.get("HOUSE_MANAGE_NO") or r.get("PBLANC_NO") or ""
        found_ids.add(hid)
        tag = "🟢추적중" if hid in TRACKED_IDS else "🆕미추적!"
        rtag = "✅검토완료" if hid in REVIEWED_IDS else ""
        print(f"  [{tag}]{rtag} id={hid} {r.get('RCRIT_PBLANC_DE')} | {r.get('HOUSE_NM')} | "
              f"접수 {r.get('RCEPT_BGNDE')}~{r.get('RCEPT_ENDDE')}")

    print("\n=== 교차검증 결과 ===")
    missing_from_api = TRACKED_IDS - found_ids
    new_untracked = found_ids - TRACKED_IDS
    print(f"alerted_state.json에 있지만 이번 90일 API 조회엔 없는 id (더 오래됐거나 폐기): {missing_from_api or '없음'}")
    print(f"API엔 있지만 alerted_state.json엔 없는 id (추적 누락 가능성!): {new_untracked or '없음'}")

    # 뉴홈 등 다른 공공분양 신호가 있는지 확인 — HOUSE_NM에 "뉴홈"/"나눔형"/"선택형"/"일반형" 포함된 non-국민 건
    print("\n=== '뉴홈' 계열 명칭이 있는데 HOUSE_DTL_SECD_NM이 '국민'이 아닌 건 (필터 누락 의심) ===")
    newhome_markers = ["뉴홈", "나눔형", "선택형"]
    suspects = [r for r in all_rows if r.get("HOUSE_DTL_SECD_NM") != "국민"
                and any(m in (r.get("HOUSE_NM") or "") for m in newhome_markers)]
    print(f"건수: {len(suspects)}")
    for r in suspects[:20]:
        print(f"  {r.get('RCRIT_PBLANC_DE')} | {r.get('HOUSE_NM')} | 구분={r.get('HOUSE_DTL_SECD_NM')} | {r.get('SUBSCRPT_AREA_CODE_NM')}")


if __name__ == "__main__":
    main()
