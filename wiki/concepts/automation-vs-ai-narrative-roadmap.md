---
title: 자동화 vs AI 서술 — SK하이닉스 데일리 체크 로드맵
created: 2026-08-05
updated: 2026-08-06
tags: [automation, architecture, roadmap, sk-hynix, peos, api]
---

# 자동화 vs AI 서술 — SK하이닉스 데일리 체크 로드맵

## 배경 (사용자 요청, 2026-08-05)

> "일단 내가 원하는 방향은 Github에서 자동으로 수집하고 간단한 계산을 해서
> 적절한 텍스트를 출력하는 코딩을 고도화하는 것이다. AI의 웹서치와 LLM
> 자연어 지원을 최소화하려고한다. 그래서 네가 없어도 꽤 훌륭한 자동화
> 툴이 완성될 수 있도록 진행해줘."

현재 SK하이닉스 데일리 체크(아침 07:00/장초반 10:00/저녁 19:00, 매일 자동
루틴)는 다수 섹션에서 **AI 웹검색 + LLM 자연어 서술**에 의존한다. 사용자는
이를 **GitHub Actions 기반 API 자동수집 → 규칙기반 계산 → 템플릿 텍스트
출력**으로 대체해, Claude 세션 없이도 리포트가 완성되는 구조로 전환하고
싶어한다. 이 페이지는 그 방향성 조사 결과와 로드맵을 기록한다.

## 핵심 발견: 이미 이 철학의 절반은 구현돼 있다

이 저장소는 사실 **두 개의 서로 다른 성숙도를 가진 시스템**이 공존한다:

1. **PEOS 파이프라인**(`engine/`, `collectors/`, `main` 브랜치) — ECOS/KOSIS/
   FRED API → 지표 계산 → 룰엔진 스코어링 → 마크다운/HTML 렌더링까지
   **완전히 LLM-free**로 이미 동작 중. `engine/rule/engine.py`가 threshold
   기반 채점을, `engine/report/markdown.py`·`html.py`가 템플릿 렌더링을
   담당한다. 이게 사용자가 원하는 아키텍처의 정확한 선례다.
2. **`scripts/investor_flow.py`** — KIS Open API로 8개 TR(수급/신용잔고/
   공매도/지수/ETF NAV/ADR 등)을 이미 실계정 검증까지 마친 상태로 수집
   중. 원칙("숫자를 지어내지 않는다", "필드 없으면 즉시 에러", "API 우선·
   웹검색은 보완")이 코드 주석에 명문화돼 있다.
3. 반면 **SK하이닉스 데일리 체크 프롬프트**(자동 루틴 3개)는 이 CSV들을
   Claude가 매번 읽어서 **서술 문장으로 손수 재구성**하는 방식이고, 여기에
   더해 HBM ASP·엔비디아 주문·CXL·트럼프 트래커·국제매체 교차검증 같은
   섹션은 전적으로 AI 웹검색+해석에 의존한다.

즉 문제는 "자동화 인프라가 없다"가 아니라 **"있는 자동화 인프라와 리포트
서술 계층 사이에 다리가 없다"**는 것 — 1단계 작업은 이 다리를 놓는 것이다.

## 항목별 자동화 가능성 평가 (2026-08-05 웹조사 기준)

### 🟢 즉시 가능 — 데이터 이미 CSV로 존재, 템플릿만 필요

| 항목 | 데이터 소스 | 비고 |
|---|---|---|
| 본주 가격/등락률/거래량/외국인보유율/드로다운 | `sources/sk-hynix-price-snapshot.csv` | KIS TR FHKST01010100, 검증완료 |
| 외국인/기관/개인 1·5·20·60일 누적 수급 | `sources/sk-hynix-investor-flow.csv` | KIS TR FHKST01010900 |
| ADR 가격+크로스체크 | `sources/sk-hynix-adr-quote.csv` | KIS TR HHDFS76240000, 3방법 크로스체크 로직 이미 존재 |
| 신용융자잔고 | `sources/sk-hynix-credit-balance.csv` | KIS TR FHPST04760000 |
| 공매도 추이 | `sources/sk-hynix-short-sale.csv` | KIS TR FHPST04830000 |
| 코스피/코스닥 지수+상한/하한종목수 | `sources/kr-index-quote.csv` | KIS TR FHPUP02100000 |
| ETF NAV/괴리율 | `sources/portfolio-etf-nav.csv` | KIS TR FHPST02400000 |
| 포트폴리오 보유종목 평가금액 | `sources/portfolio-holdings.csv` | KIS API, 매일 19:10 자동 |
| 매크로 10대 지표 + G/I/L 국면 | PEOS(`report/*.md`) + `scripts/regime_engine.py` | 이미 완전 자동, LLM 없음 |
| HBM Cycle Score 6축 중 **외국인수급(15점)·보유율(15점)** | 위 investor-flow/price-snapshot CSV | 6축 중 30/100점은 이미 100% 자동 가능 |

→ **HBM Cycle Score 산정식 자체도 완전히 코드화 가능한 가중합 공식**이다
(`hbm-cycle-score.md` "1. HBM Cycle Score" 참고: 외국인수급15+보유율15+
ASP25+엔비디아&CoWoS25+공급확대10+고객재고10=100점, 등급 임계값도 명시돼
있음). 지금은 Claude가 매일 6축을 손으로 채점하지만, **데이터가 CSV로
있는 2축은 파이썬 함수 하나로 완전 대체 가능.**

### 🟡 신규 API 통합으로 부분 자동화 가능 (검증 필요)

| 항목 | 후보 API | 상태 |
|---|---|---|
| 반도체 수출 YoY (현재 `manual_inputs/exports.yaml` 수기입력) | data.go.kr(관세청/MOTIE 데이터셋), `DATA_GO_KR_KEY` 이미 보유 | 데이터셋 존재 여부 미확인 — 다음 조사 대상 |
| 하이퍼스케일러(구글/MS/아마존/메타) CapEx 실측치 | **SEC EDGAR XBRL Company Facts API** | ✅ 인증 불필요·완전 무료 확인됨. `data.sec.gov/api/xbrl/companyconcept/CIK.../us-gaap/CapitalExpenditures...json` 으로 분기 실측 CapEx 직접 수집 가능 — 지금 "재고 센티먼트 점수 0~10"으로 손수 매기는 것 중 최소한 "CapEx가 실제로 얼마 늘었나"는 숫자로 완전 대체 가능 |
| 트럼프 2026 중간선거 확률(현재 뉴스서술+기호 방식) | Polymarket (공개 무료 확률 데이터, 공식 REST API 문서는 불명확하나 서드파티 래퍼 다수 존재) | 뉴스 해석을 "실시간 확률 %" 숫자로 치환 가능한 유망 후보 — 검증 필요 |
| 애널리스트 목표가 컨센서스(현재 매일 웹검색) | KIS 국내주식 API에 목표주가/투자의견 TR이 있는지 미확인 / FnGuide FnSpace(부분 유료 추정) / FMP·Finnhub는 한국 종목 커버리지 낮음 | 가장 불확실한 항목 — KIS Developers 포털 직접 확인 필요 |

### 🔴 구조적으로 자동화가 어려움 (본질이 뉴스 해석/의견)

| 항목 | 이유 |
|---|---|
| HBM ASP 주간 %변화 (Cycle Score 25점 배점, 최대 비중 축) | TrendForce/DRAMeXchange 데이터는 유료 구독 전용. 무료 대안(Agentic Sciences Memory Price Index)도 공식 API 없이 웹UI만 제공 — 스크래핑은 가능하나 구조 변경에 취약 |
| 엔비디아 주문량/TSMC CoWoS 활용률 (25점, 최대 비중 축) | 애초에 "공식 발표 수치"가 아니라 업계 루머·애널리스트 체크 기반 지표. TSMC 분기 HPC 매출비중(%)은 SEC 6-K로 공식 확인 가능하지만(후행지표), "CoWoS 활용률"이라는 선행성 지표 자체는 비공개 |
| 공급확대(CXMT 등 경쟁사 동향, 10점) | 뉴스/기업 발표 해석이 본질 |
| 고객재고 센티먼트(어닝콜 논조 판단, 10점) | CapEx 금액 자체는 🟡로 자동화 가능하나, "inventory/digestion/pause" 키워드의 긍정·부정 논조 판단은 키워드 카운팅으로 근사할 수는 있어도 정확도가 낮음 |
| CXL/차세대 메모리 연구 동향 | 논문·뉴스 해석이 본질 |
| 국제매체 교차검증 | 뉴스 해석이 본질 |
| 트럼프 트래커의 세부 항목별 서술(정책 발표 해석 등) | 확률 수치화(Polymarket)는 가능해도 "정책 시사점 서술"은 해석 영역 |

**HBM Cycle Score 관점에서 보면**: 6축 100점 중 자동화 가능한 건 외국인
수급+보유율(30점)뿐이고, 최대 비중인 ASP(25점)·엔비디아&CoWoS(25점)는
구조적으로 뉴스 해석 의존이 계속된다. 즉 이 특정 스코어는 **LLM 개입을
완전히 제거할 수 없다** — 다만 6축 중 2축, HBM Cycle Score 외 나머지
리포트 섹션(가격/수급/신용/공매도/지수/포트폴리오/매크로/거시국면)은
거의 전부 템플릿화 가능하다.

## 제안 로드맵 (3단계)

### 1단계 — 텍스트 생성기 구축 (즉시 착수, 코드는 대부분 이미 존재)
`scripts/investor_flow.py`의 각 `kis_fetch_*` 함수에 `--report` 형태의
마크다운/HTML 조각 출력 모드를 추가하거나, 별도 `scripts/report_sections.py`
를 신설해 CSV → 완성 문장을 룰 기반으로 뽑아낸다. 예:
```
📊 외국인 수급: 20일 누적 -5.30조원(어제 대비 +5.24조 개선),
   금일 순매수 +3조 5,883억원(KIS API 수집 이래 최대)
```
같은 문장을 f-string 템플릿 + 조건 분기(개선/악화, 역대급 여부 등 threshold
비교)로 완전 대체. **HBM Cycle Score의 외국인수급·보유율 두 축도 이 단계에서
자동 채점기로 전환** — PEOS의 `engine/rule/engine.py` 패턴을 그대로 재사용.

### 2단계 — 신규 API 통합
- SEC EDGAR: `collectors/sec_edgar.py` 신설, 4대 하이퍼스케일러 CIK 매핑 +
  `CapitalExpenditures` 태그 분기값 자동 수집 → "고객재고" 축의 정량 근거
  절반 확보
- data.go.kr: 반도체 수출 데이터셋 탐색 (`DATA_GO_KR_KEY` 이미 보유)
- Polymarket: 트럼프 트래커의 확률 부분만 수치화 자동 전환 시도
- KIS 목표주가/투자의견 TR 존재 여부 포털 직접 확인

### 3단계 — 하이브리드 구조로 명시적 분리
완전자동화가 어려운 항목(HBM ASP·엔비디아루머·CXL·국제매체·목표가 근거
서술)은 "AI 웹검색 필요" 섹션으로 리포트 구조 자체에서 명시적으로 분리.
나머지는 전부 코드 생성 텍스트로 전환해, 최종적으로 리포트의 상당 부분이
Claude 세션 없이도(GitHub Actions 크론만으로) 생성 가능한 상태를 목표로 한다.

## 진행 상황 (2026-08-05/06 갱신)

사용자 결정: **1단계+2단계(SEC EDGAR) 동시 착수**, 아키텍처는 **`scripts/`
스타일 확장 유지**(PEOS `engine/` 계층 이식 안 함) — 아래 완료.

### ✅ 1단계 완료 — `scripts/daily_report.py` 확장

기존에 이미 시세·외국인보유율·ADR·투자자별순매수·붕괴조건④를 다루고 있던
`build_report()`에 5개 섹션을 신규 추가(`scripts/investor_flow.py`에 리더
헬퍼 8개 신설: `read_price_snapshot_rows`·`foreign_hold_pct_trend`·
`read_credit_balance_rows`·`credit_balance_streak`·`read_latest_short_sale`·
`read_latest_index`):
- **HBM Cycle Score 외국인수급·보유율 2축(30/100점) 초안 자동채점** —
  `score_foreign_flow_axis()`(20일 누적 부호8점+5일모멘텀4점+당일부호3점),
  `score_foreign_holding_axis()`(전일대비%p10점+5일평균추세5점). ⚠ 세부
  배점은 hbm-cycle-score.md에 공식 문서화된 적 없는 **초안** — 사람이
  매일 정성판단하던 걸 재현 가능한 규칙으로 처음 코드화한 것, 검증/조정 필요.
- 신용융자잔고 연속증감 판정(`credit_balance_streak`, N거래일 연속 자동 카운트)
- 공매도 추이, 코스피/코스닥 지수(+상한/하한종목수), 포트폴리오 평가금액
  (계좌별 SK하이닉스 비중 자동계산, 데이터 없으면 섹션 자체 생략)

**검증**: 저장소에 이미 커밋된 실제 CSV로 end-to-end 실행 확인 —
신용융자잔고 "3거래일 연속 감소"(2026-08-04 기준) 등 그동안 사람이 CSV를
눈으로 훑어 손으로 도출하던 판정과 일치. 산출물:
`sources/sk-hynix-auto-report-2026-08-06-0843.md`.

### ✅ 2단계 착수 — `scripts/sec_edgar_capex.py` 신설

SEC EDGAR XBRL Company Concept API로 4대 하이퍼스케일러(GOOGL/MSFT/AMZN/META)
분기 CapEx 실측치 자동 수집. CIK 4개(1652044/789019/1018724/1326801) 웹조사
교차검증 완료, 응답 JSON 구조(units.USD의 val/end/fy/fp/form/filed)도 SEC
공식문서·튜토리얼로 확인. `.github/workflows/sec-edgar-capex.yml` 신설
(주1회 자동 + workflow_dispatch 수동/--raw 진단, ecos-lookup.yml과 동일 패턴).

**⚠ 미검증 상태**: 이 세션 샌드박스는 SEC 도메인 아웃바운드가 막혀 있어
(직접 curl·WebFetch 둘 다 실패 확인) **실호출 테스트를 못 했다** — CIK·JSON
구조는 문서 교차검증했지만, XBRL 태그명(PaymentsToAcquire...)이 회사마다
실제로 맞는지는 GitHub Actions 러너(`workflow_dispatch` + `raw: true`)에서
최초 실행해 확인 필요. 실패 시 CAPEX_TAG_CANDIDATES 보정.

### PR #47 (2026-08-06) — main 반영 ✅ merged

`sec-edgar-capex.yml`이 서사 브랜치에만 있어 Actions 탭에 안 보이는 문제
발견(workflow_dispatch는 default branch에 있어야 등록됨) — CLAUDE.md
"main 직접 커밋 금지" 규칙에 따라 `main` 기준 새 브랜치(`feat/sec-edgar-capex`)
분리 후 자동화 관련 4개 파일만 PR로 이관: https://github.com/stevekoo-ai/Repo_name/pull/47
(위키/서사 파일은 제외 — CLAUDE.md 브랜치 분리 원칙 유지). base(main)와
diff 확인 결과 순수 추가 diff(충돌 없음). **2026-08-06 merge 완료**,
GitHub Actions API로 "SEC EDGAR Hyperscaler CapEx"(id 328256655, active)가
`main`에 정상 등록됨을 재확인.

### 403 발견 + PR #48 (2026-08-06) — User-Agent 이메일 형식 누락 ✅ merged

merge 후 raw:true 최초 실행 결과 4개사 전부 **403 "Undeclared Automated
Tool"**([run 31063296132](https://github.com/stevekoo-ai/Repo_name/actions/runs/31063296132))
— 원인은 XBRL 태그명이 아니라 **User-Agent에 이메일 형식이 없었던 것**(SEC
공정접근 정책은 "이름 email@domain.com" 형식을 명시적으로 요구, 단순 식별
문자열로는 부족). 개인 이메일을 공개 저장소 코드에 커밋하지 않기 위해
`SEC_EDGAR_CONTACT` GitHub Secret으로 주입하도록 수정 →
https://github.com/stevekoo-ai/Repo_name/pull/48, **2026-08-06 merge 완료**.

### 재실행 삽질 + PR #49 (2026-08-06) — GMAIL_ADDRESS 재사용으로 시크릿 단순화 ✅ merged

PR #48 merge 후 사용자가 재실행했으나 여전히 403 — 원인 분석 결과 **"Re-run
failed jobs" 버튼이 PR #48 merge 이전 커밋(같은 run id, attempt 2)을 다시
돌린 것**이었음(새 dispatch가 아니었음). 이 과정에서 사용자가 신규 시크릿
등록 대신 **이미 있는 `GMAIL_ADDRESS` 시크릿 재사용을 제안** — 워크플로의
env를 `SEC_EDGAR_CONTACT: "PEOS-research ${{ secrets.GMAIL_ADDRESS }}"`로
변경해 반영: https://github.com/stevekoo-ai/Repo_name/pull/49, **2026-08-06
merge 완료**.

### ✅ 2단계 완전 검증 완료 (2026-08-06)

merge 직후 `raw:true` 재실행 → **성공**. 로그로 확인: Meta(CIK 1326801,
entityName "Meta Platforms, Inc.")에서 `CAPEX_TAG_CANDIDATES` 1번째 후보
(`PaymentsToAcquirePropertyPlantAndEquipment`)가 그대로 매칭 — 4개사 전부
fallback 태그 없이 1번째 태그로 해결됨. 이어서 정식 모드(raw 아님)도
`actions_run_trigger`로 직접 실행해 **`sources/hyperscaler-capex.csv`에
실측 데이터 커밋 완료** — 예: GOOGL 2025Q3 CapEx $63.6B, MSFT FY2026Q3
$47.5B, META 2025Q2 $29.5B(모두 SEC 정식 공시 기준). 이걸로 2단계
(하이퍼스케일러 CapEx 자동수집)는 **완전히 동작 확인된 상태** — 매주
월요일 21:00 UTC 자동 갱신, 수동 실행도 가능.

### ⚠️ SEC EDGAR 데이터 정합성 버그 발견·수정 (2026-08-06, "숙제 점검" 중 발견)

위 "완전히 동작 확인된 상태"라는 판정은 **"API 호출이 성공하고 숫자가
CSV에 들어왔다"까지만 검증한 것**이었다 — 사용자가 "숙제 다 했는지" 재점검을
요청해 daily_report.py에 실제로 연결하려던 중, 커밋된 `hyperscaler-capex.csv`를
자세히 들여다보니 두 가지 실제 문제를 발견:

1. **같은 분기가 다른 fiscal_year/fiscal_period로 중복 저장됨**: SEC의
   companyconcept API는 한 분기(예: GOOGL 2025-03-31 마감)가 **나중 필링의
   "전년동기 비교치"로 다시 보고될 때 그 나중 필링의 fy/fp를 붙여서** 내려주는
   경우가 있다 — 이전 코드는 upsert 키가 `(ticker, fiscal_year,
   fiscal_period)`였는데, 같은 분기가 "2025Q1"과 "2026Q1"이라는 서로 다른
   키로 각각 저장돼 **가짜 중복 행**이 생겼다(GOOGL·META·MSFT 3사 전부에서
   확인, 19행 중 5행이 중복).
2. **MSFT 한 분기(2025-03-31 마감)에서 진짜 값 충돌**: 같은 end_date인데
   한쪽 필링은 $16.7B, 다른 쪽은 $47.5B — **위 "MSFT FY2026Q3 $47.5B"로
   인용했던 수치가 실은 이 충돌 중 한쪽이었다**(어느 쪽이 맞는지는 이
   세션에서 재확인 못함, 아래 참고). 이전 코드는 어느 쪽이 진짜인지 검증
   없이 최신 fy/fp로 보이는 쪽을 그대로 썼다 — 이 위키·roadmap 문서에
   "검증 완료"로 인용했던 이 특정 수치는 **정정 필요**로 낮춘다.
3. **AMZN이 2017-03-31 마감 분기에서 멈춰있음**(9년 전) — 첫 성공한 후보
   태그(`PaymentsToAcquirePropertyPlantAndEquipment`)에서 데이터를 찾으면
   바로 멈추고 나머지 후보 태그를 시도하지 않던 게 원인으로 추정(Amazon이
   최근엔 다른 태그를 쓸 가능성). 재검증은 SEC 라이브 접속이 필요.

**수정한 내용** (`scripts/sec_edgar_capex.py`):
- upsert 키를 `(ticker, fiscal_year, fiscal_period)` → **`(ticker,
  end_date)`**로 변경 — end_date가 진짜 분기 식별자, fy/fp는 필링마다
  달라질 수 있어 신뢰 불가.
- 같은 end_date에 값이 다르면(진짜 충돌) **가장 먼저 제출된(filed 이른)
  값을 채택하되, 다른 값도 새 `note` 컬럼에 남긴다** — investor_flow.py의
  ADR crosscheck MISMATCH와 동일한 원칙(조용히 하나를 버리지 않음).
- 첫 성공 태그에서 멈추지 않고 **후보 태그 전부를 조회해 합친다** — 회사가
  최근 다른 태그로 바꿨을 가능성을 놓치지 않기 위함.
- 기존 CSV(19행)를 이 로직으로 로컬 재처리해 14행으로 정리, MSFT 충돌은
  `note`에 명시적으로 남겨둠(`sources/hyperscaler-capex.csv` 참고).

**⚠️ 아직 남은 문제 — 이 세션은 검증 못 함**: 위 표에 정리했듯 4개사
전부 end_date가 150일 이상 지나 스테일(GOOGL 310일·MSFT 218일·AMZN
3,415일·META 402일, 2026-08-06 기준) — 이 세션은 SEC 도메인 아웃바운드가
막혀 있어(WebFetch도 403 확인) **재조회로 진짜 최신 분기를 직접 확인하지
못했다**. `daily_report.py`에는 스테일 여부를 자동 판정해 "⚠ 재조회
필요" 라벨을 붙이도록만 반영(아래 참고) — 다음으로 필요한 건 **이 수정을
PR #51로 main에 올린 뒤(https://github.com/stevekoo-ai/Repo_name/pull/51,
병합 대기) GitHub Actions로 실제 재실행**(SEC 접속이 되는 러너에서),
MSFT 충돌 값 중 어느 쪽이 맞는지, AMZN이 정말 최신 데이터가 없는지,
GOOGL 등 나머지 3사도 2025-09/12월 이후 분기가 실제로 없는지(있는데
못 가져온 건지) 확인하는 것.

### 🆕 3단계 착수 — 체크 프롬프트를 실제로 자동화 인프라에 연결 (2026-08-06)

사용자 질문("자동화로 데이터를 미리 가져오면 토큰 사용량이 줄어들어?")에 대한
답: **부분적으로만** — 🟢 자동화 가능 섹션은 GitHub Actions가 미리 계산해두면
그 부분 토큰은 0이거나(Claude 미호출) 최소화되지만(CSV 원본 대신 완성된
한 줄만 인용), 🔴 뉴스해석 섹션(HBM ASP·엔비디아&CoWoS·CXL·국제매체·트럼프
서술·목표가 근거)은 여전히 웹검색+판단이 본질이라 줄지 않는다. 특히 HBM Cycle
Score 최대비중 두 축(ASP25+엔비디아25=50점)이 여기 해당돼 절반은 못 줄인다.
**핵심 병목 발견**: 인프라(`daily_report.py`, `sec_edgar_capex.py`)는 이미
완성·실전검증됐는데, 하루 3회 도는 체크 프롬프트 자체가 그동안 이를 안 쓰고
CSV를 직접 열어 재계산하거나 웹검색으로 재확인하고 있었다 — 이게 진짜 낭비.

**아침(07:00 KST) 트리거 수정 완료**(`trig_01CCKjPS2YWUVDsJQv1X4Av1`,
`update_trigger`로 반영): 신설 단계 "1-2"에서 `python3 scripts/daily_report.py
--ticker 000660`을 먼저 실행하고 그 출력을 시세/외국인보유율/ADR/투자자별
순매수/붕괴조건④/HBM 외국인축2개/신용융자잔고/공매도/코스피코스닥지수/
포트폴리오평가금액의 1차 근거로 그대로 인용하도록 지시, 기존 2-4(외국인
수급)·2-1(하이퍼스케일러 CapEx FACT)·3-1(HBM 2축)·3-2(포트폴리오) 단계에
"재계산·재검색 대신 1-2 출력 재사용" 포인터 삽입. 🔴 항목은 원래 지시 그대로
유지(수정 안 함).

**장초반(10:00)·저녁(19:00) 트리거는 아직 미착수** — 이 세션은 두 트리거의
정확한 현재 프롬프트 원문을 갖고 있지 않아(list_triggers API가 prompt 필드를
반환하지 않음, 이 대화 안에서 두 트리거가 실제 발동한 메시지도 없었음),
추측으로 전체 덮어쓰기하면 각 루틴 고유 내용(예: 저녁의 "카테고리별 타임라인
본격 갱신" 담당 문구 등)을 날릴 위험이 있어 보류 — 사용자 확인 후 진행
(선례: 2026-08-05 09:3x 세션은 실제 발동 메시지를 대조해 재구성했음, 이번엔
그 메시지가 이 대화 컨텍스트에 없음).

### 🆕 "숫자를 의미화"하는 업계 기법 조사 (2026-08-06, 사용자 요청)

사용자 요청("데이터 숫자를 의미화하는 방식에 대해 더 좋은 방법이 있는지 조사") —
🔴로 분류했던 항목 일부가 실은 완전자동화까진 아니어도 **더 나은 방법론**으로
개선 가능함을 웹조사로 확인. 4가지 확립된 기법 + 2개 구체적 신규 데이터 후보:

**A. 템플릿 기반 NLG(Natural Language Generation)** — AP통신이 Automated
Insights(Wordsmith)로 분기당 3,000+건의 실적 기사를 LLM 없이 생성(구조화
데이터→사전정의 템플릿 채우기, 결정론적·감사가능). 이미 우리가 daily_report.py로
하고 있는 방향이 업계 표준과 일치함을 확인 — 새 발견이라기보단 **검증**.

**B. CNN Fear & Greed Index 방법론(z-score/percentile 정규화)** — 7개 지표를
각각 "252일 이동평균 대비 얼마나 벗어났는지"로 정규화한 뒤 0~100 스케일로
합산, 균등가중. **HBM Cycle Score의 지금 배점 방식(8/4/3점 임의 구간)보다
통계적으로 더 방어 가능한 대안** — 고정된 매직넘버 대신 과거 분포 대비
표준편차로 자동 보정되는 방식이라, 국면이 바뀌어도 임계값을 손으로 재조정할
필요가 줄어든다.

**C. Loughran-McDonald 금융 특화 감성사전 + 무료 실적콜 원문(Motley Fool)** —
2011년 학계에서 개발된 재무 텍스트 전용 사전(negative/positive/uncertainty/
litigious 등 6개 카테고리), 어닝콜 톤 분석에 검증된 실적. Motley Fool이
S&P500 어닝콜 전문을 무료 공개 — 두 개를 결합하면 **"고객재고 센티먼트
0~10점"을 LLM 없이 사전 기반 단어 카운팅으로 근사 가능**(🔴→🟡 격상 후보).
단, 룰 기반 사전이 LLM 판단보다 뉘앙스가 거칠다는 명백한 품질 트레이드오프 있음.

**D. AgenticSciences memory-price-tracker(GitHub, DRAM/NAND/HBM 가격)** —
로드맵 최초 조사 때 "웹UI만 있고 API 없음"으로 판단했던 게 재확인 결과
**GitHub 저장소에 JSON으로 실제 존재**(`verified_memory_data.json`), 항목마다
`verified: true/false` + `verification_method`(예: "DRAMeXchange 직접
스크레이프") 필드로 실측/예측 구분 명시 — raw.githubusercontent.com으로
직접 fetch 가능. **HBM ASP(Cycle Score 최대비중 25점) 자동화 후보**(🔴→🟡
격상 후보). ⚠ 단, 이 프로젝트 자체가 DRAMeXchange 3자 스크레이프이지
1차 공식 출처가 아니라 신뢰도 등급은 낮게(data/manual_inputs/semiconductor.yaml의
"반도체 예외 정책 grade cap 3"과 동일하게) 잡아야 하고, 일부 필드는
"market pattern simulation between points"(포인트 사이 보간)를 쓴다고
README에 명시돼 있어 verified=true 항목만 골라 써야 함.

**E. Z-score/percentile 기반 이상치("역대급") 탐지** — 이미
`credit_balance_streak()`에서 부분 구현한 "N일 연속 증감" 패턴을, 표준편차
기준(z≥3 등)으로 일반화하면 "역대급 순매수", "이례적 낙폭" 같은 판단도
사람 손 없이 자동 플래그 가능. daily_report.py의 여러 섹션에 공통 적용 가능한
범용 유틸리티.

### ⚠️ D·C 정정 (2026-08-06, 실제 데이터 열람 후)

사용자가 A~E 전부(B/C/D/E, D는 "추천"으로 선택)를 채택해 구현 착수했으나,
**착수 전 실제 소스를 열어본 결과 D·C는 처음 조사에서 과대평가했음이
드러났다** — 정정 기록.

- **D (AgenticSciences memory-price-tracker) — HBM ASP 자동화 후보로서
  기각.** `verified_memory_data.json` 전체를 직접 열람한 결과 **HBM 항목이
  0건**(DDR4/DDR5 DRAM 현물가, GPU 컴퓨트 단가, 역대 최저가 기록,
  TrendForce 예측, 시장 이벤트 타임라인만 존재 — "HBM" 검색 결과 없음).
  게다가 DRAMeXchange 소스의 `last_update` 필드가 "2026-04-17"로, 조사
  시점(2026-08-06) 기준 **약 4개월 정체** — README의 "매주 갱신" 설명과도
  불일치. 최초 웹조사(위 "D." 항목 서술)는 이 두 가지를 확인하지 않고
  README/구조만 보고 낙관적으로 판단한 것 — **과대평가였음을 인정**.
  HBM ASP(Cycle Score 25점, 최대비중 축)는 여전히 🔴(자동화 불가)로 유지.
  일반 DRAM(DDR4/DDR5) 현물가만 필요한 별도 용도가 생기면 재검토 가능하나,
  현재 로드맵의 어떤 항목도 그 범위로 좁혀 쓸 이유가 없어 **보류**.
- **C (Loughran-McDonald + Motley Fool) — 소스 접근 차단으로 미착수.**
  Motley Fool 실적콜 전문 인덱스 페이지(`fool.com/earnings/call-transcripts/`)에
  WebFetch 시도 시 **403(봇 차단)**. 사전(Loughran-McDonald) 자체는 여전히
  유효한 방법론이지만, 이 세션에서 확보 가능한 무료 실적콜 원문 소스가
  없어 "고객재고 센티먼트" 축 자동화는 **당장은 착수 불가** — 대체 무료
  전문(transcript) 소스를 찾거나(예: 기업 IR 페이지 직접, SEC 8-K 첨부),
  사용자가 우선순위를 낮추면 로드맵에서 보류.

**B·E는 실제로 구현 가능했고 완료함** — 아래 "✅ B·E 구현 완료" 참고.

### ✅ B·E 구현 완료 (2026-08-06)

`scripts/stats_utils.py` 신설(순수 stdlib, `statistics`+`math`만 사용) —
`zscore()`(과거 관측치 대비 표준편차, 표본 5건 미만이거나 무변동이면 `None`),
`percentile_rank()`, `anomaly_label()`(z-score→"역대급/이례적/평이한 수준"
한글 라벨, ±2σ/±3σ 관례 임계값), `logistic_scale()`(z-score를 [0, 만점]
연속 스케일로 로지스틱 압축, CNN Fear&Greed와 동일한 발상).

**B로 적용**: `daily_report.py`의 `score_foreign_flow_axis()`(외국인수급
15점)·`score_foreign_holding_axis()`(보유율 15점)를 개정 — 당일 순매수(3점)·
20일 누적(8점)·전일대비 보유율 변화(10점) 세 구간을 고정 점수구간(8/4/3점
식 이분법) 대신 `logistic_scale(zscore(...))` 연속 스케일로 전환. 모멘텀
(5일vs20일, 4점)과 5일평균추세(5점)는 그 스프레드/표본 자체의 z-score를
내기엔 필요 표본(최소 25영업일 또는 5개 스냅샷 안에서의 재귀)이 부족해
방향 이분법 유지 — 데이터가 쌓이면 전환 예정.

**E로 적용**: 위 B 적용 구간에 `anomaly_label()`을 함께 출력해 "역대급/
이례적" 여부를 자동 플래그. 별도로 신용융자잔고 섹션에 "변화폭 이상치
판정"을 신설 — 연속 증감(`credit_balance_streak`, 방향만 앎)과 별개로
당일 변화폭 크기 자체가 과거 분포에서 얼마나 벗어났는지 z-score로 판정.

**검증**: 저장소 실제 CSV로 `python3 scripts/daily_report.py --ticker 000660`
end-to-end 실행 — 신용융자잔고 변화폭이 `역대급 하락(z=-3.21σ)`로 정상
플래그됨(방향 이분법("3거래일 연속 감소")만으론 드러나지 않던 크기 정보).
20일 누적 외국인수급은 절대값 기준 순매도(붕괴조건④ 충족)이면서도 과거
분포 대비로는 `z=+1.80σ`(상대적으로 양호한 흐름) — **붕괴조건④(절대
부호 기준)와 z-score(상대 분포 기준)가 다른 질문에 답한다는 걸 실행
결과로 확인**, 리포트에 두 판정을 모두 남겨 혼동 방지.

### 다음 액션

- [x] 장초반·저녁 트리거도 동일하게 수정 — 2026-08-06 완료(원문 미보유로
      아침 트리거에서 추론 재구성, [messagebox](../messagebox.md) 참고)
- [x] B·E 구현 — 위 참고. C·D는 정정 후 보류
- [x] hbm-cycle-score.md "고객재고" 축에 hyperscaler-capex.csv 실측치
      연결 — 2026-08-06 완료(`daily_report.py`에 `read_hyperscaler_capex()`
      신설). **연결 도중 SEC EDGAR 데이터 정합성 버그 발견·수정**(위
      "⚠️ SEC EDGAR 데이터 정합성 버그" 섹션) — 이전에 "완전 검증 완료"로
      기록했던 게 API 호출 성공까지만이었고 실제 값 정합성은 안 봤던 것으로
      드러남. 지금은 스테일(전부 150일↑ 경과) 상태로 연결돼 있어 다음
      단계는 ↓
- [ ] **위 버그 수정 PR #51 병합 대기 → 병합 후 GitHub Actions 재실행
      필요**(https://github.com/stevekoo-ai/Repo_name/pull/51, SEC 접속이
      막힌 이 세션 대신 Actions 러너에서) — MSFT 값 충돌 중 어느 쪽이
      맞는지, AMZN·GOOGL 등이 정말 최근 분기 데이터가 없는 건지 확인
- [ ] hbm-cycle-score.md에 위 2축(외국인수급·보유율) 초안 배점 규칙 +
      B 개정분(z-score 연속 스케일)을 공식 반영할지 사용자 검토
- [ ] C 대체 실적콜 원문 소스 탐색 또는 보류 확정 — 사용자 우선순위 대기
- [ ] D는 보류 확정(위 정정 참고) — 재검토 트리거 없으면 재착수 안 함
- [ ] data.go.kr 반도체수출, KIS 목표주가 TR, Polymarket 트럼프확률 —
      아직 미착수, 3단계(하이브리드 명시분리) 나머지 포함 사용자 우선순위 대기

## Sources

- 2026-08-05 사용자 요청 (자동화 방향 전환)
- `scripts/investor_flow.py` (8개 KIS TR, 실계정 검증 완료)
- `scripts/daily_report.py` (규칙기반 리포트 조립기, B·E 적용)
- `scripts/stats_utils.py` (z-score/percentile/anomaly_label/logistic_scale, 2026-08-06 신설)
- `scripts/sec_edgar_capex.py`, `.github/workflows/sec-edgar-capex.yml` (2단계 SEC EDGAR 자동수집)
- `engine/rule/engine.py`, `engine/report/markdown.py`, `engine/report/html.py` (PEOS 템플릿 렌더링 선례)
- [hbm-cycle-score.md](hbm-cycle-score.md) "1. HBM Cycle Score" (6축 가중치 공식)
- `data/manual_inputs/semiconductor.yaml` (반도체 신호가 왜 수동 입력인지 근거)
- WebSearch 2026-08-05: SEC EDGAR XBRL API, FMP/Finnhub 목표가 API, DRAM/NAND 무료 데이터, Polymarket, KIS 국내주식 목표주가 TR, TSMC HPC 매출비중, 네이버금융/FnGuide/DART
- 2026-08-06 직접 열람 검증: `raw.githubusercontent.com/AgenticSciences/memory-price-tracker/main/verified_memory_data.json`(D 정정 근거), `fool.com/earnings/call-transcripts/`(C 403 확인)
