# PEOS Master Implementation Instruction for Claude Code

> 문서명: **PEOS (Personal Economic Operating System) 종합 개발 작업지시서**  
> 버전: **1.0 (Integrated Master Build Spec)**  
> 목적: 앞서 정의된 개별 PRD/스펙 문서를 중복 없이 재정렬·통합하여, **Claude Code가 바로 구현을 시작할 수 있는 단일 기준 문서**를 제공한다.  
> 대상: **Claude Code**  
> 언어: **한국어**  
> 상태: **Development Ready / Master Instruction**

---

# 0. 문서 사용 지침

이 문서는 기존의 다음 문서를 하나의 구현 지시서로 통합한 것이다.

- Personal Economic Operating System (프로젝트 개요)
- System Architecture
- Data Engine
- Macro Engine
- Personal Economic Engine
- AI Report Engine
- Data Sources & Update Strategy

본 문서는 **철학 → 기능 요구사항 → 아키텍처 → 데이터 → 엔진 → 보고서 → 실행 순서 → 테스트/검증** 순서로 재구성되어 있다.  
구현 시 이 문서를 **단일 소스 오브 트루스(Single Source of Truth)** 로 사용한다.

---

# 1. 프로젝트 정의

## 1.1 프로젝트명

**PEOS (Personal Economic Operating System)**

## 1.2 프로젝트 한 줄 정의

PEOS는 단순한 경제 대시보드가 아니라,
**공식 데이터를 수집·검증하고, 거시경제와 산업 사이클을 해석한 뒤, 사용자의 상황과 자산에 맞춰 “이번 달 무엇을 해야 하는가”를 제안하는 AI 기반 개인 경제 운영체제**다.

## 1.3 프로젝트 목표

이 시스템의 목표는 “경제 정보를 보여주는 것”이 아니라,
**경제적 의사결정을 지원하는 것**이다.

반드시 아래 질문에 답할 수 있어야 한다.

> “현재 경제가 어떤 상태인가?”  
> “지난달과 무엇이 달라졌는가?”  
> “이 변화가 사용자에게 어떤 의미인가?”  
> “그래서 사용자는 이번 달 무엇을 해야 하는가?”

---

# 2. 제품 철학 및 절대 원칙

## 2.1 핵심 철학

이 시스템은 뉴스를 보여주는 서비스가 아니다.  
이 시스템은 **숫자를 해석하여 행동(Action)을 제안하는 AI**다.

기본 구조는 아래와 같다.

```text
뉴스/보도자료/공식발표
→ 공식 데이터 수집
→ 검증 및 정규화
→ 지표 생성
→ Rule Engine
→ Macro / Domain 분석
→ AI Analysis
→ Personal Recommendation
→ Action Plan
```

## 2.2 절대 원칙

1. 모든 판단은 **데이터 → 규칙 → 근거 → 결론** 순으로 수행한다.
2. AI의 감이나 추측으로 판단하지 않는다.
3. 언론은 설명 보조용으로만 사용하고, 판단의 1차 근거로 사용하지 않는다.
4. 공식 데이터가 없는 경우에만 신뢰 가능한 대체 소스를 사용한다.
5. 모든 출력은 최종적으로 **행동(Action)** 으로 끝나야 한다.
6. 사용자의 상황을 고려하지 않은 일반론 리포트는 허용하지 않는다.
7. 사실, 해석, 추정(시나리오)은 명확히 분리한다.
8. 데이터 누락 시 추측하지 않는다. `Pending` 또는 `Not Released`로 명시한다.

---

# 3. 대상 사용자(Persona)

## 3.1 기본 Persona

본 프로젝트는 불특정 다수를 위한 서비스가 아니라, 특정 사용자(Persona)를 위한 시스템이다.

### 사용자 특징
- 직업: 반도체 기업 엔지니어
- 업무 분야: 차세대 메모리, CXL, AI Infrastructure, Memory System
- 관심 분야:
  - 반도체
  - AI Infrastructure
  - Memory
  - CXL
  - Cloud
  - Data Center
  - ETF
  - 채권
  - 공공분양
  - 미국 경제
- 투자 성향:
  - 장기 투자
  - 거시경제 중심
  - 산업 사이클 중심
  - 데이터 기반 의사결정
  - 공식 통계 우선

## 3.2 Persona 반영 원칙

같은 경제 상황이라도 사용자마다 추천은 달라져야 한다.

예시:

```text
CPI 상승
→ 일반 사용자: 물가 부담
→ 본 사용자: 메모리 업황 지속 가능성 분석 → SK하이닉스 영향 → 보유 ETF 영향 → 채권 영향 → 행동 제안
```

## 3.3 사용자 프로필 데이터 구조 (필수 구현)

Claude Code는 아래 구조를 기본 스키마로 구현한다.

```yaml
user_profile:
  profile_version: 1
  updated_at: datetime

  job:
    title: string
    industry: string
    domains: [string]
    income_cycle_sensitivity: high|medium|low
    bonus_cycle_sensitivity: high|medium|low

  investment_style:
    horizon: long_term|mid_term|short_term
    macro_driven: bool
    cycle_driven: bool
    data_driven: bool
    risk_tolerance: high|medium|low
    rebalancing_rule: string

  interest_priority:
    semiconductor: float
    ai_infrastructure: float
    memory: float
    cxl: float
    cloud: float
    data_center: float
    etf: float
    bond: float
    housing: float
    fx: float

  assets:
    holdings_enabled: bool
    cash_tracking_enabled: bool
    portfolio_source: yaml|json|manual

  housing:
    target_type: public_sale
    preferred_size: "84m2+"
    priority_regions: [string]
    subscription_account_start: date
    subscription_priority_strategy: string
    moveout_deadline: date|null

  travel:
    business_trip_enabled: bool
    business_trip_regions: [string]
    leisure_travel_enabled: bool
    fx_sensitivity: high|medium|low

  reporting:
    report_day: int
    alert_time: string
    preferred_output: [dashboard, markdown, pdf, excel]
```

---

# 4. 최종 산출물 정의

PEOS는 최종적으로 다음 결과를 생성해야 한다.

1. 월간 Executive Summary
2. 경기 위치(Regime)
3. 지난달 대비 변화(Change Detection)
4. 주요 위험요인(Risk Factors)
5. 투자 전략(Stocks / ETF / Bond / Cash)
6. 자산 점검(Portfolio Health)
7. 공공분양 점검(Housing Readiness)
8. 환율 점검(FX Strategy)
9. 출장/여행 점검(Travel / Trip Readiness)
10. 이번 달 Action Plan
11. 경제 캘린더
12. 보고서 부록(Appendix)

---

# 5. 전체 시스템 아키텍처

## 5.1 아키텍처 개요

```text
Official Data Sources
→ Data Collection
→ Data Validation Engine
→ Normalized Database
→ Indicator Layer
→ Macro Engine / Semiconductor Engine / Personal Engine / Portfolio Engine / Housing Engine / FX Engine / Travel Engine
→ Rule Engine
→ Score Engine
→ AI Analysis Engine
→ Report Generation
→ Dashboard / PDF / Excel / Mobile
```

## 5.2 Layer 구조

```text
Presentation Layer
↓
Application Layer
↓
Analysis Layer
↓
Rule Engine Layer
↓
Data Layer
↓
Infrastructure Layer
```

각 Layer는 최대한 독립적으로 유지하며, 모듈 단위 테스트가 가능해야 한다.

## 5.3 권장 디렉터리 구조

```text
project/
├── app/
│   ├── dashboard/
│   ├── pages/
│   └── components/
├── data/
│   ├── raw/
│   ├── normalized/
│   ├── indicators/
│   ├── analysis/
│   ├── snapshots/
│   ├── ecos/
│   ├── kosis/
│   ├── fred/
│   ├── bls/
│   ├── imf/
│   ├── oecd/
│   ├── motie/
│   └── semiconductor/
├── engine/
│   ├── macro/
│   ├── semiconductor/
│   ├── portfolio/
│   ├── housing/
│   ├── exchange/
│   ├── travel/
│   ├── personal/
│   ├── report/
│   ├── rule/
│   └── scoring/
├── core/
│   ├── config/
│   ├── logger/
│   ├── cache/
│   ├── models/
│   └── utils/
├── config/
│   ├── api.yaml
│   ├── rules.yaml
│   ├── thresholds.yaml
│   ├── user.yaml
│   ├── portfolio.yaml
│   ├── schedule.yaml
│   └── report.yaml
├── report/
├── tests/
├── docs/
└── requirements.txt
```

---

# 6. 기술 스택

## 6.1 필수 스택
- Python 3.12+
- Pandas
- NumPy
- Requests / HTTPX
- Streamlit
- Plotly / Altair
- APScheduler 또는 GitHub Actions
- Markdown / PDF / Excel 출력
- LLM Provider 추상화 (OpenAI 또는 Claude API)

## 6.2 구현 원칙
모든 기능은 아래 순서를 따른다.

```text
Collect → Validate → Transform → Analyze → Score → Report → Recommend
```

---

# 7. 데이터 거버넌스 및 수집 전략

## 7.1 Official First 원칙

데이터 수집 우선순위:

```text
공식 API
→ 공식 Open Data
→ 공식 통계 페이지
→ 정부 보도자료
→ 공공기관 보고서
→ 기업 IR
→ 신뢰 가능한 민간 데이터
→ 언론 기사(최후의 수단)
```

언론은 설명에는 사용할 수 있으나, 판단의 1차 근거로 사용하지 않는다.

## 7.2 데이터 신뢰도 등급

- ★★★★★: 정부기관, 중앙은행, 국제기구, 공식 API
- ★★★★☆: 공공기관, 증권거래소, 공식 CSV, 기업 IR
- ★★★☆☆: 언론(공식자료 인용 시)
- ★★☆☆☆: 리서치 기관
- ★☆☆☆☆: 커뮤니티 / SNS (판단 금지)

**판단에는 기본적으로 ★★★★ 이상 데이터만 사용한다.**  
단, 반도체 특화 데이터처럼 공식성 한계가 있는 경우는 명시적 예외 정책을 둔다.

## 7.3 반도체 특화 데이터 예외 정책

반도체 산업 데이터는 공식 데이터만으로 완결되지 않을 수 있다. 따라서 아래 정책을 적용한다.

1. 정부 통계 / 기업 공시 / 기업 실적 / IR 자료는 판단용으로 사용 가능
2. 가격 기관 데이터(예: DRAM, NAND, HBM 관련 가격) 및 산업 리서치는 보조 판단용으로 사용 가능
3. 언론은 보충 설명용으로만 사용 가능
4. 공식성과 한계는 메타데이터에 명시한다

## 7.4 데이터 계층 구조

모든 데이터는 아래 계층으로 분리 저장한다.

```text
Level 1: Raw Data        (원본, 절대 수정 금지)
Level 2: Normalized Data (단위/형식 통일)
Level 3: Indicator Data  (경제지표 생성)
Level 4: Analysis Data   (점수/상태 계산)
Level 5: Report Data     (보고서 생성용)
```

## 7.5 Raw Data 불변 원칙
- Raw Data는 절대로 수정하지 않는다.
- Revision(수정 발표)이 발생하면 별도 버전으로 저장한다.
- 초기 발표 / 수정 발표 / 최종 발표를 모두 저장한다.

## 7.6 데이터 메타데이터 스키마

모든 데이터는 최소 아래 메타정보를 가진다.

```yaml
metadata:
  source: string
  release_date: date
  reference_date: date
  unit: string
  frequency: daily|weekly|monthly|quarterly|annual
  last_updated: datetime
  confidence: float
  reliability_grade: 1-5
  revision_stage: initial|revised|final
  official: bool
```

## 7.7 데이터 검증 규칙

모든 수집 데이터는 아래 항목을 검증한다.

1. Null 여부
2. 중복 여부
3. 단위 확인
4. 날짜 확인
5. 이상치 여부
6. 최신 데이터 여부
7. 이전값과의 차이
8. Revision 여부

## 7.8 이상치 처리 규칙

예:

```text
수출 증가율
전월: 15%
당월: 250%
→ Warning
→ 기저효과 여부 확인
→ 공식 발표문 재확인
→ 필요 시 보도자료로 보조 검증
→ 그대로 점수화 금지
```

이상치는 자동 경고를 발생시키고, 원인 확인 후 의미를 분리하여 해석한다.

## 7.9 데이터 누락 처리

데이터가 아직 발표되지 않았으면 직전값으로 덮어쓰지 않는다.
상태는 아래로 구분한다.

- `Pending`
- `Not Released`
- `Source Error`

AI는 누락 데이터를 추측하지 않는다.

## 7.10 교차 검증 규칙

가능한 경우 동일 데이터는 최소 2개 소스로 교차 검증한다.  
단, **유일한 공식 원자료가 존재하는 경우 단일 공식 소스를 허용**하고, Confidence 계산에 반영한다.

## 7.11 업데이트 주기

### 실시간/고빈도
- 환율: 30분
- 채권금리: 30분
- 주가지수: 5분

### 일간
- 시장 데이터 (KOSPI, KOSDAQ, S&P500, NASDAQ, SOX, DXY, WTI, Gold 등)

### 월간
- 수출
- 반도체 수출
- CPI
- PPI
- 실업률
- 산업생산
- 소매판매
- 경상수지

### 분기
- GDP
- 기업 실적
- 경제전망

### 반기/연간
- KDI 전망
- IMF / OECD 장기 전망

## 7.12 스냅샷 저장

매월 `Macro Snapshot`을 저장한다.

예:

```text
2026-07 Macro Snapshot
2026-08 Macro Snapshot
→ 자동 비교 및 변화 감지
```

---

# 8. 데이터 소스 맵

## 8.1 한국
- 한국은행 ECOS: GDP, PPI, 경상수지, 금리, 환율, 통화량, 금융통계
- 통계청 / KOSIS: CPI, 실업률, 고용률, 산업생산, 소매판매, 인구
- 산업통상자원부: 수출, 수입, 반도체 수출, 품목별 수출
- 한국은행 보고서: 경제전망, 금통위 자료
- KDI: 경제전망, 경기평가, 잠재성장률
- 청약홈: 청약 일정, 분양 정보
- LH / GH / SH: 공공분양 공급 일정 및 공고

## 8.2 미국
- BLS: CPI, PPI, Non Farm Payroll, 실업률
- Federal Reserve / FOMC: 기준금리, Beige Book, 정책 자료
- Treasury / FRED: 국채금리, Yield Curve, 금융 조건 관련 데이터

## 8.3 국제/글로벌
- IMF: 성장률, 세계경제전망, 물가
- OECD: CLI, 전망
- World Bank: 글로벌 경제 참고 데이터

## 8.4 금융시장
- KOSPI, KOSDAQ, S&P500, NASDAQ, SOX, VIX, MOVE, Dollar Index, US10Y, KR3Y, WTI, Gold, Bitcoin

## 8.5 반도체
- 반도체 수출
- DRAM / NAND / HBM 가격
- TrendForce 등 가격 지표(보조 데이터)
- Micron, SK hynix, Samsung DS, TSMC, NVIDIA, Broadcom 실적 및 가이던스
- AI Server / GPU 출하량
- CSP CapEx

## 8.6 사용자 데이터
- 보유 종목
- ETF
- 채권
- 현금
- 청약저축
- 출장 일정
- 여행 일정
- 투자 목표

---

# 9. Indicator Layer 설계

## 9.1 목적

Raw/Normalized 데이터는 직접 판단에 쓰지 않고,
반드시 **Indicator Layer**를 생성하여 Rule Engine의 입력으로 사용한다.

## 9.2 필수 지표 예시

### 한국 거시
- GDP QoQ
- GDP YoY
- 산업생산 MoM / 3M Avg
- 소매판매 MoM / 3M Avg
- 총수출 YoY / 12M Trend
- 반도체 수출 YoY / 12M Trend
- 경상수지 수준 및 3M 평균
- CPI YoY / 3M 추세 / 재가속 여부
- PPI YoY / 3M 추세
- 실업률 3M 이동평균 / 3개월 연속 상승 여부

### 미국 / 글로벌
- Non Farm Payroll Trend
- US Unemployment Trend
- PMI / ISM Direction
- Yield Curve (10Y-2Y)
- Global Growth Composite

### 금융 / 금리
- Real Rate = Policy Rate - CPI
- KR/US Rate Differential
- Bond Yield Trend
- DXY Trend

### 반도체
- Memory Cycle Trend
- DRAM Price Trend
- NAND Price Trend
- HBM Momentum
- CSP CapEx Trend
- GPU Shipment Trend

## 9.3 추세 계산 단위

모든 주요 지표는 아래 기간별 추세를 계산한다.

- 1개월
- 3개월
- 6개월
- 12개월
- 3년
- 5년

## 9.4 추세 등급 standard

```text
★★★★★ 강한 상승
★★★★☆ 상승
★★★☆☆ 횡보
★★☆☆☆ 약화
★☆☆☆☆ 급락
```

이를 내부적으로는 수치형 score로도 저장한다.

---

# 10. Rule Engine 설계

## 10.1 핵심 원칙

Rule은 코드에 하드코딩하지 않는다.  
반드시 YAML 또는 JSON으로 분리한다.

## 10.2 Rule 파일 구조 예시

```yaml
macro:
  gdp:
    score:
      positive:
        qoq_gte: 0.8
        yoy_gte: 3.0
      neutral:
        qoq_between: [0.0, 0.7]
      negative:
        qoq_lt: 0.0
    weight: 1.0

  exports:
    score:
      positive:
        yoy_gte: 10.0
      neutral:
        yoy_between: [0.0, 10.0]
      negative:
        yoy_lt: 0.0
    weight: 1.0

  semiconductor_exports:
    score:
      positive:
        yoy_gte: 20.0
      neutral:
        yoy_between: [0.0, 20.0]
      negative:
        yoy_lt: 0.0
    weight: 1.5
```

## 10.3 Rule 분리 대상

- Macro Rules
- Regime Transition Rules
- Warning Rules
- Upgrade/Downgrade Rules
- Semiconductor Rules
- Bond Rules
- FX Rules
- Housing Rules
- Action Mapping Rules

---

# 11. Macro Engine 상세 구현 명세

## 11.1 목적

Macro Engine은 경제지표를 보여주는 엔진이 아니라,
**현재 경제가 어느 국면에 있는지 객관적으로 측정하는 엔진**이다.

## 11.2 실행 순서

```text
Data Collection
→ Normalization
→ Indicator Calculation
→ Trend Detection
→ Rule Engine
→ Score Engine
→ Confidence Calculation
→ Risk Detection
→ Scenario Analysis
→ AI Report Payload 생성
```

## 11.3 Core Indicator 10

아래 10개를 코어 지표로 구현한다.

1. 실질 GDP 성장률
2. 전산업생산지수
3. 소매판매
4. 총수출 증가율
5. 반도체 수출 증가율
6. 경상수지
7. CPI
8. PPI
9. 한국 실업률
10. 미국 고용 + 글로벌 경기

## 11.4 지표별 기본 점수 규칙

### (1) 실질 GDP 성장률
- 목적: 경제 전체 체력 측정
- 중요도: ★★★★★
- 기본 score:
  - +1: QoQ ≥ 0.8% 또는 YoY ≥ 3%
  - 0: QoQ 0.0% ~ 0.7%
  - -1: QoQ < 0%

### (2) 전산업생산
- 목적: 실물경제 확인
- 중요도: ★★★★★
- 기본 score:
  - +1: 전월 +0.3% 이상
  - 0: -0.2% ~ +0.2%
  - -1: -0.3% 이하
- 추가: 최근 3개월 평균 계산

### (3) 소매판매
- 목적: 내수 확인
- 중요도: ★★★★☆
- score:
  - +1: +0.3% 이상
  - 0: -0.2% ~ +0.2%
  - -1: -0.3% 이하

### (4) 총수출 증가율
- 목적: 한국 경기 선행지표
- 중요도: ★★★★★
- score:
  - +1: 10% 이상
  - 0: 0% ~ 10%
  - -1: 음수
- 추가: 12개월 추세 필수 계산

### (5) 반도체 수출 증가율
- 목적: 한국 경제 핵심 엔진
- 중요도: ★★★★★+
- score:
  - +1: 20% 이상
  - 0: 0% ~ 20%
  - -1: 음수
- 주의: 일반 지표보다 높은 가중치 적용

### (6) 경상수지
- 목적: 국가 대외 체력
- 중요도: ★★★★☆
- 정량화 필요:
  - +1: 3개월 평균 기준 강한 흑자
  - 0: 3개월 평균 기준 소폭 흑자
  - -1: 적자

### (7) CPI
- 목적: 물가 부담
- 중요도: ★★★★★
- score:
  - +1: 1.5% ~ 2.5%
  - 0: 2.6% ~ 3.0%
  - -1: 3.1% 이상
- 추가: 재가속 여부 탐지

### (8) PPI
- 목적: 기업 원가 압력
- 중요도: ★★★★★
- score:
  - +1: 0% ~ 4%
  - 0: 4% ~ 6%
  - -1: 6% 이상

### (9) 한국 실업률
- 목적: 체감 경기
- 중요도: ★★★★☆
- 정량화 필요:
  - +1: 낮은 수준 유지 및 3개월 평균 안정
  - 0: 보합
  - -1: 3개월 연속 상승 또는 임계치 이상 상승

### (10) 미국 고용 + 글로벌 경기
- 목적: 한국 수출 환경 확인
- 중요도: ★★★★★
- 입력: NFP, 실업률, PMI/ISM, IMF/OECD
- score:
  - +1: 글로벌 우호
  - 0: 혼합
  - -1: 둔화
- 구현 시 하위 composite score로 정량화할 것

## 11.5 Macro Score 계산

모든 지표는 기본적으로 `-1/0/+1` score를 가진다.  
다만 **반도체 수출은 가중치 확대**가 필요하다.

권장 방식:

```text
Macro Weighted Score = Σ(indicator_score × weight)
```

권장 가중치 예시:
- GDP: 1.0
- 산업생산: 1.0
- 소매판매: 0.8
- 총수출: 1.0
- 반도체 수출: 1.5
- 경상수지: 0.8
- CPI: 1.0
- PPI: 1.0
- 실업률: 0.8
- 미국/글로벌: 1.0

## 11.6 총점 기반 1차 판정

기존 단순 총점 구간을 유지하되, 가중 합계 사용 시 scale을 재보정한다.  
최소 구현 버전에서는 원래 구간을 유지하고, 가중치 도입 시 별도 calibration 파일을 둔다.

기본 구간:

- +7 ~ +10: Strong Expansion
- +4 ~ +6: Expansion
- +1 ~ +3: Unbalanced Expansion
- 0 ~ -1: Early Slowdown
- -2 ~ -4: Slowdown
- -5 이하: Recession Warning

## 11.7 Regime Detection

다음 경제 사이클을 판정한다.

```text
Recovery → Early Expansion → Expansion → Late Expansion → Slowdown → Recession → Recovery
```

### Regime 전이 규칙(필수 구현)
아래 요소를 조합한다.
- 이번 달 총점
- 지난달 총점
- 개선 지표 수 / 악화 지표 수
- 물가 압력 상태
- 수출 / 반도체 추세
- 지속 조건(2개월 연속 여부)

예시:
- Early Expansion → Expansion: 총점이 2개월 연속 개선되고 수출/생산이 동반 개선
- Expansion → Late Expansion: 성장 강세 유지 + CPI/PPI 부담 상승
- Expansion → Slowdown: 총점 하락 + 악화 지표 우세 + 경고 신호 동반

## 11.8 강등 규칙

아래 중 2개 이상 발생 시 1단계 강등:
- 수출 급락
- 반도체 수출 급락
- 산업생산 2개월 감소
- CPI 재상승
- PPI 6% 이상 지속
- 환율 급등
- 금리 상승

## 11.9 즉시 경고(Warning)

아래 중 1개만 발생해도 Warning 발생:
- 수출 음수
- 반도체 수출 음수
- 실업률 급등
- 경상수지 적자
- 미국 고용 급랭
- Yield Curve 역전 심화

## 11.10 상향 규칙

아래 중 3개 이상 만족 시 1단계 상향:
- GDP 강세
- 수출 강세
- 반도체 강세
- CPI 안정
- PPI 둔화
- 금리 완화
- 미국 고용 개선

## 11.11 Confidence Score

모든 Macro 판정은 신뢰도를 가진다.

권장 계산식:

```text
Confidence =
  0.30 * Data Freshness
+ 0.25 * Source Quality
+ 0.25 * Indicator Consistency
+ 0.20 * Trend Stability
```

각 하위 요인은 0~100으로 표준화한 뒤 최종 0~100 점수로 저장한다.

## 11.12 Change Detection

지난달 대비 자동 변화 감지를 구현한다.

예시 기준:
- 수출: 전월 대비 5%p 이상 개선 → 강화
- CPI: 0.2%p 이상 하락 → 개선
- 실업률: 0.2%p 이상 상승 → 주의
- PPI: 0.3%p 이상 둔화 → 완화

이 기준은 `thresholds.yaml`로 외부화한다.

---

# 12. Semiconductor Engine 상세 명세

## 12.1 목적

반도체는 사용자의 직업, 투자, 성과급, 자산 배분과 직접 연결되므로 별도 엔진으로 구현한다.

## 12.2 입력 데이터
- 반도체 수출
- DRAM 가격
- NAND 가격
- HBM 관련 지표
- Micron 실적 및 가이던스
- SK hynix 실적 및 가이던스
- Samsung DS 실적 및 가이던스
- TSMC 매출
- NVIDIA / Broadcom 실적
- AI Server 출하량
- GPU 출하량
- CSP 투자

## 12.3 출력 점수
- Memory Cycle Score (0~100)
- AI Infrastructure Score (0~100)
- Semiconductor Score (0~100)

## 12.4 권장 계산 방식

### Memory Cycle Score
권장 구성:
- DRAM 가격 추세: 30%
- NAND 가격 추세: 15%
- 반도체 수출: 25%
- Micron / SK hynix 가이던스: 15%
- 재고/수급 관련 시그널: 15%

### AI Infrastructure Score
권장 구성:
- NVIDIA / Broadcom 실적 및 가이던스: 25%
- GPU 출하량: 20%
- AI Server 출하량: 20%
- CSP CapEx: 20%
- HBM 관련 시그널: 15%

### Semiconductor Score
권장 구성:
- Memory Cycle Score: 50%
- AI Infrastructure Score: 30%
- 한국 반도체 수출 추세: 20%

## 12.5 상태 해석 구간
- 80 이상: Strong Positive
- 65~79: Positive
- 50~64: Neutral+
- 35~49: Cautious
- 35 미만: Weak / Risk

---

# 13. Personal Economic Engine 상세 명세

## 13.1 목적

Macro 결과를 사용자의 직업, 투자, 자산, 환율, 청약, 출장, 여행과 연결하여 **실질적 행동으로 변환**한다.

## 13.2 분석 영역
1. 주식
2. ETF
3. 채권
4. 현금
5. 환율
6. 공공분양
7. 출장
8. 여행
9. 경제 일정

## 13.3 Personal Mapping 로직

반드시 다음 순서로 동작한다.

```text
Macro Result + Domain Scores + User Profile + User Assets + User Goals
→ Personal Meaning Mapping
→ Domain Recommendation
→ Unified Action Plan
```

## 13.4 투자 엔진

### 목적
거시 환경과 산업 사이클을 투자환경으로 변환한다.

### 출력
- Investment Environment Score (0~100)
- Stock Bias
- ETF Bias
- Bond Bias
- Cash Bias

### 권장 계산

```text
Investment Environment Score =
  0.35 * Macro Score Normalized
+ 0.35 * Semiconductor Score
+ 0.15 * Liquidity/Rate Condition
+ 0.15 * Risk Penalty Inverse
```

## 13.5 ETF 엔진

### 목적
현재 경기/산업 환경과 ETF 구성이 맞는지 평가

### 출력
- ETF Fit Score (by ETF or ETF bucket)

### 평가 항목 예시
- 경기 민감도 적합성
- 반도체/AI 노출 적합성
- 금리 민감도
- 방어 성격 필요성
- 현재 Macro Regime 적합성

## 13.6 채권 엔진

### 목적
금리, 물가, 실질금리를 연결하여 채권 매수 환경 평가

### 출력
- Bond Score (0~100)

### 권장 계산

```text
Bond Score =
  0.40 * Rate Direction
+ 0.25 * Real Rate Attractiveness
+ 0.20 * Inflation Slowdown Signal
+ 0.15 * Growth Slowdown Signal
```

## 13.7 환율 엔진

### 목적
환율을 투자/출장/여행/환전 의사결정으로 연결

### 입력
- 원달러
- 원엔
- Dollar Index
- 한미 금리차
- 미국 금리 방향

### 출력
- FX Score (0~100)
- 출장 환전 적합도
- 여행 환전 적합도

## 13.8 공공분양 엔진

### 목적
일반 부동산 분석이 아니라 사용자 목표형 공공분양 분석 수행

### 분석 대상
- LH / GH / SH / 청약홈
- 84㎡ 이상
- 일반공급
- 무주택
- 청약저축
- 자금 계획

### 출력
- 청약 적합도 (0~100)
- 자격 상태
- 준비도
- 필요 자금
- 주의사항

### 권장 계산식

```text
Housing Readiness Score =
  0.30 * Eligibility Fit
+ 0.25 * Funding Readiness
+ 0.20 * Region/Type Match
+ 0.15 * Timing Readiness
+ 0.10 * Competition Adjustment Inverse
```

## 13.9 플랫폼시티 분석

플랫폼시티는 별도 세부 분석 대상으로 구현한다.

반드시 포함:
- 입지
- 공급 규모
- 예상 일정
- 자금 조달
- 예상 경쟁률
- 사용자 적합도
- 리스크
- Action Plan

## 13.10 출장 엔진

출장 일정이 있을 경우 자동 분석한다.

분석 요소:
- 방문 국가/지역
- 환율
- 항공권
- 숙박비
- 출장비 부담
- 환전 시점

출력:
- Trip Readiness Score
- 출장 환전 권고
- 비용 리스크

## 13.11 여행 엔진

분석 요소:
- 환율
- 성수기/비수기
- 항공권
- 숙박비

출력:
- Travel Timing Score
- 환전 적기 판단

## 13.12 경제 일정 엔진

이번 달 반드시 확인해야 할 핵심 이벤트를 우선순위화한다.

출력 등급:
- ★★★★★ 반드시 확인
- ★★★★☆ 검토
- ★★★☆☆ 관찰

우선순위 계산 요소:
- 사용자 관련도
- 시장 영향도
- 산업 영향도
- 시간 임박성
- 포트폴리오 영향도

---

# 14. Portfolio / Asset Impact Layer

## 14.1 목적

사용자 자산 항목별로 현재 환경이 어떤 영향을 주는지 진단한다.

## 14.2 필수 자산 카테고리
- 주식
- ETF
- 채권
- 현금
- 공공분양 준비 자금
- 환율 노출

## 14.3 자산 영향도 점수 (권장)

각 자산군에 대해 0~100 점수와 별점 등급을 생성한다.

별점 변환 예시:
- 85~100: ★★★★★
- 70~84: ★★★★☆
- 55~69: ★★★☆☆
- 40~54: ★★☆☆☆
- 0~39: ★☆☆☆☆

## 14.4 자산군별 평가 예시

### 주식
- 반도체 / AI 우위 여부
- 경기민감도
- 밸류에이션 부담
- 이벤트 리스크

### ETF
- 현재 국면 적합성
- 섹터 노출 적합성
- 방어/공격 밸런스

### 채권
- 실질금리 매력
- 물가 둔화 여부
- 정책금리 방향

### 현금
- 유동성 필요도
- 향후 청약/출장/환전 필요도
- 공격적 투자 축소 필요 여부

### 공공분양 준비 자금
- 자금 확보 상태
- 일정 임박도
- 자금 이동 제한 필요성

### 환율
- USD/JPY 환전 타이밍
- 출장/여행 비용 영향

---

# 15. Action Engine 상세 명세

## 15.1 목적

모든 분석은 최종적으로 **행동**으로 끝나야 한다.

최종 보고서의 Action Plan은 다음과 같은 사용 가치를 제공해야 한다.
- 이번 달 꼭 확인해야 할 것
- 검토할 것
- 관찰만 할 것
- 보류할 것

## 15.2 Action 생성 입력

```text
Macro Regime
+ Macro Risks
+ Semiconductor Score
+ Investment Environment Score
+ Bond Score
+ FX Score
+ Housing Readiness Score
+ Upcoming Events
+ User Profile / User Assets / User Goals
```

## 15.3 Action 우선순위 계산

권장 공식:

```text
Action Priority Score =
  0.30 * User Relevance
+ 0.25 * Risk Level
+ 0.20 * Time Urgency
+ 0.15 * Portfolio Impact
+ 0.10 * Event Significance
```

## 15.4 Action 등급
- 85 이상: ★★★★★ 반드시 실행 / 반드시 확인
- 70~84: ★★★★☆ 검토 필요
- 55~69: ★★★☆☆ 관찰 필요
- 40~54: ★★☆☆☆ 참고
- 39 이하: 보류

## 15.5 Action 문장 규칙

각 행동은 반드시 아래 구조를 가진다.

1. 무엇을 할 것인가
2. 왜 지금 해야 하는가
3. 어떤 조건에서 실행을 멈출 것인가
4. 언제 다시 확인할 것인가

예시:

```text
[행동]
채권 비중 추가 확대 여부를 검토한다.
[이유]
금리 완화 기대가 형성되고 있으나 물가 둔화 확인이 추가로 필요하다.
[보류 조건]
CPI 재가속 또는 장기금리 급등 시 보류.
[재점검]
미국 CPI 및 한국은행 금통위 이후 재검토.
```

## 15.6 Conflict Resolver (필수 구현)

엔진 간 충돌 시 우선순위를 적용한다.

권장 우선순위:
1. 생존/유동성 (현금, 필수 자금, 청약 자금, 급한 환전)
2. Macro Risk
3. 산업 사이클
4. 투자 기회
5. 여행/기타 선택 행동

예시:
- 반도체 강세이더라도 청약 자금 확보가 우선이면 공격적 매수 확대를 억제
- 환율이 불리하더라도 출장 일정이 확정이면 분할 환전 제안

---

# 16. AI Report Engine 상세 명세

## 16.1 목적

모든 데이터, 분석, 점수, 개인화 결과를 **사람이 읽기 쉬운 하나의 보고서**로 생성한다.

보고서는 다음 변환을 수행해야 한다.

```text
데이터 → 정보 → 인사이트 → 행동
```

## 16.2 핵심 품질 기준
- 정확성 ★★★★★
- 최신성 ★★★★★
- 가독성 ★★★★★
- 시각화 ★★★★★
- 개인화 ★★★★★
- 실행 가능성 ★★★★★

## 16.3 보고서 생성 순서

1. Executive Summary
2. 이번 달 핵심 변화
3. Macro Dashboard
4. 경기 판정
5. 주요 지표 분석
6. 사용자 맞춤 분석
7. 자산별 영향 분석
8. 시나리오 분석
9. 위험요인
10. 추천 행동(Action)
11. 경제 캘린더
12. Appendix

## 16.4 Executive Summary 구성 규칙

첫 페이지는 3분 안에 전체 이해가 가능해야 한다. 반드시 포함:
- 현재 경기 국면
- 지난달 대비 변화
- 핵심 원인
- 이번 달 가장 중요한 변화
- 사용자에게 가장 중요한 의미

### 생성 템플릿 원칙
보고서 문장은 반드시 아래 논리 순서를 따른다.
1. 현재 상태
2. 변화
3. 원인
4. 사용자 의미
5. 행동 시사점

## 16.5 Macro Dashboard 구성

표와 그래프로 요약한다. 기본 컬럼:
- 지표
- 현재
- 이전
- 추세
- 점수

총점과 자동 판정 라벨을 함께 표시한다.

## 16.6 지표별 심층 분석 포맷

각 지표는 동일 구조를 따른다.

1. 검증된 사실
2. 최근 추세
3. 경제적 의미
4. 사용자 영향
5. 향후 전망

## 16.7 사용자 맞춤 분석

반드시 아래를 연결한다.
- 직업
- 투자
- 청약
- 환율
- 출장
- 여행
- 현금
- 목표

## 16.8 자산별 영향 분석

각 자산군에 대해 다음 정보를 제공한다.
- 영향도 별점
- 현재 해석
- 주의할 점
- 행동 힌트

## 16.9 시나리오 분석

반드시 3개 시나리오를 제공한다.
- Base Scenario
- Bull Scenario
- Bear Scenario

각 시나리오는 다음을 포함한다.
- 확률
- 핵심 전제
- 기대되는 변화
- 사용자 영향

### 시나리오 확률 계산 권장

```text
Base: 현재 추세 지속 신호 기반
Bull: 개선 신호 개수 및 강도 기반
Bear: 리스크 신호 개수 및 강도 기반
```

### 제약
- 확률 총합 = 100
- 근거 없는 숫자 사용 금지

## 16.10 깨지는 조건(Invalid Conditions)

보고서는 항상 기본 시나리오가 무효화되는 조건을 명시해야 한다.

예시:
- 수출 감소
- 반도체 수출 감소
- CPI 재상승
- PPI 상승 지속
- 환율 급등
- 미국 고용 악화

## 16.11 Action Plan 페이지

가장 중요한 페이지다.  
AI는 이번 달 해야 할 일을 우선순위로 정렬하여 제공한다.

표현 규칙:
- ★★★★★ 반드시 확인 / 반드시 실행
- ★★★★☆ 검토
- ★★★☆☆ 관찰

각 Action에는 이유와 재점검 시점을 붙인다.

## 16.12 경제 캘린더

이번 달 주요 일정을 우선순위와 함께 표시한다.

예시 항목:
- 미국 CPI
- 한국 수출
- 반도체 수출
- PPI
- 금통위
- FOMC
- GDP
- 고용

각 일정에는 사용자 영향도를 표시한다.

## 16.13 Personal Executive Brief

보고서 말미에는 사용자를 위한 전용 요약 섹션을 생성한다.

반드시 포함:
- 이번 달 한 줄 진단
- 자산별 영향 요약
- 가장 중요한 이벤트 TOP 5
- AI의 최종 제안

---

# 17. AI 작성 및 서술 규칙

## 17.1 절대 규칙
1. 단순 수치 나열 금지
2. 모든 숫자는 의미 → 영향 → 행동으로 연결
3. 공식 데이터 우선 사용
4. 사실과 추정을 구분
5. 확률은 근거와 함께 제시
6. 불필요한 낙관/비관 금지
7. Action으로 끝날 것

## 17.2 서술 구조 (필수)

각 핵심 문장은 아래 중 하나의 형태를 따른다.

### 사실 진술
```text
[사실] 공식 데이터 기준 현재 수치는 X이다.
```

### 해석
```text
[해석] 이는 Y를 의미하며, 특히 Z 영역에 영향을 준다.
```

### 추정 / 시나리오
```text
[시나리오] 향후 A~B 범위 가능성이 높으며, 확률은 C%로 본다.
```

### 행동 제안
```text
[행동] 따라서 이번 달에는 D를 확인/검토/실행하는 것이 합리적이다.
```

## 17.3 Tone & UX
- 과장 금지
- 분석가 + 자산관리사 + 실행 코치의 결합된 톤
- 사용자가 뉴스를 보지 않아도 이해 가능한 문장
- 모바일/PC 모두 읽기 쉬운 짧은 단락과 카드형 UI를 전제로 작성

---

# 18. 데이터 저장, 캐시, 스케줄링

## 18.1 저장 정책
- Raw Data: 원본 저장
- Normalized Data: 단위 통일 후 저장
- Indicator Data: 계산된 지표 저장
- Analysis Result: 점수/판정/리스크 저장
- Report Data: 보고서 payload 및 최종 markdown/json 저장

## 18.2 캐시 정책
예시:
- GDP: 24시간
- CPI: 24시간
- PPI: 24시간
- 환율: 30분
- 주가: 5분
- 채권금리: 30분

## 18.3 자동 실행 일정

권장 흐름:

```text
매일 오전: 시장 데이터 업데이트
매월 초: 한국 수출 업데이트
미국 고용 발표 시: 미국 고용 업데이트
미국 CPI 발표 시: 미국 CPI 업데이트
한국 CPI/PPI 발표 시: 업데이트
산업생산/경상수지 업데이트
→ 핵심 월간 지표 충족률 검사
→ Macro Engine 실행
→ Domain Engines 실행
→ Report 생성
```

## 18.4 리포트 생성 조건

다음 중 하나가 발생하면 리포트를 생성한다.
- 월간 주요 지표 업데이트 완료
- GDP 발표
- IMF 전망 발표
- 한국은행 경제전망 수정
- FOMC 이후 핵심 변수 변화
- 사용자가 직접 요청

## 18.5 필수 지표 충족률 정책 (권장)

- 80% 이상: Draft Report 생성 가능
- 핵심 지표 누락 시: Final Report 보류
- 대형 이벤트 발생 시: Update Note 또는 Interim Report 생성

---

# 19. 로깅 / 보안 / 예외 처리

## 19.1 로깅

모든 과정은 로그를 남긴다.
- 데이터 수집 성공/실패
- API Retry
- Cache 사용
- Revision 발생
- Rule 적용
- Score 계산
- Report 생성
- 사용자 입력 변경

## 19.2 장애 처리

```text
API 실패
→ Retry
→ 실패 시 대체 Source 사용
→ 불가 시 Cache 사용
→ Warning 표시
→ Log 저장
```

## 19.3 보안
- API Key는 `.env` 또는 비밀 관리 저장소 사용
- Git에 업로드 금지
- 사용자 개인 데이터는 별도 보호

---

# 20. 출력 데이터 구조 (권장 JSON Schema)

Claude Code는 내부적으로 아래와 유사한 structured payload를 생성할 것.

```json
{
  "report_month": "2026-07",
  "macro": {
    "regime": "Unbalanced Expansion",
    "score": 2,
    "confidence": 88,
    "warnings": ["CPI 재상승 가능성", "환율 부담"]
  },
  "macro_dashboard": [
    {
      "indicator": "GDP",
      "current": "강함",
      "previous": "강함",
      "trend": "→",
      "score": 1,
      "source": "BOK"
    }
  ],
  "personal": {
    "investment_environment_score": 84,
    "semiconductor_score": 87,
    "bond_score": 63,
    "fx_score": 54,
    "housing_readiness_score": 79
  },
  "assets": {
    "stocks": {"score": 88, "rating": "★★★★★"},
    "etf": {"score": 81, "rating": "★★★★☆"},
    "bond": {"score": 63, "rating": "★★★☆☆"},
    "cash": {"score": 72, "rating": "★★★★☆"}
  },
  "scenarios": {
    "base": {"probability": 60, "summary": "불균형 확장 유지"},
    "bull": {"probability": 20, "summary": "물가 안정 + 반도체 강세"},
    "bear": {"probability": 20, "summary": "미국 둔화 + 환율 상승"}
  },
  "actions": [
    {
      "priority": 5,
      "title": "미국 CPI 확인",
      "reason": "채권 및 환율 전략에 직접 영향",
      "invalid_condition": "CPI 재가속 시 채권 확대 보류",
      "recheck": "발표 당일"
    }
  ],
  "calendar": [
    {
      "date": "2026-07-12",
      "event": "미국 CPI",
      "importance": 5
    }
  ]
}
```

---

# 21. 테스트 전략

## 21.1 테스트 원칙
각 Engine은 독립적으로 테스트 가능해야 한다.

## 21.2 테스트 범위
- Data Collection 테스트
- Validation 테스트
- Indicator 계산 테스트
- Macro Rule 테스트
- Score 계산 테스트
- Regime 전이 테스트
- Warning/강등/상향 규칙 테스트
- Semiconductor Score 테스트
- Bond/FX/Housing Score 테스트
- Action Priority 테스트
- Report Section 생성 테스트

## 21.3 테스트 목표
- Unit Test Coverage 80% 이상
- 주요 Rule에 대한 Snapshot Test
- 월별 리포트 regression 비교 테스트

## 21.4 필수 시뮬레이션 케이스
1. 수출 강세 + 내수 둔화 + CPI 부담 → Unbalanced Expansion
2. 수출 악화 + 실업률 상승 + 경상수지 적자 → Slowdown / Recession Warning
3. 반도체 강세 + 환율 부담 → 주식 우호 / 환전 보수
4. 금리 하락 기대 + CPI 둔화 → Bond Score 상승
5. 청약 공고 임박 + 자금 준비 부족 → Housing Warning

---

# 22. 성능 목표

- Dashboard 초기 실행: 3초 이하
- 데이터 갱신: 30초 이하
- 리포트 생성: 10초 이하

---

# 23. 구현 순서 (반드시 이 순서로 진행)

## Phase 1. Core Foundation
1. 프로젝트 구조 생성
2. config 로더
3. logger / cache / env 관리
4. 공통 데이터 모델 정의
5. raw / normalized / indicator 저장 구조 구현

## Phase 2. Data Layer
1. 한국/미국 핵심 데이터 collector 구현
2. validation engine 구현
3. metadata 스키마 적용
4. snapshot 저장 구현
5. change detection 기반 마련

## Phase 3. Rule & Indicator Layer
1. indicator 계산기 구현
2. `rules.yaml` / `thresholds.yaml` 설계
3. macro basic score 계산
4. warning / upgrade / downgrade rule 적용
5. confidence score 계산

## Phase 4. Macro Engine
1. core 10 indicator 기반 macro score 계산
2. regime detection 구현
3. risk detection 구현
4. change summary 생성

## Phase 5. Domain Engines
1. semiconductor engine
2. investment/ETF engine
3. bond engine
4. FX engine
5. housing/public sale engine
6. travel/trip engine
7. calendar priority engine

## Phase 6. Personal Mapping & Action Engine
1. user profile schema 적용
2. macro → personal mapping 구현
3. action priority engine 구현
4. conflict resolver 구현

## Phase 7. Report Engine
1. structured payload 생성
2. markdown report builder
3. dashboard section renderer
4. PDF/Excel export 준비
5. appendix/source rendering 구현

## Phase 8. QA & Hardening
1. 단위 테스트
2. 통합 테스트
3. 샘플 월간 보고서 생성
4. 예외 상황 점검
5. 코드 정리 및 문서화

---

# 24. Claude Code에 대한 구체적 작업 지시

아래 원칙을 그대로 따를 것.

## 24.1 기본 구현 원칙
1. 모듈화 우선
2. 모든 Rule/Threshold는 외부 설정 파일에 분리
3. Raw Data 불변 유지
4. 지표 계산과 보고서 서술을 분리
5. 점수 계산 로직과 문장 생성 로직을 분리
6. 테스트 가능한 함수 중심으로 구현
7. 사용자 맞춤형 분석이 최종 행동으로 연결되도록 설계

## 24.2 금지 사항
- 코드 내 하드코딩된 Rule 남용 금지
- 단순 뉴스 요약 서비스처럼 구현 금지
- 설명 없이 점수만 보여주는 형태 금지
- 사용자 컨텍스트 없는 범용 분석 금지
- 데이터 누락 시 추측 금지

## 24.3 최소 기능 요건 (MVP)
MVP에서도 반드시 지원해야 한다.

- 공식 데이터 기반 수집
- Raw/Normalized/Indicator/Analysis/Report 분리 저장
- Macro Core 10 점수화
- 반도체 별도 점수화
- 개인 맞춤 요약
- Action Plan 생성
- 경제 캘린더
- Markdown 리포트 생성

## 24.4 확장 고려사항
향후 plugin 구조로 아래 영역이 추가 가능해야 한다.
- Crypto
- Gold
- Oil
- REITs
- Space Industry
- Battery
- Defense
- AI Index

코어 수정 없이 모듈 추가가 가능하도록 설계할 것.

---

# 25. 보고서 템플릿 예시 골격

```markdown
# 월간 PEOS 리포트 - YYYY-MM

## 1. Executive Summary
- 현재 경기 국면:
- 지난달 대비 변화:
- 핵심 원인:
- 사용자에게 중요한 의미:
- 이번 달 핵심 행동:

## 2. 이번 달 핵심 변화
- 수출:
- 반도체:
- CPI:
- PPI:
- 실업률:

## 3. Macro Dashboard
| 지표 | 현재 | 이전 | 추세 | 점수 |
|------|------|------|------|------|

## 4. 경기 판정
- 총점:
- Regime:
- Confidence:
- Warning:

## 5. 지표별 분석
### GDP
### 산업생산
### 소매판매
### 수출
### 반도체
### CPI
### PPI
### 실업률
### 미국/글로벌

## 6. 사용자 맞춤 분석
- 직업 관점:
- 투자 관점:
- 환율 관점:
- 공공분양 관점:
- 출장/여행 관점:

## 7. 자산별 영향 분석
- 주식:
- ETF:
- 채권:
- 현금:
- 청약 자금:
- 환율:

## 8. 시나리오 분석
- Base:
- Bull:
- Bear:
- 깨지는 조건:

## 9. 이번 달 Action Plan
### ★★★★★ 반드시 확인 / 실행
### ★★★★☆ 검토
### ★★★☆☆ 관찰

## 10. 경제 캘린더
| 날짜 | 이벤트 | 중요도 | 사용자 영향 |
|------|--------|--------|-------------|

## 11. Personal Executive Brief
- 이번 달 한 줄 진단:
- 자산별 영향 요약:
- 중요한 이벤트 TOP 5:
- 최종 제안:

## 12. Appendix
- 데이터 출처
- 지난달과 비교
- 용어 설명
```

---

# 26. 완료 기준(Definition of Done)

다음 조건이 충족되면 1차 구현 완료로 본다.

1. 핵심 데이터 수집 파이프라인이 작동한다.
2. Raw / Normalized / Indicator / Analysis / Report 저장이 분리된다.
3. Macro Core 10에 대한 score와 regime 판정이 가능하다.
4. Semiconductor Score가 계산된다.
5. Personal Mapping이 가능하다.
6. 투자/채권/환율/청약/경제일정에 대한 최소 권고가 생성된다.
7. 월간 Markdown 보고서가 자동 생성된다.
8. Action Plan이 우선순위와 이유, 재점검 시점을 포함한다.
9. 신뢰도/Warning/깨지는 조건이 보고서에 포함된다.
10. 테스트 및 기본 예외 처리가 동작한다.

---

# 27. 최종 지시

Claude Code는 이 문서를 기준으로 다음을 수행할 것.

1. 먼저 프로젝트 골격과 config 체계를 생성한다.
2. 데이터 계층 구조와 메타데이터 모델을 구현한다.
3. Macro Engine의 core scoring 및 regime detection을 구현한다.
4. Semiconductor / Bond / FX / Housing / Calendar 등 domain engine을 구현한다.
5. Personal Mapping과 Action Engine을 구현한다.
6. AI Report Engine으로 Markdown 리포트를 생성한다.
7. 모든 기능이 “정보 제공”이 아니라 “행동 제안”으로 끝나도록 보장한다.
8. 구현 중 모든 Rule/Threshold/Template는 재사용과 수정이 가능하도록 외부화한다.

이 시스템의 목표는 단순한 경제 정보 서비스가 아니라,
**사용자가 뉴스 없이도 이번 달 무엇을 해야 하는지 판단할 수 있는 수준의 개인 경제 의사결정 운영체제**를 만드는 것이다.

---

# End of Master Instruction
