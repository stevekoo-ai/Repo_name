---
essence_id: E-C
type: C
type_name: sample-schedule coordination (샘플/일정 조율)
source_textbooks: [05, 08, 10, 12, 13, 14, 27, 29, 30]
source_count: 9
master_db_count: 50
domains: [sample-coordination, schedule-alignment, quantity-negotiation, pull-in-request, timeline-gap, enclosure-FOC-DOA, soft-ask, pushback, action-item, misunderstanding-recovery]
partners: [NVIDIA, Liqid, AMD, Lenovo, Intel]
created: 2026-09-01
---

# Essence E-C - Sample / Schedule Coordination (샘플/일정 조율)

> Distilled from 9 type-C textbooks (05 NVIDIA, 08 Liqid, 10 Liqid, 12 Liqid Biweekly, 13 Liqid Biweekly, 14 AMD, 27 Lenovo CN, 29 AMD Biweekly, 30 INTEL).
> Meeting type: sample/schedule coordination - ES/CS/MP sample planning, pull-in requests, quantity negotiation, timeline gap surfacing, enclosure/FOC/DOA language.
> This volume is the compressed intelligence across ALL 9 type-C textbooks - not a single textbook.

---

## S1. 유형의 본질 (Nature of the Meeting Type)

### What this meeting type IS

Type C is a **coordination meeting** between SK Hynix (coordinator side) and a partner (NVIDIA / Liqid / AMD / Lenovo / Intel). Its purpose is NOT to make a single decision, but to keep two moving machines aligned.

The recurring 5-move cycle:

1. **Status touchback** - open with the previous sync's open item, not a new topic
2. **Schedule walk-through** - each side states milestones using ES / CS / QS / MP / power-on / volume-validation vocabulary
3. **Gap surfacing** - someone names a gap ("pushed out two months", "short timeline between QS and production just two months", "are we missing your launch")
4. **Proposal + pushback** - one side proposes (pull-in, quantity, sample type), the other pushes back (supply constraint, internal deferral, soft denial)
5. **Action item capture** - both sides commit to time-boxed parallel homework ("give me one maybe two weeks", "let's align then")

### What this meeting type is NOT

- NOT a technical deep-dive (that is type A or B)
- NOT a one-shot negotiation (it is a recurring rhythm - weekly, biweekly, monthly)
- NOT a relationship-building meeting (it is action-oriented)
- NOT a forum for open-ended questions ("that won't be open-ended. We'll have to be extremely specific" - m29)

### The two registers inside one meeting

Every type-C meeting alternates between two registers:

- **Schedule mode** (coordinator lead): direct, milestone vocabulary, risk probes, "is that okay or not"
- **Soft-ask mode** (resource requester): hedged, "some" instead of quantities, "lend" instead of "provide", "very first stage" framing

You must learn to switch between them. The same person (Sangdon / Steve / Trent) speaks both modes in one meeting.

### Why this type matters

Type C is the **highest frequency** meeting type for SK Hynix engineers working with US partners. It happens every week or two. The language is **highly formulaic** - the same 50 expressions cover roughly 80% of the moves. Master these 50 and you can lead any coordination sync.

---

## S2. 화자 아키텍처 정수 (Speaker Architecture Essence)

### The coordinator (SK Hynix side)

The coordinator runs the meeting. Across all 9 textbooks, the coordinator role is consistent:

| Name | Textbook | Role | Style |
|:---|:---|:---|:---|
| Sangdon | 30 (Intel) | SK Hynix lead | Schedule mode + soft-ask mode, "we want to align our schedule with your schedule" |
| Steve | 14 (AMD) | SK Hynix lead | Partnership framing, "this is a partnership, right? We are not a customer" |
| Trent | 12, 13 (Liqid Biweekly) | SK Hynix lead | Action-item focused, "let's make it an action item for today" |
| Triet | 08, 10 (Liqid on-site) | SK Hynix on-site | Concession language, "for sure we won't leave until everything is up and running" |

**Coordinator's 5-step structure** (Sangdon, textbook 30):
1. Status touchback ("We had touched the status of X in Y site")
2. Schedule walk-through ("we may support the ES sample at the end of Q3")
3. Alignment ask ("we want to align our schedule with your schedule")
4. Misunderstanding recovery ("it's my misunderstanding")
5. Soft ask handoff ("we had a collaboration about X previously... we would like some collaboration about Y for the future")

### The partner (NVIDIA / Liqid / AMD / Lenovo / Intel)

The partner side has three recurring roles across all 9 textbooks:

| Role | Function | Language |
|:---|:---|:---|
| **Technical partner** (Intel Jenny, AMD rep, Liqid Paul) | Provides timeline, corrects misunderstandings | "looks like we are both sides almost the same pace... results are aligned" |
| **Resource gatekeeper** (Intel Tony-GPU, AMD VP) | Controls sample quantity, asks for "shopping list" | "do you have a minimum number of cards", "I don't believe we do that for CXL" |
| **Local coordinator** (Lenovo CN rep, Liqid on-site) | Manages logistics, gives ground truth | "the soonest we can arrive is X", "we will expect to start on X" |

### The dynamic

The coordinator drives the 5-move cycle. The partner alternates between **providing** (timeline, milestone) and **pushing back** (supply constraint, internal deferral, soft deny). The coordinator's job is to convert pushback into a time-boxed action item without losing the partnership frame.

---

## S3. 핵심 전략 정수 (Core Strategy Essence)

### Strategy 1: "Align" as the master verb

The single most powerful word in type-C meetings is "align". Use it to frame every timeline question as joint planning, not pressure.

- "we want to align our schedule with your schedule and see whether it is aligning or not" (m30)
- "we need to understand each other's stack" - extends alignment to technical compatibility (m30)
- "let's cross check" - mutual verification (m30)

When you ask a partner about their timeline, preface it with "we want to align our schedule with yours" - this converts an intrusive question into a joint planning act.

### Strategy 2: Risk-voice probes

When you need an honest timeline, do not ask "when". Ask in risk voice:

- "is this timeline good or are we missing your launch" (m30)
- "I just wonder do we miss the your timeline" (m30)
- "you're gonna make some short timeline between QS and production just two months" (m30)

Risk voice shows worry, which makes the partner want to reassure you with their actual timeline.

### Strategy 3: Past precedent + future want

When bringing a new ask, frame it as a continuation:

- "we had a collaboration about X previously... we would like some collaboration about Y for the future" (m30)
- "a couple of weeks ago we discussed X" (m05)

This makes a new request feel like relationship maintenance, not a cold ask.

### Strategy 4: Internal deferral formulas

When you cannot commit, defer to "internal" without saying no:

- "let us discuss internally. It's not just X, there's Y" (m13)
- "Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?" (m14)
- "we still under discussion" (m27)
- "I'm not going to commit for that yet. Let us X first" (m29)

The pattern: **acknowledge + defer to internal + time-box the return**.

### Strategy 5: Pushback without burning the bridge

When refusing a partner's ask, use **soft deny + offer to verify + defer**:

- "I don't believe that we do that for CXL... please jump in and let me know if I'm being correct here" (m30)
- "we can go and confirm where we're at and come back" (m30)
- "We understand. But... it may not be possible" (m05)
- "we cannot delay our overall X schedule" (m05)

"I don't believe" leaves room - it is a refusal with a softener that says "this is my understanding, I could be wrong."

### Strategy 6: Funnel questioning (when you are the partner)

When a partner makes a vague ask, challenge by asking a series of specific questions:

- "is the request multiple cards... do you have a minimum number of cards... do you understand how you're going to change the software" (m30)
- "what's the expectation of involvement" (m30)
- "I'd like to see what the shopping list is and let's talk about it" (m30)

Start broad, end narrow. This turns a vague request into an actionable plan without saying no.

### Strategy 7: Time-boxed parallel homework

Action items use **time-box + parallel work + phased steps**:

- "give me one maybe two weeks to understand" (m30)
- "I'll look at the same on my side" (m30)
- "step one is X and then step two would be like Y" (m30)
- "let's align then so go and understand on your side" (m30)

"Let's align then" is the trigger that converts discussion into action.

### Strategy 8: Misunderstanding recovery

When wrong, do not over-apologize:

- "it's my misunderstanding" - attributes error to interpretation, not competence (m30)
- "Okay okay okay I understand that" - triple "okay" buys processing time, then "I understand that" closes the loop (m30)
- "hopefully that clarifies right" - partner's check after correcting you (m30)

### Strategy 9: Quantity negotiation - minimum first, then full

When asking for hardware, start small to show reasonableness:

- "just a single of gpu card will be okay so one cpu plus with the one Gaudi gpu card" (m30)
- "I believe at least you need eight cards" (m30)
- "one card first approach" then "at least eight for the whole system" (m30)

This shows you are reasonable AND have thought through the scaling.

### Strategy 10: Partnership framing

When you need leverage, reframe the relationship:

- "this is a partnership, right? We are not a customer" (m14) - type-unique to AMD
- "we can't do it without X" (m12) - dependency framing
- "we would welcome the chance" (m13) - positive framing of an ask

---

## S4. 마스터 표현 DB (Master Expression Database)

50 expressions distilled from 9 type-C textbooks. Each entry: id, expression, function, sources (textbook IDs where pattern appears), difficulty (1-5), note. Prioritized low-frequency / high-structural-value patterns. 2+ textbook patterns kept; type-unique expressions included.

```yaml
# -- Schedule alignment (the master verb) --
- id: ec-001
  expression: "we want to align our schedule with your schedule and see whether it is aligning or not"
  function: alignment_intent
  sources: [30]
  difficulty: 4
  note: THE core schedule alignment sentence. Use this to frame every timeline question as coordination, not pressure. Type-unique to Intel sync.

- id: ec-002
  expression: "we'd like to know the schedule so we can update the new intel tmr's the timeline"
  function: reason_for_ask
  sources: [30, 12, 13]
  difficulty: 3
  note: Stating the reason for your ask - "so we can update" justifies the question. Cross-textbook pattern: always give reason before asking timeline.

- id: ec-003
  expression: "is this timeline good or are we missing your launch"
  function: risk_voice_probe
  sources: [30]
  difficulty: 4
  note: Risk-voice probe. Shows worry, forces honest answer. "Are we missing your launch" is more effective than "when".

- id: ec-004
  expression: "we would like to know how much does intel lead for the validation sample"
  function: lead_time_inquiry
  sources: [30, 05, 14]
  difficulty: 4
  note: "How much does X lead" - probing partner's lead time for sample preparation. Appears across NVIDIA, AMD, Intel syncs.

- id: ec-005
  expression: "looks like we are both sides almost the same pace... results are aligned"
  function: aligned_confirmation
  sources: [30]
  difficulty: 3
  note: "Aligned" is the confirmation word. When results match, say "we are aligned."

- id: ec-006
  expression: "so let's cross check"
  function: verification_trigger
  sources: [30, 13]
  difficulty: 2
  note: "Cross check" - mutual verification commitment. Short, actionable.

- id: ec-007
  expression: "we need to understand each other's stack"
  function: stack_alignment
  sources: [30, 13]
  difficulty: 3
  note: "Stack alignment" extends schedule alignment to technical compatibility.

# -- Sample / milestone language --
- id: ec-008
  expression: "we may support the ES sample at the end of Q3 2026"
  function: es_timing
  sources: [30, 05, 14, 29]
  difficulty: 3
  note: ES (Engineering Sample) timing. "Support" is the verb for providing samples. Universal across all sample-sync textbooks.

- id: ec-009
  expression: "it's already CS candidate"
  function: cs_level_statement
  sources: [30, 05, 14]
  difficulty: 3
  note: CS (Customer Sample) milestone. "CS candidate" = being considered for CS status.

- id: ec-010
  expression: "the cmm schedule pushed out two months"
  function: delay_disclosure
  sources: [30, 10, 12]
  difficulty: 3
  note: "Pushed out" = delayed. Direct disclosure formula. Use "pushed out N months" for delays.

- id: ec-011
  expression: "we are expected to ship X by Y. That is the target"
  function: target_statement
  sources: [12, 08, 13]
  difficulty: 3
  note: "Expected to" + "that is the target" - hedged but firm. Liqid biweekly pattern.

- id: ec-012
  expression: "you're gonna make some short timeline between QS and production just two months"
  function: gap_question
  sources: [30]
  difficulty: 4
  note: Probing the gap between milestones. "Short timeline between X and Y" - gap analysis.

- id: ec-013
  expression: "we completed our power on I think early November something like that"
  function: completed_milestone
  sources: [30]
  difficulty: 2
  note: Past-tense milestone with hedging - "I think... something like that" softens the date.

- id: ec-014
  expression: "between Q1 and Q2 of next year you're good to go"
  function: go_signal
  sources: [30]
  difficulty: 3
  note: "You're good to go" - the green light signal. Use to confirm a timeline.

# -- Pull-in request --
- id: ec-015
  expression: "we're trying to pull in X"
  function: pull_in_request
  sources: [05, 14, 29]
  difficulty: 4
  note: "Pull in" = move earlier. NVIDIA HBM4E pattern, also appears in AMD. Direct but soft with "trying to".

- id: ec-016
  expression: "let's target that"
  function: target_setting
  sources: [29, 12]
  difficulty: 3
  note: Short target-setting phrase. Use after proposing a timeline.

- id: ec-017
  expression: "the original plan was X, but because Y, we did not Z"
  function: plan_deviation_disclosure
  sources: [10, 12]
  difficulty: 4
  note: Liqid pattern for explaining deviation. "Original plan was... but because... we did not" - honesty frame.

- id: ec-018
  expression: "we may be able to make it work, but it's very very difficult"
  function: conditional_difficulty
  sources: [10, 13, 29]
  difficulty: 4
  note: Hedged yes. "May be able to" + "very very difficult" - sets expectation without refusing.

# -- Internal deferral --
- id: ec-019
  expression: "let us discuss internally. It's not just X, there's Y"
  function: internal_deferral
  sources: [13, 14, 29]
  difficulty: 4
  note: "Discuss internally" + reason why - shows you are not just stalling. Cross-textbook.

- id: ec-020
  expression: "Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?"
  function: vp_escalation_deferral
  sources: [14, 13]
  difficulty: 4
  note: Escalate to VP + time-box return + ask permission. AMD pattern.

- id: ec-021
  expression: "I'm not going to commit for that yet. Let us X first"
  function: non_commitment_deferral
  sources: [29, 14]
  difficulty: 4
  note: "Not going to commit yet" + "let us X first" - honest non-commitment.

- id: ec-022
  expression: "we still under discussion"
  function: ongoing_discussion_deferral
  sources: [27, 13]
  difficulty: 2
  note: Lenovo CN pattern. Short, direct, signals no decision yet.

- id: ec-023
  expression: "Maybe in one or two quarters"
  function: timeline_vagueness
  sources: [27, 29]
  difficulty: 2
  note: Vague timeline. Use when you cannot give a quarter. "One or two quarters" is the unit.

# -- Soft ask (resource request) --
- id: ec-024
  expression: "we had a collaboration about X previously... we would like some collaboration about Y for the future"
  function: past_plus_future_ask
  sources: [30, 05]
  difficulty: 4
  note: Past precedent + future want. Makes new ask feel like relationship maintenance. Type-unique.

- id: ec-025
  expression: "we'd like to ask to some help"
  function: soft_help_request
  sources: [30]
  difficulty: 2
  note: "Some" is the hedge word. "We want 8 cards" is hard. "We would like some help" is a soft probe.

- id: ec-026
  expression: "if you provide some this system to us we can work together"
  function: barter_frame
  sources: [30, 13]
  difficulty: 4
  note: Barter frame - "you give hardware, we give collaboration data". Lowers the ask.

- id: ec-027
  expression: "we'd like to ask to lend that one or we can collaborate this work together"
  function: borrow_ask
  sources: [30]
  difficulty: 4
  note: "Lend" signals temporary borrow, not ownership. Lowers partner commitment.

- id: ec-028
  expression: "Would it be possible for you to X? Is that an option?"
  function: possibility_probe
  sources: [13]
  difficulty: 4
  note: Two-question form. "Would it be possible" + "is that an option" - very soft ask.

- id: ec-029
  expression: "just a single of gpu card will be okay so one cpu plus with the one Gaudi gpu card"
  function: minimum_viable_ask
  sources: [30, 14]
  difficulty: 3
  note: Start small to show reasonableness. "Just a single X will be okay".

- id: ec-030
  expression: "I believe at least you need eight cards"
  function: full_need_statement
  sources: [30, 14]
  difficulty: 3
  note: State full need after minimum ask. Shows scaling thought through.

# -- Pushback (partner side) --
- id: ec-031
  expression: "We understand. But... it may not be possible"
  function: soft_refusal
  sources: [05, 14, 27]
  difficulty: 4
  note: "We understand" validates, "but it may not be possible" refuses. NVIDIA pattern.

- id: ec-032
  expression: "we cannot delay our overall X schedule"
  function: schedule_protection
  sources: [05, 14]
  difficulty: 4
  note: Protecting your timeline. "Cannot delay overall X" - firm boundary.

- id: ec-033
  expression: "this is a partnership, right? We are not a customer"
  function: partnership_framing
  sources: [14]
  difficulty: 5
  note: TYPE-UNIQUE to AMD. Reframes relationship to gain leverage. "We are not a customer" - equal partner.

- id: ec-034
  expression: "I don't believe that we do that for CXL... please jump in and let me know if I'm being correct here"
  function: soft_deny_with_invite
  sources: [30]
  difficulty: 4
  note: "I don't believe" soft refusal + invite correction. Intel pattern.

- id: ec-035
  expression: "we can go and confirm where we're at and come back"
  function: deferred_refusal
  sources: [30, 14]
  difficulty: 4
  note: Defers the final no. "Confirm and come back" - soft refusal with verification promise.

- id: ec-036
  expression: "we can't do it without X"
  function: dependency_framing
  sources: [12, 13]
  difficulty: 3
  note: "Can't do it without X" - makes partner's contribution a prerequisite.

- id: ec-037
  expression: "some of them I can shift out as FOC, but the rest I need to talk with my VP"
  function: foc_shift
  sources: [14]
  difficulty: 5
  note: TYPE-UNIQUE enclosure/FOC language. FOC = Free of Charge. Partial concession + escalation.

- id: ec-038
  expression: "the supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get"
  function: supply_constraint_disclosure
  sources: [14, 29]
  difficulty: 4
  note: Explains why you cannot deliver. "Not getting as many X as we were supposed to" - honest constraint.

- id: ec-039
  expression: "If there is a problem, we'll report it, but we don't release test results"
  function: conditional_reporting
  sources: [14]
  difficulty: 4
  note: Type-unique. Boundary on what you will and will not share. "Report problems, not results".

- id: ec-040
  expression: "We will not announce X. We will not post Y. But technically we will be ready during Z"
  function: two_negative_deflection
  sources: [27]
  difficulty: 5
  note: TYPE-UNIQUE to Lenovo CN. Two negatives + "but technically" - signal readiness without commitment.

- id: ec-041
  expression: "I don't disagree with you that X. But it depends on a lot of things. You're not wrong"
  function: validate_pivot
  sources: [29]
  difficulty: 5
  note: TYPE-UNIQUE to AMD Biweekly. Validate ("not wrong") + pivot ("depends on") - soft disagreement.

- id: ec-042
  expression: "I'd like to see what the shopping list is and let's talk about it"
  function: clarification_deflection
  sources: [30]
  difficulty: 5
  note: TYPE-UNIQUE. "Shopping list" metaphor converts a vague ask into a homework assignment for the asker.

- id: ec-043
  expression: "I don't know where the volume validation question comes from what is the context of it"
  function: premise_challenge
  sources: [30]
  difficulty: 5
  note: Strongest polite challenge. Forces asker to reveal their (wrong) reasoning.

- id: ec-044
  expression: "Montage was they provided us hundreds of samples so we tested their card during the power on window"
  function: comparative_precedent
  sources: [30]
  difficulty: 5
  note: Citing competitor as benchmark. Factual, not attacking. Explains consequence.

- id: ec-045
  expression: "your device was not available at that time so you are not part of the power on window"
  function: cause_effect_correction
  sources: [30]
  difficulty: 4
  note: Cause-effect correction. "Not available, not part of" - no blame, just fact.

# -- Misunderstanding recovery --
- id: ec-046
  expression: "it's my misunderstanding"
  function: face_saving_admission
  sources: [30]
  difficulty: 5
  note: Cleanest recovery from being wrong. "Misunderstanding" attributes error to interpretation, not competence.

- id: ec-047
  expression: "Okay okay okay I understand that"
  function: correction_acknowledgment
  sources: [30, 12]
  difficulty: 2
  note: Triple "okay" buys processing time. Then "I understand that" closes the loop.

- id: ec-048
  expression: "hopefully that clarifies right"
  function: partner_confirmation_check
  sources: [30]
  difficulty: 3
  note: Partner's check after correcting you. "That clarifies" = the confusion is resolved.

# -- Action items / next steps --
- id: ec-049
  expression: "give me one maybe two weeks to understand"
  function: time_boxed_commitment
  sources: [30, 14, 29]
  difficulty: 3
  note: Time-box with "maybe" softener. "One to two weeks" is the commitment.

- id: ec-050
  expression: "let's align then so go and understand on your side"
  function: action_trigger
  sources: [30, 13]
  difficulty: 4
  note: "Let's align then" is the trigger that converts discussion to action. Then parallel homework.
```

---

## S5. 영역 어휘 정수 (Domain Vocabulary Essence)

30 terms grouped by sub-domain. Drawn from all 9 textbooks. Use these fluently - do not spell them out in meetings.

### Sample-type vocabulary

| Term | Meaning | Source textbook |
|:---|:---|:---|
| **ES** (Engineering Sample) | Earliest prototype for engineering validation | 30, 05, 14, 29 |
| **CS** (Customer Sample) | Sample sent to customer for evaluation, post-ES | 30, 05, 14 |
| **QS** (Qualification Sample) | Sample for qualification testing, pre-MP | 30 |
| **MP** (Mass Production) | Volume production milestone | 30, 05 |
| **pre-ES** | Pre-Engineering Sample, even earlier than ES | 29 |
| **EVB** (Evaluation Board) | Board for evaluating silicon | 29 |
| **CS candidate** | Sample being considered for CS status | 30 |

### Schedule / milestone vocabulary

| Term | Meaning | Source textbook |
|:---|:---|:---|
| **power-on** | Initial silicon / board bring-up validation | 30 |
| **volume validation** | Post-power-on large-scale validation | 30 |
| **bring up** | Hardware initial boot validation | 30 |
| **production qualification** | Final qualification before MP | 30 |
| **push-out** | Schedule moved later | 30 |
| **pull-in** | Schedule moved earlier | 05, 14 |
| **TMR** (Timeline / Milestone Roadmap) | Timeline reference document | 30 |
| **PDK** (Process Design Kit) | Partner's process design kit for chip design | 30 |
| **snapshot** | Roadmap revision document | 30 |
| **FOC** (Free of Charge) | Sample provided without charge | 14 |

### Enclosure / validation context

| Term | Meaning | Source textbook |
|:---|:---|:---|
| **enclosure** | Physical chassis housing samples | 14 |
| **DOA** (Dead on Arrival) | Sample that fails on first power-on | 14 |
| **Johnson City (JCY)** | Intel validation lab location | 30 |
| **GNR** (Granite Rapids) | Intel server CPU generation | 30 |
| **DMR** | Intel memory reference platform | 30 |
| **loopback** | Self-loop testing mode | 30 |
| **CMM** (CXL Memory Module) | SK Hynix's CXL memory module | 30 |

### Negotiation / soft-ask vocabulary

| Term | Meaning | Source textbook |
|:---|:---|
| **shopping list** | Metaphor for detailed request list | 30 |
| **big ticket item** | American idiom - expensive / complex item | 30 |
| **red box** | Visual reference to scope in slide | 30 |
| **stack alignment** | Technical compatibility alignment | 30 |
| **cold demo vs live demo** | Demo with recording vs live system | 08 |
| **best foot forward** | Presenting best version | 08 |
| **iron out the details** | Resolve remaining details | 13 |
| **stay tuned** | Wait for more information | 14 |
| **safer assumption** | Conservative estimate | 13 |

### Quantifier probes

| Term | Meaning | Source textbook |
|:---|:---|
| **minimum number of cards** | Smallest quantity that meets need | 30 |
| **whole setup** | Complete system (host + GPU + head node) | 30 |
| **expectation of involvement** | What level of partner engagement is expected | 30 |
| **first level** | Minimal engagement, partner already has setup | 30 |

---

## S6. 주간 학습 경로 (Weekly Learning Path)

5-day plan, 20 minutes per day. Use the 50 master expressions in S4. Each day focuses on one strategy cluster.

### Monday - Schedule alignment (S4 ec-001 to ec-007)

**Goal**: Internalize "align" as the master verb.

- **0-5 min**: Read ec-001, ec-003, ec-004 aloud 3 times each
- **5-10 min**: Write 3 sentences using "align our schedule with your schedule" for different partners (NVIDIA, AMD, Intel)
- **10-15 min**: Shadow textbook 30 excerpt 2 (line 36-50, schedule alignment language)
- **15-20 min**: Write a mock opening: "We had touched the status of X last time. We want to align our schedule with your schedule and see whether it is aligning or not. Is this timeline good or are we missing your launch?"

### Tuesday - Sample / milestone language + pull-in (ec-008 to ec-018)

**Goal**: Fluency in ES / CS / MP / QS vocabulary and pull-in requests.

- **0-5 min**: Read ec-008, ec-010, ec-015 aloud 3 times each
- **5-10 min**: Write 3 sample-type statements: "we may support the ES sample at end of Q3", "it's already CS candidate", "the X schedule pushed out two months"
- **10-15 min**: Shadow textbook 05 (NVIDIA) - pull-in language: "we're trying to pull in X"
- **15-20 min**: Write a gap-probe question: "you're gonna make a short timeline between QS and production just two months - is that clear?"

### Wednesday - Internal deferral + pushback (ec-019 to ec-045)

**Goal**: Master the "I cannot commit, but I will not say no" patterns.

- **0-5 min**: Read ec-019, ec-020, ec-031 aloud 3 times each
- **5-10 min**: Write 3 deferral responses using "let us discuss internally", "Let me talk with our VP", "I'm not going to commit for that yet"
- **10-15 min**: Shadow textbook 14 (AMD) - partnership framing and FOC shift
- **15-20 min**: Write a soft-denial: "I don't believe that we do that for CXL, but please jump in and let me know if I'm being correct here. We can go and confirm where we're at and come back."

### Thursday - Soft ask + misunderstanding recovery (ec-024 to ec-048)

**Goal**: Learn to ask for partner resources without sounding demanding, and to recover from being wrong cleanly.

- **0-5 min**: Read ec-024, ec-027, ec-046 aloud 3 times each
- **5-10 min**: Write a soft ask using past precedent + future want: "we had a collaboration about X previously... we would like some collaboration about Y for the future"
- **10-15 min**: Shadow textbook 30 excerpt 3 (line 42-60, misunderstanding recovery)
- **15-20 min**: Write a recovery: "it's my misunderstanding. I just wonder do we miss the your timeline. Okay okay okay I understand that."

### Friday - Action items + Audrey correction (ec-049 to ec-050 + S7)

**Goal**: Convert discussion into action items. Then Audrey's Friday correction.

- **0-5 min**: Read ec-049, ec-050 aloud 3 times each
- **5-10 min**: Write a closing: "let's align then so go and understand on your side. I'll look at the same on my side. Give me one maybe two weeks."
- **10-15 min**: Shadow textbook 30 excerpt 5 (line 124-145, action items + phased plan)
- **15-20 min**: Audrey Friday correction (see S7)

---

## S7. Audrey 금요일 교정 노트 (Audrey's Friday Correction)

Audrey reviews the week's written dumps. Focus on these recurring issues from type-C textbook analysis.

### Issue 1: Over-apologizing when wrong

**Learner writes**: "I'm sorry, I made a mistake."

**Audrey correction**: Use "it's my misunderstanding" instead. "Misunderstanding" attributes the error to interpretation, not competence. Then "Okay, I understand that" closes the loop. Do NOT over-apologize in English sync meetings.

### Issue 2: Asking "when" instead of risk-voice

**Learner writes**: "When will the ES sample be ready?"

**Audrey correction**: Use risk voice. "Is this timeline good or are we missing your launch?" This shows worry, which makes the partner want to reassure you with their actual timeline. "When" is a flat question that gets a flat answer.

### Issue 3: Hard ask instead of soft ask

**Learner writes**: "We need 8 Gaudi cards."

**Audrey correction**: Start with "some" and a minimum viable ask. "Just a single gpu card will be okay so one cpu plus with the one Gaudi gpu card." Then state the full need: "I believe at least you need eight cards." This shows you are reasonable and have thought through scaling.

### Issue 4: Blunt refusal

**Learner writes**: "We don't do that for CXL."

**Audrey correction**: Use "I don't believe" + invite correction. "I don't believe that we do that for CXL, but please jump in and let me know if I'm being correct here. We can go and confirm where we're at and come back." Soft deny + offer to verify + defer.

### Issue 5: No reason before the ask

**Learner writes**: "What is your schedule?"

**Audrey correction**: Give the reason first. "We'd like to know the schedule so we can update the new Intel TMR's the timeline." This justifies the question. Without a reason, the partner feels interrogated.

### Issue 6: Vague ask without precedent

**Learner writes**: "We want collaboration on AI systems."

**Audrey correction**: Frame as a continuation. "We had a collaboration about the performance testing previously. We would like some collaboration about this AI system for the future." Past precedent + future want makes a new request feel like relationship maintenance.

### Issue 7: No time-box on deferral

**Learner writes**: "Let me check and get back to you."

**Audrey correction**: Time-box it. "Give me one maybe two weeks to understand." The "maybe" softens but "one to two weeks" is the commitment.

### Friday dump writing target

Write 5 sentences (one per issue above), corrected by Audrey. Submit to Steve for review by Friday 17:00 KST.

---

## S8. 한계와 신뢰도 (Limitations and Reliability)

### Source coverage

- 9 type-C textbooks distilled (05, 08, 10, 12, 13, 14, 27, 29, 30)
- Total source expressions: 481 (52 + 48 + 52 + 52 + 57 + 60 + 50 + 52 + 48)
- Master DB: 50 entries (10.4% distillation rate)
- Coverage: all 5 partners represented (NVIDIA, Liqid, AMD, Lenovo, Intel)

### What this volume CANNOT do

- It is NOT a substitute for reading individual textbooks. Each textbook has 50+ expressions with full context - this volume distills only the cross-textbook patterns.
- It does NOT cover type-A (technical deep-dive) or type-B (one-shot negotiation) meetings.
- It does NOT include every FOC / DOA / enclosure variant - only the high-structural-value ones.
- The "shopping list" and "two-negative deflection" patterns are type-unique to single textbooks (30 and 27) - they may not generalize to all partners.

### Cross-textbook pattern confidence

| Pattern | Textbook count | Confidence |
|:---|:---|:---|
| Schedule alignment ("align") | 1 (30) | Medium - type-unique to Intel but high structural value |
| Internal deferral | 4 (13, 14, 27, 29) | High - appears across Liqid, AMD, Lenovo |
| Timeline hedging | 5 (08, 10, 12, 13, 29) | High - universal across all sync meetings |
| Action item capture | 4 (08, 12, 13, 14) | High |
| Quantity pin-down | 5 (08, 13, 14, 27, 29, 30) | High |
| Pull-in request | 3 (05, 14, 29) | Medium-high |
| Soft ask | 2 (30, 13) | Medium - concentrated in Intel and Liqid Biweekly |
| Partnership framing | 1 (14) | Low confidence, type-unique to AMD |
| Misunderstanding recovery | 1 (30) | Low confidence, type-unique to Intel |
| FOC / enclosure language | 1 (14) | Low confidence, type-unique to AMD |

### Use guidance

- For high-confidence patterns (internal deferral, timeline hedging, quantity pin-down): use directly in any partner sync.
- For medium-confidence patterns (schedule alignment, soft ask, pull-in): use with awareness that some partners may not use this register.
- For low-confidence type-unique patterns (partnership framing, misunderstanding recovery, FOC shift): use only with the specific partner textbook where they originate. Do not generalize to all partners.

### Refresh policy

This volume should be refreshed when:
- A new type-C textbook is added to the corpus
- A pattern appears in 3+ new textbooks (upgrade confidence)
- A pattern is contradicted by a new textbook (downgrade confidence)
- Audrey flags a recurring learner error not covered in S7

---

*Essence E-C - sample/schedule coordination. Distilled from 9 type-C textbooks on 2026-09-01. 50 master expressions. UTF-8 markdown.*
