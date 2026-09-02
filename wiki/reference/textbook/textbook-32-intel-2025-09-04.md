---
textbook_id: 32
meeting: Intel (September 2025 technical deep-dive)
date: 2025-09-04
type: A (technical deep-dive) - confirmed
partner: Intel (Santosh, Jerry, Jenny, Ed, Ivan, Tony)
sk_side: SK Hynix CXL system architecture, CXL device roadmap, Santosh (Intel primary), Jerry (Intel connectivity)
duration_words: 3387
audio: repo/webex-audio/2025-09-04 08 32 11_EN_Intel-extracted.wav
transcript: repo/webex-audio/2025-09-04 08 32 11_EN_Intel-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, intel, cxl, kv-cache, memory-pooling, roadmap, cxl3, cxl4, pcie-gen7, evb, backplane, technical-deepdive]
---

# Textbook 32 - Intel (2025-09-04) CXL Roadmap & Memory Pooling Deep-Dive

> **Meeting type**: A (technical deep-dive) - SK Hynix presents CXL roadmap + memory pooling architecture, Intel probes on specs, hedges on CXL4/PCIe Gen7 commitment, commits action items for backplane review
> **Learning value**: (1) How Intel politely hedges "no decision yet" while signaling positive intent, (2) SK Hynix's roadmap pull-in framing ("we are trying to pull in"), (3) collaborative action-item assignment language
> **Audrey's view**: This is a "roadmap alignment + technical probe" meeting. SK pushes for Intel's CXL4/Gen7 commitment; Intel gives a masterclass in "we're not ready to commit but we're not saying no" hedging. Both sides' language is gold for partner meetings where one side wants a firm date and the other can only give "we're working on it."

---

## 1. Speaker Architecture - How Each Side Structures Their Talk

This meeting has two distinct speaker architectures: SK Hynix's "use case enumeration then roadmap reveal" and Intel's "hedge ladder" for un-committed decisions.

### SK Side: 4-Step Use Case -> Roadmap Architecture

The SK presenter (Santosh from SK Hynix side, with Sandosh/Sandong as the Korean-name presenter) structures the talk as:

| Step | Formula | Function |
|:---|:---|:---|
| 1. Use case framing | "As you know, the many end-user are focusing on the memory intensive work code..." | "As you know" - assume shared knowledge, establish common ground |
| 2. Two-approach enumeration | "The first approach... The second approach..." | "The first approach... The second approach..." - parallel structure for clarity |
| 3. Problem-solution pairing | "In order to solve these problems, the X technology has been introduced" | "In order to solve these problems, X has been introduced" - causal framing |
| 4. Roadmap reveal with pull-in | "we are trying to pull in our 256 gigabytes to within Q4 next year" | "we are trying to pull in X to within Y" - ambitious schedule framing |

**Audrey lesson**: SK's structure is "use case first, roadmap second." They never start with the product; they start with "the many end-user are focusing on X" to justify why the roadmap matters. Then the roadmap is framed as a pull-in ("we are trying to pull in") - signaling ambition and customer focus, not just a passive schedule.

### Intel Side: The "Hedge Ladder" for Un-Committed Decisions

When Intel (Santosh - the Intel Santosh, distinct from SK's Sandosh) responds to SK's CXL4/Gen7 question, he uses a 5-rung hedge ladder. Each rung is a fixed formula:

| Rung | Formula | Original | Function |
|:---|:---|:---|:---|
| 1. State the gap | "we don't have our POR aligned" | "I think the quick comment is we don't have our POR aligned" | Honest gap statement - "POR" (Plan of Record) is the key Intel term |
| 2. State what IS known | "We know it's not going to be for X" | "We know it's not going to be for Diamond Rapids" | Negative certainty - what's ruled out |
| 3. State the trend | "The trend today is that our future product will probably have, we hope, X" | "The trend today is that our future product will probably have, we hope, CXL4 or PCIe Gen 7" | "probably have, we hope" - double hedge with aspiration |
| 4. Re-state no commit | "we don't have a POR yet. We don't have a commit yet on our side" | "from an Intel standpoint, officially, we don't have a POR yet. We don't have a commit yet on our side that we're going to do it" | Repeat the hedge - "officially" + "yet" twice |
| 5. Personal endorsement | "But I just upfront can say, I think we should focus on that" | "But I just upfront can say, I think we should focus on that" | Personal support without official commit |

**Audrey lesson**: This is the most important architecture in the meeting. When you cannot commit but want to stay encouraging, use the hedge ladder: (1) state gap, (2) state what's known, (3) state the trend with "probably, we hope", (4) re-state no commit with "yet", (5) give personal endorsement. "We don't have a POR yet" - "yet" is the key word. It means "not now, but possibly later." Never say "no" when you can say "not yet."

### Intel Side: The "Time-to-Decision" Reframe

When pushed on timing, Intel uses a specific reframe to make a delay sound short:

| Formula | Original | Function |
|:---|:---|:---|
| "Truthfully, it's not a lot of months away" | "Truthfully, it's not a lot of months away. It's a little over a quarter away. We'll have a decision." | "not a lot of months away" + "a little over a quarter away" - minimize the wait |
| "we're hoping to make our POR decision for X" | "we're hoping to make our POR decision for Coral Rapids" | "hoping to make" - aspirational, not committed |

**Audrey lesson**: When a partner pushes for a date and you can't commit, use "Truthfully, it's not a lot of months away. It's a little over a quarter away." - "truthfully" builds trust, "a little over" minimizes, "a quarter" sounds shorter than "three months." This is the art of making a delay feel small without lying.

---

## 2. Hedging & Deflection Strategies (Intel's Masterclass)

This is the **core learning value** of this meeting. Intel's hedging is more advanced than SK's because Intel is the one with no decision yet, defending against SK's push for commitment.

### Strategy 1: "We don't have a POR yet" - The Official Non-Answer

The single most-used hedge. Intel repeats it across the meeting:

| Situation | Original | Translation |
|:---|:---|:---|
| CXL4/Gen7 commit | "we don't have our POR aligned" | "POR이 아직 정렬되지 않았습니다" |
| Re-state | "from an Intel standpoint, officially, we don't have a POR yet. We don't have a commit yet on our side that we're going to do it" | "Intel 공식立场으로는 POR이 아직 없습니다. 우리가 하겠다는 commit도 아직 없습니다" |
| Soften | "But I just upfront can say, I think we should focus on that" | "하지만 솔직히 말씀드리면, 우리가 그쪽에 focus해야 한다고 생각합니다" |

**Pattern formula**: `We don't have our POR aligned. We know it's not going to be for X. From an Intel standpoint, officially, we don't have a POR yet. We don't have a commit yet. But I think we should focus on that.`

**Audrey lesson**: "POR" (Plan of Record) is Intel's key internal term - it means the official committed plan. "We don't have a POR yet" is much more professional than "we haven't decided." "Yet" is the magic word - it implies "we will, just not now." And ending with "But I think we should focus on that" gives personal support without official commit. **Memorize this: "We don't have a POR yet. But I think we should focus on that."**

### Strategy 2: "The trend today is... we hope" - Aspirational Hedging

When Intel wants to signal a positive direction without committing:

| Situation | Original | Translation |
|:---|:---|:---|
| CXL4/Gen7 likely inclusion | "The trend today is that our future product will probably have, we hope, CXL4 or PCIe Gen 7. That we have to have it to be able to feed the pipe." | "오늘날의 trend는 미래 제품에 아마도 CXL4나 PCIe Gen 7이 들어갈 것이다, 우리는 희망합니다. pipe을 feed하려면 그게 필요합니다" |

**Pattern formula**: `The trend today is that our future product will probably have, we hope, X. That we have to have it to be able to Y.`

**Audrey lesson**: Three layers of hedge in one sentence: "probably" (probability hedge) + "we hope" (aspiration hedge) + "we have to have it to be able to Y" (technical justification). The technical justification ("feed the pipe") makes the hedge sound like a reasoned prediction, not a wish. When you can't commit, give a technical reason why it makes sense - that's stronger than "we hope."

### Strategy 3: "Between X and myself, we don't really have anything official" - Naming Colleagues in the Hedge

When hedging on behalf of a team, Intel names colleagues to spread the non-commitment:

| Situation | Original | Translation |
|:---|:---|:---|
| Gen7 official status | "But officially, between Jenny and myself, we don't really have anything official to talk about yet" | "공식적으로는 Jenny와 저 사이에 아직 공식적으로 이야기할 게 없습니다" |

**Pattern formula**: `Between X and myself, we don't really have anything official to talk about yet.`

**Audrey lesson**: Naming a colleague ("between Jenny and myself") does two things: (1) it shows you're not the sole decision-maker (spreads responsibility), (2) it signals the partner that the real decision is elsewhere. This is more sophisticated than "I don't know." When you hedge, name the colleague who owns the decision with you - it sounds collaborative and honest.

### Strategy 4: "It's under evaluation" / "It's a POC" - Stage Framing

When SK faces a hard question (thermal characteristics of the new CMM-EXP), SK uses stage framing:

| Situation | Original | Translation |
|:---|:---|:---|
| Thermal concern on 2-PCB flexible CMM | "It's under the evaluation. So we are trying to put our report to the decrease the thermal effect using some mid-plate or other idea. Yeah, that's why we are calling POC." | "평가 중입니다. mid-plate 등 다른 아이디어로 thermal effect를 줄이려는 report를 작성 중입니다. 그래서 POC라고 부릅니다" |

**Pattern formula**: `It's under evaluation. We are trying to X using Y. That's why we are calling it POC.`

**Audrey lesson**: "It's under evaluation" is the SK equivalent of Intel's "we don't have a POR yet." It says "we know it's a problem, we're working on it, but we don't have the answer yet." And explicitly naming the stage ("that's why we are calling POC") sets expectations - POC means "not production, don't hold us to final specs." When your data is preliminary, name the stage explicitly: "it's under evaluation" / "it's a POC" / "it's a development sample."

### Strategy 5: "We are trying to pull in" - Ambition Framing for SK

When SK wants to show ambition without over-promising:

| Situation | Original | Translation |
|:---|:---|:---|
| 256GB schedule | "we are trying to pull in our 256 gigabytes to within Q4 next year. Actually, our sales schedule will be January of 2027, but SK hynix will try to pull in within Q4 2026" | "256GB를 내년 Q4 안으로 pull in하려고 합니다. 실제 sales schedule은 2027년 1월이지만, SK hynix가 Q4 2026 안으로 pull in을 시도할 것입니다" |

**Pattern formula**: `We are trying to pull in X to within Y. Actually, our sales schedule will be Z, but we will try to pull in within Y.`

**Audrey lesson**: "We are trying to pull in" is the key SK ambition phrase. Note the structure: (1) state the ambitious target, (2) admit the official schedule is later, (3) re-state the pull-in attempt. This shows ambition while being honest about the official plan. "Trying to" is the hedge - it's not a promise, it's an attempt. When you want to show ambition without over-committing, use "we are trying to pull in X to within Y."

### Strategy 6: "We need to make sure" - Deflecting Action to the Other Side

Intel deflects the backplane compatibility question to a future action without committing to do it themselves:

| Situation | Original | Translation |
|:---|:---|:---|
| Dual port backplane fit | "I think from an Intel side, we should take an action item to make sure that someone reviews the back plane and looks at the card to make sure that they work well" | "Intel 측에서는 action item을 잡아서 back plane을 review하고 card를 확인해서 잘 작동하는지 make sure해야 합니다" |

**Pattern formula**: `We should take an action item to make sure that someone reviews X and looks at Y to make sure that they work well.`

**Audrey lesson**: "We should take an action item to make sure that someone reviews X" - note "someone," not "I." This assigns the action to a future, unnamed person. It commits the organization without committing the speaker. When the action is real but you're not the one who'll do it, use "we should take an action item to make sure that someone reviews X."

---

## 3. Polite Challenge Patterns (Both Sides Probing)

This meeting has mutual probing - SK asks Intel for CXL4/Gen7 commitment, Intel asks SK for thermal/latency details. Both use deferent technical probes.

### Probe Type 1: "Just to confirm" - Quick Reality Check

| Formula | Original | Function |
|:---|:---|:---|
| "I just wanted to confirm" | "That's what I was thinking too. I just wanted to confirm." | Validate own understanding politely |
| "Just you have a whole rack and of course, having the rack very close to the SOC is important" | (Jerry) "Just you have a whole rack and of course, having the rack very close to the SOC is important" | "Just" softens a technical assertion |

**Audrey lesson**: "I just wanted to confirm" is the gentlest possible challenge. It says "I think I know, but I want to make sure." Use this when you suspect the other side's number but don't want to call it wrong. "I just wanted to confirm" - never "are you sure?"

### Probe Type 2: "What is the latest of X?" - Status Probe Without Pressuring

| Formula | Original | Function |
|:---|:---|:---|
| `What is the latest of the X?` | "What about the latest of the PCIe Gen 7 itself? Do you know the information? What is the latest of the PCIe Gen 7?" | "What is the latest of X" - status inquiry |
| `Is your question a spec-related or?` | (Intel) "Is your question a spec-related or?" | Receiver asks clarifying question to scope the answer |

**Audrey lesson**: "What is the latest of X?" is the polite way to ask "where are you in the process?" without asking "when will it be done?" It asks for current state, not commitment. When you want to probe a partner's progress without pressuring for a date, use "what is the latest of X?" Note Intel's response: "Is your question a spec-related or?" - Intel scopes the question before answering. This is a great defensive technique: when asked a vague question, ask what kind of answer they want.

### Probe Type 3: "What's the X of Y compared to Z?" - Comparative Technical Probe

| Formula | Original | Function |
|:---|:---|:---|
| `What's the latency of X compared to Y? Is it in A or B?` | "What's the latency of RDMA compared to CXL? Is it in milliseconds or microseconds?" | Comparative + range question - lets the speaker pick the precision |

**Audrey lesson**: "What's the X of Y compared to Z? Is it in A or B?" - this gives the partner a multiple-choice frame. They can pick "microseconds" or correct you. This is less aggressive than "what's the latency?" because it shows you've already thought about it and just want confirmation. Use this when you have a hypothesis and want the partner to validate or correct.

### Probe Type 4: "What's the thermal characteristics of that?" - Direct Physical Concern

| Formula | Original | Function |
|:---|:---|:---|
| `What's the X of that? It looks like it Y.` | "What's the thermal characteristics of that? It looks like it gets pretty hot." | Direct concern + observation - honest physical reaction |

**Audrey lesson**: "What's the thermal characteristics of that? It looks like it gets pretty hot." - this is direct and honest. No hedge, no softening. When you see a real technical concern, it's OK to be direct. "It looks like it gets pretty hot" is an observation, not a criticism. Direct technical observations are respected in engineering meetings - you don't need to soften physical reality.

### Probe Type 5: "Are we in line to get X?" - Polite Status Confirmation

| Formula | Original | Function |
|:---|:---|:---|
| `Are we in line to get the X for Y?` | "Are we in line to get the CXL, your CXL3 devices for Diamond Rapids?" | "Are we in line to get" - polite eligibility check |

**Audrey lesson**: "Are we in line to get X for Y?" is the polite way to ask "are we getting X?" It frames the question as "are we in the queue?" rather than "will you give us?" - this respects the partner's process. Use "are we in line to get" when checking if your company is on the list for a sample/EVB/early hardware.

---

## 4. Negotiation & Action Item Language

The meeting ends with concrete action items and a follow-up schedule. This is a model for closing a technical deep-dive.

### Action Item Assignment

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Take action item | Intel | "I think from an Intel side, we should take an action item to make sure that someone reviews the back plane and looks at the card to make sure that they work well" | Assign action to Intel org |
| Make a note | Intel | "We need to make a note and then when the time comes, then we need to make sure we are compatible and if not, then what needs to be done?" | "Make a note" - lighter than action item |
| Share slides | Intel facilitator | "Sandosh, send the slides out. Send the questions that SK, your RDIM is looking at" | Direct imperative for follow-up |

### Follow-Up Schedule Negotiation

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| Propose next meeting | SK | "we better keep giving a presentation of this Divina slide two weeks later. And then, Sandong, you also like, you're going to share the slides with Intel?" | "we better keep giving X two weeks later" - propose cadence |
| Confirm date | Intel | "then we will have minutes and maybe in two weeks on 17th, maybe you can bring your slides from your side and question and we can have a discussion now" | "in two weeks on 17th" - confirm concrete date |
| Assign ownership | Intel | "I'm going to put a lot of emphasis on Ivan and Ed and Jenny to help out here, but I'll be available too and we'll talk about it in two weeks" | Name the team that will help - "I'll be available too" |
| Close | Both | "Sounds good. Sounds good. Good plan. Thank you. Great slides." | Triple confirmation + compliment close |

**Audrey lesson**: Note how the follow-up is structured: (1) propose cadence ("two weeks later"), (2) confirm concrete date ("on 17th"), (3) assign ownership ("Ivan and Ed and Jenny"), (4) keep yourself available ("I'll be available too"), (5) close with triple confirmation ("Sounds good. Sounds good. Good plan.") and compliment ("Great slides"). When closing a technical meeting, follow this 5-step structure. The triple "sounds good" is not redundancy - it's mutual confirmation that both sides heard the same plan.

### Soft Commitment Language

| Pattern | Speaker | Original | Function |
|:---|:---:|:---|:---|
| "We will follow the X standardization" | SK | "we will follow the ZX standardization about the CXL3.1" | Standardization alignment commit |
| "We will send the EV board early of November" | SK | "we will send the EV board early of November" | Concrete deliverable + date |
| "We will ask to Intel's open app again" | SK | "we will ask to Intel's open app again, because we don't have the TMR CRB until maybe next year" | Request + reason for request |
| "Please check the ability of this one" | SK | "So please check the ability of this one" | "Please check the ability" - polite ask for feasibility |

**Audrey lesson**: SK uses "we will follow / we will send / we will ask" - all "we will" (commit), while Intel uses "we don't have a POR yet / we're hoping to make a decision" - all hedged. In a partner meeting, the side with the product commits, the side making the decision hedges. Know which side you're on. If you're the supplier, use "we will." If you're the customer deciding, use "we're hoping to."

---

## 5. Domain Vocabulary (Exact Usage Context)

| Term | Meaning | Usage in this meeting |
|:---|:---|:---|
| **POR** (Plan of Record) | Intel's official committed plan | "we don't have our POR aligned" / "we don't have a POR yet" - the central Intel hedge term |
| **EVB** (Evaluation Board) | Board sent to partner for testing | "We will send the EVB to Intel in November" / "About what volume of these are you thinking of? Just a few samples?" |
| **CMM-EXP** (CXL Memory Module - Expanded) | SK Hynix's CXL memory form factor | "we are recording the second gen CMM" - "recording" = "developing/recognizing" (transcript artifact) |
| **RDIM** (Registered DIMM) | Server memory module with register | "Send the questions that SK, your RDIM is looking at" - SK's RDIM team |
| **Diamond Rapids** | Intel CPU codename (current gen in lab) | "We know it's not going to be for Diamond Rapids" - ruled out for CXL4 |
| **Coral Rapids** (a.k.a. "Coral", "Diamond Rapids Plus") | Next Intel CPU after Diamond Rapids | "we're hoping to make our POR decision for Coral Rapids" - target for CXL4/Gen7 |
| **PDK** (Platform Design Kit) | Intel's platform integration documentation | "we would like to find the granularity of the PDK available" - SK waiting for PDK |
| **CRB** (Customer Reference Board) | Intel's reference motherboard | "we don't have the TMR CRB until maybe next year" - TMR = a specific CRB variant |
| **back plane** | Rack-level connectivity board | "we should take an action item to make sure that someone reviews the back plane" |
| **dual port 2x4** | CXL card with two 4-lane ports | "2x4 dual port. We need to make sure that those dual ports fit into our back plane" |
| **5x4 / 5x8 connectors** | Backplane connector types (5x4 = 5 row 4 lane, 5x8 = wider) | "technically we are on the back plate. We do have 5x4 connectors. I think the limitation is that on our platform, they're only 5x8 connectors" - compatibility gap |
| **pre-fill vs decode** | LLM inference phases | "the software would determine what's a pre-fill versus a decode worker" / "KV cache pool is more applicable for decode" |
| **bundle link** | CXL4 feature - combining multiple links | "for CXL4, when you start to think about features... bundled link, high frequency, 128 gig, where you can go 128 gig and you can interleave them and you can bundle link them" |
| **128 gig** | PCIe Gen7 / CXL4 data rate | "128 gig, where you can go 128 gig and you can interleave them and you can bundle link them, suddenly that bandwidth is starting to be appealing" |
| **feed the pipe** | Keep the data path fully utilized | "we have to have it to be able to feed the pipe" - technical justification for Gen7 |
| **pathfinding** | Intel's early exploration phase | "we're doing a lot of pathfinding, but as far as like an official, this is what we're going to do" - pathfinding is pre-POR |
| **TPI** (Thread-Level Peripheral Interface) | BMC-side signal for dual port | "it also requires some the dual port signal as the sort of the TPI you're from the BMC" |
| **BMC** (Baseboard Management Controller) | Server management controller | "the TPI you're from the BMC" |
| **mid-plate** | Thermal mitigation structure | "we are trying to put our report to the decrease the thermal effect using some mid-plate or other idea" |
| **MDS** (Memory and Density Solution, possibly Multi-Die Stack) | SK memory solution class | "your MDS solution in the future probably will play a role" - context: cheaper memory for cost-sensitive pools |
| **smart NIC** | Network card with onboard processing | "a lot of smart NIC doing RDMA and they have optimized" / "the smart NIC system and then smart NIC system handover packet to the memory pooling over the Ethernet" |
| **RAG** (transcribed as "log") | Retrieval-Augmented Generation | "the log technology has been introduced. Nowadays, many AI providers are looking into the log technology to bring the wider and the broad database" - transcript mis-transcription of "RAG" |
| **hybrid switch** | Switch converting PCIe to CXL or Ethernet to CXL | "the switch can have a function to convert from the PCIe to CXL" / "Ethernet to CXL, that's more considered a hybrid switch also" |
| **combo** | Combined Ethernet+CXL switch | "you can call that as a combo" - Jerry's naming |
| **pull in** | Move a schedule earlier | "we are trying to pull in our 256 gigabytes to within Q4 next year" |

---

## 6. Expression Database

```yaml
# ── Hedge / Deflection (Intel) ──
- id: m32-001
  expression: "we don't have our POR aligned"
  category: official_non_commit
  function: hedge_gap_statement
  speaker_role: partner
  difficulty: 5
  context: "I think the quick comment is we don't have our POR aligned"
  note: "POR = Plan of Record. 'we don't have a POR yet' is the professional non-commit. 'yet' implies future decision."

- id: m32-002
  expression: "from an Intel standpoint, officially, we don't have a POR yet. We don't have a commit yet on our side"
  category: official_non_commit
  function: double_hedge
  speaker_role: partner
  difficulty: 5
  context: "from an Intel standpoint, officially, we don't have a POR yet. We don't have a commit yet on our side that we're going to do it"
  note: "Double hedge - 'POR yet' + 'commit yet'. 'officially' separates personal view from company view."

- id: m32-003
  expression: "But I just upfront can say, I think we should focus on that"
  category: personal_endorsement
  function: soft_support
  speaker_role: partner
  difficulty: 4
  context: "But I just upfront can say, I think we should focus on that. And that's what we're looking at internally"
  note: "Personal endorsement after official non-commit. 'upfront' = 'honestly/preemptively'."

- id: m32-004
  expression: "The trend today is that our future product will probably have, we hope, X"
  category: aspirational_hedge
  function: trend_signal
  speaker_role: partner
  difficulty: 5
  context: "The trend today is that our future product will probably have, we hope, CXL4 or PCIe Gen 7"
  note: "Three-layer hedge: 'probably' + 'we hope' + technical justification ('feed the pipe')."

- id: m32-005
  expression: "between Jenny and myself, we don't really have anything official to talk about yet"
  category: team_hedge
  function: spread_responsibility
  speaker_role: partner
  difficulty: 5
  context: "But officially, between Jenny and myself, we don't really have anything official to talk about yet"
  note: "Naming colleague in the hedge spreads responsibility and signals where the real decision lives."

- id: m32-006
  expression: "Truthfully, it's not a lot of months away. It's a little over a quarter away."
  category: time_minimize
  function: delay_soften
  speaker_role: partner
  difficulty: 4
  context: "Truthfully, it's not a lot of months away. It's a little over a quarter away. We'll have a decision"
  note: "'Truthfully' builds trust. 'a little over a quarter' sounds shorter than 'three months'."

- id: m32-007
  expression: "we're hoping to make our POR decision for X around end of Y"
  category: decision_timeline
  function: aspirational_date
  speaker_role: partner
  difficulty: 4
  context: "we're hoping to make our POR decision for Coral Rapids. End of this year"
  note: "'hoping to make' - aspirational, not committed. Never 'we will decide' - always 'we're hoping to make'."

- id: m32-008
  expression: "We know it's not going to be for X"
  category: negative_certainty
  function: ruled_out_stating
  speaker_role: partner
  difficulty: 3
  context: "We know it's not going to be for Diamond Rapids"
  note: "State what's ruled out clearly. Negative certainty builds trust - you're honest about what you CAN'T do."

- id: m32-009
  expression: "we're doing a lot of pathfinding, but as far as like an official, this is what we're going to do, we will have a decision at the end of this year"
  category: pathfinding_hedge
  function: pre_decision_stating
  speaker_role: partner
  difficulty: 4
  context: "we have a lot of look at it. We're doing a lot of pathfinding, but as far as like an official, this is what we're going to do, we will have a decision at the end of this year"
  note: "'pathfinding' is the pre-POR exploration. Distinguishes exploration from commitment."

# ── Roadmap / Ambition (SK) ──
- id: m32-010
  expression: "we are trying to pull in our X to within Y"
  category: roadmap_ambition
  function: pull_in_stating
  speaker_role: presenter
  difficulty: 4
  context: "we are trying to pull in our 256 gigabytes to within Q4 next year"
  note: "'trying to pull in' - ambition hedge. Shows effort without over-promising."

- id: m32-011
  expression: "Actually, our sales schedule will be X, but we will try to pull in within Y"
  category: roadmap_honest
  function: ambition_with_honesty
  speaker_role: presenter
  difficulty: 4
  context: "Actually, our sales schedule will be January of 2027, but SK hynix will try to pull in within Q4 2026"
  note: "Admit official schedule first, then re-state pull-in attempt. Honest + ambitious."

- id: m32-012
  expression: "we will send the EVB to X in Y"
  category: deliverable_commit
  function: concrete_schedule
  speaker_role: presenter
  difficulty: 3
  context: "we will send the EVB to Intel in November"
  note: "Supplier-side commit. 'we will send' - no hedge when you're the supplier."

- id: m32-013
  expression: "we would like to know the Intel SK hynix 4.0 plan"
  category: roadmap_probe
  function: partner_plan_inquiry
  speaker_role: presenter
  difficulty: 3
  context: "we would like to know the Intel SK hynix 4.0 plan. Is that with the PCHN7 or not, we would like to discuss this one later?"
  note: "'we would like to know' - polite but direct ask for partner's roadmap."

- id: m32-014
  expression: "we would like to discuss this one later"
  category: deferral_sk
  function: agenda_park
  speaker_role: presenter
  difficulty: 3
  context: "Is that with the PCHN7 or not, we would like to discuss this one later?"
  note: "Park a topic for later. Useful when current meeting isn't the right forum."

# ── Polite Challenge / Probe ──
- id: m32-015
  expression: "I just wanted to confirm"
  category: reality_check
  function: validate_understanding
  speaker_role: questioner
  difficulty: 3
  context: "That's what I was thinking too. I just wanted to confirm."
  note: "Gentlest possible challenge. 'I think I know, but let me check'."

- id: m32-016
  expression: "What is the latest of the X?"
  category: status_probe
  function: progress_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "What about the latest of the PCIe Gen 7 itself? Do you know the information? What is the latest of the PCIe Gen 7?"
  note: "Asks for current state, not commitment. Less aggressive than 'when will it be done?'"

- id: m32-017
  expression: "What's the X of Y compared to Z? Is it in A or B?"
  category: comparative_probe
  function: range_check
  speaker_role: questioner
  difficulty: 4
  context: "What's the latency of RDMA compared to CXL? Is it in milliseconds or microseconds?"
  note: "Multiple-choice probe - lets partner pick the precision. Shows you've already thought about it."

- id: m32-018
  expression: "What's the thermal characteristics of that? It looks like it Y."
  category: direct_technical
  function: physical_concern
  speaker_role: questioner
  difficulty: 3
  context: "What's the thermal characteristics of that? It looks like it gets pretty hot."
  note: "Direct technical observation - no softening needed for physical reality."

- id: m32-019
  expression: "Are we in line to get the X for Y?"
  category: eligibility_check
  function: polite_status
  speaker_role: questioner
  difficulty: 4
  context: "Are we in line to get the CXL, your CXL3 devices for Diamond Rapids?"
  note: "'Are we in line to get' = 'are we on the list?' Respects partner's process."

- id: m32-020
  expression: "Is your question a spec-related or?"
  category: question_scope
  function: answer_scoping
  speaker_role: receiver
  difficulty: 4
  context: "Is your question a spec-related or? Are you asking the bandwidth for it?"
  note: "Defensive technique: scope the question before answering. 'What kind of answer do you want?'"

# ── Action Item / Follow-up ──
- id: m32-021
  expression: "we should take an action item to make sure that someone reviews X"
  category: action_assignment
  function: org_commit_no_owner
  speaker_role: partner
  difficulty: 4
  context: "I think from an Intel side, we should take an action item to make sure that someone reviews the back plane and looks at the card to make sure that they work well"
  note: "'someone' - assigns org action without naming the person. Commits without personal ownership."

- id: m32-022
  expression: "We need to make a note and then when the time comes, then we need to make sure we are compatible"
  category: future_action
  function: deferred_action
  speaker_role: partner
  difficulty: 3
  context: "We need to make a note and then when the time comes, then we need to make sure we are compatible and if not, then what needs to be done?"
  note: "'make a note' is lighter than 'take an action item'. 'when the time comes' - defers to future trigger."

- id: m32-023
  expression: "send the slides out. Send the questions that X is looking at"
  category: directive_imperative
  function: follow_up_assign
  speaker_role: facilitator
  difficulty: 2
  context: "Sandosh, send the slides out. Send the questions that SK, your RDIM is looking at"
  note: "Direct imperative - when you're the facilitator, be direct. No hedging on logistics."

- id: m32-024
  expression: "I'm going to put a lot of emphasis on Ivan and Ed and Jenny to help out here, but I'll be available too"
  category: team_assignment
  function: ownership_spread
  speaker_role: partner
  difficulty: 4
  context: "I'm going to put a lot of emphasis on Ivan and Ed and Jenny to help out here, but I'll be available too and we'll talk about it in two weeks"
  note: "Name the team + stay available. Spreads work while keeping yourself in the loop."

- id: m32-025
  expression: "we better keep giving a presentation of this X two weeks later"
  category: cadence_propose
  function: next_meeting
  speaker_role: presenter
  difficulty: 3
  context: "we better keep giving a presentation of this Divina slide two weeks later"
  note: "'we better' - soft proposal. 'two weeks later' - concrete cadence."

- id: m32-026
  expression: "in two weeks on the 17th, maybe you can bring your slides from your side and question and we can have a discussion now"
  category: date_confirm
  function: concrete_follow_up
  speaker_role: partner
  difficulty: 3
  context: "then we will have minutes and maybe in two weeks on 17th, maybe you can bring your slides from your side and question and we can have a discussion now"
  note: "Always pair 'two weeks' with a concrete date ('the 17th'). Vague cadence = no commitment."

- id: m32-027
  expression: "Sounds good. Sounds good. Good plan."
  category: triple_confirm
  function: mutual_close
  speaker_role: both
  difficulty: 2
  context: "Sounds good. Sounds good. Good plan. Thank you. Great slides."
  note: "Triple confirmation both sides heard the same plan. Compliment close: 'Great slides'."

# ── Standardization / Request ──
- id: m32-028
  expression: "we will follow the X standardization about Y"
  category: standard_align
  function: spec_commit
  speaker_role: presenter
  difficulty: 3
  context: "we will follow the ZX standardization about the CXL3.1"
  note: "Commit to standardization. 'ZX' likely mis-transcription of 'CXL' or 'JEDEC'."

- id: m32-029
  expression: "Please check the ability of this one"
  category: polite_request
  function: feasibility_ask
  speaker_role: presenter
  difficulty: 3
  context: "we don't have the TMR CRB until maybe next year. So please check the ability of this one"
  note: "'check the ability' = 'check feasibility'. Polite ask when requesting partner support."

- id: m32-030
  expression: "we would like to find the granularity of the PDK available"
  category: spec_request
  function: detail_inquiry
  speaker_role: presenter
  difficulty: 4
  context: "we would like to find the find granularity of the PDK available"
  note: "'granularity of the PDK' - asks for level of detail in the PDK. Technical vocabulary for 'how much detail will you share?'"

# ── Use Case Framing ──
- id: m32-031
  expression: "As you know, the many end-user are focusing on X"
  category: shared_ground
  function: assume_knowledge
  speaker_role: presenter
  difficulty: 3
  context: "As you know, the many end-user are focusing on the memory intensive work code and the in-memory database"
  note: "'As you know' assumes shared knowledge - sets common ground before the ask."

- id: m32-032
  expression: "The first approach... The second approach..."
  category: enumeration
  function: parallel_structure
  speaker_role: presenter
  difficulty: 2
  context: "That's the first approach. The second approach, nowadays, the many industry are looking at the memory-centric approach"
  note: "Parallel 'The first / The second' - clean enumeration. Use for any two-option comparison."

- id: m32-033
  expression: "In order to solve these problems, the X technology has been introduced"
  category: causal_framing
  function: problem_solution
  speaker_role: presenter
  difficulty: 3
  context: "In order to solve these problems, the log technology has been introduced"
  note: "'In order to solve X, Y has been introduced' - causal framing. 'log' = RAG (transcript error)."

- id: m32-034
  expression: "I think that the X can be along with the Y for Z"
  category: architecture_vision
  function: integration_proposal
  speaker_role: presenter
  difficulty: 4
  context: "I think that the pooling memory can be along with the log technology and log solution for the AI data infrastructure"
  note: "'I think that X can be along with Y' - propose integration without committing. Visionary tone."

- id: m32-035
  expression: "It's kind of thing and this kind of approach has been introduced and discussed in the industry with X over Y"
  category: industry_validation
  function: trend_backing
  speaker_role: presenter
  difficulty: 3
  context: "this kind of approach has been introduced and discussed in the industry with the pooling system over this interconnect"
  note: "Industry validation - 'this has been discussed in the industry' backs your proposal with external momentum."

# ── Technical Justification ──
- id: m32-036
  expression: "we have to have it to be able to feed the pipe"
  category: technical_justification
  function: necessity_stating
  speaker_role: partner
  difficulty: 4
  context: "That we have to have it to be able to feed the pipe"
  note: "'feed the pipe' - keep the data path full. Technical idiom for 'we need more bandwidth'."

- id: m32-037
  expression: "suddenly that bandwidth is starting to be appealing"
  category: value_emergence
  function: feature_value
  speaker_role: partner
  difficulty: 3
  context: "where you can go 128 gig and you can interleave them and you can bundle link them, suddenly that bandwidth is starting to be appealing"
  note: "'suddenly X is starting to be appealing' - value emerges when features combine. Use to build enthusiasm."

- id: m32-038
  expression: "It makes sense"
  category: agreement_light
  function: mild_approve
  speaker_role: partner
  difficulty: 2
  context: "It makes sense. Yeah, I'm between this. I'm between."
  note: "'It makes sense' = light agreement. Often followed by a hedge ('I'm between')."

# ── Practicality / Adoption ──
- id: m32-039
  expression: "if we become too futuristic, it just doesn't adopt"
  category: adoption_realism
  function: realism_warn
  speaker_role: partner
  difficulty: 4
  context: "This is right because what happens is if we become too futuristic, it just doesn't adopt. It takes too long to adopt"
  note: "'too futuristic' = ahead of market. Pragmatic engineering wisdom - timing matters as much as technology."

- id: m32-040
  expression: "for data center, everything needs to be scalable. If this technology is not scaling, I don't think data center is going to adopt"
  category: scalability_rule
  function: adoption_criterion
  speaker_role: partner
  difficulty: 4
  context: "for data center, everything needs to be scalable. If this technology is not scaling, I don't think data center is going to adopt"
  note: "Scalability as adoption criterion. State the criterion, then judge the tech against it."

- id: m32-041
  expression: "the ecosystem also wants everything cheap. It's like everyone wants everything"
  category: market_constraint
  function: tension_state
  speaker_role: partner
  difficulty: 4
  context: "Well, unfortunately, the ecosystem also wants everything cheap. It's like everyone wants everything. They want cheap memory. They want high capacity. They complain if the latency is high"
  note: "Triple-list the wants to show the impossible constraint. 'something's got to bend a little bit' = compromise is inevitable."

- id: m32-042
  expression: "something's got to bend a little bit"
  category: compromise_signal
  function: trade_off_accept
  speaker_role: partner
  difficulty: 4
  context: "I mean, so at some point, something's got to bend a little bit"
  note: "'something's got to bend' = compromise is needed. Use to set up a trade-off discussion."

- id: m32-043
  expression: "it will be interesting in the future to see how this plays out"
  category: open_future
  function: neutral_forecast
  speaker_role: partner
  difficulty: 3
  context: "But basically, it will be interesting in the future to see how this plays out"
  note: "Neutral forecast - no prediction, just interest. Use when you don't want to take a position."

# ── Comprehension / Clarification ──
- id: m32-044
  expression: "let's discuss about how we can validate it to your port functionally"
  category: validation_propose
  function: test_method
  speaker_role: partner
  difficulty: 3
  context: "I mean, let's discuss about how we can validate it to your port functionally. Yeah. In the platform, yeah, PDK perspective"
  note: "'let's discuss about how we can validate X' - propose validation method as discussion topic."

- id: m32-045
  expression: "the software would determine what's a pre-fill versus a decode worker"
  category: architecture_clarify
  function: role_split
  speaker_role: partner
  difficulty: 3
  context: "your different pools here, I mean, the software would determine what's a pre-fill versus a decode worker, right?"
  note: "Clarifying role split. 'right?' tag seeks confirmation."

- id: m32-046
  expression: "in my head, it's one pool. The software just carves out pre-fill and decode"
  category: mental_model
  function: own_understanding
  speaker_role: partner
  difficulty: 3
  context: "Or what you're describing here looks like two different pools, but in my head, it's one pool. The software just carves out pre-fill and decode"
  note: "'in my head, it's X' - state your mental model. Polite pushback when your model differs."

- id: m32-047
  expression: "I'm between this. I'm between."
  category: undecided_signal
  function: position_state
  speaker_role: partner
  difficulty: 3
  context: "Yeah, I'm between this. I'm between."
  note: "Honest 'I'm undecided' signal. Rare and respected - shows intellectual honesty."

# ── Closing / Meta ──
- id: m32-048
  expression: "Just time check. We have three minutes and maybe you want to cover some quick reports"
  category: time_management
  function: pace_check
  speaker_role: facilitator
  difficulty: 3
  context: "Just time check. We have three minutes and maybe you want to cover some quick reports"
  note: "Polite time check. 'Just time check' + state remaining + suggest action. Never 'we're out of time'."

- id: m32-049
  expression: "I think we don't have enough time today. So we better keep giving a presentation of this X two weeks later"
  category: defer_remaining
  function: agenda_carry
  speaker_role: presenter
  difficulty: 3
  context: "I think we don't have enough time today. So yeah, we better keep giving a presentation of this Divina slide two weeks later"
  note: "Defer remaining content to next meeting. 'we better keep giving' - propose continuation."

- id: m32-050
  expression: "we need to make sure we're all aligned here"
  category: alignment_stating
  function: shared_goal
  speaker_role: partner
  difficulty: 3
  context: "we need to make sure we're all aligned here, but then we'll go and we'll look at trying to answer every question you have"
  note: "'we need to make sure we're all aligned' - state shared goal. Unifies both sides before action items."

# ── Audio Confirm / Logistics ──
- id: m32-051
  expression: "Can you guys hear me, by the way?"
  category: audio_check
  function: logistics_check
  speaker_role: any
  difficulty: 1
  context: "One quick question of the EVBs. Can you guys hear me, by the way? Yes. Yes. The microphone didn't work earlier"
  note: "Audio check mid-meeting. 'by the way' softens the interruption."

- id: m32-052
  expression: "About what volume of these are you thinking of? Just a few samples or is it a large quantity?"
  category: quantity_probe
  function: scale_inquiry
  speaker_role: partner
  difficulty: 3
  context: "About what volume of these are you thinking of? Just a few samples or is it a large quantity? Just a few samples"
  note: "Multiple-choice quantity probe. 'few samples or large quantity' - lets partner pick the bucket."

- id: m32-053
  expression: "So just keep that in mind when we need to have a X to Y connector for each of these"
  category: compatibility_note
  function: future_warning
  speaker_role: partner
  difficulty: 3
  context: "just keep that in mind when we need to have a 5x4 to 5x8 connector for each of these"
  note: "'keep that in mind' - flag for future attention without action item. Softer than 'make a note'."

- id: m32-054
  expression: "Yeah, that's all from me. Any other comments?"
  category: turn_close
  function: open_floor
  speaker_role: presenter
  difficulty: 2
  context: "That's all from me. Any other comments?"
  note: "Simple close + open floor. Use at end of your section."

- id: m32-055
  expression: "That's the reason why we are coming here and wanting to hear about your plan"
  category: meeting_purpose
  function: intent_stating
  speaker_role: presenter
  difficulty: 3
  context: "That's the reason why we are coming here and wanting to hear about your plan"
  note: "State meeting purpose directly. 'wanting to hear about your plan' - sets expectation for partner."

- id: m32-056
  expression: "we'll go and we'll look at trying to answer every question you have"
  category: response_commit
  function: thorough_response
  speaker_role: partner
  difficulty: 3
  context: "we need to make sure we're all aligned here, but then we'll go and we'll look at trying to answer every question you have"
  note: "'try to answer every question' - commits to thoroughness without committing to specific answers."
```

---

## 7. Excerpt Map (Mon-Fri Shadowing)

Audio: `repo/webex-audio/2025-09-04 08 32 11_EN_Intel-extracted.wav` (total ~32 minutes, 3,387 words)
5 recommended excerpts for weekly rotation.

| # | Time (est) | Line range | Content summary | Learning point | Shadowing difficulty |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 00:00-03:00 | line 1-21 | SK use case framing: in-memory DB, RAG (transcribed "log"), KV cache, memory pooling | Use case enumeration: "The first approach... The second approach..." / "As you know" | ★★☆ |
| 2 | 03:00-07:00 | line 28-78 | Hybrid switch discussion: PCIe-CXL, Ethernet-CXL combo, latency probe, RDMA vs CXL, adoption realism | Polite probe: "What's the latency of X compared to Y? Is it in A or B?" / "if we become too futuristic, it just doesn't adopt" | ★★★ |
| 3 | 07:00-13:00 | line 145-205 | SK roadmap pull-in (256GB Q4 2026) + Intel hedge ladder on CXL4/Gen7 ("we don't have a POR yet") | Hedge ladder: "we don't have our POR aligned" -> "we know it's not going to be for X" -> "the trend today is... we hope" -> "we don't have a commit yet" -> "But I think we should focus on that" | ★★★★ |
| 4 | 13:00-20:00 | line 217-280 | CXL3.1 2nd gen CMM-EXP, thermal concern, dual port 2x4, backplane compatibility action item | Direct probe: "What's the thermal characteristics of that?" / Action item: "we should take an action item to make sure that someone reviews the back plane" | ★★★★ |
| 5 | 20:00-32:00 | line 300-346 | EVB volume question, 5x4 vs 5x8 connector mismatch, follow-up schedule, triple confirmation close | Follow-up negotiation: "in two weeks on the 17th" / "I'm going to put a lot of emphasis on Ivan and Ed and Jenny" / "Sounds good. Sounds good. Good plan." | ★★★ |

**Usage**:
- Mon: Excerpt 1, Tue: Excerpt 2, Wed: Excerpt 3, Thu: Excerpt 4, Fri: Excerpt 5
- Daily 20-min routine: insert excerpts into slots 1-6
- Excerpts 3 and 4 are highest value - hedge ladder + action item assignment are dense and immediately usable

---

## 8. Audrey's Teaching Notes

### Register (speech style) Analysis

This is a **roadmap alignment + technical probe** register. Two distinct sub-registers:

- **SK presenter register**: Use case framing -> roadmap commit -> deliverable dates. Uses "we will" / "we are trying to pull in" / "we would like to know." Supplier-side - confident on own roadmap, deferent on partner's plan.
- **Intel partner register**: Hedge ladder on decisions, direct on technical observations. Uses "we don't have a POR yet" / "the trend today is... we hope" / "Truthfully, it's not a lot of months away." Customer-side - non-committal on roadmap, engaged on technical detail.

The key dynamic: SK wants Intel's CXL4/Gen7 commitment; Intel cannot give it. The whole meeting is SK probing and Intel hedging, with both sides preserving the relationship.

### Pragmatics Core

1. **"POR" as the central hedge term**: "Plan of Record" is Intel-internal vocabulary that signals "official commitment." "We don't have a POR yet" is the professional non-commit. "Yet" carries the promise of future decision. Learn this term - it's used across Intel, AMD, and other US semiconductor partners.

2. **Personal vs. official separation**: Intel Santosh repeatedly separates his personal view from Intel's official position. "From an Intel standpoint, officially, we don't have a POR yet. But I just upfront can say, I think we should focus on that." This two-track language (official=no, personal=yes) preserves both the company position and the relationship. **Always separate "officially we don't have X" from "personally I think Y."**

3. **Naming colleagues in hedges**: "Between Jenny and myself, we don't really have anything official to talk about yet." Naming a colleague in the hedge does two things: (a) shows you're not sole decision-maker, (b) signals where the real decision lives. This is honest and useful for the partner.

4. **"We're hoping to make our POR decision"**: Never "we will decide." Always "we're hoping to make a decision." The "hoping to make" construction is the aspirational timeline - it gives a date without committing to the decision itself.

5. **Triple confirmation close**: "Sounds good. Sounds good. Good plan. Thank you. Great slides." - both sides confirm the same plan three times. This is not redundancy - it's mutual verification that both heard the same follow-up. Always close with triple confirmation + compliment.

### Top 5 Must-Use

1. **"We don't have a POR yet. But I think we should focus on that."** - Official non-commit + personal endorsement. Use when you can't commit but want to stay encouraging.
2. **"we are trying to pull in our X to within Y"** - Ambition hedge. Shows effort without over-promising.
3. **"We should take an action item to make sure that someone reviews X"** - Assign org action without personal ownership.
4. **"in two weeks on the 17th"** - Always pair relative time with concrete date. Vague cadence = no commitment.
5. **"What's the X of Y compared to Z? Is it in A or B?"** - Multiple-choice probe. Shows you've thought about it, lets partner pick precision.

### Korean vs. English Comparison

| Korean style | English (this meeting) | Difference |
|:---|:---|:---|
| "아직 결정 안 됐습니다" | "We don't have a POR yet" | Korean ends at "not decided"; English adds "yet" (implying future) |
| "내부 검토 후 결정하겠습니다" | "We're hoping to make our POR decision around end of this year" | Korean passive; English "hoping to make" is active aspiration |
| "개인적으로는 좋다고 생각합니다" | "But I just upfront can say, I think we should focus on that" | English separates "officially" from "personally upfront" |
| "일정을 앞당기려고 합니다" | "we are trying to pull in our X to within Y" | English "trying to pull in" shows effort without promise |
| "다음 회의에서 논의하죠" | "we better keep giving a presentation of this X two weeks later" | English adds "we better" (soft proposal) + concrete date |
| "확인해 보겠습니다" | "we should take an action item to make sure that someone reviews X" | English "action item" + "someone" assigns org without personal ownership |
| "다 들립니까?" | "Can you guys hear me, by the way?" | "by the way" softens the interruption |

---

## 9. How to Use This Textbook

1. **Daily 20-min routine**: Use Section 7's 5 excerpts, rotating Mon-Fri. Excerpts 3 and 4 (hedge ladder + action item) are highest priority.
2. **Expression DB**: Of the 56 expressions, prioritize Section 8's Top 5 first. Then study the hedge cluster (m32-001 to m32-009) - these are the most reusable across any partner meeting where you can't commit.
3. **Audrey Friday correction**: This week's dump should focus on Section 2 (Intel's hedge ladder). Practice the 5-rung sequence: state gap -> state what's known -> state trend with "probably, we hope" -> re-state no commit with "yet" -> personal endorsement.
4. **Comparison learning**: Use Section 8's Korean-vs-English table. The key shift is from passive ("검토하겠습니다") to active aspiration ("we're hoping to make our POR decision") - English expects you to sound like you WANT the decision, even when you can't make it.
5. **Role-play**: Practice both sides. (a) SK side: "we are trying to pull in" + "we would like to know Intel's CXL4 plan." (b) Intel side: "we don't have a POR yet" + "the trend today is... we hope" + "But I think we should focus on that." Both registers are needed in real partner meetings.

---

*Textbook 32 - Intel (2025-09-04) CXL Roadmap & Memory Pooling Deep-Dive. Type A (technical deep-dive). Expression DB 56 entries. 5 excerpt segments. Written: 2026-09-01.*
