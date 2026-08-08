---
title: Reporting Framework — Wiki Data to Reports
created: 2026-08-08
updated: 2026-08-08
tags: [reporting, framework, architecture, analytics]
---

# Reporting Framework: How Wiki Data Flows into Reports

This document explains how data from the 4-layer wiki structure is synthesized into reports, dashboards, and decision outputs.

## Reporting Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│  RAW SOURCES (sources/)                                     │
│  News, research, data, transcripts                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
        [INGEST WORKFLOW]
        (CLAUDE.md /ingest)
                 │
    ┌────────────┴────────────┐
    ↓                         ↓
┌─────────────┐        ┌─────────────┐
│ Layer 1: Entity      │ Layer 3: Concept  │
│ (current state)      │ (framework)       │
└────────┬────────────────────┬────────────┘
         │                    │
         ↓                    ↓
    ┌─────────────┐    ┌──────────────┐
    │ Layer 2:    │    │ Layer 4:     │
    │ Entity      │    │ Monitoring   │
    │ Journal     │    │ (daily       │
    │ (history)   │    │  tracking)   │
    └────────────────────────────────┘
         │                 │
         ↓                 ↓
    [REPORT GENERATION]
    (daily/weekly/monthly)
         │
    ┌────┴────────┬───────────┬────────────┐
    ↓             ↓           ↓            ↓
┌────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
│Morning │ │Daily    │ │Weekly   │ │Monthly   │
│Report  │ │Email    │ │Summary  │ │Archive   │
│(HTML)  │ │Summary  │ │(HTML)   │ │(MD)      │
└────────┘ └─────────┘ └─────────┘ └──────────┘
```

---

## Data Flows by Layer

### Layer 1 (Entity Current State) → Reports

**Questions answered**:
- "What is the current state of X?"
- "What changed since last week?"
- "Is X at risk or in opportunity zone?"

**Report sections that use Layer 1**:
- **Morning Status**: Current prices, key metrics, technical levels
- **Watchlist Snapshot**: What we're tracking right now (top of entities/)
- **Decision Summary**: Current state of all active entities

**Example Flow**:
1. Entity page: entities/sk-hynix.md (current state updated 8/7 after -3.95% close)
2. Report generation script reads entities/ folder
3. Morning report includes: "SK하이닉스: 1,436,000원, -3.95% (과매도 근접)"

**Data Freshness**:
- Entity pages updated when state changes (event-driven, not time-driven)
- Reports pull latest entity state → always current

---

### Layer 2 (Entity Journal) → Reports

**Questions answered**:
- "How did we get here?" (state transition narrative)
- "What was the decision made on 8/5 based on?"
- "Are we repeating a pattern from July?"

**Report sections that use Layer 2**:
- **Historical Context**: 1-week, 1-month, 3-month review narratives
- **Decision Rationale**: "Why did score change from X to Y?" (trace through journal entries)
- **Pattern Validation**: "Is this Q3 event similar to Q2?" (cross-journal comparison)
- **Audit Trail**: "Show me every price change for SK하이닉스 from 7/13-8/8"

**Example Flow**:
1. Need for weekly report: "How did SK하이닉스 enter oversold territory?"
2. Read entity-journals/sk-hynix-journal.md → see 8/6 (dropped -10.37%) and 8/5 (+5.77%)
3. Report section: "SK하이닉스는 8/5 반등 이후 8/6-8/7 조정. 선제 매도 압력 vs. 외국인 누적매도 균형 시점."

**Data Freshness**:
- Journal entries appended as state changes occur
- Weekly/monthly reports read completed past entries (stable reference)

---

### Layer 3 (Concept Framework) → Reports

**Questions answered**:
- "How do we evaluate/score this thing?"
- "What are the decision thresholds?"
- "Has our methodology changed?"

**Report sections that use Layer 3**:
- **Framework Definitions**: "HBM Cycle Score is 0-100 based on..."
- **Methodology**: "We track 5 collapse conditions: ASP, Nvidia orders, CoWoS, foreign flows, export growth"
- **Invariant Thresholds**: "Oversold threshold is RSI 30, Warning is RSI 40"
- **Concept Documentation**: Full framework reference (so readers can understand scores)

**Example Flow**:
1. Report writer: "I want to include HBM Cycle Score in morning report"
2. Read concepts/hbm-cycle-score.md → get definition and axes
3. Report section: "## HBM Cycle Score Methodology\n[Insert concept definition]\n[Link to live score below]"

**Data Freshness**:
- Concepts change rarely (every few weeks or months at most)
- Framework reference is evergreen within a report period
- When concept *does* change, it propagates to all future reports

---

### Layer 4 (Monitoring Tracking) → Reports

**Questions answered**:
- "What is today's score?" (current)
- "How did it move from yesterday to today?" (change narrative)
- "Are we hitting alert thresholds?" (decision signals)

**Report sections that use Layer 4**:
- **Daily Status**: "HBM Cycle Score: 75/100 (Watching, ④ condition triggered)"
- **Change Log**: Last 5 days of score movements with rationale
- **Alert Section**: "🔴 1 Red Alert: 외국인 순매도 전환 확정"
- **Trend Arrow**: ↑/↓/→ based on last 3-5 days

**Example Flow**:
1. Daily report generation (8 AM KST)
2. Read monitoring/hbm-cycle-score-status.md → Latest Status section shows "75/100" from 8/7
3. Read dated change log → "8/7: -5 (외국인 누적매도 전환), 8/6: -10 (미국 반도체 약세)"
4. Report: "## HBM Cycle Score: 75/100 ⚠️ (Watching)\n경계 구간. 외국인 순매도 1개 조건 충족. 다음 확인: 8/9"

**Data Freshness**:
- Monitoring pages updated daily (or per-check cadence)
- Reports pull latest monitoring status → always current as of last check

---

## Report Types by Layer Coverage

### Morning Brief (All Layers)

| Layer | Scope | Purpose |
|---|---|---|
| Entity (L1) | Current prices/metrics only | "What's the snapshot right now?" |
| Concept (L3) | Brief framework reference | "Here's how we evaluate it" |
| Monitoring (L4) | Today's score + last 1-2 changes | "Decision signal for today" |

**Not included**: Entity journals (too verbose for daily brief)

---

### Weekly Review (All Layers + Context)

| Layer | Scope | Purpose |
|---|---|---|
| Entity (L1) | Current state vs. week-ago state | "What changed this week?" |
| Entity-Journal (L2) | All entries from past 7 days | "Walk through the week's events" |
| Concept (L3) | Framework (unchanged unless evolved) | "Our evaluation method" |
| Monitoring (L4) | Last 7 days of score evolution | "Score trend for the week" |

---

### Monthly Archive (Selective Layers)

| Layer | Scope | Purpose |
|---|---|---|
| Entity (L1) | Month-end state snapshot | "Where did we end the month?" |
| Entity-Journal (L2) | Rotate/archive month's entries | "Complete month audit trail" |
| Concept (L3) | Framework (if evolved) | "Document any methodology changes" |
| Monitoring (L4) | Rotate/archive month's scores | "Complete month tracking record" |

**Rotation after archiving**:
- Entity-Journal entries for this month → `entity-journals/sk-hynix-2026-07.md`
- Monitoring entries for this month → `monitoring/hbm-cycle-score-status-2026-07.md`
- Concept and current-state entity remain (no rotation)

---

## Common Report Generation Patterns

### Pattern 1: Daily Status (Morning Report)

```
## [Entity] — Daily Status

### Current State (Entity L1)
[Entity current-state summary + key metrics]

### Today's Score (Monitoring L4)
[Latest monitoring status]
- Score: X/100
- Change: [+Y from yesterday]
- Alert: [🔴/🟡/🟢]

### Decision Signal
[Link to concept L3 for methodology]
[Rationale for today's signal]
```

**Queries**:
- Read: `entities/sk-hynix.md` (L1)
- Read: `monitoring/hbm-cycle-score-status.md` (L4, latest status only)
- Reference: `concepts/hbm-cycle-score.md` (L3)

---

### Pattern 2: Weekly Review (Historical Context)

```
## [Entity] — Weekly Review (YYYY-MM-DD to YYYY-MM-DD)

### Week's Summary
[Entity L1 — this week's state change]

### Key Events
[Entity-Journal L2 — dated entries from past 7 days]

### Score Evolution
[Monitoring L4 — daily scores for the week]

### Analysis & Next Week
[Interpretation of patterns seen in Layers 1-4]
```

**Queries**:
- Read: `entities/sk-hynix.md` (L1, current)
- Read: `entity-journals/sk-hynix-journal.md` (L2, filter to past 7 days)
- Read: `monitoring/hbm-cycle-score-status.md` (L4, filter to past 7 days)

---

### Pattern 3: Concept Explanation (Reference Section)

```
## Methodology: [Concept Name]

[Include full concept definition from L3]

### Framework
[Copy-paste concepts/hbm-cycle-score.md]

### Current Tracking
See [monitoring/hbm-cycle-score-status.md](link) for today's status.
```

**Queries**:
- Read: `concepts/hbm-cycle-score.md` (L3, full framework)
- Link to: `monitoring/hbm-cycle-score-status.md` (L4)

---

## Report Generation Guidelines

### DO ✅

1. **Pull current state from Layer 1 (Entity)**
   - Always read entities/ for latest state
   - Use "Last verified" timestamp from entity

2. **Use Layer 2 (Journal) for historical context**
   - Quote dated entries when explaining "why"
   - Filter to relevant time window (last 7/30 days)

3. **Reference Layer 3 (Concept) for methodology**
   - Copy framework definition into reports
   - Link to concept page for full details

4. **Pull Layer 4 (Monitoring) for daily scores**
   - Read "Latest Status" section for current values
   - Include recent dated change log (last 5 entries)

5. **Link between layers**
   - Entity → Journal ("See history")
   - Concept → Monitoring ("See live score")
   - Report → All 4 layers

### DON'T ❌

1. **Don't duplicate Layer 2 in Layer 1**
   - Don't put "8/6: -10.37%, 8/5: +5.77%" in entity current state
   - Keep entity ≤300 lines (move history to journal)

2. **Don't manually edit Monitoring pages for formatting**
   - Monitoring is append-only
   - Format at report-generation time, not source-editing time

3. **Don't put today's score in Concept definition**
   - Concept is framework, not status
   - Score goes in monitoring, not concept

4. **Don't use layers from different dates in the same analysis**
   - Example: Use entity checked-on-8/8 + journal entry from 8/5 ✓
   - Example: Use entity checked-on-8/8 + entity checked-on-8/5 ❌ (pick latest)

---

## Automation Integration

### Automated Report Generation Script (`daily_report.py`, etc.)

**Should follow this pattern**:

```python
# Daily Report Generation

# 1. Load current entity states (Layer 1)
entities = load_all_entities('wiki/entities/')

# 2. Load today's monitoring scores (Layer 4)
monitoring = load_all_monitoring('wiki/monitoring/')

# 3. Generate status section
for entity_name, entity_data in entities.items():
    monitoring_data = monitoring.get(entity_name)
    report += f"## {entity_name}\n"
    report += f"Current: {entity_data['state']}\n"
    report += f"Score: {monitoring_data['today_score']}\n"
    
# 4. Link to concept/journal for detail views
report += f"See [concept](wiki/concepts/{entity_name}-concept.md) for methodology\n"
report += f"See [journal](wiki/entity-journals/{entity_name}-journal.md) for history\n"
```

**Do NOT**:
- Load entity-journals (too verbose for daily)
- Manually format monitoring entries (use append-only entries as-is)
- Update concepts based on daily score (concepts are framework-only)

---

## Reporting Checklist

Before publishing a report:

- [ ] All entity current-state pulled from Layer 1 (entities/)
- [ ] All historical context from Layer 2 (entity-journals/)
- [ ] All methodology from Layer 3 (concepts/)
- [ ] All daily scores from Layer 4 (monitoring/)
- [ ] Cross-layer links functional (entity ↔ journal, concept ↔ monitoring)
- [ ] No dated entries appearing in entity current-state sections
- [ ] No framework changes in monitoring pages
- [ ] Report data is fresh (checked date matches Layer 1/4 update times)

---

## Sources

- [Knowledge Model — 4-Layer Architecture](../concepts/knowledge-model.md)
- [Entity Lifecycle Maturity](../concepts/entity-lifecycle-maturity.md)
- [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md)
- [Architecture Amendment — 4-Layer Specification](../architecture-amendment-4layer.md)
- [CLAUDE.md — Wiki Schema](../../CLAUDE.md)
