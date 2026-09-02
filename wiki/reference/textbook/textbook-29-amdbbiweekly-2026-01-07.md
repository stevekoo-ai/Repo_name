---
textbook_id: 29
meeting: AMD biweekly
date: 2026-01-07
type: C (sample/schedule coordination)
partner: AMD (Ketan, Keith, Santosh, Rowan)
sk_side: SK Hynix CXL SW/App team (Jerry, Yoon Jung, Rita, Hyoung-Jun)
duration_words: 7121
audio: repo/webex-audio/2026-01-07 09 04 54_EN_AMDbiweekly-extracted.wav
transcript: repo/webex-audio/2026-01-07 09 04 54_EN_AMDbiweekly-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, amd, cxl, biweekly, sample-coordination, pre-es, evb, thermal, gpu-eval, tiering]
---

# Textbook 29 - AMD Biweekly (2026-01-07)

> **Meeting type**: C (sample/schedule coordination) - confirmed. Sample timing, enclosure vs no-enclosure, quantity (50-60) for volume validation, thermal model feedback by Q1.
> **Learning value**: The "polite proposal + counter-probe + commitment-soft" dance of a biweekly sync. SK side proposes timeline tables; AMD side probes risk, then soft-defers commitment.
> **Audrey view**: This is a coordination meeting, not a pitch. The skill here is **managing expectations on both sides without breaking the relationship** - you'll learn how to push a schedule, push back on a request, and defer a commitment without saying "no".

---

## 1. Speech architecture - SK proposal table + AMD probe-defer (5 stages)

This biweekly follows a fixed 5-stage architecture. The SK side opens with a **table-driven proposal**, the AMD side probes for risk, then both sides converge on a soft target. Each stage has a fixed language formula - that's the backbone you copy.

### Stage 1: Proposal open with timeline options (Option-then-Ask)

SK opens with a 2-option timeline and immediately asks for the partner's preference. Never a single take-it-or-leave-it - always branches.

| Speech formula | Original | Function |
|:---|:---|:---|
| `if X, we can provide in Y. But if Z is required, maybe we can provide in W` | "we can provide the pre-year sample in April this year. But if an inclusion is required, maybe we can provide in June this year" | Branch the timeline by feature |
| `So could you please let us know your thoughts about this proposal` | "So could you please let us know your thoughts about this proposal" | Close with polite choice-ask |
| `Is the X time frame would be sufficient without Y?` | "Is the April time frame would be sufficient without the case? Is it okay?" | Yes/no narrowing |

**Audrey lesson**: English coordination meetings open with **options, not answers**. "If X we can do April, but if Y we can do June" - you give the partner a choice so the conversation becomes "which option" instead of "yes/no". Korean style is to propose one date and wait; English style branches and asks preference.

### Stage 2: Risk probe by partner (Concern-then-Consequence)

AMD doesn't reject the date - they probe the risk consequence. The concern is named, then the consequence is unpacked.

| Speech formula | Original | Function |
|:---|:---|:---|
| `The only concern I have is are we going to run into any X without Y?` | "The only concern I have is are we going to run into any thermal issues without it having a case?" | Concern framing - polite doubt |
| `I am not sure how much testing you guys will have done by then` | "I am not sure how much testing you guys will have done by then. To determine if no casing is sufficient." | Hedged probe - "I am not sure" |
| `if we hit the thermal issue then we have to get sidetracked with the real problem` | "if we hit the thermal issue then we have to get sidetracked with the real problem" | Consequence reasoning |
| `they are not going to go draw in debug` | "They are not going to go draw in debug. They are just going to remove the cards" | Stakeholder behavior prediction |

**Audrey lesson**: When the partner proposes a tight date, you don't say "no, that's risky". You say "**The only concern I have is are we going to run into X**" - "concern" not "problem", "are we going to run into" (we together) not "you will cause". Then you unpack the consequence so the partner sees the risk themselves.

### Stage 3: Re-attribution of concern to a third party (Concern Brokerage)

The riskiest move - Ketan attributes the thermal concern to "Ketan" himself in third person. SK does the same when they push back: it's not "I think", it's "Ketan is concerned".

| Speech formula | Original | Function |
|:---|:---|:---|
| `I think X is concerned in general about Y` | "I think Ketan is concerned in general about if we hit the thermal issue" | Third-party attribution softens the push |
| `even on your side you can give us feedback if that's reasonable or not` | "even on your side you can give us feedback if that's reasonable or not. Rather than having this try out" | Reframe ask as feedback request |

**Audrey lesson**: When you push back on a partner, attribute the concern to a stakeholder who isn't in the room. "I think Ketan is concerned about..." - it's no longer you vs the partner, it's "the constraint" vs the proposal. This is a critical coordination meeting skill.

### Stage 4: Worst-case reframe + soft target (Worst-case-then-Target)

SK doesn't commit to a date either - they reframe their own schedule as "worst case" and propose a "target".

| Speech formula | Original | Function |
|:---|:---|:---|
| `the schedule in the table in the June timeframe, I think it's the worst case` | "the schedule in the table in the June timeframe for the pre-ES. I think it's the worst case" | Reframe own proposal as worst-case |
| `if we don't have any issue on X, we can deliver around the Y timeframe` | "if we don't have any issue on pre-engineering sample with the revision A. We can deliver around the early May timeframe with the inclusion" | Conditional best-case |
| `Let's let's target that` | "Let's let's target that" | Convergence - target setting |

**Audrey lesson**: Never commit to a single date in a coordination meeting. "**Let's target that**" - the word "target" replaces "promise". A target is a goal you aim for; a promise is a commitment you owe. Coordination meetings use "target", not "commit" or "promise".

### Stage 5: Action item assignment with scope (Action-with-Scope)

When the meeting lands an action, the assignment specifies the scope, not just the owner.

| Speech formula | Original | Function |
|:---|:---|:---|
| `if you don't mind, please have that action item to actually check with the X team` | "Ketan, if you don't mind, please have that action item to actually check with the DAE team members who are working on similar setup" | Action item request with scope |
| `I'll find that out and get back to you` | "Yeah, let me - I'll I'll find that out and get back to you" | Soft accept of action |
| `we will try to do best to deliver them as soon as possible` | "we will try to do best to deliver them as soon as possible" | Best-effort commitment (no specific date) |

**Audrey lesson**: Action items in coordination meetings are scoped, not just owned. "Check with the DAE team who are working on similar setup" - you tell the partner **who** to talk to and **what** to ask, not just "please check". And the accept is soft: "I'll find that out and get back to you" - not "I'll do it", but "I'll find out".

---

## 2. Hedging & deflection strategies

The core learning value. Both sides use soft-defer language to avoid "no" while making "no" the practical answer.

### Strategy 1: "I'm not going to commit for that yet" (Soft Refusal)

AMD refuses a tighter timeline by stating non-commitment directly but with a "yet" that promises future.

| Situation | Original speech | Translation |
|:---|:---|:---|
| Preliminary perf data in 2 weeks | "but in any preliminary data would be available like in in couple of weeks - And no, I'm not going to commit for that yet. Uh, let's let's let us the team work through the functional testing first and then we will jump into, uh, the performance" | "수치 데이터 2주 안에 가능할까요 - 아뇨, 아직 커밋은 못 합니다. 기능 테스트 끝나고 성능 들어갈게요" |

**Pattern**: `I'm not going to commit for that yet. Let us X first and then we will Y.`

**Audrey lesson**: Korean style softens refusal with "검토해 보겠습니다". English coordination uses **"I'm not going to commit for that yet"** - direct refusal + "yet" (future) + condition ("let us X first"). The "yet" preserves the relationship; the "first" sets the precondition. Use this exact sequence.

### Strategy 2: "I'm being little conservative to be honest" (Self-disclosure hedge)

AMD hedges a 2-month estimate by naming the conservatism explicitly.

| Situation | Original speech | Translation |
|:---|:---|:---|
| Perf data in couple months | "if I'm being little conservative to be honest, but, uh, uh, just didn't want to commit something that we we might not get to that's the reason I'm seeing couple of months" | "솔직히 보수적으로 말씀드리는 건데, 우리가 못 할 약속은 하고 싶지 않아서 두 달 정도 말씀드립니다" |

**Pattern**: `I'm being conservative to be honest. Just didn't want to commit something that we might not get to.`

**Audrey lesson**: When you give a long timeline, name your conservatism. "I'm being conservative to be honest" - this transforms a disappointing number into a sign of reliability. You're not slow; you're reliable. Then "just didn't want to commit something that we might not get to" - you're protecting the partner from a broken promise. This is gold.

### Strategy 3: "We anticipate those" (Pre-emptive validation of concern)

AMD validates SK's concern before answering - acknowledges the gap is expected, not a bug.

| Situation | Original speech | Translation |
|:---|:---|:---|
| Performance gaps in early data | "There are gaps because we anticipate those because this is not tuned values, right? We anticipate those" | "차이가 있는데, 예상된 겁니다 - 튜닝된 값이 아니니까요. 예상된 겁니다" |

**Pattern**: `There are gaps because we anticipate those because X. We anticipate those.`

**Audrey lesson**: When your early data looks bad, you have two options - excuse it, or own it as expected. "We anticipate those" - the word "anticipate" turns a problem into a plan. Korean style is "예상된 현상입니다"; English coordination uses "we anticipate those" twice for emphasis. Repeat the verb - it sounds deliberate.

### Strategy 4: "That won't be open-ended" (Scope-fence on partner request)

AMD accepts a request but fences the scope immediately, before the partner can ask for more.

| Situation | Original speech | Translation |
|:---|:---|:---|
| GPU server access for SK team | "if they can time share it with Hynix, but, uh, that won't be open-ended. We'll have to be extremely specific about the experimentation" | "Hynix와 시간 공유 가능한지 확인하겠습니다 - 단, open-ended는 안 됩니다. 실험 범위 극히 구체적이어야 합니다" |

**Pattern**: `we can X, but that won't be open-ended. We'll have to be extremely specific about Y.`

**Audrey lesson**: When a partner asks for an open resource (server access, lab time, eng support), accept conditionally but fence the scope **before** they expand it. "That won't be open-ended" - the metaphor (open-ended = no end) makes the limit feel natural. "We'll have to be extremely specific" - "extremely" makes the firmness clear while staying polite.

### Strategy 5: "You're not wrong" + "But" (Validation-then-Pivot)

AMD validates SK's technical expectation, then pivots to "it depends" to defer the conclusion.

| Situation | Original speech | Translation |
|:---|:---|:---|
| 1R1W should be higher than 2R1W | "I don't disagree with you that one read one write has to be the highest. But it depends on a lot of things... You're not wrong." | "1R1W가 가장 높아야 한다는 점에 동의합니다 - 하지만 여러 요인에 따라 다릅니다... 틀린 말씀 아닙니다" |

**Pattern**: `I don't disagree with you that X. But it depends on a lot of things. You're not wrong.`

**Audrey lesson**: When the partner states a technically correct expectation that your data doesn't yet match, never say "but actually..." Start with **"I don't disagree with you that X"** (full validation), then "But it depends on a lot of things" (pivot to uncertainty), then "You're not wrong" (closing validation). The partner leaves feeling heard, not corrected.

### Strategy 6: "We'll get there" (Soft forward promise)

AMD refuses immediate answer but promises eventual arrival.

| Situation | Original speech | Translation |
|:---|:---|:---|
| Performance analysis | "So, uh, give us some time. But we'll get there in terms of expectation. You're not wrong." | "시간 좀 주세요. 기대치에는 도달할 겁니다. 틀린 말씀 아닙니다" |

**Pattern**: `Give us some time. But we'll get there in terms of X.`

**Audrey lesson**: "We'll get there" is the gentlest forward promise in English. It doesn't commit to a date, doesn't specify a path - it just says "we're moving and we'll arrive". Use this when you can't commit to a date but want to keep the partner's confidence. "Give us some time" + "we'll get there" - the pair is the most relationship-preserving deferral in the meeting.

---

## 3. Polite challenge patterns

The questioner's deferent technical probes - SK side uses these to push AMD without breaking the sync cadence.

### Question type 1: Branch-narrow confirm (April-or-May?)

| Speech formula | Original | Function |
|:---|:---|:---|
| `Is it X in Y time frame, in Z time frame? Or Z or Y? You said Y?` | "Is it without case in April time frame, in May time frame? Or May or April? You said April? Yes, right" | Quick branch-narrow - pin the answer |

**Audrey lesson**: When the partner's timeline is ambiguous, repeat both options back as a question. "April or May? You said April?" - this forces a yes/no confirmation. Don't ask "when is it"; ask "you said X - yes?". That's how you pin a soft commitment.

### Question type 2: Scope probe (What is the feedback you're looking for?)

| Speech formula | Original | Function |
|:---|:---|:---|
| `What is needed here?` | "What is needed here? Sorry Ketan, I may have lost track on this" | Honest reset - admit lost thread |
| `what is the feedback that you're looking for here?` | "but also question to Hyoung-Jun's like what is the feedback that you're looking for here?" | Scope-clarify the ask |
| `is there any kind of - you must have this feedback by this date for your product decision?` | "is there any kind of - you must have this feedback by this date for your product decision or your design decisions or anything like Q?" | Hard deadline probe |

**Audrey lesson**: When you don't understand a partner's request, admit it. "What is needed here? Sorry, I may have lost track" - admitting lost track is better than guessing wrong. Then "what is the feedback you're looking for" - clarify the ask, not the answer. And finally probe for hard deadline: "you must have this by Q?" - if there's a real date, you'll find it.

### Question type 3: Solid proposal check (Is there a solid proposal?)

| Speech formula | Original | Function |
|:---|:---|:---|
| `Is there a solid proposal that this is what you would want to do with the X?` | "Is there a solid proposal that this is what you would want to do with the GPU?" | Ask for concreteness |
| `So we can run it by the DAE team and we can run it by the AE team somebody has a GPU setup` | "So we can run it by the DAE team and we can run it by the AE team somebody has a GPU setup" | Internal routing preview |

**Audrey lesson**: When a partner proposes a vague collaboration, ask "**Is there a solid proposal that this is what you would want to do with X?**" - "solid proposal" sets the bar. The partner must produce concrete scope before you route internally. Don't say "we need more detail"; ask "is there a solid proposal".

### Question type 4: Configuration minimum probe

| Speech formula | Original | Function |
|:---|:---|:---|
| `is there any minimum configuration you need like` | "Jerry, maybe if - if a - if Ketan is able to find out a GPU server then is there any minimum configuration you need like" | Probe the floor of the ask |

**Audrey lesson**: When the partner asks for "a server" or "samples", ask for the **minimum**. "Is there any minimum configuration you need?" - this transforms an open ask into a bounded request. The partner must give you a number, not a wishlist. Use this every time a partner asks for resources.

### Question type 5: Confirmation by restate (You said April?)

| Speech formula | Original | Function |
|:---|:---|:---|
| `You said April? Yes, right.` | "You said April? Yes, right" | Quick restate-confirm |
| `So can you share with me how many the quantity` | "So can you can you uh share with me how many the quantity I mean we you estimate for that the pre-engineering sample. I think it was 50 or something like that" | Re-state own assumption + ask confirm |

**Audrey lesson**: Biweekly meetings are full of soft numbers - "50 or something like that". You confirm by re-stating your assumption: "I think it was 50 or something like that" - the partner either confirms ("50, 50, 50") or corrects. This is faster than asking "how many" cold.

---

## 4. Negotiation & action item language

The heart of a Type C meeting. Sample schedule, quantity, scope, and action items.

### Negotiation: Timeline target setting

| Speech | Speaker | Original | Function |
|:---|:--:|:---|:---|
| Conditional best-case | SK | "if we don't have any issue on pre-engineering sample with the revision A. We can deliver around the early May timeframe with the inclusion" | Conditional best-case |
| Worst-case frame | SK | "the schedule in the table in the June timeframe for the pre-ES. I think it's the worst case" | Self-reframe as worst-case |
| Target lock | AMD | "Let's let's target that" | Convergence verb - "target" |
| Quantity pin | AMD | "So can you share with me how many the quantity I mean we you estimate for that the pre-engineering sample. I think it was 50 or something like that" | Confirm quantity |
| Quantity confirm | AMD | "50 for volume. 50 for volume for volume validation Ketan" | Triple-repeat for lock-in |

**Audrey lesson**:
- "Let's target that" - the verb "target" replaces "agree" or "promise". A target is a shared aim, not a contract. Use "target" in every biweekly convergence.
- The triple-repeat "50, 50, 50" / "50 for volume, 50 for volume for volume validation" is the spoken equivalent of bold text. When you want a number locked in a meeting, repeat it. Three times is the magic number.

### Negotiation: Resource ask with scope-fence

| Speech | Speaker | Original | Function |
|:---|:--:|:---|:---|
| Open ask | SK | "we would like to know if that kind of a GPU infrastructure, yeah, can be available in at the AMD site" | Open resource ask |
| Scope-fence accept | AMD | "if they can time share it with Hynix, but, uh, that won't be open-ended. We'll have to be extremely specific about the experimentation" | Conditional accept + scope limit |
| Routing preview | AMD | "So we can run it by the DAE team and we can run it by the AE team somebody has a GPU setup" | Internal routing preview |
| Action item assign | AMD | "Ketan, if you don't mind, please have that action item to actually check with the DAE team members who are working on similar setup" | Action item with scope |

**Audrey lesson**: When you accept an open ask, immediately fence it. "That won't be open-ended" + "extremely specific" - these two phrases turn a vague yes into a bounded yes. The partner leaves knowing they got a yes, but you've kept control of scope.

### Action item language

| Speech | Speaker | Original | Function |
|:---|:--:|:---|:---|
| Soft accept | AMD | "Yeah, let me - I'll I'll find that out and get back to you" | "I'll find that out" - not "I'll do it" |
| Best-effort commit | SK | "we will try to do best to deliver them as soon as possible" | "try to do best" - no specific date |
| Action item request | AMD | "Ketan, if you don't mind, please have that action item to actually check with the DAE team" | Action item assignment with politeness |
| Action item scoping | AMD | "to check with the DAE team members who are working on similar setup" | Scope - who to ask |
| Conditional deliver | SK | "even if evaluation board has some issue, if you want to have a little more this evaluation card let us know" | Conditional offer - "if you want X, let us know" |
| Email follow-up commit | AMD | "could could you please uh email us? Uh, uh, yeah" | Email as follow-up channel |
| Timeline-bound action | SK | "what is the feedback that you're looking for here? ... you must have this feedback by this date" | Probe for hard deadline |
| Deadline answer | SK | "I think the Q1 timeframe - next four weeks. Yeah, February will be better" | Deadline answer with preferred earlier |

**Audrey lesson**:
- "I'll find that out and get back to you" - never say "I'll do it" in a biweekly. You "find out" (gather info) and "get back" (return with answer). This protects you if the answer is no.
- "Try to do best to deliver as soon as possible" - "try" + "best" + "as soon as possible" - three softeners, no specific date. Use this when you cannot commit a date but want to show effort.
- "If you want X, let us know" - SK's pattern. You offer, the partner must ask. Don't push resources on a partner - put the option on the table and let them pull.

---

## 5. Domain vocabulary with exact usage context

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **pre-ES (pre-engineering sample)** | Stage between EVB and early ES - has enclosure, standard form factor | "the pre-ES in the middle between the EVV and early ES. They will have an enclosure standard form factor size" |
| **EVB (evaluation board)** | Open PCB for early lab eval, no enclosure | "the EVB you already have and currently available. There is no enclosure" |
| **enclosure / inclusion** | The case around the card for thermal dissipation | "if an inclusion is required, maybe we can provide in June" / "no casing is sufficient" |
| **form factor E3.S** | Standard server slot spec | "the form factor is E3.S. Because the cards we have today those are not conforming to the form factor" |
| **volume validation** | Production-scale validation with 50+ cards in real servers | "50 for volume. 50 for volume for volume validation Ketan" |
| **link retrain** | PCIe/CXL link re-establishment test | "we have run link retrained and that passed the past 35 000 cycles" |
| **link enable/disable** | Link state transition test | "for link enable disable we saw about 12 failures out of 35 000 cycles" |
| **SBR** | (Subsystem Boundary Register) - link stability metric | "but like SBR we saw about seven failures out of 35 000 cycles" |
| **stepping** | Silicon revision - new mask fixes | "they will improve its latency for their next stepping of the controller" |
| **revision A PCB** | First PCB revision for pre-ES | "if we don't have any issue on pre-engineering sample with the revision A" |
| **auto numa** | Linux kernel automatic NUMA tiering | "the experiments we ran was with auto numa and the TPP enhancement" |
| **TPP (Transparent Page Placement)** | Linux kernel tiering framework | "auto numa and the TPP enhancement that the team was working on is already submitted as patch request" |
| **Venice** | AMD next-gen server platform | "Related to Venice so they have not had a chance to go and run the simulation" |
| **MI GPU** | AMD Instinct MI series GPU (chip-down, not PCIe) | "the AMD GPU is not a PCIe form factor, right - it is chip-down" |
| **vLLM** | Open-source LLM inference engine | "based on the NVIDIA Dynamo software stack and the vLLM" |
| **NVIDIA Dynamo** | NVIDIA inference serving stack | "based on the NVIDIA Dynamo software stack" |
| **KV cache offloading** | Move KV cache from GPU to CXL pool | "the industry are exploring the KV cache of loading from the GPU's memory to the disagreed memory pool" |
| **memory pooling POC** | Proof-of-concept for shared CXL memory | "the next step will be the using our the POC of the memory pooling system" |
| **thermal models / simulation** | CFD thermal simulation input for module design | "SK Hynix provided some thermal models for the 512 gigabyte module. They wanted to see what profile we could obtain with running simulations" |
| **XConn** | Switch vendor acquired by Marvell | "I think you saw the news - XConn got acquired by Marvell" |
| **DAE / AE team** | AMD internal teams - Design Automation Eng / Application Eng | "we can run it by the DAE team and we can run it by the AE team" |
| **QTR** | (Quarterly Technical Review) prior cross-team review | "during the QTR - that discussion was 50 to 60 but - I think that the Cox mentioned that..." |
| **lattice** | (here) in-memory database class - Redis-like | "we need to have some the client application for based on the lattice" |

---

## 6. Expression Database

52 entries with prefix m29. Each tagged with category, function, speaker role, difficulty (1-5), context, pattern, note.

```yaml
# ── Proposal opening (Option-then-Ask) ──
- id: m29-001
  expression: "if X, we can provide in Y. But if Z is required, maybe we can provide in W"
  category: proposal_open
  function: branched_timeline
  speaker_role: proposer
  difficulty: 4
  context: "we can provide the pre-year sample in April this year. But if an inclusion is required, maybe we can provide in June this year"
  note: Never single-date - always branch by feature

- id: m29-002
  expression: "So could you please let us know your thoughts about this proposal"
  category: proposal_close
  function: choice_ask
  speaker_role: proposer
  difficulty: 3
  context: "So could you please let us know your thoughts about this proposal"
  note: Polite close - ask for thoughts, not decision

- id: m29-003
  expression: "Is the X time frame would be sufficient without Y?"
  category: yes_no_narrow
  function: answer_pin
  speaker_role: proposer
  difficulty: 3
  context: "Is the April time frame would be sufficient without the case? Is it okay?"

- id: m29-004
  expression: "I think maybe let me reiterate"
  category: soft_reset
  function: reframe
  speaker_role: proposer
  difficulty: 3
  context: "I think maybe let me reiterate"
  note: "maybe" softens the restart - polite re-state

# ── Risk probe (Concern-then-Consequence) ──
- id: m29-005
  expression: "The only concern I have is are we going to run into any X without Y?"
  category: concern_frame
  function: polite_doubt
  speaker_role: partner
  difficulty: 4
  context: "The only concern I have is are we going to run into any thermal issues without it having a case?"
  note: "concern" not "problem", "are we" (together) not "will you"

- id: m29-006
  expression: "I am not sure how much testing you guys will have done by then"
  category: hedged_probe
  function: uncertainty_state
  speaker_role: partner
  difficulty: 3
  context: "I am not sure how much testing you guys will have done by then. To determine if no casing is sufficient"

- id: m29-007
  expression: "if we hit the thermal issue then we have to get sidetracked with the real problem"
  category: consequence
  function: risk_unfold
  speaker_role: partner
  difficulty: 4
  context: "if we hit the thermal issue then we have to get sidetracked with the real problem"

- id: m29-008
  expression: "they are not going to go draw in debug. They are just going to remove the cards"
  category: stakeholder_predict
  function: behavior_forecast
  speaker_role: partner
  difficulty: 4
  context: "If they are going into that it is not going to be people hanging out there to see what if you are having issues. They are going to remove the cards"
  note: Predict the worst behavior of the end stakeholder - this justifies the concern

# ── Concern brokerage (third-party attribution) ──
- id: m29-009
  expression: "I think X is concerned in general about Y"
  category: third_party_concern
  function: brokerage
  speaker_role: partner
  difficulty: 5
  context: "I think Ketan is concerned in general about if we hit the thermal issue then we have to get sidetracked"
  note: Attribute concern to non-present stakeholder - depersonalizes pushback

- id: m29-010
  expression: "even on your side you can give us feedback if that's reasonable or not"
  category: reframe_ask
  function: feedback_request
  speaker_role: partner
  difficulty: 4
  context: "even on your side you can give us feedback if that's reasonable or not. Rather than having this try out"
  note: Refuse a trial - ask for analysis instead

# ── Worst-case reframe + soft target ──
- id: m29-011
  expression: "the schedule in the table in the X timeframe, I think it's the worst case"
  category: self_reframe
  function: worst_case_state
  speaker_role: proposer
  difficulty: 4
  context: "the schedule in the table in the June timeframe for the pre-ES. I think it's the worst case"
  note: Reframe own proposal as worst-case to enable better-case offer

- id: m29-012
  expression: "if we don't have any issue on X, we can deliver around the Y timeframe"
  category: conditional_best
  function: best_case_offer
  speaker_role: proposer
  difficulty: 4
  context: "if we don't have any issue on pre-engineering sample with the revision A. We can deliver around the early May timeframe with the inclusion"

- id: m29-013
  expression: "Let's target that"
  category: convergence
  function: target_lock
  speaker_role: either
  difficulty: 3
  context: "Let's let's target that"
  note: "target" not "promise" - shared aim, not contract

- id: m29-014
  expression: "So can you share with me how many the quantity I mean we estimate for X"
  category: quantity_pin
  function: number_confirm
  speaker_role: partner
  difficulty: 3
  context: "So can you can you uh share with me how many the quantity I mean we you estimate for that the pre-engineering sample. I think it was 50 or something like that"

- id: m29-015
  expression: "X for Y, X for Y for Y validation"
  category: triple_lock
  function: number_reinforce
  speaker_role: partner
  difficulty: 3
  context: "50 for volume. 50 for volume for volume validation Ketan"
  note: Triple-repeat locks the number in the meeting memory

# ── Soft refusal (I'm not going to commit for that yet) ──
- id: m29-016
  expression: "I'm not going to commit for that yet. Let us X first and then we will Y"
  category: soft_refusal
  function: defer_with_condition
  speaker_role: partner
  difficulty: 5
  context: "no, I'm not going to commit for that yet. Uh, let's let's let us the team work through the functional testing first and then we will jump into the performance"
  note: Direct refusal + "yet" (future) + precondition. Use this exact sequence.

- id: m29-017
  expression: "I'm being conservative to be honest"
  category: self_disclosure
  function: conservatism_name
  speaker_role: either
  difficulty: 4
  context: "if I'm being little conservative to be honest, but, uh, uh, just didn't want to commit something that we we might not get to"
  note: Name your conservatism - turns slow into reliable

- id: m29-018
  expression: "just didn't want to commit something that we might not get to"
  category: rationale
  function: promise_protect
  speaker_role: either
  difficulty: 4
  context: "just didn't want to commit something that we we might not get to that's the reason I'm seeing couple of months"
  note: Frame long timeline as protecting partner from broken promise

- id: m29-019
  expression: "There are gaps because we anticipate those because X"
  category: pre_emptive_validation
  function: expected_problem
  speaker_role: partner
  difficulty: 4
  context: "There are gaps because we anticipate those because this is not tuned values, right? We anticipate those"
  note: Repeat the verb - sounds deliberate

- id: m29-020
  expression: "that won't be open-ended. We'll have to be extremely specific about Y"
  category: scope_fence
  function: resource_limit
  speaker_role: partner
  difficulty: 5
  context: "if they can time share it with Hynix, but, uh, that won't be open-ended. We'll have to be extremely specific about the experimentation"
  note: Accept open ask conditionally, fence scope immediately

- id: m29-021
  expression: "I don't disagree with you that X. But it depends on a lot of things"
  category: validate_pivot
  function: full_validation_then_uncertainty
  speaker_role: partner
  difficulty: 5
  context: "I don't disagree with you that one read one write has to be the highest. But it depends on a lot of things"
  note: Never "but actually..." - always full validation first

- id: m29-022
  expression: "You're not wrong"
  category: closing_validation
  function: agree_preserve
  speaker_role: partner
  difficulty: 3
  context: "You're not wrong. Um, one read one write has much higher efficiency than two read one write for CXL is expected to"

- id: m29-023
  expression: "give us some time. But we'll get there in terms of X"
  category: soft_forward
  function: future_promise
  speaker_role: partner
  difficulty: 4
  context: "So, uh, give us some time. But we'll get there in terms of expectation"
  note: "We'll get there" - gentlest forward promise in English

# ── Polite challenge (Branch-narrow, scope probe) ──
- id: m29-024
  expression: "Is it X in Y time frame, in Z time frame? Or Z or Y? You said Y?"
  category: branch_narrow
  function: pin_answer
  speaker_role: questioner
  difficulty: 3
  context: "Is it without case in April time frame, in May time frame? Or May or April? You said April? Yes, right"

- id: m29-025
  expression: "What is needed here? Sorry, I may have lost track on this"
  category: honest_reset
  function: thread_recover
  speaker_role: questioner
  difficulty: 4
  context: "What is needed here? Sorry Ketan, I may have lost track on this"
  note: Admit lost track - better than guessing wrong

- id: m29-026
  expression: "what is the feedback that you're looking for here?"
  category: scope_clarify
  function: ask_clarify
  speaker_role: questioner
  difficulty: 3
  context: "but also question to Hyoung-Jun's like what is the feedback that you're looking for here?"

- id: m29-027
  expression: "is there any kind of - you must have this feedback by this date for your product decision?"
  category: hard_deadline_probe
  function: deadline_extract
  speaker_role: questioner
  difficulty: 5
  context: "is there any kind of - you must have this feedback by this date for your product decision or your design decisions or anything like Q?"
  note: "Must have by this date" - extract the real deadline

- id: m29-028
  expression: "Is there a solid proposal that this is what you would want to do with X?"
  category: concreteness_check
  function: scope_bar
  speaker_role: partner
  difficulty: 4
  context: "Is there a solid proposal that this is what you would want to do with the GPU?"
  note: "Solid proposal" sets the bar - partner must produce concrete scope

- id: m29-029
  expression: "is there any minimum configuration you need like"
  category: minimum_probe
  function: bound_the_ask
  speaker_role: partner
  difficulty: 4
  context: "Jerry, maybe if - if a - if Ketan is able to find out a GPU server then is there any minimum configuration you need like"

- id: m29-030
  expression: "You said X? Yes, right"
  category: restate_confirm
  function: quick_lock
  speaker_role: questioner
  difficulty: 2
  context: "You said April? Yes, right"

# ── Negotiation - timeline / quantity / scope ──
- id: m29-031
  expression: "I'll find that out and get back to you"
  category: soft_accept
  function: info_gather_promise
  speaker_role: either
  difficulty: 3
  context: "Yeah, let me - I'll I'll find that out and get back to you"
  note: Never "I'll do it" - always "I'll find that out and get back"

- id: m29-032
  expression: "we will try to do best to deliver them as soon as possible"
  category: best_effort
  function: no_date_commit
  speaker_role: proposer
  difficulty: 3
  context: "Yeah, we will try to do best to deliver them as soon as possible"

- id: m29-033
  expression: "if you don't mind, please have that action item to actually check with the X team"
  category: action_item_request
  function: scoped_assign
  speaker_role: either
  difficulty: 4
  context: "Ketan, if you don't mind, please have that action item to actually check with the DAE team members who are working on similar setup"

- id: m29-034
  expression: "even if X has some issue, if you want to have a little more Y, let us know"
  category: conditional_offer
  function: pull_not_push
  speaker_role: proposer
  difficulty: 4
  context: "even if evaluation board has some issue - even though evaluation board has some issue for the summer or the no inclusion, I mean nonetheless if you want to have a little more this evaluation card for this let us know"
  note: Offer, partner must ask - don't push resources

- id: m29-035
  expression: "we are talking about two things. One is X, second one is Y"
  category: thread_untangle
  function: clarify_threads
  speaker_role: either
  difficulty: 4
  context: "Yeah, okay, we are talking about two things. One is EVB if as per the discussion during QTR - then Keith maybe you Keith needs to go back and check if AMD needs more EVB - that's one. And second one is we are saying like in May time frame we will have a three ES samples with the case and then we need to know like a quantity"

- id: m29-036
  expression: "I anticipated that answer"
  category: expectation_state
  function: predict_ack
  speaker_role: questioner
  difficulty: 3
  context: "Oh - I - yes, I anticipated that answer"
  note: Pre-acknowledge the soft answer - shows you read it coming

- id: m29-037
  expression: "Q1 timeframe - next four weeks. Yeah, February will be better"
  category: deadline_answer
  function: deadline_with_preferred
  speaker_role: questioner
  difficulty: 3
  context: "I think the Q1 timeframe - next four weeks. Yeah, but next four weeks. Yeah, but February will be better"

# ── Deflection by network drop / time ──
- id: m29-038
  expression: "Sorry, my network is behaving today. Can you repeat the last two statements, please?"
  category: network_reset
  function: thread_replay
  speaker_role: either
  difficulty: 2
  context: "Sorry my network is behaving today. Can can you repeat the last two statements, please? I lost you after uh in between"

- id: m29-039
  expression: "I lost my network for a few minutes in between"
  category: network_drop
  function: session_resume
  speaker_role: either
  difficulty: 2
  context: "I think let let's - sorry actually I lost my network for a few minutes in between. Um, Jerry I lost your previous comments"

- id: m29-040
  expression: "I need to drop it now until next four years"
  category: meeting_drop
  function: parallel_meeting
  speaker_role: either
  difficulty: 2
  context: "I'm going to drop it now until next four years if do you have any more slides?"
  note: "Drop" = leave meeting for parallel commitment

- id: m29-041
  expression: "I have another like a meeting can I drop it?"
  category: meeting_exit
  function: polite_leave
  speaker_role: either
  difficulty: 2
  context: "in the one more thing like I need I have another like a meeting can I drop it?"

# ── Discourse & coordination markers ──
- id: m29-042
  expression: "let's discuss next time. How about that?"
  category: defer_item
  function: skip_graceful
  speaker_role: either
  difficulty: 2
  context: "the another item is let's Discuss next time. How about that? Yes, it's okay to skip that"

- id: m29-043
  expression: "do you have any other comments or the questions"
  category: meeting_close
  function: open_floor
  speaker_role: either
  difficulty: 2
  context: "today is all of our item is done. So do you have any other any other comments or the questions"

- id: m29-044
  expression: "we'll keep you posted"
  category: update_promise
  function: ongoing_commit
  speaker_role: either
  difficulty: 2
  context: "sooner than that, but, uh, we'll we'll uh, we'll keep you posted"

- id: m29-045
  expression: "we'll have to dig into the details as to where it did stop"
  category: investigation_promise
  function: debug_commit
  speaker_role: partner
  difficulty: 4
  context: "There's obviously there is something that we would probably need to - I just had my team run the test and not stop the test. Um, but you know we'll have to dig into the details as to where it did stop"

- id: m29-046
  expression: "we can share the data if it's available earlier or any updates that we may find in between"
  category: conditional_share
  function: opportunistic_share
  speaker_role: partner
  difficulty: 4
  context: "we can share the data if it's available earlier or any updates that we may find in between"

- id: m29-047
  expression: "let me see if we can if we have a machine that we can spare"
  category: soft_resource_check
  function: internal_check
  speaker_role: partner
  difficulty: 3
  context: "let me see if we can if we have a - we have a machine that we can spare and then what configuration it is"

- id: m29-048
  expression: "as far as I know from the GPU site"
  category: knowledge_scope
  function: knowledge_bound
  speaker_role: partner
  difficulty: 3
  context: "there is no partner lab right for as as far as I know from the GPU site"

- id: m29-049
  expression: "but we'll have to be extremely specific about X"
  category: specificity_demand
  function: scope_lock
  speaker_role: partner
  difficulty: 4
  context: "We'll have to be extremely specific about the experimentation"

- id: m29-050
  expression: "we are aligned on X but he might not have been aware of Y"
  category: alignment_gaps
  function: agreement_with_caveat
  speaker_role: partner
  difficulty: 5
  context: "we are definitely aligned on - but he might not have been aware of the differences between the pump factors and the thermal challenges and the features as such"
  note: Validate exec alignment, flag detail gaps underneath

- id: m29-051
  expression: "let's get that details to the validation team and then come back to you with our response that does this make sense does this not make sense"
  category: internal_route
  function: route_and_return
  speaker_role: partner
  difficulty: 4
  context: "Let's get that details to the validation team and then come back to you with the our response that does this make sense does this not make sense"

- id: m29-052
  expression: "I'm missing the point"
  category: honest_admit
  function: thread_admit
  speaker_role: either
  difficulty: 2
  context: "Sorry. I'm missing the point"
  note: Quick admit - faster than guessing
```

---

## 7. Excerpt map (5 segments for Mon-Fri shadowing)

Audio: `repo/webex-audio/2026-01-07 09 04 54_EN_AMDbiweekly-extracted.wav` (~7,121 words, ~60 min)
5 recommended excerpts (~1-2 min each), Mon-Fri rotation.

| # | Time estimate | Line range | Summary | Learning point | Shadowing difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | Opening - proposal | line 1-22 | SK proposes April-without-case vs June-with-case; AMD probes thermal risk | Branched proposal + concern probe formula | ★★★ |
| 2 | Worst-case reframe | line 77-103 | SK reframes June as worst-case, offers early May with enclosure; AMD locks "Let's target that" | Worst-case-then-target convergence | ★★★ |
| 3 | Soft refusal | line 156-165 | AMD refuses 2-week perf data with "I'm not going to commit for that yet" + "conservative to be honest" | Soft refusal + self-disclosure hedge | ★★★★ |
| 4 | Scope-fence on GPU | line 211-228 | AMD accepts GPU server ask conditionally with "that won't be open-ended" + "extremely specific" | Scope-fence accept pattern | ★★★★ |
| 5 | Validate-pivot on perf | line 295-307 | AMD validates SK's 1R1W expectation with "I don't disagree with you" + "You're not wrong" + "we'll get there" | Full validation before pivot - relationship-preserving pushback | ★★★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, ... Fri: Excerpt 5
- Excerpt 5 is the highest value - the validate-pivot pattern is the most reusable across any technical meeting
- Excerpt 3 + 4 pair teach the two sides of soft refusal (refuse a date / accept a request with scope-fence)

---

## 8. Audrey's teaching notes

### Register (register) analysis
This is a **biweekly coordination** register - not a pitch, not a deep-dive. The register is "mutual schedule management with technical justification". Both sides hold information asymmetrically:
- **SK side role**: Proposer - presents tables, branches timelines, reframes worst-case
- **AMD side role**: Validator - probes risk, defers commitments, fences scope

You need both roles - when you propose a schedule to a partner, you're SK. When a partner asks you for resources, you're AMD. Both roles use soft language to avoid breaking the relationship while protecting their own constraints.

### Pragmatics core
1. **"Let's target that" replaces "let's agree"** - A target is a shared aim, not a contract. In a biweekly, you never "agree" - you "target". This preserves your right to slip.
2. **"I'm not going to commit for that yet"** - English coordination uses **direct refusal + "yet" (future) + precondition**. Korean style says "검토해 보겠습니다" (will review); English style says "I'm not going to commit yet - let us X first". The "yet" preserves the relationship; the precondition protects the timeline.
3. **Concern brokerage** - "I think Ketan is concerned about..." - when you push back, attribute the concern to a stakeholder not in the room. It's no longer you vs the partner; it's "the constraint" vs the proposal.
4. **Triple-repeat to lock a number** - "50 for volume. 50 for volume for volume validation." - in spoken English, repetition IS emphasis. Don't say "let me emphasize" - repeat the number three times.
5. **"You're not wrong" before "but it depends"** - never open a pushback with "but". Open with full validation ("I don't disagree with you that X"), close with another ("You're not wrong"), put the pivot in the middle ("But it depends on a lot of things"). The partner leaves feeling heard.

### Top 5 must-use
1. **"Let's target that"** - every biweekly convergence, replace "agree" with "target"
2. **"I'm not going to commit for that yet. Let us X first and then we will Y"** - soft refusal sequence
3. **"that won't be open-ended. We'll have to be extremely specific about Y"** - scope-fence on resource ask
4. **"I don't disagree with you that X. But it depends on a lot of things. You're not wrong."** - validate-pivot sequence
5. **"I think X is concerned in general about Y"** - concern brokerage to a non-present stakeholder

### Korean vs English comparison
| Korean style | English (this meeting) | Difference |
|:---|:---|:---|
| "4월에 가능합니다" | "if X, we can provide in April. But if Y is required, maybe we can provide in June" | Korean - single date; English - branched by feature |
| "검토해 보겠습니다" | "I'm not going to commit for that yet. Let us X first" | Korean - soft defer verb; English - direct refusal + yet + condition |
| "5월에 타겟합시다" | "Let's target that" | "target" replaces "agree/promise" |
| " Ketan이 우려합니다" | "I think Ketan is concerned in general about..." | Third-party attribution - depersonalize push |
| "틀린 말씀 아니지만" | "I don't disagree with you. You're not wrong. But it depends" | English requires double validation before pivot |
| "최악의 경우 6월" | "the June timeframe, I think it's the worst case" | Self-reframe as worst-case enables best-case offer |
| "자원 부족으로..." | "that won't be open-ended. We'll have to be extremely specific" | Korean - blame resource; English - scope-fence |

---

## 9. How to use this textbook

1. **Daily 20-min routine**: 5 excerpts (Section 7), Mon-Fri rotation. Excerpt 5 (validate-pivot) is the most reusable - hit it on Friday for retention.
2. **Expression DB**: 52 entries. Start with Top 5 in Section 8. The "soft refusal" (m29-016), "scope-fence" (m29-020), and "validate-pivot" (m29-021) entries are the highest structural value - drill them until they're reflexive.
3. **Audrey Friday dump**: This textbook is built for coordination meetings. Focus the Friday dump on the **concern brokerage** (m29-009) and **soft refusal** (m29-016) patterns - they're the hardest Korean-to-English shifts because they require you to NOT say the soft Korean verb.
4. **Compare study**: The Korean-vs-English table in Section 8 - the key shift is **direct refusal + "yet" + precondition** instead of soft "검토해 보겠습니다". Drill this difference.
5. **Pair with textbook 01**: This is the coordination counterpart to textbook 01's pitch. If 01 teaches you how to **present a product**, 29 teaches you how to **manage a partner week-to-week**. Use them in alternating weeks.

---

*Textbook 29 - AMD Biweekly (2026-01-07). Meeting type C (sample/schedule coordination). 52 expressions in DB. 5 excerpt segments. Written: 2026-09-01.*
