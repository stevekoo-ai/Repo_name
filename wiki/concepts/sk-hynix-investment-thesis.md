---
title: SK Hynix Investment Thesis
created: 2026-08-09
updated: 2026-08-09
tags: [investment, sk-hynix, decision-framework, semiconductor, portfolio]
---

# SK Hynix Investment Thesis

## Framework Overview

This page defines the investment decision framework for SK Hynix stock holdings (1,200 shares, ~180M KRW, 35% portfolio weight).

The thesis bridges macro economic signals, semiconductor industry cycles (HBM market), and personal portfolio constraints to arrive at actionable HOLD/BUY/SELL signals.

## Decision Hierarchy

### Layer 0: Valuation Band (근사치, 2026-08-09 추가)

**출처**: 사용자가 외부(Gemini 생성) 프로젝트 스펙(`Project_SKH_Alpha_Prompt.md`)을
업로드하며 별도의 yfinance/DART 기반 독립 퀀트 시스템 구축을 요청 — 검토 결과
기존 4계층 엔진과 중복되는 시스템이 될 위험이 커서(이미 거시국면 판정이
G/I/L·Investment Clock·PEOS 3개로 나뉘어 혼란스러운 전례 있음), 사용자
승인 하에 **새 지표(P/E Z-score, ERP)만 추출해 기존 엔진에 통합**하는
방식으로 진행. 첨부 스펙의 나머지 지표(수출모멘텀·외국인수급)는 이미
`hbm-cycle-score.md`·`macro-indicators.md`가 자동 추적 중이라 재사용.

- **P/E Z-score(근사)**: 실제 P/E가 아니라 [rally-justification-analysis.md](rally-justification-analysis.md)의
  이격도(divergence = log₁₀(주가지수) - log₁₀(영업이익지수), 24Q1=100 기준)
  시계열의 Z-score. 실제 PER 계산에 필요한 발행주식수 시계열이 미검증
  (2025 자사주 소각 ~2.1%, 2026 ADR 신주발행·자사주 매입 ~40조 등으로
  최근 2년간 변동)이라 대체 채택 — 방향은 동일(양수=고평가 방향,
  음수=저평가 방향)하나 절대 PER 수치는 아님.
  - Z ≤ -1.5: 저평가 극단(밸류에이션 관점 매수 매력)
  - Z ≥ +1.5: 고평가 극단(밸류에이션 관점 수익실현 검토)
  - **2026-08-09 현재값: Z ≈ 1.06(중립)**, 26Q2(6월 말) 이격도 -0.108 —
    26Q1(-0.207)보다 고평가 방향으로 이동(6월 사상최고 2,987,000원까지
    선반영 랠리와 일치).
  - ⚠️ 샘플 10개 분기뿐(24Q1~26Q2) — 표준 밴드(5~10년, 20~40분기) 대비
    부족, 방향성 참고용.
- **ERP(Equity Risk Premium)**: Earnings Yield(선행PER 6.8~6.9배 앵커 기반
  근사) - 미국 10년물 국채(FRED DGS10). **2026-08-09 기준 아직 미산출**
  — `us_10y` 시리즈를 `scripts/macro_data.py`에 신규 등록, `macro-data-sync.yml`
  다음 실행부터 자동 수집 시작. ⚠️ 원화자산에 달러 무위험금리를 쓰는
  방법론적 한계 있음(사용자 원안 그대로 채택 — 글로벌 반도체 밸류에이션
  비교 관행).
- **동작 방식**: 이 계층은 다른 계층의 신호를 뒤집지 않음 — 극단치일 때만
  `risk_flags`/`triggers`에 참고 정보로 추가되고, confidence는 자동
  조정하지 않는다(기계적 매도 자동집행 위험 방지, 최종 판단은 사람이).
- 구현: `engine/valuation/hynix_band.py`, 원자료: `sources/sk-hynix-quarterly-fundamentals.csv`

### Layer 1: Macro Regime (Primary Driver)
- **상승 (Bullish)**: Base case HOLD, BUY on dips if HBM score ≥ 양호
- **조정 (Adjustment)**: Cautious HOLD, BUY if Kr confidence ≥ 70% + rate score ≥ 55
- **약세 (Bearish)**: Default SELL, 방어모드 (50% trim consideration)
- **위기 (Crisis)**: Immediate SELL signal, 25-50% reduction

### Layer 2: Semiconductor Health (Secondary Driver)
- **양호 (Healthy)**: Supports BUY, enable position expansion
- **정상 (Neutral)**: Allows HOLD, no directional bias
- **부진 (Weak)**: Triggers SELL, profit-taking mode
- **극악 (Severe)**: Forced SELL, 30% immediate reduction

### Layer 3: Financial Conditions (Gating Mechanism)
- **Extreme Easing (점수 ≥ 80)**: Enables BUY, reduces cost of carry
- **Easing (70~79)**: Supports BUY thesis
- **Neutral (55~69)**: Allows HOLD, risk-neutral positioning
- **Tightening (40~54)**: Caution mode, reduce leverage exposure
- **Extreme Tightening (<40)**: Defensive posture, consider reduction

### Layer 4: External Signals (Conditional Triggers)
- Foreign investor flows: Track as early warning for sentiment shift
- HBM ASP trend: Monitor for margin sustainability
- US CapEx cycle: Proxy for memory demand outlook
- Currency moves: USD strength = export advantage, risk of margin compression

## Decision Tree

```
START: Macro Regime Check
├─ 위기 → SELL (80% confidence) + 25% reduction
├─ 약세 → SELL (70% confidence) + 50% reduction
├─ 상승
│  ├─ Confidence ≥ 75% + Semis ≥ 양호 → BUY (75%)
│  ├─ Confidence ≥ 75% + Semis = 정상 → HOLD (70%)
│  └─ Confidence < 75% → HOLD (65%)
└─ 조정
   ├─ Confidence ≥ 70% + Rate Score ≥ 55 → BUY (60%)
   ├─ Confidence ≥ 70% → HOLD (65%)
   └─ Confidence < 70% → HOLD (50%)

MODIFIER: Semiconductor Downgrade
├─ 부진 → force SELL (70% confidence)
└─ 극악 → force SELL + 30% reduction (80% confidence)

MODIFIER: Rate Environment
├─ Score < 40 (Extreme Tightening)
│  └─ reduce confidence by 15%p, shift BUY → HOLD
├─ Score ≥ 70 (Easing)
│  └─ +10%p confidence bonus if HOLD/BUY
└─ 40-70 → neutral

OUTPUT: Signal + Triggers + Confidence + Risk Flags
```

## Conditional Triggers (Preconditions Required)

Each trigger fires only when its precondition is met. Prices are reference levels, not hard stops.

| Trigger | Precondition | Action | Urgency |
|---------|--------------|--------|---------|
| **Price < 1,400K** | Macro 상승/조정 + Kr Conf ≥ 70% | 추가 매수 200주 | 높음 |
| **Price < 1,200K** | Semis ≥ 양호 + Rate ≥ 완화 | 적극 매수 300주 | 최고 |
| **Foreign -6조↓** | 1개월 누적 유출 | 방어모드: 50% 감량 | 높음 |
| **HBM ASP ↓ 5%+** | 연속 하락신호 | 수익실현 300주 매도 | 중간 |
| **Macro 약세전환** | 신뢰도 하락 + 지표악화 | 긴급 평가 | 최고 |

## Risk Management Rules

### Position Sizing
- Never increase position above 1,200 shares without explicit macro upgrade to "상승" (70%+ Conf)
- Never reduce below 600 shares without explicit macro downgrade to "약세" or lower

### Stop Losses (Not Implemented Yet)
- Technical stop at 1,100K (10% below current): evaluate but do not auto-sell
- Fundamental stop at "위기" macro or Semis "극악": prompt SELL evaluation within 24h

### Portfolio Constraint
- SK Hynix ≤ 40% portfolio weight (currently 35%)
- If price appreciates significantly: consider profit-taking to rebalance

## Macro-Semiconductor Linkage Patterns

### US CapEx ↑ → Memory Demand ↑
- Signal: US 지출 증가, IT 업종 선도주 모멘텀
- Impact: HBM 수요 지속 → ASP 강세 → Hynix 이윤율 확대
- Timing: 6-9개월 lead lag

### Interest Rate ↓ → Tech Investment Cycle ↑
- Signal: 기준금리 인하, 장기금리 하향
- Impact: 설비투자 심화 → 메모리 수요 ↑ → ASP 상향
- Timing: 2-3개월

### Foreign Investor Retreat ← Macro "약세"
- Signal: 한국 거시신뢰도 하락, 외국인 순매도
- Impact: Hynix 수급 악화 → 주가 약세 → 기술주 선회
- Timing: 1-2주

### Competition (CXMT) Pressures ASP ↓
- Signal: 중국 DRAM 수출 가속, pricing pressure in spot market
- Impact: 전사 수익성 악화, margin pressure on HBM
- Timing: 3-6개월 (경보 단계)

## Framework Maintenance

### Triggers for Thesis Revision
- [ ] Macro regime changes for 2+ consecutive weeks
- [ ] Semiconductor band moves 2+ tiers (e.g., 양호 → 부진)
- [ ] Rate environment crosses major threshold (e.g., 70 → 55, 40 → 60)
- [ ] Foreign net flows reverse by >2조 KRW
- [ ] CXMT market share reaches 15%+ (currently ~8%)

### Data Sources
- Macro regime: `wiki/entities/korea-macro-regime.md` (updated monthly)
- Semiconductor score: `engine/personal/mapping.py` (daily)
- Rate environment: `engine/rate_analysis/scoring.py` (daily)
- Foreign flows: SK Hynix ADR cross-check vs domestic volume
- HBM ASP: SK Hynix guidance + analyst reports (monthly)

## Sources

- [SK Hynix Analyst Thesis Checkpoints](../entities/sk-hynix.md) — current state snapshot
- [SK Hynix Decision Tracker](../monitoring/sk-hynix-decision-tracker.md) — daily decision log
- [Korea Macro Regime](../entities/korea-macro-regime.md) — macro framework
- [SK하이닉스 주가 상승의 정당성 분석](rally-justification-analysis.md) — Layer 0 divergence 시계열 원본
- `engine/exporters/sk_hynix_decision.py` — decision engine implementation
- `engine/valuation/hynix_band.py` — Layer 0 (P/E Z-score 근사 + ERP) 구현
- `sources/sk-hynix-quarterly-fundamentals.csv` — Layer 0 원자료 (분기별 영업이익·종가)
