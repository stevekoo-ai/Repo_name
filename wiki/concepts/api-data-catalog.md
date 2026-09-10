---
title: API 데이터 카탈로그 — 무엇을 어느 API로 가져오는가
created: 2026-09-07
updated: 2026-09-10
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
| 통계청 KOSIS | 필요 | 🟢 2026-09-08 좌표 확정: 7개 중 6개 확정(cpi/실업률/소매판매액/산업생산/반도체출하/반도체재고) — k_employed_yoy만 미해결(YoY 계산 로직 필요). 연결은 간헐적으로 완전 두절될 수 있음(사전확인 로직 있음) | 한국 물가·고용·생산 (CCI 반도체 사이클 축 포함) |
| 국토부 실거래가 | 필요 | ✅ 정상 (2026-09-07 복구) | 부동산 판단의 유일한 실측 원천 |
| 관세청 수출입 | 필요 | ✅ 정상 | 수출입 실적 1990.01~ |
| US BLS | 선택(없으면 일 25회) | ✅ 정상 (2026-09-07 신설) | 미국 임금·구인 — 연준 경로의 맨 앞단 |
| IMF WEO | 불필요 | ✅ 정상 (2026-09-07 신설) | **유일하게 전망치를 주는 소스** |
| OECD SDMX | 불필요 | ✅ 살아있음 / 미구현 — FRED 미러로 대체 가능 | (미사용) |
| 한국투자증권 KIS | 필요 | ✅ 정상 (일 3회 자동 수집) | 주가·수급·ADR·보유종목 |

## 1. FRED — 미국·글로벌 거시

키 없이 도는 CSV 엔드포인트가 기본 경로, `FRED_API_KEY`는 폴백.

**⚠️ 이 저장소엔 FRED 시리즈 정의가 두 벌 있다**(2026-09-10 확인) —
[collectors/fred.py](../../collectors/fred.py)는 `data/normalized/fred_*.csv`에,
[scripts/macro_data.py](../../scripts/macro_data.py) PRESETS는
`sources/macro-series.csv`에 쌓는다. 같은 지표가 이름만 다르게 양쪽에
있고(`us_2y` vs `us_2y_treasury`) 이력 길이도 다르다(10년물은 전자가
1962년부터, 원/달러는 후자가 2005년부터). 아래 표는 **양쪽을 합친 것**이며
마지막 열이 출처를 밝힌다 — 새 지표를 넣기 전에 여기서 먼저 확인할 것.

**⚠️ 신선도 함정**: 환율 시리즈(`DEX*`)는 관측 시점이 **뉴욕 정오**이고
발표가 며칠 밀린다 — 2026-09-07 실측에서 최신값이 08-28이었다(10일 지연).
당일 환율이 필요하면 ECOS(서울 종가 15:30)를 쓸 것. 두 소스를 섞어
상관계수를 내면 관측시각 차이 때문에 가짜 선후관계가 만들어진다 —
[4개국 통화 상호영향 분석](fx-cross-currency-krw-usd-jpy-cny.md) 참고.

| 지표 key | FRED series_id | 정의 위치 → 저장 위치 |
|---|---|---|
| `hy_oas` | `BAMLH0A0HYM2` | collectors/fred.py → `data/normalized/` |
| `kr_cpi_oecd` | `KORCPIALLMINMEI` | collectors/fred.py → `data/normalized/` |
| `kr_industrial_production_oecd` | `KORPROINDMISMEI` | collectors/fred.py → `data/normalized/` |
| `kr_retail_sales_mom_oecd` | `KORSLRTTO01GPSAM` | collectors/fred.py → `data/normalized/` |
| `kr_unemployment_oecd` | `LRHUTTTTKRM156S` | collectors/fred.py → `data/normalized/` |
| `us_10y` | `DGS10` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_10y_treasury` | `DGS10` | collectors/fred.py → `data/normalized/` |
| `us_2y` | `DGS2` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_2y_treasury` | `DGS2` | collectors/fred.py → `data/normalized/` |
| `us_3m` | `DGS3MO` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_3m_treasury` | `DGS3MO` | collectors/fred.py → `data/normalized/` |
| `us_brent` | `DCOILBRENTEU` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_core_cpi` | `CPILFESL` | collectors/fred.py → `data/normalized/` |
| `us_cpi` | `CPIAUCSL` | collectors/fred.py → `data/normalized/` |
| `us_dollar_index` | `DTWEXBGS` | collectors/fred.py → `data/normalized/` |
| `us_dollar_index_major` | `DTWEXM` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_fed_funds` | `FEDFUNDS` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_fed_funds_rate` | `FEDFUNDS` | collectors/fred.py → `data/normalized/` |
| `us_gdp_nominal` | `GDP` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_gdp_qoq` | `A191RL1Q225SBEA` | collectors/fred.py → `data/normalized/` |
| `us_gdp_real` | `GDPC1` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_hy_oas` | `BAMLH0A0HYM2` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_hy_tr` | `BAMLHYH0A0HYM2TRIV` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_ig_tr` | `BAMLCC0A0CMTRIV` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_industrial_production` | `INDPRO` | collectors/fred.py → `data/normalized/` |
| `us_nasdaq` | `NASDAQCOM` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_nonfarm_payroll` | `PAYEMS` | collectors/fred.py → `data/normalized/` |
| `us_oecd_cli` | `USALOLITOAASTSAM` | collectors/fred.py → `data/normalized/` |
| `us_ppi` | `PPIACO` | collectors/fred.py → `data/normalized/` |
| `us_retail_sales` | `RSAFS` | collectors/fred.py → `data/normalized/` |
| `us_sp500` | `SP500` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_sp500_oecd` | `SPASTT01USM661N` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_trade_balance` | `BOPGSTB` | collectors/fred.py → `data/normalized/` |
| `us_treasury_3m` | `DGS3MO` | collectors/fred.py → `data/normalized/` |
| `us_unemployment` | `UNRATE` | collectors/fred.py → `data/normalized/` |
| `us_vix` | `VIXCLS` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_wilshire` | `WILL5000PRFC` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_wti` | `DCOILWTICO` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `us_yield_curve_10y2y` | `T10Y2Y` | collectors/fred.py → `data/normalized/` |
| `usd_cny` | `DEXCHUS` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `usd_jpy` | `DEXJPUS` | macro_data.py PRESETS → `sources/macro-series.csv` |
| `usd_krw_fred` | `DEXKOUS` | macro_data.py PRESETS → `sources/macro-series.csv` |

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

**⚠️ 원래 문제가 두 개였다. 섞어 보면 진단이 어긋난다.**

1. **통계표 ID가 틀렸다(2026-09-07 시점).** 프로브 실측에서 데이터
   엔드포인트(statisticsParameterData.do)가 `"해당 통계표가 존재하지
   않습니다"`로 응답했다 — 서버에 닿았고 인증도 통과했으며 좌표만
   틀렸다는 뜻이다. 등록된 7개 시리즈가 이 이유로 전부 값을 못
   가져오고 있었다(2026-09-08 좌표 확정으로 3개는 해소 — 아래 표).
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

**2026-09-08 연결 완전 두절이 잠깐 있었다**: 후보 14개(지표 7개 ×
후보 2개씩)를 처음 돌렸을 때 **하나도 빠짐없이 connect timeout**
(15초)이었다 — tblId가 뭐든 상관없이 TCP 연결 자체가 안 됐다. 바로
전날(09-07)엔 같은 엔드포인트가 정상 연결됐었다(원인 미상: kosis.kr
측 문제 / GitHub Actions IP 대역 차단 / 반복 진단 트래픽 — [미검증]).
`kosis_lookup.py`에 8초짜리 연결 사전확인(`_connectivity_check`)을
추가한 뒤 재시도하니 약 15분 뒤 연결이 복구돼 아래 실측이 나왔다 —
**kosis.kr은 좌표가 맞아도 이 저장소의 실행 시점에 따라 아예 응답하지
않을 수 있다**는 게 이번에 새로 확인된 사실.

**✅ 2026-09-08 좌표 확정 결과 — 7개 중 6개 확정, 1개 미해결**:

전반부(itmId=ALL로 응답을 받아본 뒤 항목명을 사람이 읽는 방식)로는
3개만 확정하고 막혔다. 이후 KOSIS 공식 통계목록(statisticsList.do)·
통계표설명(getMeta type=ITM) API로 전환해(`scripts/kosis_catalog.py`,
드릴다운 기록은
[wiki/concepts/kosis-category-catalog.md](../../wiki/concepts/kosis-category-catalog.md))
나머지 3개도 추측 없이 확정했다.

| 지표 | 결과 | 비고 |
|---|---|---|
| `cpi_index` | ✅ 확정 | DT_1J22003/T/T10(전국). 228행 수신, 2025-09 117.06 |
| `unemployment_rate` | ✅ 확정 | tbl_id는 원래도 맞았음 — itm_id만 오류(13103005→T80) |
| `retail_sales_index` | ✅ 확정(단, 단위 정정) | DT_1K41002 — **지수가 아니라 명목 경상금액(억원)**. 기존 "2020=100" 단위 메모가 틀렸었다 |
| `industrial_production_index` | ✅ 확정 | DT_1F02001(시도/산업별 광공업생산지수) T10/objL1=00/objL2=0(총지수). **광공업 범위**(전산업 아님) 주의 |
| `semiconductor_shipment_index` | ✅ 확정 | 같은 표, T11/objL2=C261(반도체 제조업). 2026-07 159.1 |
| `semiconductor_inventory_index` | ✅ 확정 | 같은 표, T12/objL2=C261. 2026-07 106.5 |
| `k_employed_yoy` | ⚠️ 미해결 | 표는 연결되나 **레벨값만 주고 YoY가 없다** — 좌표만 바꾸면 조용한 오작동(늘 0점)이 되므로 보류. YoY 계산 로직 추가 필요 |

| 지표 key | orgId/tblId/itmId | 주기 | 단위 |
|---|---|---|---|
| `cpi_index` | `101/DT_1J22003 itm=T objL1=T10` | M | 2020=100 |
| `industrial_production_index` | `101/DT_1F02001 itm=T10 objL1=00 objL2=0` | M | 2020=100 |
| `k_employed_yoy` | `101/DT_1DA7001S itm=13103005 objL1=00` | M | % |
| `retail_sales_index` | `101/DT_1K41002 itm=T1 objL1=G0` | M | 억원(경상금액, 지수 아님) |
| `semiconductor_inventory_index` | `101/DT_1F02001 itm=T12 objL1=00 objL2=C261` | M | 2020=100 |
| `semiconductor_shipment_index` | `101/DT_1F02001 itm=T11 objL1=00 objL2=C261` | M | 2020=100 |
| `unemployment_rate` | `101/DT_1DA7004S itm=T80 objL1=00` | M | % |

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
| 한국 취업자 YoY | 표는 연결되나 레벨값만 줌 | `fetch_series`에 YoY 계산 로직 추가 필요(§3 표 참고) |
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

