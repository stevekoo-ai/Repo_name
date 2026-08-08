---
title: Decision Intelligence — Reading the Wiki for Decision-Making
created: 2026-08-08
updated: 2026-08-08
tags: [decision, intelligence, reading-guide, architecture]
---

# Decision Intelligence: How to Read the Wiki for Decision-Making

This document is a guide for users who want to use the wiki to make better decisions. It explains which pages to read for each type of decision, and how to interpret what you find.

## Core Principle

**The wiki is organized by layer, not by use case.** You must pick the right combination of layers for your decision type.

```
Decision Type           Layers to Read              Read Time
─────────────────────────────────────────────────────────────
"What is X?"            Layer 1 only               1–2 min
"Why did X change?"     Layers 1 + 2              5–10 min  
"How do we evaluate?"   Layer 3 only              3–5 min
"Should we act today?"  Layers 1 + 3 + 4          10–15 min
"Is X in a pattern?"    Layers 2 + 3 + watch-list 15–30 min
```

---

## Decision Workflows

### Decision 1: "What is the current state of X?"

**Layers**: Layer 1 only (Entity current-state)

**Read**:
1. Go to `wiki/index.md` → Find entity in the list
2. Open `entities/sk-hynix.md` (example)
3. Read: Frontmatter → Current state paragraph → Key metrics table → "Last verified"
4. **Stop here** — you have the answer

**Time**: 1–2 minutes

**What you learn**:
- SK하이닉스 is at 1,436,000원 as of 8/7
- It's -3.95% on the day, near oversold (RSI 37.98)
- Foreign fund flows are net-negative (cumulative 5.3T loss)

**Example Q&A**:
- Q: "What's SK하이닉스 trading at?"
- A: [Read entity, see current metrics] "1,436,000원, RSI near 38 (not yet oversold at 30)"

---

### Decision 2: "Why did X change from [date1] to [date2]?"

**Layers**: Layers 1 + 2 (Entity current-state + Entity-Journal)

**Read**:
1. Start at `entities/sk-hynix.md` (Layer 1) → current state
2. Scan "최근 움직임 요약" (Recent movement summary) if present
3. If summary doesn't explain the specific change, click → `entity-journals/sk-hynix-journal.md`
4. Scan the dated entries between [date1] and [date2] in reverse-chronological order
5. Find the entry where change happened, read its rationale

**Time**: 5–10 minutes

**What you learn**:
- 8/6 to 8/7 drop was -3.95%
- 8/6 context: Previous day's -10.37% drop (US semis weakness + foreign selloff)
- 8/7 likely technical bounce recovery, but momentum weak (still negative for day)

**Example Q&A**:
- Q: "SK하이닉스 dropped 10% on 8/6. Why? Will it recover?"
- A: [Read entity summary] "Foreign outflow signal (④ collapse condition met, 5.3T cumulative short)" → [Read journal 8/6 entry] "US semiconductor sector weakness (SOX -2.5%) + foreign funds shifted to net sellers after 8/5 rally"

**Warning**: Don't confuse "why" (Layer 2 causation) with "what" (Layer 1 current state). You need both.

---

### Decision 3: "How do we evaluate/score this thing?"

**Layers**: Layer 3 only (Concept framework)

**Read**:
1. Go to `wiki/index.md` → Find concept section
2. Open `concepts/hbm-cycle-score.md` (example)
3. Read: Definition → Methodology → Axes/Thresholds → Collapse conditions
4. **Stop here** — you understand the framework

**Time**: 3–5 minutes

**What you learn**:
- HBM Cycle Score is 0–100
- Calculated on 4 axes: Supply, Demand, Technical, Sentiment
- 5 "collapse conditions" (hard stops that trigger score drop)
- Oversold threshold is RSI ≤30

**Example Q&A**:
- Q: "I don't understand how HBM Cycle Score works. Explain it."
- A: [Read concepts/hbm-cycle-score.md] "It's a composite score on 4 axes, with 5 hard collapse rules..."

**Note**: This decision does NOT involve today's score. Framework rarely changes. If it does, concept page will have a "Last changed" note.

---

### Decision 4: "Should we act on X today?"

**Layers**: 1 + 3 + 4 (Entity current-state + Concept framework + Monitoring tracking)

**Read**:
1. **Entity (Layer 1)**: `entities/sk-hynix.md` → Current state (~1 min)
   - What is the price/metrics right now?
   
2. **Concept (Layer 3)**: `concepts/hbm-cycle-score.md` → Framework (~2 min)
   - How do we define "action-worthy"?
   
3. **Monitoring (Layer 4)**: `monitoring/hbm-cycle-score-status.md` → Latest Status (~2 min)
   - What is today's score?
   - Which decision signals are active?
   
4. **Synthesis**: Compare [Entity state] + [Concept criteria] + [Today's score] → Decide

**Time**: 10–15 minutes

**Decision Tree**:
```
Current state (L1): 1,436,000원, RSI 37.98
           ↓
Concept thresholds (L3): Oversold = RSI ≤30
           ↓
Today's score (L4): 75/100 (Watching), 1/5 collapse triggered
           ↓
Decision: NOT oversold yet (RSI >30), but at risk (1 collapse condition met)
          → Monitor, don't buy yet. Wait for RSI ≤30 or 2+ conditions.
```

**Example Q&A**:
- Q: "Should we buy SK하이닉스 today?"
- A: [Read entity] Current price is near-oversold territory (RSI 37.98). [Read concept] Oversold threshold is 30. [Read monitoring] Score is 75/100, watch level (1/5 conditions triggered). Decision: "Not yet. Wait for RSI ≤30 or more signals. Currently in monitoring phase, not action phase."

---

### Decision 5: "Is X in a pattern? Should we update our framework?"

**Layers**: 2 + 3 + Entity Watch List (Journal + Concept + Entity pattern tracker)

**Read**:
1. **Entity Watch List** (in entity page, Layer 1): See pattern count
   - "HBM4 공급 확정: [1회] ✓"
   
2. **Entity-Journal** (Layer 2): Read all related entries
   - When was each pattern occurrence?
   - What was the context?
   
3. **Concept** (Layer 3): Read current definition
   - Is this pattern already considered?
   - If not, do 3+ occurrences justify updating the concept?
   
4. **Concept Lifecycle** (reference): Check 4-condition AND rule
   - Does pattern meet all 4 justification criteria?

**Time**: 15–30 minutes (plus decision discussion)

**Example Q&A**:
- Q: "We've seen HBM4 supply confirmed for SK하이닉스, CXMT, and Samsung. Should we update the HBM Cycle Score concept to include 'HBM4 supply expansion'?"
- A: [Read entity watch lists] HBM4 confirmations: SK(1), CXMT(waiting), Samsung(waiting) — 1 confirmed only. [Check concept-lifecycle-maturity.md] 4-condition rule says: 3+ repetitions, existing assumption violated, new variable, statistical significance. Decision: "Not yet. Need 3+ confirmations (we have 1). Wait for CXMT Q1 2026 confirmation + Samsung roadmap. When 3/3 confirmed, revisit concept."

**Important**: This is NOT a quick decision. It requires consensus (user + agent) before concepts change.

---

## Common Mistakes in Decision-Making

### ❌ Mistake 1: Reading only Layer 1 when you need Layer 2

**Symptom**: "SK하이닉스 was at 1,436,000원 on 8/7. Why? I don't know."

**Problem**: You read entity current-state (what), but not entity-journal (why).

**Fix**: Always follow entity → journal when explaining changes.

---

### ❌ Mistake 2: Reading Layer 4 without Layer 3

**Symptom**: "Score dropped from 80 to 75 (Watching). Is this bad?"

**Problem**: You read today's score (Layer 4), but don't understand what it means (Layer 3).

**Fix**: Always read concept first to understand "what is Watching?"

---

### ❌ Mistake 3: Using old entity-journal data instead of Layer 1

**Symptom**: "I'm reading entity-journals/sk-hynix-journal.md, and I see '1,200,000원 on 7/25'. Should we buy here?"

**Problem**: That was the price 2 weeks ago. Current price is 1,436,000원 (Layer 1).

**Fix**: Always start with Layer 1 (current state) for today's decisions. Use Layer 2 only for historical context.

---

### ❌ Mistake 4: Modifying concepts based on one event

**Symptom**: "HBM4 supply was confirmed once. Should we update hbm-cycle-score.md?"

**Problem**: One event is not a pattern. Concept changes require 3+ repetitions (Concept Lifecycle rule).

**Fix**: Record event in Entity Watch List. When count reaches 3+, then reconsider concept.

---

### ❌ Mistake 5: Confusing "Monitoring status" with "Entity state"

**Symptom**: "Monitoring score is 75 (Watching). So SK하이닉스 price is 75,000원?"

**Problem**: 75 is an abstract score, not a price. The actual price is in Layer 1 (entity).

**Fix**: Layer 4 (monitoring) is not a price or value. It's a decision signal. Always look at Layer 1 for actual state.

---

## Reading Guide by Role

### I'm an Analyst → Decision Support

**Your workflow**:
1. **Morning**: Read Layer 1 (entity states) → morning status (3 min)
2. **Mid-day**: Read Layer 4 (monitoring scores) if checking for alerts (1 min per check)
3. **Decision time**: Read Layers 1+3+4 together (10 min per decision)
4. **Weekly review**: Read Layers 1+2 for historical context (20 min per entity)

**Read infrequently**:
- Layer 3 (concepts) — only when onboarding or concept changes (rare)
- Entity-journals (Layer 2) — only when explaining a past decision or analyzing patterns (not daily)

---

### I'm a Developer → Architecture Understanding

**Your workflow**:
1. **Onboarding**: Read [Knowledge Model](../concepts/knowledge-model.md) (20 min)
2. **Creating entities**: Read [Entity Lifecycle](../concepts/entity-lifecycle-maturity.md) (15 min)
3. **Modifying concepts**: Read [Concept Lifecycle](../concepts/concept-lifecycle-maturity.md) (10 min)
4. **Building reports**: Read [Reporting Framework](../concepts/reporting-framework.md) (20 min)
5. **Coding**: Follow CLAUDE.md /ingest and /query workflows

**Read every session**:
- CLAUDE.md (reference material, ~10 min if new change)
- [messagebox.md](../messagebox.md) before sync (1 min, for coordination)

---

### I'm a User (Non-Technical) → Decision-Making

**Your workflow**:
1. **Question**: What do I need to decide right now?
2. **Layer mapping**: Use the "Decision Workflows" table above
3. **Read**: Only the layers needed for that decision
4. **Stop**: Don't go deeper unless analysis uncovers follow-up questions

**Don't read**:
- Full entity-journals (too much detail)
- Full concepts (read just the 1-2 relevant axes)
- Architecture documents (leave to analysts/developers)

---

## Quick Reference: What Each Layer Answers

| Layer | File | Question | Answer |
|---|---|---|---|
| **1. Entity** | `entities/foo.md` | "What is X right now?" | Current state summary + metrics |
| **2. Journal** | `entity-journals/foo-journal.md` | "How did X get here?" | Complete dated timeline |
| **3. Concept** | `concepts/foo.md` | "How do we evaluate X?" | Framework definition + axes |
| **4. Monitoring** | `monitoring/foo-status.md` | "What is X's score today?" | Today's value + recent changes |

---

## Signal Interpretation Guide

### What does a monitoring score mean?

| Score Range | Meaning | Action |
|---|---|---|
| **0–40** | High Risk / Highly Oversold | ⛔ Avoid unless opportunity confirmed |
| **40–60** | Neutral / Balanced | ⏸️ Monitor, wait for signal |
| **60–80** | Caution / Watching | ⚠️ Monitor closely, prepare for action |
| **80–100** | Bullish / Uptrend | 🟢 Conditions favorable, watch for entry |

**Example**:
- HBM Cycle Score = 75/100 → "Watching" zone
- Interpretation: "Positive momentum, but 1/5 collapse conditions triggered (foreign outflow). Monitor daily; if 2+ conditions trigger, shift to caution."

---

## Decision Framework Checklist

Before making a decision, check:

- [ ] I've read Layer 1 (current state)
- [ ] I understand what the decision threshold is (Layer 3)
- [ ] I know today's score/status (Layer 4)
- [ ] If explaining "why", I've traced to Layer 2 (journal entry)
- [ ] I'm not confusing abstract scores with actual values
- [ ] I'm not making 3-event decision based on 1 occurrence
- [ ] I've linked back to sources where appropriate

---

## Examples: End-to-End Decision Walks

### Example 1: "Should I buy SK하이닉스 stock?"

**Step 1: Current state (Layer 1)**
- Read: entities/sk-hynix.md
- Find: 1,436,000원, RSI 37.98 (near oversold)

**Step 2: Evaluation framework (Layer 3)**
- Read: concepts/hbm-cycle-score.md
- Find: Oversold at RSI ≤30, our score includes 5 collapse conditions

**Step 3: Today's signal (Layer 4)**
- Read: monitoring/hbm-cycle-score-status.md → Latest Status
- Find: HBM Cycle Score 75/100 (Watch), 1/5 conditions triggered (외국인 순매도)

**Step 4: Decide**
```
Current state:  1,436,000원, RSI 37.98 (not yet oversold)
Framework:      Oversold at RSI ≤30, 1 condition OK, need 2+ for high conviction
Today's signal: 75/100 (Watch), 1/5 triggered
Decision:       "Not yet. RSI has to drop to ≤30, or 2nd condition must trigger.
                 Currently in 'monitor' phase, not 'act' phase."
```

---

### Example 2: "Why did SK하이닉스 drop 10% yesterday?"

**Step 1: Current state (Layer 1)**
- Read: entities/sk-hynix.md
- Find: 8/6 close was -10.37% from prior day

**Step 2: Explanation (Layer 2 — Journal)**
- Read: entity-journals/sk-hynix-journal.md
- Find: 8/6 entry: "미국 반도체 약세 (SOX -2.5%) + 외국인 대량매도"
- Also find 8/7 entry: "외국인 순매도 지속, RSI 하락 추세"

**Step 3: Context (Layer 3)**
- Read: concepts/hbm-cycle-score.md
- Find: Foreign outflow is ④ collapse condition
- Understand: This is a known risk pattern we track

**Step 4: Synthesize**
```
Why it dropped:  US semis weakness (SOX) + Korean market contagion
Pattern:         Foreign outflow (④ condition) — our framework already tracking this
Next check:      8/9 to see if foreign flows stabilize or continue selling
```

---

## Sources

- [Knowledge Model — 4-Layer Architecture](../concepts/knowledge-model.md)
- [Concept Lifecycle Maturity](../concepts/concept-lifecycle-maturity.md)
- [Entity Lifecycle Maturity](../concepts/entity-lifecycle-maturity.md)
- [Reporting Framework](../concepts/reporting-framework.md)
- [CLAUDE.md — Workflows](../../CLAUDE.md)
- [SK하이닉스 Entity (Live Example)](../entities/sk-hynix.md)
- [HBM Cycle Score Concept (Live Example)](../concepts/hbm-cycle-score.md)
- [HBM Cycle Score Monitoring (Live Example)](../monitoring/hbm-cycle-score-status.md)
