---
title: Knowledge Model — 4-Layer Wiki Architecture
created: 2026-08-08
updated: 2026-08-08
tags: [architecture, knowledge-model, 4-layer]
---

# Knowledge Model: The 4-Layer Wiki System

This document explains how the wiki organizes and represents knowledge in a 4-layer separation model that eliminates duplication while preserving full history and decision-making support.

## The Problem (Before 4-Layer)

Before August 2026, the wiki mixed two concepts in every file:
- **Current state** — "What is SK하이닉스 valued at right now?"
- **Historical timeline** — "What were all the price/news events from July-August?"

This caused:
1. **Data duplication** — same facts recorded in entity files, concept files, log.md, and monitoring simultaneously
2. **File bloat** — SK하이닉스 entity grew to 1,255 lines mixing current state (5 lines) with 30+ dated entries (1,200 lines)
3. **Token waste** — loading one entity for a current-state question consumed 24,000+ tokens of history
4. **Single Source of Truth violation** — updates in one place weren't reflected elsewhere, creating divergence

## The Solution: 4-Layer Architecture

The wiki now separates concerns into 4 independent, interlinked layers:

```
┌─────────────────────────────────────────────┐
│  ENTITY (Current State Only)                │  Layer 1
│  entities/sk-hynix.md ~82 lines             │
│  "최근 상태: 1,436,000원, -3.95% (8/7)"     │
└────────────┬────────────────────────────────┘
             │ links to
             ↓
┌─────────────────────────────────────────────┐
│  ENTITY JOURNAL (Historical Timeline)       │  Layer 2
│  entity-journals/sk-hynix-journal.md        │
│  ~1,209 lines, all entries since 2026-07-13│
│  Append-only audit trail                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  CONCEPT (Framework Definition)             │  Layer 3
│  concepts/hbm-cycle-score.md ~150 lines     │
│  "0-100 scale, 4 axes, collapse rules"      │
└────────────┬────────────────────────────────┘
             │ links to
             ↓
┌─────────────────────────────────────────────┐
│  MONITORING (Daily Tracking & Status)       │  Layer 4
│  monitoring/hbm-cycle-score-status.md       │
│  Today's score + dated log of changes       │
│  Append-only tracking ledger                │
└─────────────────────────────────────────────┘
```

## Layer Definitions

### Layer 1: Entity — Current State Only

**Purpose**: Single, authoritative snapshot of an entity's current state.

**What belongs here**:
- One-paragraph summary of current status
- Key metrics table (6–10 rows, current values only)
- "Last verified" metadata
- Link to entity-journal for history

**What does NOT belong here**:
- Dated entries or historical narrative
- "3 months ago..." or "previously..."
- Revisions/corrections marked with dates
- Complete timeline of changes

**Example**: `entities/sk-hynix.md` (82 lines)
- Frontmatter
- Current state: "반도체 제조사. 최근 상태: 1,436,000원(-3.95%, 8/7)"
- Metrics table
- "다음에 볼 것" watch list
- Link to entity-journals/

**Size Expectation**: 50–300 lines (fit on one screen)

**Update Rule**: Only update when the entity's actual state changes, not when reviewed.

---

### Layer 2: Entity Journal — Historical Timeline

**Purpose**: Complete audit trail of all state changes, organized reverse-chronologically (newest first).

**What belongs here**:
- Every dated observation/event since entity creation
- State transitions with rationale
- Corrections and revisions (preserves history of changes)
- Full details of events that entity-current-state summarizes

**What does NOT belong here**:
- Framework definitions or methodology
- Forward-looking analysis or predictions
- Monitoring scores (those go in monitoring/)

**Example**: `entity-journals/sk-hynix-journal.md` (1,209 lines)
- Frontmatter
- Header: "SK하이닉스 — 주가·펀더멘털 변화 일지"
- 1,188 dated entries, reverse-chronological (newest 2026-08-08, oldest 2026-07-13)
- Back-link to entity current state

**Design**: Append-only, never edited. Once an entry is added, it stays forever (audit trail property).

**Size Expectation**: Unbounded. Growth is expected. Monthly rotation to e.g., `sk-hynix-2026-07.md` when >100KB.

**Update Rule**: Append a new dated entry whenever entity state changes.

---

### Layer 3: Concept — Framework Only

**Purpose**: Stable definition of a recurring idea, methodology, or analytical framework.

**What belongs here**:
- Concept definition and scope
- Calculation/evaluation methodology
- Invariant thresholds or conditions (rarely change)
- Relationships to other concepts
- Link to monitoring/ for daily tracking

**What does NOT belong here**:
- Today's score or daily status (goes in monitoring/)
- Dated check history or verification log (goes in monitoring/)
- Event-specific observations (go in entities/)

**Example**: `concepts/hbm-cycle-score.md` (framework only, ~100 lines)
- Frontmatter
- "HBM Cycle Score Definition: 0–100 scale"
- "4 axes: Supply, Demand, Technical, Sentiment"
- "Collapse conditions (5): ASP, Nvidia, CoWoS, foreign flows, export growth"
- "Relationship to [macro-indicators.md](#)..."
- "Daily tracking: See [monitoring/hbm-cycle-score-status.md](../monitoring/hbm-cycle-score-status.md)"
- Sources

**Design**: Framework updates only when the concept definition itself changes (rare).

**Size Expectation**: 50–200 lines (framework is stable).

**Update Rule**: Only update when framework definition evolves (requires Concept Lifecycle justification). Do NOT manually edit for daily changes.

---

### Layer 4: Monitoring — Daily Tracking & Status

**Purpose**: Append-only record of daily tracking scores, status, and decision-relevant changes.

**What belongs here**:
- Today's status or score
- Dated log of daily changes (newest at top)
- Why the score changed (rationale tied to concept axes)
- Decision signals ("Buy", "Hold", "Risk Alert")
- Back-link to concept for framework definition

**What does NOT belong here**:
- Framework definition (goes in concept/)
- Historical events not tied to daily decision-making (goes in entity-journal/)

**Example**: `monitoring/hbm-cycle-score-status.md` (daily tracking)
- Frontmatter
- "## Latest Status (2026-08-08 저녁)"
- **Score: 75/100** (Watching)
- **Status**: 경계 (60~80점)
- **Collapse Conditions**: 🔴 1/5 (외국인 20일 누적 순매도 전환)
- "## Check History (reverse chronological)"
- 2026-08-07 entry, 2026-08-06 entry, ...

**Design**: Append-only, never edited. Each day's entry is final (like log.md).

**Size Expectation**: Unbounded. Monthly rotation to `monitoring/hbm-cycle-score-status-2026-07.md` when >100KB.

**Update Rule**: Append a new dated entry whenever status changes or at fixed check cadence (e.g., daily).

---

## How the Layers Relate

### Entity ↔ Entity-Journal (Always Paired)

- **Entity** asks: "What is the current state of SK하이닉스?"
  - Answer: "1,436,000원, -3.95%, near-term risk watch"
  - Read: top of entities/sk-hynix.md (82 lines)

- **Entity-Journal** asks: "How did it get here? What changed from 8/6 to 8/7?"
  - Answer: Full timeline with all events and reasoning
  - Read: entity-journals/sk-hynix-journal.md (click from entity page)

### Concept ↔ Monitoring (Always Paired)

- **Concept** asks: "How is HBM Cycle Score calculated?"
  - Answer: "0–100, 4 axes (Supply/Demand/Technical/Sentiment), 5 collapse conditions"
  - Read: concepts/hbm-cycle-score.md (framework only, ~100 lines)

- **Monitoring** asks: "What is today's HBM Cycle Score?"
  - Answer: "75/100 (Watching), 1/5 collapse conditions met"
  - Read: monitoring/hbm-cycle-score-status.md (today's section)

### Sources ↔ All Layers

- `sources/` (raw inputs) → ingest into Entity/Concept layers
- Entity-Journal and Monitoring layers preserve Sources links to the inputs that triggered state changes

---

## Single Source of Truth (After 4-Layer)

Each fact now lives in exactly one authoritative location:

| Type of Fact | Lives Here | Referenced From |
|---|---|---|
| SK하이닉스 current price | entities/sk-hynix.md | monitoring pages, decision logs |
| SK하이닉스 8/7 price-drop event | entity-journals/sk-hynix-journal.md | (not duplicated elsewhere) |
| HBM Score definition & axes | concepts/hbm-cycle-score.md | (framework is canonical) |
| HBM Score today's value | monitoring/hbm-cycle-score-status.md | (not in concept) |

This prevents drift: update one place, all references are fresh.

---

## Reading Paths by Use Case

### "What is the current state?"
1. Start: Entity page (50–300 lines, under 1 minute read)
2. Example: entities/sk-hynix.md → "1,436,000원, -3.95%, 과매도 근접"

### "What led to this state? What changed?"
1. Start: Entity page
2. Follow: Link to entity-journals/
3. Example: entity-journals/sk-hynix-journal.md → see all events since 7/13

### "How do we score/evaluate this concept?"
1. Start: Concept page (framework only, ~1 min read)
2. Example: concepts/hbm-cycle-score.md → "0–100, 4 axes, 5 collapse conditions"

### "What is today's score? Should we act?"
1. Start: Monitoring page → Latest Status section
2. Deep-dive: Check dated change log to understand why it changed
3. Example: monitoring/hbm-cycle-score-status.md → "75/100 (Watch), 1/5 conditions"

### "Why did the score change between 8/6 and 8/7?"
1. Start: Monitoring page → dated change log
2. Cross-check: Link to concept for axis definitions
3. Example: "외국인 순매도 전환 (④ 조건 충족)" → see concepts/ for what this metric means

---

## Token Efficiency Gains

By separating layers, we eliminate redundant reads:

| Scenario | Old Approach | New Approach | Savings |
|---|---|---|---|
| "What is SK하이닉스 trading at?" | Load 1,255-line entity file (40KB, 20K tokens) | Load 82-line entity file (5KB, 500 tokens) | 95% reduction |
| "How did HBM score get to 75?" | Load 250-line concept with 30+ dated entries | Load 150-line concept + 3-line monitoring status | 40% reduction |
| "Show me all CXMT updates since 7/15" | Grep multiple files (entities, concepts, log) | Read single entity-journal file (ordered, complete) | 60% faster |

Projected annualized savings (10+ entities): ~200K tokens/month when pattern generalizes.

---

## Design Principles

1. **Separation of Concerns**: Entity ≠ Journal; Concept ≠ Monitoring
2. **Single Source of Truth**: Each fact in one authoritative location, referenced from others
3. **Audit Trail**: Journals and monitoring are append-only, preserving complete history
4. **Context Stability**: Current state in 50–300 lines; history one click away
5. **Fast Access**: Pick the right layer for your question, read 1–3 minutes max

---

## Sources

- [Architecture Amendment — 4-Layer Specification](../architecture-amendment-4layer.md)
- [Entity Lifecycle Maturity](../concepts/entity-lifecycle-maturity.md)
- [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md)
- [CLAUDE.md — Workflows](../../CLAUDE.md)
