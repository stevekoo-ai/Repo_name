---
textbook_id: 30
meeting: INTEL (December sync, sample/schedule coordination)
date: 2025-12-05
type: C (sample/schedule coordination) - confirmed after reading
partner: Intel (Jenny, Ivan, Ed, Looper, Tony-GPU)
sk_side: Sangdon (lead), Tony, Dogun, Jerry
duration_words: 5290
audio: repo/webex-audio/2025-12-05 09 18 29_EN_INTEL-extracted.wav
transcript: repo/webex-audio/2025-12-05 09 18 29_EN_INTEL-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, intel, cxl, cmm, es-cs-mp, sample-schedule, gaudi, kv-cache, validation, type-c]
---

# Textbook 30 - INTEL December Sync (2025-12-05)

> **Meeting type**: C (sample/schedule coordination) - SK Hynix CMM sample schedule + Intel volume validation timeline alignment + Gaudi GPU collaboration request
> **Learning value**: Schedule alignment language ("align our schedule with your schedule"), polite misunderstanding recovery, soft hardware request, "shopping list" clarification pattern
> **Audrey view**: This meeting is the classic "schedule coordination + soft ask" pattern. You will learn how to (1) push for timeline clarity without seeming pushy, (2) recover from a misunderstanding cleanly, (3) ask for partner hardware without sounding demanding.

---

## 1. Speech architecture - Sangdon's meeting lead structure (5 steps)

Sangdon (SK Hynix lead) runs this sync in a 5-step structure. Each step has a **fixed language formula**. This is the bone structure you should follow when leading a schedule coordination meeting.

### Step 1: Status touchback (Status Recap)

Sangdon opens by touching the previous sync's open item, not by starting a new topic.

| Language formula | Original | Function |
|:---|:---|:---|
| `We had touched the status of X in Y site` | "We had touched the status of the scanning second gen CMM in Intel site" | Touchback - "we had touched" connects to prior sync |
| `We would like to touch X first but our engineering team didn't join` | "We would like to touch the GNR white paper collaboration first but our engineering team didn't join this morning" | Agenda reorder with reason - "would like to touch X but Y" |

**Audrey lesson**: English sync meetings open with "We had touched X last time" - not "Let's start." The past perfect "had touched" signals continuity. Then "We would like to touch X first but Y" lets you reorder the agenda without dropping a topic - you state the want, then the blocker. Memorize this opener.

### Step 2: Schedule presentation (Schedule Walk-through)

Sangdon presents the SK Hynix CMM schedule by naming each milestone with its quarter.

| Language formula | Original | Function |
|:---|:---|:---|
| `as SK hynix the cmm schedule pushed out two months` | "as SK hynix the cmm schedule pushed out two months" | Push-out disclosure - "pushed out N months" |
| `SK hynix may support the ES sample at the end of q3 2026` | "SK hynix may support the ES sample rap maybe end of q3 2026" | Sample type + quarter - "ES sample at the end of Q3" |
| `the pomeo is already CS level at the end of q3 in 2026` | "the pomeo is already CS level the at the end of q3 in 2026" | CS (Customer Sample) milestone statement |
| `we would like to know is that okay or not` | "we would like to know is that okay or not" | Validation ask - "is that okay or not" |

**Audrey lesson**: Schedule talk in English hardware meetings uses a fixed vocabulary: **ES (Engineering Sample), CS (Customer Sample), MP (Mass Production), qualification, production**. You do NOT say "we will make samples." You say "we may support the ES sample at the end of Q3." "Support" is the verb - the partner "receives" and you "support." And "is that okay or not" is the direct close - do not soften it to "is that fine?" Use the binary "okay or not" when you need a yes/no on a timeline.

### Step 3: Schedule alignment ask (Alignment Request)

Sangdon explicitly states the alignment goal - not just asking a question, but naming the intent.

| Language formula | Original | Function |
|:---|:---|:---|
| `we want to just trying to align our schedule with your schedule and see whether it is aligning or not` | "we want to just trying to align our the our schedule with your schedule and see whether it is aligning or not" | Alignment intent stated directly |
| `we'd like to know the schedule so we can update the new intel tmr's the timeline` | "we'd like to know the schedule so we can update the new intel tmr's the timeline" | Reason for ask - "so we can update" |
| `we would like to know how much the does intel lead the for the validation sample` | "we would like to know how much the does intel lead the for the validation sample" | "How much does Intel lead" - probe partner timeline |
| `is this timeline is good or are we missing your launch` | "is this timeline is good or are we missing your launch" | Risk probe - "are we missing your launch" |

**Audrey lesson**: "We want to align our schedule with your schedule" is the single most useful sentence in this entire meeting. It frames every question that follows as coordination, not pressure. When you ask a partner about their timeline, preface it with "we want to align our schedule with yours" - this converts a potentially intrusive question into a joint planning act. And "are we missing your launch" is the risk-voice version - it shows you are worried about being late, which makes the partner want to reassure you with their actual timeline.

### Step 4: Misunderstanding recovery (Misunderstanding Recovery)

When Intel corrects Sangdon's wrong assumption about volume validation, Sangdon uses a clean recovery formula.

| Language formula | Original | Function |
|:---|:---|:---|
| `I just wonder uh do we miss the your timeline` | "I just wonder uh do we miss the your timeline" | "I just wonder" - softener before admitting confusion |
| `it's my misunderstanding` | "it's my misunderstanding" | Direct admission - "it's my misunderstanding" (not "I'm sorry") |
| `I don't know where about that` | "I don't know where about that" | Knowledge gap admission |
| `Okay okay okay I understand that` | "Okay okay okay I understand that" | Triple "okay" - acknowledgment after correction |
| `hopefully that clarifies right` | "hopefully that clarifies right" (Intel Jenny) | Partner's confirmation - "that clarifies" |

**Audrey lesson**: When you are wrong in a meeting, the cleanest recovery is **"it's my misunderstanding"** - not "I'm sorry, I made a mistake." "Misunderstanding" attributes the error to interpretation, not competence. Then "Okay, I understand that" closes the loop. Do NOT over-apologize. And the triple "okay okay okay" is actually a useful stalling pattern - it buys you a second to process the correction before you respond.

### Step 5: Soft ask handoff (Soft Request Handoff)

When Sangdon hands the Gaudi GPU topic to Tony, he uses a "we asked two inters for" formula.

| Language formula | Original | Function |
|:---|:---|:---|
| `we asked two inters for the future collaboration` | "we asked two inters for the future collaboration" | Frame as pre-existing ask, not new demand |
| `we had a collaboration about X previously` | "we had a collaboration about the performance testing previously" | Past collaboration as precedent |
| `we would like some collaboration about this AI system for the future` | "we would like some collaboration about this AI system for the future" | Future-collaboration ask |
| `we'd like to ask to some help` | "we'd like to ask to some help" | Soft ask - "ask to some help" (non-standard but functional) |

**Audrey lesson**: When bringing a new ask to a partner, frame it as a continuation: "we had a collaboration about X previously... we would like some collaboration about Y for the future." This pattern - **past precedent + future want** - makes a new request feel like relationship maintenance, not a cold ask. Even though "ask to some help" is grammatically non-standard, the pragmatic function is clear: it softens "we need help" into "we'd like to ask for some help."

---

## 2. Hedging & deflection strategies

This meeting's **real learning value**. Both sides deflect: SK Hynix hedges on the Gaudi ask specifics, Intel hedges on certification and on the Gaudi commitment.

### Strategy 1: Misunderstanding as deflection (Misunderstanding Claim)

When Sangdon's volume validation question gets challenged, he deflects by attributing it to misunderstanding.

| Situation | Original language | Translation |
|:---|:---|:---|
| Volume validation challenge | "I just uh know uh it's my misunderstanding so when CPU side started volume validation but uh I just wonder uh do we miss the your timeline" | "제가 오해한 부분이 있어서요, CPU 쪽에서 volume validation을 시작했는데 저희가 타임라인을 놓쳤나 해서요" |

**Pattern formula**: `It's my misunderstanding. I just wonder do we miss X.`

**Audrey lesson**: "It's my misunderstanding" is a face-saving deflection. Instead of "I was wrong," you say "I misunderstood." This preserves the relationship - the error was in interpretation, not in your engineering. Then "I just wonder" softens the follow-up. Use this when a partner corrects you in front of others.

### Strategy 2: Vague "some help" / "some collaboration" (Vague Request Hedging)

SK Hynix deflects on the specifics of the Gaudi ask by using "some" instead of quantities.

| Situation | Original language | Translation |
|:---|:---|:---|
| Gaudi request | "we would like some collaboration about this AI system" / "we'd like to ask to some help" / "if intel provided some this system to us we can work together" | "AI 시스템에 대해 some collaboration을" / "some help를 요청드리고 싶습니다" / "some system을 제공해주시면 같이 일할 수 있습니다" |

**Pattern formula**: `We would like some X. If you provide some Y, we can work together.`

**Audrey lesson**: "Some" is the hedge word for requests. "We want 8 Gaudi cards" is a hard ask. "We would like some collaboration" is a soft probe. You use "some" when you do not yet know what the partner will agree to - it lets the partner fill in the quantity. This is NOT weakness - it is opening the negotiation space. But note: Intel pushes back on this vagueness (see Section 3) - "some" only works as an opener, not as a plan.

### Strategy 3: First-stage framing (Early-Stage Framing)

SK Hynix frames the Gaudi work as "very first stage" to lower the stakes.

| Situation | Original language | Translation |
|:---|:---|:---|
| Performance unknown | "it's very first stage to us we don't know the how much performance improved or not because" | "저희에게는 아주 초기 단계라서 성능이 얼마나 개선될지 모릅니다" |
| Data gathering | "we're gathering some data pattern and they will compare the performance with the gpu or not" | "데이터 패턴을 모으고 있고 GPU 유무에 따른 성능을 비교할 예정입니다" |

**Pattern formula**: `It's very first stage to us. We don't know X because Y. We're gathering Z.`

**Audrey lesson**: "It's very first stage to us" is a humility marker that lowers expectations. When you ask a partner for hardware and they ask "what will you do with it," you say "it's very first stage" - this signals you are not promising results, you are exploring. This protects you from later accountability. Combine with "we're gathering some data" - "gathering" is exploratory, "measuring" is committed.

### Strategy 4: Certification refusal (Polite Refusal via "I don't believe")

Intel deflects the implicit certification request by using "I don't believe" instead of "we don't do."

| Situation | Original language | Translation |
|:---|:---|:---|
| CXL certification | "I don't believe that we do that for CXL... I don't believe we'll provide that... I wasn't aligned any certification today either" | "CXL에 대해 그런 건 하지 않는 걸로 알고 있습니다... 제공하지 않을 것으로... 인증 관련해서는 aligned 되어 있지 않습니다" |

**Pattern formula**: `I don't believe we do X. I don't believe we'll provide Y. Let me confirm and come back.`

**Audrey lesson**: "We don't do that" is blunt. "I don't believe we do that" leaves room - it is a refusal with a softener that says "this is my understanding, I could be wrong." This is how you refuse a partner's ask without burning the bridge. Note Jenny adds "but please jump in and let me know if I'm being correct here" - inviting correction. Then "we can go and confirm where we're at and come back" - defers the final no. This is professional refusal: **soft deny + offer to verify + defer**.

### Strategy 5: "Shopping list" deflection (Clarification-as-Deferral)

Intel Tony deflects the Gaudi commitment by reframing the ask as a "shopping list" that needs detail.

| Situation | Original language | Translation |
|:---|:---|:---|
| Gaudi ask | "I'd like to see what the shopping list is and let's talk about it" | "쇼핑 리스트가 뭔지 보고 이야기해 봅시다" |
| Card quantity probe | "is the request multiple cards do you have a minimum number of cards that you need to do the work" | "요청이 여러 카드인가요, 최소 몇 장이 필요한가요" |
| Software stack probe | "do you understand how you're going to change the software to access the kvcache mechanism when you run inference" | "추론 시 KV cache에 접근하기 위해 소프트웨어를 어떻게 바꿀지 이해하고 있습니까" |

**Pattern formula**: `I'd like to see what the shopping list is. Do you have a minimum number? Do you understand how you'll handle X?`

**Audrey lesson**: "Shopping list" is a brilliant deflection metaphor. Instead of saying "your request is too vague," Tony says "I'd like to see what the shopping list is" - playful but firm. This converts a refusal into a clarification request. When a partner asks you for something vague, do not say no - say "I'd like to see the shopping list" or "I need a better focus of what we're gonna complete." This buys time and forces the asker to do the work.

---

## 3. Polite challenge patterns

Intel uses polite but firm challenges to push back on SK Hynix's assumptions and vague asks. **These are patterns you will face when you ask a partner for something.**

### Challenge type 1: Context challenge (Context Question)

Intel challenges the volume validation question by asking for context, not by answering.

| Language formula | Original | Function |
|:---|:---|:---|
| `I don't know where the volume validation question comes from what is the context of it` | "I don't know where the volume validation question comes from what is the context of it" | "Where does this question come from" - challenges the premise |
| `why is the volume validation question coming up` | "why is why is the volume validation question coming up" | "Why is this coming up" - premise challenge |

**Audrey lesson**: When a partner asks a question based on a wrong assumption, the strongest response is "I don't know where that question comes from - what is the context?" This forces the asker to explain their reasoning, which often reveals the misunderstanding without you having to correct them directly. This is more powerful than saying "you're wrong" - it makes them self-correct.

### Challenge type 2: Comparative precedent (Comparative Precedent)

Intel uses Montage as a benchmark to explain why SK Hynix missed the power-on window.

| Language formula | Original | Function |
|:---|:---|:---|
| `Montage was they provided us hundreds of samples so we tested their card during the power on window` | "Montage was they provided us hundreds of samples so we tested their card during the power on window" | Comparative - "Montage did X, you did not" |
| `your device was not available at that time so you are not part of the power on window` | "your device was not available at that time so you are not part of the power on window" | Direct cause-effect - "not available, not part of" |

**Audrey lesson**: When correcting a partner, citing a competitor's behavior is a powerful tool. "Montage provided hundreds of samples, so we tested their card" - this is a factual comparison that explains the consequence without attacking. "Your device was not available, so you are not part of X" - cause and effect, not blame. Use this structure when you need to explain why a partner missed a window: **"X did Y, so Z happened. You did not, so W."**

### Challenge type 3: Clarification probe (Clarification Probe)

Intel Tony pushes the Gaudi ask from "some cards" to "what exactly."

| Language formula | Original | Function |
|:---|:---|:---|
| `is the request multiple cards do you have a minimum number of cards` | "is the request multiple cards do you have a minimum number of cards that you need to do the work" | Quantity probe |
| `are you looking for the whole setup the host server the gpu the head node everything` | "are you looking for the whole setup the hopes server the gpu the head node everything" | Scope probe - "the whole setup" |
| `do you understand how you're going to change the software` | "do you understand how you're going to change the software to access the kvcache mechanism" | Capability probe |
| `what's the expectation of involvement is it just this is first level` | "what's the what's the expectation of involvement is it just this is first level you already have everything set up" | Expectation probe |

**Audrey lesson**: When a partner makes a vague ask, you challenge by asking a **series of specific questions**: how many, what scope, do you have the capability, what is the expectation. Each question narrows the ask. This is "funnel questioning" - start broad ("what's the expectation of involvement"), end narrow ("do you have a minimum number of cards"). Memorize this sequence - it is how you turn a vague request into an actionable plan without saying no.

### Challenge type 4: Scope-narrowing (Scope Narrowing)

Intel Tony narrows the SK Hynix picture from "complicated" to "just the red box."

| Language formula | Original | Function |
|:---|:---|:---|
| `the picture is complicated... it's not complicated it's overloaded` | "but it's not just it's not complicated it's overloaded it's overloaded" | Reframe - "not complicated, overloaded" |
| `what we're talking about here really we're just talking about the KV cache model right` | "what we're talking about here really we're just talking about the KV cache model right" | Scope narrowing with tag question |
| `I just wanted to make sure because the picture is complicated` | "I just wanted to make sure because the picture is complicated" | "I just wanted to make sure" - clarification preface |

**Audrey lesson**: "I just wanted to make sure because the picture is complicated" is a polite way to say "your slide is too messy, let's narrow it." Then "we're just talking about X, right?" - the tag question "right?" forces confirmation and narrows scope. This is how you redirect a meeting that is drifting: **preface + reframe + tag question**. "I just wanted to make sure... we're just talking about X, right?"

### Challenge type 5: Software-as-key pushback (Software-as-Key Pushback)

Intel Tony challenges the Gaudi ask by elevating "software" as the real complexity.

| Language formula | Original | Function |
|:---|:---|:---|
| `sometimes the software is the key piece` | "sometimes the software is the key piece" | Elevates software as the real issue |
| `software is like a big word... it's a big ticket item` | "software is like a big word yeah it's a big ticket item" | "Big ticket item" - signals cost/complexity |
| `we're gonna have to expand on that point` | "we're gonna have to expand on that point" | "Expand on that point" - demand for detail |

**Audrey lesson**: When a partner asks for hardware, reframe the ask as a software problem. "The software is the key piece" - this shifts the conversation from "will you give us cards" to "do you have the software capability." This is a polite pushback because it implies the asker has not thought through the hard part. "Big ticket item" is an American business idiom meaning "expensive/complex item" - use it to signal that something is not trivial.

---

## 4. Negotiation & action item language (Section 4 - KEY for Type C)

This is the core learning for schedule coordination meetings. Timeline targets, sample-type language, milestone coordination, alignment, and next-step commitments.

### 4.1 Schedule / milestone language

| Language formula | Speaker | Original | Function |
|:---|:---:|:---|:---|
| ES sample at end of Q3 | SK | "SK hynix may support the ES sample rap maybe end of q3 2026" | ES (Engineering Sample) timing |
| CS candidate / CS level | SK | "it's already CS candidate pomeo which we expect" / "the pomeo is already CS level" | CS (Customer Sample) milestone |
| MP / production in Q2/Q3 | Intel | "the qs to be in q2 q3 27 in production" / "production june which actually this should be right" | MP / production timing |
| QS to production in two months | SK | "you're gonna make some short timeline between qs and production just two months" | QS-to-MP gap probe |
| 12 channel and 16 channel | Intel | "you have the 12 channel dmr also... 12 and 16 correct" | Spec confirmation |
| Power on early November | Intel | "we completed our power on I think early November something like that" | Milestone past-tense - "completed" |
| Pushed out two months | SK | "the cmm schedule pushed out two months" | Delay disclosure |
| GNR first PDKs Q1/early Q2 | Intel | "the first pdk's so qs is right here... mid april possibly to august" | PDK timing |

**Audrey lesson**: Schedule coordination meetings use a **fixed vocabulary set**: ES, CS, MP, QS, PDK, power-on, volume validation, production qualification, launch. You must use these abbreviations fluently - do not spell them out. "ES at end of Q3, CS candidate, MP by late Q2" - this is how a schedule is stated in English. The verb "support" is used for giving samples ("we support the ES sample"), "receive" for getting them ("you receive the system"). Memorize this verb pairing.

### 4.2 Alignment language

| Language formula | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Align our schedule with your schedule | SK | "we want to just trying to align our the our schedule with your schedule and see whether it is aligning or not" | Core alignment ask |
| Are we missing your launch | SK | "is this timeline is good or are we missing missing your your launch" | Risk-voice alignment probe |
| Both sides almost the same pace | Intel | "looks like we are both sides almost the same pace that means a result observed in in our side as well as intel size is aligned" | "Aligned" - confirmation of alignment |
| Cross check | SK | "so let's cross check" | "Cross check" - mutual verification |
| Stack alignment | SK | "we need a stack stack alignment" / "we need to understand each other stack" | Technical alignment request |
| We are both sides aligned | Intel | "both team can share result once they have the more debugging time" | "Both teams can share" - alignment confirmation |

**Audrey lesson**: "Align" is THE verb of schedule meetings. "We want to align our schedule with yours" - memorize this. Then "are we missing your launch" is the risk probe that forces the partner to reveal their true timeline. And "stack alignment" extends this to technical compatibility - "we need to understand each other's stack." Use "align" for schedule, "stack alignment" for technical compatibility.

### 4.3 Sample / quantity negotiation

| Language formula | Speaker | Original | Function |
|:---|:---:|:---|:---|
| 20 cars (samples) sent | Intel | "now that you have sent us 20 cars we have started testing that in our lab" | "Cars" = "cards" (samples) - Intel usage |
| Hundreds of samples | Intel | "Montage was they provided us hundreds of samples" | Comparative quantity |
| At least eight cars | SK | "I believe at least you need eight cars but" / "we looking like eight cars like a whole system at least like eight car system" | Minimum quantity statement |
| Minimum number of cards | Intel | "do you have a minimum number of cards that you need to do the work" | Quantity probe |
| One card first approach | SK | "just a single of gpu card will be okay so one cpu plus with the one Gaudi gpu card" | Minimum viable ask - "one card first" |

**Audrey lesson**: Note "cars" in the transcript is a transcription error for "cards" (CXL memory cards / Gaudi cards). The quantity negotiation pattern: **start with minimum, expand to full system.** "One card first... then eight cards for the whole system." This is how you ask for hardware: start small ("one card will be okay"), then state the full need ("at least eight for the whole system"). This shows you are reasonable and have thought through the scaling.

### 4.4 Action items & next steps

| Language formula | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Give me one maybe two weeks | Intel | "give me give me one maybe two weeks to understand" | Time-bound commitment |
| Go and understand on your side | Intel | "go and understand on your side if you could explain to us a little more of what flows you're interested in" | Mutual homework assignment |
| Let's align then | Intel | "let's let's align then so go and go and understand on your side" | "Let's align then" - action trigger |
| I'll look at the same on my side | Intel | "I'll look at the same on my side" | Parallel work commitment |
| Step one / step two framing | Intel | "step one is the one card and then it's what we are going to do... step two would be like a multiple cards" | Phased plan - "step one... step two" |
| We'll work with you if you see any host related issues | Intel | "we'll work with you if if you see any host related issues based on your testing" | Conditional support offer |
| Next step probably we need to bring system software engineers | SK | "I think the next step probably we need to bring sign down maybe we need to bring system software or engineers" | "Next step probably we need to bring X" - resource escalation |
| Let's keep discuss about this one | SK | "any question or or as kni sweep uh more clear about the red box and and then uh let's keep discuss about this one" | "Let's keep discuss" - continuation commitment |

**Audrey lesson**: Action items in English meetings use **time-boxed commitments + parallel work.** "Give me one maybe two weeks" - the "maybe" softens but the "one to two weeks" is the commitment. "I'll look at the same on my side" - parallel work, not blocking. "Step one is X, step two is Y" - phased planning. Memorize this pattern: **time-box + parallel work + phased steps.** And "let's align then" is the trigger that converts discussion into action.

### 4.5 Soft "ask for help" language

| Language formula | Speaker | Original | Function |
|:---|:---:|:---|:---|
| We'd like to ask to some help | SK | "we'd like to ask to some help" | Soft ask |
| If intel provided some this system to us we can work together | SK | "if inter provided some this system to us we can uh work together in inter side" | Conditional collaboration - "if you provide X, we can Y" |
| We'd like to ask to lend that one | SK | "we'd like to ask to lend that one or we can collaborate this work together" | "Lend" - temporary hardware ask |
| Could you provide us some Gaudi card and system | SK | "could you provide us uh some Gaudi card and system" | Direct but softened with "some" |
| I really wanted to Intel's help | SK | "What that's great yeah I really wanted to Intel's help" | Direct appreciation of help offer |

**Audrey lesson**: "Lend" is the key word for temporary hardware asks. "We'd like to ask to lend that one" - this signals you want to borrow, not own. This lowers the partner's commitment. Combined with "if you provide X, we can work together" - this is a barter frame: you get hardware, partner gets collaboration data. Use "lend" when you want to test hardware, "provide" when you want to keep it.

---

## 5. Domain vocabulary (with exact usage context)

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **CMM** (CXL Memory Module) | SK Hynix's CXL memory module | "the scanning second gen CMM in Intel site" - second gen CMM under test |
| **ES** (Engineering Sample) | Early prototype sample for engineering validation | "SK hynix may support the ES sample at the end of q3 2026" - ES is the earliest sample type |
| **CS** (Customer Sample) | Sample sent to customer for evaluation | "it's already CS candidate pomeo which we expect" / "the pomeo is already CS level" - CS is post-ES |
| **MP** (Mass Production) | Volume production milestone | "in production" - MP is referred to as "production" |
| **QS** (Qualification Sample) | Sample for qualification testing | "the qs to be in q2 q3 27 in production" - QS precedes production |
| **PDK** (Process Design Kit) | Intel's process design kit for chip design | "if we get the the upstream PDK so yeah we can we will try to do that" - "upstream PDK" |
| **GNR** (Granite Rapids) | Intel server CPU generation | "Yeah we have a GNR" / "the GNR white paper collaboration" |
| **DMR** | Intel memory reference platform | "not only the dm" / "12 channel dmr" / "16 channel" - DMR is the test platform |
| **Power-on** | Initial silicon/board bring-up validation | "we completed our power on I think early November" - power-on is a completed milestone |
| **Volume validation** | Post-power-on large-scale validation | "after the power on window it goes to the volume validation" - volume validation follows power-on |
| **Johnson City** (JCY) | Intel validation lab location | "when you receive the systems right Johnson city" / "when you get your johnson city" |
| **TMR** | Timeline/Milestone Roadmap (contextual) | "we can update the new intel tmr's the timeline" - TMR used as timeline reference |
| **Bring up** | Hardware initial boot validation | "we expect engineering samples and bring up" - bring up = initial validation |
| **Montage** | Competitor CXL vendor (Montage Technology) | "Montage was they provided us hundreds of samples" - comparative benchmark |
| **Loopback** | Self-loop testing mode | "any testing would be done with like loop for" - loopback test |
| **Memtier** | Memory benchmark tool (memtier_benchmark) | "you create a single memtier instance pointing to a specific Redis server" |
| **Redis server** | In-memory database for CXL testing | "create 86 Redis server and they have a memtier client pointing to each server" |
| **KV cache** | LLM key-value cache (use case for CXL) | "storing your KV cache in your cxl node" - CXL as KV cache tier |
| **Gaudi** | Intel's AI/ML GPU accelerator | "intel has a GPU card which called Gaudi" / "one Gaudi gpu card" |
| **Snapshot** | Intel's roadmap revision document | "the snapshot was available" / "this is what was in the snapshot that the email I sent you" |
| **Shopping list** | Metaphor for detailed request list | "I'd like to see what the shopping list is and let's talk about it" |
| **Stack** | Software/hardware stack | "we need to understand each other stack" / "stack alignment" |
| **Big ticket item** | American idiom - expensive/complex item | "software is like a big word yeah it's a big ticket item" |
| **Red box** | Visual reference to scope in slide | "just like a red box only" - narrowing scope to one element |
| **Pull-in / Push-out** | Schedule move earlier / later | "the cmm schedule pushed out two months" - push-out = delay |
| **Cross check** | Mutual verification of results | "so let's cross check" |

---

## 6. Expression DB (Expression Database)

48 expressions with pragmatic value from this meeting. Each tagged with category, function, speaker role, difficulty (1-5), context, pattern, note.

```yaml
# -- Schedule alignment (Schedule Coordination) --
- id: m30-001
  expression: "we want to just trying to align our schedule with your schedule and see whether it is aligning or not"
  category: schedule_alignment
  function: alignment_intent
  speaker_role: sk_lead
  difficulty: 4
  context: "we want to just trying to align our the our schedule with your schedule and see whether it is aligning or not"
  pattern: "we want to align our schedule with your schedule and see whether it is aligning or not"
  note: THE core schedule alignment sentence. Use this to frame every timeline question as coordination, not pressure.

- id: m30-002
  expression: "we'd like to know the schedule so we can update the new intel tmr's the timeline"
  category: schedule_alignment
  function: reason_for_ask
  speaker_role: sk_lead
  difficulty: 3
  context: "we'd like to know the schedule so we can update the new intel tmr's the timeline for the timeline which is the highlighted red dot box"
  pattern: "we'd like to know X so we can update Y"
  note: Stating the reason for your ask - "so we can update" justifies the question.

- id: m30-003
  expression: "is this timeline is good or are we missing your launch"
  category: schedule_risk_probe
  function: risk_voice_alignment
  speaker_role: sk_lead
  difficulty: 4
  context: "is this timeline is is good or are we missing missing your your launch"
  pattern: "is this timeline good or are we missing your launch"
  note: "Are we missing your launch" is the risk-voice probe. Shows worry, forces honest answer.

- id: m30-004
  expression: "we would like to know how much the does intel lead the for the validation sample"
  category: partner_timeline_probe
  function: lead_time_inquiry
  speaker_role: sk_lead
  difficulty: 4
  context: "we would like collaboration with Intel what what uh how much the does intel lead the for the validation sample"
  pattern: "we would like to know how much does intel lead for X"
  note: "How much does Intel lead" - probing partner's lead time for sample preparation.

- id: m30-005
  expression: "looks like we are both sides almost the same pace that means a result observed in in our side as well as intel size is aligned"
  category: alignment_confirmation
  function: aligned_confirmation
  speaker_role: intel
  difficulty: 3
  context: "I think the good news is looks like we are both sides almost the same pace that means a result observed in in our side as well as intel size is aligned"
  pattern: "both sides almost the same pace... results are aligned"
  note: "Aligned" - the confirmation word. When results match, say "we are aligned."

- id: m30-006
  expression: "so let's cross check"
  category: mutual_verification
  function: verification_trigger
  speaker_role: either
  difficulty: 2
  context: "so yeah we can we will try to do that yeah so let's cross check yeah"
  pattern: "let's cross check"
  note: "Cross check" - mutual verification commitment. Short, actionable.

# -- Sample / milestone language --
- id: m30-007
  expression: "SK hynix may support the ES sample at the end of q3 2026"
  category: sample_milestone
  function: es_timing
  speaker_role: sk_lead
  difficulty: 3
  context: "as kianics support the ESS or ES sample rap uh maybe end of q3 2026"
  pattern: "we may support the ES sample at the end of QX YYYY"
  note: ES (Engineering Sample) timing statement. "Support" is the verb for providing samples.

- id: m30-008
  expression: "it's already CS candidate pomeo which we expect"
  category: sample_milestone
  function: cs_level_statement
  speaker_role: sk_lead
  difficulty: 3
  context: "but it's already CS candidate pomeo which we expect"
  pattern: "it's already CS candidate"
  note: CS (Customer Sample) milestone. "CS candidate" = being considered for CS status.

- id: m30-009
  expression: "the cmm schedule pushed out two months"
  category: schedule_delay
  function: delay_disclosure
  speaker_role: sk_lead
  difficulty: 3
  context: "as SK hynix the cmm schedule pushed out two months yeah so unfortunately"
  pattern: "the X schedule pushed out N months"
  note: "Pushed out" = delayed. Direct disclosure formula.

- id: m30-010
  expression: "you're gonna make some short timeline between qs and production just two months"
  category: milestone_gap_probe
  function: gap_question
  speaker_role: sk_lead
  difficulty: 4
  context: "you you're gonna make some short timeline between qs and production just two months is that uh clear"
  pattern: "you're gonna make a short timeline between X and Y just N months"
  note: Probing the gap between milestones. "Short timeline between X and Y" - gap analysis.

- id: m30-011
  expression: "we completed our power on I think early November something like that"
  category: milestone_past
  function: completed_milestone
  speaker_role: intel
  difficulty: 2
  context: "right now in we are in December right we completed our power on I think early November something like that"
  pattern: "we completed our X I think early November something like that"
  note: Past-tense milestone with hedging - "I think... something like that" softens the date.

- id: m30-012
  expression: "the qs to be in q2 q3 27 in production"
  category: mp_timing
  function: production_timeline
  speaker_role: intel
  difficulty: 3
  context: "the schedule shows um the qs to be in q2 q3 27 in production"
  pattern: "the QS to be in Q2 Q3 YY in production"
  note: QS and MP timing in one sentence. Note "in production" = MP.

- id: m30-013
  expression: "between q1 and q2 of next year you're good to go"
  category: timeline_commitment
  function: go_signal
  speaker_role: intel
  difficulty: 3
  context: "the bottom line is if you get Jonathan said a between q1 and q2 of next year you're you're good to go"
  pattern: "between Q1 and Q2 of next year you're good to go"
  note: "You're good to go" - the green light signal. Use this to confirm a timeline.

# -- Misunderstanding recovery --
- id: m30-014
  expression: "it's my misunderstanding"
  category: misunderstanding_recovery
  function: face_saving_admission
  speaker_role: sk_lead
  difficulty: 5
  context: "I just uh know uh it's my misunderstanding so when CPU side started volume validation"
  pattern: "it's my misunderstanding"
  note: Cleanest recovery from being wrong. "Misunderstanding" attributes error to interpretation, not competence. MEMORIZE.

- id: m30-015
  expression: "I just wonder uh do we miss the your timeline"
  category: soft_probe
  function: softened_question
  speaker_role: sk_lead
  difficulty: 4
  context: "I just wonder uh do we miss the your timeline but because I don't know where about that"
  pattern: "I just wonder do we miss X"
  note: "I just wonder" softens any question. Use before a potentially embarrassing question.

- id: m30-016
  expression: "I don't know where about that"
  category: knowledge_gap
  function: admission
  speaker_role: sk_lead
  difficulty: 2
  context: "I don't know where about that"
  pattern: "I don't know where about that"
  note: Non-standard but functional. Standard version: "I'm not sure about that."

- id: m30-017
  expression: "Okay okay okay I understand that"
  category: acknowledgment
  function: correction_acknowledgment
  speaker_role: sk_lead
  difficulty: 2
  context: "Okay okay okay I understand that yeah hopefully that clarifies right"
  pattern: "Okay okay okay I understand that"
  note: Triple "okay" buys processing time. Then "I understand that" closes the loop.

- id: m30-018
  expression: "hopefully that clarifies right"
  category: confirmation_check
  function: partner_confirmation
  speaker_role: intel
  difficulty: 3
  context: "hopefully that clarifies right yeah yeah"
  pattern: "hopefully that clarifies right"
  note: Partner's check after correcting you. "That clarifies" = the confusion is resolved.

# -- Polite challenge / pushback --
- id: m30-019
  expression: "I don't know where the volume validation question comes from what is the context of it"
  category: premise_challenge
  function: context_demand
  speaker_role: intel
  difficulty: 5
  context: "I don't know where the volume validation question comes from what is the context of it"
  pattern: "I don't know where the X question comes from what is the context of it"
  note: Strongest polite challenge. Forces asker to reveal their (wrong) reasoning. MEMORIZE.

- id: m30-020
  expression: "Montage was they provided us hundreds of samples so we tested their card during the power on window"
  category: comparative_precedent
  function: competitor_benchmark
  speaker_role: intel
  difficulty: 5
  context: "Montage was they provided us hundreds of samples so we tested their card during the power on window"
  pattern: "X provided us hundreds of samples so we tested their card during Y"
  note: Citing a competitor as benchmark. Factual, not attacking. Explains consequence.

- id: m30-021
  expression: "your device was not available at that time so you are not part of the power on window"
  category: cause_effect_correction
  function: factual_correction
  speaker_role: intel
  difficulty: 4
  context: "your device was not available at that time so you are not part of the power on window"
  pattern: "your device was not available at that time so you are not part of X"
  note: Cause-effect correction. "Not available, not part of" - no blame, just fact.

- id: m30-022
  expression: "I don't believe that we do that for CXL"
  category: polite_refusal
  function: soft_deny
  speaker_role: intel
  difficulty: 4
  context: "I don't believe that we do that for cxl but please um for those jump in and let me know if I'm being correct here"
  pattern: "I don't believe that we do that for X"
  note: "I don't believe" is a soft refusal. Leaves room for correction.

- id: m30-023
  expression: "please jump in and let me know if I'm being correct here"
  category: invite_correction
  function: openness_signal
  speaker_role: intel
  difficulty: 4
  context: "please um for those jump in and let me know if I'm being correct here"
  pattern: "please jump in and let me know if I'm being correct here"
  note: Invites colleagues to correct you. Signals openness while stating position.

- id: m30-024
  expression: "we can go and confirm where we're at and confirm that there's nothing new that happened and come back"
  category: deferred_refusal
  function: verify_and_return
  speaker_role: intel
  difficulty: 4
  context: "what we can do which is go and confirm where we're at and confirm that there's nothing new that happened and come back"
  pattern: "we can go and confirm where we're at and come back"
  note: Defers the final no. "Confirm and come back" - soft refusal with verification promise.

# -- Clarification probe (Intel Tony on Gaudi ask) --
- id: m30-025
  expression: "I'd like to see what the shopping list is and let's talk about it"
  category: clarification_deflection
  function: detail_demand
  speaker_role: intel
  difficulty: 5
  context: "I think for the next step i'd like to to see what the shopping list is and let's talk about it"
  pattern: "I'd like to see what the shopping list is and let's talk about it"
  note: "Shopping list" metaphor converts a vague ask into a homework assignment for the asker. Brilliant deflection.

- id: m30-026
  expression: "is the request multiple cards do you have a minimum number of cards that you need to do the work"
  category: quantity_probe
  function: funnel_question
  speaker_role: intel
  difficulty: 4
  context: "is the request multiple cards do you have a minimum number of cards that you need to do the work"
  pattern: "is the request X do you have a minimum number of Y"
  note: Funnel question - narrows from "some" to a specific minimum.

- id: m30-027
  expression: "are you looking for the whole setup the host server the gpu the head node everything"
  category: scope_probe
  function: scope_narrowing
  speaker_role: intel
  difficulty: 4
  context: "is your ask just for the gpu card the Gaudi are you looking for the whole setup the hopes server the gpu the head node everything"
  pattern: "are you looking for the whole setup the X the Y the Z everything"
  note: Scope probe - "the whole setup... everything" lists scope options to force a choice.

- id: m30-028
  expression: "what's the expectation of involvement is it just this is first level"
  category: expectation_probe
  function: involvement_check
  speaker_role: intel
  difficulty: 5
  context: "what's the what's the expectation of involvement is it just this is first level you already have everything set up in your lab"
  pattern: "what's the expectation of involvement is it just first level"
  note: "Expectation of involvement" - the key phrase. Asks partner to define their ask precisely.

- id: m30-029
  expression: "do you understand how you're going to change the software to access the kvcache mechanism"
  category: capability_probe
  function: capability_check
  speaker_role: intel
  difficulty: 5
  context: "do you understand how you're going to change the software to access the kvcache mechanism when you run inference are you familiar with that"
  pattern: "do you understand how you're going to change X to access Y"
  note: Capability probe - "do you understand how" challenges the asker's readiness.

- id: m30-030
  expression: "sometimes the software is the key piece"
  category: reframe
  function: complexity_elevation
  speaker_role: intel
  difficulty: 4
  context: "because i mean that's when you talk about this stuff sometimes the software is the key piece"
  pattern: "sometimes the software is the key piece"
  note: Reframes a hardware ask as a software problem. Polite pushback.

- id: m30-031
  expression: "software is like a big word yeah it's a big ticket item"
  category: idiom
  function: complexity_signal
  speaker_role: intel
  difficulty: 4
  context: "because software is like a big word yeah it's a big ticket item"
  pattern: "X is a big ticket item"
  note: "Big ticket item" = expensive/complex. American business idiom. Signals something is not trivial.

# -- Scope narrowing --
- id: m30-032
  expression: "I just wanted to make sure because the picture is complicated"
  category: clarification_preface
  function: polite_narrow
  speaker_role: intel
  difficulty: 4
  context: "I just wanted to make sure because the picture is complicated"
  pattern: "I just wanted to make sure because X is complicated"
  note: Polite way to say "your slide is too messy." Preface before narrowing.

- id: m30-033
  expression: "what we're talking about here really we're just talking about the KV cache model right"
  category: scope_narrow
  function: tag_confirm
  speaker_role: intel
  difficulty: 4
  context: "what we're talking about here really we're just talking about the KV cache model right of this of this picture"
  pattern: "what we're talking about here really we're just talking about X right"
  note: "Right?" tag forces confirmation and narrows scope. Redirect drifting meetings.

- id: m30-034
  expression: "it's not complicated it's overloaded"
  category: reframe
  function: precise_correction
  speaker_role: intel
  difficulty: 4
  context: "but it's not just it's not complicated it's overloaded it's overloaded"
  pattern: "it's not X it's Y"
  note: Precise word correction. "Not complicated, overloaded" - sharper than accepting "complicated."

# -- Soft ask (SK Hynix Gaudi request) --
- id: m30-035
  expression: "we had a collaboration about X previously... we would like some collaboration about Y for the future"
  category: precedent_request
  function: past_plus_future
  speaker_role: sk_lead
  difficulty: 4
  context: "we had a collaboration about the uh performance testing previously uh but uh inter has a GPU card which called Gaudi and uh we would like uh some collaboration about this AI system uh for the future"
  pattern: "we had a collaboration about X previously... we would like some collaboration about Y for the future"
  note: Past precedent + future want. Makes a new ask feel like relationship maintenance.

- id: m30-036
  expression: "we'd like to ask to some help"
  category: soft_ask
  function: help_request
  speaker_role: sk_lead
  difficulty: 2
  context: "we'd like to ask to some help"
  pattern: "we'd like to ask to some help"
  note: Non-standard grammar but functional. Standard: "we'd like to ask for some help."

- id: m30-037
  expression: "if intel provided some this system to us we can work together"
  category: conditional_collaboration
  function: barter_frame
  speaker_role: sk_lead
  difficulty: 4
  context: "if uh inter provided some this system to us we can uh work together in inter side"
  pattern: "if you provide X to us we can work together"
  note: Barter frame - "you give hardware, we give collaboration data."

- id: m30-038
  expression: "we'd like to ask to lend that one or we can collaborate this work together"
  category: lend_request
  function: borrow_ask
  speaker_role: sk_lead
  difficulty: 4
  context: "we'd like to ask to lend that one or we can collaborate this work together"
  pattern: "we'd like to ask to lend X or we can collaborate"
  note: "Lend" signals temporary borrow, not ownership. Lowers partner commitment.

- id: m30-039
  expression: "just a single of gpu card will be okay so one cpu plus with the one Gaudi gpu card"
  category: minimum_viable_ask
  function: small_start
  speaker_role: sk_lead
  difficulty: 3
  context: "I mean just a single of gpu card will be okay so one cpu plus with the one Gaudi gpu card"
  pattern: "just a single X will be okay so one Y plus one Z"
  note: Minimum viable ask. Start small to show reasonableness.

- id: m30-040
  expression: "I believe at least you need eight cars but"
  category: full_system_quantity
  function: full_need_statement
  speaker_role: sk_lead
  difficulty: 3
  context: "I believe at least you need eight cars but but yeah probably you need to exactly"
  pattern: "I believe at least you need eight cards"
  note: "Cars" = transcription error for "cards." Full system need after minimum ask.

# -- Early-stage hedging --
- id: m30-041
  expression: "it's very first stage to us we don't know the how much performance improved or not"
  category: early_stage_framing
  function: humility_marker
  speaker_role: sk_lead
  difficulty: 4
  context: "it's very first stage to us we don't know the how much performance improved or not because"
  pattern: "it's very first stage to us we don't know X"
  note: Lowers expectations. Signals exploration, not commitment. Protects from later accountability.

- id: m30-042
  expression: "we're gathering some data pattern and they will compare the performance with the gpu or not"
  category: exploratory_work
  function: gathering_frame
  speaker_role: sk_lead
  difficulty: 3
  context: "our the system engineer will we're gathering some data pattern and they will compare the performance with the gpu or not"
  pattern: "we're gathering some X and will compare Y"
  note: "Gathering" is exploratory, "measuring" is committed. Use "gathering" when you are not yet sure.

# -- Action items / next steps --
- id: m30-043
  expression: "give me give me one maybe two weeks to understand"
  category: time_boxed_commitment
  function: soft_deadline
  speaker_role: intel
  difficulty: 3
  context: "give me give me um i don't know give me give me one maybe two weeks to understand"
  pattern: "give me one maybe two weeks to understand"
  note: Time-box with "maybe" softener. "One to two weeks" is the commitment.

- id: m30-044
  expression: "let's align then so go and understand on your side"
  category: action_trigger
  function: parallel_homework
  speaker_role: intel
  difficulty: 4
  context: "let's let's align then so go and go and understand on your side if you could explain to us a little more of what flows you're interested in"
  pattern: "let's align then so go and understand on your side"
  note: "Let's align then" is the trigger that converts discussion to action. Then parallel homework.

- id: m30-045
  expression: "I'll look at the same on my side"
  category: parallel_work
  function: mirrored_commitment
  speaker_role: intel
  difficulty: 3
  context: "I'll look at the same on my side it could be that i have engineers in a lab with Gaudi's"
  pattern: "I'll look at the same on my side"
  note: Parallel work commitment. "On my side" - mirrored accountability.

- id: m30-046
  expression: "step one is the one card and then step two would be like a multiple cards"
  category: phased_plan
  function: step_breakdown
  speaker_role: either
  difficulty: 3
  context: "like a step one is the one card and then it's what we are going to do and then step two would be like a multiple cards"
  pattern: "step one is X and then step two would be like Y"
  note: Phased plan. "Step one... step two" - shows progression without overcommitting.

- id: m30-047
  expression: "we'll work with you if you see any host related issues based on your testing"
  category: conditional_support
  function: support_offer
  speaker_role: intel
  difficulty: 3
  context: "we'll work with you if if you see any host related issues based on your testing"
  pattern: "we'll work with you if you see any X based on your Y"
  note: Conditional support. "If you see X" - Intel commits only if issues arise.

- id: m30-048
  expression: "we need to understand each other stack"
  category: technical_alignment
  function: stack_alignment
  speaker_role: either
  difficulty: 3
  context: "we need to understand each other stack what is our plan and what and where intel can can help"
  pattern: "we need to understand each other's stack"
  note: "Stack alignment" - extends schedule alignment to technical compatibility.
```

---

## 7. Excerpt map (Excerpt Map for Shadowing)

Audio: `repo/webex-audio/2025-12-05 09 18 29_EN_INTEL-extracted.wav` (83MB, ~5,290 words)
Recommended 5 excerpts for Mon-Fri shadowing. Each ~1-2 minutes.

**Note on segmentation**: The transcript was flagged for abnormally long sentence segments (avg 159.7 chars). Line numbers below refer to the corrected transcript's line numbering. Segments are run-on (multiple sentences merged per line) - when shadowing, split at the sentence boundaries marked below, not at line breaks.

| # | Time (est.) | Line range | Content summary | Learning point | Shadowing difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 00:00-02:00 | line 1-16 | Bandwidth scaling debug status + "both sides almost the same pace... aligned" + "let's cross check" | Status touchback + alignment confirmation | ★★☆ |
| 2 | 02:00-06:00 | line 36-50 | CMM schedule pushed out 2 months + ES/CS/MP timeline + "we want to align our schedule with your schedule" | Schedule alignment language (KEY) | ★★★★ |
| 3 | 06:00-10:00 | line 42-60 | Volume validation misunderstanding + "it's my misunderstanding" + Intel correction with Montage precedent | Misunderstanding recovery + polite correction | ★★★★★ |
| 4 | 10:00-16:00 | line 84-100 | Gaudi collaboration request + "we had a collaboration previously... we would like some collaboration" + Intel "what's the expectation of involvement" | Soft ask + clarification probe (KEY) | ★★★★ |
| 5 | 16:00-20:00 | line 124-145 | "Shopping list" + "step one is one card, step two is multiple cards" + "give me one maybe two weeks" + "let's align then" | Action items + phased plan | ★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, ... Fri: Excerpt 5
- Insert into daily routine (20 min) sections 1-6
- Excerpts 2, 3, 4 are highest value - schedule alignment, misunderstanding recovery, and soft ask are the core Type C patterns

---

## 8. Audrey's teaching notes

### Register (style) analysis
This meeting is **schedule coordination + soft ask** register. Two distinct modes:
- **Schedule mode** (Sangdon lead): "we want to align our schedule with your schedule" - direct, time-bound, milestone vocabulary (ES/CS/MP), risk probes ("are we missing your launch")
- **Soft-ask mode** (Tony lead): "we'd like to ask to some help" / "if you provide some system, we can work together" - hedged, "some" instead of quantities, "lend" instead of "provide", early-stage framing

You must learn both modes: schedule mode for timeline coordination, soft-ask mode for requesting partner resources.

### Pragmatics (pragmatics) core
1. **"Align" is the master verb**: "We want to align our schedule with your schedule" frames every question as joint planning. Memorize this - it converts intrusive questions into coordination.
2. **"It's my misunderstanding" recovery**: When wrong, do not over-apologize. "It's my misunderstanding" attributes the error to interpretation. Then "Okay, I understand that" closes the loop.
3. **"Shopping list" deflection**: When asked vaguely, respond with "I'd like to see what the shopping list is" - this converts refusal into a clarification request.
4. **"Some" as hedge opener**: "We would like some collaboration" opens negotiation space. But it only works as an opener - the partner will push for specifics ("how many cards?").
5. **Comparative precedent**: "Montage provided hundreds of samples" - citing a competitor's behavior explains a consequence without attacking. Use this to explain why a partner missed a window.

### Top 5 you must use now
1. **"We want to align our schedule with your schedule and see whether it is aligning or not"** - the core schedule alignment sentence
2. **"It's my misunderstanding"** - cleanest recovery from being wrong
3. **"I'd like to see what the shopping list is and let's talk about it"** - clarification-as-deferral
4. **"We had a collaboration about X previously... we would like some collaboration about Y for the future"** - soft ask with precedent
5. **"Give me one maybe two weeks to understand"** - time-boxed commitment with softener

### Korean vs English comparison
| Korean | English (this meeting) | Difference |
|:---|:---|:---|
| "일정 맞춰보고 싶습니다" | "we want to align our schedule with your schedule and see whether it is aligning or not" | English states the intent explicitly - "align" is the verb |
| "제가 오해했습니다" | "it's my misunderstanding" | English uses noun form ("misunderstanding") not verb ("I misunderstood") - less personal |
| "도움 좀 부탁드립니다" | "we'd like to ask to some help" / "we'd like to ask to lend that one" | English uses "lend" for temporary, "provide" for permanent |
| "검토하고 다시 연락드리겠습니다" | "we can go and confirm where we're at and come back" | English specifies "where we're at" - status check, not generic "review" |
| "언제쯤 가능한가요?" | "is this timeline good or are we missing your launch" | English adds risk-voice - "are we missing your launch" shows worry |
| "몇 개가 필요하세요?" | "do you have a minimum number of cards that you need to do the work" | English specifies "minimum number" + "to do the work" - purpose-linked quantity |
| "단계적으로 하죠" | "step one is the one card and then step two would be like a multiple cards" | English numbers the steps explicitly |

---

## 9. How to use this textbook

1. **Daily 20-min routine**: Use Section 7's 5 excerpts, Mon-Fri rotation
2. **Expression DB**: From Section 6's 48 expressions, prioritize Section 8's Top 5 first
3. **Audrey Friday correction**: Focus on Section 4 (schedule alignment) and Section 2 (hedging) for dump writing
4. **Comparison learning**: Use Section 8's Korean-English comparison table to internalize the differences

### Limitations (S9)
- **Transcript segmentation issue**: The source transcript was flagged for abnormally long sentence segments (avg 159.7 chars). Lines are run-on - multiple sentences merged per line. For excerpt mapping (Section 7), split at sentence boundaries (period+space), not at line breaks. Line numbers are preserved for traceability but do not correspond to sentence units.
- **Transcription errors**: "cars" should be "cards" (CXL/Gaudi cards); "pomeo" appears to be a transcription artifact for a CS milestone term; "sundown"/"sandhame"/"sandoval" are all transcription variants of "Sangdon"; "inters" = "Intel"; "kianics" = "SK hynix". These errors are in the source transcript and preserved for traceability - do not reproduce them in your own speech.
- **Audio sync**: The audio file exists but segment-to-time mapping is estimated. For precise shadowing, listen to the audio and locate the excerpt by content keywords.
- **Non-standard English**: Some SK Hynix speaker utterances are grammatically non-standard ("we'd like to ask to some help", "I don't know where about that"). These are preserved for authenticity but should be recognized as learner English - the pragmatic function is clear even when grammar is imperfect. Use the standard versions in the "pattern" field of the Expression DB.

---

*Textbook 30 - INTEL December Sync (2025-12-05). Meeting type C (sample/schedule coordination). Expression DB 48 entries. 5 excerpt segments. Written: 2026-09-01.*
