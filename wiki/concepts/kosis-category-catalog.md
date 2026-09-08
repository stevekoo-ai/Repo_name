---
title: KOSIS 통계목록 카탈로그 (실측 기록)
created: 2026-09-08
updated: 2026-09-08
tags: [kosis, api, data-catalog, kosis-category-catalog]
---

# KOSIS 통계목록 카탈로그 (실측 기록)

## 이 문서가 왜 있는가

2026-09-08 사용자 질문: "전체 카탈로그를 KOSIS에서 제공하고 있을 것인데?
이것을 확인하고... 전체 카탈로그가 있어야 다음에 어떤 지표를 확인해보자고
했을 때 바로 어떤 API를 호출해야 할지가 나올 거잖아?"

`scripts/kosis_catalog.py`(GitHub Actions에서만 실행 가능, kosis.kr이 이
샌드박스에서 EGRESS_BLOCKED)로 KOSIS 공식 통계목록(`statisticsList.do`)·
통계표설명(`getMeta&type=ITM`) API를 실측 호출해 얻은 결과를 여기 기록한다.

**중요 — 왜 이 문서가 raw JSON이 아니라 markdown인가**: 처음엔
`data/raw/kosis/`에 원본 JSON을 커밋할 계획이었다. 그런데 `.gitignore`에
`data/raw/*/*.json`이 이미 있다 — 이 저장소의 raw-tier(Level 1)는
**의도적으로 버전관리 대상이 아니다**("재현 가능한 중간 산출물, git에
안 넣는다"는 기존 정책, `.gitignore` 주석 참고). `kosis-catalog.yml`이
매번 "No new catalog artifacts"만 찍고 아무것도 커밋 못 한 이유가 이것 —
raw JSON에 의존한 설계가 애초에 이 저장소 관례와 맞지 않았다. 그래서 실측
결과를 **사람이 읽고 재사용할 수 있는 이 markdown 문서**에 직접 기록하는
방식으로 바꿨다. (raw JSON 자체는 각 GitHub Actions 실행 로그에는 남아있고,
로컬 재현이 필요하면 `python -m scripts.kosis_catalog list-category/item-meta`
를 다시 돌리면 된다 — API가 멱등이라 재현 비용이 낮다는 게 애초에 raw-tier를
git에 안 넣는 이 저장소 정책의 전제와도 맞는다.)

## 최상위 대분류 (vwCd=MT_ZTITLE, parentListId="") — 2026-09-08 실측

**주의**: 공식 매뉴얼(`docs/kosis/openApi_manual_v1.0.pdf`, §2.1.3.1) 예제가
`parentListId='A'`를 "최상위 목록 생성"이라 주석 달았는데, 실측해보니
**'A'는 root가 아니라 "인구" 대분류 자체**였다(그 예제 앱이 데모용으로
하드코딩한 시작점일 뿐). **진짜 최상위는 `parentListId=""`(빈 문자열)**.

| LIST_ID | LIST_NM | LIST_ID | LIST_NM |
|---|---|---|---|
| A | 인구 | K1 | 농림 |
| B | 사회일반 | K2 | 수산 |
| C | 범죄ㆍ안전 | L | 광업ㆍ제조업 |
| D | 노동 | M1 | 건설 |
| E | 소득ㆍ소비ㆍ자산 | M2 | 교통ㆍ물류 |
| F | 보건 | N1 | 정보통신 |
| G | 복지 | N2 | 과학ㆍ기술 |
| H1 | 교육ㆍ훈련 | O | 도소매ㆍ서비스 |
| H2 | 문화ㆍ여가 | P1 | 임금 |
| I1 | 주거 | P2 | 물가 |
| I2 | 국토이용 | Q | 국민계정 |
| J1 | 경제일반ㆍ경기 | R | 정부ㆍ재정 |
| J2 | 기업경영 | S1 | 금융 |
| — | — | S2 | 무역ㆍ국제수지 |
| — | — | T | 환경 |
| — | — | U | 에너지 |
| — | — | V | 지역통계 |

## 광업ㆍ제조업(L) 드릴다운 — industrial_production_index·반도체 출하/재고용

```
L (광업ㆍ제조업)
└─ L_4 (광업제조업동향조사)
   ├─ 101_G131 (생산, 출하, 재고)   ← 이쪽
   └─ 101_G132 (생산능력, 가동률)
```

`101_G131` 산하 통계표 11개 (2026-09-08 실측, `list-category --parent-list-id 101_G131`):

| TBL_ID | TBL_NM | 비고 |
|---|---|---|
| DT_1F02001 | 시도/산업별 광공업생산지수(2020=100) | ✅ 3개 지표 모두 이 표로 확정(아래 참고) |
| DT_1F02003 | 시도 재별 제조업생산지수(2020=100) | |
| DT_1F02004 | 시도 공업구조별 제조업생산지수(2020=100) | |
| DT_1F02005 | 설비용기계류 생산지수(2020=100) | |
| DT_1F02007 | 기업규모별 제조업생산지수(매출액 기준)(2020=100) | |
| DT_1F02011 | 기본분류 일부항목 제외 광공업생산지수(2020=100) | |
| DT_1F02012 | 품목별 광공업 생산·출하·재고·내수·수출량 | ⚠️ item-meta 실측 완료(72개 품목) — **반도체 없음**, 석유화학/철강/자동차부품/전기·가스업 위주(품목 코드 20xxxxxx=화학, 24xxxxxx=금속, 30xxxxxx=자동차, 35xxxxxx=전기가스). 반도체 후보에서 제외. |
| DT_1F02013 | 제조업 재고율 | |
| DT_1F02016 | 내수/수출 광공업출하지수(2020=100) | |
| DT_1F02031 | 광역경제권/산업별지수(2020=100) | |
| DT_1F02061 | 명절과조업효과조정 광공업생산지수(2020=100) | |

### DT_1F02001 확정 결과 (2026-09-08)

`item-meta`로 이 표의 분류 구조를 확인한 결과 3개 분류축이 있었다:
- `ITEM`(항목): T10=생산지수(원지수), T11=생산자제품 출하지수(원지수),
  T12=생산자제품 재고지수(원지수) — 이게 `itmId` 자리.
  (T20/T21/T22는 계절조정판)
- `A`(시도별): 00=전국, 11=서울 ... — `objL1` 자리.
- `B`(산업별): 0=총지수, C26=전자부품ㆍ컴퓨터ㆍ영상ㆍ음향및통신장비 제조업,
  **C261=반도체 제조업**(C26의 하위) — `objL2` 자리.

`verify-data`로 실제 데이터까지 확인(3개 조합 전부 성공):

| 지표 | itmId | objL1 | objL2 | 실측값 |
|---|---|---|---|---|
| industrial_production_index | T10 | 00 | 0(총지수) | 2026-06 123.3, 2026-07 120.4 |
| semiconductor_shipment_index | T11 | 00 | C261(반도체 제조업) | 2026-07 159.1 |
| semiconductor_inventory_index | T12 | 00 | C261(반도체 제조업) | 2026-06 88.7, 2026-07 106.5 |

**주의**: 이 표는 "광공업"(광업+제조업) 범위다 — 서비스업·건설업까지
포함하는 "전산업생산지수"와는 다르다. 한국 언론·한은이 "산업생산"이라
할 때 통상 이 광공업생산지수를 가리키므로 매크로 프록시로는 적절하지만
스케일 차이는 인지하고 있을 것. `collectors/kosis.py::KOSIS_SERIES`에
반영 완료.

## 노동(D) — k_employed_yoy용

2026-09-08 실측 시도 2회 모두 연결 실패(KOSIS 간헐적 완전 연결 두절,
`collectors/kosis.py` 문서화된 현상과 동일) — 아직 드릴다운 못 함.
다음 세션에서 `list-category --parent-list-id D`부터 재시도.

## 사용법 재현

```bash
# GitHub Actions에서만 (kosis.kr이 로컬 샌드박스에서 EGRESS_BLOCKED)
python -m scripts.kosis_catalog list-category --vw-cd MT_ZTITLE --parent-list-id ""      # 최상위 30개
python -m scripts.kosis_catalog list-category --vw-cd MT_ZTITLE --parent-list-id L        # 광업ㆍ제조업 하위
python -m scripts.kosis_catalog list-category --vw-cd MT_ZTITLE --parent-list-id L_4      # 광업제조업동향조사 하위
python -m scripts.kosis_catalog list-category --vw-cd MT_ZTITLE --parent-list-id 101_G131 # 생산,출하,재고 표 목록
python -m scripts.kosis_catalog item-meta --org-id 101 --tbl-id DT_1F02012                # 표 하나의 품목 코드
```

## 관련 문서

- [자동화 파이프라인 레퍼런스](../architecture/automation-pipeline-reference.md)
- `collectors/kosis.py` — KOSIS_SERIES 좌표 정의(7개 중 3개 확정, 4개 미해결)
- `docs/kosis/openApi_manual_v1.0.pdf` — 공식 개발가이드(172쪽, 2026-09-08 다운로드)

## Sources

- `scripts/kosis_catalog.py` 실행 결과(GitHub Actions 워크플로 `kosis-catalog.yml`
  run #5~#10, 2026-09-08) — `statisticsList.do`(통계목록)·`statisticsData.do?
  method=getMeta&type=ITM`(통계표설명) 실측 호출 로그.
- `docs/kosis/openApi_manual_v1.0.pdf` — KOSIS 공식 OpenAPI 개발가이드(§2.1.3.1
  통계목록, §2.5.3.4 통계표설명).
- `collectors/kosis.py` 모듈 docstring 및 `KOSIS_SERIES` 딕셔너리 — 기존
  좌표 확정/미해결 현황.
