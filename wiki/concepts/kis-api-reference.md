---
title: KIS Open API 데이터 카탈로그
created: 2026-07-31
updated: 2026-07-31
tags: [kis-api, data-reference, infrastructure, github-actions]
---

한국투자증권(KIS) Open API로 실제 가져올 수 있는 데이터를 정리한 참고
페이지. 이후 논의 중 "이 데이터 API로 확인 가능한가?"가 나오면 매번
`open-trading-api` 저장소를 다시 뒤지지 않고 이 페이지부터 확인한다.
두 구역으로 나뉜다 — **① 이미 구현돼 자동 수집 중인 것**, **② 조사는
끝났지만 아직 구현 안 한 것(필요해지면 바로 착수 가능)**.

## 0. 인증 방식 (공통)

모든 TR은 OAuth2 접근토큰(`kis_get_token()`)이 필요 — `KIS_APP_KEY`/
`KIS_APP_SECRET`(계좌별로 `_ISP`/`_IRP` 오버라이드 존재)를 GitHub
Secrets에서만 읽고, 발급받은 토큰은 `scripts/.kis_token_cache.json`에
캐싱해 여러 워크플로가 공유한다(2026-07-31 PR #35로 충돌 해결).
자세한 시크릿 목록은 [entities/automation-infrastructure.md](../entities/automation-infrastructure.md) 참고.

## 1. 이미 구현됨 — 매일 자동 수집 중

| 커맨드(`scripts/investor_flow.py` 또는 `portfolio_holdings.py`) | TR ID | 무엇을 가져오나 | 저장 파일 | 실계정 검증 |
| --- | --- | --- | --- | --- |
| `investor_flow.py fetch` | `FHKST01010900` | 종목별 일별 투자자매매동향 — 외국인/기관/개인 순매수 수량·금액(최근 30영업일) | `sources/sk-hynix-investor-flow.csv` | ✅ 2026-07-28 검증(금액은 백만원 단위로 확인) |
| `investor_flow.py quote` | `FHKST01010100` | 국내주식 현재가·전일대비·등락률·거래량(즉석 조회용, 미저장) | — | ✅ 검증 |
| `investor_flow.py snapshot` | `FHKST01010100` | 위와 같은 TR — 부가 필드로 **외국인 보유율·보유수량·250일 최고가·그 대비 등락률(드로다운)**까지 저장 | `sources/sk-hynix-price-snapshot.csv` | ✅ 검증 |
| `investor_flow.py adr-quote`(기본, 일별) | `HHDFS76240000` | 해외상장(ADR) 종목의 **일별 확정 시세** — 호출 시각과 무관하게 마지막 마감 거래일의 정확한 종가·등락률 | `sources/sk-hynix-adr-quote.csv` | 🔧 필드명은 검증됨, 단 **버그 발견+수정 중**([PR #40](https://github.com/stevekoo-ai/Repo_name/pull/40), 병합 대기): API의 `rate` 필드가 `diff`와 부호가 어긋나는 응답 확인(2026-07-31 SKHY, diff=+3.10인데 rate=-2.08%) → `change_pct`를 `diff`·전일종가로 직접 재계산하도록 수정 |
| `investor_flow.py adr-quote --intraday` | `HHDFS76200200` | 해외상장 종목 실시간 현재가 — 나스닥 정규장(22:30~05:00 KST) 밖에서는 "현재가=전일종가"만 반환하는 한계 있음 | 〃 | ✅ 검증(단, 이 한계도 함께 확인됨) |
| `investor_flow.py credit-balance` | `FHPST04760000` | **국내주식 신용잔고 일별추이** — 융자(신규/상환/잔고 주수·금액·비율)와 대주(공매도용 대여) 잔고를 종목별로. **찐반등 신호①(빚의 청산)의 데이터소스** | `sources/sk-hynix-credit-balance.csv` | ✅ 검증 완료(2026-08-01, 필드명 정상·`loan_balance_qty` 값 교차검증 완료 — [market-cycles-leverage-risk.md](market-cycles-leverage-risk.md) 참고. `loan_balance_amt` 금액 단위는 여전히 미확정, 절대 금액 표기 금지) |
| `investor_flow.py index-quote` | `FHPUP02100000` | **국내업종 현재지수** — 코스피(0001)/코스닥(1001)/코스피200(2001) 현재가·전일대비·등락률 + **상승/하락/보합/상한가/하한가 종목수** | `sources/kr-index-quote.csv` | ✅ 검증 완료(2026-08-01, PR #39 첫 실행에서 정상 수집 확인) |
| `investor_flow.py short-sale` | `FHPST04830000` | 국내주식 **공매도 일별추이** — 당일/누적 공매도 체결수량·비중·거래대금 | `sources/sk-hynix-short-sale.csv` | ✅ 검증 완료(2026-08-01, PR #39 첫 실행에서 정상 수집 확인) |
| `investor_flow.py etf-nav` | `FHPST02400000` | **ETF/ETN 현재가+NAV+추적오차율+괴리율** | `sources/portfolio-etf-nav.csv` | ✅ 검증 완료(2026-08-01, PR #39 첫 실행에서 정상 수집 확인) |
| `portfolio_holdings.py sync`(일반/ISA 계좌) | `TTTC8434R`(실전)/`VTTC8434R`(모의) | 계좌별 보유종목·수량·평균단가·평가금액·손익률 | `sources/portfolio-holdings.csv` | ✅ 검증 |
| `portfolio_holdings.py sync`(연금 계좌, IRP/DC) | `TTTC2202R` | 위와 동일(퇴직연금 계좌 전용 TR) | 〃 | ✅ 검증 |

**"⚠ 미검증" 항목을 실제로 쓸 때**: 각 커맨드에 `--raw` 플래그를 붙이면
파싱 없이 원본 JSON을 그대로 출력한다 — 응답 필드명이 스크립트 상단의
`*_FIELDS` 딕셔너리와 다르면 거기만 고치면 된다(값을 지어내지 않기
위해, 예상 필드가 없으면 스크립트가 조용히 넘어가지 않고 에러로
멈추도록 이미 구현돼 있음).

## 2. 조사 완료, 아직 미구현 — 필요해지면 바로 참고

출처: `stevekoo-ai/open-trading-api`(KIS 공식 예제 저장소) `examples_llm/`
디렉터리. 아래 파일 경로는 그 저장소 기준.

### 2-1. 대차거래(공매도 잔고의 대체 지표)

- **`daily_loan_trans()`** — TR `HHPST074500C0` — `domestic_stock/daily_loan_trans/`
  종목별 일별 대차거래추이 — 당일 잔고 주수·금액. KRX의 "공매도 잔고 공시"(0.5%+ 보유분) 자체는 이 저장소에서 못 찾았고, 이게 가장 가까운 프록시.

### 2-2. 배당·기업행사 캘린더 (예탁원정보, `ksdinfo_*` 계열)

전부 `domestic_stock/ksdinfo_*/` 아래, TR은 `HHKDB669xxxC0` 패턴. 전부 날짜+종목코드 형태의 일정표를 반환(자유 텍스트 아님).

| 함수 | TR ID | 내용 |
| --- | --- | --- |
| `ksdinfo_dividend` | `HHKDB669102C0` | 배당일정(배당락일·지급일 등) |
| `ksdinfo_bonus_issue` | `HHKDB669101C0` | 무상증자일정 |
| `ksdinfo_paidin_capin` | `HHKDB669100C0` | 유상증자일정 |
| `ksdinfo_merger_split` | `HHKDB669104C0` | 합병/분할일정 |
| `ksdinfo_cap_dcrs` | `HHKDB669106C0` | 자본감소(감자)일정 |
| `ksdinfo_list_info` | `HHKDB669107C0` | 상장정보일정 |
| `ksdinfo_pub_offer` | `HHKDB669108C0` | 공모주청약일정 |
| `ksdinfo_sharehld_meet` | `HHKDB669111C0` | 주주총회일정 |
| `ksdinfo_purreq` | `HHKDB669103C0` | 주식매수청구일정 |
| `ksdinfo_forfeit` | `HHKDB669109C0` | 실권주일정 |
| `ksdinfo_rev_split` | `HHKDB669105C0` | 액면교체일정 |
| `ksdinfo_mand_deposit` | `HHKDB669110C0` | 의무예치일정 |

**참고**: 자사주 매입/처분 공시는 이 저장소 어디에도 없었다 — KIS가 아니라 DART(금융감독원 전자공시)가 필요한 영역.

### 2-3. 공매도·목표가 랭킹 (시장 전체 상위 종목)

- **`short_sale()`** — TR `FHPST04820000` — `domestic_stock/short_sale/` — 국내주식 공매도 상위종목(시장 전체 랭킹)
- **`credit_balance()`** — TR `FHKST17010000` — `domestic_stock/credit_balance/` — 신용잔고 상위종목(시장 전체 랭킹, 융자/대주 구분)
- **`dividend_rate()`** — TR `HHKDB13470100` — `domestic_stock/dividend_rate/` — 배당률 상위종목

### 2-4. 뉴스/속보

- **`news_title()`**(국내) — TR `FHKST01011800` — `domestic_stock/news_title/` — 종합 시황/공시 제목, 종목코드·날짜·키워드로 필터
- **`news_title()`**(해외) — TR `HHPSTH60100C1` — `overseas_stock/news_title/`
- **`brknews_title()`**(해외 속보) — TR `FHKST01011801` — `overseas_stock/brknews_title/`

### 2-5. 해외 지수 (SOX·나스닥 등, 미국장 확인용)

- **`inquire_daily_chartprice()`** — TR `FHKST03030100` — `overseas_stock/inquire_daily_chartprice/` — 해외 지수/환율 일·주·월·년봉. `fid_cond_mrkt_div_code="N"`
- **`inquire_time_indexchartprice()`** — TR `FHKST03030200` — `overseas_stock/inquire_time_indexchartprice/` — 해외지수 분봉
- **⚠ 심볼 미확인**: SOX(필라델피아 반도체지수)·나스닥종합의 정확한 KIS 심볼 문자열은 예제 코드에서 확정하지 못함 — `stocks_info/overseas_index_code.py`(마스터파일 `frgn_code.mst` 파싱)로 먼저 조회해야 함. 구현 시 이 조회부터 선행할 것.
- 업종 프록시: **`industry_theme()`** — TR `HHDFS76370000` — `overseas_stock/industry_theme/` — 거래소+업종코드로 그 섹터 전체 시세(나스닥 반도체 업종 스냅샷 대용 가능)

### 2-6. 실시간 체결가/호가 (웹소켓, 폴링 아님)

국내: `ccnl_krx`/`ccnl_nxt`(TR `H0STCNT0`, 실시간체결가), `asking_price_krx`/`asking_price_nxt`(TR `H0STASP0`, 실시간호가), `exp_ccnl_krx`(실시간 예상체결). REST 폴링형 대안: **`inquire_asking_price_exp_ccn()`** — `domestic_stock/inquire_asking_price_exp_ccn/` — 호가+예상체결 스냅샷 1회 조회.

해외: `asking_price`(TR `HDFSASP0`, 미국은 무료·아시아는 유료), `delayed_asking_price_asia`(TR `HDFSASP1`, 아시아 지연호가 무료).

**현재 이 저장소의 3회 배치 체크(07/10/19시)와는 성격이 안 맞음** — 실시간 스트림을 상시 구독해야 의미가 있어서, 지금의 "하루 몇 번 스냅샷" 구조에 넣으려면 별도 아키텍처가 필요.

### 2-7. 금리·채권

- **`comp_interest()`** — TR `FHPST07020000` — `domestic_stock/comp_interest/` — 금리 종합(콜금리·CD·국고채 등, `domestic_stock` 폴더에 있지만 사실상 매크로 지표) — 지금은 FRED/ECOS로 미국·한국 금리를 이미 수집 중이라 우선순위 낮음, 국내 세부 금리(회사채 등)가 추가로 필요해지면 참고.
- `domestic_bond/` 폴더 전체를 아직 깊게 조사하지 않음 — 채권 수익률 관련 TR이 더 있을 가능성 있음(미확인, 필요시 재조사).

### 2-8. ETF 구성종목·NAV 추이 (보유 ETF 심층분석용)

- **`etfetn.inquire_component_stock_price()`** — TR `FHKST121600C0` — ETF 구성종목 상세시세(보유 ETF가 실제 뭘 담고 있는지 확인)
- **`etfetn.nav_comparison_daily_trend()`** — TR `FHPST02440200` — NAV 대비 시장가 일별 추이(최대 100일)

## 3. 우선순위 판단 메모

다음에 API 확장이 또 필요해지면 이 순서로 검토:
1. **해외지수(SOX) 심볼 확인 후 구현** — 미국장 섹션을 매번 웹검색하는 대신 API로 대체 가능해짐(가장 임팩트 큼)
2. **`ksdinfo_dividend`** — 배당 일정은 이미 보유 중인 배당형 ETF와 SK하이닉스 자체 배당 추적에 유용
3. **`daily_loan_trans`(대차거래)** — 공매도 잔고 프록시로 `short-sale`(체결 기준)을 보완

## Sources

- [stevekoo-ai/open-trading-api](https://github.com/stevekoo-ai/open-trading-api) — KIS 공식 Open API 예제 저장소(2026-07-31 조사)
- [scripts/investor_flow.py](../../scripts/investor_flow.py), [scripts/portfolio_holdings.py](../../scripts/portfolio_holdings.py)
- [PR #39](https://github.com/stevekoo-ai/Repo_name/pull/39) — 신용잔고·지수·공매도·ETF NAV 구현, main 병합 완료
- [concepts/market-cycles-leverage-risk.md](market-cycles-leverage-risk.md) "1-4-1" — 신용잔고 데이터 활용처
- [entities/automation-infrastructure.md](../entities/automation-infrastructure.md) — 시크릿·워크플로우 전체 목록
