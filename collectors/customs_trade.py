"""관세청 수출입총괄(GW) collector — 월별 총수출/총수입 실측(달러).

2026-08-17: 사용자 요청("수출입동향과 코스피지수 관계를 가장 길고 오래된
데이터로")에 대한 진짜 해결책. data/manual_inputs/exports.yaml(월 1회 수동,
2026-04부터만 존재)의 한계를 넘어서려고 만들었다 — 이 API는 1990.01부터
실측 데이터가 확인됐다(config/api.yaml의 customs_trade note 참고. 그 이전은
미확인이지 존재하지 않는다는 뜻은 아님).

base_url은 WebSearch로 5+10개 후보를 추측했지만 전부 틀렸다
(NO_OPENAPI_SERVICE_ERROR) — 사용자가 data.go.kr Swagger 문서를 직접 열어
정확한 주소를 알려준 뒤에야 확인됐다(apis.data.go.kr/1220000/Newtrade/
getNewtradeList). 실측으로 확인된 제약: strtYymm~endYymm이 1년(12개월)을
넘으면 resultCode=99("조회기간은 1년이내만 가능")로 거부된다 — 그래서 이
모듈은 연도 단위로 나눠 호출한다.

응답은 XML(JSON 미지원, type 파라미터 없음). 필드: year(YYYY.MM 문자열),
expDlr/impDlr(달러, 정수 문자열), expCnt/impCnt(건수), balPayments(무역수지).
반도체 등 품목별 세부는 이 API에 없다(별도 상품 "품목별 국가별 수출입실적
(nitemtrade)" — 이번 세션엔 활용신청 안 돼 있어 미구현, 필요해지면 이 파일과
같은 패턴으로 추가).
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests

from core.config import api_config, get_api_key
from core.logger import log_event
from . import base

# 관세청이 실제로 강제하는 제약(실측 확인, 추측 아님) — 1년 초과 조회는 resultCode 99.
_MAX_MONTHS_PER_CALL = 12
_EARLIEST_CONFIRMED_YYYYMM = "199001"  # 이보다 이전은 시도 안 해봄 — 없다는 뜻 아님


def _fetch_year_window(strt_yymm: str, end_yymm: str, api_key: str, timeout: int = 20) -> list[dict]:
    """단일 API 호출 — 최대 1년(12개월) 창. XML 파싱 후 dict 리스트로 반환."""
    base_url = api_config()["sources"]["customs_trade"]["base_url"]
    resp = requests.get(
        base_url,
        params={
            "serviceKey": api_key, "strtYymm": strt_yymm, "endYymm": end_yymm,
            "numOfRows": 20, "pageNo": 1,
        },
        timeout=timeout,
    )
    base.raise_for_status(resp)
    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as exc:
        raise RuntimeError(f"관세청 API가 XML이 아닌 응답을 반환({base.redact_url(str(exc))})") from None

    result_code = root.findtext("header/resultCode")
    if result_code != "00":
        result_msg = root.findtext("header/resultMsg", default="(메시지 없음)")
        raise RuntimeError(f"관세청 API 오류 resultCode={result_code}: {result_msg}")

    rows = []
    for item in root.findall("body/items/item"):
        year_raw = item.findtext("year")
        if not year_raw or year_raw == "총계":  # getNewtradeList는 마지막에 합계 행을 끼워 준다
            continue
        exp_dlr = item.findtext("expDlr")
        imp_dlr = item.findtext("impDlr")
        if exp_dlr is None or imp_dlr is None:
            continue
        yyyy, mm = year_raw.split(".")
        rows.append({
            "date": f"{yyyy}-{mm}-01",
            "exp_dlr": float(exp_dlr),
            "imp_dlr": float(imp_dlr),
            "exp_cnt": float(item.findtext("expCnt", default="0") or 0),
            "imp_cnt": float(item.findtext("impCnt", default="0") or 0),
            "bal_payments": float(item.findtext("balPayments", default="0") or 0),
        })
    return rows


def _year_windows(start_yyyymm: str, end_yyyymm: str) -> list[tuple[str, str]]:
    """start~end를 [연초, 연말] 구간들로 쪼갠다 — 1년 제약 대응. 첫/마지막 구간만 잘릴 수 있음."""
    start_y, start_m = int(start_yyyymm[:4]), int(start_yyyymm[4:6])
    end_y, end_m = int(end_yyyymm[:4]), int(end_yyyymm[4:6])
    windows = []
    for y in range(start_y, end_y + 1):
        window_start_m = start_m if y == start_y else 1
        window_end_m = end_m if y == end_y else 12
        windows.append((f"{y}{window_start_m:02d}", f"{y}{window_end_m:02d}"))
    return windows


def fetch_range(start_yyyymm: str, end_yyyymm: str) -> list[dict]:
    """start_yyyymm~end_yyyymm(둘 다 "YYYYMM") 전체를 연도별로 나눠 호출해 합친다.

    각 연도 창은 base.retry()로 감싸 개별 실패가 전체를 죽이지 않게 한다 — 한
    해가 실패해도 나머지 해는 계속 채워진다(이 저장소의 "부분 실패는 조용히
    삼키지 않되 전체를 막지도 않는다" 관례).
    """
    api_key = get_api_key("customs_trade")
    if not api_key:
        log_event("collector.customs_trade.no_key", level="warning",
                  note="DATA_GO_KR_KEY not set — skipping")
        return []

    all_rows: list[dict] = []
    for strt, end in _year_windows(start_yyyymm, end_yyyymm):
        rows = base.retry(
            lambda s=strt, e=end: _fetch_year_window(s, e, api_key),
            label=f"customs_trade:{strt}-{end}",
        )
        if rows:
            all_rows.extend(rows)
    return all_rows


def backfill(start_yyyymm: str = _EARLIEST_CONFIRMED_YYYYMM) -> dict[str, int]:
    """전체 이력을 처음부터 끝까지(지금 달까지) 가져와 raw+normalized에 쌓는다.

    한 번 돌리면 이후엔 update_recent()로 최근 구간만 갱신하면 된다 — 매번
    1990년부터 다시 부르는 건 낭비이자 API에도 불필요한 부하."""
    today = datetime.now(timezone.utc)
    end_yyyymm = today.strftime("%Y%m")
    rows = fetch_range(start_yyyymm, end_yyyymm)
    return _store(rows)


def update_recent(months_back: int = 14) -> dict[str, int]:
    """최근 N개월(기본 14 — 매달 자동 실행 전제로 한 달 정도 여유)만 갱신."""
    today = datetime.now(timezone.utc)
    y, m = today.year, today.month - months_back
    while m <= 0:
        m += 12
        y -= 1
    start_yyyymm = f"{y}{m:02d}"
    end_yyyymm = today.strftime("%Y%m")
    rows = fetch_range(start_yyyymm, end_yyyymm)
    return _store(rows)


def _store(rows: list[dict]) -> dict[str, int]:
    if not rows:
        return {"exp": 0, "imp": 0}
    base.write_raw("customs_trade", "newtrade_monthly", rows)
    exp_normalized = base.append_normalized(
        "customs_export_dlr", [{"date": r["date"], "value": r["exp_dlr"]} for r in rows])
    imp_normalized = base.append_normalized(
        "customs_import_dlr", [{"date": r["date"], "value": r["imp_dlr"]} for r in rows])
    return {"exp": len(exp_normalized), "imp": len(imp_normalized)}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["backfill", "update-recent"],
                         help="backfill: 1990.01(또는 --start)~현재 전체 이력. "
                              "update-recent: 최근 --months-back개월만.")
    parser.add_argument("--start", default=_EARLIEST_CONFIRMED_YYYYMM,
                         help="backfill 시작월(YYYYMM), 기본 1990년 1월")
    parser.add_argument("--months-back", type=int, default=14,
                         help="update-recent가 갱신할 개월 수, 기본 14")
    args = parser.parse_args()

    if args.mode == "backfill":
        result = backfill(args.start)
    else:
        result = update_recent(args.months_back)
    print(f"customs_trade {args.mode}: exp={result['exp']} rows, imp={result['imp']} rows "
          f"(data/normalized/customs_export_dlr.csv, customs_import_dlr.csv)")
