---
title: API 데이터 카탈로그 — 무엇을 어느 API로 가져오는가
created: 2026-09-07
updated: 2026-09-08
tags: [api, data-source, lookup-table, automation, reference]
---

> ⚙️ **이 문서는 자동 생성된다.** 손으로 고치지 말 것 —
> `PYTHONPATH=. python3 scripts/build_api_catalog.py` 가 각 수집기 모듈의
> 시리즈 정의를 직접 읽어 다시 쓴다. 시리즈를 추가하면 문서는 따라온다.
> `tests/test_api_catalog.py`가 문서와 코드의 드리프트를 검사한다.

2026-09-07 사용자 요청("각 API가 가져올 수 있는 데이터의 종류를 확인해
위키에 저장하고, 필요한 데이터를 API로 가져올 수 있는 lookup table")으로
만들었다. 계기는 같은 날 API 전수 프로브에서 드러난 사고들이다 — 부동산
실거래 수집이 한 달간 조용히 멈춰 있었고(워크플로는 234회 연속 "success"),
BLS 키는 주입되는데 쓰는 코드가 없었으며, KOSIS 실패 원인이 코드 주석과
정반대였다. **무엇을 가질 수 있는지 한눈에 보이지 않으면 이런 공백을
아무도 눈치채지 못한다.**

## 0. 소스별 현황 요약

| 소스 | 키 필요 | 현재 상태 | 이 저장소에서의 역할 |
|---|---|---|---|
| FRED | 불필요(키리스 CSV) | ✅ 정상 | 미국·글로벌 거시의 기본 축, OECD 미러 포함 |
| 한국은행 ECOS | 필요 | ✅ 정상 | 한국 금리·환율·경상수지 원천 |
| 통계청 KOSIS | 필요 | 🔴 2026-09-08 실측: 데이터 엔드포인트 14/14 전부 connect timeout — 좌표 문제와 별개로 지금 이 순간 연결 자체가 끊김(전날엔 연결 정상) | 한국 물가·고용·생산 (CCI 반도체 사이클 축 포함) |
| 국토부 실거래가 | 필요 | ✅ 정상 (2026-09-07 복구) | 부동산 판단의 유일한 실측 원천 |
| 관세청 수출입 | 필요 | ✅ 정상 | 수출입 실적 1990.01~ |
| US BLS | 선택(없으면 일 25회) | ✅ 정상 (2026-09-07 신설) | 미국 임금·구인 — 연준 경로의 맨 앞단 |
| IMF WEO | 불필요 | ✅ 정상 (2026-09-07 신설) | **유일하게 전망치를 주는 소스** |
| OECD SDMX | 불필요 | ✅ 살아있음 / 미구현 — FRED 미러로 대체 가능 | (미사용) |
| 한국투자증권 KIS | 필요 | ✅ 정상 (일 3회 자동 수집) | 주가·수급·ADR·보유종목 |

## 1. FRED — 미국·글로벌 거시

키 없이 도는 CSV 엔드포인트가 기본 경로, `FRED_API_KEY`는 폴백. 코드:
[collectors/fred.py](../../collectors/fred.py)

**⚠️ 신선도 함정**: 환율 시리즈(`DEX*`)는 관측 시점이 **뉴욕 정오**이고
발표가 며칠 밀린다 — 2026-09-07 실측에서 최신값이 08-28이었다(10일 지연).
당일 환율이 필요하면 ECOS(서울 종가 15:30)를 쓸 것. 두 소스를 섞어
상관계수를 내면 관측시각 차이 때문에 가짜 선후관계가 만들어진다 —
[4개국 통화 상호영향 분석](fx-cross-currency-krw-usd-jpy-cny.md) 참고.

| 지표 key | FRED series_id |
|---|---|
| `hy_oas` | `BAMLH0A0HYM2` |
| `kr_cpi_oecd` | `KORCPIALLMINMEI` |
| `kr_industrial_production_oecd` | `KORPROINDMISMEI` |
| `kr_retail_sales_mom_oecd` | `KORSLRTTO01GPSAM` |
| `kr_unemployment_oecd` | `LRHUTTTTKRM156S` |
| `us_10y_treasury` | `DGS10` |
| `us_2y_treasury` | `DGS2` |
| `us_3m_treasury` | `DGS3MO` |
| `us_core_cpi` | `CPILFESL` |
| `us_cpi` | `CPIAUCSL` |
| `us_dollar_index` | `DTWEXBGS` |
| `us_fed_funds_rate` | `FEDFUNDS` |
| `us_gdp_qoq` | `A191RL1Q225SBEA` |
| `us_industrial_production` | `INDPRO` |
| `us_nonfarm_payroll` | `PAYEMS` |
| `us_oecd_cli` | `USALOLITOAASTSAM` |
| `us_ppi` | `PPIACO` |
| `us_retail_sales` | `RSAFS` |
| `us_trade_balance` | `BOPGSTB` |
| `us_treasury_3m` | `DGS3MO` |
| `us_unemployment` | `UNRATE` |
| `us_yield_curve_10y2y` | `T10Y2Y` |

## 2. 한국은행 ECOS — 한국 금리·환율

코드: [collectors/ecos.py](../../collectors/ecos.py) · 키: `ECOS_API_KEY`

| 지표 key | 통계표/항목 코드 | 주기 | 단위 |
|---|---|---|---|
| `base_rate` | `722Y001 / 0101000` | M | % |
| `current_account` | `301Y013 / 000000` | M | 백만달러 |
| `gdp_growth_qoq` | `902Y015 / KOR` | Q | % |
| `kr_10y_yield` | `817Y002 / 010400000` | D | % |
| `kr_3y_yield` | `817Y002 / 010200000` | D | % |
| `ppi_yoy_level` | `404Y014 / *AA` | M | 2020=100 |
| `usdkrw` | `731Y001 / 0000001` | D | KRW |

**신규 시리즈 찾는 법**: `scripts/ecos_lookup.py` (StatisticTableList /
StatisticItemList) — ecos-lookup.yml 워크플로로 실행.

## 3. 통계청 KOSIS — 한국 물가·고용·생산

코드: [collectors/kosis.py](../../collectors/kosis.py) · 키: `KOSIS_API_KEY`

**⚠️ 문제가 두 개다. 섞어 보면 진단이 어긋난다.**

1. **통계표 ID가 틀렸다.** 2026-09-07 프로브 실측에서 데이터 엔드포인트
   (statisticsParameterData.do)가 `"해당 통계표가 존재하지 않습니다"`로
   응답했다 — 서버에 닿았고 인증도 통과했으며 좌표만 틀렸다는 뜻이다.
   등록된 7개 시리즈가 이 이유로 전부 값을 못 가져온다.
2. **kosis.kr 연결이 간헐적으로 불안정하다.** 같은 날 몇 분 뒤 검색
   엔드포인트(statisticsSearch.do)는 `connect timeout=20`으로 죽었다 —
   같은 호스트인데 한쪽은 응답하고 한쪽은 TCP 연결조차 안 됐다.

코드 주석에 오래 적혀 있던 "kosis.kr TCP 타임아웃 / 한국 IP 제한 의심"은
**연결 불안정(2번)에 대해서는 맞는 관찰**이었다. 다만 그게 시리즈가
실패하는 이유(1번)는 아니었는데 하나로 뭉뚱그려져 있었고, 그래서
"네트워크 문제라 손쓸 수 없다"로 결론나 통계표 좌표를 아무도 고치지
않았다. **재시도로 해결되는 문제와 좌표를 고쳐야 하는 문제는 다르다.**

**신규/정정 통계표 찾는 법**: `scripts/kosis_lookup.py --search <키워드>`
(2026-09-07 추가, 연결 불안정을 감안해 3회 재시도). 예전엔 "KOSIS엔
외부에서 닿는 검색 API가 없다"고 적혀 있었지만 통합검색
(statisticsSearch.do)이 존재한다 — 그 잘못된 전제 때문에 통계표를 계속
추측만 하고 있었다.

**🔴 2026-09-08 좌표 확정 작업 중 실측**: 후보 14개(지표 7개 × 후보 2개씩)를
데이터 엔드포인트로 전부 찔러봤는데 **하나도 빠짐없이 connect timeout**
(15초)이었다. tblId가 뭐든 상관없이 TCP 연결 자체가 안 됐다는 뜻 — 좌표가
맞고 틀리고를 떠나 이 순간은 검증 자체가 불가능했다. 바로 전날(09-07)
같은 엔드포인트가 정상 연결돼 JSON 에러 응답("해당 통계표가 존재하지
않습니다")을 받았던 것과 대조적 — 하루 사이 완전 연결 두절로 악화된
것으로 보인다(원인 미상: kosis.kr 측 문제 / GitHub Actions IP 대역 차단 /
이날 반복된 진단 트래픽으로 인한 일시적 차단, 셋 다 가능성 있고 [미검증]).
`kosis_lookup.py`에 8초짜리 연결 사전확인을 추가해, 다음 시도부터는
14개 후보를 다 돌리기 전에 연결 자체가 죽어 있는지부터 싸게 확인한다.

| 지표 key | orgId/tblId/itmId | 주기 | 단위 |
|---|---|---|---|
| `cpi_index` | `101/DT_1J17009 itm=T60` | M | 2020=100 |
| `industrial_production_index` | `101/DT_1JH20151 itm=13103141670T4` | M | 2020=100 |
| `k_employed_yoy` | `101/DT_1DA7001S itm=13103005` | M | Persons |
| `retail_sales_index` | `101/DT_1K31009 itm=13103159999T2A` | M | 2020=100 |
| `semiconductor_inventory_index` | `101/DT_1E66010 itm=T30` | M | 2020=100 |
| `semiconductor_shipment_index` | `101/DT_1E66010 itm=T10` | M | 2020=100 |
| `unemployment_rate` | `101/DT_1DA7004S itm=13103005` | M | % |

## 4. 국토교통부 실거래가 — 부동산

코드: [collectors/molit.py](../../collectors/molit.py) 외 3종 ·
키: `DATA_GO_KR_KEY` (**활용신청은 상품 단위** — 키가 같아도 API마다 별도 승인)

| 상품 | 모듈 | 수집 지역 |
|---|---|---|
| 아파트 매매 | `collectors/molit.py` | 55개 시군구 |
| 아파트 전월세 | `collectors/molit_rent.py` | 55개 |
| 연립다세대 매매 | `collectors/molit_villa.py` | 55개 |
| 오피스텔 매매 | `collectors/molit_officetel.py` | 55개 |

**응답 형식 주의**: `type=json`을 요청해도 **XML로 온다**. 2026-09-07
이전 코드는 `resp.json()`만 부르다 깨졌고, 그 실패를 인증 오류로 오진해
한 달간 수집이 멈췄다. 지금은 `collectors/base.parse_data_go_kr_items()`가
형식을 신뢰하지 않고 양쪽 다 파싱한다 — 새 data.go.kr 상품을 붙일 땐
반드시 이 파서를 쓸 것.

**월 단위 데이터**: 계약 신고가 최대 30일 밀리므로 당월 데이터는 거의
비어 있다. "daily"는 수집 주기이지 데이터 주기가 아니다.

## 5. 관세청 수출입총괄 — 무역

코드: [collectors/customs_trade.py](../../collectors/customs_trade.py) ·
키: `DATA_GO_KR_KEY` (별도 활용신청 필요)

| 필드 | 의미 |
|---|---|
| `exp_dlr` / `imp_dlr` | 총수출 / 총수입 (달러) |
| `exp_cnt` / `imp_cnt` | 수출 / 수입 건수 |
| `bal_payments` | 무역수지 |

**제약(실측)**: 조회 기간이 1년(12개월)을 넘으면 `resultCode=99`로 거부된다
— 여러 해는 연도별로 나눠 호출해야 한다. **1990.01까지 실측 데이터 존재.**
품목별(반도체 등) 세부는 이 API에 없다 — 별도 상품(nitemtrade) 활용신청 필요.

## 6. US BLS — 미국 고용·물가

코드: [collectors/bls.py](../../collectors/bls.py) · 키: `BLS_API_KEY` **선택**
(v2는 키 없이 일 25회, 키가 있으면 일 500회)

FRED와 겹치는 축은 교차검증용이고, **FRED가 잘 안 주는 축**이 이 소스의
존재 이유다. 미국 고용·임금 → 연준 → 미 10년물 → 원/달러 → 하이닉스
외국인 수급, 그리고 한국 기준금리 → 부동산 대출금리로 이어지는 사슬의
맨 앞단인데, 지금까지 CPI와 실업률 두 개로만 보고 있었다.

| 지표 key | BLS series_id | 설명 | 단위 |
|---|---|---|---|
| `us_avg_hourly_earnings` | `CES0500000003` | 민간 시간당 평균임금 | 달러 |
| `us_cpi_all` | `CUUR0000SA0` | 소비자물가지수 CPI-U 전체(도시) | 1982-84=100 |
| `us_cpi_core` | `CUUR0000SA0L1E` | 근원 CPI(식품·에너지 제외) | 1982-84=100 |
| `us_job_openings` | `JTS000000000000000JOL` | JOLTS 구인건수 | 천건 |
| `us_labor_participation` | `LNS11300000` | 경제활동참가율 | % |
| `us_nonfarm_payroll` | `CES0000000001` | 비농업부문 총고용 | 천명 |
| `us_ppi_final_demand` | `WPUFD4` | 생산자물가 최종수요 | index |
| `us_unemployment` | `LNS14000000` | 실업률(계절조정) | % |

**실측 함정 두 가지** (둘 다 조용히 데이터를 망가뜨린다):

1. `period` 필드의 `M13`은 월이 아니라 **연평균**이다. 안 거르면 매년
   12월 뒤에 13번째 포인트가 끼어 시계열이 오염된다.
2. **연도 범위 한도는 포함 연수로 센다** — 키 없이 10년, 키가 있으면
   20년. 초과하면 BLS는 **에러를 내지 않고 앞 10년만 주면서 최신 연도를
   통째로 버린다.** 2026-09-07 첫 수집에서 `startyear=올해-10`(= 11년
   요청)이라 8개 시리즈가 전부 2016-01~2025-12에서 멈췄고, 같은 날
   프로브는 CPI가 2026-07까지 있음을 확인해줬다 — 최신 9개월치를 아무
   경고 없이 잃고 있었다. 지금은 `_HISTORY_YEARS = 9`(= 정확히 10년).

## 7. IMF WEO — 유일하게 전망치를 주는 소스

코드: [collectors/imf.py](../../collectors/imf.py) · 키 불필요

다른 소스는 전부 이미 일어난 일만 준다. IMF WEO는 연 2회(4월·10월)
갱신되는 공식 전망을 함께 싣는다 — 2026년 9월 현재 **2031년까지**.

**실측과 전망은 반드시 분리 저장한다**:
- `imf_<지표>_<국가>` — 관측된 과거만
- `imf_<지표>_<국가>_forecast` — 전망 구간만

섞으면 리포트가 예측을 실측으로 제시하게 된다. 전망은 근거로 쓰되
실측인 척하면 안 된다 — R1(실측 우선)과 같은 계열의 규칙.

국가: KOR, USA, CHN, JPN

| 지표 key | WEO 코드 | 설명 | 단위 |
|---|---|---|---|
| `current_account` | `BCA_NGDPD` | 경상수지(GDP 대비 %) | % of GDP |
| `gdp_growth` | `NGDP_RPCH` | 실질 GDP 성장률(연간, %) | % |
| `govt_debt` | `GGXWDG_NGDP` | 일반정부 총부채(GDP 대비 %) | % of GDP |
| `inflation` | `PCPIPCH` | 소비자물가 상승률(연평균, %) | % |
| `unemployment` | `LUR` | 실업률(연간, %) | % |

## 8. 한국투자증권 KIS — 주가·수급

코드: [scripts/investor_flow.py](../../scripts/investor_flow.py) ·
키: `KIS_APP_KEY`/`KIS_APP_SECRET` (+ IRP/ISA 계좌별 별도 키)

| 수집물 | 저장 위치 | 주기 |
|---|---|---|
| 종가·외국인보유율·250일 고가 | `sources/sk-hynix-price-snapshot.csv` | 일 3회 |
| 투자자별 순매수(외국인/기관/개인) | `sources/sk-hynix-investor-flow.csv` | 일 3회 |
| ADR 가격·등락 | `sources/sk-hynix-adr-quote.csv` | 일 3회 |
| 보유 종목 현황 | `sources/portfolio-holdings.csv` | 일 1회 |

**⚠️ 토큰 재발급 제한**: 같은 appkey로 단시간에 토큰을 다시 발급하면 403이
난다. 2026-07-28~30에 이것 때문에 워크플로가 3일 연속 실패했다. 새 워크플로를
만들 땐 `kis_get_token()`의 공유 캐시를 반드시 재사용할 것.
`scripts/api_probe.py`가 KIS를 기본으로 건너뛰는 이유도 이것이다
(`PROBE_KIS=1`을 명시할 때만 찌른다).

## 9. 아직 못 가져오는 것 (알려진 공백)

| 원하는 데이터 | 현재 상태 | 다음 수순 |
|---|---|---|
| 품목별 수출입(반도체 단독) | 관세청 별도 상품 미신청 | data.go.kr에서 nitemtrade 활용신청 |
| 한국 물가·고용·생산 | KOSIS 통계표 ID 오류 | `kosis_lookup.py --search`로 좌표 재확정 |
| DRAM/NAND/HBM 현물가 | 공식 무료 API 없음 | 수동 입력(`data/manual_inputs/semiconductor.yaml`) 유지 |
| 청약 공고 | 개인 대상 공식 API 미제공 | 수동 입력 유지 |
| 산업부 수출입 동향 | 공식 API 미공개 | 관세청 API로 대체 중 |

## 10. 살아있는지 확인하는 법

```
gh workflow run api-probe.yml        # 또는 Actions 탭에서 "API 전체 생존 프로브"
```

모든 소스에 최소 1회씩 호출해 ALIVE/EMPTY/DEAD/SKIPPED로 보고한다.
`SKIPPED`는 키 미설정 등으로 시도조차 안 한 것이라 **실패가 아니다** —
이 구분이 없으면 "키가 없는 것"과 "API가 죽은 것"이 뒤섞인다.
코드: [scripts/api_probe.py](../../scripts/api_probe.py)

## Sources

- `scripts/build_api_catalog.py` — 이 문서를 생성하는 코드(단일 출처)
- `scripts/api_probe.py` — 생존 확인 도구, 2026-09-07 이 카탈로그의 계기
- `config/api.yaml` — 소스 등록부(키 이름·base_url·신뢰등급)
- [자동화 파이프라인 레퍼런스](../architecture/automation-pipeline-reference.md)
- [4개국 통화 상호영향 분석](fx-cross-currency-krw-usd-jpy-cny.md) — 관측시각 함정

