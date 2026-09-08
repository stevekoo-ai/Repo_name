"""KOSIS 공식 카탈로그 도구 — 통계목록(statisticsList.do) + 통계표설명(getMeta) + 개발가이드 PDF.

2026-09-08 신설. 사용자 질문 "지금 KOSIS에 요청하는 항목이 데이터 제공
가능 아이템이 맞아? 전체 제공 가능 리스트는 확보해서 저장했어?"에서
시작됨 — 지금까지(`scripts/kosis_lookup.py`)는 통계표 하나하나를
`itmId=ALL`로 무식하게 찍어보고 응답에 담긴 항목명을 사람이 읽어
"이게 맞다"고 판단하는 방식이었다. 이건 검증이지 카탈로그가 아니다.

WebSearch로 확인한 사실 — **KOSIS는 이 저장소가 안 쓰고 있던 공식
서비스 두 개를 더 제공한다**:

1. **통계목록** (`statisticsList.do`) — 카테고리(대분류→중분류→…)를 타고
   내려가며 그 아래 실제 존재하는 통계표(TBL_ID/TBL_NM) 전체를 나열하는
   진짜 "카탈로그" API. 파라미터: `vwCd`(뷰 코드, 예: MT_ZTITLE=국내통계
   주제별), `parentListId`(시작 목록 ID — 최상위는 아직 실측 확인 전).
2. **통계표설명** (`statisticsData.do?method=getMeta&type=ITM`) — 통계표
   하나(orgId+tblId)가 실제로 갖고 있는 분류/항목 코드(itmId/objL1 등)
   목록을 직접 돌려준다. 지금까지 `collectors/kosis.py`/`kosis_lookup.py`가
   `itmId=ALL`로 응답을 받아본 뒤 사람이 항목명을 읽고 맞는 코드를
   추측하던 걸 대체할 수 있다 — 이게 있으면 애초에 "추측"이 필요 없다.

이 모듈이 하는 일 — 전부 GitHub Actions에서만 실행 가능(kosis.kr이 이
샌드박스에서 EGRESS_BLOCKED):

- `download_manual()`: 공식 개발가이드 PDF(`openApi_manual_v1.0.pdf`)를
  받아 저장소에 커밋 — 다음에 새 지표를 찾을 때 추측 대신 이 문서를 먼저
  본다.
- `list_category()`: `statisticsList.do` 한 번 호출 — 카테고리 계층의
  한 층을 가져온다. 최상위 전체를 무작정 크롤링하지 않는다(KOSIS는
  농림·수산·문화 등 이 저장소와 무관한 대분류가 수백 개다) — 사용자가
  선택한 카테고리만 타고 내려간다.
- `table_item_metadata()`: 표 하나의 분류/항목 코드 목록을 가져온다 —
  아직 미해결인 4개 지표(industrial_production_index, 반도체 출하/재고,
  k_employed_yoy)에 우선 적용해서 추측 없이 정확한 좌표를 찾는 데 쓴다.

저장 위치: `data/raw/kosis/`(원본 JSON, 이 저장소의 raw-tier 관례 그대로)
+ `docs/kosis/openApi_manual_v1.0.pdf`(매뉴얼).

Usage (모두 GitHub Actions, KOSIS_API_KEY 필요):
    python -m scripts.kosis_catalog manual
    python -m scripts.kosis_catalog list-category --vw-cd MT_ZTITLE --parent-list-id ""
    python -m scripts.kosis_catalog item-meta --org-id 101 --tbl-id DT_1JH20151
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from collectors.base import raise_for_status, redact_url

KOSIS_BASE_URL = "https://kosis.kr/openapi"
MANUAL_URL = f"{KOSIS_BASE_URL}/file/openApi_manual_v1.0.pdf"

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw" / "kosis"
MANUAL_PATH = REPO_ROOT / "docs" / "kosis" / "openApi_manual_v1.0.pdf"

_TIMEOUT = 15


def _get_api_key() -> str:
    import os

    key = os.environ.get("KOSIS_API_KEY")
    if not key:
        print("KOSIS_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    return key


def _save_raw(label: str, payload) -> Path:
    """data/raw/kosis/에 원본 응답 저장 — 이 저장소의 raw-tier 관례
    (collectors/base.write_raw와 동일 패턴, 타임스탬프 파일명으로 불변).

    초 단위까지만 찍으면 같은 프로세스에서 연달아 호출할 때(예: 카테고리를
    타고 내려가며 여러 층을 저장) 파일명이 충돌해 이전 응답을 덮어쓴다 —
    마이크로초까지 찍어 불변성을 지킨다."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = RAW_DIR / f"{label}__{ts}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def download_manual() -> bool:
    """공식 개발가이드 PDF를 받아 docs/kosis/에 저장. API 키 불필요(정적 파일)."""
    print(f"GET {MANUAL_URL}", flush=True)
    try:
        resp = requests.get(MANUAL_URL, timeout=_TIMEOUT)
        raise_for_status(resp)
    except Exception as exc:
        print(f"❌ 매뉴얼 다운로드 실패: {redact_url(str(exc))[:300]}", flush=True)
        return False
    if not resp.content.startswith(b"%PDF"):
        print(f"❌ PDF가 아닌 응답(형식이 바뀌었을 수 있음): {resp.content[:100]!r}", flush=True)
        return False
    MANUAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANUAL_PATH.write_bytes(resp.content)
    print(f"✅ 저장: {MANUAL_PATH} ({len(resp.content):,} bytes)", flush=True)
    return True


def list_category(vw_cd: str, parent_list_id: str, api_key: str) -> list[dict] | None:
    """statisticsList.do 한 번 호출 — 카테고리 계층의 한 층(하위 목록 또는
    말단 통계표)을 가져온다. 응답 행에 TBL_ID가 채워져 있으면 그게 말단
    통계표, 없으면(LIST_ID만 있으면) 하위 카테고리 — 그 LIST_ID를
    parent_list_id로 다시 호출해 더 내려갈 수 있다."""
    params = {
        "method": "getList", "apiKey": api_key, "format": "json", "jsonVD": "Y",
        "vwCd": vw_cd, "parentListId": parent_list_id,
    }
    resp = requests.get(f"{KOSIS_BASE_URL}/statisticsList.do", params=params, timeout=_TIMEOUT)
    raise_for_status(resp)
    payload = resp.json()
    if isinstance(payload, dict) and payload.get("err"):
        print(f"❌ KOSIS 오류 {payload.get('err')}: {payload.get('errMsg')}", flush=True)
        return None
    if not isinstance(payload, list):
        print(f"❌ 예상과 다른 응답 형식: {str(payload)[:300]}", flush=True)
        return None
    return payload


def table_item_metadata(org_id: str, tbl_id: str, api_key: str) -> list[dict] | None:
    """statisticsData.do?method=getMeta&type=ITM — 표 하나의 분류/항목
    코드 목록을 직접 가져온다. 이게 있으면 itmId=ALL로 추측할 필요가
    없다 — 정확히 어떤 itmId/objL1 조합이 존재하는지 여기서 알 수 있다."""
    params = {
        "method": "getMeta", "type": "ITM", "apiKey": api_key,
        "format": "json", "jsonVD": "Y", "orgId": org_id, "tblId": tbl_id,
    }
    resp = requests.get(f"{KOSIS_BASE_URL}/statisticsData.do", params=params, timeout=_TIMEOUT)
    raise_for_status(resp)
    payload = resp.json()
    if isinstance(payload, dict) and payload.get("err"):
        print(f"❌ KOSIS 오류 {payload.get('err')}: {payload.get('errMsg')}", flush=True)
        return None
    if not isinstance(payload, list):
        print(f"❌ 예상과 다른 응답 형식: {str(payload)[:300]}", flush=True)
        return None
    return payload


def _print_category_rows(rows: list[dict]) -> None:
    for r in rows:
        if r.get("TBL_ID"):
            print(f"  [표] TBL_ID={r.get('TBL_ID')} TBL_NM={r.get('TBL_NM')} "
                  f"ORG_ID={r.get('ORG_ID')}", flush=True)
        else:
            print(f"  [분류] LIST_ID={r.get('LIST_ID')} LIST_NM={r.get('LIST_NM')} "
                  f"(더 내려가려면 --parent-list-id {r.get('LIST_ID')!r})", flush=True)


def _print_item_rows(rows: list[dict]) -> None:
    for r in rows:
        print(f"  OBJ_ID={r.get('OBJ_ID')} OBJ_NM={r.get('OBJ_NM')}  "
              f"OBJ_VAL_ID={r.get('OBJ_VAL_ID') or r.get('ITM_ID')} "
              f"OBJ_VAL_NM={r.get('OBJ_VAL_NM') or r.get('ITM_NM')}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("manual", help="공식 개발가이드 PDF 다운로드")

    p_cat = sub.add_parser("list-category", help="통계목록 한 층 조회")
    p_cat.add_argument("--vw-cd", default="MT_ZTITLE", help="뷰 코드 (기본: MT_ZTITLE=국내통계 주제별)")
    p_cat.add_argument("--parent-list-id", default="", help="시작 목록 ID (빈 문자열=최상위 시도)")

    p_item = sub.add_parser("item-meta", help="통계표 하나의 분류/항목 코드 조회")
    p_item.add_argument("--org-id", required=True)
    p_item.add_argument("--tbl-id", required=True)

    args = parser.parse_args()

    if args.cmd == "manual":
        return 0 if download_manual() else 1

    api_key = _get_api_key()

    if args.cmd == "list-category":
        print(f"=== 통계목록: vwCd={args.vw_cd} parentListId={args.parent_list_id!r} ===", flush=True)
        rows = None
        last_error = None
        for attempt in range(1, 4):
            try:
                rows = list_category(args.vw_cd, args.parent_list_id, api_key)
                break
            except Exception as exc:
                last_error = exc
                print(f"  [시도 {attempt}/3 실패] {type(exc).__name__}: "
                      f"{redact_url(str(exc))[:200]}", flush=True)
                if attempt < 3:
                    time.sleep(10 * attempt)
        if rows is None:
            if last_error is not None:
                print(f"3회 모두 실패 — 연결 문제로 보인다: {redact_url(str(last_error))[:200]}",
                      flush=True)
            return 1
        _print_category_rows(rows)
        path = _save_raw(f"category_{args.vw_cd}_{args.parent_list_id or 'root'}", rows)
        print(f"\n{len(rows)}행 저장: {path}", flush=True)
        return 0

    if args.cmd == "item-meta":
        print(f"=== 통계표설명(분류/항목): orgId={args.org_id} tblId={args.tbl_id} ===", flush=True)
        rows = None
        last_error = None
        for attempt in range(1, 4):
            try:
                rows = table_item_metadata(args.org_id, args.tbl_id, api_key)
                break
            except Exception as exc:
                last_error = exc
                print(f"  [시도 {attempt}/3 실패] {type(exc).__name__}: "
                      f"{redact_url(str(exc))[:200]}", flush=True)
                if attempt < 3:
                    time.sleep(10 * attempt)
        if rows is None:
            if last_error is not None:
                print(f"3회 모두 실패 — 연결 문제로 보인다: {redact_url(str(last_error))[:200]}",
                      flush=True)
            return 1
        _print_item_rows(rows)
        path = _save_raw(f"item_meta_{args.org_id}_{args.tbl_id}", rows)
        print(f"\n{len(rows)}행 저장: {path}", flush=True)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
