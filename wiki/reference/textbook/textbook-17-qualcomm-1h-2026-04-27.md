---
textbook_id: 17
meeting: Qualcomm 1H (1H Summary / Roadmap Recap)
date: 2026-04-27
type: B (Roadmap / Supply Alignment)
partner: Qualcomm (LPDDR6 alignment, LPDDR7 framework, San Diego consortium planning)
sk_side: SK Hynix memory roadmap, LPDDR7 framework (profile approach proposal)
duration_words: 2562
audio: repo/webex-audio/2026-04-27 13 51 50_EN_Qualcomm_1H-extracted.wav
transcript: repo/webex-audio/2026-04-27 13 51 50_EN_Qualcomm_1H-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, qualcomm, lpddr6, lpddr7, roadmap, supply-alignment, frequency-negotiation, lpsm, profile-approach, consortium]
---

# Textbook 17 - Qualcomm 1H Summary (2026-04-27)

> **Meeting type**: B (Roadmap / Supply Alignment) - confirmed. Initial type B, no reclassification.
> **Learning value**: frequency negotiation ("26 is 5.3, 27 is 6.4, 28 is 7.2"), requirement framing as "business assignment on reasonable price premium", consortium scheduling, polite doubt expression ("Which I doubt because..."), alignment summarizing ("So I think that's a line. We're aligned that X. And then we're not, you know, on complete agreement for Y").
> **Audrey's view**: This is a roadmap negotiation where Qualcomm pushes spec (frequency, validation timing) and SK Hynix owns the LPSM framework proposal. The gold is in the *alignment language* - "we're aligned that X, not in complete agreement for Y, first two years we're good, need to go figure out the back for the third year". That is the exact template for partial-agreement statements in roadmap meetings. Memorize it.

---

## 1. Speaker Architecture - Qualcomm's 5-Stage Roadmap Pitch

The Qualcomm presenter (senior PM / memory roadmap owner) structures the LPDDR6 alignment pitch in a fixed 5-stage formula. Each stage has a fixed language pattern. This is the skeleton you should learn for any partner-side roadmap ask.

### Stage 1: Appreciation Anchor (Gratitude Preface)

Open with explicit appreciation for prior support before asking for more. This is partner-side courtesy - never start a roadmap ask with the ask.

| Pattern | Original | Function |
|:---|:---|:---|
| `We really appreciate SK HYNIX continued support for X development` | "We really appreciate SK HINIX continued support for QSP2K memory development" | Gratitude anchor - frames ask as continuation, not new demand |
| `Particularly the planned investment in custom X development for Y` | "Particularly the planned investment in custom LPDDR 6 SOCAM development for 2026" | Specific appreciation - ties gratitude to concrete prior commitment |

**Audrey lesson**: In English roadmap meetings, the gratitude preface is not optional decoration. It is the *frame* that makes the subsequent ask feel like a continuation of partnership rather than a new imposition. Korean "지원해 주셔서 감사합니다" maps to this, but the English version must include a *specific* item ("the planned investment in custom LPDDR6 SOCAM development for 2026"), not a generic thanks. Specificity = sincerity in English business register.

### Stage 2: Requirement Framing (Necessity Stating)

Move from gratitude to requirement with "we definitely need X" + "the only way that we can actually work with to make sure that Y".

| Pattern | Original | Function |
|:---|:---|:---|
| `we definitely need business assignment on reasonable price premium over X` | "we definitely need business assignment on reasonable price premium over LPDDR 5X" | Requirement with hedge - "reasonable" softens the demand |
| `the only way that we can actually work with to make sure that we launch X this year` | "the only way that we can actually work with to make sure that we launch LPDDR 6 this year" | Necessity framing - "the only way" raises urgency |
| `That's our request` | "That's our request" | Explicit close - marks section end |

**Audrey lesson**: "reasonable price premium" - the word "reasonable" is doing real work. "We need a price premium" sounds demanding; "we need a *reasonable* price premium" sounds like a fair ask. Always hedge a numerical demand with a softening adjective ("reasonable", "modest", "appropriate"). And "That's our request" as a section-closing formula - explicit, declarative, no apology.

### Stage 3: Approach Proposal (Path Suggestion)

Don't just state the requirement - propose a concrete path. Use "maybe we can X" to keep the proposal collaborative.

| Pattern | Original | Function |
|:---|:---|:---|
| `to come up with a plan, maybe we can choose one mutual customer` | "to come up with a plan, maybe we can choose one mutual customer and have them design or launch it with us" | Collaborative proposal - "maybe we can" not "you should" |
| `we don't need to be in it for making money, but we need to just make sure that technology moves forward` | "we don't need to be in it for making money, but we need to just make sure that technology moves forward" | Non-monetary framing - repositions ask as ecosystem-good |
| `Not necessarily we'll see like millions of designs on it. So it won't be a large investment` | "Not necessarily we'll see like millions of designs on it. So it won't be a large investment" | Scope-bounding - preempts counterpart's investment fear |

**Audrey lesson**: "we don't need to be in it for making money" is a powerful reframe. Qualcomm is literally saying "this is not a money play, this is a tech-forward play". When you ask a partner for something that costs them, frame it as ecosystem benefit, not your gain. And then immediately bound the scope: "won't be a large investment... few hundred thousand at the most". The pattern is: *reframe purpose + bound cost*.

### Stage 4: Spec Push (Frequency Roadmap)

Push for higher spec with market justification, then explicitly acknowledge counterpart's resistance.

| Pattern | Original | Function |
|:---|:---|:---|
| `I think we talked about X alignment to early Y. I think you guys are pushing it back` | "I think we talked about 7.2 gigahertz alignment to early 28. I think you guys are pushing it back" | Direct resistance acknowledgment - names the disagreement |
| `Just to say that that's where we see the market going` | "Just to say that that's where we see the market going" | Market-justification - "the market" as neutral authority |
| `Of course you guys can discuss that internally and see where you guys stand with it` | "Of course you guys can discuss that internally and see where you guys stand with it" | Defer to internal - preserves relationship over the point |
| `So just a, just a, you know, same message. So you guys need to really think about that` | "So just a, just a, you know, same message. So you guys need to really think about that" | Message emphasis - "you need to think about that" without dictating |

**Audrey lesson**: "I think you guys are pushing it back" is direct but not aggressive. It names the resistance out loud, which is honest. Then immediately: "that's where we see the market going" - appealing to a third party (market) rather than personal preference. Then: "you guys can discuss that internally" - returning the decision to them. This three-step pattern (name resistance > cite market > defer internally) is the polite-push template.

### Stage 5: Cross-BU Amplification (Sentiment Echo)

Close the spec push by showing the same ask echoes in other BUs (automotive, server), making it harder to dismiss as a single-team wish.

| Pattern | Original | Function |
|:---|:---|:---|
| `We shared the same sentiment on the mobile side. We're thinking similar stuff on the automotive as well` | "We shared the same sentiment on the mobile side. We're thinking similar stuff on the automotive as well" | BU-echo - "same sentiment" amplifies the ask |
| `So just a, just a, you know, same message` | "So just a, just a, you know, same message" | Message consolidation formula |
| `even if we settle on mobile, I think that the case still remains open for other BU's` | "even if we settle on mobile, I think that the case still remains open for other BU's" | Keeps the door open - "the case still remains open" |

**Audrey lesson**: When your ask is being resisted in one BU, don't drop it - echo it from other BUs. "Same sentiment on mobile, similar on automotive" makes the ask look like a market-wide need, not a single team's wish. The phrase "the case still remains open" is critical - it means "I'm not forcing it now, but the question is not closed". This is the polite-persistence formula.

---

## 2. Hedging & Deflection Strategies

This meeting's real learning value. Both sides do heavy hedging because neither wants to commit to a 3-year frequency roadmap they may not deliver.

### Strategy 1: Graceful Misunderstanding Ownership

When the counterpart calls out a contradiction in your signals, own the misunderstanding rather than defending.

| Situation | Original | Translation |
|:---|:---|:---|
| SK points out Qualcomm's CS-timeline signals suggested they wanted 6.4 this year | "Maybe that was my misunderstanding, but that's how it came out" | "제가 오해했을 수도 있습니다만, 그렇게 들었습니다" |

**Pattern**: `Maybe that was my misunderstanding, but that's how it came out.`

**Audrey lesson**: This is gold. When someone says "your actions suggested X, but you just said Y", the weak response is "no, I never said that". The strong response is "Maybe that was my misunderstanding, but that's how it came out". Two moves: (a) "Maybe" hedges your concession, (b) "that's how it came out" returns partial responsibility to the counterpart ("that's how it came across from your side"). Neither fully admits fault nor blames. This is the English middle path.

### Strategy 2: Doubt With Softening

Express doubt about counterpart's claim without contradicting directly.

| Situation | Original | Translation |
|:---|:---|:---|
| SK says market may accept 6.4 for two years | "Which I doubt because there are other businesses that are, you know, interested in also an LB6. Auto is one of them, of course, and then server side is another one which needs higher speeds" | "의심스럽습니다만, 다른 BU도 LB6에 관심 있으니까요. 자동차, 서버 쪽이 더 높은 스피드를 원합니다" |

**Pattern**: `Which I doubt because there are other X that are interested in Y. A is one of them, and B is another which needs Z.`

**Audrey lesson**: "Which I doubt" is a beautiful soft negation. Not "I disagree", not "you're wrong" - "I doubt". Then immediately back it with concrete evidence (auto, server BUs). The structure: *doubt statement > because > concrete counterexamples*. Korean "그건 아닐 것 같습니다만" maps roughly, but the English version must list the counterexamples explicitly to land.

### Strategy 3: First-Priority Redirection

When pushed on a spec point you can't commit to, redirect to a smaller first priority you can commit to.

| Situation | Original | Translation |
|:---|:---|:---|
| Qualcomm pushes 6.4 timing | "the current market conditions, they're not even asking for 12.8 or 6.4 at this time. So it's not really our priority. Our first priority is whether LB6 getting validated first and whether that's 5.3 or 6.4 is it's not secondary" | "지금 시장에선 12.8이나 6.4를 요구하지 않습니다. 우선순위가 아닙니다. 첫 번째 우선순위는 LB6 검증 자체이고, 5.3이냐 6.4냐는 부차적입니다" |

**Pattern**: `Current market conditions are not asking for X. So it's not really our priority. Our first priority is Y. Whether that's A or B is secondary.`

**Audrey lesson**: This is the roadmap deflection formula. Don't refuse the spec - reframe the priority. "It's not really our priority" + "Our first priority is Y" + "X vs A is secondary". Three moves: market-justification > positive priority > downgrade the disputed point. Note "secondary" here doesn't mean "unimportant" - it means "comes after the first priority". This is the SK-side equivalent of Qualcomm's "we don't need to be in it for making money" reframe.

### Strategy 4: Direct Deflection (Two-Word Refusal)

When a direct question lands, sometimes the strongest move is the shortest answer.

| Situation | Original | Translation |
|:---|:---|:---|
| Qualcomm asks about SK Hynix's LPDDR7 study/solution | "What that." / "Not at this time." / "Not this time." | "그건요." / "지금은요, 아닙니다." / "이번엔 아닙니다." |

**Pattern**: `Not at this time.`

**Audrey lesson**: "Not at this time" is the polite-no. It's not "no", it's not "we don't know", it's "not now". The implication is "later maybe" without committing. Use it when you don't want to share internal work yet. Two words, hard to push further. When paired with the next pattern ("we can look together"), it converts a refusal into a partnership invitation.

### Strategy 5: Partnership Reframe (Refusal-to-Invite)

After a direct refusal, immediately offer a "look together" framing to convert the no into a collaboration door.

| Situation | Original | Translation |
|:---|:---|:---|
| Qualcomm asks about SK's LPDDR7 work; SK says "not at this time" | "Okay, we can we can look together" | "네, 같이 살펴볼 수는 있겠지요" |

**Pattern**: `Not at this time. ... We can look together.`

**Audrey lesson**: The pairing is the technique. Refuse ("not at this time") > invite ("we can look together"). The refusal protects internal IP; the invite preserves the relationship. Korean "이번엔 말씀드리기 어렵지만 같이 살펴보죠" maps closely. The English version must come *immediately* - don't let the silence after "not at this time" sit for more than one beat.

### Strategy 6: Partial-Agreement Summary

When you've agreed on some points and disagreed on others, summarize explicitly which is which.

| Situation | Original | Translation |
|:---|:---|:---|
| Both sides agreed on 5.3 and 6.4 but not 7.2 | "So I think that's a line. We're aligned that 26 is 5.3, 27 is 6.4. And then we're not, you know, on complete agreement for 7.2 the year after. I think that's where the differences are. So first two years we're good. We need to go figure out the back for the third year" | "정리하면, 26년 5.3, 27년 6.4는 맞춰졌고요. 그 다음 해 7.2는 완전한 합의가 아닙니다. 거기가 차이입니다. 2년은 좋고, 3년 차는 다시 논의해야 합니다" |

**Pattern**: `So I think that's a line. We're aligned that X. And then we're not, you know, on complete agreement for Y. I think that's where the differences are. So first two years we're good. We need to go figure out the back for the third year.`

**Audrey lesson**: This is the single most valuable pattern in this textbook for roadmap meetings. "So I think that's a line" - "그게 선이네요" meaning "that's the boundary line". Then explicitly: aligned on X, not in complete agreement on Y, that's where the differences are. Then: "first two years we're good" - confirm what's settled - "need to go figure out the back" - park the disagreement for later. This converts a 3-year argument into a 2-year agreement + a deferred item. Use this every time you have partial roadmap agreement.

### Strategy 7: Value-Based Reassurance

When proposing a framework that might constrain the partner, reassure them it preserves their product strategy flexibility.

| Situation | Original | Translation |
|:---|:---|:---|
| SK proposes LPSM profile approach; Qualcomm exec welcomes | "we are not giving that the more flexibility and value to you. And that doesn't necessarily means that you develop the two separate design. Based on your product strategies and value proposition, you have continued to combo and the same design or separate design for density" | "여러분에게 유연성과 가치를 더 드리는 겁니다. 굳이 두 개를 따로 설계하라는 건 아닙니다. 제품 전략에 따라 통합 설계도 가능하고 밀도에 따라 분리 설계도 가능합니다" |

**Pattern**: `We are not giving less flexibility to you. That doesn't necessarily mean you develop X. Based on your strategies, you can A or B.`

**Audrey lesson**: When you propose a framework, anticipate the partner's fear ("does this force me to do extra work?") and pre-empt it. "Doesn't necessarily mean X" + "you can A or B" is the reassurance template. "Based on your product strategies" defers the choice to them, which is respectful.

---

## 3. Polite Challenge Patterns (Questioner's Side)

### Pattern Type 1: Math-Based Challenge

Use math to expose an inconsistency in the counterpart's roadmap without saying "you're wrong".

| Pattern | Original | Function |
|:---|:---|:---|
| `I think technically speaking, X. So yours is Y. Or is that because you're trying to Z?` | "I think technically speaking, 26, LP6 speed 10.7 next year 12.8 a year after is 12.8. I think it's three years. So yours is two years you're planning that way. Or is that because you're trying to push beyond 10.7 this year, 26 right. That was your ask." | Math-expose > question the cause |

**Audrey lesson**: Don't say "your plan is wrong". Lay out the math ("26, then 27, then 28 - that's three years; yours covers two") and let the gap speak for itself. Then offer a possible explanation as a question ("or is that because...?"). This converts a challenge into a curiosity question. The phrase "That was your ask" at the end - acknowledging the counterpart's stated position - shows you listened, which makes the challenge harder to dismiss.

### Pattern Type 2: Mixed-Signal Callout

When the counterpart's words and timelines don't match, name the mismatch directly but attribute it to your interpretation.

| Pattern | Original | Function |
|:---|:---|:---|
| `Not the message that I got from looking at the timelines. So you were very set on X, which tells me that yes, you really want to push X this year. If you were a little more relaxed on sitting here, you know` | "Not the message that I got from looking at the timelines. So you were very set on certain timelines for trying to validate 6.4, which tells me that yes, you really want to push 6.4 this year. If you were a little more relaxed on sitting here, you know, but we should at some point help you validate 6.4 after the CS" | Mixed-signal callout - "what I got from you vs what you just said" |

**Audrey lesson**: "Not the message that I got from looking at the timelines" - this is calling the counterpart inconsistent without saying "you're contradicting yourself". Two moves: (a) attribute the message to *your* interpretation ("the message that I got"), (b) ground it in their data ("from looking at the timelines"). Then describe the inference: "which tells me that yes, you really want to push 6.4". This is confrontational made polite through the "I-message" framing.

### Pattern Type 3: Direct Probe (Timing)

When you need a specific timeline answer, ask short and direct without hedging.

| Pattern | Original | Function |
|:---|:---|:---|
| `Where are you planning on kicking off the console [consortium]?` | "Where are you planning on kicking off the console?" | Direct timing probe - "where/when are you planning to X" |

**Audrey lesson**: In a meeting full of hedges, the direct question is powerful. "Where are you planning on kicking off the consortium?" is short, plain, and impossible to dodge. Note "kicking off" - conversational, not bureaucratic ("initiating", "launching"). Use this register for direct probes: short, simple verb ("kicking off", "starting", "doing"), no softeners. The contrast with the surrounding hedges makes it land.

### Pattern Type 4: Whole-Market Reframing

When the counterpart is negotiating one segment (mobile), reframe to the whole market to break the impasse.

| Pattern | Original | Function |
|:---|:---|:---|
| `I just wanted to make sure that we understand the whole market segment, not just mobile` | "I just wanted to make sure that we understand the whole market segment, not just mobile" | Scope expansion - "not just X, the whole Y" |

**Audrey lesson**: When you're stuck on a per-segment disagreement, expand the scope. "I just wanted to make sure that we understand the whole market segment, not just mobile" - this isn't a question, it's a reframe. It says "your mobile-only position is too narrow". The phrase "I just wanted to make sure" softens what would otherwise be a direct criticism. Pattern: *softener > reframe > scope-broadener*.

### Pattern Type 5: Validation-First Probe

When pushing for spec commitment, first ask whether any validation is planned, defer the speed point.

| Pattern | Original | Function |
|:---|:---|:---|
| `We wanted to check first if you have plans for X validation by the end of this year, right?` | "We wanted to check first if you have plans for LB6 validation by the end of this year, right?" | Soft probe - "we wanted to check first" + tag question "right?" |

**Audrey lesson**: "We wanted to check first" is a soft preface. It signals a question without committing to a demand. Tag question "right?" at the end invites confirmation rather than a long answer. Use this for binary-check probes: "yes or no, do you have a plan?" Then the speed can be discussed after the validation baseline is established.

---

## 4. Negotiation & Action-Item Language

This is the key section for type B (roadmap) meetings. The negotiation language in this meeting covers: requirement stating, scope bounding, timeline deferral, consortium scheduling, and framework welcoming.

### Negotiation Patterns

| Pattern | Speaker | Original | Function |
|:---|:-:|:---|:---|
| Requirement stating | Qualcomm | "we definitely need business assignment on reasonable price premium over LPDDR 5X" | Hard requirement + "reasonable" softener |
| Necessity framing | Qualcomm | "the only way that we can actually work with to make sure that we launch LPDDR 6 this year" | "The only way" - urgency |
| Non-monetary reframe | Qualcomm | "we don't need to be in it for making money, but we need to just make sure that technology moves forward" | Ecosystem-good framing |
| Scope bounding | Qualcomm | "Maybe it will be few hundred thousand, you know, at the most" | Pre-empt investment fear |
| Path suggestion | Qualcomm | "to come up with a plan, maybe we can choose one mutual customer and have them design or launch it with us" | Collaborative proposal |
| Internal deferral | Qualcomm | "Of course you guys can discuss that internally and see where you guys stand with it" | Defer decision to counterpart |
| Spec resistance acknowledgment | Qualcomm | "I think you guys are pushing it back" | Direct naming of resistance |
| Partial agreement summary | Qualcomm | "We're aligned that 26 is 5.3, 27 is 6.4. And then we're not, you know, on complete agreement for 7.2 the year after" | State aligned vs disagreed |
| Deferred resolution | Qualcomm | "let's settle on that maybe in a few months, figure out where you guys are going" | Park the disagreement |
| Direct refusal | SK Hynix | "Not at this time" | Polite-no |
| Partnership invite after refusal | SK Hynix | "we can we can look together" | Convert no to collaboration door |
| Framework welcoming | Qualcomm | "I fully understand the intention of such a framework. I welcome." | Executive endorsement formula |
| Consortium scheduling | SK Hynix | "Our plan is at least two or three months in the legal work. And so that is our show point to set up and probably good time is our, you know, August" | Soft timeline proposal with reasoning |
| Travel efficiency proposal | SK Hynix | "Combine your travel is more easier than and make the one trip" | Logistics-justified timing |
| Value reassurance | Qualcomm | "we are not giving that the more flexibility and value to you" | Pre-empt partner fear |

**Audrey lessons**:
- "the only way that we can actually work with to make sure that we launch X this year" - "the only way" is a strong urgency marker. Use sparingly; overuse kills it.
- "few hundred thousand, at the most" - "at the most" bounds the ask from above. Always give an upper bound when asking for investment; the partner's fear is the unknown ceiling, not the number itself.
- "Combine your travel is more easier" - the grammar is non-native ("more easier"), but the *pragmatic move* is gold: justify the meeting date by partner's convenience. This is exactly the right kind of move even if the English is imperfect. Steve, do not be afraid of imperfect English when the pragmatic move is right.
- "I fully understand the intention of such a framework. I welcome." - this is the executive endorsement formula. Two moves: (a) "I fully understand" - confirm comprehension, (b) "I welcome" - explicit acceptance. Note: "I welcome" alone, no object. This is senior-register English; you don't need to say "I welcome it" - the bare "I welcome" is more powerful.

### Action-Item Language

| Pattern | Speaker | Original | Function |
|:---|:-:|:---|:---|
| Plan to follow up | Qualcomm | "let's settle on that maybe in a few months, figure out where you guys are going and maybe we'll get some feedback from the market" | Deferred decision + market feedback source |
| Meeting commitment | SK Hynix | "you can meet in San Diego" + "August 20 and 21" | Concrete date + place |
| Internal-study note | Qualcomm | "Qualcomm has a more confident than it is achievable we can do a ball based on certain technical direction" | Internal-direction confidence claim (no external commitment) |
| Timing-anchored action | SK Hynix | "Our plan is at least two or three months in the legal work" | Soft timeline with work-stream reasoning |
| Travel-coupled action | SK Hynix | "Combine your travel is more easier than and make the one trip" | Logistics-justified scheduling |

**Audrey lesson**: This meeting has few formal "action items" (no "I will send you X by Y") - that's because roadmap alignment meetings produce *deferred decisions*, not action items. The action-item equivalent here is "let's settle on that maybe in a few months" - a deferred decision with a vague time. In roadmap meetings, that is the norm. Don't force a hard action item when the decision isn't ripe; use "let's settle on that in a few months" instead.

---

## 5. Domain Vocabulary with Exact Usage Context

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **QSP2K** | Qualcomm Snapdragon Platform 2K (memory program) | "We really appreciate SK HINIX continued support for QSP2K memory development" - appreciation anchor with program name |
| **SOCAM** | System-on-Chip Advanced Memory (Qualcomm custom memory designation) | "the planned investment in custom LPDDR 6 SOCAM development for 2026" - custom-design investment ask |
| **business assignment** | Allocation of a specific business/product to a vendor | "we definitely need business assignment on reasonable price premium over LPDDR 5X" - vendor-lock ask |
| **price premium** | Markup over previous-gen pricing | "reasonable price premium over LPDDR 5X" - pricing ask with softener |
| **attach** | Design-in / win at a customer account | "we need to see, you know, some some attach on LPDDR 6" - design-win count |
| **mutual customer** | Customer both parties work with | "we can choose one mutual customer and have them design or launch it with us" - joint design-in proposal |
| **CS** | Customer Sample (chipset sampling milestone) | "the base CS is Q3 28" - sampling milestone |
| **UFS 4 to 1 / UFS 5** | Universal Flash Storage generations | "UFS 4 to 1 and the package we have discussed previously" + "UFS 5, which is under consideration" - storage roadmap |
| **COB** | Chip-on-Board packaging | "please re-look, consider that package moves to COB" - packaging request |
| **46 ball / 418 / 563 ball** | Package ball counts (pinout specs) | "Small four factor 4 channel LPDDR6, 518 and LPDDR5 at 563 ball" - package spec comparison |
| **auto gen entry** | Entry-level automotive chipset | "we have added a entry level chip, which would utilize LP6 at 6.4 gigahertz" - automotive roadmap addition |
| **BU** | Business Unit | "the case still remains open for other BU's" - cross-BU argument |
| **LPSM** | LPDDR Server/Standard Memory (framework name) | "we discussed this kind of LPSM framework" - SK-side framework proposal |
| **profile approach** | Single spec with sub-profiles for mobile/server | "the profile approach in the LPSM" - framework structure proposal |
| **consortium** | Standards body kickoff | "Where are you planning on kicking off the console [consortium]?" - standards-body start probe |
| **one dean and a meter** | (Transcription of "one-die and a-meter" - likely DRAM die stacking + metering) | "the only chance that we'll be able to reach that is with our one dean and a meter, but it's doesn't come until after our third generation" - SK-internal technical path |
| **third generation / fourth generation** | Die generation in roadmap | "it doesn't come until after our third generation" - die-generation reference |
| **32 gigabit / 16 gigabit LB6** | LPDDR6 die densities | "whether we'll utilize our second generation of these six, which is 32 gigabit LB6 or this year's LB6 16 gigabit LB6" - die density choice |
| **validated** | Spec confirmed working | "Our first priority is whether LB6 getting validated first" - validation milestone |
| **Vienna ready / aware ready** | (Likely transcription of "preliminary-ready" / "early-aware" - readiness stages) | "LPDR6 beginning is a Vienna ready and scoping that kind of data center" - readiness stage designation |
| **combo** | Combined design (mobile + server in one) | "you have continued to combo and the same design or separate design for density" - design strategy choice |
| **legal work** | Consortium legal/setup preparation | "at least two or three months in the legal work" - pre-consortium legal preparation |
| **journey meeting** | (Transcription of "Journey [internal codename]" meeting or similar) | "August is our journey meeting in San Diego" - internal-meeting name |

---

## 6. Expression Database (50 entries)

```yaml
# ── Appreciation Anchor (Opening) ──
- id: m17-001
  expression: "We really appreciate SK HYNIX continued support for X development"
  category: appreciation_anchor
  function: gratitude_preface
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "We really appreciate SK HINIX continued support for QSP2K memory development"
  pattern: "We really appreciate X continued support for Y development"
  note: Roadmap ask opening formula. Specific program name required.

- id: m17-002
  expression: "Particularly the planned investment in custom X development for Y"
  category: appreciation_specific
  function: specific_gratitude
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "Particularly the planned investment in custom LPDDR 6 SOCAM development for 2026"
  note: Specific-appreciation move - concrete item + year. Specificity = sincerity.

# ── Requirement Framing ──
- id: m17-003
  expression: "we definitely need business assignment on reasonable price premium over X"
  category: requirement_stating
  function: hard_ask_with_softener
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "we definitely need business assignment on reasonable price premium over LPDDR 5X"
  note: "definitely need" + "reasonable" - hard ask with softener. "business assignment" = vendor lock.

- id: m17-004
  expression: "the only way that we can actually work with to make sure that we launch X this year"
  category: necessity_framing
  function: urgency_raise
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "the only way that we can actually work with to make sure that we launch LPDDR 6 this year"
  note: "the only way" - strong urgency marker. Use sparingly.

- id: m17-005
  expression: "That's our request"
  category: section_close
  function: explicit_ask_close
  speaker_role: presenter_qualcomm
  difficulty: 2
  context: "I think we should seriously look into that. That's our request."
  note: Section-closing formula - declarative, no apology.

# ── Approach Proposal ──
- id: m17-006
  expression: "to come up with a plan, maybe we can choose one mutual customer"
  category: collaborative_proposal
  function: path_suggestion
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "to come up with a plan, maybe we can choose one mutual customer and have them design or launch it with us"
  note: "maybe we can" - collaborative proposal. Not "you should".

- id: m17-007
  expression: "we don't need to be in it for making money, but we need to just make sure that technology moves forward"
  category: non_monetary_reframe
  function: ecosystem_good_framing
  speaker_role: presenter_qualcomm
  difficulty: 5
  context: "we don't need to be in it for making money, but we need to just make sure that technology moves forward"
  note: Reframe demand as ecosystem benefit. Powerful move.

- id: m17-008
  expression: "Not necessarily we'll see like millions of designs on it. So it won't be a large investment"
  category: scope_bounding
  function: investment_fear_preempt
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "Not necessarily we'll see like millions of designs on it. So it won't be a large investment"
  note: Pre-empt counterpart's investment fear. Bound scope.

- id: m17-009
  expression: "Maybe it will be few hundred thousand, you know, at the most"
  category: upper_bound
  function: ceiling_set
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "Maybe it will be few hundred thousand, you know, at the most"
  note: "at the most" - upper bound. Always give a ceiling for investment asks.

# ── Spec Push / Resistance Acknowledgment ──
- id: m17-010
  expression: "I think we talked about X alignment to early Y. I think you guys are pushing it back"
  category: resistance_acknowledgment
  function: name_disagreement
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "I think we talked about 7.2 gigahertz alignment to early 28. I think you guys are pushing it back"
  note: Direct resistance acknowledgment - names the disagreement out loud.

- id: m17-011
  expression: "Just to say that that's where we see the market going"
  category: market_justification
  function: third_party_authority
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "Just to say that that's where we see the market going"
  note: "the market" as neutral authority. Not "we want", "the market wants".

- id: m17-012
  expression: "Of course you guys can discuss that internally and see where you guys stand with it"
  category: internal_deferral
  function: return_decision
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "Of course you guys can discuss that internally and see where you guys stand with it"
  note: Defer to internal discussion. Preserves relationship over the point.

- id: m17-013
  expression: "So please re-look, consider that package moves to COB"
  category: direct_request
  function: explicit_ask
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "So please re-look, consider that package moves to COB"
  note: "please re-look, consider" - polite but direct. Two verbs (re-look + consider) soften the imperative.

- id: m17-014
  expression: "We shared the same sentiment on the mobile side. We're thinking similar stuff on the automotive as well"
  category: cross_bu_echo
  function: ask_amplification
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "We shared the same sentiment on the mobile side. We're thinking similar stuff on the automotive as well"
  note: BU-echo amplification. Makes single-team ask look market-wide.

- id: m17-015
  expression: "Any questions, concerns?"
  category: question_invitation
  function: section_pause
  speaker_role: presenter_qualcomm
  difficulty: 2
  context: "Any questions, concerns?"
  note: Short question invitation. Note plural "concerns" - invites pushback, not just questions.

# ── Hedging & Deflection ──
- id: m17-016
  expression: "Maybe that was my misunderstanding, but that's how it came out"
  category: graceful_ownership
  function: misunderstanding_own
  speaker_role: questioner_qualcomm
  difficulty: 5
  context: "Maybe that was my misunderstanding, but that's how it came out"
  note: Gold. "Maybe" hedges concession; "that's how it came out" returns partial responsibility.

- id: m17-017
  expression: "If you were a little more relaxed on sitting here, you know"
  category: soft_pushback
  function: condition_softening
  speaker_role: questioner_qualcomm
  difficulty: 4
  context: "If you were a little more relaxed on sitting here, you know, but we should at some point help you validate 6.4"
  note: "If you were a little more relaxed" - soft condition for pushback.

- id: m17-018
  expression: "What I get from you is that yes, you are convinced that you should be doing X at Y time frame"
  category: mixed_signal_callout
  function: inconsistency_name
  speaker_role: questioner_qualcomm
  difficulty: 5
  context: "What I get from you is that yes, you are convinced that you should be doing 6.4 at CS time frame"
  note: I-message callout. "What I get from you" attributes interpretation to yourself.

- id: m17-019
  expression: "the current market conditions, they're not even asking for X at this time. So it's not really our priority"
  category: priority_redirection
  function: first_priority_reframe
  speaker_role: questioner_sk
  difficulty: 4
  context: "the current market conditions, they're not even asking for 12.8 or 6.4 at this time. So it's not really our priority"
  note: Roadmap deflection formula. Market-justification > "not our priority".

- id: m17-020
  expression: "Our first priority is whether X getting validated first and whether that's A or B is it's not secondary"
  category: priority_downgrade
  function: disputed_point_downgrade
  speaker_role: questioner_sk
  difficulty: 4
  context: "Our first priority is whether LB6 getting validated first and whether that's 5.3 or 6.4 is it's not secondary"
  note: "secondary" doesn't mean unimportant - means "after the first priority". Refuses the spec point without refusing validation.

- id: m17-021
  expression: "Not at this time"
  category: direct_deflection
  function: polite_no
  speaker_role: questioner_sk
  difficulty: 2
  context: "What that." "Not at this time."
  note: Two-word polite-no. Not "no", not "we don't know", "not now". Hard to push further.

- id: m17-022
  expression: "we can we can look together"
  category: partnership_invite
  function: refusal_to_collaboration
  speaker_role: questioner_sk
  difficulty: 3
  context: "Okay, we can we can look together"
  note: Pair with "Not at this time" - refusal > invite. Convert no to door.

- id: m17-023
  expression: "Which I doubt because there are other businesses that are, you know, interested in also an LB6"
  category: soft_doubt
  function: polite_negation
  speaker_role: questioner_qualcomm
  difficulty: 5
  context: "Which I doubt because there are other businesses that are, you know, interested in also an LB6. Auto is one of them, of course"
  note: "Which I doubt" - soft negation. Then back with concrete counterexamples.

- id: m17-024
  expression: "even if we settle on mobile, I think that the case still remains open for other BU's"
  category: open_door
  function: persistence_preserve
  speaker_role: questioner_qualcomm
  difficulty: 4
  context: "even if we settle on mobile, I think that the case still remains open for other BU's"
  note: "the case still remains open" - "not forcing now, but not closed". Polite persistence.

- id: m17-025
  expression: "we don't want to develop the two separate design"
  category: value_reassurance
  function: partner_fear_preempt
  speaker_role: questioner_qualcomm
  difficulty: 4
  context: "we are not giving that the more flexibility and value to you. And that doesn't necessarily means that you develop the two separate design"
  note: Pre-empt partner's "this means extra work for me" fear.

- id: m17-026
  expression: "Based on your product strategies and value proposition, you have continued to combo and the same design or separate design for density"
  category: flexibility_preservation
  function: choice_defer
  speaker_role: questioner_qualcomm
  difficulty: 5
  context: "Based on your product strategies and value proposition, you have continued to combo and the same design or separate design for density"
  note: "Based on your strategies, you can A or B" - defer choice to partner. Respectful.

# ── Polite Challenge ──
- id: m17-027
  expression: "I think technically speaking, X. So yours is Y"
  category: math_based_challenge
  function: inconsistency_expose
  speaker_role: questioner_sk
  difficulty: 5
  context: "I think technically speaking, 26, LP6 speed 10.7 next year 12.8 a year after is 12.8. I think it's three years. So yours is two years you're planning that way"
  note: Math-expose > question the cause. Let the gap speak.

- id: m17-028
  expression: "Or is that because you're trying to push beyond X this year, right. That was your ask"
  category: cause_question
  function: attribution_offer
  speaker_role: questioner_sk
  difficulty: 4
  context: "Or is that because you're trying to push beyond 10.7 this year, 26 right. That was your ask"
  note: "That was your ask" - acknowledge counterpart's position. Show you listened.

- id: m17-029
  expression: "Not the message that I got from looking at the timelines"
  category: mixed_signal_callout
  function: inconsistency_describe
  speaker_role: questioner_qualcomm
  difficulty: 5
  context: "Not the message that I got from looking at the timelines. So you were very set on certain timelines"
  note: "the message that I got" - I-message framing. Ground in their data ("timelines").

- id: m17-030
  expression: "We wanted to check first if you have plans for X validation by the end of this year, right?"
  category: validation_probe
  function: binary_check
  speaker_role: questioner_sk
  difficulty: 3
  context: "We wanted to check first if you have plans for LB6 validation by the end of this year, right?"
  note: "we wanted to check first" + tag "right?" - soft binary probe.

- id: m17-031
  expression: "Where are you planning on kicking off the console [consortium]?"
  category: direct_probe
  function: timing_question
  speaker_role: questioner_qualcomm
  difficulty: 2
  context: "Where are you planning on kicking off the console?"
  note: Direct timing probe. Short, plain. Contrast with surrounding hedges makes it land.

- id: m17-032
  expression: "I just wanted to make sure that we understand the whole market segment, not just mobile"
  category: scope_expansion
  function: segment_reframe
  speaker_role: questioner_qualcomm
  difficulty: 4
  context: "I just wanted to make sure that we understand the whole market segment, not just mobile"
  note: "I just wanted to make sure" softens what would be a direct criticism. "not just X, the whole Y".

- id: m17-033
  expression: "I fully understand the intention of such a framework. I welcome"
  category: executive_endorsement
  function: framework_accept
  speaker_role: presenter_qualcomm
  difficulty: 5
  context: "I fully understand the intention of such a framework. I welcome."
  note: Senior-register. Bare "I welcome" - no object needed. Two moves: confirm comprehension > explicit accept.

# ── Negotiation & Alignment Summary ──
- id: m17-034
  expression: "So I think that's a line. We're aligned that X. And then we're not, you know, on complete agreement for Y"
  category: partial_agreement_summary
  function: alignment_state
  speaker_role: presenter_qualcomm
  difficulty: 5
  context: "So I think that's a line. We're aligned that 26 is 5.3, 27 is 6.4. And then we're not, you know, on complete agreement for 7.2 the year after"
  note: THE most valuable pattern in this textbook. Convert 3-year argument into 2-year agreement + deferred item.

- id: m17-035
  expression: "So first two years we're good. We need to go figure out the back for the third year"
  category: deferred_resolution
  function: park_disagreement
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "So first two years we're good. We need to go figure out the back for the third year"
  note: "first N we're good" + "go figure out the back for M" - park the disagreement.

- id: m17-036
  expression: "let's settle on that maybe in a few months, figure out where you guys are going"
  category: deferred_decision
  function: roadmap_park
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "let's settle on that maybe in a few months, figure out where you guys are going"
  note: Roadmap action-item equivalent. Deferred decision with vague time.

- id: m17-037
  expression: "Our plan is at least two or three months in the legal work"
  category: soft_timeline
  function: timeline_with_reasoning
  speaker_role: presenter_sk
  difficulty: 3
  context: "Our plan is at least two or three months in the legal work. And so that is our show point to set up"
  note: "at least two or three months" + work-stream reason. Soft timeline proposal.

- id: m17-038
  expression: "probably good time is our, you know, August and August is our journey meeting in San Diego"
  category: timing_proposal
  function: anchor_to_event
  speaker_role: presenter_sk
  difficulty: 4
  context: "probably good time is our, you know, August and August is our journey meeting in San Diego"
  note: Anchor proposal to existing event. "probably good time" - soft.

- id: m17-039
  expression: "Combine your travel is more easier than and make the one trip"
  category: travel_efficiency
  function: logistics_justification
  speaker_role: presenter_sk
  difficulty: 3
  context: "Combine your travel is more easier than and make the one trip"
  note: Non-native grammar ("more easier"), but pragmatic move is gold - justify date by partner's convenience.

- id: m17-040
  expression: "you can meet in San Diego"
  category: meeting_commitment
  function: concrete_date_place
  speaker_role: presenter_sk
  difficulty: 2
  context: "August 20. 20 and 21. You can meet in San Diego."
  note: Concrete date + place. Note brevity - "you can meet in X". Not "would you like to meet".

- id: m17-041
  expression: "Qualcomm has a more confident than it is achievable we can do a ball based on certain technical direction"
  category: internal_confidence_claim
  function: direction_assert
  speaker_role: presenter_qualcomm
  difficulty: 5
  context: "Qualcomm has a more confident than it is achievable we can do a ball based on certain technical direction"
  note: Internal-direction confidence - no external commitment. "more confident than it is achievable" - confidence growth claim.

- id: m17-042
  expression: "the working solution. So that is our six months later, I can say, and we are more confident that is working"
  category: confidence_progress
  function: timeline_progress
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "So that is our six months later, I can say, and we are more confident that is working"
  note: Confidence-growth report. "six months later... more confident". Internal progress update.

- id: m17-043
  expression: "we are not giving that the more flexibility and value to you"
  category: value_assertion
  function: partner_benefit_frame
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "we are not giving that the more flexibility and value to you"
  note: Reassure partner framework benefits them. "more flexibility and value" - the two benefits.

- id: m17-044
  expression: "LPDDR has never seen that long of a except for like maybe LP3, LP4 times where there was not much choice"
  category: precedent_argument
  function: history_cite
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "LPDDR has never seen that long of a except for like maybe LP3, LP4 times where there was not much choice"
  note: Historical-precedent argument. "has never seen" + "except for". Use history to challenge current plan.

- id: m17-045
  expression: "we are the first implementation is 6.4, but we are looking at 7.2 at some point in time"
  category: timeline_split
  function: current_plus_future
  speaker_role: presenter_qualcomm
  difficulty: 3
  context: "we are the first implementation is 6.4, but we are looking at 7.2 at some point in time. In 28 time frame as well"
  note: "first implementation is X, but looking at Y at some point" - split current vs future. Avoids forcing Y now.

- id: m17-046
  expression: "since it's 28 so we're already saying 7.2 by the way just so that you can see it across the road map"
  category: roadmap_consistency
  function: cross_year_anchor
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "since it's 28 so we're already saying 7.2 by the way just so that you can see it across the road map"
  note: "just so that you can see it across the road map" - consistency-justification for repeating the ask.

- id: m17-047
  expression: "current spec format, especially the several LPDR6 spec is we think that too heavy and not well organized"
  category: spec_criticism
  function: constructive_critique
  speaker_role: presenter_sk
  difficulty: 4
  context: "current spec format, especially the several LPDR6 spec is we think that too heavy and not well organized"
  note: Constructive critique - "we think that too heavy and not well organized". Specific + actionable.

- id: m17-048
  expression: "the baseline IO, architecture, configuration, timing and the CA bus, every speed of meaning timing that kind of should be common for any profile"
  category: framework_principle
  function: common_base_assert
  speaker_role: presenter_sk
  difficulty: 5
  context: "the baseline IO, architecture, configuration, timing and the CA bus, every speed of meaning timing that kind of should be common for any profile"
  note: Framework design principle. "should be common for any profile" - the invariant-across-profiles assertion.

- id: m17-049
  expression: "I think we should seriously look into that"
  category: consideration_ask
  function: seriousness_emphasis
  speaker_role: presenter_qualcomm
  difficulty: 2
  context: "But I think we should seriously look into that. That's our request."
  note: "seriously look into" - soft ask with seriousness marker. Not "do it", "look into it seriously".

- id: m17-050
  expression: "Yeah, I know you were talking about mobile, but I just wanted to make sure that we understand the whole market segment, not just mobile"
  category: acknowledgment_reframe
  function: acknowledge_then_expand
  speaker_role: presenter_qualcomm
  difficulty: 4
  context: "Yeah, I know you were talking about mobile, but I just wanted to make sure that we understand the whole market segment, not just mobile"
  note: "Yeah, I know you were talking about X, but I just wanted to make sure Y". Acknowledge > reframe. Avoid "but you're wrong".
```

---

## 7. Excerpt Map for Shadowing

Audio: `repo/webex-audio/2026-04-27 13 51 50_EN_Qualcomm_1H-extracted.wav` (about 18 min, 2,562 words)
Recommended 5 excerpts (Mon-Fri rotation). Each about 1-2 minutes.

| # | Time (estimated) | Line range | Summary | Learning point | Difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 0:30-1:30 | line 5-16 | Qualcomm appreciation anchor + LPDDR6 requirement framing + "That's our request" | Roadmap-ask opening formula: gratitude > requirement > scope-bound > "That's our request" | ★★★ |
| 2 | 1:30-3:00 | line 38-65 | SK math-based challenge on 3-year roadmap + Qualcomm's "Maybe that was my misunderstanding" | Polite challenge (math-expose) + graceful misunderstanding ownership | ★★★★ |
| 3 | 3:00-5:00 | line 76-104 | SK priority-redirect + Qualcomm partial-agreement summary "We're aligned that 26 is 5.3..." | Priority-deflection formula + THE partial-agreement summary template | ★★★★★ |
| 4 | 5:00-8:00 | line 110-150 | SK LPSM framework proposal + consortium timing + San Diego August 20-21 | Framework pitch structure + soft timeline proposal with travel-efficiency justification | ★★★★ |
| 5 | 8:00-end | line 152-184 | Qualcomm exec welcomes framework + value reassurance + "we don't want to develop the two separate design" | Executive endorsement formula + partner-fear pre-emption | ★★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, Wed: Excerpt 3, Thu: Excerpt 4, Fri: Excerpt 5
- Daily 20-min routine slots
- Excerpt 3 is the highest-value - the partial-agreement summary is the must-memorize pattern for any roadmap meeting

---

## 8. Audrey's Teaching Notes

### Register Analysis
This meeting is **roadmap-negotiation register** - distinct from technical-deepdive (Textbook 01 Marvell) or issue-debug. Characteristics:
- Long turns with structured arguments (Qualcomm's 5-stage pitch)
- Heavy use of alignment-summary language ("we're aligned that X, not in complete agreement for Y")
- Time-anchored comparisons ("26 is 5.3, 27 is 6.4, 28 is 7.2") - year-as-spec-shorthand
- Deferral language outweighs commitment language - because the decisions aren't ripe
- Both sides hedge more than they commit - that is the *nature* of roadmap meetings, not a flaw

### Pragmatics Core
1. **Partial-agreement summarizing**: The most valuable pragmatic move in this meeting is Qualcomm's "So I think that's a line. We're aligned that X. And then we're not, you know, on complete agreement for Y. So first two years we're good. We need to go figure out the back for the third year." This converts a 3-year argument into a 2-year agreement + a deferred item. Memorize this template; use it in every roadmap meeting where you have partial alignment.
2. **Graceful misunderstanding ownership**: "Maybe that was my misunderstanding, but that's how it came out" - the middle path between admitting fault and blaming. "Maybe" hedges your concession; "that's how it came out" returns partial responsibility to the counterpart. Use this when someone calls out a contradiction in your signals.
3. **Non-monetary reframe**: "We don't need to be in it for making money, but we need to just make sure that technology moves forward" - reframe a pricing/cost ask as ecosystem-good. This is the partner-side move that converts a mercenary ask into a mission ask. The Korean equivalent ("수익 목적이 아니라 기술 진전을 위한 겁니다") exists but is rarely used in Korean business settings; in English it is standard.
4. **Direct-refusal + invite pair**: "Not at this time" + "we can we can look together". Two beats: refuse > invite. The refusal protects internal IP; the invite preserves the relationship. Never let the silence after "not at this time" sit for more than one beat.
5. **BU-echo amplification**: When your ask is resisted in one BU, echo from other BUs. "Same sentiment on mobile, similar on automotive, server needs higher speeds" - the same ask becomes a market-wide need. "The case still remains open" - polite persistence that doesn't drop the ask.

### Top 5 Must-Use
1. **"So I think that's a line. We're aligned that X. And then we're not, you know, on complete agreement for Y. So first N years we're good. We need to go figure out the back for the rest."** - partial-agreement summary
2. **"Maybe that was my misunderstanding, but that's how it came out"** - graceful misunderstanding ownership
3. **"We don't need to be in it for making money, but we need to just make sure that technology moves forward"** - non-monetary reframe
4. **"Not at this time. ... We can look together."** - direct-refusal + invite pair
5. **"Which I doubt because there are other X that are interested in Y. A is one of them, B is another which needs Z."** - soft doubt with evidence

### Korean vs English Comparison

| Korean style | English (this meeting) | Difference |
|:---|:---|:---|
| "2년까지는 맞춰졌고 3년 차는 다시 논의하죠" | "So first two years we're good. We need to go figure out the back for the third year" | Korean says "다시 논의하죠" (vague); English "go figure out the back" is action-oriented but still soft |
| "제가 오해했을 수도 있겠네요" | "Maybe that was my misunderstanding, but that's how it came out" | Korean ends at the admission; English adds "that's how it came out" to share responsibility |
| "지금은 말씀드리기 어렵습니다" | "Not at this time. ... We can look together." | Korean ends at the refusal; English immediately pairs with invite |
| "수익 목적이 아닙니다" | "we don't need to be in it for making money, but we need to just make sure that technology moves forward" | Korean is shorter; English spells out the alternative goal explicitly |
| "다른 BU도 같은 생각입니다" | "We shared the same sentiment on the mobile side. We're thinking similar stuff on the automotive as well" | Korean uses one sentence; English echoes twice ("same sentiment" + "similar stuff") for amplification |
| "의심스럽습니다" | "Which I doubt because there are other businesses that are, you know, interested in also an LB6" | Korean is bare doubt; English always backs doubt with concrete counterexamples |

---

## 9. How to Use This Textbook

1. **Daily 20-min routine**: Use Section 7 excerpt map - 5 excerpts rotated Mon-Fri
2. **Expression DB**: From Section 6's 50 entries, prioritize Section 8's Top 5 first
3. **Friday Audrey correction session**: Focus dump-writing on Section 2 (hedging/deflection) and Section 4 (negotiation) - these are the highest-value patterns for type B meetings
4. **Comparison learning**: Use Section 8's Korean-vs-English table to internalize the timing differences (especially: English pairs refusals with invites, Korean ends refusals alone)
5. **Roadmap meeting prep**: Before any Qualcomm/roadmap meeting, rehearse the partial-agreement summary template ("So I think that's a line. We're aligned that X. And then we're not in complete agreement for Y...") - this is the single most reusable pattern in this textbook

---

*Textbook 17 - Qualcomm 1H Summary (2026-04-27). Meeting type B (Roadmap / Supply Alignment). Expression DB 50 entries. 5 excerpt segments. Written: 2026-09-02.*
