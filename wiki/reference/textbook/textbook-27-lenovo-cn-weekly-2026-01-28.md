---
textbook_id: 27
meeting: Lenovo(CN)weekly
date: 2026-01-28
type: C (sample/schedule coordination)
partner: Lenovo China (Derek, John Won, Fred, Jerry, Dave)
sk_side: SK Hynix CXL/BMC engineering, sample qualification, system reservation
duration_words: 2843
audio: repo/webex-audio/2026-01-28 10 26 08_EN_Lenovo(CN)weekly-extracted.wav
transcript: repo/webex-audio/2026-01-28 10 26 08_EN_Lenovo(CN)weekly-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, lenovo, cxl, smm, amd-venice-sp8, sample-coordination, schedule-alignment, ecdsa, firmware-signing, type-c]
---

# Textbook 27 - Lenovo(CN) weekly (2026-01-28)

> **Meeting type**: C (sample/schedule coordination) - confirmed. Heavy schedule negotiation around AMD Venice SP8 launch, SMM controller delay, ES sample timing, sustained qualification after Q2 27, mid-February test case definition, thermal testing, system reservation in Beijing lab. Plus two side agendas: CMM firmware signing authority and early collaboration on ECDSA boot-time security validation.
> **Learning value**: How to politely package a delay decision, how to negotiate schedule pull-in without offending, how to defer answers gracefully, how to coordinate test case definition across two teams, how to propose a "soft yes" with conditional follow-up.
> **Audrey view**: This is acoordination call between two non-native English teams (Korean + Chinese). The English is broken in places - that is actually useful, because the speakers still manage to negotiate politely through fragments. The pragmatic skeleton (deflection, hedging, conditional commitment) survives the broken grammar. Learn the skeleton, not the fragments.

---

## 1. Speaker Architecture - how each side structures a coordination update

### Side A: SK presenter - the "decision-then-implications" formula

The SK presenter opens not with a problem but with a **decision already made**, then walks through implications. This is the opposite of the Marvell "problem-first" pitch. In a weekly sync, you do not re-pitch - you report decisions and align.

| Stage formula | Original | Function |
|:---|:---|:---|
| `So I checked the current leaders with X. So currently we have this a lot about the Y. And for the new projects like the Z.` | "So I checked the current leaders with Ren Yuan. So Jerry and Dave and the Hanning team. So currently we have this a lot about the SVTM 3.1. And for the new projects like the VINIS." | Context recap before the decision |
| `But for the X it's already fixed. The schedule is fixed. But the schedule is for the X SP8.` | "But for the VINIS it's already fixed. The schedule is fixed. But the schedule is for the VINIS SP8." | Lock in the part that is firm |
| `Yeah. I heard the X delayed again and again. So cannot meet our schedule.` | "I heard the SMM controller delayed again and again. So cannot meet our schedule." | The honest problem - blame on a third party (SMM), not Lenovo |
| `Only we will not announce the chip support for the X. We will not post in our website. But technically we will be ready during the Y phase.` | "Only we will not announce the chip support for the SMM. We will not post in our website. But technically we will be ready during the MPI phase." | The deflection core: 2 negatives + "But technically" |
| `If we post the business case or customer order. We will quickly involve the X. Maybe in one or two quarters.` | "If we post the business case or customer order. We will quickly involve the SMM. Maybe in one or two quarters." | Conditional re-engagement - keeps the door open |
| `So that's our decision. Share with the X team.` | "So that's our decision. Share with the Hanning team." | Close the statement - "that's our decision" |

**Audrey lesson**: In a weekly sync, open with the decision, not the problem. "So that's our decision" is a closing line that signals "we are not negotiating this point - we are informing". Then move to coordination. Korean engineers often over-explain the problem first; in a sync, the partner wants the decision first, then the implications.

### Side B: Derek (Lenovo) - the "acknowledge-then-probe" formula

Derek does not push back on the decision. He **acknowledges first**, signals he already knew, then probes the implications. This is the polite partner dance.

| Stage formula | Original | Function |
|:---|:---|:---|
| `Yeah. Thanks for letting us know.` | "Yeah. Thanks for letting us know." | Standard acknowledgment |
| `I already aware of that. Because we already have some made a call last night.` | "I already aware of that. Because we already have some made a call last night." | Pre-empt - "I am not surprised" |
| `So I think it's a reasonable decision.` | "So I think it's a reasonable decision." | Endorse the partner's decision |
| `So I respect your decision.` | "So I respect your decision." | Deference - defer to the partner's call |
| `So I think we need to discuss. Even you will not have the official X, But you will have Y.` | "So I think we need to discuss. Even you will not have the official MPI and certification for your AMD SP8 project. But you will have a hardware and firmware enablement and validation." | Reframe - "even so, let us discuss what IS happening" |
| `So I think that the I mean when we start to that kind of the evaluation... Do you still.` | "So I think that the I mean when we start to that kind of the evaluation under the development phase with our official ES samples or I mean. Do you still." | Hedge into a probe - "I mean" + "or I mean" softens |

**Audrey lesson**: "I respect your decision" is a high-value phrase. It does NOT mean "I agree" - it means "I will not fight this, but I have follow-up questions". In a sync, when a partner announces a delay, do not argue the decision. Acknowledge, then immediately pivot to "so what CAN we do". Derek's pivot is the template: "Even you will not have X, but you will have Y" - find what is still on the table.

### Side A: SK negotiator - the "propose-then-ask" formula

Later in the meeting, the SK side proposes new items (signing authority, ECDSA early collaboration) using a clean structure.

| Stage formula | Original | Function |
|:---|:---|:---|
| `We would like to talk about X for Y. The controller vendor took on Z. And for Gen two, we need to discuss whether the same approach is acceptable.` | "We would like to talk about signing authority for 20 and generation CMM module for Gen one. The controller vendor took on the signing responsibility. And for Gen two, we need to discuss whether the same approach is acceptable." | Background + open question |
| `Well, if the module manufacturer should assume this responsibility instead. So what does that work thing about this.` | "Well, if the module manufacturer should assume this responsibility instead. So what does that work thing about this." | Present the alternative - "what do you think" |
| `We would like to propose to renewable early collaboration to validation, X using Y under existing Z.` | "we would like to propose to renewable early collaboration to validation, good time security using ECD SA algorithm, algorithm under existing first CMM module." | Soft proposal - "we would like to propose" |

**Audrey lesson**: "We would like to talk about X" is the gentle way to introduce a new agenda item mid-meeting. "We need to discuss whether the same approach is acceptable" - this is how you flag an open question without taking a position. "We would like to propose" is the formal proposal opener - softer than "we propose".

---

## 2. Hedging / deflection strategies - how weaknesses are politely packaged

This is the key value of this transcript. A weekly sync is full of small weaknesses: delays, missing info, unavailable samples, uncertain timelines. Each one is packaged with a specific formula.

### Strategy 1: Two negatives + "But technically" (Decision softening)

The SK presenter packages the SMM delay decision with two "will not" statements, then immediately offers "But technically we will be ready". This softens the announcement.

| Weakness | Original | Translation |
|:---|:---|:---|
| SMM not officially supported at MPI | "Only we will not announce the chip support for the SMM. We will not post in our website. **But technically we will be ready during the MPI phase.**" | "SMM 지원은 공식 발표 안 합니다. 웹사이트에도 안 올립니다. **하지만 기술적으로는 MPI 단계에 준비됩니다.**" |

**Pattern formula**: `We will not announce X. We will not post Y. But technically we will be ready during Z.`

**Audrey lesson**: When you have to announce a negative decision to a partner, double-state the negative ("will not announce... will not post"), then pivot with "But technically we will be ready". The "technically" is doing heavy lifting - it says "the business announcement is off, but the engineering work continues". This lets the partner save face: they are not getting nothing, they are getting technical readiness without official stamp.

### Strategy 2: Conditional re-engagement (Keep the door open)

After announcing the delay, the presenter immediately offers a conditional path back.

| Weakness | Original | Translation |
|:---|:---|:---|
| SMM volume uncertain | "If we post the business case or customer order. We will quickly involve the SMM. Maybe in one or two quarters." | "비즈니스 케이스나 고객 주문이 있으면, SMM을 빠르게 투입합니다. 1~2 쿼터 안에요." |

**Pattern formula**: `If we post the business case or customer order, we will quickly involve X. Maybe in one or two quarters.`

**Audrey lesson**: "Maybe in one or two quarters" is the classic vague timeline. Never commit to a quarter - commit to a range. "One or two quarters" buys flexibility. The conditional "if we post the business case" makes the re-engagement depend on a market trigger, not on SK's goodwill. This is how you keep a partner warm without promising anything.

### Strategy 3: "We still under discussion" (Soft deferral)

When the partner asks a direct question you cannot answer, defer with "we still under discussion" rather than "I don't know".

| Situation | Original | Translation |
|:---|:---|:---|
| Which phase the test falls in | "We still under discussion. Yeah." | "여전히 논의 중입니다." |
| Sustained qualification timing | "Yeah. We still under discussion." | "네, 여전히 논의 중입니다." |

**Pattern formula**: `We still under discussion.` (standalone, with "yeah" to soften)

**Audrey lesson**: "We still under discussion" is the partner-meeting version of "I don't know yet". It implies work is in progress, not ignorance. Always prefer "we are still under discussion" over "I don't know" in a sync. It signals the question is being handled, not dodged.

### Strategy 4: "I need a double confirm" (Info not available, will confirm)

When you genuinely lack info, name the gap and commit to confirming.

| Situation | Original | Translation |
|:---|:---|:---|
| Cable ready time unknown | "I haven't got the details data for cable ready time. So I need a double confirm." | "케이블 준비 시점에 대한 상세 데이터가 아직 없습니다. 다시 확인해 보겠습니다." |
| Signing impact unclear | "I need a double confirm with our program management PM. So I need to discuss that internally. Maybe, yeah, from now I think maybe it's in, it will not impact us, but I need a double confirm." | "PM과 다시 확인해야 합니다. 내부 논의가 필요합니다. 아마 영향은 없을 것 같은데, 다시 확인하겠습니다." |

**Pattern formula**: `I haven't got the details for X. So I need a double confirm.` / `I need a double confirm with our PM. I need to discuss that internally. Maybe it will not impact us, but I need a double confirm.`

**Audrey lesson**: "I need a double confirm" is non-native English but it works - partners understand it. The native version is "I need to double-check" or "I need to confirm with the team". The structure is gold: (1) admit you lack the info, (2) name who you will check with, (3) give a preliminary read ("maybe it will not impact us"), (4) restate the commitment to confirm. The preliminary read is key - it gives the partner something to work with while you confirm.

### Strategy 5: "Bad news" reframe (Polite pushback reception)

Derek gently labels the decision as "bad news" - a soft protest - then immediately accepts it.

| Situation | Original | Translation |
|:---|:---|:---|
| SK delays SMM sustained qual | "So I think that it's a bad news. Because we would like to go with your the first launch target on AMD Venice SP8 and first launch the target. But yeah, I understand the opportunity. We don't. We haven't aligned with your project schedule." | "그건 안 좋은 소식이네요. 저희는 AMD Venice SP8 첫 출시 타겟에 맞추고 싶었거든요. 하지만 기회는 이해합니다. 저희가 프로젝트 일정을 맞추지 못한 거죠." |
| SK reframe | "Maybe it's not a bad news." | "어쩌면 안 좋은 소식이 아닐 수도요." |

**Pattern formula**: `I think it's a bad news. Because we would like to go with X. But yeah, I understand the opportunity. We haven't aligned with your project schedule.` / Reframe: `Maybe it's not a bad news.`

**Audrey lesson**: "I think it's a bad news" is a polite way to register disappointment without attacking. Follow it with "But yeah, I understand" - this acknowledges the partner's constraint. Then "We haven't aligned with your project schedule" - this takes some responsibility, which makes the protest land softer. The SK reframe "Maybe it's not a bad news" is a gracious response - do not argue when a partner accepts gracefully.

### Strategy 6: Conditional "I can try" (Tentative commitment)

Fred offers to try a test on the V4 platform, with a face-saving escape if it fails.

| Situation | Original | Translation |
|:---|:---|:---|
| BMC ECDSA validation request | "But I can try. I'll talk to our engineer first. I can provide you with a test solution. But this is for the next generation of products. ... I can try it on our V4 platform. If there is any problem, I can also do some feedback on the next VW platform." | "해볼 수는 있습니다. 먼저 엔지니어와 얘기하겠습니다. 테스트 솔루션을 제공할 수 있습니다. 단, 이건 다음 세대 제품용입니다. V4 플랫폼에서 시도해 볼 수 있습니다. 문제가 있으면 다음 VW 플랫폼에 피드백하겠습니다." |

**Pattern formula**: `I can try. I'll talk to our engineer first. I can provide you with a test solution. But this is for the next generation. I can try it on our V4 platform. If there is any problem, I can do some feedback on the next platform.`

**Audrey lesson**: "I can try" is weaker than "I will" but stronger than "maybe". When a partner asks for something you cannot commit to fully, "I can try" plus a scope limit ("this is for the next generation") plus a fallback ("if there is any problem, I can do some feedback on the next platform") gives the partner a real commitment while protecting you. The fallback is key - it gives you an exit if the first attempt fails.

### Strategy 7: "Maybe we could use your ES sample" (Hedged proposal)

Derek proposes using ES samples for hardware qualification, hedged with "maybe".

| Situation | Original | Translation |
|:---|:---|:---|
| Schedule risk on BF samples | "So for this case maybe we could use your your ES simple. The hardware is same as simple." | "이번 경우에는 ES 샘플을 쓰면 어떨까 싶습니다. 하드웨어는 같으니까요." |

**Pattern formula**: `So for this case maybe we could use your ES sample. The hardware is same.`

**Audrey lesson**: "Maybe we could use" is the hedge-proposal pattern. "Maybe" + "could" double-softens. Then justify with a technical fact ("the hardware is same") - this gives the proposal substance. In a sync, when you want to propose a workaround, lead with "maybe we could" and back it with a technical reason.

---

## 3. Polite challenge patterns - the questioner's deferent probes

This meeting has gentle probes, not hard challenges. The partners are coordinating, not debating.

### Probe 1: "Do you still" - the trailing probe

| Formula | Original | Function |
|:---|:---|:---|
| `So I think that the I mean when we start to that kind of the evaluation under the development phase with our official ES samples or I mean. Do you still.` | "So I think that the I mean when we start to that kind of the evaluation under the development phase with our official ES samples or I mean. Do you still." | Trailing probe - the question is implied, not finished |

**Audrey lesson**: "Do you still" is an unfinished question. In spoken English, leaving a question unfinished can be polite - it invites the partner to fill in. The "I mean" and "or I mean" fillers signal the speaker is thinking out loud, which softens the probe. Native speakers do this too. Use "I mean" to buy time when forming a sensitive question.

### Probe 2: "My question is the I mean" - the framed probe

| Formula | Original | Function |
|:---|:---|:---|
| `My question is the I mean you don't like to have the summer evaluation with the CMM device. But at this moment we only have the the evaluation board. So I'm not sure you you have a plan to evaluate summer test with the real device or simulation level.` | "My question is the I mean you don't like to have the summer evaluation with the CMM device. But at this moment we only have the the evaluation board. So I'm not sure you you have a plan to evaluate summer test with the real device or simulation level." | Frame the constraint, then ask |

**Pattern formula**: `My question is the I mean you don't like X. But at this moment we only have Y. So I'm not sure you have a plan to evaluate Z with the real device or simulation level.`

**Audrey lesson**: State the constraint ("we only have the evaluation board"), then ask the open question ("real device or simulation level"). Offering two options ("real device or simulation level") makes the question easier to answer than an open "how will you test". Always offer options when probing a partner's plan.

### Probe 3: "Am I correct?" - the timeline confirmation

| Formula | Original | Function |
|:---|:---|:---|
| `So it means that the I guess that the it will be the after the Q1 over 27 time frame. Am I correct?` | "So it means that the I guess that the it will be the after the Q1 over 27 time frame. Am I correct?" | Restate the timeline + ask for confirmation |

**Audrey lesson**: "Am I correct?" is the timeline-confirmation pattern. After a partner gives a vague timeline, restate it with your understanding and ask "Am I correct?". This forces a clean confirmation and avoids later misalignment. The partner corrected it immediately: "No. After Q2. After Q2. Q2 27." - the correction was clean because the question was direct.

### Probe 4: "Should we" - the procedural check

| Formula | Original | Function |
|:---|:---|:---|
| `Should we wait on another tent?` | "Should we wait on another tent?" | Procedural - should we wait for more attendees |
| `Should we finish this meeting, Fred?` | "Should we finish this meeting, Fred?" | Closing check |

**Audrey lesson**: "Should we" is the procedural-question pattern. Use it for logistics (waiting, starting, finishing), not for technical content. It delegates the decision to the partner politely.

---

## 4. Negotiation / action item language

This is the heart of a Type C meeting. Most of the value is here.

### Schedule negotiation patterns

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Lock the firm part | SK | "But for the VINIS it's already fixed. The schedule is fixed." | Establish what is not negotiable |
| Name the slip | SK | "I heard the SMM controller delayed again and again. So cannot meet our schedule." | Honest reporting of a third-party delay |
| Soft timeline | SK | "Maybe in one or two quarters." | Vague re-engagement |
| Coordinate test case definition | SK | "we will define the test case and the different schedule based on your samples and also based on our project schedule" | Joint planning formula |
| Target date soft | SK | "the test case will be defined with the target is maybe early or February. ... Maybe middle February." | Soft target with hedged date |
| Internal alignment time | SK | "we almost need two weeks to align with our internal team" | Name the coordination cost |
| Confirm timeline understanding | Derek | "So the February means the next month?" | Clarify - do not assume |
| Emphatic correction | SK | "No. No. No. No. Not early. Not early. Maybe middle February." | Multi-no correction - be unambiguous |
| Sustained qual timing | Derek | "if you're and the user have some order or interest in the using 670 model so you will have the sustain qualification. So yeah. It will be happened after the launch of your after launch." | Conditional future - "after launch" |
| Timeline restatement | Derek | "So it means that the I guess that the it will be the after the Q1 over 27 time frame. Am I correct?" | Confirm understanding |
| Timeline correction | SK | "No. After Q2. After Q2. Q2 27. 27. I see." | Clean correction |
| Schedule risk acknowledgment | Derek | "I believe that there is a no timeline issue. Yeah. In that time frame." | Close the timeline concern |
| Sample readiness check | Derek | "your yes simple is almost ready" | Confirm sample availability |

**Audrey lesson**: The schedule-negotiation dance has 5 moves: (1) lock what is firm, (2) name what slipped, (3) propose a soft target, (4) confirm understanding, (5) correct if needed. The most important is step 4 - always restate the timeline and ask "Am I correct?". This meeting shows the value: the partner guessed Q1, the answer was Q2 - a one-quarter correction caught in real time.

### Sample quantity negotiation

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Ask for quantity | SK | "Please let us know the how many quantity you will require for your internal evaluation purpose test purpose and and even your summeRDIM." | Open request for sample count |
| Justify the ask | SK | "I think you are different geo and different kinds of development team including bios efi bios and BMC team. Yeah. They would like to validate the functionality. So yeah. Please align with your internal team and let us know." | Explain WHY the count matters - multiple teams |
| System reservation | SK | "during the QTR we we will reserve one system to you. So that that's what we will be in Beijing or in your headquarters." | Offer a system for the partner's lab |
| System placement logic | Derek | "If just one system I think I think we we we can set up a data in a Beijing lab. If you have more system we will share system to our headquarters." | If/then for resource allocation |
| Co-location benefit | Derek | "If we set up a system in Beijing where we do some tests with Lenovo it will be more convenience in such a for example some issue happen or some new product need to test and we need to co-work that would be more convenience." | Justify the placement - "more convenience" |

**Audrey lesson**: When asking for sample quantity, justify the ask: "different geo and different kinds of development team including BIOS, EFI BIOS, and BMC team - they would like to validate the functionality". This makes the request look reasonable, not greedy. And "please align with your internal team and let us know" - defer the answer to the partner's internal sync, do not demand an answer on the call.

### Action item patterns

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Email follow-up | Derek | "Can you send me an email after a meeting and we start to talk this the request with our engineer." | Request written follow-up |
| Internal alignment then meeting | SK | "after we aligned internally we will host a meeting another meeting to align with you and to work to to confirm your schedule" | Two-step coordination - internal first, then joint |
| Test plan ownership | Derek | "We started to plan our test items last time a Samantha request we need to make a plan for a test." | Remind of prior action item |
| Confirm internally then report | Fred | "I need a double confirm with our program management PM. So I need to discuss that internally. ... Please let us know after your internally." | Internal check commitment |
| Try + feedback | Fred | "I can try it on our V4 platform. If there is any problem, I can also do some feedback on the next VW platform." | Tentative action with fallback |

**Audrey lesson**: "Can you send me an email after a meeting" is a high-value action-item pattern. Spoken commitments evaporate; an email creates a record. Always close an action item with "send me an email" or "please let us know after your internal discussion". The two-step "we will align internally, then we will host another meeting to align with you" is the cleanest coordination pattern - never try to finalize a cross-company plan in one call.

### Closing patterns

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Agenda check | SK | "We have all covered today's agenda. Do you have any agenda for this meeting?" | Confirm closure |
| No more | Derek | "Not saying from me. Okay." | Polite no |
| Close question | Derek | "Should we finish this meeting, Fred?" | Polite close initiation |
| Sign-off | Fred | "Yes." | Confirm |
| Farewell | SK | "Have a good day. Thank you. Bye-bye. Thank you." | Standard close |

**Audrey lesson**: "We have all covered today's agenda. Do you have any agenda for this meeting?" - this is the formal close. Always ask the partner if they have anything before closing. "Should we finish this meeting?" is the polite close-initiation - it delegates the final call to the partner.

---

## 5. Domain vocabulary with exact usage context

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **SVTM** | SK Hynix internal program name (likely a validation/qualification program) | "currently we have this a lot about the SVTM 3.1" - program version reference |
| **VINIS / VINIS SP8** | AMD Venice SP8 platform project name | "for the VINIS it's already fixed. The schedule is fixed. But the schedule is for the VINIS SP8" - schedule lock |
| **OXTREM** | Follow-on project, still being decided | "for the OXTREM is still under sighting by our project team" - "under sighting" = under consideration/selection |
| **SMM** | Shared Memory Module / CXL memory module | "I heard the SMM controller delayed again and again. So cannot meet our schedule" - the delayed component |
| **MPI phase** | Mass Production Introduction phase | "we will not announce the chip support for the SMM... But technically we will be ready during the MPI phase" - the phase gate |
| **ES sample** | Engineering Sample - early silicon for development | "maybe we could use your your ES simple" - proposed for hardware qualification |
| **BF / bring-up firmware** | Early firmware for first boot | "you know BF our BF is very early. Yes. And for only early years simple could meet our schedule" - BF too early for full schedule |
| **STB / SIT phase** | System Test Build / System Integration Test phase | "during the STB phase or SIT phase no problem which phase is owned by IOT" - test phase ownership |
| **IOT** | (likely) IO Test or a test team | "which phase is owned by IOT" - ownership |
| **summeRDIM / summer RDIM** | (likely) CXL RDIMM - the memory module form factor | "SummeRDIM wanted to have that test with our real device" - the real-device test target |
| **RDIM / MRDIM** | Registered DIMM / Multiplexer Combined RDIMM | "for the R-Dim is 1dbc-8000... for MRDIM is not not all the wonder will pass 1dbc-1-1-4-1-1-2-100" - speed binning |
| **1DPC 8000** | One DIMM Per Channel at 8000 MT/s | "not all the wonders could pass the 1dbc-8000" - speed yield issue |
| **BBS schedule** | (likely) Build/Bring-up Schedule | "Our BBS schedule is a no fly now" - locked schedule |
| **sustained qualification** | Long-term production qualification (after launch) | "you will have the sustain qualification. So yeah. It will be happened after the launch" - post-launch qual |
| **PSI Gen 5 / Gen 6** | PCIe Gen 5 / Gen 6 (cable) | "currently the cable is a Gen 5. So we want to use a new cable and waiting for the PSI Gen 6" - cable spec gap |
| **signing authority** | Who signs the firmware with a key | "we would like to talk about signing authority for 20 and generation CMM module" - ownership question |
| **SPDM** | Security Protocol and Data Model (DMI-SPDM) | "the key can be used for SPDM. Oh, not the same. Not, not the same. It is not related with SPDM. SPDM is related with certificate" - clarification |
| **secure boot** | Boot-time firmware authenticity verification | "for the security boot feature, we use this key" - key usage |
| **ECDSA** | Elliptic Curve Digital Signature Algorithm | "we would like to propose to renewable early collaboration to validation, good time security using ECD SA algorithm" - proposed algorithm |
| **PQC** | Post-Quantum Cryptography | "it will go to end generation will use PQC for this" - future crypto plan |
| **BMC** | Baseboard Management Controller | "we need to get our BMC engineer to support that" - team owner |
| **V4 / VW platform** | Lenovo platform names | "I can try it on our V4 platform. If there is any problem, I can also do some feedback on the next VW platform" - test platform progression |
| **QTR** | (likely) Quarter / quarterly review | "during the QTR we we will reserve one system to you" - system reservation window |
| **no fly now** | Locked schedule (aviation metaphor) | "Our BBS schedule is a no fly now" - cannot move |
| **under sighting** | Under consideration (non-native) | "for the OXTREM is still under sighting by our project team" - being decided |

---

## 6. Expression DB

45 entries from this meeting. IDs prefixed `m27`.

```yaml
# ── Decision announcement (Type C: schedule) ──
- id: m27-001
  expression: "So that's our decision. Share with the X team."
  category: decision_announcement
  function: close_decision
  speaker_role: presenter
  difficulty: 3
  context: "So that's our decision. Share with the Hanning team."
  note: Weekly sync decision-closing formula - "that's our decision" signals not negotiating

- id: m27-002
  expression: "We will not announce X. We will not post in our website. But technically we will be ready during the Y phase."
  category: deflection_negation_but
  function: decision_softening
  speaker_role: presenter
  difficulty: 5
  context: "Only we will not announce the chip support for the SMM. We will not post in our website. But technically we will be ready during the MPI phase."
  note: Two-negative + "But technically" - the key deflection for a delay decision

- id: m27-003
  expression: "If we post the business case or customer order, we will quickly involve X. Maybe in one or two quarters."
  category: conditional_reengagement
  function: keep_door_open
  speaker_role: presenter
  difficulty: 5
  context: "If we post the business case or customer order. We will quickly involve the SMM. Maybe in one or two quarters."
  note: Conditional re-engagement with vague timeline - "one or two quarters" buys flexibility

- id: m27-004
  expression: "Maybe in one or two quarters."
  category: vague_timeline
  function: flexible_commitment
  speaker_role: presenter
  difficulty: 3
  context: "Maybe in one or two quarters."
  note: The vague timeline formula - never commit to a single quarter, commit to a range

- id: m27-005
  expression: "I heard the X delayed again and again. So cannot meet our schedule."
  category: honest_reporting
  function: third_party_blame
  speaker_role: presenter
  difficulty: 4
  context: "I heard the SMM controller delayed again and again. So cannot meet our schedule."
  note: Blame a third party (SMM), not the partner - honest reporting of a delay

# ── Acknowledgment (Lenovo side) ──
- id: m27-006
  expression: "Thanks for letting us know."
  category: acknowledgment
  function: standard_ack
  speaker_role: questioner
  difficulty: 2
  context: "Yeah. Thanks for letting us know."

- id: m27-007
  expression: "I already aware of that. Because we already have some made a call last night."
  category: preempt_ack
  function: not_surprised
  speaker_role: questioner
  difficulty: 4
  context: "I already aware of that. Because we already have some made a call last night."
  note: "I already aware" is non-native but works - signals the news is not a surprise

- id: m27-008
  expression: "I think it's a reasonable decision."
  category: endorsement
  function: accept_decision
  speaker_role: questioner
  difficulty: 3
  context: "So I think it's a reasonable decision."
  note: Endorse the partner's decision before probing implications

- id: m27-009
  expression: "I respect your decision."
  category: deference
  function: defer_to_partner
  speaker_role: questioner
  difficulty: 4
  context: "So I respect your decision."
  note: "I respect" is NOT "I agree" - it means "I will not fight this, but I have follow-ups"

- id: m27-010
  expression: "Even you will not have the official X, but you will have Y."
  category: reframe
  function: pivot_to_available
  speaker_role: questioner
  difficulty: 5
  context: "Even you will not have the official MPI and certification for your AMD SP8 project. But you will have a hardware and firmware enablement and validation."
  note: Reframe - find what IS still on the table after a negative decision

# ── Soft deferral ──
- id: m27-011
  expression: "We still under discussion."
  category: soft_deferral
  function: not_yet_decided
  speaker_role: presenter
  difficulty: 3
  context: "We still under discussion. Yeah."
  note: "I don't know" replacement - implies work in progress

- id: m27-012
  expression: "I haven't got the details for X. So I need a double confirm."
  category: info_gap_commit
  function: confirm_later
  speaker_role: presenter
  difficulty: 4
  context: "I haven't got the details data for cable ready time. So I need a double confirm."
  note: Non-native "double confirm" - native: "double-check" or "confirm with the team"

- id: m27-013
  expression: "I need a double confirm with our PM. I need to discuss that internally. Maybe it will not impact us, but I need a double confirm."
  category: info_gap_commit
  function: confirm_with_prelim_read
  speaker_role: questioner
  difficulty: 5
  context: "I need a double confirm with our program management PM. So I need to discuss that internally. Maybe, yeah, from now I think maybe it's in, it will not impact us, but I need a double confirm."
  note: 4-part structure: (1) who I will check with (2) internal discussion (3) preliminary read (4) restate commitment

- id: m27-014
  expression: "Once you get the information, please share with the team."
  category: follow_up_request
  function: request_share
  speaker_role: questioner
  difficulty: 3
  context: "once you get the information, please share with the team and and."

# ── Schedule negotiation ──
- id: m27-015
  expression: "But for the X it's already fixed. The schedule is fixed."
  category: schedule_lock
  function: establish_firm
  speaker_role: presenter
  difficulty: 3
  context: "But for the VINIS it's already fixed. The schedule is fixed."

- id: m27-016
  expression: "we will define the test case and the different schedule based on your samples and also based on our project schedule"
  category: joint_planning
  function: coordinate
  speaker_role: presenter
  difficulty: 4
  context: "we will talk with the SMM and SK to define the test case and the different schedule based on your samples and also based on our project schedule"

- id: m27-017
  expression: "the test case will be defined with the target is maybe early or February."
  category: soft_target
  function: tentative_date
  speaker_role: presenter
  difficulty: 3
  context: "the test case will be defined with the target is maybe early or February."

- id: m27-018
  expression: "Maybe middle February."
  category: refined_target
  function: narrow_range
  speaker_role: presenter
  difficulty: 2
  context: "No. No. No. No. Not early. Not early. Maybe middle February."

- id: m27-019
  expression: "we almost need two weeks to align with our internal team"
  category: coordination_cost
  function: name_time_cost
  speaker_role: presenter
  difficulty: 4
  context: "we we we we we we we almost need two weeks to align with our internal team"
  note: Name the coordination cost - partners underestimate internal alignment time

- id: m27-020
  expression: "So the February means the next month?"
  category: clarify_assume
  function: confirm_understanding
  speaker_role: questioner
  difficulty: 3
  context: "So the February means the next month?"
  note: Always clarify relative dates - "February" from a Jan 28 call = next month

- id: m27-021
  expression: "No. No. No. No. Not early. Not early."
  category: emphatic_correction
  function: unambiguous_no
  speaker_role: presenter
  difficulty: 3
  context: "No. No. No. No. Not early. Not early. Maybe middle February."
  note: Multi-no correction - be unambiguous when correcting a timeline assumption

# ── Timeline confirmation ──
- id: m27-022
  expression: "So it means that the I guess that the it will be the after the Q1 over 27 time frame. Am I correct?"
  category: timeline_confirm
  function: restate_and_check
  speaker_role: questioner
  difficulty: 5
  context: "So it means that the I guess that the it will be the after the Q1 over 27 time frame. Am I correct?"
  note: Always restate a vague timeline and ask "Am I correct?" - catches one-quarter errors

- id: m27-023
  expression: "No. After Q2. After Q2. Q2 27."
  category: clean_correction
  function: correct_timeline
  speaker_role: presenter
  difficulty: 3
  context: "No. After Q2. After Q2. Q2 27. 27. I see."

- id: m27-024
  expression: "I believe that there is a no timeline issue. In that time frame."
  category: close_concern
  function: resolve_worry
  speaker_role: questioner
  difficulty: 4
  context: "I believe that there is a no timeline issue. Yeah. In that time frame."

# ── Sample coordination ──
- id: m27-025
  expression: "Please let us know the how many quantity you will require for your internal evaluation purpose test purpose"
  category: quantity_request
  function: ask_sample_count
  speaker_role: presenter
  difficulty: 4
  context: "Please let us know the how many quantity you will require for your internal evaluation purpose test purpose and and even your summeRDIM."

- id: m27-026
  expression: "Please align with your internal team and let us know."
  category: defer_to_internal
  function: offload_decision
  speaker_role: presenter
  difficulty: 3
  context: "Please align with your internal team and let us know."

- id: m27-027
  expression: "during the QTR we will reserve one system to you. So that's what we will be in Beijing or in your headquarters."
  category: resource_offer
  function: system_reservation
  speaker_role: presenter
  difficulty: 4
  context: "during the QTR we we will reserve one system to you. So that that's what we will be in Beijing or in your headquarters."

- id: m27-028
  expression: "If just one system I think we can set up a data in a Beijing lab. If you have more system we will share system to our headquarters."
  category: resource_allocation
  function: if_then_placement
  speaker_role: questioner
  difficulty: 4
  context: "If just one system I think I think we we we can set up a data in a Beijing lab. If you have more system we will share system to our headquarters."

- id: m27-029
  expression: "If we set up a system in Beijing where we do some tests with Lenovo it will be more convenience"
  category: justify_placement
  function: convenience_argument
  speaker_role: questioner
  difficulty: 4
  context: "If we set up a system in Beijing where we do some tests with Lenovo it will be more convenience in such a for example some issue happen or some new product need to test and we need to co-work that would be more convenience."

# ── Hedged proposal ──
- id: m27-030
  expression: "So for this case maybe we could use your ES sample. The hardware is same."
  category: hedged_proposal
  function: workaround_suggest
  speaker_role: questioner
  difficulty: 5
  context: "So for this case maybe we could use your your ES simple. The hardware is same as simple."
  note: "Maybe we could" double-softens, then justify with technical fact

- id: m27-031
  expression: "I'm not sure you have a plan to evaluate summer test with the real device or simulation level."
  category: two_option_probe
  function: option_offer
  speaker_role: questioner
  difficulty: 4
  context: "So I'm not sure you you have a plan to evaluate summer test with the real device or simulation level."
  note: Offer two options - easier to answer than open "how will you test"

# ── Polite pushback ──
- id: m27-032
  expression: "I think that it's a bad news. Because we would like to go with your the first launch target on X. But yeah, I understand the opportunity."
  category: polite_pushback
  function: register_disappointment
  speaker_role: questioner
  difficulty: 5
  context: "So I think that it's a bad news. Because we would like to go with your the first launch target on AMD Venice SP8 and first launch the target. But yeah, I understand the opportunity."

- id: m27-033
  expression: "Maybe it's not a bad news."
  category: reframe
  function: gracious_reframe
  speaker_role: presenter
  difficulty: 4
  context: "Maybe it's not a bad news."

- id: m27-034
  expression: "We haven't aligned with your project schedule."
  category: shared_responsibility
  function: take_some_blame
  speaker_role: questioner
  difficulty: 4
  context: "We don't. We haven't aligned with your project schedule."
  note: Take some responsibility to soften the pushback

# ── Conditional commitment ──
- id: m27-035
  expression: "I can try. I'll talk to our engineer first. I can provide you with a test solution. But this is for the next generation of products."
  category: tentative_commit
  function: soft_yes_with_scope
  speaker_role: questioner
  difficulty: 5
  context: "But I can try. I'll talk to our engineer first. I can provide you with a test solution. But this is for the next generation of products."

- id: m27-036
  expression: "I can try it on our V4 platform. If there is any problem, I can also do some feedback on the next VW platform."
  category: tentative_commit
  function: try_with_fallback
  speaker_role: questioner
  difficulty: 5
  context: "I can try it on our V4 platform. If there is any problem, I can also do some feedback on the next VW platform."
  note: Try + fallback - gives an exit if the first attempt fails

- id: m27-037
  expression: "we are discussing the solution"
  category: in_progress
  function: status_soft
  speaker_role: questioner
  difficulty: 3
  context: "We don't have a Warfight right now. We are discussing the solution."

- id: m27-038
  expression: "I'm not sure if we will have a Warfight tonight. But if you have a solution, you can try to validate it in the BMC area. But we can't guarantee that this thing will be done smoothly."
  category: conditional_with_disclaimer
  function: soft_yes_with_risk
  speaker_role: questioner
  difficulty: 5
  context: "I'm not sure if we will have a Warfight tonight. But if you have a solution, you can try to validate it in the BMC area. But we can't guarantee that this thing will be done smoothly."

# ── Action items ──
- id: m27-039
  expression: "Can you send me an email after a meeting and we start to talk this the request with our engineer."
  category: action_item
  function: written_followup
  speaker_role: questioner
  difficulty: 4
  context: "Can you send me an email after a meeting and we start to talk this the request with our engineer."
  note: Spoken commitments evaporate - always request an email for the record

- id: m27-040
  expression: "after we aligned internally we will host a meeting another meeting to align with you and to confirm your schedule"
  category: two_step_coord
  function: internal_then_joint
  speaker_role: presenter
  difficulty: 4
  context: "And then after we aligned internally we will host a meeting another meeting to align with you and to work to to confirm your schedule."

- id: m27-041
  expression: "Please let us know after your internally."
  category: follow_up_request
  function: check_back
  speaker_role: presenter
  difficulty: 3
  context: "Please let us know after your internally."

- id: m27-042
  expression: "We have all covered today's agenda. Do you have any agenda for this meeting?"
  category: close_check
  function: confirm_closure
  speaker_role: presenter
  difficulty: 3
  context: "We have all covered today's agenda. Do you have any agenda for this meeting?"

- id: m27-043
  expression: "Should we finish this meeting?"
  category: close_init
  function: polite_close
  speaker_role: questioner
  difficulty: 2
  context: "Should we finish this meeting, Fred?"

# ── Proposal openers ──
- id: m27-044
  expression: "We would like to talk about X for Y."
  category: agenda_intro
  function: introduce_topic
  speaker_role: presenter
  difficulty: 3
  context: "We would like to talk about signing authority for 20 and generation CMM module for Gen one."

- id: m27-045
  expression: "We would like to propose to renewable early collaboration to validation, X using Y under existing Z."
  category: proposal
  function: soft_propose
  speaker_role: presenter
  difficulty: 5
  context: "we would like to propose to renewable early collaboration to validation, good time security using ECD SA algorithm, algorithm under existing first CMM module."
  note: "We would like to propose" - softer than "we propose"

- id: m27-046
  expression: "We need to discuss whether the same approach is acceptable."
  category: open_question
  function: flag_open_issue
  speaker_role: presenter
  difficulty: 4
  context: "And for Gen two, we need to discuss whether the same approach is acceptable."

- id: m27-047
  expression: "I hope that your marketing team has a good promotion to for your end user and has a lot of strong interests from your end user and hope that we will start the sustained qualification next year."
  category: polite_expectation
  function: hopeful_close
  speaker_role: questioner
  difficulty: 4
  context: "I hope that the I mean you you're marketing in your this team has a good promotion to for your end user and has a lot of strong interests from your end user and hope that we will start the the sustained qualification next year."
  note: "I hope that" - polite expectation without demanding

- id: m27-048
  expression: "Our BBS schedule is a no fly now."
  category: locked_schedule
  function: cannot_move
  speaker_role: questioner
  difficulty: 4
  context: "Our our schedule is our BBS schedule is is a no fly now. So some of them will start test maybe in October or early or September."
  note: "No fly" = aviation metaphor for a locked schedule - cannot move

- id: m27-049
  expression: "It will be happened after the launch of your after launch."
  category: post_launch_timing
  function: phase_gate
  speaker_role: questioner
  difficulty: 3
  context: "It will be happened after the launch of your after launch."

- id: m27-050
  expression: "Not saying from me. Okay."
  category: no_more
  function: polite_no
  speaker_role: questioner
  difficulty: 2
  context: "Not saying from me. Okay."
  note: Non-native "not saying from me" - native: "nothing from me" or "I have nothing more"
```

---

## 7. Excerpt map for shadowing

Audio: `repo/webex-audio/2026-01-28 10 26 08_EN_Lenovo(CN)weekly-extracted.wav` (about 30 min, 2,843 words)
5 excerpts for Mon-Fri rotation. Each about 1-2 min.

| # | Time (approx) | Line range | Summary | Learning point | Difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | Opening (line 33-62) | 33-62 | SK presenter announces SMM delay decision: "we will not announce... but technically we will be ready during MPI" + "maybe in one or two quarters" | Two-negative + "But technically" deflection, conditional re-engagement | ★★★★ |
| 2 | Acknowledge-probe (line 64-100) | 64-100 | Derek acknowledges ("reasonable decision", "I respect your decision"), reframes ("even you will not have X, but you will have Y"), proposes ES sample workaround | Acknowledge-then-probe formula, "even so, let us discuss what IS happening" | ★★★★ |
| 3 | Schedule negotiation (line 108-150) | 108-150 | Test case definition target "early or February" -> Derek clarifies "February means next month?" -> SK corrects "No. No. No. No. Not early. Maybe middle February." + "two weeks to align internally" | Soft target, clarify assumption, emphatic correction, coordination cost | ★★★★ |
| 4 | Sustained qual timeline (line 172-200) | 172-200 | Derek probes sustained qualification timing, restates "after Q1 over 27, am I correct?", SK corrects "No. After Q2. Q2 27", Derek closes "no timeline issue in that time frame" | Timeline restatement + "Am I correct?" + clean correction | ★★★★ |
| 5 | Soft yes with fallback (line 396-407) | 396-407 | Fred on ECDSA validation: "I can try. I'll talk to our engineer first. I can provide a test solution. But this is for the next generation. I can try it on our V4 platform. If there is any problem, I can do some feedback on the next VW platform." | Tentative commitment with scope limit and fallback | ★★★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, Wed: Excerpt 3, Thu: Excerpt 4, Fri: Excerpt 5
- Daily 20-min routine: insert excerpts into slots
- Excerpts 1, 3, 4 are the highest value - deflection and timeline negotiation are the heart of Type C

---

## 8. Audrey teaching notes

### Register analysis

This is a **weekly sync register** - lower formality than a pitch, higher than a casual chat. The English is broken in places (both teams are non-native: Korean + Chinese). The pragmatic skeleton still works - that is the lesson. You can negotiate politely through fragments if you know the formulas.

Two register layers:
- **SK presenter**: Decision-reporting register - "so that's our decision", "we will not announce", "but technically we will be ready". Firm but not aggressive.
- **Derek (Lenovo)**: Partner-acknowledgment register - "thanks for letting us know", "I respect your decision", "even you will not have X, but you will have Y". Deferent but probing.

### Pragmatics core

1. **Two-negative + "But technically"**: When announcing a delay decision, double-state the negative, then pivot with "But technically we will be ready". The "technically" separates business announcement from engineering readiness. This is the key deflection for Type C meetings.

2. **"I respect your decision" != "I agree"**: "I respect your decision" means "I will not fight this, but I have follow-up questions". Derek uses it perfectly - endorse, then immediately probe what IS still on the table. Do not argue a decision that is already made; pivot to coordination.

3. **"Am I correct?" timeline check**: After a partner gives a vague timeline ("after Q1 over 27"), always restate it and ask "Am I correct?". This meeting shows why - the partner corrected Q1 to Q2 in real time. Without the check, you would have a one-quarter misunderstanding on record.

4. **"I can try" + scope + fallback**: When you cannot commit to a partner's request fully, use "I can try" + a scope limit ("this is for the next generation") + a fallback ("if there is any problem, I can do some feedback on the next platform"). This gives a real commitment while protecting you.

5. **"Maybe in one or two quarters"**: The vague timeline formula. Never commit to a single quarter in a sync - commit to a range. "One or two quarters" buys a full quarter of flexibility.

### Top 5 must-use from this meeting

1. **"We will not announce X. We will not post in our website. But technically we will be ready during the Y phase."** - delay-decision deflection
2. **"I respect your decision. Even you will not have the official X, but you will have Y."** - acknowledge-then-pivot
3. **"So it means that the I guess it will be after Q1, Am I correct?"** - timeline restatement + confirmation
4. **"I can try. I can provide you with a test solution. But this is for the next generation. I can try it on our V4 platform. If there is any problem, I can do some feedback on the next platform."** - tentative commitment with fallback
5. **"Please let us know the how many quantity you will require. Please align with your internal team and let us know."** - defer the answer to the partner's internal sync

### Korean vs English comparison

| Korean | English (this meeting) | Difference |
|:---|:---|:---|
| "SMM은 공식 지원 안 합니다" | "We will not announce the chip support for the SMM. We will not post in our website. But technically we will be ready." | Korean: single negative. English: double negative + "But technically" pivot |
| "알겠습니다" | "Thanks for letting us know. I already aware of that. I think it's a reasonable decision. I respect your decision." | Korean: one acknowledgment. English: four-layer acknowledgment (thanks + already knew + reasonable + respect) |
| "내부 검토 후 얘기하죠" | "We still under discussion. We need to discuss that internally. Maybe it will not impact us, but I need a double confirm." | Korean: one deferral. English: deferral + preliminary read + restate commitment |
| "2월 쯤요" | "Maybe early or February. Not early. Maybe middle February." | Korean: one vague date. English: hedge -> clarify -> emphatic correction -> narrowed range |
| "Q1 이후인 거죠?" | "So it means that the I guess it will be after Q1 over 27, Am I correct?" | Korean: confirm. English: restate + "Am I correct?" to force clean confirmation |
| "해볼게요" | "I can try. I'll talk to our engineer first. I can provide a test solution. But this is for the next generation. If there is any problem, I can do some feedback on the next platform." | Korean: single verb. English: try + scope + fallback |
| "메일 주세요" | "Can you send me an email after a meeting" | Korean: imperative. English: "Can you send me" - request form |

---

## 9. How to use this textbook

1. **Daily 20-min routine**: Rotate the 5 excerpts in section 7 Mon-Fri. Excerpts 1, 3, 4 are the highest value for Type C - the deflection and timeline-negotiation patterns.
2. **Expression DB**: Of the 50 entries, start with the Top 5 in section 8. Then expand to m27-002 (two-negative deflection), m27-009 ("I respect your decision"), m27-022 ("Am I correct?"), m27-035 ("I can try" + scope), m27-039 (email follow-up).
3. **Audrey Friday correction**: This week, write a dump focused on a delay-announcement scenario. Use the two-negative + "But technically" structure. Practice the "I respect your decision" acknowledgment from the partner side.
4. **Comparison learning**: Use the Korean-vs-English table in section 8. The biggest gap is the acknowledgment layer - Korean "알겠습니다" maps to a four-layer English acknowledgment. Drill this.
5. **Non-native English tolerance**: This transcript has broken English from both sides. Do not copy the grammar - copy the pragmatic skeleton. "I already aware" is wrong grammar but right pragmatics. Learn the function, fix the form.

---

*Textbook 27 - Lenovo(CN) weekly (2026-01-28). Meeting type C (sample/schedule coordination). Expression DB 50 entries. 5 excerpt segments. Written 2026-09-01.*
