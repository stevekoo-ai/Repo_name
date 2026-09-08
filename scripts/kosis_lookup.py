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

2026-09-07 확장: 위 설명("KOSIS는 외부에서 닿는 키워드 검색 API가 없다")은
틀렸다. KOSIS OpenAPI에는 통합검색(statisticsSearch.do)이 있고 GitHub Actions
러너에서 정상 응답한다 — 그래서 이제 후보를 손으로 추측할 필요가 없다.
--search 모드로 키워드를 던지면 실제 (ORG_ID, TBL_ID, TBL_NM)을 받아온다.
기존 후보 검증 모드는 그대로 두되(찾은 표가 맞는지 ITM_ID/C1까지 확인해야
하므로 둘 다 필요), 새 표를 찾을 때는 --search를 먼저 쓸 것.

Usage:
    KOSIS_API_KEY=... python -m scripts.kosis_lookup                 # 후보 검증
    KOSIS_API_KEY=... python -m scripts.kosis_lookup cpi_index       # 한 지표만
    KOSIS_API_KEY=... python -m scripts.kosis_lookup --search 소비자물가지수
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime

import requests

from collectors.base import raise_for_status, redact_url

KOSIS_BASE_URL = "https://kosis.kr/openapi"

# A few plausible (orgId, tblId) candidates per indicator, gathered from
# public references (KOSIS itself has no reachable-from-here keyword search).
# 2026-09-08: kosis.kr이 이 샌드박스에서 완전히 차단돼(EGRESS_BLOCKED) 로컬
# WebFetch로 devGuide/통계표 페이지를 열어볼 수 없다 — GitHub Actions에서
# 실제로 찔러보는 것만이 검증 수단이다. 아래 후보는 WebSearch로 찾은,
# 실제 KOSIS 웹 화면(statHtml.do) URL에 등장하는 tblId들 — 웹 화면에 존재한다고
# OpenAPI에서도 항상 되는 건 아니므로(예: DT_1DA7004S는 웹엔 있는데 예전 실측에서
# "잘못된 요청 변수" 오류) 여러 후보를 순서대로 실측 검증한다.
CANDIDATES: dict[str, list[tuple[str, str]]] = {
    "cpi_index": [("101", "DT_1J22003"), ("101", "DT_1J17009")],
    "industrial_production_index": [("101", "DT_1JH20151"), ("101", "DT_1F01012")],
    "retail_sales_index": [("101", "DT_1K41002"), ("101", "DT_1K31009")],
    "unemployment_rate": [("101", "DT_1DA7004S"), ("101", "DT_1DA7012S")],
    # k_employed_yoy: 취업자수(전년동월비) — CCI K-Sahm Rule 축. 경제활동인구조사
    # 계열의 취업자수 원표(DT_1DA7012S)에서 전년동월비 항목(ITM_ID)을 찾거나,
    # 못 찾으면 실업률 표(DT_1DA7004S)에 취업자수 항목이 같이 들어있을 수 있어
    # 함께 시도한다.
    "k_employed_yoy": [("101", "DT_1DA7012S"), ("101", "DT_1DA7004S")],
    # 반도체 출하/재고 — 광공업생산지수(2020=100, 산업별) 표 안에 "반도체" 세세분류
    # 항목이 C1(objL1)로 들어있는 구조로 추정. DT_1F01012가 그 원표일 가능성이 커
    # 우선 시도, 안 되면 예전 추정치(DT_1E66010)도 함께.
    "semiconductor_shipment_index": [("101", "DT_1F01012"), ("101", "DT_1E66010")],
    "semiconductor_inventory_index": [("101", "DT_1F01012"), ("101", "DT_1E66010")],
}


# 2026-09-08: 표마다 분류축(classification dimension) 개수가 다르다 — 어떤
# 표는 itmId 하나뿐이고(objL1 없음), 어떤 표는 objL1까지, 어떤 표는 objL2까지
# 쓴다. 실측(2026-07-14)에서 unemployment_rate 후보가 "잘못된 요청 변수를
# 호출 하였습니다"로 실패했던 게 tblId 자체가 틀려서가 아니라 이 표가 objL2를
# 안 쓰는데 objL2=ALL을 보내서였을 가능성이 있다 — objL1까지만 보내는 조합도
# 시도해서 tblId 자체는 유효한데 파라미터 모양만 틀렸던 경우를 구제한다.
_PARAM_SHAPES: tuple[dict, ...] = (
    {"itmId": "ALL", "objL1": "ALL", "objL2": "ALL"},
    {"itmId": "ALL", "objL1": "ALL"},
    {"itmId": "ALL"},
)


def _try_candidate(api_key: str, org_id: str, tbl_id: str, start: str, end: str, prd_se: str) -> dict:
    url = f"{KOSIS_BASE_URL}/Param/statisticsParameterData.do"
    last_error = last_err_code = None
    for shape in _PARAM_SHAPES:
        params = {
            "method": "getList", "apiKey": api_key, "format": "json", "jsonVD": "Y",
            "prdSe": prd_se, "startPrdDe": start, "endPrdDe": end,
            "orgId": org_id, "tblId": tbl_id, **shape,
        }
        try:
            resp = requests.get(url, params=params, timeout=15)
            raise_for_status(resp)
            payload = resp.json()
        except Exception as exc:  # network/JSON errors reported as-is, not raised
            return {"ok": False, "error": str(exc)}
        if isinstance(payload, dict) and payload.get("err"):
            last_error = payload.get("errMsg", "unknown error")
            last_err_code = payload.get("err")
            # "해당 통계표가 존재하지 않습니다"는 tblId 자체가 없다는 뜻이라 파라미터
            # 모양을 바꿔봐야 소용없다 — 그런 경우만 다음 후보로 바로 넘어간다.
            if "존재하지 않습니다" in str(last_error):
                break
            continue   # 그 외 오류(파라미터 모양 등)는 다음 shape로 재시도
        if isinstance(payload, list) and payload:
            return {"ok": True, "rows": payload, "param_shape": shape}
        last_error, last_err_code = "empty response", None
    return {"ok": False, "error": last_error or "unknown error", "err_code": last_err_code}


def search_tables(api_key: str, keyword: str, limit: int = 15) -> list[dict]:
    """KOSIS 통합검색(statisticsSearch.do) — 키워드로 실제 통계표를 찾는다.

    이 저장소의 KOSIS 통계표 ID 4개가 전부 틀렸던 이유가 "검색 API가 없으니
    공개 자료를 보고 추측한다"였는데, 그 전제가 틀렸다. 이 엔드포인트가
    ORG_ID/TBL_ID/TBL_NM을 직접 돌려주므로 추측할 이유가 없다.
    """
    url = f"{KOSIS_BASE_URL}/statisticsSearch.do"
    params = {
        "method": "getList", "apiKey": api_key, "format": "json", "jsonVD": "Y",
        "searchNm": keyword, "startCount": 1, "resultCount": limit,
    }
    resp = requests.get(url, params=params, timeout=20)
    raise_for_status(resp)
    payload = resp.json()
    if isinstance(payload, dict) and payload.get("err"):
        raise RuntimeError(f"KOSIS 검색 오류 {payload.get('err')}: {payload.get('errMsg')}")
    return payload if isinstance(payload, list) else []


def _run_search(api_key: str, keyword: str) -> None:
    print(f"=== KOSIS 통합검색: {keyword!r} ===", flush=True)
    # kosis.kr은 GitHub Actions 러너에서 간헐적으로 TCP connect 자체가 타임아웃
    # 난다(2026-09-07 실측: 데이터 엔드포인트는 응답하는데 같은 호스트의 검색
    # 엔드포인트가 connect timeout=20으로 죽음). 한 번 실패로 포기하면 "검색
    # API가 없다"는 예전의 잘못된 결론으로 되돌아가게 되므로 몇 번 재시도한다.
    rows = None
    last_error = None
    for attempt in range(1, 4):
        try:
            rows = search_tables(api_key, keyword)
            break
        except Exception as exc:
            last_error = exc
            # ⚠️ 반드시 redact_url을 먼저 통과시킨 뒤 자를 것. requests의
            # ConnectTimeout 메시지에는 요청 URL 전체(= ?apiKey=...)가 박혀 있고,
            # 그냥 자르면 키가 **중간에서 잘린 채** 찍힌다. GitHub Actions의
            # 시크릿 마스킹은 값 전체가 일치할 때만 ***로 가리므로, 잘린
            # 조각은 마스킹을 그대로 통과해 로그에 남는다. 2026-09-07 이
            # 함수의 첫 버전이 정확히 그렇게 KOSIS 키 앞부분을 노출시켰다.
            safe = redact_url(str(exc))
            print(f"  [시도 {attempt}/3 실패] {type(exc).__name__}: {safe[:200]}", flush=True)
            if attempt < 3:
                time.sleep(10 * attempt)
    if rows is None:
        print(f"  3회 모두 실패 — kosis.kr 연결 문제로 보인다"
              f"(마지막 오류: {redact_url(str(last_error))})")
        print("  이건 통계표가 없다는 뜻이 아니다. 잠시 후 다시 시도할 것.")
        return
    if not rows:
        print("  검색 결과 없음")
        return
    for r in rows:
        # 표 이름/주기/수록기간까지 같이 찍어야 어느 표를 골라야 할지 판단이 된다.
        print(f"  ORG_ID={r.get('ORG_ID')} TBL_ID={r.get('TBL_ID')}")
        print(f"    표명: {r.get('TBL_NM')}")
        print(f"    기관: {r.get('ORG_NM')} / 주기: {r.get('PRD_SE')} / "
              f"수록: {r.get('PRD_DE_START')}~{r.get('PRD_DE_END')}")
    print(f"\n  → 쓸 표를 고른 뒤 `python -m scripts.kosis_lookup` 후보 목록에 추가해서 "
          f"ITM_ID/C1(objL1)까지 확인할 것.")


def main() -> None:
    api_key = os.environ.get("KOSIS_API_KEY")
    if not api_key:
        print("KOSIS_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    today = datetime.utcnow()
    end_m = today.strftime("%Y%m")
    start_m = today.replace(year=today.year - 1).strftime("%Y%m")

    args = sys.argv[1:]
    if args and args[0] == "--search":
        if len(args) < 2:
            print("사용법: python -m scripts.kosis_lookup --search <키워드>", file=sys.stderr)
            sys.exit(1)
        _run_search(api_key, " ".join(args[1:]))
        return

    only = args[0] if args else None
    series_keys = [only] if only else list(CANDIDATES)

    first = True
    for key in series_keys:
        print(f"\n=== {key} ===", flush=True)
        for org_id, tbl_id in CANDIDATES[key]:
            # KOSIS appears to rate/burst-limit at the connection level (seen as a
            # sudden run of TCP connect timeouts to every subsequent call once
            # tripped) — space calls out and retry once after a longer pause
            # rather than firing candidates back-to-back.
            if not first:
                time.sleep(5)
            first = False
            print(f"-- orgId={org_id} tblId={tbl_id} (prdSe=M, {start_m}-{end_m})", flush=True)
            result = _try_candidate(api_key, org_id, tbl_id, start_m, end_m, "M")
            if not result["ok"] and "timed out" in result["error"]:
                print(f"   FAILED (timeout, retrying once after 15s): {result['error']}", flush=True)
                time.sleep(15)
                result = _try_candidate(api_key, org_id, tbl_id, start_m, end_m, "M")
            if not result["ok"]:
                print(f"   FAILED: {result['error']}", flush=True)
                continue
            rows = result["rows"]
            seen: set[tuple[str, str]] = set()
            print(f"   OK (param_shape={result.get('param_shape')}) — {len(rows)} rows returned. "
                  f"Distinct ITM_ID/C1 combos:", flush=True)
            for r in rows:
                combo = (r.get("ITM_ID"), r.get("C1"))
                if combo in seen:
                    continue
                seen.add(combo)
                print(f"     ITM_ID={r.get('ITM_ID')} ITM_NM={r.get('ITM_NM')} "
                      f"C1={r.get('C1')} C1_NM={r.get('C1_NM')} "
                      f"(sample: PRD_DE={r.get('PRD_DE')} DT={r.get('DT')})", flush=True)


if __name__ == "__main__":
    main()
