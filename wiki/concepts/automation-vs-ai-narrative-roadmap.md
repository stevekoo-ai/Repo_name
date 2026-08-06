---
title: 자동화 vs AI 서술 — SK하이닉스 데일리 체크 로드맵
created: 2026-08-05
updated: 2026-08-05
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

### PR #47 (2026-08-06) — main 반영

`sec-edgar-capex.yml`이 서사 브랜치에만 있어 Actions 탭에 안 보이는 문제
발견(workflow_dispatch는 default branch에 있어야 등록됨) — CLAUDE.md
"main 직접 커밋 금지" 규칙에 따라 `main` 기준 새 브랜치(`feat/sec-edgar-capex`)
분리 후 자동화 관련 4개 파일만 PR로 이관: https://github.com/stevekoo-ai/Repo_name/pull/47
(위키/서사 파일은 제외 — CLAUDE.md 브랜치 분리 원칙 유지). base(main)와
diff 확인 결과 순수 추가 diff(충돌 없음). 구독 중, merge 후 GitHub Actions에서
raw:true 검증 예정.

### 다음 액션

- [ ] PR #47 merge
- [ ] merge 후 GitHub Actions에서 `sec-edgar-capex.yml`을 `raw: true`로 최초 실행 →
      필드명/태그 검증
- [ ] 검증 통과하면 정기 스케줄 가동 확인(주1회, 월요일 21:00 UTC)
- [ ] hbm-cycle-score.md에 위 2축 초안 배점 규칙을 공식 반영할지 사용자 검토
- [ ] data.go.kr 반도체수출, KIS 목표주가 TR, Polymarket 트럼프확률 — 아직 미착수

## Sources

- 2026-08-05 사용자 요청 (자동화 방향 전환)
- `scripts/investor_flow.py` (8개 KIS TR, 실계정 검증 완료)
- `engine/rule/engine.py`, `engine/report/markdown.py`, `engine/report/html.py` (PEOS 템플릿 렌더링 선례)
- [hbm-cycle-score.md](hbm-cycle-score.md) "1. HBM Cycle Score" (6축 가중치 공식)
- `data/manual_inputs/semiconductor.yaml` (반도체 신호가 왜 수동 입력인지 근거)
- WebSearch 2026-08-05: SEC EDGAR XBRL API, FMP/Finnhub 목표가 API, DRAM/NAND 무료 데이터, Polymarket, KIS 국내주식 목표주가 TR, TSMC HPC 매출비중, 네이버금융/FnGuide/DART
