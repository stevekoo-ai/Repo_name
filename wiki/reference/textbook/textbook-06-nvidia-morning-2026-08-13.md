---
textbook_id: 06
meeting: NVIDIA Morning (NVIDIA Memory Roadmap, SK Hynix per-product alignment)
date: 2026-08-13
type: B (Roadmap/Supply 정합)
partner: NVIDIA (Barry, Gautam referenced, networking presenter, multiple SK-facing speakers)
sk_side: SK Hynix (Kool G, Chumokang/automotive, HBM team, LP team, multiple product owners)
duration_words: 9708
audio: repo/webex-audio/2026-08-13 09 01 49_EN_NVIDIA_Morning-extracted.wav
transcript: repo/webex-audio/2026-08-13 09 01 49_EN_NVIDIA_Morning-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, nvidia, roadmap, lpddr, gddr, hbm, socam, alignment, type-b]
---

# Textbook 06 - NVIDIA Morning (2026-08-13)

> **Meeting type**: B (Roadmap/Supply 정합) - per-product roadmap alignment between NVIDIA (customer) and SK Hynix (supplier). Both sides walk through product-by-product roadmaps and negotiate density, speed, packaging, and timeline targets.
> **Learning value**: Type B meetings have a different structure than Type A. There is no pitch to defend. Instead, the language is "alignment language" - asking for confirmation of demand, signaling drop/hold decisions, pushing back on speed targets, and coordinating milestones. The valuable patterns here are LOW FREQUENCY, HIGH STRUCTURAL VALUE: roadmap alignment idioms, target negotiation, spec pushback, milestone coordination.
> **Audrey's view**: This is the textbook for "how to talk when you and your customer are synchronizing roadmaps." Steve, you do this kind of meeting every quarter. Memorize the alignment patterns in S2 and S4 - these are what separate a mid-level engineer from a senior roadmap owner in English.

---

## 1. Speaker Architecture - The Roadmap Alignment Dance (4 roles)

Type B meetings have a different speaker architecture than Type A. There is no single presenter. Instead, four roles rotate:

### Role 1: Roadmap Walker (Barry, NVIDIA - LP/GDDR sections)

Barry walks through the roadmap slide-by-slide. His job is NOT to pitch - it is to surface "items that seem odd" and invite SK response.

| Pattern | Original | Function |
|:---|:---|:---|
| `a couple items on here that seem a little odd given the current environment` | "again there'll be a couple items on here that seem a little odd given the current environment. We just want to talk through some of the issues." | Surface friction - flags the item as unusual without blaming |
| `I just want to talk through it with you guys, understand your thoughts on the roadmap timeline for this part` | "I'd like to talk through it with you guys, understand your thoughts on the roadmap timeline for this part" | Open-ended ask - invites SK's view instead of demanding |
| `I don't think there will be any questions on that, but I'll pause there` | "I don't think there will be any questions on that, but I'll pause there. Anything you want to dig into?" | Confidence + invitation - signals "this is settled, but I respect your right to challenge" |

**Audrey lesson**: A roadmap walker does NOT say "we want X by Y." He says "we want to talk through some of the issues" and "understand your thoughts." This invites the supplier to surface concerns first. When you walk a roadmap in English, frame each item as a discussion, not a demand. "We want to talk through X" is the senior phrasing.

### Role 2: Decision Pressure (SK side, asking for commitments)

SK pushes for decision deadlines when NVIDIA's roadmap creates development risk.

| Pattern | Original | Function |
|:---|:---|:---|
| `we need some sort of decision by October of this year, whether we'll continue to develop the die, or just completely drop it` | "So we need some sort of decision by October of this year, whether we'll continue to develop the die, or just completely drop it" | Decision deadline - binary choice with explicit date |
| `if there is no concrete input we'll probably just drop or hold off the development` | "I could put a timeframe if there is no concrete input will probably just drop or hold off the development" | Consequence statement - what happens without input |
| `when NVIDIA plans your projects, I think you have to assume that we no longer have that` | "I think when NVIDIA plans your projects, I think you have to assume that we no longer have that" | Forced assumption - tells customer to plan without us |

**Audrey lesson**: When a supplier drops a die, the language is NOT "we won't make it." It is "you have to assume we no longer have that" - the burden of planning shifts to the customer. This is senior supplier language. Memorize: "I think you have to assume that we no longer have that." It puts the decision consequence on the customer's planning side, not on your production side.

### Role 3: Target Negotiator (Barry + SK engineers on speed/density)

The most valuable patterns in this meeting. Both sides negotiate fmax, density, rank, and package targets.

| Pattern | Original | Function |
|:---|:---|:---|
| `we are targeting for 12.1 Gbps, so are we well aligned?` | "We are targeting for 12.1 DPS, so are we well aligned?" | Alignment check - "are we well aligned?" is THE Type B question |
| `I think generally we're well aligned` | "I think generally we're well aligned" | Affirm with hedge - "generally" leaves room |
| `there tends to be a little bit of flexibility around the numbers we're shooting at` | "when we have these discussions with Gotham there tends to be a little bit of flexibility around the numbers we're shooting at" | Soft pushback - "flexibility" signals target is not rigid |
| `my concern right now is we're struggling through the current qualification to get adequate margins` | "my concern right now is we're struggling through the current qualification to get adequate margins" | Concern framing - "my concern is" instead of "we can't" |
| `I worry as we go through the second round of this at a similar frequency spectrum that people will get antsy` | "I worry as we go through the second round of this at a similar frequency spectrum that people will get antsy to make sure there's an adequate margin" | Third-party attribution - "people will get antsy" not "I will be upset" |
| `if you are going to change your fmax, then we may need to have different optimization work` | "if you are going to change your fmax, then we may need to have different optimization work based on that frequency" | Conditional cost - "if you change X, we need to redo Y" |

**Audrey lesson**: "Are we well aligned?" is the single most valuable question in Type B meetings. It converts a negotiation into a coordination check. And the response "I think generally we're well aligned" - the word "generally" is critical. It affirms alignment while preserving room to reopen the discussion. NEVER drop "generally" when you are not 100% sure.

### Role 4: Product Specialist (Chumokang on automotive, networking presenter)

Product-specific deep dives happen within the roadmap walk. Specialists ask focused questions on their product.

| Pattern | Original | Function |
|:---|:---|:---|
| `this is Chumokang in charge of automotive` | "Hi, this is Chumokang in charge of automotive. I have two questions about the sole derivative and sole next." | Self-identification + scope - "in charge of X" |
| `what is the difference between the sole and sole derivative?` | "What is the difference between the sole and sole derivative and why NVIDIA chooses 646 for the next?" | Direct technical question - no hedging for specialist scope |
| `we really would like to get there higher speed` | "we really would like to get there higher speed. Since that one is a really important thing for the autonomous driving" | Justified ask - ties speed to application |

**Audrey lesson**: A specialist says "I am in charge of X" and then asks direct questions. No hedging needed within your domain - you ARE the authority. But the ask is always justified by the application: "we want higher speed because autonomous driving needs it." Never state a spec ask without the application reason.

---

## 2. Hedging & Deflection - Type B Edition

Type B hedging is different from Type A. In Type A, the presenter hedges weaknesses. In Type B, both sides hedge COMMITMENTS - because every commitment has business and engineering risk.

### Strategy 1: "Under consideration" - The Polite Hold

When SK is leaning toward dropping a die but has not decided, the language is "under consideration" with a deadline attached.

| Situation | Original | Translation |
|:---|:---|:---|
| LP5X 32Gbit development hold | "So that's under consideration so we're effectively holding off the development because of the recent change of your memory demands. So we for us to continue to develop it we need some sort of decision by October." | "검토 중이며, 고객 메모리 수요 변화로 사실상 개발 보류 중입니다. 계속 개발하려면 10월까지 결정이 필요합니다" |

**Pattern formula**: `That's under consideration. We're effectively holding off the development because of X. We need some sort of decision by Y.`

**Audrey lesson**: "Under consideration" is the English roadmap-meeting equivalent of "검토 중입니다" - but with a critical addition: "we're effectively holding off" tells the customer the de facto state is stopped, and "we need a decision by Y" gives a deadline. Korean engineers often say "검토 중입니다" and leave it open-ended. In English roadmap meetings, you MUST attach a deadline or the customer will assume you are still developing. "Under consideration + holding off + decision by Y" is the full formula.

### Strategy 2: "POR" - Plan of Record as Soft Boundary

SK and NVIDIA use "POR" (Plan of Record) to distinguish committed plans from possibilities.

| Situation | Original | Translation |
|:---|:---|:---|
| LP5 backward compatibility on Rosa | "It's technically possible but not our POR" | "기술적으로 가능하지만 당사 계획(Plan of Record)은 아닙니다" |
| BlueField 4 LPDDR5x configs | "we are evaluating additional configuration of 12 gigabyte and 8 gigabyte components, but it's not a POR yet, we are still exploring" | "12기가, 8기가 추가 구성을 평가 중이나 아직 POR는 아니며 탐색 단계입니다" |

**Pattern formula**: `It's technically possible but not our POR. We're still exploring.`

**Audrey lesson**: "POR" is a roadmap-meeting term of art. Saying "not our POR" tells the customer "do not plan around this." It is stronger than "we're considering" - it explicitly says this is NOT the plan. When a customer asks if you can do something and you are not committing, say "it's technically possible but not our POR." This protects you from later blame. "We are still exploring" softens it.

### Strategy 3: "Concern" Instead of "No"

When SK cannot commit to a speed target, they frame it as a "concern" about margin, not a refusal.

| Situation | Original | Translation |
|:---|:---|:---|
| HBM4e 12.1 Gbps fmax | "my concern right now is we're struggling through the current qualification to get adequate margins. I worry as we go through the second round of this at a similar frequency spectrum that people will get antsy" | "현재 관심사는 마진 확보에 어려움을 겪고 있다는 것입니다. 유사 주파수에서 2차 라운드 진행 시 사람들이 불안해할 수 있습니다" |
| 16 Gbps jump for LP6 | "it's very abrupt... there's like there's mountain that we have to surmount to go there" | "매우 갑작스럽습니다. 넘어야 할 산이 있습니다" |

**Pattern formula**: `My concern right now is we're struggling through X. I worry as we go through Y that people will get antsy.`

**Audrey lesson**: "We can't do 12.1" is a refusal. "My concern is we're struggling to get adequate margins" is a senior engineering concern. The difference: the concern invites collaboration ("let's work on margin together"), while the refusal ends the conversation. And "people will get antsy" - attributing concern to unnamed "people" - is brilliant deflection. It is not "I will be upset," it is "stakeholders will be nervous." Steve, use "my concern is" + "people will get antsy" when you want to push back on a target without saying no.

### Strategy 4: "Most Likely" - Hedged Forecast

When SK forecasts a future state, they use "most likely" instead of "will."

| Situation | Original | Translation |
|:---|:---|:---|
| Future capacity target | "the year after will most likely be one ninety two" | "그 다음 해는 아마도 192(기가바이트)가 될 것입니다" |
| Buffer in Feynman | "by default it's only going to be there for study purposes" | "기본적으로 연구 목적으로만 존재할 예정입니다" |

**Pattern formula**: `We'll most likely be X. By default it's only going to be there for Y.`

**Audrey lesson**: "Most likely" is the roadmap forecaster's hedge. Roadmaps change. If you say "we will be at 192," the customer holds you to it. If you say "we'll most likely be at 192," you preserve revision room. "By default" does the same - it states the current plan while signaling it can change. In Korean you would say "아마도" or "기본적으로" - the English equivalents are "most likely" and "by default." Never state a roadmap forecast without one of these hedges.

### Strategy 5: "Big Question Mark" - Acknowledging Unknowns

SK openly flags uncertainty when a target has unresolved technical risk.

| Situation | Original | Translation |
|:---|:---|:---|
| 16 Gbps buffer type | "So we may have some other type of the property design. So I think we'll use a big question mark" | "다른 유형의 property 설계가 필요할 수 있습니다. 큰 물음표로 표시하겠습니다" |
| HBM5 custom 30 Gbps | "So if your roadmap suggesting that up to 30 Gbps, then it delivers flexible confusion in a scaling style" | "로드맵이 30 Gbps까지 제시하면 확장 방식에서 유연한 혼란이 발생합니다" |

**Audrey lesson**: "Big question mark" is a vivid, honest hedge. It says "we don't know yet." This is more credible than fake confidence. Steve, when a customer asks about a target you have not internally resolved, say "I think we'll put a big question mark on that." It signals honesty and keeps the discussion open. Korean engineers often feel pressure to give a number - "big question mark" gives you permission to not have one yet.

---

## 3. Polite Challenge - Asking for the Reason Behind a Spec

Type B meetings have a specific challenge pattern: asking WHY a customer wants a spec, when the spec creates engineering risk for you.

### Challenge 1: "I wanted to understand the background"

| Pattern | Original | Function |
|:---|:---|:---|
| `I wanted to kind of understand the background. Why the sudden jump to 16. What is the technical background behind you guys asking for a higher bandwidth` | "I wanted to kind of understand the background. Why the sudden jump to 16. What is the technical background behind you guys asking for a higher bandwidth CPU they need to." | Challenge the rationale - "why the sudden jump" |

**Audrey lesson**: "Why did you ask for 16?" is confrontational. "I wanted to understand the background. Why the sudden jump to 16?" is a senior engineer asking for context. The phrase "the sudden jump" names the concern (abruptness) without accusing. And "what is the technical background" invites a technical answer, not a business answer. Use "I wanted to understand the background behind X" when you need to challenge a spec request.

### Challenge 2: "Can you clarify" - Asking for Definition

| Pattern | Original | Function |
|:---|:---|:---|
| `Can you clarify the last bit that feature product tool leverage buffer component. So do you mean so can parts or just to increase the speed` | "Can you clarify the last bit that feature product tool leverage buffer component. So. Do you mean so can parts or just to increase the speed if we mean that this is not a so can." | Clarification request - "do you mean X or Y" |

**Audrey lesson**: "Can you clarify" is the safest challenge. It says "I heard you but I need precision." Then offering two options ("do you mean X or Y") forces the customer to be specific - vague asks are common in roadmap meetings and they create engineering risk. Steve, whenever a customer request is ambiguous, respond with "Can you clarify - do you mean X or Y?" This forces them to commit to one.

### Challenge 3: "That's not aligned with our roadmap"

| Pattern | Original | Function |
|:---|:---|:---|
| `there are a couple of things that's not aligned with our roadmap as you see when we share our roadmap` | "So there are a couple of things that's not aligned with our roadmap as you see in when we share our roadmap, but the first thing is 32 gig BD5X" | Direct alignment challenge - "not aligned" is the vocabulary |

**Audrey lesson**: "Not aligned with our roadmap" is the Type B phrase for "we disagree." It does not say "you are wrong" - it says "our plans do not match yours, let's reconcile." This is the single most important Type B phrase. Memorize it. When a customer roadmap conflicts with yours, say "this is not aligned with our roadmap" - not "we can't do that."

### Challenge 4: "We're a little bit confused why"

| Pattern | Original | Function |
|:---|:---|:---|
| `we're a little bit confused why that device is there` | "So we're a little bit confused why that devices there because we've effectively. We are considering just holding off the development for that device" | Polite confusion - "we're confused" invites explanation |

**Audrey lesson**: "We're confused why X" is gentler than "why is X there." It positions you as trying to understand, not challenging. Steve, when a customer roadmap has an item you believe is wrong, say "we're a little bit confused why that device is there" - then explain your position. This is much safer than "we think that's a mistake."

### Challenge 5: "That's a bigger ask"

| Pattern | Original | Function |
|:---|:---|:---|
| `that's a bigger ask. Maybe it's the next gen buffer` | "That's a bigger ask. Maybe it's the next gen buffer. I mean, we need to also start looking at higher speeds. But right now it's just an area we want to explore" | Acknowledge scope - "bigger ask" names the magnitude |

**Audrey lesson**: "That's a bigger ask" is how you acknowledge a request is large without refusing it. It signals to the customer "we heard you, and we want you to know this is not trivial." Follow with "maybe it's the next gen" to defer to a future cycle. Steve, when a customer asks for something hard, say "that's a bigger ask" - it sets expectations without saying no.

---

## 4. Roadmap Alignment Patterns (Type B Negotiation)

The core of this textbook. Type B negotiation is NOT "we want X lower price." It is "we are targeting X in Y timeframe, are you aligned?" The patterns below are organized by alignment type.

### Pattern A: Target Timeline Alignment

| Pattern | Speaker | Original | Function |
|:---|:--:|:---|:---|
| `we expect we'll have more of a push for X in Y timeframe` | NV | "we get out into 2029 2030, we expect we'll have more of a push for six gig per second interfaces in that timeframe" | Future demand signal - "expect a push for X in Y" |
| `we're pushing for X configurations to prove out the design` | NV | "we're pushing for 14 for configurations to prove out the design" | Near-term validation target |
| `we need X by October` | SK | "we need some sort of decision by October of this year" | Decision deadline |
| `our next GP bring up will start roughly middle of 27` | NV | "our next GP bring up will start roughly middle of 27" | Bring-up milestone |
| `we hope to achieve X in second half of next year` | NV | "we hope to achieve production qualification in the second half of next year" | Qualification target |
| `we are also preparing our CS end of January next year according to our proposal` | SK | "we are also preparing our CS end of January next year according to our proposal" | Sample milestone with "according to our proposal" hedge |

**Audrey lesson**: Type B timeline statements always have a hedge and a source. "We expect a push for X" (expect = hedge). "According to our proposal" (source attribution). NEVER state a timeline as "we will deliver X on Y" in a roadmap meeting - too rigid. Use "we're targeting X" or "we expect X" or "we're preparing X according to our proposal."

### Pattern B: Density / Speed / Packaging Requirements

| Pattern | Speaker | Original | Function |
|:---|:--:|:---|:---|
| `we'd like X but Y is limited` | SK | "we'd like to push frequency but... it's a bigger ask" | Spec pushback with constraint |
| `if we can get the native way that's more optimal but we may consider a buffer` | NV | "If we can get the native way that's more optimal but we may consider a buffer in some of these applications to increase the speed" | Preferred path + fallback |
| `32 gigabit is still our main requirement` | NV | "So I think 32 gigabit is still our main requirement" | Priority declaration |
| `we prioritize non-buffer designs because of cost and power` | SK | "I would prioritize non buffer designs because of cost and power also" | Priority with reason |
| `the immediate ask is 518 ball with all the possible configs` | NV | "the immediate ask is 518 ball with all the possible confets" | "Immediate ask" - near-term request |
| `we are targeting 78 terabytes per second for that generation, so challenging I'm sure` | NV | "Targeting 78 terabytes per second for that generation, so challenging I'm sure" | Target + empathy ("challenging I'm sure") |

**Audrey lesson**: "The immediate ask is X" is a powerful phrase. It separates near-term needs from future possibilities. Use this when you want to focus the supplier: "the immediate ask is X, the future discussion is still open." And note "challenging I'm sure" - acknowledging the supplier's difficulty while stating the target. This empathy costs nothing and builds collaboration.

### Pattern C: Milestone Coordination

| Pattern | Speaker | Original | Function |
|:---|:--:|:---|:---|
| `we'd like to check your test-bake schedule` | SK | "we'd like to check your test-bake schedule because we are also considering our engineer dispatch timely manner" | Schedule coordination with reason |
| `we appreciate if you confirm our proposal and give some feedback` | SK | "we appreciate if you confirm our proposal and give some feedback" | Confirmation request - polite formal |
| `when that's confirmed would you let us know as soon as possible because that's something that we would need when we design` | SK | "when that's confirmed would you let us know as soon as possible because that's something that we would need ahead of time for us to design" | Urgency with design dependency |
| `we'll do the validation with the buffer die` | NV | "We'll do the validation with the buffer die" | Action statement |
| `we need to bring up the buffer up to speed` | SK | "We need to bring up the buffer up to speed" | Bring-up commitment |

### Pattern D: Decision Expressions

| Pattern | Speaker | Original | Function |
|:---|:--:|:---|:---|
| `we'd like to confirm X` | SK | "we'd like to confirm our proposal" | Confirmation request |
| `under consideration` | SK | "that's under consideration" | Decision pending |
| `it's not a POR yet, we're still exploring` | NV | "it's not a POR yet, we are still exploring" | Not committed |
| `we'll continue to discuss the impact of this proposed... it sounds like a change` | NV | "We'll continue to discuss the impact of this proposed. It sounds like a change." | Acknowledging change proposal |
| `it's still being discussed but current direction is X` | NV | "It's still being discussed but current direction is maybe 8dp and 16dp you limit to say 1.3" | Current direction with "still being discussed" hedge |
| `we will touch X first` | SK | "first session we will touch NVIDIA's social roadmap first" | Meeting flow - "touch X" |
| `we'd like to come from some items for further discussions` | SK | "we'd like to come from some items for further discussions" | Open discussion items |

**Audrey lesson**: Type B meetings are full of "still being discussed," "current direction is," "we're still exploring" - these are NOT weak language. They are the precise vocabulary of roadmap management. A committed plan in a roadmap meeting is rare because roadmaps change. Steve, when you state a plan that is not final, use "the current direction is X" or "the current thinking is X" - this protects you if the plan changes next quarter.

### Pattern E: "Aligned" - The Master Word

| Pattern | Original | Function |
|:---|:---|:---|
| `are we well aligned?` | "are we well aligned?" | THE alignment check |
| `I think generally we're well aligned` | "I think generally we're well aligned" | Affirm with hedge |
| `I think they were aligned on the six` | "Yeah, if that's the case, I think I think they were aligned on the six" | Past alignment confirmation |
| `I think it's pretty well aligned with the rest of the public data` | "But aside from that, I think it's pretty well aligned with the rest of the public data" | Aligned with external data |
| `not aligned with our roadmap` | "there are a couple of things that's not aligned with our roadmap" | Negative alignment |

**Audrey lesson**: "Aligned" is THE word of Type B meetings. Use it constantly. "Are we aligned?" "I think we're aligned." "This is not aligned." The word "aligned" is preferred over "agreed" because agreement is binary (yes/no) while alignment is a spectrum (we are mostly in the same place). In roadmap meetings, you are almost never 100% agreed, but you are usually "well aligned." Use "aligned" instead of "agreed."

---

## 5. Domain Vocabulary (Roadmap Alignment Edition)

The specialized vocabulary of memory roadmap meetings. Each term with its specific roadmap context.

| Term | Meaning | In-meeting usage |
|:---|:---|:---|
| **POR** (Plan of Record) | Committed plan, official roadmap item | "it's technically possible but not our POR" - "not a POR yet" distinguishes exploration from commitment |
| **fmax** | Maximum operating frequency | "we are targeting for 12.1 DPS for fmax" - "targeting X for fmax" is the standard phrasing |
| **guard band** | Safety margin above spec speed | "each of the speed bin has to include like at least 5% or even 10% guard band" - 5-10% typical |
| **bring up** | Initial hardware power-on and validation | "our next GP bring up will start roughly middle of 27" - "bring up starts in X" |
| **ES** (Engineering Sample) | Early prototype silicon | "the left edge of the ES window being about the time we need to start stacking our base die plus your core together" |
| **CS** (Customer Sample) | Sample sent to customer for validation | "the CS window is really starting to now attach it to the GPU" |
| **NPI** (New Product Introduction) | Formal product launch process | "the NPI with the HMF review start maybe end of this year or early next year" |
| **POC** (Pull-in Of Commitment) | Schedule advancement request | "we are preparing region BB and proposed our pull-in schedule as the end of November" - "pull-in schedule" = earlier |
| **by six / by twelve / by 24** | Memory channel width (x6, x12, x24) | "the 518 ball is either by 12 or the by 24 dice buffer is right now designed for by six only" |
| **rank** | Number of independent access banks | "we optimize our controller for three ranks" / "single rank gives you decent performance" |
| **so can** (SoC AM) | System-on-Chip Advanced Memory | "since that one is a really important thing for the autonomous driving... we are utilized like a 646 ball" |
| **646 / 518 / 529 ball** | Package pin counts | "the common thread seems to be 646 is where the market will settle" - "ball" = pin count |
| **dynamic / static efficiency** | LP6 power-efficiency modes | "the dynamic in the static efficiency configurations that are being supported... static efficiency is the preferred config" |
| **16DP / 32DP** | 16-channel / 32-channel DIMM package | "we make everything same height or start with a smaller and also enable different height for 32dp" |
| **wafer** | Full silicon wafer | "we need to have a plan to consume the whole wafer in some form" - whole-wafer consumption is a real constraint |
| **trim off the lowest parts** | Bin-out low-performance parts | "Maybe we choose to trim off the lowest parts for some reason. But at the end of the day, we've got to consume the whole wafer" |
| **standard ecosystem vs custom** | Standard vs custom HBM | "put those into the standard ecosystem, and let the custom be more optimized" - sorting strategy |
| **Gotham** | NVIDIA's internal name for a CPU/GPU program | "when we have these discussions with Gotham there tends to be a little bit of flexibility" |
| **Rosa / Feynman / Rubin / Vera / Julia** | NVIDIA product code names | "Rosa next we are going to update a lot so that we are looking for the like 16 giga BPS" |
| **BlueField 3 / 4 / 4.1** | NVIDIA DPU generations | "the current Bluefield 3 is still using DDR5, but the coming Bluefield 4 that is launching with Vera" |
| **MRDIM Gen 3** | DDR5 MCR DIMM, 3rd gen | "MRDIM Gen 3 is pushing to 16. So we want to compete with those in terms of frequency" - competitive benchmark |
| **UCIe** | Universal Chiplet Interconnect Express | referenced in custom HBM context |
| **buffer die** | Discrete buffer on module for signal integrity | "this is a new type of buffer we think because we think that current property design support only up to 14.4" |
| **Peregrine** | Transistor node/candidate for next gen | "Whether or not we can we have to map the road transistor or the peregrine transistor. That's the critical point" |
| **back-to-back testing** | A/B comparison of two designs | "we'll have our test vehicle for back-to-back testing of the base die" |
| **qualification / qual** | Formal validation process | "we are just about to complete the qualification of that with SSSK hynix" |
| **die / core / base die** | HBM stack components | "the time we need to start stacking our base die plus your core together" |
| **height** (1.3 / 1.8 / 1.9) | Stack height in mm | "16dp you limit to say 1.3 and then we state 32dp with a different height 1.8" |
| **POC** (Proof of Concept) | Concept validation | "the future discussion is still open" |
| **discrete on the board** | Discrete component (not module) | "This could be a buffer. This could be a discrete on the board" |
| **cherry-pick** | Select best parts | "if there needs to be some cherry picking of parts, you know, we can try to accommodate that as well" |

---

## 6. Expression Database

48 entries. YAML schema. IDs "m06-NNN".

```yaml
# ── Roadmap Walker (Presentation Architecture for Type B) ──
- id: m06-001
  expression: "there'll be a couple items on here that seem a little odd given the current environment"
  category: roadmap_walker
  function: friction_surface
  speaker_role: walker
  difficulty: 5
  context: "again there'll be a couple items on here that seem a little odd given the current environment. We just want to talk through some of the issues."
  note: Type B walker flags friction items without blame. "seem a little odd given the current environment" is the senior phrasing.

- id: m06-002
  expression: "I'd like to talk through it with you guys, understand your thoughts on X"
  category: roadmap_walker
  function: open_invitation
  speaker_role: walker
  difficulty: 4
  context: "I'd like to talk through it with you guys, understand your thoughts on the roadmap timeline for this part"
  note: Open-ended ask - invites supplier view instead of demanding

- id: m06-003
  expression: "I don't think there will be any questions on that, but I'll pause there"
  category: roadmap_walker
  function: confidence_with_invitation
  speaker_role: walker
  difficulty: 4
  context: "I don't think there will be any questions on that, but I'll pause there. Anything you want to dig into?"
  note: Signals "this is settled" while preserving the right to challenge

- id: m06-004
  expression: "Anything you want to dig into?"
  category: question_invitation
  function: open_challenge
  speaker_role: walker
  difficulty: 3
  context: "Anything you want to dig into?"
  note: "dig into" - more collaborative than "any questions"

- id: m06-005
  expression: "I'll go through quickly for HBM roadmap. So, first, let me recap what we discussed a couple weeks ago"
  category: roadmap_walker
  function: recap_opener
  speaker_role: walker
  difficulty: 3
  context: "Okay, let me start and go through quickly our HBM roadmap. So, first, let me recap what we discussed a couple weeks ago. Product by product."
  note: "recap" opens continuity - signals "we have history, let's build on it"

- id: m06-006
  expression: "Product by product"
  category: roadmap_walker
  function: structure_signal
  speaker_role: walker
  difficulty: 2
  context: "Product by product."
  note: Short structure signal - tells the audience the order of discussion

- id: m06-007
  expression: "those are my slides"
  category: transition
  function: section_close
  speaker_role: walker
  difficulty: 2
  context: "Okay so those are my slides."

# ── Alignment Language (The core Type B vocabulary) ──
- id: m06-008
  expression: "are we well aligned?"
  category: alignment
  function: alignment_check
  speaker_role: either
  difficulty: 5
  context: "We are targeting for 12.1 DPS, so are we well aligned?"
  note: THE Type B question. Memorize. Use this in every roadmap meeting.

- id: m06-009
  expression: "I think generally we're well aligned"
  category: alignment
  function: aligned_with_hedge
  speaker_role: either
  difficulty: 5
  context: "I think generally we're well aligned."
  note: "generally" preserves room to reopen. Never drop it unless 100% sure.

- id: m06-010
  expression: "I think they were aligned on the X"
  category: alignment
  function: past_alignment
  speaker_role: either
  difficulty: 4
  context: "Yeah, if that's the case, I think I think they were aligned on the six."
  note: Past alignment - "were aligned" confirms historical agreement

- id: m06-011
  expression: "it's pretty well aligned with the rest of the public data"
  category: alignment
  function: external_alignment
  speaker_role: either
  difficulty: 4
  context: "I think it's pretty well aligned with the rest of the public data."

- id: m06-012
  expression: "there are a couple of things that's not aligned with our roadmap"
  category: alignment
  function: misalignment_flag
  speaker_role: supplier
  difficulty: 5
  context: "So there are a couple of things that's not aligned with our roadmap as you see in when we share our roadmap"
  note: Type B phrase for "we disagree" - "not aligned" not "wrong"

# ── Decision Pressure (Supplier side) ──
- id: m06-013
  expression: "we need some sort of decision by October of this year, whether we'll continue to develop the die, or just completely drop it"
  category: decision_pressure
  function: binary_deadline
  speaker_role: supplier
  difficulty: 5
  context: "So we need some sort of decision by October of this year, whether we'll continue to develop the die, or just completely drop it."
  note: Binary choice + explicit date. Senior supplier language.

- id: m06-014
  expression: "if there is no concrete input we'll probably just drop or hold off the development"
  category: decision_pressure
  function: consequence
  speaker_role: supplier
  difficulty: 4
  context: "I could put a timeframe if there is no concrete input will probably just drop or hold off the development."

- id: m06-015
  expression: "I think you have to assume that we no longer have that"
  category: decision_pressure
  function: forced_assumption
  speaker_role: supplier
  difficulty: 5
  context: "I think when NVIDIA plans your projects, I think you have to assume that we no longer have that."
  note: Shifts planning burden to customer. Critical senior phrase.

- id: m06-016
  expression: "we're a little bit confused why that device is there"
  category: polite_challenge
  function: confusion_invitation
  speaker_role: supplier
  difficulty: 4
  context: "So we're a little bit confused why that devices there because we've effectively."
  note: "we're confused" invites explanation without accusation

# ── Hedging & Deflection (Type B) ──
- id: m06-017
  expression: "that's under consideration, we're effectively holding off the development"
  category: hedging
  function: polite_hold
  speaker_role: supplier
  difficulty: 5
  context: "So that's under consideration so we're effectively holding off the development because of the recent change of your memory demands."
  note: "under consideration + holding off + deadline" is the full formula

- id: m06-018
  expression: "it's technically possible but not our POR"
  category: hedging
  function: not_committed
  speaker_role: either
  difficulty: 5
  context: "But I mean, it's technically possible but not our POR."
  note: "POR" tells customer "do not plan around this"

- id: m06-019
  expression: "it's not a POR yet, we're still exploring"
  category: hedging
  function: exploration_phase
  speaker_role: customer
  difficulty: 4
  context: "it's not a POR yet, we are still exploring to see if there are availability in the market"

- id: m06-020
  expression: "my concern right now is we're struggling through the current qualification to get adequate margins"
  category: concern_framing
  function: senior_pushback
  speaker_role: supplier
  difficulty: 5
  context: "my concern right now is we're struggling through the current qualification to get adequate margins"
  note: "concern" not "refusal" - invites collaboration

- id: m06-021
  expression: "I worry as we go through Y that people will get antsy"
  category: concern_framing
  function: third_party_attribution
  speaker_role: supplier
  difficulty: 5
  context: "I worry as we go through the second round of this at a similar frequency spectrum that people will get antsy"
  note: "people will get antsy" - defers concern to unnamed stakeholders

- id: m06-022
  expression: "we'll most likely be X"
  category: hedging
  function: forecast_hedge
  speaker_role: either
  difficulty: 3
  context: "the year after will most likely be one ninety two"

- id: m06-023
  expression: "by default it's only going to be there for study purposes"
  category: hedging
  function: scope_limit
  speaker_role: either
  difficulty: 4
  context: "by fault is going to be if it is there, it's only going to be there for study purposes."

- id: m06-024
  expression: "I think we'll use a big question mark"
  category: hedging
  function: honest_unknown
  speaker_role: supplier
  difficulty: 4
  context: "So I think we'll use a big question mark."

# ── Spec Pushback ──
- id: m06-025
  expression: "I wanted to kind of understand the background. Why the sudden jump to X"
  category: spec_pushback
  function: rationale_challenge
  speaker_role: supplier
  difficulty: 5
  context: "I wanted to kind of understand the background. Why the sudden jump to 16."
  note: "the sudden jump" names the concern without accusing

- id: m06-026
  expression: "it's very abrupt... there's like there's mountain that we have to surmount to go there"
  category: spec_pushback
  function: magnitude_metaphor
  speaker_role: supplier
  difficulty: 4
  context: "But it's very abrupt because I mean the spec EOL speed is 14.4. So for us to prepare for that we there there's like there's mountain that we have to surmount to go there."

- id: m06-027
  expression: "it's something that we have to collaborate, we have to discuss before we can conclusively say that we can do X"
  category: spec_pushback
  function: collaborative_uncertainty
  speaker_role: supplier
  difficulty: 5
  context: "it's something that we have to collaborate. We have to discuss before we can conclusively say that we can do 16."

- id: m06-028
  expression: "Can you clarify - do you mean X or Y"
  category: clarification
  function: binary_clarify
  speaker_role: either
  difficulty: 4
  context: "Can you clarify the last bit that feature product tool leverage buffer component. So. Do you mean so can parts or just to increase the speed"

- id: m06-029
  expression: "that's a bigger ask. Maybe it's the next gen X"
  category: scope_acknowledgment
  function: defer_to_next
  speaker_role: either
  difficulty: 4
  context: "That's a bigger ask. Maybe it's the next gen buffer."

- id: m06-030
  expression: "if you are going to change your fmax, then we may need to have different optimization work"
  category: conditional_cost
  function: change_cost
  speaker_role: supplier
  difficulty: 5
  context: "if you are going to change your fmax, then we may need to have different optimization work based on that frequency."
  note: "if you change X, we need to redo Y" - conditional cost statement

# ── Target Negotiation ──
- id: m06-031
  expression: "we expect we'll have more of a push for X in Y timeframe"
  category: target_signal
  function: future_demand
  speaker_role: customer
  difficulty: 4
  context: "we expect we'll have more of a push for six gig per second interfaces in that timeframe"

- id: m06-032
  expression: "we're pushing for X configurations to prove out the design"
  category: target_signal
  function: validation_target
  speaker_role: customer
  difficulty: 3
  context: "we're pushing for 14 for configurations to prove out the design"

- id: m06-033
  expression: "the immediate ask is X"
  category: target_signal
  function: near_term_focus
  speaker_role: customer
  difficulty: 4
  context: "the immediate ask is 518 ball with all the possible confets"

- id: m06-034
  expression: "if we can get the native way that's more optimal but we may consider a buffer"
  category: target_negotiation
  function: preferred_with_fallback
  speaker_role: customer
  difficulty: 4
  context: "If we can get the native way that's more optimal but we may consider a buffer in some of these applications to increase the speed"

- id: m06-035
  expression: "X is still our main requirement"
  category: priority_declaration
  function: priority
  speaker_role: customer
  difficulty: 3
  context: "So I think 32 gigabit is still our main requirement."

- id: m06-036
  expression: "we prioritize non-buffer designs because of cost and power"
  category: priority_declaration
  function: priority_with_reason
  speaker_role: supplier
  difficulty: 4
  context: "I would prioritize non buffer designs because of cost and power also"

- id: m06-037
  expression: "we are targeting X for Y, so challenging I'm sure"
  category: target_with_empathy
  function: target_empathy
  speaker_role: customer
  difficulty: 5
  context: "Targeting 78 terabytes per second for that generation, so challenging I'm sure"
  note: "challenging I'm sure" - empathy costs nothing, builds collaboration

# ── Milestone Coordination ──
- id: m06-038
  expression: "we'd like to check your X schedule because we are also considering Y"
  category: schedule_coordination
  function: schedule_with_reason
  speaker_role: supplier
  difficulty: 4
  context: "we'd like to check your test-bake schedule because we are also considering our engineer dispatch timely manner"

- id: m06-039
  expression: "we appreciate if you confirm our proposal and give some feedback"
  category: confirmation_request
  function: polite_formal_confirm
  speaker_role: supplier
  difficulty: 4
  context: "we appreciate if you confirm our proposal and give some feedback"

- id: m06-040
  expression: "when that's confirmed would you let us know as soon as possible because that's something that we would need ahead of time for us to design"
  category: urgency_request
  function: design_dependency_urgency
  speaker_role: supplier
  difficulty: 5
  context: "when that's confirmed would you let us know as soon as possible because that's something that we would need when we or that something that we need ahead of time for us to design"

- id: m06-041
  expression: "it's still being discussed but current direction is X"
  category: direction_hedge
  function: current_direction
  speaker_role: customer
  difficulty: 4
  context: "It's still being discussed but current direction is maybe 8dp and 16dp you limit to say 1.3"
  note: "current direction" + "still being discussed" - roadmap management vocabulary

# ── Specialist Self-Identification ──
- id: m06-042
  expression: "this is X in charge of Y"
  category: self_identification
  function: scope_claim
  speaker_role: specialist
  difficulty: 3
  context: "Hi, this is Chumokang in charge of automotive. I have two questions about the sole derivative and sole next."
  note: "in charge of X" claims authority and scope

- id: m06-043
  expression: "we really would like to get there higher speed. Since that one is a really important thing for X"
  category: justified_ask
  function: application_justification
  speaker_role: specialist
  difficulty: 4
  context: "we really would like to get there higher speed. Since that one is a really important thing for the autonomous driving"

# ── Whole Wafer Constraint ──
- id: m06-044
  expression: "we need to have a plan to consume the whole wafer in some form"
  category: business_constraint
  function: capacity_reality
  speaker_role: either
  difficulty: 4
  context: "We need to have a plan to consume the whole wafer in some form. Maybe we choose to trim off the lowest parts for some reason. But at the end of the day, we've got to consume the whole wafer."

- id: m06-045
  expression: "is there some sorting out of worst wafers, put those into the standard ecosystem, and let the custom be more optimized"
  category: sorting_strategy
  function: bin_proposal
  speaker_role: customer
  difficulty: 4
  context: "Is there some sorting out of worst wafers, put those into the standard ecosystem, and let the custom be more optimized?"

# ── Meeting Management ──
- id: m06-046
  expression: "we'll have a parallel discussion, X at 3pm and afterward we will touch Y and Z"
  category: agenda
  function: schedule_layout
  speaker_role: host
  difficulty: 3
  context: "we will have a parallel discussion, HBAM GDDR at 3pm and afterward we will touch LPEX and SOCAM DL6"

- id: m06-047
  expression: "first session we will touch X first"
  category: agenda
  function: order_signal
  speaker_role: host
  difficulty: 2
  context: "first session we will touch NVIDIA's social roadmap first"

- id: m06-048
  expression: "we'd like to come from some items for further discussions"
  category: discussion_open
  function: open_items
  speaker_role: supplier
  difficulty: 3
  context: "we'd like to come from some items for further discussions"
```

---

## 7. Excerpt Map for Shadowing

Audio: `repo/webex-audio/2026-08-13 09 01 49_EN_NVIDIA_Morning-extracted.wav` (approximately 60 minutes, 9,708 words).
Recommended 5 excerpt segments for Mon-Fri rotation. Each segment 1-2 minutes.

| # | Time (est.) | Lines | Content summary | Learning point | Shadowing difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | Opening (lines 4-7, 26-31) | 4-31 | SK host agenda + Barry opens LP roadmap, "we expect a push for 6G in 2029-2030 timeframe" | Roadmap walker opening - "expect a push for X in Y timeframe" | ★★★ |
| 2 | LP5X decision pressure (lines 33-52) | 33-52 | SK "not aligned with our roadmap" + "need decision by October" + "under consideration, holding off" | Decision pressure formula + "under consideration + holding off + deadline" | ★★★★ |
| 3 | LP6 density negotiation (lines 78-95) | 78-95 | NV asks about 48Gbit LP6, SK proposes 24/32 instead, "32 is main requirement", "prioritize non-buffer because of cost and power" | Density/speed/packaging alignment - priority declaration with reason | ★★★★ |
| 4 | HBM4e fmax negotiation (lines 723-742) | 723-742 | SK "we are targeting 12.1 Gbps, are we well aligned?" + NV "generally well aligned" + "concern about adequate margins" + "people will get antsy" | THE alignment exchange - "are we well aligned?" + "concern" pushback + "people will get antsy" deflection | ★★★★★ |
| 5 | Whole-wafer strategy (lines 822-827) | 822-827 | NV "we need to have a plan to consume the whole wafer" + "sorting out worst wafers, put those into the standard ecosystem, let the custom be more optimized" | Business constraint - "consume the whole wafer" + bin sorting strategy | ★★★★ |

**Usage**:
- Mon: Excerpt 1 (roadmap walker opening)
- Tue: Excerpt 2 (decision pressure - LP5X drop scenario)
- Wed: Excerpt 3 (density negotiation - LP6 32 vs 24 vs 48)
- Thu: Excerpt 4 (HBM4e fmax - the "are we well aligned" exchange - HIGHEST VALUE)
- Fri: Excerpt 5 (whole-wafer strategy - senior business constraint language)

Excerpt 4 is the single most valuable segment in this textbook. The "are we well aligned?" + "generally well aligned" + "concern about margins" + "people will get antsy" sequence in 20 lines contains more Type B pragmatic value than the rest combined. Shadow it until automatic.

---

## 8. Audrey's Teaching Notes

### Register (화체) Analysis

This meeting is **Type B roadmap alignment** register. Unlike Type A (pitch + defense), here both sides are peers synchronizing plans. The register has three layers:

- **Walker register** (Barry): "we want to talk through," "understand your thoughts," "I'll pause there" - low assertion, high invitation
- **Decision-maker register** (SK): "we need a decision by October," "you have to assume we no longer have that," "under consideration" - firm but collaborative
- **Engineering-negotiation register** (both): "are we well aligned?" "my concern is margins," "if you change fmax we need to redo optimization" - technical precision with face preserved

### Pragmatics (화용론) Core

1. **"Aligned" over "agreed"**: Roadmap meetings avoid "agree" because agreement is binary. "Aligned" is spectrum - you can be "well aligned," "generally aligned," "not aligned." Steve, when you state agreement, use "aligned." When you state disagreement, use "not aligned" - never "we disagree."

2. **"Under consideration" + holding off + deadline**: This is the Korean "검토 중입니다" with three additions English requires: (a) "we're effectively holding off" - what is actually happening, (b) "because of X" - the reason, (c) "decision by Y" - the deadline. The Korean version leaves it open; the English version forces closure.

3. **"POR" as a boundary**: "Not our POR" is the strongest soft refusal in roadmap meetings. It tells the customer "do not plan around this" without saying "we won't do it." Steve, when a customer asks if you can do something you are not committing to, "it's technically possible but not our POR" is the senior answer.

4. **"Concern" over "no"**: Senior engineers never say "we can't do 12.1 Gbps." They say "my concern is we're struggling to get adequate margins." The concern invites collaboration; the refusal ends the conversation. "I worry people will get antsy" attributes the concern to unnamed stakeholders - brilliant deflection.

5. **"People will get antsy"**: Never "I will be upset." The concern is always someone else's - "people," "stakeholders," "the team." This depersonalizes the pushback and makes it about system reality, not personal resistance.

### Top 5 You Should Use Immediately

1. **"Are we well aligned?"** - the Type B master question. Use at end of every spec discussion.
2. **"That's under consideration. We're effectively holding off the development. We need a decision by October."** - the full hold formula with deadline.
3. **"I think generally we're well aligned"** - affirm with hedge. Never drop "generally" unless 100% committed.
4. **"My concern right now is we're struggling through the current qualification to get adequate margins"** - pushback via concern, not refusal.
5. **"I think you have to assume that we no longer have that"** - shift planning burden to customer when dropping a die.

### Korean vs English Roadmap Phrases

| Korean | English (this meeting) | Difference |
|:---|:---|:---|
| "검토 중입니다" | "That's under consideration. We're effectively holding off. We need a decision by October." | Korean is open-ended; English requires state + reason + deadline |
| "계획에 없습니다" | "It's technically possible but not our POR." | "POR" explicitly tells customer not to plan around it |
| "안 됩니다" | "My concern is we're struggling to get adequate margins." | "concern" invites collaboration; "안 됩니다" ends discussion |
| "우리 로드맵과 다릅니다" | "This is not aligned with our roadmap." | "not aligned" invites reconciliation; "다르다" can sound like refusal |
| "10월까지 답 주세요" | "We need some sort of decision by October, whether we'll continue or just completely drop it." | English makes the binary choice explicit |
| "아마 192가 될 겁니다" | "We'll most likely be 192." | "most likely" preserves revision room; "아마" is vaguer |
| "왜 16으로跳吗?" | "I wanted to understand the background. Why the sudden jump to 16?" | "sudden jump" names concern; "왜" is direct |
| "그건 큰 요청입니다" | "That's a bigger ask. Maybe it's the next gen." | "bigger ask" acknowledges scope without refusing |
| "잘 맞춰져 있습니다" | "I think we're well aligned." | "aligned" is spectrum; "agreed" is binary |

---

## 9. How to Use This Textbook

1. **Daily 20-min routine**: 5 excerpts from S7, rotated Mon-Fri. Excerpt 4 (HBM4e fmax) is highest value - shadow it 3x per week.
2. **Expression DB**: 48 entries. Memorize S8 Top 5 first - these are the survival phrases for any roadmap meeting.
3. **Audrey Friday correction**: Focus writing dump on S2 (hedging) and S4 (alignment patterns). The "aligned" vocabulary and "under consideration + holding off + deadline" formula are the highest priorities.
4. **Comparison learning**: S8 Korean-English comparison table - practice the full English formula every time you would use the short Korean version. The Korean "검토 중입니다" must ALWAYS expand to "under consideration + holding off + deadline by Y" in English.
5. **Role-play pairs**: With Audrey, role-play the LP5X drop scenario (excerpt 2) and HBM4e fmax negotiation (excerpt 4). These are the two most common Type B scenarios you will face every quarter.

---

*Textbook 06 - NVIDIA Morning (2026-08-13). Meeting type B (Roadmap/Supply alignment). Expression DB 48 entries. 5 excerpt segments. Written: 2026-09-02. Reclassification: confirmed Type B from initial hypothesis - no reclassification needed.*
