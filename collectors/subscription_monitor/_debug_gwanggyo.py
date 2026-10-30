"""
일회성 디버그 스크립트 (throwaway branch 전용, main에 병합 안 함).

2026-10-30 광교 자연앤 센트레빌(A17BL, HOUSE_MANAGE_NO=2026000528) 공고를
자동감시(alerted_state.json)가 왜 못 잡았는지 근본원인 확인용.
fetch_and_render.py의 fetch_all()은 cond[HOUSE_DTL_SECD_NM::EQ]="국민" 필터를
쓰는데, 이 공고가 "민간참여 공공주택사업"이라 HOUSE_DTL_SECD_NM이 "민영"으로
분류돼 있다면 그게 근본원인(폴링 주기 문제가 아니라 필터 자체 배제) —
이 가설을 라이브 API로 직접 확인한다.
"""

import json
import os
import urllib.parse
import urllib.request

BASE_URL = "https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/getAPTLttotPblancDetail"


def fetch(params: dict, service_key: str) -> dict:
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Infuser {service_key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def main():
    key = os.environ["DATA_GO_KR_KEY"]

    print("=== 1. HOUSE_MANAGE_NO=2026000528 직접 조회 (필터 없음) ===")
    data = fetch({"page": 1, "perPage": 10, "cond[HOUSE_MANAGE_NO::EQ]": "2026000528"}, key)
    rows = data.get("data", [])
    print(f"matchCount={data.get('matchCount')}, rows={len(rows)}")
    for r in rows:
        print(json.dumps({
            "HOUSE_MANAGE_NO": r.get("HOUSE_MANAGE_NO"),
            "HOUSE_NM": r.get("HOUSE_NM"),
            "HOUSE_DTL_SECD_NM": r.get("HOUSE_DTL_SECD_NM"),
            "HOUSE_SECD_NM": r.get("HOUSE_SECD_NM"),
            "RCRIT_PBLANC_DE": r.get("RCRIT_PBLANC_DE"),
            "RCEPT_BGNDE": r.get("RCEPT_BGNDE"),
            "RCEPT_ENDDE": r.get("RCEPT_ENDDE"),
            "HSSPLY_ADRES": r.get("HSSPLY_ADRES"),
            "SUBSCRPT_AREA_CODE_NM": r.get("SUBSCRPT_AREA_CODE_NM"),
        }, ensure_ascii=False, indent=2))

    print("\n=== 2. HOUSE_NM에 '광교' 또는 '센트레빌' 포함 검색 (필터 없음, 오늘 공고일 기준) ===")
    for kw in ["광교", "센트레빌"]:
        data = fetch({"page": 1, "perPage": 20, "cond[HOUSE_NM::LIKE]": kw,
                       "cond[RCRIT_PBLANC_DE::GTE]": "20261025"}, key)
        rows = data.get("data", [])
        print(f"keyword={kw}: matchCount={data.get('matchCount')}, rows={len(rows)}")
        for r in rows:
            print(f"  - {r.get('HOUSE_MANAGE_NO')} | {r.get('HOUSE_NM')} | "
                  f"HOUSE_DTL_SECD_NM={r.get('HOUSE_DTL_SECD_NM')} | "
                  f"RCRIT_PBLANC_DE={r.get('RCRIT_PBLANC_DE')} | "
                  f"ADRES={r.get('HSSPLY_ADRES')}")

    print("\n=== 3. 기존 fetch_all() 필터(국민, RCEPT_ENDDE>=오늘)로 이 건이 잡히는지 ===")
    import datetime
    today = datetime.datetime.now().strftime("%Y%m%d")
    data = fetch({"page": 1, "perPage": 200, "cond[HOUSE_DTL_SECD_NM::EQ]": "국민",
                   "cond[RCEPT_ENDDE::GTE]": today}, key)
    rows = data.get("data", [])
    found = [r for r in rows if r.get("HOUSE_MANAGE_NO") == "2026000528"]
    print(f"국민 필터 결과 {len(rows)}건 중 2026000528 포함 여부: {bool(found)}")


if __name__ == "__main__":
    main()
