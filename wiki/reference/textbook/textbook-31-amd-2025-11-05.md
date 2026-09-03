---
textbook_id: 31
meeting: AMD (November technical deep-dive, architecture/product)
date: 2025-11-05
type: B (Roadmap/Supply alignment) - RECLASSIFIED from initial A
partner: AMD (Senior technical spokesperson, Rita - performance validation, Gary)
sk_side: SK hynix CXL collaboration lead, Yoon Jung (module verification engineer, Taiwan joint camp participant)
duration_words: 3357
audio: repo/webex-audio/2025-11-05 09 10 07_EN_AMD-extracted.wav
transcript: repo/webex-audio/2025-11-05 09 10 07_EN_AMD-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, amd, cxl, venice, florence, software-tiering, thermal-simulation, gpu-cxl, roadmap-alignment, proposal]
---

# Textbook 31 - AMD CXL Collaboration (2025-11-05)

> **Meeting type**: B (Roadmap/Supply alignment) - RECLASSIFIED from initial A. The transcript is agenda-driven proposal review, not single-product architecture deep-dive. CPU launch schedule confirmation + 3 formal collaboration proposals + technical Q&A.
> **Learning value**: How SK hynix structures proposals politely, how AMD receives with conditional acceptance, roadmap timeline language, technical pushback on power/spec, deflection via "we need to check".
> **Audrey view**: This meeting is "proposal + conditional acceptance" - the heart of partner collaboration. SK pushes 3 asks; AMD receives each with "yes, but we need to figure out". You must learn both sides.

---

## 1. Speaker architecture - Agenda-driven proposal flow

Unlike Marvell PFMA (one presenter, one product reveal), this meeting has **3 distinct talk architectures** layered. Master each.

### Architecture A: SK proposal structure (4-step formula)

Every SK proposal in this meeting follows the same 4-step formula. This is the structure you use when proposing collaboration to a partner.

| Step | Formula | Example from transcript |
|:---|:---|:---|
| 1. Context framing | `The main purpose of this collaboration is that we would like to X` | "The main purpose of this collaboration is that we would like to make the large and large and larger capacity over this extra interface" |
| 2. Problem statement | `So but the problem is the, as you know, X require Y` | "So but the problem is the, as you know, the large amount of the memory density require the power, a lot of power" |
| 3. Constraint statement | `So the limitation is the X. If we have the Y type.` | "So the limitation is the 40W. If we have the 2T type" |
| 4. Ask | `So we would like to X under considering of Y` | "So we would like to check the summer evaluation under considering of the power" |

**Audrey lesson**: English proposals do NOT start with "We want X." They start with **purpose** ("The main purpose is we would like to X"), then **problem** ("the problem is..."), then **constraint** ("the limitation is..."), then **ask** ("we would like to check"). This 4-layer structure makes the ask feel reasoned, not demanding. Memorize this skeleton.

### Architecture B: AMD reception structure (4-step response)

AMD responds to every proposal with the same 4-step formula. This is how a senior partner receives a proposal without committing.

| Step | Formula | Example |
|:---|:---|:---|
| 1. Validate | `You do bring up a very good point` / `Yes, we are absolutely interested` | "You do bring up a very good point. And the two components that are important in this is what is the controller power itself" |
| 2. Add nuance | `And the two components that are important in this is X and we debated that a lot in Y` | "we debated that a lot in JEDEC. I still think that the controller is taking more liberty on power than it should" |
| 3. Soft critique | `I still think that X is taking more liberty on Y than it should` | "I still think that the controller is taking more liberty on power than it should" |
| 4. Conditional collaboration | `If you have X, we can work on Y, but if you have Z, it would be good for us to exchange that information` | "if you have some theoretical tools which can calculate the powers... it would be good for us to exchange that information" |

**Audrey lesson**: AMD never says "yes" outright. The pattern is **validate -> nuance -> soft critique -> conditional**. "We are absolutely interested" is followed immediately by "if you have X, we can work on Y". The "if" clause is where the real negotiation happens. When a partner says "interested", listen for the "if" that follows.

### Architecture C: Engineer Q&A (Yoon Jung's verification query)

Yoon Jung shifts register from proposal to technical verification. Note the **humble preface** before technical asks.

| Step | Formula | Example |
|:---|:---|:---|
| 1. Self-intro with credential | `Hi, this is X from SK. Hi, who is a Y engineer and participated in Z` | "Hi, this is Yoon Jung from SK. who is a 6-year module verification engineer and participated in the Taiwan joint camp" |
| 2. Visual check | `Can you see my screen?` | "Can you see my screen?" |
| 3. Context summary | `We have run the test to verify our EVB for total X categories like Y` | "We have run the test to verify our EVB for total 13 categories like power, summer and control feature" |
| 4. Inverted question | `So before that, do you have any questions for our X?` | "So before that, do you have any questions for our bring up test list?" |
| 5. Direct ask | `Could you share the X with Y because we have not used Z?` | "Could you share the test plan or test items with AND Internet because we have not used AND GoPy" |

**Audrey lesson**: When a junior engineer takes the floor in a senior meeting, the humble preface matters. "Hi, this is X. Y engineer. Participated in Z." - establishes credibility before asking. Then "So before that, do you have any questions for our X?" - inverts the dynamic, offering the partner the floor first. This is Korean politeness translated to English.

---

## 2. Hedging/Deflection strategies (THE key value)

The most important section for this meeting. AMD deflects without ever saying "no" or "I don't know". SK also hedges on commitments.

### Strategy 1: Memory hedge - "I don't have it on top of my head"

When AMD doesn't recall a date, they avoid "I don't know" and use the idiom.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| SP8 PR timeline | "I don't have it on top of my head either. ... I'll have to double check the PR timeline" | "지금 머릿속에 없네요. PR 타임라인 다시 확인해봐야겠습니다" |

**Pattern formula**: `I don't have it on top of my head. I'll have to double check X.`

**Audrey lesson**: "I don't know" is amateur. "I don't have it on top of my head" is professional - it implies the information exists, just not currently accessible. Followed immediately by "I'll have to double check". The action commitment neutralizes the knowledge gap. Memorize this combo.

### Strategy 2: Roadmap caveat - "subject to change" with visual metaphor

AMD protects the Florence roadmap dates by referencing how they're visually drawn in their own roadmap.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Florence dates | "Florence is still in planning, different stages of planning, all the Florence products. So these dates are going to be... Like if you look at the way we present our roadmap, the WANSP7 and SP8 would be tarlick boxes, Florence boxes would be dotted boxes to say that these are in various stages of planning and subject to change" | "Florence는 아직 기획 단계여서, 저희 로드맵에서 SP7/SP8은 실선 박스, Florence는 점선 박스로 표시합니다 - 기획 중이라 언제든 바뀔 수 있다는 의미입니다" |

**Pattern formula**: `X is still in planning, different stages of planning. If you look at the way we present our roadmap, Y would be solid boxes, Z would be dotted boxes to say that these are in various stages of planning and subject to change.`

**Audrey lesson**: AMD doesn't say "the dates might change". They invoke a **visual metaphor** - "solid boxes vs dotted boxes" - to make the caveat tangible and blameless. "Subject to change" is the formal phrase, but the metaphor is what makes it land. When you give a roadmap that may shift, give the visual frame.

### Strategy 3: Soft accusation of partner's partner - "taking more liberty than it should"

AMD subtly criticizes the controller partner (not SK) for power numbers, deflecting blame away from themselves.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Controller power | "I still think that the controller is taking more liberty on power than it should. When I proposed original numbers, I proposed it with some conversations with our internal teams on what generally the number should be. And I think that the controller power is higher than it should be. So there is some potential there." | "컨트롤러가 전력에서 허용 범위보다 더 잡아먹고 있다고 봅니다. 제가 원래 제안한 수치는 내부팀과 논의한 일반적 기준이었는데, 현재 컨트롤러 전력이 그보다 높습니다. 개선 여지가 있습니다" |

**Pattern formula**: `I still think that X is taking more liberty on Y than it should. When I proposed original numbers, I proposed it with some conversations with our internal teams. So there is some potential there.`

**Audrey lesson**: AMD doesn't say "the controller vendor is bad". They say "taking more liberty on power than it should" - "liberty" is the polite word for "over-budget". And "there is some potential there" reframes the criticism as opportunity. This is gold: critique + opportunity in one sentence. Use this when discussing a third-party supplier's spec with a partner.

### Strategy 4: Hard limit with reason - "absolutely nothing we will be able to guide you on yet"

When AMD genuinely cannot help, they state the hard limit but explain why, with a future path.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Bias knob optimization | "So there is absolutely nothing that we will be able to guide you on yet till we get enough cards and run our performance testing" | "카드를 충분히 확보하고 성능 테스트를 돌리기 전까지는 안내해 드릴 수 있는 게 아직 아무것도 없습니다" |

**Pattern formula**: `There is absolutely nothing we will be able to guide you on yet till we X and run Y.`

**Audrey lesson**: Note "absolutely nothing" - strong negation - softened by "yet" and "till we X". The "yet" implies it will come. The "till we X" gives the condition. This is a hard "no" that feels like a "wait". When you cannot deliver now but will later, use this formula.

### Strategy 5: Concern framing - "What I'm finding concerning is"

AMD frames a soft pushback as a concern, not a complaint.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Power vs bandwidth ratio | "What I signed concerning is, I mean, we are seeing the power reduce over the speed that likes 5600 to 3200. But it is not very drastic, which means that our controller power is still kind of much higher. Is there something else we are missing?" | "제가 우려되는 건, 5600에서 3200으로 속도를 낮춰도 전력이 크게 안 줄더라는 겁니다. 컨트롤러 전력이 여전히 너무 높은 것 같습니다. 혹시 우리가 놓치는 게 있을까요?" |

**Pattern formula**: `What I'm finding concerning is X. But it is not Y, which means that Z. Is there something else we are missing?`

**Audrey lesson**: "I have a concern" is weak. "What I'm finding concerning is X" - the gerund "finding" makes it an active observation, not an opinion. Ending with "Is there something else we are missing?" turns the concern into a joint investigation, not an accusation. This is the polite way to challenge a partner's data.

### Strategy 6: Conditional collaboration - "if you have X, it would be good for us to exchange"

AMD proposes data exchange as conditional, not as commitment.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Theoretical tools | "if you have some theoretical tools which can calculate the powers and at various speeds at various capacity points, it would be good for us to exchange that information" | "전력을 다양한 속도/용량에서 계산하는 이론적 도구가 있으시면, 그 정보를 교환하면 좋겠습니다" |

**Pattern formula**: `If you have X which can Y, it would be good for us to exchange Z.`

**Audrey lesson**: Not "please send us X" but "if you have X, it would be good for us to exchange" - "exchange" implies reciprocity (we give, you give), making it a soft ask. And "if you have" gives the partner an out (if they don't have it, no obligation). This is negotiation-grade politeness.

### Strategy 7: Self-deprecating English preface - "I'm not good at English, sorry"

Yoon Jung uses a Korean self-deprecation pattern before a clarifying question.

| Situation | Original phrasing | Translation |
|:---|:---|:---|
| Bias knob clarification | "I'm not good at English, sorry, but so do you mean with next bias, you can optimize the performance?" | "영어가 부족해 죄송한데, 다음 bias로 성능 최적화가 가능하다는 뜻입니까?" |

**Audrey lesson**: This is a Korean-English pattern that Americans find endearing but unnecessary. Audrey's note: it's OK once, but English speakers don't preface with "I'm not good at English" - they just ask. Better version: "Just to clarify - do you mean X?" However, in a senior meeting where you're the junior, this self-deprecation signals humility and buys patience. Use sparingly.

---

## 3. Polite challenge patterns (Questioner side)

Both SK and AMD challenge each other's data and roadmap. These are the patterns you use to push back politely.

### Type 1: Direct confirmation check - "Is this information, updated information?"

| Formula | Original | Function |
|:---|:---|:---|
| `Is this information, updated information? Is it right?` | "Is this information, updated information? Is it right?" | Quick validation of partner's data |

**Audrey lesson**: Simple but effective. "Is this right?" is the most direct polite challenge. Use when you have your own data and want to cross-check.

### Type 2: Future probe - "Do you see transitions from X to Y happening anytime soon?"

| Formula | Original | Function |
|:---|:---|:---|
| `Do you see X happening anytime soon for Y?` | "do you see transitions from gen 6 to gen 7 happening anytime soon for the CXL controllers?" | Future roadmap probe without demanding commitment |

### Type 3: Rhetorical challenge - "Does it even make sense to X even if Y?"

| Formula | Original | Function |
|:---|:---|:---|
| `Does it even make sense to X even if Y? Let me ask it that way.` | "But it even makes sense to transition to gen 7 even if the CPU is capable. Let me ask it that way." | Reframes own question to soften it |

**Audrey lesson**: "Let me ask it that way" is a powerful self-correction marker - it signals you're refining your question live. This shows active thinking, not scripted attack.

### Type 4: Clarification probe - "Are you looking at it from the X or the next gen Y?"

| Formula | Original | Function |
|:---|:---|:---|
| `Are you looking at it from the X that we have on Y or is this the next gen Z?` | "Are you looking at it from the CMM that we have on Children or is this the next gen CMM that we are looking at?" | Scope clarification - which generation? |

**Audrey lesson**: "Are you looking at X or Y?" forces the partner to commit to scope. This prevents later misunderstanding about which product the discussion covers.

### Type 5: Inverted offer - "So before that, do you have any questions for our X?"

| Formula | Original | Function |
|:---|:---|:---|
| `So before that, do you have any questions for our X?` | "So before that, do you have any questions for our bring up test list?" | Give partner floor first, then ask |

**Audrey lesson**: This is the Korean way of asking - give the partner the chance to ask first, then ask yours. In English, this can confuse the flow because the partner expects you to drive. Use it intentionally as a courtesy, not as avoidance.

### Type 6: Concern-as-question - "Is there something else we are missing?"

| Formula | Original | Function |
|:---|:---|:---|
| `Is there something else we are missing?` | "Is there something else we are missing?" | Concern reframed as joint investigation |

### Type 7: Technical optimization probe - "Is there any bias option or any test option to optimize X?"

| Formula | Original | Function |
|:---|:---|:---|
| `Is there any X option or any Y option to optimize Z? Do you have any recommended option?` | "is there any bias option or any test option to optimize the performance? Do you have any recommended option?" | Technical ask, double-formulated for politeness |

---

## 4. Negotiation/Action item language (KEY section for Type B)

The heart of this textbook. Timeline targets, volume requests, spec pushback, milestone coordination - all the Type B language.

### Timeline targets

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `plan to get it to production is end of June, early July` | AMD | "plan to get it to production is end of June, early July. So that is correct" | Production target with quarter granularity |
| `Q4 is the right time for the PR` | AMD | "I think Q4 is the right time for the PR" | PR (production readiness) target |
| `Launch is couple months later` | AMD | "Launch is couple months later, so that's where you have" | Launch vs production distinction |
| `production will start next year, July` | SK | "Venice SP7, the production will start next year, July" | SK's understanding of partner schedule |
| `production started October, on October in 2028` | SK | "Florence SP8 and the LPDDR production started October, on October in 2028" | Multi-year roadmap statement |

**Audrey lesson**: Notice "plan to get it to production is end of June, early July" - AMD doesn't say "we will produce in July". They say "plan to get it to production is..." - the noun phrase "plan to get it to production" is the subject, not "we". This depersonalizes the commitment. Use this when you want to convey a target without personal guarantee.

### Volume/capacity requests

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `we would like to make the large and large and larger capacity over this extra interface` | SK | "we would like to make the large and large and larger capacity over this extra interface" | Capacity expansion request |
| `we have a plan to make the 512 GB memory motor using the Monolithic, the DRAM` | SK | "we have a plan to make the 512 GB memory motor using the Monolithic, the DRAM, the media" | Specific capacity target |
| `you don't like to provide that kind of a solution, 512 GB solution for the Florence` | SK | "You don't like to provide that kind of a solution, 512 GB solution for the Florence" | Specific product ask for specific platform |

### Spec pushback

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `the controller is taking more liberty on power than it should` | AMD | (see Section 2 Strategy 3) | Push back on partner's partner |
| `we are also under the debating... We should bring the gen 7 or gen 6 for the third gen` | SK | "we are also under the debating... We should bring the gen 7 or gen 6 for the third gen" | Internal indecision disclosure |
| `we should also consider the mechanical spec of this over` | SK | "we should also consider the mechanical spec of this over" | Mechanical constraint consideration |
| `That's where the TCO comes into play. Does the TCO make sense with X and Y in the front?` | AMD | "That's where the TCO comes into play. Does the TCO make sense with DDR5 and gen 7 in the front?" | TCO-based challenge |

### Milestone coordination - "aligned with" / "subject to"

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `these dates are going to be... subject to change` | AMD | "these are in various stages of planning and subject to change" | Caveat on roadmap |
| `we are the product and develop and on promotion schedule is based on the CPU schedule` | SK | "we are the product and develop and on promotion schedule is based on the CPU schedule" | SK's dependency statement |
| `If you have any update information, please let us know` | SK | "If you have any update information, please let us know" | Update request |
| `the WANSP7 and SP8 would be tarlick boxes, Florence boxes would be dotted boxes` | AMD | (see Section 2 Strategy 2) | Visual roadmap distinction |

### Soft commitment / "under consideration" language

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `I'll get back to you with what if they have more questions` | AMD | "I'll get back to you with what if they have more questions" | Soft follow-up commit |
| `We'll have to figure out who has that information` | AMD | "We'll have to figure out who has that information and we can see how we can share it" | Internal routing without commit |
| `I will let you know our projection and the opinion` | SK | "I will let you know our projection and the opinion" | Soft future commit |
| `I cannot share the much item today, but yeah, maybe we will let you know` | SK | "I cannot share the much item today, but yeah, maybe we will let you know" | Explicit deferral |
| `We need time to figure out more to make it clear` | SK | "There are a lot of discussion points. We need time to figure out more to make it clear" | Delay request |
| `we'll be happy to review and work with you on that` | AMD | "we'll be happy to review and work with you on that" | Polite acceptance without specifics |

### Proposal acceptance language (KEY)

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `Yes, we are absolutely interested and always happy to collaborate on any kind of white papers` | AMD | "Yes, we are absolutely interested and always happy to collaborate on any kind of white papers and collaboration material there, which can publications there, which can help" | Strong acceptance - white paper |
| `I'll be happy to review the proposal` | AMD | "I'll be happy to review the proposal and if you want to talk further in this meeting on that or have a meeting, I'll be happy to do that" | Review acceptance with meeting offer |
| `it is definitely interesting just that it has been very challenging to make it meaningful` | AMD | "it is definitely interesting just that it has been very challenging to make it meaningful" | Accept + caveat pattern |

**Audrey lesson**: "definitely interesting just that it has been very challenging" - the "just that" is the hedge that follows the positive. "Yes, interesting, just that hard." This is the polite partner pattern: positive word + "just that" + reality check. Use this when you want to accept in spirit while flagging difficulty.

### Action item language

| Phrase | Speaker | Original | Function |
|:---|:---:|:---|:---|
| `I will double check on that` | AMD | "I will double check on that" | Soft action item |
| `we'll have to double check the PR timeline` | AMD | "we'll have to double check the PR timeline" | Action with scope |
| `I'll get back to you with what if they have more questions` | AMD | "I'll get back to you with what if they have more questions" | Follow-up commit |
| `Please share the data after measurement` | SK | "Please share the data after measurement" | Direct action request |
| `we can see how we can share it` | AMD | "we can see how we can share it" | Tentative share commit |

**Audrey lesson**: Note AMD never says "I'll take an action item" (Marvell did). AMD uses softer "I'll double check" and "I'll get back to you". This is a more informal action-item register. When the partner is closer (regular collaboration), "I'll get back to you" suffices. When you need formal accountability, escalate to "I'll take an action item to follow up on X".

---

## 5. Domain vocabulary with exact usage context

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **Venice** | AMD CPU codename (next-gen, 2026) | "Venice SP7, the production will start next year, July" - SP7 = socket type |
| **Florence** | AMD CPU codename (next-next-gen, 2028) | "Florence is still in planning, different stages of planning, all the Florence products" |
| **Turin** | AMD current-gen CPU (EPYC 9005) | "we already validate that evaluation device under the Turin network" |
| **SP7 / SP8** | Socket types (server platforms) | "Venice SP7... the SP8 next next year, January" - SP8 is newer socket |
| **PR** (Production Readiness) | Production qualification milestone | "Q4 is the right time for the PR" - PR comes before launch |
| **TTM** (Time To Market) | Product market entry | "Florence TTM is not planning for that" |
| **QTR** (Quarterly Transparency Report) | AMD's customer-facing roadmap doc | "the dates you see in QTR are going to be the kind of production date" |
| **CXL VR** (CXL Volatile RAM) | CXL-attached memory module type | "the base of fiber 1, 2, gigabyte CML VR" - 512GB CXL VR module |
| **CMM** (CXL Memory Module) | CXL memory module form factor | "the second generation to five six, your bite CMM EVB" - CMM Evaluation Board |
| **EVB** (Evaluation Board) | Hardware eval platform | "We have run the test to verify our EVB for total 13 categories" |
| **E3.S** | Server form factor (EDSFF) | "the E3.S, we are discussing under the ZXTG as the form factor" |
| **ZXTG** | ZhiuXing Technical Group (CXL form factor working group) | "under the ZXTG as the form factor" |
| **rigid-flux-deer PCB** | PCB technology type (likely "Rigid-Flex-Direct" - transcription noise) | "the third generation, the rigid-flux-deer PCB module" |
| **Lizit Flux** (Likely "Liquid Flux" - transcription noise) | Solder flux technology | "Even if they add some the Lizit Flux technology, but the Lizit Flux technology itself does not require much cost" |
| **Monolithic DRAM** | Single-die DRAM (vs 3DS stacked) | "the 512 GB memory motor using the Monolithic, the DRAM, the media, I mean, not 3DS" |
| **3DS** (3D Stacked) | Stacked DRAM technology | "not 3DS and other the stack technology" - contrast with Monolithic |
| **gen 6 / gen 7** | PCIe generation | "the transition from gen 6 to gen 7" - bandwidth doubles in gen 7 |
| **JEDEC** | Memory standards body | "we debated that a lot in JEDEC" - implies the speaker is a JEDEC participant |
| **TCO** (Total Cost of Ownership) | Cost-per-unit metric | "That's where the TCO comes into play. Does the TCO make sense with DDR5 and gen 7 in the front?" |
| **thermal simulation** | Power/heat modeling | "we can work on the thermal simulations, of course" |
| **software tiering** | SW-based memory tier management | "AMD is driving the software based tiering. So SSSK hynix also has a good software stack for the tiering" |
| **bring up** | Hardware initial bring-up test | "we already validate that evaluation device under the Turin network" / "bring up test list" |
| **bias knob** | Performance tuning parameter | "run with different bias knobs to come up with the RESTP" |
| **RESTP** (likely "recipe" - transcription noise) | Tuning recipe/configuration | "run with different bias knobs to come up with the RESTP" |
| **1R1W / 2R1W** | 1-read-1-write / 2-read-1-write bandwidth test | "the 1 with 1 right performance bandwidth is higher than 2 with 1 right" |
| **wideRDIM** | Wide-register DIMM variant | "we should be able to start sharing them with wideRDIMs" |
| **GoPy** | AMD's CXL diagnostic tool | "we can verify more on the check cell status or anything with AND GoPy" |
| **MemEyeSpec** | CXL memory eye specification/test | "And the third one is MemEyeSpec" - agenda item |
| **KV cache** | LLM key-value cache (GPU use case) | "the key value cache and you know, emergency and expanded in the AI environment" |
| **MI GPU** | AMD Instinct GPU series | "AMD MI GPU and the SSK hynix CMM collaboration evaluation" |
| **tarlick boxes / dotted boxes** | Solid-line / dotted-line roadmap visual | "the WANSP7 and SP8 would be tarlick boxes, Florence boxes would be dotted boxes" |

---

## 6. Expression DB (Expression Database)

55 expressions with id, expression, category, function, speaker_role, difficulty, context, pattern, note. IDs prefixed `m31`.

```yaml
# ── Proposal Architecture (SK side) ──
- id: m31-001
  expression: "The main purpose of this collaboration is that we would like to X"
  category: proposal_framing
  function: purpose_statement
  speaker_role: proposer
  difficulty: 4
  context: "The main purpose of this collaboration is that we would like to make the large and large and larger capacity over this extra interface"
  pattern: "The main purpose of this collaboration is that we would like to X"
  note: 4-step proposal opening - never start with "We want X", start with purpose.

- id: m31-002
  expression: "So but the problem is the, as you know, X require Y"
  category: problem_framing
  function: shared_problem
  speaker_role: proposer
  difficulty: 4
  context: "So but the problem is the, as you know, the large amount of the memory density require the power, a lot of power"
  note: "as you know" - invokes shared knowledge, builds alliance before ask.

- id: m31-003
  expression: "So the limitation is the X. If we have the Y type."
  category: constraint_stating
  function: technical_limit
  speaker_role: proposer
  difficulty: 3
  context: "So the limitation is the 40W. If we have the 2T type"

- id: m31-004
  expression: "So we would like to check the X under considering of Y"
  category: ask_formulation
  function: polite_ask
  speaker_role: proposer
  difficulty: 5
  context: "So we would like to check the summer evaluation under considering of the power"
  note: "under considering of" is Korean-English; native: "considering X" or "taking Y into account". But the structure is gold.

- id: m31-005
  expression: "We are proposing the X evaluation and the collaboration of Y"
  category: proposal_offer
  function: collaboration_proposal
  speaker_role: proposer
  difficulty: 4
  context: "we are the proposing a performance evaluation and the collaboration of a software in software theory"

# ── Reception Architecture (AMD side) ──
- id: m31-006
  expression: "You do bring up a very good point"
  category: validation
  function: positive_reception
  speaker_role: receiver
  difficulty: 3
  context: "You do bring up a very good point. And the two components that are important in this is what is the controller power itself"
  note: "do bring up" - the "do" emphasizes sincerity. Better than "good point".

- id: m31-007
  expression: "Yes, we are absolutely interested and always happy to collaborate on any kind of X"
  category: acceptance_strong
  function: positive_acceptance
  speaker_role: receiver
  difficulty: 4
  context: "Yes, we are absolutely interested and always happy to collaborate on any kind of white papers and collaboration material there"
  note: "absolutely interested + always happy" - double positive. Watch for the "if" that follows.

- id: m31-008
  expression: "I'll be happy to review the proposal and if you want to talk further, I'll be happy to do that"
  category: acceptance_review
  function: review_acceptance
  speaker_role: receiver
  difficulty: 4
  context: "I'll be happy to review the proposal and if you want to talk further in this meeting on that or have a meeting, I'll be happy to do that"

- id: m31-009
  expression: "it is definitely interesting just that it has been very challenging to make it meaningful"
  category: accept_with_caveat
  function: positive_with_reality_check
  speaker_role: receiver
  difficulty: 5
  context: "it is definitely interesting just that it has been very challenging to make it meaningful"
  pattern: "definitely X just that Y"
  note: KEY pattern - positive word + "just that" + reality check. Polite partner caveat.

- id: m31-010
  expression: "if you have X, we can work on Y, but if you have Z, it would be good for us to exchange"
  category: conditional_collaboration
  function: if_then_negotiation
  speaker_role: receiver
  difficulty: 5
  context: "if you have some theoretical tools which can calculate the powers... it would be good for us to exchange that information"

# ── Hedging/Deflection (AMD) ──
- id: m31-011
  expression: "I don't have it on top of my head either"
  category: memory_hedge
  function: knowledge_gap
  speaker_role: receiver
  difficulty: 3
  context: "I don't have it on top of my head either"
  note: NEVER say "I don't know". Use this. Implies info exists, just not currently accessible.

- id: m31-012
  expression: "I'll have to double check the X"
  category: action_soft
  function: follow_up_commit
  speaker_role: receiver
  difficulty: 3
  context: "I'll have to double check the PR timeline"
  note: softer than "action item" - informal collaboration register.

- id: m31-013
  expression: "X is still in planning, different stages of planning"
  category: roadmap_caveat
  function: planning_stage
  speaker_role: receiver
  difficulty: 4
  context: "Florence is still in planning, different stages of planning, all the Florence products"

- id: m31-014
  expression: "the X would be solid boxes, Y would be dotted boxes to say that these are in various stages of planning and subject to change"
  category: visual_metaphor_caveat
  function: roadmap_visual
  speaker_role: receiver
  difficulty: 5
  context: "the WANSP7 and SP8 would be tarlick boxes, Florence boxes would be dotted boxes to say that these are in various stages of planning and subject to change"
  note: Solid vs dotted boxes - visual metaphor makes caveat tangible. USE THIS.

- id: m31-015
  expression: "I still think that X is taking more liberty on Y than it should"
  category: soft_accusation
  function: polite_critique
  speaker_role: receiver
  difficulty: 5
  context: "I still think that the controller is taking more liberty on power than it should"
  note: "taking more liberty than it should" - polite way to say "over budget". Critique of partner's partner.

- id: m31-016
  expression: "There is not much you can do on the X side"
  category: limitation_acceptance
  function: constraint_acknowledge
  speaker_role: receiver
  difficulty: 4
  context: "There is not much you can do on the memory side"

- id: m31-017
  expression: "So there is some potential there"
  category: opportunity_reframe
  function: critique_to_opportunity
  speaker_role: receiver
  difficulty: 4
  context: "I think that the controller power is higher than it should be. So there is some potential there"
  note: Reframes critique as opportunity in one sentence.

- id: m31-018
  expression: "There is absolutely nothing that we will be able to guide you on yet till we X"
  category: hard_limit_with_reason
  function: conditional_no
  speaker_role: receiver
  difficulty: 5
  context: "there is absolutely nothing that we will be able to guide you on yet till we get enough cards and run our performance testing"
  note: "absolutely nothing" + "yet" + "till we X" - hard no softened by future condition.

- id: m31-019
  expression: "What I'm finding concerning is X"
  category: concern_framing
  function: polite_pushback
  speaker_role: questioner
  difficulty: 5
  context: "What I signed concerning is, I mean, we are seeing the power reduce over the speed"
  note: "finding concerning" - gerund makes it active observation, not opinion.

- id: m31-020
  expression: "Is there something else we are missing?"
  category: joint_investigation
  function: concern_to_question
  speaker_role: questioner
  difficulty: 4
  context: "Is there something else we are missing?"
  note: Turns concern into joint investigation, not accusation.

- id: m31-021
  expression: "That's an open question"
  category: open_acknowledgment
  function: no_answer_available
  speaker_role: receiver
  difficulty: 3
  context: "We haven't even talked about what would be behind the behind-sakes. We are considering it to be DDR5 or would it be DDR6 by then? Because if that is the story, it changes completely on the power. That's an open question"

- id: m31-022
  expression: "I cannot share the much item today, but yeah, maybe we will let you know"
  category: explicit_deferral
  function: defer_commit
  speaker_role: proposer
  difficulty: 3
  context: "I cannot share the much item today, but yeah, maybe we will let you know"
  note: Korean-English pattern - direct deferral. Native: "I can't share specifics today, but we'll follow up."

- id: m31-023
  expression: "We need time to figure out more to make it clear"
  category: delay_request
  function: ask_for_time
  speaker_role: proposer
  difficulty: 3
  context: "There are a lot of discussion points. We need time to figure out more to make it clear"

# ── Polite Challenge ──
- id: m31-024
  expression: "Is this information, updated information? Is it right?"
  category: direct_confirm
  function: data_validation
  speaker_role: questioner
  difficulty: 2
  context: "Is this information, updated information? Is it right?"

- id: m31-025
  expression: "Do you see X happening anytime soon for Y?"
  category: future_probe
  function: roadmap_probe
  speaker_role: questioner
  difficulty: 4
  context: "do you see transitions from gen 6 to gen 7 happening anytime soon for the CXL controllers?"

- id: m31-026
  expression: "Does it even make sense to X even if Y? Let me ask it that way."
  category: rhetorical_challenge
  function: refined_question
  speaker_role: questioner
  difficulty: 5
  context: "But it even makes sense to transition to gen 7 even if the CPU is capable. Let me ask it that way"
  note: "Let me ask it that way" - self-correction marker, shows live thinking.

- id: m31-027
  expression: "Are you looking at it from the X that we have on Y or is this the next gen Z?"
  category: scope_clarification
  function: commit_to_scope
  speaker_role: questioner
  difficulty: 4
  context: "Are you looking at it from the CMM that we have on Children or is this the next gen CMM that we are looking at?"

- id: m31-028
  expression: "So before that, do you have any questions for our X?"
  category: inverted_offer
  function: partner_first
  speaker_role: questioner
  difficulty: 4
  context: "So before that, do you have any questions for our bring up test list?"
  note: Korean courtesy pattern - give partner floor first.

- id: m31-029
  expression: "Is there any X option or any Y option to optimize Z?"
  category: technical_probe
  function: optimization_ask
  speaker_role: questioner
  difficulty: 4
  context: "is there any bias option or any test option to optimize the performance? Do you have any recommended option?"

- id: m31-030
  expression: "Could you share the X with Y because we have not used Z?"
  category: tool_request
  function: ask_for_resource
  speaker_role: questioner
  difficulty: 3
  context: "Could you share the test plan or test items with AND Internet because we have not used AND GoPy"

- id: m31-031
  expression: "I'm not good at English, sorry, but so do you mean X?"
  category: self_deprecating_clarify
  function: korean_preface
  speaker_role: questioner
  difficulty: 3
  context: "I'm not good at English, sorry, but so do you mean with next bias, you can optimize the performance?"
  note: Korean pattern. Native alt: "Just to clarify - do you mean X?"

# ── Negotiation/Timeline ──
- id: m31-032
  expression: "plan to get it to production is end of June, early July"
  category: production_target
  function: timeline_commit
  speaker_role: receiver
  difficulty: 4
  context: "plan to get it to production is end of June, early July"
  note: Noun phrase as subject, not "we will". Depersonalizes commitment.

- id: m31-033
  expression: "Q4 is the right time for the X"
  category: milestone_target
  function: target_quarter
  speaker_role: receiver
  difficulty: 3
  context: "I think Q4 is the right time for the PR"

- id: m31-034
  expression: "Launch is couple months later"
  category: launch_distinction
  function: launch_vs_production
  speaker_role: receiver
  difficulty: 3
  context: "Launch is couple months later, so that's where you have"

- id: m31-035
  expression: "the dates you see in QTR are going to be the kind of production date"
  category: source_clarification
  function: doc_reference
  speaker_role: receiver
  difficulty: 4
  context: "the dates you see in QTR are going to be the kind of production date that they are written fuzzy between production as in PR and launch"

- id: m31-036
  expression: "the X is not planning for that"
  category: not_in_roadmap
  function: scope_exclude
  speaker_role: receiver
  difficulty: 3
  context: "The Florence TTM is not planning for that, but I'm just curious to know your perspective"

- id: m31-037
  expression: "I'm just curious to know your perspective"
  category: perspective_ask
  function: opinion_request
  speaker_role: questioner
  difficulty: 4
  context: "The Florence TTM is not planning for that, but I'm just curious to know your perspective"
  note: "just curious" softens what could be a challenge.

- id: m31-038
  expression: "the product and develop and on promotion schedule is based on the X schedule"
  category: dependency_statement
  function: sk_dependency
  speaker_role: proposer
  difficulty: 4
  context: "we are the product and develop and on promotion schedule is based on the CPU schedule"
  note: SK discloses dependency on AMD - important negotiation leverage point.

- id: m31-039
  expression: "If you have any update information, please let us know"
  category: update_request
  function: ask_for_updates
  speaker_role: proposer
  difficulty: 2
  context: "If you have any update information, please let us know"

- id: m31-040
  expression: "That's where the TCO comes into play. Does the TCO make sense with X and Y in the front?"
  category: tco_challenge
  function: economic_challenge
  speaker_role: receiver
  difficulty: 5
  context: "That's where the TCO comes into play. Does the TCO make sense with DDR5 and gen 7 in the front? Or does it have to go to DDR6 for the power reasons beyond gen 6?"
  note: TCO framing - reframes technical question as economic question.

- id: m31-041
  expression: "We are also under the debating... We should bring the X or Y for the Z"
  category: internal_indecision
  function: honest_disclosure
  speaker_role: proposer
  difficulty: 4
  context: "we are also under the debating... We should bring the gen 7 or gen 6 for the third gen"

- id: m31-042
  expression: "There are a lot of discussion points"
  category: complexity_acknowledgment
  function: scope_size
  speaker_role: proposer
  difficulty: 2
  context: "There are a lot of discussion points. We need time to figure out more to make it clear"

# ── Action Items / Follow-up ──
- id: m31-043
  expression: "I will double check on that"
  category: soft_action_item
  function: soft_commit
  speaker_role: receiver
  difficulty: 2
  context: "I will double check on that"

- id: m31-044
  expression: "I'll get back to you with X"
  category: follow_up_commit
  function: response_promise
  speaker_role: receiver
  difficulty: 3
  context: "I'll get back to you with what if they have more questions"

- id: m31-045
  expression: "We'll have to figure out who has that information"
  category: internal_routing
  function: no_direct_answer
  speaker_role: receiver
  difficulty: 4
  context: "We'll have to figure out who has that information and we can see how we can share it"
  note: Honest "I don't know who knows" - more credible than fake commitment.

- id: m31-046
  expression: "we can see how we can share it"
  category: tentative_share
  function: share_intent
  speaker_role: receiver
  difficulty: 3
  context: "we can see how we can share it"

- id: m31-047
  expression: "Please share the data after measurement"
  category: direct_action
  function: action_request
  speaker_role: proposer
  difficulty: 2
  context: "Please share the data after measurement"

- id: m31-048
  expression: "we'll be happy to review and work with you on that"
  category: collaboration_accept
  function: partnership_language
  speaker_role: receiver
  difficulty: 3
  context: "we'll be happy to review and work with you on that"

- id: m31-049
  expression: "I will let you know our projection and the opinion"
  category: soft_future_commit
  function: opinion_promise
  speaker_role: proposer
  difficulty: 3
  context: "I will let you know our projection and the opinion"

# ── Discourse Markers / Misc ──
- id: m31-050
  expression: "Yeah, so SP7, yeah, plan to get it to production is X"
  category: discourse_confirmation
  function: confirm_with_detail
  speaker_role: receiver
  difficulty: 3
  context: "Yeah, so SP7, yeah, plan to get it to production is end of June, early July"

- id: m31-051
  expression: "sorry to interject, but I wanted to say this before we move out of the slide"
  category: interruption_courtesy
  function: polite_interrupt
  speaker_role: receiver
  difficulty: 4
  context: "sorry to interject, but I wanted to say this before we move out of the slide"
  note: "sorry to interject" + "before we move out of the slide" - time-bounded interruption.

- id: m31-052
  expression: "Just to make sure I understand correctly" (used implicitly here)
  category: comprehension_check
  function: polite_preface
  speaker_role: questioner
  difficulty: 5
  context: (echo from Marvell textbook - not verbatim in this transcript, but the pattern matters)
  note: Even though not verbatim here, "Just checking - is X correct?" pattern is used in m31-024.

- id: m31-053
  expression: "Okay, I see. / Yeah, understand."
  category: comprehension_ack
  function: confirm_understanding
  speaker_role: receiver
  difficulty: 2
  context: "Yeah, understand. Yeah, so we already decoded it"

- id: m31-054
  expression: "Yeah, okay, I see. Okay, thank you."
  category: close_ack
  function: polite_close
  speaker_role: proposer
  difficulty: 2
  context: "Yeah, okay, I see. Okay, thank you. If you have any update information, please let us know"

- id: m31-055
  expression: "we can start with X and then continue announcing it. That's that's true."
  category: phased_agreement
  function: incremental_path
  speaker_role: receiver
  difficulty: 4
  context: "We can start with children and then continue announcing it. That's that's true"
  note: "start with X, then continue Y" - phased rollout language.
```

---

## 7. Excerpt map - 5 segments for Mon-Fri shadowing

Audio: `repo/webex-audio/2025-11-05 09 10 07_EN_AMD-extracted.wav` (59MB wav file, ~3,357 transcript words)

| # | Time (est.) | Line range | Content summary | Learning point | Shadowing difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | Opening (line 4-13) | CPU schedule confirmation - Venice/Florence SP7/SP8 dates | "production will start next year, July" - timeline statement pattern | ★★☆ |
| 2 | Roadmap caveat (line 28-32) | AMD "Florence is still in planning... solid boxes vs dotted boxes" | Visual metaphor caveat - "subject to change" | ★★★★ |
| 3 | Thermal proposal (line 56-65) | SK proposal 1: thermal simulation, E3.S 40W budget | 4-step proposal formula: purpose -> problem -> constraint -> ask | ★★★★ |
| 4 | Power debate (line 95-118) | PCIe gen 6 vs gen 7, TCO, DDR5/DDR6 question | "Does it even make sense to X even if Y?" - rhetorical challenge | ★★★★★ |
| 5 | GPU collaboration + engineer Q&A (line 181-240) | GPU+CMM proposal + Yoon Jung's EVB test Q&A + bias knob | Engineer humble preface + "absolutely nothing we will be able to guide you on yet" hard limit | ★★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, Wed: Excerpt 3, Thu: Excerpt 4, Fri: Excerpt 5
- Daily routine (20 min) of shadowing slots - place excerpts in slots
- Excerpts 3, 4 are highest value - proposal formula + rhetorical challenge patterns

---

## 8. Audrey's teaching notes

### Register (style) analysis
This meeting has **three register layers** shifting throughout:

1. **Roadmap/schedule register** (formal, both sides): "production will start", "plan to get it to production", "subject to change" - careful, depersonalized.
2. **Proposal register** (SK, polite-formal): "we would like to", "we are proposing", "we hope to identify" - Korean-polite English, slightly over-formal.
3. **Technical debate register** (AMD, peer-peer): "I still think that", "What I'm finding concerning is", "That's where the TCO comes into play" - direct, expert-to-expert.

Notice AMD shifts register based on topic - formal for roadmap commitments, direct for technical debate. SK stays in formal-proposal register throughout. Audrey's note: when you shift up to expert debate, you can be more direct. When you shift down to roadmap commitment, you must be more careful. Match register to topic.

### Pragmatics (language in use) core
1. **Depersonalized commitment**: AMD says "plan to get it to production is end of June" - not "we will produce in June". The subject is "plan to get it to production", not "we". This protects the speaker from personal guarantee. When you commit on behalf of a company, use noun phrases as subjects, not "we will".

2. **Caveat by metaphor**: "solid boxes vs dotted boxes" - AMD doesn't say "Florence dates may change". They invoke a visual metaphor. The partner immediately pictures the difference. This is far more memorable than "subject to change" alone.

3. **Positive + "just that" + reality**: "it is definitely interesting just that it has been very challenging". The "just that" is the hinge - positive word followed by reality check. This is the polite partner pattern for accepting in spirit while flagging difficulty.

4. **"liberty on power than it should"**: Critique of the controller partner (third-party). "Taking more liberty" is the polite way to say "over budget". When you can't name the problem directly, use "taking more liberty than it should" or "more aggressive than it should be".

5. **"absolutely nothing we will be able to guide you on yet"**: Hard no softened by "yet" and "till we X". The strength of "absolutely nothing" is balanced by the future condition. Use this when you genuinely cannot deliver now.

### Top 5 must-use
1. **"I don't have it on top of my head. I'll have to double check X."** - Never say "I don't know". Use this combo.
2. **"X is still in planning, different stages of planning, subject to change"** - Roadmap caveat formula.
3. **"You do bring up a very good point"** - Validation before pushback.
4. **"definitely X just that Y"** - Accept in spirit, flag difficulty. "Definitely interesting just that it has been challenging."
5. **"There is absolutely nothing we will be able to guide you on yet till we X"** - Hard no with future condition.

### Korean vs English comparison table

| Korean pattern | English (this meeting) | Difference |
|:---|:---|:---|
| "확인해 보겠습니다" | "I'll have to double check X" | Korean is generic; English scopes the double-check to X. |
| "검토해 보겠습니다" | "I cannot share the much item today, but maybe we will let you know" | Korean is shorter; English explicit about what can't be shared now. |
| "기획 중이라 변경될 수 있습니다" | "X is still in planning, different stages of planning, subject to change" | Korean is direct; English adds "different stages" + "subject to change" for emphasis. |
| "제가 영어가 부족해서요" | "I'm not good at English, sorry, but so do you mean X?" | Korean humility - acceptable in Korean, unnecessary in English. Use "Just to clarify - do you mean X?" |
| "컨트롤러가 전력을 너무 많이 잡아먹습니다" | "the controller is taking more liberty on power than it should" | Korean direct blame; English "taking more liberty" - softer, third-party critique. |
| "지금은 안내해 드릴 게 없습니다" | "There is absolutely nothing we will be able to guide you on yet" | Korean stops at "없다"; English adds "yet" to imply future. |
| "궁금합니다" | "I'm just curious to know your perspective" | Korean plain; English "just curious" softens what could be a challenge. |
| "제안합니다" | "We are proposing the X evaluation and the collaboration of Y" | Korean verb-led; English noun-led - "proposing the X" sounds more formal. |

---

## 9. How to use this textbook

1. **Daily 20-min routine**: Section 7 excerpt map, 5 segments Mon-Fri rotation
2. **Expression DB**: Section 6, 55 entries - start with Section 8 Top 5
3. **Friday Audrey correction**: Focus on Section 2 (hedging/deflection) + Section 4 (negotiation) - dump writing
4. **Comparison study**: Section 8 Korean-vs-English table to internalize register shifts
5. **Proposal drill**: Use Section 1 Architecture A (4-step SK proposal formula) to draft your next proposal to AMD or other partner. Skeleton: "The main purpose of this collaboration is that we would like to X. The problem is, as you know, Y requires Z. The limitation is W. So we would like to check V under considering of U."
6. **Reception drill**: Use Section 1 Architecture B (4-step AMD response) to draft your reply when receiving a proposal. Skeleton: "You do bring up a very good point. The X components that are important here is Y. I still think that Z is taking more liberty on W than it should. If you have V, we can work on U."

---

*Textbook 31 - AMD CXL Collaboration (2025-11-05). Type B (Roadmap/Supply alignment) - RECLASSIFIED from initial A. 55 expression DB entries. 5 excerpt segments. Written: 2026-09-01.*
