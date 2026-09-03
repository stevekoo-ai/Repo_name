---
textbook_id: 19
meeting: MSFT (Microsoft CXL/AI memory discussion)
date: 2026-03-12
type: D (issue/quality debugging) - confirmed
partner: Microsoft (Mike, Gary, plus quality/PI program owners)
sk_side: SK Hynix (CXL product planning, device quality, DDR5 UEA analysis)
duration_words: 1659
audio: repo/webex-audio/2026-03-12 09 07 48_EN_MSFT-extracted.wav
transcript: repo/webex-audio/2026-03-12 09 07 48_EN_MSFT-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, microsoft, cxl, ddr5, uea, quality-metrics, fa-turnaround, cdl, issue-debugging]
---

# Textbook 19 - MSFT CXL/AI Memory Discussion (2026-03-12)

> **Meeting type**: D (issue/quality debugging) - Microsoft reports DDR5 UEA error trends, quality metrics (ABQ, FA turnaround), power targets; SK Hynix presents CXL CMM roadmap and commits to root cause investigation
> **Learning value**: Issue diagnosis language, quality metrics framing, soft challenge on competitor comparison, roadmap overlay with caveats, FA (failure analysis) turnaround coordination
> **Audrey's view**: This is a "quality review + roadmap sync" hybrid. The D-type core is the DDR5 UEA debugging exchange and the quality metrics review. You must learn how Microsoft frames quality issues politely while pushing for root cause, and how SK Hynix commits to investigation without admitting fault.

---

## 1. Speaker Architecture - Three Presentation Modes

This meeting has three distinct presentation modes, each with its own structural formula. Unlike a single-pitch meeting (Type A), this is a multi-topic review where each side takes turns presenting data.

### Mode 1: SK Hynix CXL Roadmap (Product Progression)

The SK presenter uses a **"we already have X, now we are targeting Y, also we have Z"** progression formula. Each generation is introduced by anchoring on the previous one.

| Formula | Original | Function |
|:---|:---|:---|
| `We already have our first gen X. Now we are targeting our second generation X with Y.` | "We already have our first gen CXL CMM BDR5 and now we are targeting our second generation CXL CMM BDR5 with the S2T" | Anchor + next gen - establishes credibility before introducing new |
| `The density is up to X on Y on Z` | "The density is up to 236 gigabytes on CXL 3.1 on PCIJ6" | Spec listing - three parameters chained |
| `Currently we have our EVB and our ES targeting this year and ... we'll target to intercept that BMR.` | "Currently we have our EVB and our ES targeting this year and of this year and it will be next year, February and we'll target to intercept that BMR" | Milestone staging - EVB/ES as near-term, intercept as far |
| `Also we have the third generation.` | "Also we have the third generation." | Brief forward pointer - keeps roadmap open without detail |
| `Let's move on. This is just an appendix.` | "Let's move on. This is just an appendix." | Decisive transition - downplay remaining content |

**Audrey lesson**: When presenting a roadmap, anchor each generation on the previous one. "We already have X, now we are targeting Y" is much stronger than "We are developing Y." The "already" establishes that you have shipped, which is the credibility foundation. Then "also we have the third generation" - a one-line forward pointer keeps the roadmap horizon visible without overcommitting detail.

### Mode 2: Microsoft Quality Metrics Review (Data-First Framing)

The MSFT quality presenter uses a **"chart at top is showing X, good news is Y, but there were some Z"** structure. Data first, then evaluation, then challenge.

| Formula | Original | Function |
|:---|:---|:---|
| `First, we'll be going over the skate behind this all metrics.` | "First, we'll be going over the skate behind this all metrics." (likely "scope behind these quality metrics") | Agenda setting - opens section |
| `The chart at the top is showing your average box for X and Y.` | "The chart at the top is showing your average box for quality and commodity quality" | Data introduction - chart-first framing |
| `And then I also put in the X to get your trend.` | "And then I also put in the quarter rolling average in here to get your trend" | Trend overlay - context for evaluation |
| `And the good news is with X, there is a Y trend going into Z.` | "And the good news is with SK high nicks, there is a 10 word trend going into 2026 of Q1" (likely "downward trend") | Positive framing first - softens later critique |
| `The good thing is also that you guys were able to lower your X, you know, quarter over quarter for the last Y quarters` | "The good thing is also that you guys were able to lower your ABQ, you know, quarter over quarter for the last three quarters" | Acknowledgment of improvement before push |
| `Now the X, I'm just planning the distributions for the last Y quarters.` | "Now the F8 turnaround time, I'm just planning the distributions for the last four quarters" | Pivot to next metric - "Now the X" |
| `You could see that, you know, Q4 was a really rough year for you guys.` | "You could see that, you know, Q4 was a really rough year for you guys" | Direct critique - "rough year" as honest feedback |
| `But, you know, there were some X that really took a long time.` | "But, you know, there were some FAs that really took a long time" | Specific issue callout - "some X" softens blame |
| `I mean, we got to really drive that down.` | "I mean, we got to really drive that down" | Action expectation - "drive that down" |
| `You know, like 30 is a target that we want to target.` | "You know, like 30 is a target that we want to target" | Numeric target setting |
| `And anyways, for the Qols in the Q1 of 2026, it looks like this year you guys are off to a good start.` | "And anyways, for the Qols in the Q1 of 2026, it looks like this year you guys are off to a good start" | Recovery acknowledgment - ends on positive |

**Audrey lesson**: This is the "sandwich feedback" structure in business English: (1) chart/data first, (2) good news / positive trend acknowledgment, (3) "but" pivot to the issue, (4) target setting, (5) recovery acknowledgment. The "good news is" / "good thing is also" / "but" / "anyways" sequence is the formula. "You could see that Q4 was a really rough year for you guys" - direct but softened by "you know" and "for you guys" (familiar). End with "off to a good start" to keep the relationship positive.

### Mode 3: Microsoft Power Target Guidance (Caveat-First)

The MSFT power presenter (Mike) uses a **"previously we provided X, this picks up where that left off, with a caveat that Y, to align with Z"** structure. Caveat before data.

| Formula | Original | Function |
|:---|:---|:---|
| `So I just wanted to give some updated guidance on X for these higher speed grains.` | "So I just wanted to give some updated guidance on power targets for these higher speed grains" | Purpose statement - "just wanted to" softens |
| `And so previously we provided guidance up to X. So this picks up where that left off` | "And so previously we provided guidance up to 7200. So this picks up where that left off" | Continuity framing - links to prior commitment |
| `with a little bit of a caveat in that we slightly reduced our X targets` | "with a little bit of a caveat in that we slightly reduced our 7200 targets" | Soft caveat - "a little bit of a caveat" + "slightly" double-softens |
| `and that's to align with our intercept of newer material and newer designs transitioned in our intercept timeline.` | "and that's to align with our intercept of newer material and newer designs transitioned in our intercept timeline" | Justification - "to align with" as rationale |
| `In easy conversation here is that everything that we tested has been best in class` | "In easy conversation here is that everything that we tested has been best in class" | Reassurance - "best in class" after a target reduction |
| `And we are anticipating the future improvements to be even just to maintain that same conversation.` | "And we are anticipating the future improvements to be even just to maintain that same conversation" | Forward expectation - "anticipating" |
| `So congratulations on all the hard work that you guys continue to put in here.` | "So congratulations on all the hard work that you guys continue to put in here" | Compliment close - "continue to put in" |

**Audrey lesson**: When you must give negative news (reduced target), structure it as: (1) continuity ("picks up where that left off"), (2) double-softened caveat ("a little bit of a caveat" + "slightly"), (3) justification ("to align with"), (4) reassurance ("best in class"), (5) compliment close. The "a little bit of a caveat" is gold - it announces bad news while minimizing it. Never say "we have bad news" - say "a little bit of a caveat."

---

## 2. Hedging & Deflection Strategies

The key D-type value: how each side handles issue ownership, uncertainty, and quality pressure politely.

### Strategy 1: "At this moment" Disclaimer (No-Fault Distance)

SK side disclaims connection to the issue while not denying it outright. "At this moment" creates temporal distance - "not now, maybe later."

| Situation | Original | Translation |
|:---|:---|:---|
| Device issue attribution | "we didn't find that there is a specific connection to the our device issues at this moment" | "현재 시점에서는 당사 디바이스 이슈와의 구체적 연관을 발견하지 못했습니다" |
| Future investigation commitment | "Definitely we will do further." | "추가 조사는 확실히 하겠습니다" |

**Pattern formula**: `We didn't find that there is a specific connection to X at this moment. Definitely we will do further.`

**Audrey lesson**: "at this moment" is the gold-standard hedge for issue ownership. It does not deny ("we did not find" is past-tense non-finding, not "there is no connection"). It does not promise resolution ("we will do further" is vague commitment). It buys time. Korean "현재로서는" maps to "at this moment." Never say "it's not our issue" - say "we didn't find a connection at this moment." The "Definitely" after is critical - it shows cooperation without admitting fault.

### Strategy 2: Trend Convergence Check (System-vs-Device Frame)

SK side asks whether competitor trends are similar or different, to determine whether the issue is system-level (similar across vendors) or device-specific (only SK).

| Situation | Original | Translation |
|:---|:---|:---|
| Competitor comparison probe | "But how about the other vendors device status of the DDR5 UEA trend? Is it similar or they're totally different independent?" | "다른 벤더의 DDR5 UEA 트렌드는 어떻습니까? 비슷한가요, 아니면 완전히 다른가요?" |

**Pattern formula**: `How about the other vendors' status of X trend? Is it similar or are they totally different independent?`

**Audrey lesson**: This is a brilliant deflection move. If competitors show the same trend, the issue is likely system-level (Microsoft's platform, not SK's device). If different, it is device-specific (SK's problem). Asking this question forces Microsoft to reveal whether SK is being singled out. The phrasing "totally different independent" is a non-native but pragmatically sharp formulation - "independent" emphasizes "not correlated with our trend." Use this when you suspect a quality issue may be system-level, not your device.

### Strategy 3: "Some leeway" Flexibility Hedge (Microsoft on CDL)

Microsoft hedges its own roadmap by signaling flexibility where the milestone is not yet official.

| Situation | Original | Translation |
|:---|:---|:---|
| CDL timing flexibility | "But there are some leeway since there isn't, since it's, you know, not actual official CDL form" | "다만 공식 CDL 형식이 아니기 때문에 약간의 여유는 있습니다" |
| Planning status disclaimer | "that's still in planning. It hasn't passed through the full approval loop yet. And so there could potentially be changes there." | "아직 계획 단계이고 전체 승인 루프를 통과하지 않았습니다. 그래서 변경될 가능성이 있습니다" |
| "current view" framing | "But this is the current view that we have." | "다만 이것은 당사가 현재 보고 있는 view입니다" |

**Pattern formula**: `X is still in planning. It hasn't passed through the full approval loop yet. There could potentially be changes there. But this is the current view that we have.`

**Audrey lesson**: When you give a roadmap that is not yet committed, use this sequence: (1) "still in planning" - status, (2) "hasn't passed through the full approval loop" - reason, (3) "could potentially be changes" - hedge, (4) "this is the current view that we have" - temporal disclaimer. The "current view" framing is critical - it tells the listener "this is true today, but do not hold us to it." Use this when asked about future programs that are not yet approved.

### Strategy 4: "A little bit of a caveat" (Soft Bad News)

Microsoft announces a target reduction with double-softening.

| Situation | Original | Translation |
|:---|:---|:---|
| Power target reduction | "this picks up where that left off with a little bit of a caveat in that we slightly reduced our 7200 targets and that's to align with our intercept of newer material and newer designs" | "앞선 가이던스에 이어지지만, 7200 타겟을 약간 하향한 작은 caveat이 있습니다. 신소재/신설계 intercept에 맞추기 위해서입니다" |

**Pattern formula**: `This picks up where that left off with a little bit of a caveat in that we slightly reduced X. That's to align with Y.`

**Audrey lesson**: "a little bit of a caveat" is the polite-English way to introduce negative news. "Caveat" alone sounds formal/warning; "a little bit of a caveat" softens it. Paired with "slightly reduced" (not "cut" or "lowered"), the downgrade is minimized. Then "to align with" provides a rationale that frames the change as coordination, not retreat. When you must announce a delay or reduction, use "a little bit of a caveat" + "slightly" + "to align with."

### Strategy 5: "Best in class" Reassurance After Negative

Microsoft immediately follows the target reduction with a positive reassurance.

| Situation | Original | Translation |
|:---|:---|:---|
| Reassurance after caveat | "In easy conversation here is that everything that we tested has been best in class and meeting all of our expectations." | "쉽게 말씀드리면, 테스트한 모든 것이 best in class이며 당사 기대를 모두 충족했습니다" |

**Pattern formula**: `In easy conversation here is that everything that we tested has been best in class and meeting all of our expectations.`

**Audrey lesson**: After any negative (target reduction, delay, issue), immediately pivot to a positive. "Best in class" is the strongest positive you can give a supplier - it says "you are the best." "Meeting all of our expectations" reinforces. The phrase "in easy conversation here is that" is a discourse marker meaning "to put it simply" - it lowers tension before the positive. Use this sequence: caveat -> "in easy conversation" -> "best in class."

---

## 3. Polite Challenge Patterns

### Challenge Type 1: "Based on your investigation, I haven't seen X"

Soft challenge that turns a question into a statement of personal observation.

| Formula | Original | Function |
|:---|:---|:---|
| `Based on your technology investigation, I haven't seen any CXL this moment and still you're preferred to have an EV card.` | "Based on your technology investigation, I haven't seen any CXL this moment and still you're preferred to have an EV card." | Observation-as-question: "I haven't seen X" implies "where is X?" |

**Audrey lesson**: "Based on your X, I haven't seen Y" is a deferential challenge. It cites the partner's own investigation, then states your own non-observation. It does not ask "why no CXL?" - it says "I haven't seen CXL." The implication is clear but the form is non-confrontational. Use this when a partner promised something that is not visible in their data.

### Challenge Type 2: "Are we the only one who" (Competitive Comparison)

| Formula | Original | Function |
|:---|:---|:---|
| `Are we the only one who you just measured the power consumption or just curious? I mean, you know, technology, technology, are we better?` | "Are we the only one who you just measured the power consumption or just curious? I mean, you know, technology, technology, are we better?" | Self-comparison probe - "are we the only one" + "are we better?" |

**Audrey lesson**: This is a non-native but effective formulation. "Are we the only one who you measured" asks whether the partner is comparing only SK or all vendors. Then "are we better?" is the direct question. The "just curious" softens it. Use "Are we the only one who" when you want to know if you are being singled out, and "are we better?" when you want a competitive read. The stammering "technology, technology" is a natural speech repair - rephrasing in real time.

### Challenge Type 3: "Just checking" Status Confirmation

| Formula | Original | Function |
|:---|:---|:---|
| `Just checking the C46 AG, 256 gigabyte, that's just in test finding. I don't know, official POL?` | "Just checking the C46 AG, 256 gigabyte, that's just in test finding. I don't know, official POL?" | "Just checking" + "I don't know" + upward intonation question |

**Audrey lesson**: "Just checking X" is a low-stakes confirmation. "I don't know, official POL?" turns the question into a collaborative search - "I don't know, is it official POL?" - inviting the partner to confirm. Use "Just checking X" when you want to verify a status without appearing to challenge.

### Challenge Type 4: "Is it similar or totally different independent?" (Either-Or Probe)

| Formula | Original | Function |
|:---|:---|:---|
| `Is it similar or they're totally different independent?` | "Is it similar or they're totally different independent?" | Binary probe - forces a clear answer |

**Audrey lesson**: "Is it X or Y?" forces the partner to choose. "Similar" = system-level issue; "totally different independent" = device-specific. This is a sharp diagnostic question disguised as a simple either-or. Use this when you need to localize an issue: "Is it similar across vendors, or are they totally different independent?"

### Challenge Type 5: "And also on the Gen 10 where we are seeing some correlation to system crashes" (Direct Issue Statement)

| Formula | Original | Function |
|:---|:---|:---|
| `And also on the Gen 10 where we are seeing some correlation to system crashes, which I know we have been actively interacting on.` | "And also on the Gen 10 where we are seeing some correlation to system crashes, which I know we have been actively interacting on" | Direct issue + acknowledgment of ongoing work |

**Audrey lesson**: "where we are seeing some correlation to system crashes" is direct - it names the issue (system crashes). But "which I know we have been actively interacting on" softens by acknowledging the ongoing collaboration. Use "where we are seeing some correlation to X, which I know we have been actively interacting on" when raising an issue that is already being worked - it shows you are tracking, not surprising.

---

## 4. Negotiation & Action Item Language

### Action Commitment Patterns

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Root cause investigation commitment | SK | "We will investigate it on it for finding the root cause of our devices." | "We will investigate" - formal commitment to find root cause |
| Soft further investigation | SK | "Definitely we will do further." | "Definitely" + "further" - vague but committed |
| Acknowledgment of issue ownership | SK | "Okay, understood. We will investigate it on it for finding the root cause of our devices." | "Okay, understood" - acceptance before commitment |
| Quality target setting | MSFT | "You know, like 30 is a target that we want to target." | "30 is a target that we want to target" - numeric target |
| Drive-down expectation | MSFT | "I mean, we got to really drive that down." | "drive that down" - action expectation |
| Timeline expectation | MSFT | "we're kind of expecting you guys to get that started in Q1 in 2026" | "kind of expecting" + "get that started in Q1" - soft timeline push |
| Approval loop pending | MSFT | "It hasn't passed through the full approval loop yet." | "approval loop" - internal governance frame |

**Audrey lesson**:
- "We will investigate it for finding the root cause" is the formal issue-resolution commitment. Use "for finding the root cause" (not "to find") - it sounds more analytical. Pair with "Okay, understood" before to show acceptance.
- "30 is a target that we want to target" - the repetition of "target" is natural in spoken English. It emphasizes the number. Use "X is a target that we want to target" when setting a numeric goal.
- "we got to really drive that down" - "drive down" is the phrasal verb for reducing a metric (turnaround time, defect rate, error rate). Use "drive X down" for metrics you want to reduce.
- "kind of expecting" softens a timeline push. "We are expecting" sounds demanding; "we're kind of expecting" sounds like a gentle reminder.

### Flexibility & Coordination Language

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Flexibility hedge | MSFT | "But there are some leeway since there isn't, since it's, you know, not actual official CDL form" | "some leeway" - flexibility window |
| Acknowledgment of in-progress | MSFT | "And so, you know, we're kind of expecting you guys to get that started in Q1 in 2026" | "kind of expecting" - soft timeline |
| Recovery acknowledgment | MSFT | "anyways, for the Qols in the Q1 of 2026, it looks like this year you guys are off to a good start" | "off to a good start" - positive restart |
| Compliment close | MSFT | "congrats on that" / "Hope this is helpful" | Compliment + utility check |

---

## 5. Domain Vocabulary (Exact Usage Context)

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **CXL CMM** (CXL Compute Memory Module) | CXL memory expander module | "We already have our first gen CXL CMM BDR5" - generation framing |
| **S2T** | Second-generation controller (likely SK's in-house or 3rd-party CXL controller) | "now we are targeting our second generation CXL CMM BDR5 with the S2T" - "with the X" controller specification |
| **EVB** (Evaluation Board) | Hardware evaluation platform | "Currently we have our EVB and our ES targeting this year" - "EVB and ES" paired milestones |
| **ES** (Engineering Sample) | Early sample for evaluation | "our ES targeting this year" - sample stage |
| **intercept** | Targeted timing to catch a platform window | "we'll target to intercept that BMR" / "to align with our intercept of newer material" - intercept as timing target |
| **DDR5 UEA** (Use Error Analysis) | Field error analysis on DDR5 devices | "the DDR5 UEA trend" - error trend analysis |
| **on correct level** (likely "on-die correct level" or "on-chip correct level") | Error correction at device level | "a dramatic increase of the on correct level compared to the previous quarter" - error metric |
| **ABQ** (Average Bug Quality) | Composite quality metric | "your average box for quality and commodity quality" / "lower your ABQ quarter over quarter" - quality metric |
| **FA** (Failure Analysis) | Root cause investigation of failed units | "there were some FAs that really took a long time" - FA turnaround time |
| **FA turnaround time** | Time to complete failure analysis | "the F8 turnaround time" (transcription of "FA turnaround time") - duration metric |
| **CDL** (Critical Design Lot / Compute Design Lot) | Formal design verification milestone | "we're kind of expecting you guys to get that started in Q1" / "not actual official CDL form" - milestone |
| **EV / DV / PV** (Engineering / Design / Production Verification) | Three development milestones | "EV, DV and PV that that are is just released, it's like, you know, EV exit, PV exit" - milestone exit language |
| **PVR** (Production Verification Release?) | Release after production verification | "growth happens after after PVR" - post-PVR is deployment |
| **building block and PI program** | Component-level + Product Integration program | "overlaid with our building block and PI program" - overlay structure |
| **HBC** (High Bandwidth Compute?) | Microsoft program name | "the blue is for our HBC Venice" - color-coded program |
| **C419e / C460G** | Microsoft platform designations | "C419e, you know, you guys are getting a EV to your platform" - platform mapping |
| **PMR** (likely Platform Module Reference) | Microsoft program | "you guys are also going to get a, you know, PMR system, but that's at the end of the year in Q4" |
| **POL** (Point of Load? or Program of Record?) | Official program status | "I don't know, official POL?" / "It's not an official POL yet" - status check |
| **leading edge** | Most advanced programs only | "we're just showing leading edge here and MPI" - scope qualifier |
| **best in class** | Top performer among suppliers | "everything that we tested has been best in class" - supplier ranking |
| **grains** (likely "grades" or speed-binned DRAM) | DRAM speed tiers | "power targets for these higher speed grains" - speed grade |

---

## 6. Expression DB

```yaml
# - Issue Diagnosis (D-type core) -
- id: m19-001
  expression: "we didn't find that there is a specific connection to X at this moment"
  category: issue_diagnosis
  function: no_fault_disclaimer
  speaker_role: defender
  difficulty: 5
  context: "we didn't find that there is a specific connection to the our device issues at this moment"
  pattern: "we didn't find that there is a specific connection to X at this moment"
  note: "at this moment" 시간적 거리 - 부정도 아니고 인정도 아닌 회피의 황금표현

- id: m19-002
  expression: "Definitely we will do further."
  category: commitment_soft
  function: vague_investigation_promise
  speaker_role: defender
  difficulty: 3
  context: "Definitely we will do further."
  note: "Definitely"로 협조 표시, "further"로 범위 모호. "추가 조사 확실히 하겠습니다"

- id: m19-003
  expression: "We will investigate it for finding the root cause of X"
  category: action_commitment
  function: root_cause_promise
  speaker_role: defender
  difficulty: 4
  context: "We will investigate it on it for finding the root cause of our devices."
  pattern: "We will investigate it for finding the root cause of X"
  note: "for finding" (not "to find") - 분석적 뉘앙스

- id: m19-004
  expression: "Okay, understood."
  category: acceptance
  function: issue_acknowledgment
  speaker_role: defender
  difficulty: 2
  context: "Okay, understood. We will investigate it on it for finding the root cause of our devices."
  note: "Okay, understood" - 이슈 수용 후 action 연결 패턴

- id: m19-005
  expression: "That sounds good."
  category: acceptance
  function: positive_close
  speaker_role: questioner
  difficulty: 2
  context: "That sounds good. Thank you."

- id: m19-006
  expression: "how about the other vendors device status of the X trend?"
  category: competitor_probe
  function: deflection_via_comparison
  speaker_role: defender
  difficulty: 5
  context: "But how about the other vendors device status of the DDR5 UEA trend?"
  note: 이슈 책임을 system-level vs device-level로 구분하기 위한 질문

- id: m19-007
  expression: "Is it similar or are they totally different independent?"
  category: binary_probe
  function: either_or_diagnostic
  speaker_role: defender
  difficulty: 4
  context: "Is it similar or they're totally different independent?"
  note: "totally different independent" - 비원어 표현이지만 pragmaticshigh 날카로움

- id: m19-008
  expression: "And also on the Gen 10 where we are seeing some correlation to system crashes"
  category: issue_statement
  function: direct_issue_naming
  speaker_role: questioner
  difficulty: 4
  context: "And also on the Gen 10 where we are seeing some correlation to system crashes, which I know we have been actively interacting on"
  note: "some correlation to X" - 직접적 이슈 명명 + "actively interacting on"으로 진행 중 표시

- id: m19-009
  expression: "which I know we have been actively interacting on"
  category: ongoing_collaboration
  function: collaboration_acknowledgment
  speaker_role: questioner
  difficulty: 3
  context: "which I know we have been actively interacting on"
  note: 이슈 제기 후 진행 중임을 인정 - 공격 아님

- id: m19-010
  expression: "it's not like a uniform trend where we would suspect it's something system related"
  category: diagnosis_logic
  function: system_vs_device_reasoning
  speaker_role: questioner
  difficulty: 5
  context: "And it's not like a uniform trend where we would suspect it's something system related, the trends are different for each competitor"
  note: "uniform trend" + "we would suspect" - 논리적 추론 화법

# - Quality Metrics Review -
- id: m19-011
  expression: "First, we'll be going over the X behind this all metrics"
  category: agenda_setting
  function: section_opening
  speaker_role: presenter
  difficulty: 3
  context: "First, we'll be going over the skate behind this all metrics"

- id: m19-012
  expression: "The chart at the top is showing your X for Y"
  category: data_introduction
  function: chart_first_framing
  speaker_role: presenter
  difficulty: 3
  context: "The chart at the top is showing your average box for quality and commodity quality"

- id: m19-013
  expression: "And the good news is with X, there is a Y trend going into Z"
  category: positive_framing
  function: sandwich_feedback_open
  speaker_role: presenter
  difficulty: 4
  context: "And the good news is with SK high nicks, there is a 10 word trend going into 2026 of Q1"

- id: m19-014
  expression: "The good thing is also that you guys were able to lower your X, quarter over quarter for the last Y quarters"
  category: positive_framing
  function: improvement_acknowledgment
  speaker_role: presenter
  difficulty: 4
  context: "The good thing is also that you guys were able to lower your ABQ, you know, quarter over quarter for the last three quarters"
  note: "quarter over quarter" - 분기별 추세 표현

- id: m19-015
  expression: "Now the X, I'm just planning the distributions for the last Y quarters"
  category: metric_pivot
  function: topic_transition
  speaker_role: presenter
  difficulty: 3
  context: "Now the F8 turnaround time, I'm just planning the distributions for the last four quarters"

- id: m19-016
  expression: "You could see that, you know, X was a really rough year for you guys"
  category: direct_critique
  function: honest_feedback
  speaker_role: presenter
  difficulty: 4
  context: "You could see that, you know, Q4 was a really rough year for you guys"
  note: "rough year" - 직접적 비판, "for you guys"로 familiar하게

- id: m19-017
  expression: "But, you know, there were some X that really took a long time"
  category: issue_callout
  function: specific_issue_highlight
  speaker_role: presenter
  difficulty: 3
  context: "But, you know, there were some FAs that really took a long time"
  note: "some X" - 전부가 아닌 일부, 비난 완화

- id: m19-018
  expression: "I mean, we got to really drive that down"
  category: action_expectation
  function: reduction_demand
  speaker_role: presenter
  difficulty: 3
  context: "I mean, we got to really drive that down"
  note: "drive X down" - 메트릭 감소 액션 동사

- id: m19-019
  expression: "X is a target that we want to target"
  category: target_setting
  function: numeric_goal
  speaker_role: presenter
  difficulty: 3
  context: "You know, like 30 is a target that we want to target"
  note: "target" 반복 - 숫자 강조

- id: m19-020
  expression: "anyways, for the X, it looks like this year you guys are off to a good start"
  category: recovery_acknowledgment
  function: positive_close
  speaker_role: presenter
  difficulty: 3
  context: "And anyways, for the Qols in the Q1 of 2026, it looks like this year you guys are off to a good start"
  note: "off to a good start" - 회복 인정

- id: m19-021
  expression: "Yeah, congrats on that."
  category: compliment
  function: positive_reinforcement
  speaker_role: presenter
  difficulty: 2
  context: "Yeah, congrats on that. Thank you. Thank you."

# - Power Target Guidance (Caveat-First) -
- id: m19-022
  expression: "I just wanted to give some updated guidance on X for Y"
  category: purpose_statement
  function: soft_opening
  speaker_role: presenter
  difficulty: 3
  context: "So I just wanted to give some updated guidance on power targets for these higher speed grains"
  note: "just wanted to" - 목적 진입 완화

- id: m19-023
  expression: "previously we provided guidance up to X. So this picks up where that left off"
  category: continuity_framing
  function: link_to_prior
  speaker_role: presenter
  difficulty: 4
  context: "And so previously we provided guidance up to 7200. So this picks up where that left off"

- id: m19-024
  expression: "with a little bit of a caveat in that we slightly reduced our X"
  category: soft_bad_news
  function: double_softened_reduction
  speaker_role: presenter
  difficulty: 5
  context: "with a little bit of a caveat in that we slightly reduced our 7200 targets"
  note: "a little bit of a caveat" + "slightly" - 이중 완화. 부정 소식 전달 황금패턴

- id: m19-025
  expression: "and that's to align with our intercept of newer material and newer designs"
  category: justification
  function: rationale_for_change
  speaker_role: presenter
  difficulty: 4
  context: "and that's to align with our intercept of newer material and newer designs transitioned in our intercept timeline"
  note: "to align with" - 변화를 조정으로 프레이밍, 후퇴로 보이지 않게

- id: m19-026
  expression: "In easy conversation here is that everything that we tested has been best in class"
  category: reassurance
  function: positive_after_negative
  speaker_role: presenter
  difficulty: 4
  context: "In easy conversation here is that everything that we tested has been best in class and meeting all of our expectations"
  note: "In easy conversation here is that" - "쉽게 말하면" 담화 표지

- id: m19-027
  expression: "meeting all of our expectations"
  category: reassurance
  function: expectation_met
  speaker_role: presenter
  difficulty: 2
  context: "best in class and meeting all of our expectations"

- id: m19-028
  expression: "And we are anticipating the future improvements to be even just to maintain that same conversation"
  category: forward_expectation
  function: continuity_commitment
  speaker_role: presenter
  difficulty: 4
  context: "And we are anticipating the future improvements to be even just to maintain that same conversation"

- id: m19-029
  expression: "So congratulations on all the hard work that you guys continue to put in here"
  category: compliment_close
  function: appreciation
  speaker_role: presenter
  difficulty: 3
  context: "So congratulations on all the hard work that you guys continue to put in here"
  note: "continue to put in" - 지속 노력 인정

- id: m19-030
  expression: "Any other questions?"
  category: question_invitation
  function: section_close
  speaker_role: presenter
  difficulty: 2
  context: "Any other questions?"

# - Polite Challenge -
- id: m19-031
  expression: "Based on your technology investigation, I haven't seen any X"
  category: deferential_challenge
  function: observation_as_question
  speaker_role: questioner
  difficulty: 5
  context: "Based on your technology investigation, I haven't seen any CXL this moment and still you're preferred to have an EV card"
  note: "I haven't seen X" - 질문을 관찰 진술로. 비대립적 도전

- id: m19-032
  expression: "Are we the only one who you just measured X or just curious?"
  category: comparison_probe
  function: single_out_check
  speaker_role: questioner
  difficulty: 4
  context: "Are we the only one who you just measured the power consumption or just curious?"

- id: m19-033
  expression: "I mean, you know, are we better?"
  category: direct_comparison
  function: competitive_read
  speaker_role: questioner
  difficulty: 3
  context: "I mean, you know, technology, technology, are we better?"

- id: m19-034
  expression: "Just checking the X, that's just in test finding. I don't know, official Y?"
  category: status_confirmation
  function: low_stakes_check
  speaker_role: questioner
  difficulty: 3
  context: "Just checking the C46 AG, 256 gigabyte, that's just in test finding. I don't know, official POL?"

- id: m19-035
  expression: "Yeah, it's not an official POL yet."
  category: status_response
  function: planning_status
  speaker_role: presenter
  difficulty: 3
  context: "Yeah, it's not an official POL yet. Until I'm planning."

# - Roadmap Overlay (CDL) -
- id: m19-036
  expression: "This is showing the X targets overlaid with our Y program"
  category: roadmap_overlay
  function: view_introduction
  speaker_role: presenter
  difficulty: 4
  context: "This is showing the CDL targets overlaid with our building block and PI program"

- id: m19-037
  expression: "we're kind of expecting you guys to get that started in X"
  category: timeline_expectation
  function: soft_timeline_push
  speaker_role: presenter
  difficulty: 4
  context: "we're kind of expecting you guys to get that started in Q1 in 2026"
  note: "kind of expecting" - 요구를 기대로 완화

- id: m19-038
  expression: "But there are some leeway since there isn't, since it's, you know, not actual official X form"
  category: flexibility_hedge
  function: timeline_flexibility
  speaker_role: presenter
  difficulty: 4
  context: "But there are some leeway since there isn't, since it's, you know, not actual official CDL form"
  note: "some leeway" - 유연성 창. 말 더듬는 사이에 정중하게 삽입

- id: m19-039
  expression: "X is still in planning. It hasn't passed through the full approval loop yet."
  category: roadmap_hedge
  function: uncommitted_disclaimer
  speaker_role: presenter
  difficulty: 5
  context: "that's still in planning. It hasn't passed through the full approval loop yet"
  note: 미확정 로드맵 정중 표현 - "still in planning" + "approval loop"

- id: m19-040
  expression: "there could potentially be changes there"
  category: change_hedge
  function: possibility_disclaimer
  speaker_role: presenter
  difficulty: 3
  context: "And so there could potentially be changes there"

- id: m19-041
  expression: "But this is the current view that we have"
  category: temporal_disclaimer
  function: as_of_now_framing
  speaker_role: presenter
  difficulty: 4
  context: "But this is the current view that we have"
  note: "current view" - "오늘 기준 view" 시간적 면책

- id: m19-042
  expression: "we're just showing leading edge here"
  category: scope_qualifier
  function: view_scope
  speaker_role: presenter
  difficulty: 3
  context: "So like like storage or even like GPU, you know, we typically don't get you guys any of those platforms. So yeah, just make sure to understand that it's not the complete picture"
  note: "leading edge" - 최선단 프로그램만 표시. scope 한정

- id: m19-043
  expression: "just make sure to understand that it's not the complete picture"
  category: scope_disclaimer
  function: completeness_hedge
  speaker_role: presenter
  difficulty: 3
  context: "just make sure to understand that it's not the complete picture, but it is showing the leading edge program"

- id: m19-044
  expression: "growth happens after after PVR"
  category: milestone_sequence
  function: stage_definition
  speaker_role: presenter
  difficulty: 3
  context: "I think I mentioned before, but, you know, growth happens after after PVR"

- id: m19-045
  expression: "EV, DV and PV that are just released, it's like, you know, EV exit, PV exit"
  category: milestone_exit
  function: stage_naming
  speaker_role: presenter
  difficulty: 4
  context: "our three major development milestones, you know, EV, DV and PV that that are is just released, it's like, you know, EV exit, PV exit, PV exit, more or less"

# - CXL Roadmap Presentation -
- id: m19-046
  expression: "We already have our first gen X. Now we are targeting our second generation X with Y."
  category: roadmap_progression
  function: anchor_next_gen
  speaker_role: presenter
  difficulty: 5
  context: "We already have our first gen CXL CMM BDR5 and now we are targeting our second generation CXL CMM BDR5 with the S2T"
  note: "already" + "now targeting" - 신뢰 기반 차세대 도입

- id: m19-047
  expression: "The density is up to X on Y on Z"
  category: spec_listing
  function: triple_param_chain
  speaker_role: presenter
  difficulty: 3
  context: "The density is up to 236 gigabytes on CXL 3.1 on PCIJ6"

- id: m19-048
  expression: "Currently we have our EVB and our ES targeting this year"
  category: near_term_milestone
  function: short_term_plan
  speaker_role: presenter
  difficulty: 3
  context: "Currently we have our EVB and our ES targeting this year"

- id: m19-049
  expression: "we'll target to intercept that BMR"
  category: intercept_target
  function: timing_alignment
  speaker_role: presenter
  difficulty: 4
  context: "it will be next year, February and we'll target to intercept that BMR"

- id: m19-050
  expression: "Also we have the third generation."
  category: forward_pointer
  function: roadmap_horizon
  speaker_role: presenter
  difficulty: 2
  context: "Also we have the third generation."
  note: 한 줄 전방 포인터 - 상세 없이 로드맵 horizon 유지

- id: m19-051
  expression: "Let's move on. This is just an appendix."
  category: transition
  function: downplay_skip
  speaker_role: presenter
  difficulty: 3
  context: "Let's move on. This is just an appendix. You can refer to us."

# - Discourse Markers & Softening -
- id: m19-052
  expression: "One quick question about the X"
  category: question_opening
  function: short_question_intro
  speaker_role: questioner
  difficulty: 2
  context: "One quick question about the DDR5 UEA hard plan"

- id: m19-053
  expression: "I'd appreciate if we do understand that this is the first file of our analysis"
  category: polite_preface
  function: context_setting
  speaker_role: questioner
  difficulty: 4
  context: "I'd appreciate if we do understand that this is the first file of our analysis"

- id: m19-054
  expression: "could you briefly say about the comparison of X and Y?"
  category: comparison_request
  function: data_request
  speaker_role: questioner
  difficulty: 3
  context: "So could you briefly say about the comparison of our other data and vendor status?"

- id: m19-055
  expression: "If you could go to the previous slide"
  category: slide_navigation
  function: request_action
  speaker_role: questioner
  difficulty: 2
  context: "Gary, if you could go to the previous slide"

- id: m19-056
  expression: "So you are saying that for the case of the Gen 9, X is the matter"
  category: restatement
  function: understanding_confirm
  speaker_role: questioner
  difficulty: 4
  context: "So you are saying that for the case of the Gen 9, our devices level on the correct level, a dramatic increase of the on correct level compared to the previous quarter is the matter. Right?"
  note: "So you are saying that ... is the matter. Right?" - 확인式 정리

- id: m19-057
  expression: "Hope this is helpful."
  category: utility_check
  function: presentation_close
  speaker_role: presenter
  difficulty: 2
  context: "Hope this is helpful."

- id: m19-058
  expression: "I hope you're getting better."
  category: personal_check
  function: human_connection
  speaker_role: questioner
  difficulty: 2
  context: "I hope you're getting better."
  note: 회의 중 개인적 안부 - 관계 유지 화법
```

---

## 7. Excerpt Map (Shadowing)

Audio: `repo/webex-audio/2026-03-12 09 07 48_EN_MSFT-extracted.wav` (transcript ~1,659 words, short meeting)
5 segments for Mon-Fri shadowing rotation.

| # | Time/Line range | Summary | Learning point | Shadowing difficulty |
|:-:|:--|:---|:---|:--:|
| 1 | Lines 1-25 (CXL roadmap) | SK presenter: "We already have first gen CXL CMM, now targeting second generation with S2T, density 256GB on CXL 3.1 / PCIe6" | Roadmap progression formula: "already have X, now targeting Y with Z" | ★★☆ |
| 2 | Lines 26-46 (DDR5 UEA debugging) | SK asks about error trend, Microsoft confirms Gen 9 on-correct level increase is the matter, Gen 10 correlation to system crashes, competitor trends different | Issue diagnosis: "we didn't find specific connection at this moment" + "is it similar or totally different independent?" | ★★★★ |
| 3 | Lines 47-62 (Power target caveat) | Mike: "previously we provided guidance up to 7200, this picks up where that left off with a little bit of a caveat, we slightly reduced, to align with intercept of newer material, best in class" | Soft bad news: "a little bit of a caveat" + "slightly" + "to align with" + "best in class" reassurance | ★★★★ |
| 4 | Lines 64-83 (Quality metrics sandwich) | MSFT: "chart at top showing ABQ, good news is downward trend, you lowered ABQ quarter over quarter, but Q4 was a rough year, FAs took long time, drive that down, 30 is a target, off to a good start" | Sandwich feedback: "good news is" / "good thing is also" / "but" / "drive that down" / "off to a good start" | ★★★★ |
| 5 | Lines 84-117 (CDL roadmap overlay) | MSFT: "CDL targets overlaid with building block and PI program, expecting you to get started in Q1, some leeway, C460G still in planning, not passed approval loop, this is current view" | Roadmap hedge: "some leeway" / "still in planning" / "hasn't passed approval loop" / "current view that we have" | ★★★ |

**Usage**:
- Mon: Excerpt 1 (roadmap progression)
- Tue: Excerpt 2 (issue diagnosis - D-type core)
- Wed: Excerpt 3 (caveat-first bad news)
- Thu: Excerpt 4 (sandwich feedback)
- Fri: Excerpt 5 (roadmap hedging)
- Excerpts 2, 3, 4 are highest value - D-type issue/quality language dense

---

## 8. Audrey's Teaching Notes

### Register Analysis
This meeting is a **supplier quality review + roadmap sync** register. Two modes alternate:
- **Microsoft side (quality reviewer)**: Data-first framing, sandwich feedback, caveat-first bad news, target setting. Authority position - sets targets, evaluates SK.
- **SK Hynix side (supplier/defender)**: Roadmap progression, issue disclaimer, root cause commitment. Responsive position - answers challenges, commits to action.

You must learn both:
- As Microsoft (when you evaluate a partner): sandwich feedback, "good news is" / "but" / "off to a good start" sequence, "drive that down" target setting.
- As SK Hynix (when you are evaluated): "at this moment" disclaimer, "definitely we will do further" commitment, "we will investigate for finding the root cause" formal action.

### Pragmatics Core
1. **"At this moment" temporal distance**: The most valuable D-type hedge. "We didn't find a connection at this moment" - past tense non-finding + temporal hedge. It neither denies nor admits. It buys investigation time while showing cooperation ("definitely we will do further"). Korean "현재로서는" maps exactly. NEVER say "it's not our issue" - always "we didn't find a connection at this moment."

2. **"A little bit of a caveat" double-softening**: When announcing a target reduction (negative), use "a little bit of a caveat" (formal but softened) + "slightly" (minimizing adverb) + "to align with" (rationale as coordination, not retreat). This three-part structure is the polite-English way to deliver any downgrade.

3. **Sandwich feedback sequence**: "good news is X" / "good thing is also Y" / "but Z was a rough year" / "drive that down" / "anyways, off to a good start." The "anyways" before the positive close is critical - it signals "putting the critique aside." Korean equivalent: "그래도" - but in English "anyways" is more conversational.

4. **Competitor trend probe as deflection**: "How about the other vendors' status of X trend? Is it similar or are they totally different independent?" - This question localizes the issue. If similar = system-level (not SK's fault). If different = device-specific (SK's fault). Asking this is a defensive move that forces the evaluator to reveal whether the issue is universal or vendor-specific. Use this in any quality review where you suspect the issue is platform-level.

5. **"Current view" temporal disclaimer**: "But this is the current view that we have" - when giving a roadmap that may change. This is a rolling disclaimer. It says "true today, not guaranteed tomorrow." Use this after any future program description that is not yet approved.

### Top 5 Must-Use
1. **"we didn't find that there is a specific connection to X at this moment"** - issue ownership hedge
2. **"with a little bit of a caveat in that we slightly reduced X, to align with Y"** - soft bad news
3. **"the good news is X. The good thing is also Y. But Z was a rough year."** - sandwich feedback open
4. **"Is it similar or are they totally different independent?"** - competitor trend probe
5. **"X is still in planning. It hasn't passed through the full approval loop yet. This is the current view that we have."** - roadmap hedge

### Korean vs English Comparison
| Korean | English (this meeting) | Difference |
|:---|:---|:---|
| "현재로서는 연관성을 못 찾았습니다" | "we didn't find that there is a specific connection at this moment" | 영어는 past tense non-finding + temporal hedge로 이중 회피 |
| "약간 하향했습니다" | "with a little bit of a caveat, we slightly reduced X, to align with Y" | 영어는 "caveat" + "slightly" + "align" 삼중 완화 |
| "잘하고 있습니다만" | "the good news is X. The good thing is also Y. But Z was a rough year" | 영어는 긍정 2번 후 "but" 1번 - 비판 전 여유 확보 |
| "다른 벤더도 같은가요?" | "Is it similar or are they totally different independent?" | 영어는 either-or로 명확한 답 강제 |
| "아직 계획 단계입니다" | "still in planning. Hasn't passed through the full approval loop yet. This is the current view that we have." | 영어는 상태 + 이유 + 시간 면책 3단 |

---

## 9. How to Use This Textbook

1. **Daily 20-min routine**: Use the 5 excerpts in Section 7, Mon-Fri rotation. Excerpts 2, 3, 4 are highest value.
2. **Expression DB**: Start with Section 8 Top 5. These are D-type issue/quality essentials.
3. **Audrey Friday correction**: Focus your dump on Section 2 (hedging/deflection) and Section 3 (polite challenge) - these are the D-type core.
4. **Comparison learning**: Use Section 8 Korean-vs-English table to internalize the difference in issue-handling register.
5. **Role-play**: Practice both sides - Microsoft evaluator (sandwich feedback) and SK defender (at-this-moment hedge). You will be in both roles across different meetings.

---

*Textbook 19 - MSFT CXL/AI Memory Discussion (2026-03-12). Meeting type D (issue/quality debugging). Expression DB 58 entries. 5 excerpt segments. Written: 2026-09-02.*
