---
title: SK Hynix Daily Decision Tracker
created: 2026-08-09
updated: 2026-08-09
tags: [monitoring, sk-hynix, decision-daily, investment-tracking, append-only]
---

# SK Hynix Daily Decision Tracker

**Framework**: [SK Hynix Investment Thesis](../concepts/sk-hynix-investment-thesis.md)

**Current Status**: Monitoring begins 2026-08-09

This page is **append-only** (newest entries at bottom). Each daily check records the investment signal (HOLD/BUY/SELL), confidence level, key drivers, and any conditional triggers that activate.

## Latest Summary (as of 2026-08-09)

**Current Position**: 1,200 shares (HOLD)
**Signal**: Pending first run
**Confidence**: —
**Next Major Check**: After initial pipeline execution

---

## Daily Tracking Log (Reverse Chronological)

### 2026-08-09 10:00
- **Status**: Framework initialized, awaiting first engine run
- **Signal**: —
- **Confidence**: —
- **Key Drivers**:
  - Macro regime: TBD (pending daily PEOS run)
  - Semiconductor band: TBD
  - Rate environment: TBD
- **Triggers**: —
- **Next Check**: Same day after report generation

---

## Concept Framework

### Decision Hierarchy
1. **Macro Regime** (Primary): 상승(BUY) > 조정(HOLD) > 약세(SELL) > 위기(SELL)
2. **Semiconductor Health** (Secondary): Bands 양호/정상/부진/극악 modulate signals
3. **Rate Environment** (Gating): Easing supports, Tightening discourages ENTER/BUY
4. **External Signals** (Conditions): Foreign flows, HBM ASP, CapEx cycle trigger actions

### Conditional Triggers (Not Auto-Executed)
- **Price < 1,400K** (if macro 상승/조정 + Conf ≥ 70%): 추가 매수 200주
- **Price < 1,200K** (if semis 양호 + rate ≥ 완화): 적극 매수 300주
- **Foreign -6조↓** (1-month cumulative outflow): 방어모드 50% 감량
- **HBM ASP ↓ 5%+** (sustained decline): 수익실현 300주 매도
- **Macro 약세전환**: 긴급 재평가

### Risk Management
- Position floor: 600 shares (40% of current)
- Position ceiling: 1,200 shares (current, no expansion without macro 상승)
- Stop loss philosophy: Evaluate when triggered, do not auto-sell

---

## Sources

- [SK Hynix Investment Thesis](../concepts/sk-hynix-investment-thesis.md) — framework definition
- [SK Hynix Entity](../entities/sk-hynix.md) — current state snapshot
- Daily PEOS Report — macro regime, semiconductor score, rate analysis
- `engine/exporters/sk_hynix_decision.py` — decision engine
