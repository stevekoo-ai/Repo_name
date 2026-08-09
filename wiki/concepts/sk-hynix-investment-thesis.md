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
- `engine/exporters/sk_hynix_decision.py` — decision engine implementation
