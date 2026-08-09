---
title: Rolling Aggregation Framework — Monthly/Quarterly Trending
created: 2026-08-09
updated: 2026-08-09
tags: [phase-3b, aggregation, trending, decision-intelligence]
---

# Rolling Aggregation Framework

## Purpose

Transform daily decision signals (SK Hynix HOLD/BUY/SELL + confidence, Real Estate WAIT/ENTER + confidence) into rolling windows (Week/Month/Quarter/Year) to identify trends and compare periods.

**Goal**: Move from snapshot decision-making → trend-aware decision-making by showing how signals have evolved over time.

---

## 1. Architecture

### 1.1 Data Flow

```
Daily Report
  ↓
  Decision Engines (sk_hynix_decision.py + real_estate_decision.py)
  ↓
  Signal Recorder (signal_recorder.py)
    ↓
    CSV append: data/daily_signals/signal_YYYYMM.csv
  ↓
  Rolling Aggregator (rolling_aggregator.py)
    ↓
    Load past 90 days + aggregate by period
  ↓
  Markdown Renderer
    ↓
    Section 4: Rolling Windows (Month/Quarter/Year)
```

### 1.2 Key Components

#### Signal Recorder (`signal_recorder.py`)

- **Function**: `record_daily_signal(date, sk_signal, sk_confidence, re_signal, re_confidence, notes)`
- **Storage**: CSV files under `data/daily_signals/signal_YYYYMM.csv` (monthly files)
- **Pattern**: Append-only (one row per day, never overwrite)
- **Fields**: date, sk_hynix_signal, sk_hynix_confidence, real_estate_signal, real_estate_confidence, notes

#### Rolling Aggregator (`rolling_aggregator.py`)

- **Input**: List of DailySignal records (load from CSV via signal_recorder.load_signals())
- **Processing**: Aggregate by week/month/quarter/year
- **Output**: AggregatedPeriod dataclass with:
  - Primary signal (most common)
  - Average confidence
  - Signal counts (distribution)
  - Confidence trend (↑/→/↓)
  - Period-over-period comparison

---

## 2. Aggregation Logic

### 2.1 Period Definition

| Period | Definition | Example |
|--------|------------|---------|
| Week | ISO week (Mon-Sun) | 2026-W32 |
| Month | Calendar month | 2026-08 |
| Quarter | Q1-Q4 | 2026-Q3 |
| Year | Calendar year | 2026 |

### 2.2 Signal Primary Selection

**SK Hynix / Real Estate**: Most common signal over the period.

If HOLD=15, BUY=5, SELL=0 → primary = HOLD

### 2.3 Confidence Averaging

Simple arithmetic mean of daily confidence values.

Example: 50%, 48%, 45%, 50%, 52% → avg = 49%

### 2.4 Confidence Trend

Compare first 1/3 vs last 1/3 of period:

- If last_avg > first_avg + 2 → ↑ (improving)
- If last_avg < first_avg - 2 → ↓ (declining)
- Otherwise → → (stable)

### 2.5 Period Comparison

Compare current period vs previous period:

- **Signal Strength Change**: SELL(0) < HOLD(1) < BUY(2)
  - Example: HOLD(1) → BUY(2) = improvement
- **Confidence Difference**: >+5%p = improved, <-5%p = declined, else = same

---

## 3. Rolling Window Sections

Three new markdown sections appear after Section 3.5 (Economic Events):

### 3.1 Monthly Rolling Window

```
## 📊 Month Rolling Window (2026-08-01 ~ 2026-08-31)

**기간**: 31일 기록

### SK Hynix: 보유/매도 추적

| 지표 | 값 |
|------|--------|
| 주요신호 | HOLD |
| 평균신뢰도 | 50.4% ↑ |
| HOLD | 22일 |
| BUY | 7일 |
| SELL | 2일 |

### Real Estate: 진입/대기 추적

| 지표 | 값 |
|------|--------|
| 주요신호 | WAIT |
| 평균신뢰도 | 61.2% → |
| WAIT | 28일 |
| ENTER | 3일 |

### Period Comparison

- **SK Hynix**: IMPROVED (이전 월: HOLD 45%)
- **Real Estate**: SAME (이전 월: WAIT 61%)
```

### 3.2 Quarterly Rolling Window

Aggregates 3 months into single quarter.

### 3.3 Year-to-Date Rolling Window

Aggregates entire year's signals.

---

## 4. Integration Checklist

### Phase 3b Implementation

- [ ] **engine/report/signal_recorder.py** (완료)
  - `record_daily_signal()` 함수 구현
  - `load_signals()` 함수 구현
  - CSV append 메커니즘 구현

- [ ] **engine/report/rolling_aggregator.py** (완료)
  - `DailySignal` / `AggregatedPeriod` dataclass
  - `aggregate_signals_by_period()` 함수
  - `compare_periods()` 함수
  - `generate_rolling_window_markdown()` 함수

- [ ] **engine/report/payload.py** (필요한 수정)
  - `build_report_payload()` 마지막에 rolling aggregator 호출
  - Monthly / Quarterly / YTD 데이터 payload에 추가

- [ ] **engine/report/markdown.py** (필요한 수정)
  - 3개 rolling window section 함수 신설
  - Section 4-6에 삽입 (economic events 이후)

- [ ] **github/workflows/daily-peos-report.yml** (필요한 수정)
  - 매일 신호 기록: `signal_recorder.record_daily_signal()`호출

### Phase 3b Test Cases

- [ ] test_phase3b_aggregation.py
  - Signal aggregation by period
  - Trend calculation (↑/→/↓)
  - Period comparison logic
  - Markdown generation
  - All tests: 100% pass

---

## 5. Future Enhancements (Phase 3c+)

### 5.1 Multi-Year Trending

Extend lookback from 90 days → 2 years for annual patterns.

### 5.2 Event Correlation

Link rolling window trends to economic events:

- "CPI spike on 2026-08-12 → SK confidence -15%p next week"

### 5.3 Signal Momentum

Derivative of confidence: dConfidence/dWeek (acceleration/deceleration)

### 5.4 Rolling Windows Dashboard

Interactive HTML page showing:
- Line charts: confidence over time
- Waterfall: period-over-period change
- Heatmap: signal dominance by week

---

## 6. Example: August 2026 Reconstruction

**Scenario**: User requests "지난 한 달 의사결정 추이를 보여줘"

```
1. load_signals(start="2026-07-10", end="2026-08-09")
   ↓
2. aggregate_signals_by_period([signals], "month")
   ↓
3. Result:
   {
     "July": {
       "SK": HOLD (45% confidence), counts={HOLD:15, BUY:10, SELL:0}
       "RE": WAIT (62% confidence), counts={WAIT:22, ENTER:3}
     },
     "Aug (partial)": {
       "SK": HOLD (52% confidence), counts={HOLD:6, BUY:3, SELL:0}
       "RE": WAIT (62% confidence), counts={WAIT:7, ENTER:2}
     }
   }
   ↓
4. compare_periods(aug_partial, july)
   → SK: "improved" (45% → 52%)
   → RE: "same" (62% → 62%)
   ↓
5. Markdown output in report Section 4
```

---

## References

- `engine/report/signal_recorder.py` — Signal persistence
- `engine/report/rolling_aggregator.py` — Aggregation & comparison
- `engine/report/payload.py` — Integration point
- `engine/report/markdown.py` — Rendering
- `wiki/monitoring/sk-hynix-decision-tracker.md` — Daily signal journal
- `wiki/monitoring/real-estate-decision-tracker.md` — Daily signal journal

---

## Maintenance

- **Last Updated**: 2026-08-09 (Framework definition)
- **Implementation Status**: Phase 3b IN PROGRESS
- **Next Milestone**: Integration into daily report (Phase 3b complete)
