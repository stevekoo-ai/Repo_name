"""API 데이터 카탈로그 생성기 — "어떤 데이터를 어느 API로 가져오는가" lookup table.

2026-09-07 신설. 사용자 요청: "각 API가 가져올 수 있는 데이터의 종류가
있을 것인데, 이것을 확인하여 위키에 저장해 놓고 필요한 데이터를 API로
가져올 수 있는 lookup table을 만들어보자."

**왜 손으로 쓰지 않고 생성하는가**: 이 저장소는 방금 "문서/주석이 코드와
어긋나서 한 달을 잃는" 사고를 두 번 겪었다 — collectors/kosis.py 주석은
실패 원인을 "TCP 타임아웃"이라 적고 있었지만 실제로는 통계표 ID 오류였고,
scripts/kosis_lookup.py는 "KOSIS엔 검색 API가 없다"고 단언했지만 있었다.
카탈로그를 손으로 관리하면 똑같은 드리프트가 반복된다. 그래서 각 수집기
모듈의 시리즈 정의를 **직접 읽어** 문서를 만들고, 테스트가 문서의 최신성을
검사한다(tests/test_api_catalog.py).

즉 이 문서의 단일 출처는 코드다. 시리즈를 추가하면 문서는 따라온다.

사용:
    PYTHONPATH=. python3 scripts/build_api_catalog.py          # 위키 문서 갱신
    PYTHONPATH=. python3 scripts/build_api_catalog.py --check  # 최신인지 검사만
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OUTPUT_PATH = REPO_ROOT / "wiki" / "concepts" / "api-data-catalog.md"

# 프로브 최종 실측 상태(2026-09-07 Actions run 34128807744 + 후속 수정).
# 이 값은 코드에서 읽어낼 수 없는 "지금 살아 있는가"라서 여기 명시한다 —
# scripts/api_probe.py를 돌리면 언제든 다시 확인할 수 있고, 바뀌면 여기를 고친다.
LIVE_STATUS: dict[str, str] = {
    "fred": "✅ 정상",
    "ecos": "✅ 정상",
    "kosis": "⚠️ 통계표 ID 오류(좌표) + 간헐적 연결 불안정 — 원인 두 가지",
    "molit": "✅ 정상 (2026-09-07 복구)",
    "customs_trade": "✅ 정상",
    "bls": "✅ 정상 (2026-09-07 신설)",
    "imf": "✅ 정상 (2026-09-07 신설)",
    "oecd": "✅ 살아있음 / 미구현 — FRED 미러로 대체 가능",
    "kis": "✅ 정상 (일 3회 자동 수집)",
}


def _fred_rows() -> list[tuple[str, str, str]]:
    from collectors import fred
    return [(key, sid, "일/월") for key, sid in sorted(fred.SERIES.items())]


def _ecos_rows() -> list[tuple[str, str, str]]:
    from collectors import ecos
    out = []
    for key, spec in sorted(ecos.ECOS_SERIES.items()):
        coord = f"{spec['stat_code']} / {spec['item_code1']}"
        out.append((key, coord, spec.get("cycle", "?")))
    return out


def _kosis_rows() -> list[tuple[str, str, str]]:
    from collectors import kosis
    out = []
    for key, spec in sorted(kosis.KOSIS_SERIES.items()):
        coord = f"{spec['org_id']}/{spec['tbl_id']} itm={spec['itm_id']}"
        out.append((key, coord, spec.get("cycle", "?")))
    return out


def _bls_rows() -> list[tuple[str, str, str]]:
    from collectors import bls
    return [(key, sid, "월") for key, (sid, _, _) in sorted(bls.BLS_SERIES.items())]


def _imf_rows() -> list[tuple[str, str, str]]:
    from collectors import imf
    return [(key, code, "연(전망 포함)") for key, (code, _, _) in sorted(imf.IMF_SERIES.items())]


def _describe(rows: list[tuple[str, str, str]], desc_lookup) -> list[str]:
    lines = ["| 지표 key | 코드/좌표 | 주기 | 설명 |", "|---|---|---|---|"]
    for key, code, cycle in rows:
        lines.append(f"| `{key}` | `{code}` | {cycle} | {desc_lookup(key)} |")
    return lines


def build() -> str:
    from collectors import bls, ecos, imf, kosis
    from collectors.kr_regions import all_regions

    today = date.today().isoformat()
    L: list[str] = []
    A = L.append

    A("---")
    A("title: API 데이터 카탈로그 — 무엇을 어느 API로 가져오는가")
    A(f"created: 2026-09-07")
    A(f"updated: {today}")
    A("tags: [api, data-source, lookup-table, automation, reference]")
    A("---")
    A("")
    A("> ⚙️ **이 문서는 자동 생성된다.** 손으로 고치지 말 것 —")
    A("> `PYTHONPATH=. python3 scripts/build_api_catalog.py` 가 각 수집기 모듈의")
    A("> 시리즈 정의를 직접 읽어 다시 쓴다. 시리즈를 추가하면 문서는 따라온다.")
    A("> `tests/test_api_catalog.py`가 문서와 코드의 드리프트를 검사한다.")
    A("")
    A("2026-09-07 사용자 요청(\"각 API가 가져올 수 있는 데이터의 종류를 확인해")
    A("위키에 저장하고, 필요한 데이터를 API로 가져올 수 있는 lookup table\")으로")
    A("만들었다. 계기는 같은 날 API 전수 프로브에서 드러난 사고들이다 — 부동산")
    A("실거래 수집이 한 달간 조용히 멈춰 있었고(워크플로는 234회 연속 \"success\"),")
    A("BLS 키는 주입되는데 쓰는 코드가 없었으며, KOSIS 실패 원인이 코드 주석과")
    A("정반대였다. **무엇을 가질 수 있는지 한눈에 보이지 않으면 이런 공백을")
    A("아무도 눈치채지 못한다.**")
    A("")
    A("## 0. 소스별 현황 요약")
    A("")
    A("| 소스 | 키 필요 | 현재 상태 | 이 저장소에서의 역할 |")
    A("|---|---|---|---|")
    A("| FRED | 불필요(키리스 CSV) | " + LIVE_STATUS["fred"] + " | 미국·글로벌 거시의 기본 축, OECD 미러 포함 |")
    A("| 한국은행 ECOS | 필요 | " + LIVE_STATUS["ecos"] + " | 한국 금리·환율·경상수지 원천 |")
    A("| 통계청 KOSIS | 필요 | " + LIVE_STATUS["kosis"] + " | 한국 물가·고용·생산 (CCI 반도체 사이클 축 포함) |")
    A("| 국토부 실거래가 | 필요 | " + LIVE_STATUS["molit"] + " | 부동산 판단의 유일한 실측 원천 |")
    A("| 관세청 수출입 | 필요 | " + LIVE_STATUS["customs_trade"] + " | 수출입 실적 1990.01~ |")
    A("| US BLS | 선택(없으면 일 25회) | " + LIVE_STATUS["bls"] + " | 미국 임금·구인 — 연준 경로의 맨 앞단 |")
    A("| IMF WEO | 불필요 | " + LIVE_STATUS["imf"] + " | **유일하게 전망치를 주는 소스** |")
    A("| OECD SDMX | 불필요 | " + LIVE_STATUS["oecd"] + " | (미사용) |")
    A("| 한국투자증권 KIS | 필요 | " + LIVE_STATUS["kis"] + " | 주가·수급·ADR·보유종목 |")
    A("")
    A("## 1. FRED — 미국·글로벌 거시")
    A("")
    A("키 없이 도는 CSV 엔드포인트가 기본 경로, `FRED_API_KEY`는 폴백. 코드:")
    A("[collectors/fred.py](../../collectors/fred.py)")
    A("")
    A("**⚠️ 신선도 함정**: 환율 시리즈(`DEX*`)는 관측 시점이 **뉴욕 정오**이고")
    A("발표가 며칠 밀린다 — 2026-09-07 실측에서 최신값이 08-28이었다(10일 지연).")
    A("당일 환율이 필요하면 ECOS(서울 종가 15:30)를 쓸 것. 두 소스를 섞어")
    A("상관계수를 내면 관측시각 차이 때문에 가짜 선후관계가 만들어진다 —")
    A("[4개국 통화 상호영향 분석](fx-cross-currency-krw-usd-jpy-cny.md) 참고.")
    A("")
    A("| 지표 key | FRED series_id |")
    A("|---|---|")
    for key, sid, _ in _fred_rows():
        A(f"| `{key}` | `{sid}` |")
    A("")
    A("## 2. 한국은행 ECOS — 한국 금리·환율")
    A("")
    A("코드: [collectors/ecos.py](../../collectors/ecos.py) · 키: `ECOS_API_KEY`")
    A("")
    A("| 지표 key | 통계표/항목 코드 | 주기 | 단위 |")
    A("|---|---|---|---|")
    for key, coord, cycle in _ecos_rows():
        A(f"| `{key}` | `{coord}` | {cycle} | {ecos.ECOS_SERIES[key].get('unit','')} |")
    A("")
    A("**신규 시리즈 찾는 법**: `scripts/ecos_lookup.py` (StatisticTableList /")
    A("StatisticItemList) — ecos-lookup.yml 워크플로로 실행.")
    A("")
    A("## 3. 통계청 KOSIS — 한국 물가·고용·생산")
    A("")
    A("코드: [collectors/kosis.py](../../collectors/kosis.py) · 키: `KOSIS_API_KEY`")
    A("")
    A("**⚠️ 문제가 두 개다. 섞어 보면 진단이 어긋난다.**")
    A("")
    A("1. **통계표 ID가 틀렸다.** 2026-09-07 프로브 실측에서 데이터 엔드포인트")
    A("   (statisticsParameterData.do)가 `\"해당 통계표가 존재하지 않습니다\"`로")
    A("   응답했다 — 서버에 닿았고 인증도 통과했으며 좌표만 틀렸다는 뜻이다.")
    A("   등록된 7개 시리즈가 이 이유로 전부 값을 못 가져온다.")
    A("2. **kosis.kr 연결이 간헐적으로 불안정하다.** 같은 날 몇 분 뒤 검색")
    A("   엔드포인트(statisticsSearch.do)는 `connect timeout=20`으로 죽었다 —")
    A("   같은 호스트인데 한쪽은 응답하고 한쪽은 TCP 연결조차 안 됐다.")
    A("")
    A("코드 주석에 오래 적혀 있던 \"kosis.kr TCP 타임아웃 / 한국 IP 제한 의심\"은")
    A("**연결 불안정(2번)에 대해서는 맞는 관찰**이었다. 다만 그게 시리즈가")
    A("실패하는 이유(1번)는 아니었는데 하나로 뭉뚱그려져 있었고, 그래서")
    A("\"네트워크 문제라 손쓸 수 없다\"로 결론나 통계표 좌표를 아무도 고치지")
    A("않았다. **재시도로 해결되는 문제와 좌표를 고쳐야 하는 문제는 다르다.**")
    A("")
    A("**신규/정정 통계표 찾는 법**: `scripts/kosis_lookup.py --search <키워드>`")
    A("(2026-09-07 추가, 연결 불안정을 감안해 3회 재시도). 예전엔 \"KOSIS엔")
    A("외부에서 닿는 검색 API가 없다\"고 적혀 있었지만 통합검색")
    A("(statisticsSearch.do)이 존재한다 — 그 잘못된 전제 때문에 통계표를 계속")
    A("추측만 하고 있었다.")
    A("")
    A("| 지표 key | orgId/tblId/itmId | 주기 | 단위 |")
    A("|---|---|---|---|")
    for key, coord, cycle in _kosis_rows():
        A(f"| `{key}` | `{coord}` | {cycle} | {kosis.KOSIS_SERIES[key].get('unit','')} |")
    A("")
    A("## 4. 국토교통부 실거래가 — 부동산")
    A("")
    A("코드: [collectors/molit.py](../../collectors/molit.py) 외 3종 ·")
    A("키: `DATA_GO_KR_KEY` (**활용신청은 상품 단위** — 키가 같아도 API마다 별도 승인)")
    A("")
    A("| 상품 | 모듈 | 수집 지역 |")
    A("|---|---|---|")
    A(f"| 아파트 매매 | `collectors/molit.py` | {len(all_regions())}개 시군구 |")
    A(f"| 아파트 전월세 | `collectors/molit_rent.py` | {len(all_regions())}개 |")
    A(f"| 연립다세대 매매 | `collectors/molit_villa.py` | {len(all_regions())}개 |")
    A(f"| 오피스텔 매매 | `collectors/molit_officetel.py` | {len(all_regions())}개 |")
    A("")
    A("**응답 형식 주의**: `type=json`을 요청해도 **XML로 온다**. 2026-09-07")
    A("이전 코드는 `resp.json()`만 부르다 깨졌고, 그 실패를 인증 오류로 오진해")
    A("한 달간 수집이 멈췄다. 지금은 `collectors/base.parse_data_go_kr_items()`가")
    A("형식을 신뢰하지 않고 양쪽 다 파싱한다 — 새 data.go.kr 상품을 붙일 땐")
    A("반드시 이 파서를 쓸 것.")
    A("")
    A("**월 단위 데이터**: 계약 신고가 최대 30일 밀리므로 당월 데이터는 거의")
    A("비어 있다. \"daily\"는 수집 주기이지 데이터 주기가 아니다.")
    A("")
    A("## 5. 관세청 수출입총괄 — 무역")
    A("")
    A("코드: [collectors/customs_trade.py](../../collectors/customs_trade.py) ·")
    A("키: `DATA_GO_KR_KEY` (별도 활용신청 필요)")
    A("")
    A("| 필드 | 의미 |")
    A("|---|---|")
    A("| `exp_dlr` / `imp_dlr` | 총수출 / 총수입 (달러) |")
    A("| `exp_cnt` / `imp_cnt` | 수출 / 수입 건수 |")
    A("| `bal_payments` | 무역수지 |")
    A("")
    A("**제약(실측)**: 조회 기간이 1년(12개월)을 넘으면 `resultCode=99`로 거부된다")
    A("— 여러 해는 연도별로 나눠 호출해야 한다. **1990.01까지 실측 데이터 존재.**")
    A("품목별(반도체 등) 세부는 이 API에 없다 — 별도 상품(nitemtrade) 활용신청 필요.")
    A("")
    A("## 6. US BLS — 미국 고용·물가")
    A("")
    A("코드: [collectors/bls.py](../../collectors/bls.py) · 키: `BLS_API_KEY` **선택**")
    A("(v2는 키 없이 일 25회, 키가 있으면 일 500회)")
    A("")
    A("FRED와 겹치는 축은 교차검증용이고, **FRED가 잘 안 주는 축**이 이 소스의")
    A("존재 이유다. 미국 고용·임금 → 연준 → 미 10년물 → 원/달러 → 하이닉스")
    A("외국인 수급, 그리고 한국 기준금리 → 부동산 대출금리로 이어지는 사슬의")
    A("맨 앞단인데, 지금까지 CPI와 실업률 두 개로만 보고 있었다.")
    A("")
    A("| 지표 key | BLS series_id | 설명 | 단위 |")
    A("|---|---|---|---|")
    for key, (sid, label, unit) in sorted(bls.BLS_SERIES.items()):
        A(f"| `{key}` | `{sid}` | {label} | {unit} |")
    A("")
    A("**실측 함정 두 가지** (둘 다 조용히 데이터를 망가뜨린다):")
    A("")
    A("1. `period` 필드의 `M13`은 월이 아니라 **연평균**이다. 안 거르면 매년")
    A("   12월 뒤에 13번째 포인트가 끼어 시계열이 오염된다.")
    A("2. **연도 범위 한도는 포함 연수로 센다** — 키 없이 10년, 키가 있으면")
    A("   20년. 초과하면 BLS는 **에러를 내지 않고 앞 10년만 주면서 최신 연도를")
    A("   통째로 버린다.** 2026-09-07 첫 수집에서 `startyear=올해-10`(= 11년")
    A("   요청)이라 8개 시리즈가 전부 2016-01~2025-12에서 멈췄고, 같은 날")
    A("   프로브는 CPI가 2026-07까지 있음을 확인해줬다 — 최신 9개월치를 아무")
    A("   경고 없이 잃고 있었다. 지금은 `_HISTORY_YEARS = 9`(= 정확히 10년).")
    A("")
    A("## 7. IMF WEO — 유일하게 전망치를 주는 소스")
    A("")
    A("코드: [collectors/imf.py](../../collectors/imf.py) · 키 불필요")
    A("")
    A("다른 소스는 전부 이미 일어난 일만 준다. IMF WEO는 연 2회(4월·10월)")
    A("갱신되는 공식 전망을 함께 싣는다 — 2026년 9월 현재 **2031년까지**.")
    A("")
    A("**실측과 전망은 반드시 분리 저장한다**:")
    A("- `imf_<지표>_<국가>` — 관측된 과거만")
    A("- `imf_<지표>_<국가>_forecast` — 전망 구간만")
    A("")
    A("섞으면 리포트가 예측을 실측으로 제시하게 된다. 전망은 근거로 쓰되")
    A("실측인 척하면 안 된다 — R1(실측 우선)과 같은 계열의 규칙.")
    A("")
    A(f"국가: {', '.join(imf.COUNTRIES)}")
    A("")
    A("| 지표 key | WEO 코드 | 설명 | 단위 |")
    A("|---|---|---|---|")
    for key, (code, label, unit) in sorted(imf.IMF_SERIES.items()):
        A(f"| `{key}` | `{code}` | {label} | {unit} |")
    A("")
    A("## 8. 한국투자증권 KIS — 주가·수급")
    A("")
    A("코드: [scripts/investor_flow.py](../../scripts/investor_flow.py) ·")
    A("키: `KIS_APP_KEY`/`KIS_APP_SECRET` (+ IRP/ISA 계좌별 별도 키)")
    A("")
    A("| 수집물 | 저장 위치 | 주기 |")
    A("|---|---|---|")
    A("| 종가·외국인보유율·250일 고가 | `sources/sk-hynix-price-snapshot.csv` | 일 3회 |")
    A("| 투자자별 순매수(외국인/기관/개인) | `sources/sk-hynix-investor-flow.csv` | 일 3회 |")
    A("| ADR 가격·등락 | `sources/sk-hynix-adr-quote.csv` | 일 3회 |")
    A("| 보유 종목 현황 | `sources/portfolio-holdings.csv` | 일 1회 |")
    A("")
    A("**⚠️ 토큰 재발급 제한**: 같은 appkey로 단시간에 토큰을 다시 발급하면 403이")
    A("난다. 2026-07-28~30에 이것 때문에 워크플로가 3일 연속 실패했다. 새 워크플로를")
    A("만들 땐 `kis_get_token()`의 공유 캐시를 반드시 재사용할 것.")
    A("`scripts/api_probe.py`가 KIS를 기본으로 건너뛰는 이유도 이것이다")
    A("(`PROBE_KIS=1`을 명시할 때만 찌른다).")
    A("")
    A("## 9. 아직 못 가져오는 것 (알려진 공백)")
    A("")
    A("| 원하는 데이터 | 현재 상태 | 다음 수순 |")
    A("|---|---|---|")
    A("| 품목별 수출입(반도체 단독) | 관세청 별도 상품 미신청 | data.go.kr에서 nitemtrade 활용신청 |")
    A("| 한국 물가·고용·생산 | KOSIS 통계표 ID 오류 | `kosis_lookup.py --search`로 좌표 재확정 |")
    A("| DRAM/NAND/HBM 현물가 | 공식 무료 API 없음 | 수동 입력(`data/manual_inputs/semiconductor.yaml`) 유지 |")
    A("| 청약 공고 | 개인 대상 공식 API 미제공 | 수동 입력 유지 |")
    A("| 산업부 수출입 동향 | 공식 API 미공개 | 관세청 API로 대체 중 |")
    A("")
    A("## 10. 살아있는지 확인하는 법")
    A("")
    A("```")
    A("gh workflow run api-probe.yml        # 또는 Actions 탭에서 \"API 전체 생존 프로브\"")
    A("```")
    A("")
    A("모든 소스에 최소 1회씩 호출해 ALIVE/EMPTY/DEAD/SKIPPED로 보고한다.")
    A("`SKIPPED`는 키 미설정 등으로 시도조차 안 한 것이라 **실패가 아니다** —")
    A("이 구분이 없으면 \"키가 없는 것\"과 \"API가 죽은 것\"이 뒤섞인다.")
    A("코드: [scripts/api_probe.py](../../scripts/api_probe.py)")
    A("")
    A("## Sources")
    A("")
    A("- `scripts/build_api_catalog.py` — 이 문서를 생성하는 코드(단일 출처)")
    A("- `scripts/api_probe.py` — 생존 확인 도구, 2026-09-07 이 카탈로그의 계기")
    A("- `config/api.yaml` — 소스 등록부(키 이름·base_url·신뢰등급)")
    A("- [자동화 파이프라인 레퍼런스](../architecture/automation-pipeline-reference.md)")
    A("- [4개국 통화 상호영향 분석](fx-cross-currency-krw-usd-jpy-cny.md) — 관측시각 함정")
    A("")
    return "\n".join(L) + "\n"


def main() -> int:
    content = build()
    check_only = "--check" in sys.argv
    if check_only:
        if not OUTPUT_PATH.exists():
            print(f"카탈로그 문서가 없다: {OUTPUT_PATH}", file=sys.stderr)
            return 1
        current = OUTPUT_PATH.read_text(encoding="utf-8")
        # updated: 줄은 생성일이라 매일 바뀐다 — 내용 비교에서 제외한다.
        def _strip_updated(text: str) -> str:
            return "\n".join(l for l in text.splitlines() if not l.startswith("updated:"))
        if _strip_updated(current) != _strip_updated(content):
            print("카탈로그가 코드와 어긋난다 — "
                  "PYTHONPATH=. python3 scripts/build_api_catalog.py 로 재생성할 것",
                  file=sys.stderr)
            return 1
        print("카탈로그 최신 상태 OK")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} ({len(content.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
