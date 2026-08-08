---
title: Wiki Architecture Amendment — 4-Layer Reorganization (2026-08-08)
created: 2026-08-08
updated: 2026-08-08
tags: [architecture, operations, structural-redesign]
---

## Problem Statement

The original 2-layer wiki design (entities/ + concepts/) has evolved into a **hybrid timeline-archive** structure that violates the Single Source of Truth principle:

- **entities/** files have become **Historical Timelines** (chronological journeys from discovery to now), not **Current State** snapshots
  - Example: `sk-hynix.md` is 1,255 lines containing 30+ dated entries spanning 8/3–8/8
  - Makes current state hard to find (buried in the latest entries)
  - Duplicates information already in `sources/` and `concepts/`

- **concepts/** files have evolved into **Daily Dashboards** (scores, monitoring tables, tracking updates), not **Frameworks** (invariant patterns/theories)
  - Example: `hbm-cycle-score.md` contains daily-updated numeric scores
  - Example: `panic-recovery-signals.md` contains dated tracking entries mixed with framework definitions
  - Makes it hard to distinguish framework (reusable theory) from instantaneous state (today's observation)

- **Data is duplicated across multiple locations**:
  - Same fact stated in entity timeline AND in concept monitoring AND in log.md
  - Updates happen in one place but not reflected in others

## Solution: 4-Layer Architecture

```
Layer 1: ENTITY (Current State Only)
└─ entities/sk-hynix.md
   - Latest state as of today
   - Metadata: when state was last verified, next review date
   - Links to entity-journals/ for historical context
   - No dated entries; all entries summarized to prose

Layer 2: ENTITY JOURNAL (Historical Timeline)
└─ entity-journals/sk-hynix-journal.md
   - Chronological log of state changes
   - Every dated entry from entities/sk-hynix.md moves here
   - Append-only (for audit trail)
   - Can be rotated monthly (e.g., entity-journals/sk-hynix-2026-07.md) when too large

Layer 3: CONCEPT (Framework Only)
└─ concepts/hbm-cycle-score.md
   - Definition: what the score means, how it's calculated, invariant assumptions
   - Example thresholds (conceptual, not today's values)
   - Cross-linked references to how the concept applies elsewhere
   - NO daily scores, NO dated tracking entries

Layer 4: MONITORING (Daily Tracking & Scores)
└─ monitoring/hbm-cycle-score-status.md
   - Today's score: 75/100 (updated daily)
   - Today's signal: [example state]
   - Dated entries (same format as old concept pages)
   - Single Source of Truth for "what's today's state"
   - Gets pruned/rotated monthly (monitoring/hbm-cycle-score-2026-08.md)
```

## Migration Strategy

### Step 1: Separate entities/sk-hynix.md

**Keep in entities/sk-hynix.md:**
- Current state (1 prose paragraph, max 300 words)
- Next review date
- Key metadata (last verified: 2026-08-08, next check: 2026-08-10)
- Links to entity-journals/ for "historical record"
- "Sources" section (unchanged)

**Move to entity-journals/sk-hynix-journal.md:**
- All dated entries (## 🟦 2026-08-07, ## 🔴 2026-08-06, etc.)
- Chronological order (oldest first, newest last)
- Frontmatter links back to entities/sk-hynix.md

### Step 2: Separate concepts/\*.md into concepts/ + monitoring/

**In concepts/hbm-cycle-score.md (framework only):**
- "## Definition": what the score measures
- "## Calculation Method": formula, inputs, thresholds (conceptual, not today's state)
- "## Invariant Thresholds": when to escalate, when to calm (framework-level decision rules)
- "## Cross-References": how HBM Cycle Score relates to other concepts
- Example values (illustrative only, not dated)

**New: monitoring/hbm-cycle-score-status.md:**
- "## Latest Score": 75/100 (as of 2026-08-08, next update 2026-08-09)
- "## Status Breakdown": today's axis values (supply, retention, etc.)
- "## Dated Change Log": timestamped entries showing score evolution
- Gets rotated to monitoring/hbm-cycle-score-2026-08.md at month end

### Step 3: Establish Single Source of Truth

For every fact that appears in multiple places, ensure:
1. **One authoritative location** (source of truth)
2. **References only from other locations** (cite, don't duplicate)

Example:
- "SK하이닉스 외국인 보유율 50.77%" lives in: **entity-journals/sk-hynix-journal.md** (dated entry, 2026-08-07 09:50)
- Referenced in: monitoring/market-cycles-status.md (link + inline summary)
- Referenced in: log.md (event summary)
- **NOT repeated verbatim** in concepts/market-cycles-leverage-risk.md (that should link, not duplicate)

## Updated CLAUDE.md Rules

### Entity Page Structure

```
---
title: [Entity Name]
created: YYYY-MM-DD
updated: YYYY-MM-DD (same as last-verified-state)
tags: [...]
---

## Current State

[1-3 sentence summary of entity's present condition]

### Last Verified
- Date: YYYY-MM-DD HH:MM UTC
- Next Review: YYYY-MM-DD (or "ongoing daily checks")

## Related Pages
- History: [entity-journals/foo-journal.md](../entity-journals/foo-journal.md)
- Full record of [entity name's] state changes since [creation date]

## Sources
[unchanged]
```

### Entity Journal Structure

```
---
title: [Entity Name] — Change Journal
created: YYYY-MM-DD (same as entity creation date)
updated: YYYY-MM-DD (updates on every new entry)
tags: [entity-name, journal]
---

## Overview
This is the historical timeline for [Entity Name]. For current state, see [entities/foo.md](../entities/foo.md).

Entries are reverse-chronological (newest first).

## YYYY-MM-DD HH:MM UTC

[Current state as observed]
[What changed since last entry]
[Sources/evidence]

## YYYY-MM-DD HH:MM UTC

[Previous entry]
...
```

### Concept Page Structure (Framework Only)

```
---
title: [Concept Name]
created: YYYY-MM-DD
updated: YYYY-MM-DD (only if framework itself changed)
tags: [concept-discipline, ...]
---

## Definition
[What this concept means, when it applies]

## Calculation / Methodology
[How this framework is applied or scored]

## Invariant Thresholds
| Signal | Threshold | Interpretation |
|---|---|---|
| Example | > 70 | Escalate to action |

## Cross-References
- Related: [Other Concept](...)
- Monitoring Status: [monitoring/foo-status.md](../monitoring/foo-status.md)

## Sources
[Original papers/principles that define this concept]
```

### Monitoring Page Structure

```
---
title: [Concept Name] — Daily Status
created: YYYY-MM-DD (first monitoring entry date)
updated: YYYY-MM-DD (latest update)
tags: [monitoring, ...]
---

## Latest Status (as of YYYY-MM-DD HH:MM UTC)

**Score**: 75/100
**Interpretation**: [What the score means in context]
**Next Update**: YYYY-MM-DD HH:MM UTC (±1 day)

## Today's Breakdown
- **Axis 1**: [component value] (weight: 30%)
- **Axis 2**: [component value] (weight: 40%)
- **Axis 3**: [component value] (weight: 30%)

## Recent Changes (Last 7 Days)

| Date | Score | Change | Reason |
|---|---|---|---|
| 2026-08-08 | 75/100 | +2 | [reason] |
| 2026-08-07 | 73/100 | -5 | [reason] |

## Dated Change Log (Append-Only)

### 2026-08-08 09:50 UTC
[Entry describing today's state and what changed]

### 2026-08-07 19:30 UTC
[Previous entry]

## Sources
- Concept Framework: [concepts/foo.md](../concepts/foo.md)
- Data: [entities/bar.md](../entities/bar.md), [sources/...](../../sources/...)
```

## Migration Timeline

1. **2026-08-08 (today)**:
   - Create entity-journals/ and monitoring/ folders
   - Create this amendment document
   - Begin migration of sk-hynix.md (highest priority, 94KB)

2. **2026-08-09**:
   - Complete sk-hynix.md → sk-hynix-journal.md split
   - Begin migration of HBM Cycle Score and panic-recovery-signals

3. **2026-08-10**:
   - Complete all concept → monitoring splits
   - Audit for duplicate data locations

4. **2026-08-11+**:
   - Index changes in wiki/index.md
   - Update log.md with migration events

## Expected Benefits

| Problem | Before | After |
|---|---|---|
| "Where is current state?" | Buried in latest entries (1,255 lines) | Plainly visible (50-200 lines, top of entity page) |
| "How do I find history?" | Scroll down or search log.md | Click entity-journals/ link from entity page |
| Data Duplication | Same fact in entity + concept + log | Single location, referenced from elsewhere |
| Concept Clarity | "Is this today's score or the formula?" | Concepts = formula; Monitoring = today's score |
| Archive Size | log.md grows 17KB/day, Context bloat | log.md + monitoring/ rotated monthly, Context stays stable |

## References
- [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md) — when to modify frameworks
- [Multi-Client Conflict Prevention](../concepts/multi-client-conflict-prevention.md) — sync during multi-layer migration
- [CLAUDE.md](../../CLAUDE.md) — original 2-layer schema (this amendment supersedes the entities/concepts sections)
