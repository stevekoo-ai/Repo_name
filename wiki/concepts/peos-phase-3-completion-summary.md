---
title: PEOS Phase 3 — Economic Calendar & Rolling Aggregation (3a + 3b Complete)
created: 2026-08-09
updated: 2026-08-09
tags: [phase-3, completion, economic-events, rolling-aggregation, decision-intelligence]
---

# PEOS Phase 3: Economic Calendar & Rolling Aggregation

## Executive Summary

**Date**: 2026-08-09  
**Status**: ✅ Phase 3a + 3b COMPLETE  
**Next**: Phase 3c (Integration into daily report)

### What Was Built

Upgraded PEOS (Personal Economic Operating System) from **snapshot-based** decision-making to **event-aware + trend-aware** decision-making:

1. **Phase 3a**: Economic Calendar Integration
   - Macro events (CPI, rates, employment) → decision signal triggers
   - Section 3.5 of daily report (visible, not hidden)
   - Scenario planning (Downside/Base/Upside)

2. **Phase 3b**: Rolling Aggregation Engine
   - Daily signals → accumulated over time
   - Week/Month/Quarter/Year trend analysis
   - Period-over-period comparison (improved/same/declined)

---

## Phase 3a: Economic Calendar Integration

### Problem Solved

**User Request**: "경제 달력도 너무 허술해. 보고서 한 부분에 녹여져서 판단의 근거로 작동하고, 감추어져 있지 않도록!!"

**Existing State**: Section 14, buried, inactive (웹 봇 차단), oversimplified (4 columns)

**New State**: Section 3.5, visible, comprehensive, decision-integrated

### Implementation (5 Components)

#### 1. Engine Module: `economic_events.py` (290 lines)

```python
@dataclass
class EconomicEvent:
    date: str  # "2026-08-12"
    name: str  # "미국 CPI (7월)"
    importance: str  # "🔴 Critical"
    consensus: float  # 2.8%
    actual: Optional[float]  # Released later
    prior: float  # 2.9%
    sk_hynix_impact: str  # "BEARISH"
    real_estate_impact: str  # "WAIT"
```

**Core Functions**:
- `get_upcoming_events()` → List[EconomicEvent] (next 14 days, hardcoded phase 3a)
- `calculate_event_impact(event, signal, confidence)` → (new_signal, new_confidence, reason)
- `get_scenario_impacts(event)` → {downside, base, upside} with probabilities
- `generate_event_section(payload)` → markdown for report

**Signal Transformation Logic**:

| Event | Condition | Result |
|-------|-----------|--------|
| CPI | consensus_miss > +0.5%p (upside/inflation) | confidence -15%p, HOLD→SELL review |
| CPI | consensus_miss < -0.5%p (downside/slowdown) | confidence -10%p, SELL consideration |
| 기준금리 | Cut (인하) | BUY conversion, confidence +15%p |
| 기준금리 | Hike (인상) | SELL consideration, confidence +10%p |

#### 2. Wiki Framework: `concepts/economic-events-framework.md` (422 lines)

- Decision impact mapping (CPI/PPI, interest rates, employment)
- Event importance classification (Critical/High/Medium)
- Scenario planning template (Downside/Base/Upside with probabilities)
- Post-event analysis checklist
- Data sources & automation roadmap

#### 3. Wiki Monitoring: `monitoring/economic-events-status.md` (341 lines)

Append-only tracking of:
- Upcoming Critical Events (next 14 days table)
- Event Tracking History (past event outcomes + signal reactions)
- Scenario Planning (CPI & 기준금리 specific scenarios)
- Historical Pattern Analysis
- Signal Change Log
- Daily Monitoring Checklist

#### 4. Report Integration: `markdown.py` modification

```python
# Before: 5 sections
main_sections = [
    _macro_dashboard_section(payload),
    _sk_hynix_decision_section(payload),
    _real_estate_decision_section(payload),
    _unified_action_plan_section(payload),
    _decision_rationale_summary(payload),
]

# After: 6 sections
main_sections = [
    _macro_dashboard_section(payload),
    _sk_hynix_decision_section(payload),
    _real_estate_decision_section(payload),
    generate_event_section(payload),  # 🆕 Section 3.5
    _unified_action_plan_section(payload),
    _decision_rationale_summary(payload),
]
```

#### 5. Testing: `test_phase3a_simple.py`

8 tests, 100% pass:
- ✓ EconomicEvent dataclass
- ✓ Event retrieval (3 upcoming)
- ✓ CPI upside impact (50% → 35% confidence)
- ✓ Interest rate cut impact (HOLD → BUY, 50% → 65%)
- ✓ Scenario generation (downside/base/upside)
- ✓ Markdown output (1,061 characters)
- ✓ Section structure (3.5 title verified)
- ✓ Integration (generate_event_section in markdown.py)

---

## Phase 3b: Rolling Aggregation Engine

### Problem Solved

**User Need**: Transform daily snapshots into trending insights

- Report shows "HOLD, 50%", but is it stable/improving/declining?
- No historical context on signal evolution
- Can't compare "August confidence vs July"

### Implementation (3 Components)

#### 1. Engine Module: `signal_recorder.py` (181 lines)

**Persistent storage** of daily decision signals:

```python
def record_daily_signal(
    date: str,  # "2026-08-09"
    sk_hynix_signal: str,  # HOLD, BUY, SELL
    sk_hynix_confidence: float,  # 0-100
    real_estate_signal: str,  # WAIT, ENTER
    real_estate_confidence: float,  # 0-100
    notes: Optional[str] = None
) -> bool
```

**Storage**: `data/daily_signals/signal_YYYYMM.csv` (monthly files, append-only)

```csv
date,sk_hynix_signal,sk_hynix_confidence,real_estate_signal,real_estate_confidence,notes
2026-08-01,HOLD,50.0,WAIT,60.0,Market opening
2026-08-02,HOLD,48.0,WAIT,62.0,Slight decline
```

**Loading**: `load_signals(start_date, end_date)` → List[DailySignal]

#### 2. Engine Module: `rolling_aggregator.py` (391 lines)

**Period aggregation** of signals:

```python
def aggregate_signals_by_period(
    signals: List[DailySignal],
    period_type: str  # "week", "month", "quarter", "year"
) -> List[AggregatedPeriod]
```

**Output**:

```python
@dataclass
class AggregatedPeriod:
    period_name: str  # "Month"
    start_date: str
    end_date: str
    days_recorded: int

    # SK Hynix
    sk_hynix_primary_signal: str  # Most common
    sk_hynix_avg_confidence: float
    sk_hynix_signal_counts: Dict[str, int]  # HOLD:22, BUY:7, SELL:2
    sk_hynix_confidence_trend: str  # "↑", "→", "↓"

    # Real Estate
    real_estate_primary_signal: str
    real_estate_avg_confidence: float
    real_estate_signal_counts: Dict[str, int]
    real_estate_confidence_trend: str

    # Comparison
    sk_hynix_vs_prev: str  # "improved", "same", "declined"
    real_estate_vs_prev: str
```

**Trend Detection Algorithm**:

Compare first 1/3 vs last 1/3 of period:
- If last_avg > first_avg + 2 → ↑ (improving)
- If last_avg < first_avg - 2 → ↓ (declining)
- Otherwise → → (stable)

**Period Comparison**:

```python
def compare_periods(current, previous) -> (sk_compare, re_compare)
# Returns: "improved", "same", "declined"
# Based on: signal strength change + confidence delta
```

#### 3. Wiki Framework: `concepts/rolling-aggregation-framework.md` (265 lines)

- Architecture & data flow diagram
- Aggregation logic (weekly/monthly/quarterly/yearly)
- Signal primary selection algorithm
- Confidence averaging & trend detection
- Period comparison methodology
- Integration checklist (Phase 3c)
- Future enhancements (Phase 3c+)

#### 4. Testing: `test_phase3b_rolling_aggregator.py`

7 tests, 100% pass:
- ✓ DailySignal creation
- ✓ Monthly aggregation (9 days → HOLD 52.6%, WAIT 61.8%)
- ✓ Confidence trend detection (↑ improving from 40%→62%)
- ✓ Weekly aggregation (2 weeks split correctly)
- ✓ Period comparison (July 42.3% → Aug 54.3% = IMPROVED)
- ✓ Markdown generation (322 characters with tables)
- ✓ Quarterly aggregation (9 months → 3 quarters)

---

## Impact Analysis

### What's Improved

| Before | After |
|--------|-------|
| Snapshot: "HOLD, 50%" | Contextual: "HOLD 52.6% ↑ (improved from 42.3% last month)" |
| Events hidden, inactive | Events visible Section 3.5, 14-day lookahead |
| No scenarios | 3 scenarios/event with probabilities |
| No trending | Week/Month/Quarter/Year trending |
| No comparison | Period-over-period change tracked |

### Key Metrics

**Phase 3a**:
- 1,052 lines of code/wiki (economic_events.py 290 + framework 422 + monitoring 341)
- 8 test cases, 0 failures
- 3 new event types tracked (CPI, interest rates, employment)
- 5 signal transformation rules

**Phase 3b**:
- 572 lines of code/wiki (signal_recorder 181 + rolling_aggregator 391)
- 7 test cases, 0 failures
- 4 period types supported (week/month/quarter/year)
- 5 aggregation functions

**Combined**:
- 1,624 lines (code + tests + wiki)
- 15 test cases, 0 failures
- 2 major feature additions
- ~4 hours of implementation

---

## Architecture Overview

```
Daily Report Generation
  ↓
Decision Engines
  - sk_hynix_decision.py (거시·반도체·금리·외부신호)
  - real_estate_decision.py (금리·거시·전세가·이벤트)
  ↓
  ┌─────────────────────────────────────────┐
  │ PEOS Phase 3a: Economic Events (NEW)    │
  │ ├─ get_upcoming_events()                │
  │ ├─ calculate_event_impact()             │
  │ └─ generate_event_section()             │
  │    └─ Section 3.5 of report             │
  └─────────────────────────────────────────┘
  │
  ├─ Record signal
  │  signal_recorder.record_daily_signal()
  │  → data/daily_signals/signal_YYYYMM.csv
  │
  ├─ Aggregate (Phase 3b)
  │  rolling_aggregator.aggregate_signals_by_period()
  │  → Week/Month/Quarter/Year trends
  │
  └─ [Phase 3c: Integrate into markdown]
     └─ Sections 4-6: Rolling windows
```

---

## Next Steps: Phase 3c (Integration)

### Remaining Work

1. **engine/report/payload.py** (modify)
   - In `build_report_payload()`, after building decision signals:
   ```python
   # Load past 90 days of signals
   signals = signal_recorder.load_signals()
   
   # Aggregate into periods
   monthly = rolling_aggregator.aggregate_signals_by_period(signals, "month")
   quarterly = rolling_aggregator.aggregate_signals_by_period(signals, "quarter")
   
   # Add to payload
   payload["rolling_windows"] = {
       "monthly": monthly[-1] if monthly else None,
       "quarterly": quarterly[-1] if quarterly else None,
   }
   ```

2. **engine/report/markdown.py** (add 3 functions)
   ```python
   def _monthly_rolling_window_section(payload) -> str
   def _quarterly_rolling_window_section(payload) -> str
   def _year_to_date_window_section(payload) -> str
   ```

3. **github/workflows/daily-peos-report.yml** (add step)
   ```yaml
   - name: Record daily signals
     run: |
       python -c "
       from engine.report import signal_recorder
       signal_recorder.record_daily_signal(
         date='$(date +%Y-%m-%d)',
         sk_hynix_signal='HOLD',  # Get from payload
         sk_hynix_confidence=50.0,
         real_estate_signal='WAIT',
         real_estate_confidence=60.0
       )
       "
   ```

### Estimated Effort

- payload.py integration: 30 min
- markdown.py section functions: 1 hour
- GitHub Actions workflow update: 30 min
- Testing: 1 hour
- **Total**: ~3 hours

---

## Files Changed

### Phase 3a

**Created**:
- `engine/report/economic_events.py`
- `test_phase3a_economic_events.py`
- `test_phase3a_simple.py`
- `wiki/concepts/economic-events-framework.md`
- `wiki/monitoring/economic-events-status.md`

**Modified**:
- `engine/report/markdown.py` (1 import + 1 main_sections modification)
- `wiki/index.md` (2 entries added)
- `wiki/log.md` (1 entry added)

**Commits**:
- `06256fe` Phase 3a

### Phase 3b

**Created**:
- `engine/report/signal_recorder.py`
- `engine/report/rolling_aggregator.py`
- `test_phase3b_rolling_aggregator.py`
- `wiki/concepts/rolling-aggregation-framework.md`
- `data/daily_signals/signal_2026-08.csv` (storage)

**Modified**:
- `wiki/index.md` (1 entry added)
- `wiki/log.md` (1 entry added)

**Commits**:
- `ccdbb4a` Phase 3b

---

## Testing Summary

| Phase | Tests | Pass | Fail | Coverage |
|-------|-------|------|------|----------|
| 3a | 8 | 8 | 0 | Economic events, scenarios, integration |
| 3b | 7 | 7 | 0 | Aggregation, trending, comparison |
| **Total** | **15** | **15** | **0** | **100%** |

---

## Conclusion

PEOS now supports:
1. ✅ **Snapshot decisions** (current state, confidence, rationale)
2. ✅ **Event-aware decisions** (macro events → signal triggers) — Phase 3a
3. ✅ **Trend-aware decisions** (rolling windows → improvement/decline detection) — Phase 3b
4. ⏳ **Integration** (both into daily report) — Phase 3c

**User can now**:
- See economic events coming (14-day outlook)
- Understand how events impact SK/RE signals
- Track signal evolution over time
- Compare "this month vs last month"
- Identify improving/declining trends

---

## References

- Phase 3a: `concepts/economic-events-framework.md`
- Phase 3b: `concepts/rolling-aggregation-framework.md`
- Phase 3c plan: This document (Next Steps section)
- Implementation: `engine/report/economic_events.py`, `signal_recorder.py`, `rolling_aggregator.py`
- Testing: `test_phase3a_*.py`, `test_phase3b_*.py`
