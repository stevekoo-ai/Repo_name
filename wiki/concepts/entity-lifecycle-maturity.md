---
title: Entity Lifecycle — Discovery to Mature State
created: 2026-08-08
updated: 2026-08-08
tags: [entity, lifecycle, maturity, architecture]
---

# Entity Lifecycle: How Entities Transition from Discovery to Mature State

This document describes how an entity evolves through states in the wiki, from initial discovery through mature operation, and how to recognize each stage.

## Entity States

### Stage 1: Mention (Not Yet an Entity)

**Definition**: The thing is mentioned in a source or conversation, but hasn't been formalized as a wiki entity.

**Characteristics**:
- Appears in `sources/` files
- May be cited in log.md as "discussed X" (not yet "entity/X")
- Not in `wiki/index.md`
- No dedicated entity file

**Decision Rules**:
- Is this a recurring person/org/product/stock that we'll track over time?
- Will we need historical snapshots of its state?
- **If YES** → Promote to Stage 2 (Entity Discovery)
- **If NO** → Keep in sources/summaries only

**Example**: "한국은행 기준금리 결정" mentioned in a macro news source. Not yet an entity (monetary policy is a concept, not a recurring thing to track).

---

### Stage 2: Entity Discovery — Initial File Creation

**Definition**: Created `entities/foo.md` with initial current state and first journal entry.

**What happens**:
1. Create `entities/foo.md` (current state, ~50–100 lines)
   - Frontmatter (created: today, updated: today)
   - 1–2 paragraph summary of current state
   - Key metrics table (if applicable)
   - "Last verified: [date]"
   - "See entity-journals/foo-journal.md for history"

2. Create `entity-journals/foo-journal.md` (history)
   - Frontmatter (created: same as entity, updated: today)
   - Header explaining journal purpose
   - First entry: "Date: today. State: [initial state]. Source: [link]."

3. Update `wiki/index.md` to list new entity
4. Append `log.md`: "INGEST → created entities/foo.md + entity-journals/foo-journal.md"

**Checklist**:
- [ ] Entity page is 50–100 lines (current state only, no dated entries)
- [ ] Journal page is created with first entry
- [ ] Both pages linked to each other
- [ ] index.md updated
- [ ] log.md entry added

**Example**: First mention of CXMT (Changxin Memory) in July 2026 → create entities/cxmt.md with initial snapshot, entity-journals/cxmt-journal.md with first entry.

---

### Stage 3: Entity Observation — Regular Updates

**Definition**: Entity exists and is being tracked. New states are observed and recorded.

**What happens**:
- Every time entity's state changes materially:
  1. Summarize new state → update `entities/foo.md` (replace current-state section)
  2. Log change with rationale → append `entity-journals/foo-journal.md`
  3. Update "Last verified" timestamp in entity
  4. Append `log.md`: "UPDATE entities/foo.md + entity-journals/foo-journal.md → [reason]"

**Size Expectations**:
- Entity page: stays 50–300 lines (current state is bounded)
- Entity-journal page: grows unbounded (append-only)

**Update Frequency**: As often as state materially changes (daily, weekly, or as events warrant). Not on a fixed schedule.

**Example**: SK하이닉스 stock price changes from 1,200K to 1,436K on 8/7. Update entities/sk-hynix.md "현재 상태" section. Append entity-journals/sk-hynix-journal.md with new dated entry.

---

### Stage 4: Entity as Pattern Anchor (Concept Link)

**Definition**: Entity's patterns become stable enough to inform concept definitions or concept watches.

**What happens**:
- Entity's state changes start to align with concept patterns (e.g., HBM Cycle Score)
- Add a "Watch List" section to entity page:
  ```markdown
  ## 🔍 Watch List: Concept Lifecycle 추적
  
  [Concept] occurrences tied to this entity:
  - Concept: [State] [Date] ✓ or ⏳
  ```
- Each concept tie is a "pattern candidate" — does it justify concept updates?
- Use [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md) to decide

**Example**: SK하이닉스 entity "Watch List" tracks HBM4 supply confirmations:
- "HBM4 공급 확정 [1회] ✓" (one confirmation so far)
- "CXMT HBM4 신호 [기대중] ⏳" (watching for pattern)
- "삼성 HBM4 신호 [기대중] ⏳"
- Concept update to hbm-cycle-score.md requires 3+ confirmations (pattern rule)

**Decision Rule**: When you observe an entity behavior that matches a concept pattern, record it in entity's Watch List. When count reaches threshold (usually 3+), revisit concept definition.

---

### Stage 5: Entity as Decision Signal (Monitoring Link)

**Definition**: Entity state directly drives monitoring/tracking pages.

**What happens**:
- Entity's state changes trigger updates to monitoring pages
- Example: SK하이닉스 ADR mismatch → triggers update to monitoring/adr-tracking-status.md
- Monitoring page links back to entity for current state

**Example**: When SK하이닉스 enters "과매도" (oversold, RSI<30), this triggers:
- monitoring/sk-hynix-oversold-status.md updated with date/reason
- Entity page links to monitoring for context

---

### Stage 6: Entity Maturity — Stable Tracking

**Definition**: Entity has become a stable reference point with predictable update cadence.

**Characteristics**:
- Entity file changes only when state materially changes (not reviewed frequently)
- Entity-journal grows at predictable rate (e.g., 1-2 entries/week)
- Watch List tracks 2–3 concept patterns
- Multiple monitoring pages reference this entity
- Cross-referenced by 5+ other wiki pages

**Sustainability**: 
- Entity can be managed indefinitely (append-only journal design)
- No rotation needed for entity page itself
- Journal rotation to monthly archives when >100KB

**Example**: SK하이닉스 entity by August 2026:
- 82-line current state
- 1,200+ line journal (7/13–8/8)
- Watch List: HBM4 public signals, ④ 외국인 순매도 tracking
- Referenced by: 7 monitoring pages, 3 concepts, 2 macro analysis pages

---

## Transition Matrix

| From → To | Trigger | Action | Check |
|---|---|---|---|
| Mention → Discovery | "This will recur, we'll track it" | Create entity + journal files | Both files exist, linked |
| Discovery → Observation | First state change | Update entity + append journal | Entity ≤300 lines, journal appended |
| Observation → Pattern Anchor | Concept pattern match | Add Watch List section to entity | Watch List entries recorded |
| Pattern Anchor → Decision Signal | Monitoring signal triggered | Link entity from monitoring page | Bidirectional links exist |
| Decision Signal → Maturity | 3+ concept references + 5+ backlinks | No action needed (is mature) | All links functional |

---

## How to Recognize Each Stage

### Is this entity in Stage 2 (Discovery)?
- [ ] Created in last week
- [ ] Very little change history yet
- [ ] Journal has <10 entries
- [ ] No Watch List or monitoring links yet

### Is this entity in Stage 3–4 (Observation + Pattern)?
- [ ] Has 1+ months of history
- [ ] Journal has 10+ entries
- [ ] Watch List section present
- [ ] May have 1–2 monitoring links

### Is this entity in Stage 5–6 (Mature)?
- [ ] Has 3+ months of history
- [ ] Journal has 50+ entries
- [ ] Watch List active with 2–3 patterns
- [ ] Referenced by 5+ pages
- [ ] Bidirectional links to 3+ monitoring pages

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Keeping Dated Entries in Entity Current-State
- **Wrong**: entities/sk-hynix.md has "8/7 체크: -3.95%", "8/6 체크: -10.37%"
- **Right**: Move to entity-journals/sk-hynix-journal.md, keep only latest in entity
- **Rule**: Entity page must reflect current state only (~50–300 lines)

### ❌ Mistake 2: Not Creating an Entity-Journal
- **Wrong**: Entity page has full history, no journal
- **Right**: Split immediately when >300 lines
- **Rule**: Entity + Journal always paired

### ❌ Mistake 3: Modifying Entity Watch List Too Freely
- **Wrong**: Add 20 "potential patterns" to Watch List
- **Right**: Record only confirmed occurrences with dates
- **Rule**: Watch List is a tally, not a wishlist. Use dates to track pattern count.

### ❌ Mistake 4: Updating Entity "Last Verified" When Just Reviewing
- **Wrong**: updated: 2026-08-08 (just reviewed the page, no state change)
- **Right**: updated: 2026-08-07 (when actual state last changed)
- **Rule**: "Updated" = state change, not review date

---

## Entity Lifecycle in the 4-Layer Model

Entity lifecycle is **Layers 1–2 only** (doesn't touch concepts/monitoring):

```
Layer 1 (Entity)        Stage 2: Create           Stage 3–6: Update
entities/sk-hynix.md    "Discovery"              "Observation → Maturity"
~82 lines               (initial state)          (current state refreshes)
Current state only
                        ↓
                        Layer 2 (Entity-Journal)
                        entity-journals/sk-hynix-journal.md
                        Append-only journal (1,200+ lines)
                        
                        ← Reverse-chronological, growing unbounded
```

Watch List (entity page) **monitors** Layers 3–4, but doesn't modify them:
- Points to concept for pattern definition
- Records pattern occurrence count
- Concept updates follow Concept Lifecycle rules (separate)

---

## Decision Tree: When to Create an Entity

```
Q1: Is this a recurring person/org/stock/product?
  ├─ NO → Not an entity (keep in concept/summary)
  └─ YES → Q2
    Q2: Will we need to track its state changes over time?
      ├─ NO → Not an entity (static reference)
      └─ YES → Q3
        Q3: Will tracking this inform decision-making or analytics?
          ├─ NO → Not an entity yet (dormant mention)
          └─ YES → Create entity now
```

---

## Sources

- [Knowledge Model — 4-Layer Architecture](../concepts/knowledge-model.md)
- [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md)
- [Architecture Amendment — 4-Layer Specification](../architecture-amendment-4layer.md)
- [SK하이닉스 Entity (Live Example)](../entities/sk-hynix.md)
- [SK하이닉스 Journal (Live Example)](../entity-journals/sk-hynix-journal.md)
