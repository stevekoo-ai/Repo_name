---
title: KIS Open API 데이터 카탈로그
created: 2026-07-31
updated: 2026-08-04
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
| `investor_flow.py adr-quote`(기본, 일별) | `HHDFS76240000` | 해외상장(ADR) 종목의 **일별 확정 시세** — 호출 시각과 무관하게 마지막 마감 거래일의 정확한 종가·등락률. **3방법 크로스체크**(rate 필드/diff 재계산/전거래일 이력 대조)가 전부 일치해야 `change_pct`를 확정, 어긋나면 값을 비우고 `crosscheck=MISMATCH`로 CSV에 남김 — 상세는 아래 "ADR 크로스체크" 참고 | `sources/sk-hynix-adr-quote.csv` | ✅ **[PR #40](https://github.com/stevekoo-ai/Repo_name/pull/40) 병합 완료(2026-08-01)** — 부호버그 수정+크로스체크 로직 반영. 단 실계정 API로는 아직 미검증(샌드박스 제약) — 다음 GitHub Actions 실행에서 `--raw`로 `rate` 필드 존재 여부·crosscheck 판정 재확인 필요 |
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

### ADR 크로스체크 (2026-08-01 신설 — 사용자 요청)

사용자가 "ADR이 왜 매번 틀리냐"고 질문한 뒤([체크포인트⑥ 포스트모템](sk-hynix-analyst-thesis-checkpoints.md)
참고), "3가지 방법이 모두 같으면 확정, 안 맞으면 나한테 보고하고 결정은
내가 한다"고 명시적으로 요청 — `kis_fetch_overseas_daily_price()`가
이제 서로 독립적인 3가지 방법으로 등락률을 계산해 대조한다:

- **A) rate** — API가 자체 계산해 주는 등락률 필드(그대로 신뢰하면 위험 — 이게 바로 원래 버그였음)
- **B) calc** — 같은 응답 행의 `diff`(변동폭)·종가로 직접 재계산
- **C) hist** — 같은 API 응답의 전 거래일 확정 종가(`output2[1]`)를 독립적인 전일종가로 삼아 재계산 — `diff`에 전혀 의존하지 않는 유일한 방법이라, A·B가 같은 원인으로 동시에 틀렸을 경우도 걸러낼 수 있음

**판정**: 확보 가능한 방법들(2~3개)이 오차범위(0.1%p) 안에서 일치하면
그 값을 확정치로 채택하고 `sources/sk-hynix-adr-quote.csv`의 `crosscheck`
컬럼에 `OK`(3/3 일치)나 `OK_PARTIAL(2/3)`을 기록. **불일치하면 숫자를
지어내지 않고 `change_pct`를 비워둔 채 `crosscheck=MISMATCH`로 표시**,
`crosscheck_detail` 컬럼에 세 값을 전부 남기고(`rate:-2.08|calc:+2.17|hist:+2.17`
형식) stderr에도 경고를 출력한다. `daily_report.py`의 자동 1차 리포트도
MISMATCH를 크래시 없이 "등락률 미확정, 사용자 확인 필요"로 표시하도록
갱신됨. **이 컬럼을 읽는 사람(또는 Claude 세션)의 역할**: MISMATCH 행을
발견하면 세 값을 그대로 사용자에게 보고하고, 어느 쪽을 최종값으로 쓸지는
사용자가 결정하도록 한다 — 자동으로 어느 한쪽을 골라 확정하지 않는다.
아직 실계정 API 호출로 검증은 못 했음(샌드박스 아웃바운드 차단) — 다음
GitHub Actions 실행에서 `--raw`로 `rate` 필드 존재 여부·`output2[1]`이
실제로 전 거래일인지 재확인 필요.

### 5년 백필 & 외국인보유율의 KIS 구조적 한계 (2026-08-04 신설 — 사용자 요청)

사용자가 "5년치를 KIS API 하나로만 뽑으려니 걸리는 게 있다"며 짚어준
문제를 검증한 결과. 새 스크립트 `scripts/hynix_5y_history.py`(가격/보유율/
merge 3개 서브커맨드)로 정리.

**① 주가는 KIS로 5년치 가능**: `inquire-daily-itemchartprice`(TR
`FHKST03010100`)가 `FID_INPUT_DATE_1/2`로 날짜 range를 받는다 — 1회
호출 최대 ~100건이라 90~100일 창으로 나눠 페이지네이션하면 된다.
✅ `stevekoo-ai/open-trading-api` 공식 예제로 파라미터·필드명 교차검증
완료(`stck_bsop_date`/`stck_oprc`/`stck_hgpr`/`stck_lwpr`/`stck_clpr`/
`acml_vol`/`acml_tr_pbmn`).

**② 외국인 보유율은 KIS 전체를 뒤져도 5년치가 안 된다 — 구조적 한계
확정**. 이번에 3개 경로를 전부 확인했고 셋 다 "최근 30영업일" 벽에
막힌다:
- `inquire-investor`(`FHKST01010900`, `investor_flow.py fetch`가 이미
  씀) — docstring 자체가 "최근 30영업일" 명시, 날짜 range 파라미터 없음
- `inquire-price`(`FHKST01010100`, `investor_flow.py snapshot`이 이미
  씀) — `hts_frgn_ehrt`(외국인 보유율)를 부수 필드로 주지만 "오늘 시점"
  스냅샷 1건뿐
- **🆕 `inquire-daily-price`(`FHKST01010400`)** — 이번에 새로 발견. 일별
  `hts_frgn_ehrt`를 배열로 주긴 하지만 공식 예제 docstring에 "최근
  30거래일(주,월)로 제한되어 있습니다"라고 명시돼 있어 역시 30일 벽.
  (참고로 이 TR과 `inquire-daily-itemchartprice`의 `FID_ORG_ADJ_PRC`
  0/1 의미가 문서상 서로 반대로 보임 — 전자는 "0:수정주가미반영
  1:수정주가반영", 후자는 "0:수정주가 1:원주가". 실사용 전 `--raw`로
  실제 종가 흐름과 대조 확인 권장.)

→ **결론: 외국인 보유율 5년 이력은 KIS 밖에서 구해야 한다.** KRX
정보데이터시스템 Open API(`openapi.krx.co.kr` — 웹 대시보드
`data.krx.co.kr`과 다른 도메인, 흔히 혼동됨)가 유력 후보이나, 이
세션은 두 도메인 모두 아웃바운드 네트워크가 막혀 있어(화이트리스트
프록시) 실호출로 검증 못 함 — `hynix_5y_history.py`의
`foreign-ownership` 서브커맨드는 **엔드포인트·파라미터명·응답
필드명 전부 미검증 추정치**로 작성돼 있다. 서비스 신청 후 실제
명세서로 대조·수정 필요. 대안으로 커뮤니티 라이브러리
`sharebook-kr/pykrx`(비공식 스크래핑 경로, 정식 Open API 아님)도
검토 가능.

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
