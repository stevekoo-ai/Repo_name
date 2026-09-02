---
textbook_id: 34
meeting: AMDCXLsync
date: 2025-07-23
type: A (기술 Deep-dive)
partner: AMD (Rita + AMD host architect)
sk_side: CXL System Architecture, Viva, Thomas, Katon (signed off before close)
duration_words: 3720
audio: repo/webex-audio/2025-07-23 08 29 22_EN_AMDCXLsync-extracted.wav
transcript: repo/webex-audio/2025-07-23 08 29 22_EN_AMDCXLsync-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, amd, cxl, read-latency, hybrid-memory, protocol, technical-deepdive]
---

# Textbook 34 - AMD CXL sync (2025-07-23)

> **회의 유형**: A (기술 Deep-dive) - SK Hynix가 CXL read latency reporting proposal 발표, AMD가 protocol/host architecture 관점에서 기술 도전
> **학습 가치**: 발표자의 proposal framing, 응답자의 정중한 기술 pushback, brainstorm marker 화법, action item 분배
> **Audrey 관점**: 이 회의는 "proposal pitch + technical defense"의 전형. AMD 아키텍처는 네가 proposal을 내놓을 때 partner가 어떻게 도전하는지 보여준다. 특히 "I'm thinking aloud here, so I'm going to say garbage here for a minute" 같은 brainstorm marker는 영어 고급 화법이다.

---

## 1. 발화 아키텍처 - 발표자(SK)의 proposal 설계 (5단계)

SK 측 발표자는 CXL consortium에 제출할 proposal을 AMD와 사전 리뷰하는 자리다. 발표는 5단계 구조로 설계된다.

### 단계 1: 문제 프레이밍 (Problem Framing)

제품 기능을 설명하기 전에 "host가 알 수 없는 것"으로 문제를 격상한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `in the hybrid CXL system, host could not figure out X` | "As you know, in the hybrid CXL system, host could not figure out how long the read latency will take." | "host가 알 수 없다" - 불확실성 강조 |
| `we propose our proposal is to X` | "So we propose our proposal is to notify host can host the latency of read latency notify." | proposal 공식 - "we propose our proposal is to" (중복적이지만 한국인 발표자에겐 안전한 공식) |
| `So host can improve utilization by X when Y` | "So host can improve utilization by task switching when the long latency is expected." | benefit 연결 - "So host can X by Y when Z" |

**Audrey 교훈**: "host could not figure out X" - 이 "could not figure out"이 문제 프레이밍의 핵심이다. "X can't do Y"가 아니라 "X could not figure out Y"로 표현하면, 기술적 한계를 인지적 문제로 프레이밍한다. "알 수 없다"가 "안 된다"보다 proposal의 당위성을 높인다.

### 단계 2: 선행 제약 인정 (Prior Constraint Acknowledgement)

새 proposal을 설명하기 전에 이전 회의에서 partner가 제기한 constraint를 먼저 인정한다. 이게 신뢰를 만든다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `X had comment about Y in the previous meeting` | "And Rita had comment about CCI in the previous meeting." | 선행 발언 회상 - partner 의견 존중 |
| `So we have constraint about X integration` | "So we have constraint about CCI integration." | 제약 명시 - "we have constraint about X" |

**Audrey 교훈**: 발표 중반에 "X had comment about Y in the previous meeting"을 끼워 넣어라. 이 한 마디가 "나는 네 말을 기억하고 있고, 반영했다"는 신호다. partner는 자기 의견이 반영됐는지를 가장 민감하게 본다.

### 단계 3: 기술적 이유 나열 (Technical Reasoning)

왜 기존 mechanism이 안 되는지, "There is no mechanism to..."로 시작한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `There is no mechanism to X in real time` | "There is no mechanism to report actual latency in real time." | 부정적 진술 - gap 명시 |
| `There are some X features, A, B` | "There are some latency features, media execution time, and maintenance operation time." | 현존 기능 나열 - 비교 우위 설정 |
| `So it could not show X in real time` | "So it could not show the actual read latency in real time." | 결론 - "could not show" |
| `When using X, it's not possible to predict whether Y or not` | "When using hybrid CXL memory, it's not possible to predict whether a DRAM cache hit or not." | 불확실성 정식화 |

**Audrey 교훈**: "There is no mechanism to X" - 이 표현이 gap을 만드는 공식이다. "We need X"라고 하기 전에 "There is no mechanism to X"로 gap을 먼저 보여라. 그래야 제안의 당위성이 생긴다.

### 단계 4: 결론 (Conclusion)

제약를 종합하여 "cannot be integrated"로 결론.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So I think the X feature cannot be integrated into Y` | "So I think the latency report feature cannot be integrated into CCI." | 부정 결론 - "cannot be integrated" |

### 단계 5: 피드백 초청 (Feedback Invitation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So I'll buy your thoughts on this.` | "So I'll buy your thoughts on this." | "I'll buy your thoughts" - 의견 수용 표현 |

**Audrey 교훈**: "I'll buy your thoughts on this"는 한국인이 거의 모르는 고급 표현이다. "What do you think?"보다 격식 있고, "I'd like your feedback"보다 partner를 존중하는 뉘앙스다. "buy"가 "accept/take" 의미로 쓰였다. 회의에서 의견을 구할 때 무조건 써라.

### 보너스: 재설명 요청시 (When Asked to Re-explain)

AMD 측이 "Sorry, I missed understanding that bit"라고 하자, SK 발표자는 이렇게 대응한다:

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Maybe can you walk through again from slide X, that will be better, like just to refresh.` | "Maybe can you walk through again from slide two, that will be better, like just to refresh." | 재설명 권유 - "just to refresh"가 부드럽게 |

---

## 1b. 발화 아키텍처 - AMD 응답자의 5단계 기술 도전 (가장 중요)

이 회의의 **진짜 학습 가치**. AMD 아키텍처 담당자가 proposal을 어떻게 정중하게 도전하는지. 네가 AMD 입장이 되어 partner proposal을 리뷰할 때, 또는 SK 입장에서 partner 도전을 받을 때 모두 배워야 한다.

### 단계 1: 명확화 질문 (Clarifying Probe)

도전을 시작할 때 "Why do you think...?"로 partner 논리의 빈 곳을 탐색한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So sorry, I followed you till the last point. Why do you think it cannot be X?` | "So sorry, I followed you till the last point. Why do you think it cannot be integrated in CCI?" | 부분 이해 인정 + "Why do you think" 도전 |
| `in what X or in what Y you think that Z can be included?` | "in what command or in what packet you think that this Devload can be included?" | 구체적 위치 요구 - proposal의 빈 곳 탐색 |

**Audrey 교훈**: "I followed you till the last point"로 먼저 경청을 표시한 뒤 "Why do you think X?"로 도전한다. "Why do you think"은 "Why is X"보다 훨씬 정중하다 - 상대의 추론을 묻는 것이지 사실을 부정하는 게 아니기 때문.

### 단계 2: 직접 기술 교정 (Direct Technical Correction)

논리가 꺾이는 지점을 "That's going to be wrong from the X perspective"로 짚는다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So that's going to be wrong from the X perspective also.` | "So that's going to be wrong from the protocol perspective also." | "also" 부사로 완화 - 직접 교정 |
| `Even for X, it will be wrong.` | "Even for type two, it will be wrong." | 일반화 - "Even for X"로 범위 확장 |
| `The X cannot precede the Y by this much amount.` | "The completion cannot precede the data by this much amount." | protocol 위반 지적 - "cannot precede" |
| `That's all I'm trying to say.` | "That's all I'm trying to say." | 도전 의도 명시 - 공격이 아님을 표시 |

**Audrey 교훈**: "That's going to be wrong from the X perspective also" - "from the X perspective"로 한정하면 직접 공격이 아니다. "Y is wrong"이 아니라 "from the protocol perspective, Y is wrong" - 관점을 명시하면 부드럽다. 그리고 "also"를 붙여 "이것도 (다른 것과 마찬가지로) 문제다"로 만든다.

### 단계 3: 효율성 논증 (Efficiency Argument)

기술적 정당성 다음에는 비용/효율로 도전한다. "If you are going to X, that's going to be a lot of Y" 구조.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If you are going to get another X for every Y, that's going to be a lot of Z being consumed.` | "If you are going to get another S2M packet for every read, that's going to be a lot of link bandwidth being consumed." | 비용 논증 - "a lot of X being consumed" |
| `That will impact the X and overall Y.` | "That will impact the flit efficiency and overall link efficiency." | 영향 명시 |
| `If the only purpose of that X is going to be Y, I think that's a big overhead.` | "If the only purpose of that packet is going to be communicating latency, I think that's a big overhead." | 단일 목적 비용 - "big overhead" |

**Audrey 교훈**: "If the only purpose of X is going to be Y, I think that's a big overhead" - 이게 영어 기술 회의에서 가장 자주 쓰이는 비용 도전 공식이다. "only purpose"로 단일성을 강조하고, "big overhead"로 비용을 명시한다. 한국어로는 "그거 하는 데 비용이 너무 큽니다"인데, 영어는 "If the only purpose... that's a big overhead"로 조건문 형태로 말한다.

### 단계 4: 대안 제시 (Alternative Suggestion)

효율 문제를 지적한 후 "perhaps you might be able to"로 대안을 제시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `perhaps you might be able to X with Y anyways, right?` | "perhaps you might be able to decouple this with Devload anyways, right?" | "perhaps" + "might" + "anyways" + "right?" - 4중 완화 |
| `Instead, if you look at the X, the way X is communicated is Y` | "Instead, if you look at the Devload, the way Devloads are communicated is Devloads are sent along anything that the device is indicating to the host." | 대안 설명 - "the way X is communicated is Y" |
| `So they are not separate packets. They're just shoved along anything that's going to the host.` | "So they are not separate packets. They're just shoved along anything that's going to the host." | informal 설명 - "shoved along" (덩달아 보냄) |
| `It is just more of a level indication.` | "It is just more of a level indication." | 비유 - "more of a X" |

**Audrey 교훈**: "perhaps you might be able to X anyways, right?" - 이 "anyways, right?"가 제안을 부드럽게 만든다. "anyways"가 "어차피 그렇게 할 수 있잖아" 뉘앙스. 제안이 명령이 아니라 observation이 되게 만든다. 그리고 "the way X is communicated is Y" - 이게 설명 구조다. "X는 Y렇게 소통된다" - mechanism 설명할 때 써라.

### 단계 5: Brainstorm Mode 전환 (Explicit Brainstorm Disclaimer)

기술 도전 후 "I'm thinking aloud here"로 brainstorm mode임을 명시하고, 아이디어를 자유롭게 던진다. 이게 영어 고급 화법이다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Just for the conversation purposes, let's say your X is Y and Z is W.` | "Just for the conversation purposes, let's say your cache hit is 100 nanosecond and cache misses 1 microsecond." | 가정 설정 - "Just for the conversation purposes" |
| `I'm thinking aloud here, so I am going to say garbage here for a minute.` | "I'm thinking aloud here, so I am going to say garbage here for a minute." | brainstorm disclaimer - "say garbage" |
| `But if there was something like X, can we do something?` | "But if there was something like posted read transaction from the host side that you issue the transaction, do you look at the buffers whenever the read response comes back from the device? Can we do something?" | 가정식 질문 - "if there was something like X" |
| `And again, as I said, I started thinking aloud here, so I'm still on my speaking garbage mode.` | "And again, as I said, I started thinking aloud here, so I'm still on my speaking garbage mode." | brainstorm 유지 - "speaking garbage mode" |
| `But that could be a useful way of doing it, as I think.` | "But that could be a useful way of doing it, as I think." | tentative endorsement - "could be... as I think" |
| `As long as we don't get too greedy on getting real time, I think, yeah, we could try to find a workaround.` | "As long as we don't get too greedy on getting real time, I think, yeah, we could try to find a workaround." | 원칙 설정 - "As long as we don't get too greedy on X" |

**Audrey 교훈**: "I'm thinking aloud here, so I'm going to say garbage here for a minute" - 이 표현이 영어 회의에서 brainstorm marker로 가장 강력하다. 자기가 말하는 것을 "garbage"로 겸하면서, 아이디어를 자유롭게 던질 수 있다. partner도 이걸 듣고 "아, 이 사람 지금 brainstorm 중이구나"하고 방어적으로 듣지 않는다. 한국어로는 "그냥 생각나는 대로 말해볼게요" 정도인데, 영어는 "say garbage here for a minute"으로 더 극적으로 자기 낮추기를 한다. 그리고 "I'm still on my speaking garbage mode"로 brainstorm가 계속됨을 표시한다. 이 패턴을 외워라.

### 단계 6: 직접 비판 + 전환 (Direct Critique + Reframe)

가끔 "you're moving the problem, you're not solving the problem"으로 직접 비판을 날린다. 그러나 바로 "if you want to solve the problem"으로 constructive 전환.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `That's just you are moving the problem, you're not solving the problem.` | "Yeah, that's just you are moving the problem, you're not solving the problem." | 직접 비판 - "moving vs solving" 대비 |
| `I think like we need to, if you want to solve the problem, whatever it says, instead of X, we need to make Y` | "I think like we need to, if you want to solve the problem, whatever it says, instead of one to one request to response relationship, we need to make one to two, one to two relationship with the question response?" | constructive 전환 - "if you want to solve the problem" |
| `Or maybe that may be heavy lifting.` | "Or maybe that may be heavy lifting." | 비용 인정 - "heavy lifting" |

**Audrey 교훈**: "you're moving the problem, you're not solving the problem" - 이게 영어 기술 회의에서 가장 강력한 direct critique 중 하나다. 그러나 바로 다음에 "if you want to solve the problem, we need to X"로 전환하면, 비판이 아니라 개선 제안이 된다. 비판 → 전환 패턴을 외워라. 그리고 "heavy lifting" - 큰 작업/비용을 의미하는 미국식 관용 표현. "그거 큰 공사다"의 영어 버전.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의에서 AMD 응답자가 약점/불확실성을 어떻게 포장하는지. 이게 네가 직접 써야 할 화법이다.

### 전략 1: 이중 hedge (Double Hedge)

확신 없는 발언을 "I think" + "I assume"으로 이중 완화한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| protocol 수정 필요성 | "even with alternative fields that we can pursue, I think the protocol flow, I think, needs modification, I assume." | "대안 필드를 쓰더라도, protocol flow는 수정이 필요할 겁니다, 제생각엔요" |

**패턴 공식**: `I think X, I think, needs Y, I assume.`

**Audrey 교훈**: "I think, I assume"의 이중 hedge는 영어 회의에서 매우 자주 쓰인다. 한국인은 "그런 것 같습니다"로 한 번에 하지만, 영어는 "I think X, I assume"로 두 번 겹쳐야 같은 겸손함이 나온다. 그러나 너무 남용하면 자신감 없게 들리니, 정말不确定할 때만 써라.

### 전략 2: Brainstorm Mode 면책 (Brainstorm Disclaimer)

부정확한 아이디어를 던지기 전에 "I'm going to say garbage"로 미리 면책한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 임시 아이디어 제시 | "I'm thinking aloud here, so I am going to say garbage here for a minute. But if there was something like posted read transaction from the host side..." | "지금 생각나는 대로 말하겠습니다. 잠시 쓸모없는 소리 좀 할게요. 그런데 만약 host 측에서 posted read transaction이라는 게 있다면..." |
| brainstorm 유지 | "And again, as I said, I started thinking aloud here, so I'm still on my speaking garbage mode." | "다시 말하지만, 지금 생각나는 대로 말하는 중이라, 아직 쓸데없는 말 모드입니다" |

**패턴 공식**: `I'm thinking aloud here, so I'm going to say garbage here for a minute. [idea]. And again, I'm still on my speaking garbage mode.`

**Audrey 교훈**: "say garbage"는 자기 아이디어를 미리 깎아내리는 고급 화법이다. partner는 "garbage"라고 들으면 방어적으로 듣지 않는다. 그리고 "speaking garbage mode"로 상태를 명시하면, 잘못된 아이디어를 던져도 체면이 안 깎인다. 한국어로는 "제가 생각나는 대로 말해볼게요"인데, 이 정도로는 충분한 disclaimer가 안 된다. "garbage"까지 내려가야 영어답다.

### 전략 3: Tentative Endorsement

아이디어를 지지하되 "could be... as I think"로 확신을 부여하지 않는다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 자기 아이디어에 대한 평가 | "But that could be a useful way of doing it, as I think." | "그게 유용한 방법이 될 수도 있을 것 같습니다" |
| 해결책 가능성 | "As long as we don't get too greedy on getting real time, I think, yeah, we could try to find a workaround." | "real time에 너무 욕심만 부리지 않는다면, workaround를 찾을 수 있을 겁니다" |

**패턴 공식**: `X could be a useful way of doing it, as I think. As long as we don't get too greedy on Y, we could try to find a workaround.`

**Audrey 교훈**: "as I think"를 문장 끝에 붙여라. "I think X could be useful"보다 "X could be useful, as I think"가 더 겸손하다. 그리고 "As long as we don't get too greedy on X" - "too greedy"는 partner의 과도한 요구를 부드럽게 제한하는 화법이다. "그거 너무 많이 요구하지 마세요"의 영어 버전.

### 전략 4: Self-Deprecating Commitment

다음 액션을 약속하되, 자기가 한 말이 완전하지 않음을 인정한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 후속 약속 | "Yeah, I'll try to give more thoughts. I think some of the details that I mentioned probably doesn't make sense this time, but I will think about that." | "좀 더 생각해 보겠습니다. 제가 말한 것 중 일부는 아마 지금은 말이 안 될 수도 있는데, 생각해 보겠습니다" |

**패턴 공식**: `I'll try to give more thoughts. Some of the details that I mentioned probably doesn't make sense this time, but I will think about that.`

**Audrey 교훈**: "I'll try to give more thoughts"는 "I'll think about it"보다 진지하다. 그리고 "some of the details that I mentioned probably doesn't make sense" - 자기 발언의 불완정성을 인정하면, partner는 "이 사람 솔직하구나"라고 믿는다. 약속과 humility를 같이 하면 신뢰가 쌓인다.

### 전략 5: Honest Knowledge Gap (솔직한 모름)

정보가 없을 때 "I don't know"가 아니라 "I'm trying to figure out what we could do"로 표현한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| host 활용 방법 모름 | "And as a host implementation, I'm trying to figure out what we could do with this information." | "host 구현 입장에서, 이 정보로 우리가 뭘 할 수 있을지 알아내는 중입니다" |
| 유용성 불확실 | "In that case, I'm not sure if anything of our long latency can be useful for the host at all." | "그 경우, long latency가 host에 전혀 유용한지 확신이 안 듭니다" |
| 구현 불확실 | "I'm not sure how that could work, but I was just thinking more about brainstorming." | "어떻게 작동할지 확신은 없지만, brainstorm 차원에서 생각해 봤습니다" |

**Audrey 교훈**: "I'm trying to figure out what we could do with X" - "I don't know" 대신 "I'm trying to figure out"을 써라. 모르는 것을 "조사 중"으로 프레이밍. 그리고 "I'm not sure if X can be useful at all" - "at all"이 honest 평가를 강화한다. "전혀 유용한지 확신이 안 듭니다"가 "별로 유용하지 않을 것 같습니다"보다 솔직하다.

### 전략 6: 아이디어 축소 (Idea Diminishment)

brainstorm 중에 아이디어를 던지되 "maybe", "something like that", "I wouldn't say either of them were ideal"로 축소한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 가능한 방법 | "Maybe we have a way of de-allocating certain entries in the buffer and just keep the data buffers ready or data buffers waiting, something like that." | "buffer의 일부 entry를 해제하고 data buffer를 준비시키거나 대기시키는 방법 같은 게 있을 수도 있습니다" |
| 과거 제품 평가 | "I wouldn't say that either of them were ideal." | "둘 다 이상적이었다고는 말 못 합니다" |

**Audrey 교훈**: "something like that"은 brainstorm에서 아이디어의 윤곽만 잡을 때 쓴다. 구체화하지 않겠다는 신호. 그리고 "I wouldn't say either of them were ideal" - "both were not ideal"보다 훨씬 정중한 부정이다. "I wouldn't say"가 "I don't say"보다 더 soft - 가정법이니까.

---

## 3. 정중한 도전 화법 (Polite Challenge)

### 질문 유형 1: 부분 이해 인정 + 도전 (Partial Understanding + Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So sorry, I followed you till the last point. Why do you think X?` | "So sorry, I followed you till the last point. Why do you think it cannot be integrated in CCI?" | 부분 경청 표시 + 도전 |
| `Sorry, I missed understanding that bit, and that's why I was looking to talk about it today.` | "Sorry, I missed understanding that bit, and that's why I was looking to talk about it today." | 솔직한 미이해 인정 |

**Audrey 교훈**: "I followed you till the last point"로 먼저 경청을 표시한 뒤 "Why do you think X?"로 도전. 이게 영어 회의에서 가장 정중한 도전 화법이다. "I missed understanding that bit" - 솔직한 미이해 인정은 partner를 공격하지 않고 자기 부족을 드러내는 겸손 화법.

### 질문 유형 2: 구체적 위치 요구 (Specific Location Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `in what X or in what Y you think that Z can be included?` | "in what command or in what packet you think that this Devload can be included?" | proposal의 구체적 위치 요구 |
| `How would you use that bit to communicate from X to Y?` | "How would you use that bit to communicate from device to host?" | mechanism 구체화 요구 |

### 질문 유형 3: 직접 protocol 교정 (Direct Protocol Correction)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `NDR happens only for the X. For Y, the NDR is issued only for the rights.` | "NDR happens only for the type two devices. For type three devices, the NDR is issued only for the rights." | protocol 사실 명시 |
| `So that's going to be wrong from the X perspective also.` | "So that's going to be wrong from the protocol perspective also." | "from the X perspective"로 한정 |
| `Even for X, it will be wrong.` | "Even for type two, it will be wrong." | "Even for X" 일반화 |
| `The X cannot precede the Y by this much amount.` | "The completion cannot precede the data by this much amount." | protocol 위반 정식화 |
| `That's all I'm trying to say.` | "That's all I'm trying to say." | 도전 의도 명시 - 공격 방지 |

**Audrey 교훈**: "That's all I'm trying to say"는 공격적으로 들린 발언을 정중하게 마무리하는 화법이다. "내가 말하려던 건 그게 전부야" - 더 이상 도전 안 하겠다는 신호. 이걸 붙이면 partner가 방어적으로 반응하지 않는다.

### 질문 유형 4: 직접 비판 (Direct Critique)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `That's just you are moving the problem, you're not solving the problem.` | "Yeah, that's just you are moving the problem, you're not solving the problem." | "moving vs solving" 대비 - 가장 강한 비판 |
| `I think that's a big overhead.` | "If the only purpose of that packet is going to be communicating latency, I think that's a big overhead." | 비용 직접 지적 |

**Audrey 교훈**: "moving the problem" - 문제를 다른 곳으로 옮기기만 하고 해결 안 한다는 비판. 영어 기술 회의에서 가장 직접적이면서도 깔끔한 비판 표현. "you're not solving the problem"과 짝을 이룬다. 이 정도는 한국어 회의에서도 강한 편이지만, 영어로는 오히려 깔끔하게 들린다.

### 질문 유형 5: 확장 요청 (Expansion Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Sorry, can you expand on that a bit more?` | "Sorry, can you expand on that a bit more?" | 정중한 확장 요청 |
| `Maybe can you walk through again from slide X, that will be better, like just to refresh.` | "Maybe can you walk through again from slide two, that will be better, like just to refresh." | 재설명 권유 - "just to refresh" |
| `So, just a quick twist in thinking, if X, would Y be different when Z?` | "Okay, so just a quick twist in thinking, if this long latency based device, if there to be addressed as non-coherent to explicitly the GPUs, of course, you will need many accompaniments like backing validation. And UI or P2P, you know, could this actually be a little different when these addresses will not be recognized by the host, the CPU?" | "just a quick twist in thinking" - 사고 전환 제안 |

**Audrey 교훈**: "just a quick twist in thinking"은 발표자의 관점을 바꿔보자는 고급 화법이다. "다른 각도로 생각해 보면"의 영어 버전. "twist in thinking"이 한국인이 잘 안 쓰는 표현인데, 영어 회의에서 관점 전환을 제안할 때 매우 자연스럽다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

### 기계적 논의 (Mechanical Discussion) 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 조건부 액션 | AMD | "If you can deliver the connector, we can review that." | "If you can X, we can Y" - 조건부 action item |
| 팀 리뷰 요청 | AMD | "Can you share the slides so I can run it by the [team]?" | "run it by the team" - 팀 검토 표현 |
| 팀 전달 | SK | "Viva, you can send it to me, and then I can decrypt it and send it to server." | action chain - 누가 무엇을 할지 명시 |

### CXL proposal 후속 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| action item 분배 | AMD | "Rita, can you also please look on advice if one to two relationship, if it is possible to add that and how big that lifting would be?" | 특정인에게 액션 할당 - "how big that lifting would be" (비용 평가) |
| 이메일 후속 | AMD | "Maybe even offline if you have something or something come in your mind, maybe you can send an email or I'll give your thoughts." | 후속 채널 - "even offline if X" |
| commitment | AMD | "Yeah, I would definitely do that." | "definitely" 강한 약속 |
| tentative commitment | AMD | "Yeah, I'll try to give more thoughts." | "try to"로 완화 |
| off-cycle 회의 제안 | AMD | "Let us revisit it and if we need it, if we need it, maybe we can, we can, we can set up a separate off cycle meeting just to discuss more." | "off cycle meeting" - 정기 외 회의 |
| 가치 인정 | SK | "It always helps to discuss this before the consortium discussion because it really helps out to narrow down the realistic choices that we can make to make a good proposal." | 회의 가치 메타 발언 - partner 관계 강화 |
| gratitude | AMD | "And thank you for talking through this because it wasn't becoming clear to me in the material. So I lost that understanding back when I was reading through it. So good that we talked through that." | 솔직한 감사 - "good that we talked through that" |

### 마무리 (Closing)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 시간 제한 퇴장 | AMD | "No, we already out of time and then I have to attend another meeting." | 시간 제한 정중 퇴장 |
| 후속 채널 | AMD | "Yes, and we need email or give me a call afterwards." | 이메일/전화 후속 |

**Audrey 교훈**:
- "run it by the team" - 한국인이 거의 모르는 표현. "팀에 검토받다"의 영어 버전. 회의에서 "제가 팀에 한번 검토해 보겠습니다"라고 말할 때, "I'll run it by the team"을 써라.
- "off cycle meeting" - 정기 회의 외에 별도 회의를 잡을 때 쓰는 공식 표현. "따로 회의 잡을까요?"의 영어 버전.
- "It always helps to discuss this before the consortium discussion" - partner 회의의 가치를 인정하는 meta 발언. 이걸 말하면 partner 관계가 강화된다. "언제나 X 전에 논의하면 도움이 된다" - partner 신뢰 구축.
- "good that we talked through that" - 회의 마무리에 "이야기해서 다행이다"를 붙여라. 이게 partner와의 관계를 긍정적으로 닫는 화법이다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/protocol/host architecture 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **NDR** (Non-data Response) | CXL.cachecast에서 data 없는 응답 패킷 | "NDR happens only for the type two devices. For type three devices, the NDR is issued only for the rights." - type 별 발생 조건 |
| **DRS** (Data Response) | data 포함 응답 패킷 | "Every read for type three, only thing you get is DRS." - type 3 read 응답 |
| **M2S** (Mem-to-Sub / Host-to-Device) | host → device request | "using M2S as request field, using the reserve field bits" - reserved field 제안 |
| **S2M** (Sub-to-Mem / Device-to-Host) | device → host response | "S2M NDR happens only for right, not for the transactions." - NDR 범위 |
| **CCI** (CXL.cache Interface) | CXL.cache 프로토콜 인터페이스 | "the latency report feature cannot be integrated into CCI" - 통합 불가 주장 |
| **CDAT** (Coherent Device Attribute Table) | boot-time device 속성 테이블 | "in CDAT information, we can communicate only one latency" - 단일 latency 한계 |
| **Devload** | device → host 비동기 부하 표시 | "Devloads are sent along anything that the device is indicating to the host. They are not separate packets." - 비동기 level indication |
| **flit** | link 전송 단위 | "That will impact the flit efficiency and overall link efficiency." - 효율 영향 |
| **QoS class** | HDLM range 기반 서비스 품질 | "QoS class, by the way, but that generally ties to a Hdm range." - 정적 mapping 한계 |
| **HDLM** (Host-managed Device Memory) | host 관리 디바이스 메모리 영역 | "It is the Hdm range base that this set of addresses are slow, this set of addresses are fast." - range 기반 |
| **type two / type three** | CXL 디바이스 타입 (Type 2 = cache coherent, Type 3 = memory) | "Even for type two, it will be wrong." - 일반화 |
| **posted read** | response 대기 없이 발행되는 읽기 | "if there was something like posted read transaction from the host side" - brainstorm |
| **PCIe card slot** | PCIe 카드 슬롯 | "The only way to plug anything in would be through the PCIe card slot." - 기계적 제약 |
| **MCIO** | Mini CoolEdge IO 커넥터 (신호 케이블) | "the connection between the drive, cage, and the motherboard is through MCIO." - 케이블 연결 |
| **drive backplane / drive cage** | 드라이브 수용 기구 | "if connector location is not changed, then without the case, I think we can fit it." - 기구 논의 |
| **EVB sample** (Evaluation Board) | 평가용 보드 샘플 | "Our EVB sample is bigger than the bigger, the width is one 10 millimeter, the length is 20 millimeter." - 치수 |
| **consortium discussion** | CXL 컨소시엄 표준 논의 | "It always helps to discuss this before the consortium discussion" - 표준 제안 전 사전 리뷰 |
| **heavy lifting** | 큰 작업/비용 (관용구) | "Or maybe that may be heavy lifting." - 비용 평가 |
| **bring up** | 하드웨어 초기 구동 검증 | (이 회의에선 직접 언급 없음, EVB sample 맥락) |
| **run it by the team** | 팀에 검토 받다 (관용구) | "Can you share the slides so I can run it by the [team]?" - 협업 액션 |
| **off cycle meeting** | 정기 외 별도 회의 | "maybe we can set up a separate off cycle meeting just to discuss more." - 후속 회의 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m34-001
  expression: "in the hybrid CXL system, host could not figure out X"
  category: presentation_framing
  function: problem_escalation
  speaker_role: presenter
  difficulty: 4
  context: "As you know, in the hybrid CXL system, host could not figure out how long the read latency will take."
  note: "could not figure out"이 인지적 문제로 프레이밍 - "can't do"보다 proposal 당위성 높음

- id: m34-002
  expression: "we propose our proposal is to X"
  category: presentation_reveal
  function: proposal_introduction
  speaker_role: presenter
  difficulty: 3
  context: "So we propose our proposal is to notify host can host the latency of read latency notify."
  note: 중복적이지만 한국인 발표자에겐 안전한 공식

- id: m34-003
  expression: "So host can improve utilization by X when Y"
  category: presentation_benefit
  function: benefit_connection
  speaker_role: presenter
  difficulty: 3
  context: "So host can improve utilization by task switching when the long latency is expected."

- id: m34-004
  expression: "X had comment about Y in the previous meeting"
  category: prior_acknowledgement
  function: reference_back
  speaker_role: presenter
  difficulty: 4
  context: "And Rita had comment about CCI in the previous meeting."
  note: 선행 발언 회상 - partner 의견 존중. 신뢰 구축

- id: m34-005
  expression: "So we have constraint about X integration"
  category: constraint_stating
  function: limitation_acknowledgement
  speaker_role: presenter
  difficulty: 3
  context: "So we have constraint about CCI integration."

- id: m34-006
  expression: "There is no mechanism to X in real time"
  category: gap_stating
  function: gap_creation
  speaker_role: presenter
  difficulty: 4
  context: "There is no mechanism to report actual latency in real time."
  note: "We need X" 전에 gap 먼저 보여주는 공식

- id: m34-007
  expression: "When using X, it's not possible to predict whether Y or not"
  category: uncertainty_stating
  function: indeterminacy_framing
  speaker_role: presenter
  difficulty: 4
  context: "When using hybrid CXL memory, it's not possible to predict whether a DRAM cache hit or not."

- id: m34-008
  expression: "So I think the X feature cannot be integrated into Y"
  category: negative_conclusion
  function: conclusion_draw
  speaker_role: presenter
  difficulty: 3
  context: "So I think the latency report feature cannot be integrated into CCI."

- id: m34-009
  expression: "So I'll buy your thoughts on this."
  category: feedback_invitation
  function: opinion_request
  speaker_role: presenter
  difficulty: 5
  context: "So I'll buy your thoughts on this."
  note: "What do you think?"보다 격식 있는 고급 표현. "buy" = "accept/take"

- id: m34-010
  expression: "Maybe can you walk through again from slide X, that will be better, like just to refresh."
  category: re_explanation_request
  function: refresh_ask
  speaker_role: questioner
  difficulty: 4
  context: "Maybe can you walk through again from slide two, that will be better, like just to refresh."
  note: "just to refresh"가 부드럽게

# ── AMD 응답자: 명확화·도전 (Clarifying & Challenge) ──
- id: m34-011
  expression: "So sorry, I followed you till the last point. Why do you think X?"
  category: clarifying_probe
  function: partial_understanding_challenge
  speaker_role: responder
  difficulty: 5
  context: "So sorry, I followed you till the last point. Why do you think it cannot be integrated in CCI?"
  note: 경청 표시 후 도전 - 가장 정중한 challenge 화법

- id: m34-012
  expression: "in what X or in what Y you think that Z can be included?"
  category: specific_probe
  function: location_inquiry
  speaker_role: responder
  difficulty: 4
  context: "in what command or in what packet you think that this Devload can be included?"

- id: m34-013
  expression: "How would you use that bit to communicate from X to Y?"
  category: mechanism_probe
  function: mechanism_inquiry
  speaker_role: responder
  difficulty: 3
  context: "How would you use that bit to communicate from device to host?"

- id: m34-014
  expression: "Sorry, I missed understanding that bit, and that's why I was looking to talk about it today."
  category: honest_acknowledgement
  function: misunderstanding_admit
  speaker_role: responder
  difficulty: 5
  context: "Sorry, I missed understanding that bit, and that's why I was looking to talk about it today."
  note: 솔직한 미이해 인정 - partner 공격 않고 자기 부족 드러냄

- id: m34-015
  expression: "So that's going to be wrong from the X perspective also."
  category: direct_correction
  function: perspective_limited_critique
  speaker_role: responder
  difficulty: 5
  context: "So that's going to be wrong from the protocol perspective also."
  note: "from the X perspective"로 한정하면 직접 공격이 아님

- id: m34-016
  expression: "Even for X, it will be wrong."
  category: generalization
  function: scope_extension
  speaker_role: responder
  difficulty: 3
  context: "Even for type two, it will be wrong."

- id: m34-017
  expression: "The X cannot precede the Y by this much amount."
  category: protocol_violation
  function: rule_violation_state
  speaker_role: responder
  difficulty: 4
  context: "The completion cannot precede the data by this much amount."

- id: m34-018
  expression: "That's all I'm trying to say."
  category: intent_clarify
  function: attack_disarm
  speaker_role: responder
  difficulty: 4
  context: "That's all I'm trying to say."
  note: 공격적으로 들린 발언 정중하게 마무리

- id: m34-019
  expression: "That's just you are moving the problem, you're not solving the problem."
  category: direct_critique
  function: moving_vs_solving
  speaker_role: responder
  difficulty: 5
  context: "Yeah, that's just you are moving the problem, you're not solving the problem."
  note: 가장 강한 직접 비판 - "moving vs solving" 대비

- id: m34-020
  expression: "I think like we need to, if you want to solve the problem, instead of X, we need to make Y"
  category: constructive_redirect
  function: critique_to_solution
  speaker_role: responder
  difficulty: 5
  context: "I think like we need to, if you want to solve the problem, whatever it says, instead of one to one request to response relationship, we need to make one to two, one to two relationship."
  note: 비판 후 즉시 "if you want to solve"로 constructive 전환

- id: m34-021
  expression: "Or maybe that may be heavy lifting."
  category: cost_acknowledge
  function: cost_idiom
  speaker_role: responder
  difficulty: 4
  context: "Or maybe that may be heavy lifting."
  note: "heavy lifting" - 큰 작업/비용. "큰 공사다"의 영어 버전

- id: m34-022
  expression: "Sorry, can you expand on that a bit more?"
  category: expansion_request
  function: polite_expansion
  speaker_role: responder
  difficulty: 3
  context: "Sorry, can you expand on that a bit more?"

- id: m34-023
  expression: "just a quick twist in thinking, if X, would Y be different when Z?"
  category: perspective_shift
  function: thinking_reframe
  speaker_role: questioner
  difficulty: 5
  context: "Okay, so just a quick twist in thinking, if this long latency based device, if there to be addressed as non-coherent to explicitly the GPUs..."
  note: "twist in thinking" - 관점 전환 제안. 한국인이 잘 안 쓰는 고급 표현

# ── 효율성 논증 (Efficiency Argument) ──
- id: m34-024
  expression: "If you are going to get another X for every Y, that's going to be a lot of Z being consumed."
  category: efficiency_argument
  function: cost_chain
  speaker_role: responder
  difficulty: 5
  context: "If you are going to get another S2M packet for every read, that's going to be a lot of link bandwidth being consumed."

- id: m34-025
  expression: "That will impact the X and overall Y."
  category: impact_stating
  function: impact_chain
  speaker_role: responder
  difficulty: 3
  context: "That will impact the flit efficiency and overall link efficiency."

- id: m34-026
  expression: "If the only purpose of that X is going to be Y, I think that's a big overhead."
  category: single_purpose_cost
  function: cost_critique
  speaker_role: responder
  difficulty: 5
  context: "If the only purpose of that packet is going to be communicating latency, I think that's a big overhead."
  note: 영어 기술 회의에서 가장 자주 쓰이는 비용 도전 공식

- id: m34-027
  expression: "So they are not separate packets. They're just shoved along anything that's going to the host."
  category: informal_explanation
  function: mechanism_clarify
  speaker_role: responder
  difficulty: 4
  context: "So they are not separate packets. They're just shoved along anything that's going to the host."
  note: "shoved along" - informal. "덩달아 보냄" 뉘앙스

- id: m34-028
  expression: "It is just more of a level indication."
  category: analogy
  function: function_clarify
  speaker_role: responder
  difficulty: 3
  context: "It is just more of a level indication."
  note: "more of a X" - 비유 공식

- id: m34-029
  expression: "the way X is communicated is Y"
  category: mechanism_explain
  function: mechanism_structure
  speaker_role: responder
  difficulty: 4
  context: "the way Devloads are communicated is Devloads are sent along anything that the device is indicating to the host."

- id: m34-030
  expression: "Whereas in this case, if you want to do it per X basis, then you really need that Y"
  category: contrast_structure
  function: contrast_explain
  speaker_role: responder
  difficulty: 5
  context: "Whereas in this case, if you want to do it per packet basis, then, or per transaction basis, then you really need that synchronous communication"

# ── Brainstorm Marker (가장 중요) ──
- id: m34-031
  expression: "Just for the conversation purposes, let's say your X is Y and Z is W."
  category: hypothetical_frame
  function: hypothetical_setup
  speaker_role: responder
  difficulty: 5
  context: "Just for the conversation purposes, let's say your cache hit is 100 nanosecond and cache misses 1 microsecond."
  note: "Just for the conversation purposes" - 가정 설정 공식

- id: m34-032
  expression: "I'm thinking aloud here, so I am going to say garbage here for a minute."
  category: brainstorm_disclaimer
  function: idea_immunity
  speaker_role: responder
  difficulty: 5
  context: "I'm thinking aloud here, so I am going to say garbage here for a minute."
  note: brainstorm marker - "say garbage"로 자기 낮추기. 고급 화법

- id: m34-033
  expression: "And again, as I said, I started thinking aloud here, so I'm still on my speaking garbage mode."
  category: brainstorm_sustain
  function: mode_continue
  speaker_role: responder
  difficulty: 5
  context: "And again, as I said, I started thinking aloud here, so I'm still on my speaking garbage mode."
  note: brainstorm 유지 - "speaking garbage mode"

- id: m34-034
  expression: "But if there was something like X, can we do something?"
  category: brainstorm_question
  function: idea_propose
  speaker_role: responder
  difficulty: 4
  context: "But if there was something like posted read transaction from the host side... Can we do something?"

- id: m34-035
  expression: "But that could be a useful way of doing it, as I think."
  category: tentative_endorsement
  function: soft_support
  speaker_role: responder
  difficulty: 5
  context: "But that could be a useful way of doing it, as I think."
  note: "as I think" 문장 끝 - 더 겸손

- id: m34-036
  expression: "As long as we don't get too greedy on getting real time, I think, yeah, we could try to find a workaround."
  category: principle_frame
  function: principle_with_workaround
  speaker_role: responder
  difficulty: 5
  context: "As long as we don't get too greedy on getting real time, I think, yeah, we could try to find a workaround."
  note: "too greedy on X" - partner 과도한 요구 부드럽게 제한

# ── 회피·솔직함 (Hedging & Honesty) ──
- id: m34-037
  expression: "I think X, I think, needs Y, I assume."
  category: double_hedge
  function: dual_softening
  speaker_role: responder
  difficulty: 4
  context: "even with alternative fields that we can pursue, I think the protocol flow, I think, needs modification, I assume."
  note: 이중 hedge - "I think" + "I assume"

- id: m34-038
  expression: "I'm trying to figure out what we could do with this information."
  category: honest_gap
  function: investigating_state
  speaker_role: responder
  difficulty: 4
  context: "And as a host implementation, I'm trying to figure out what we could do with this information."
  note: "I don't know" 대신 "I'm trying to figure out"

- id: m34-039
  expression: "I'm not sure if anything of X can be useful for Y at all."
  category: honest_assessment
  function: uncertain_value
  speaker_role: responder
  difficulty: 4
  context: "In that case, I'm not sure if anything of our long latency can be useful for the host at all."

- id: m34-040
  expression: "I'm not sure how that could work, but I was just thinking more about brainstorming."
  category: explicit_uncertainty
  function: brainstorm_flag
  speaker_role: questioner
  difficulty: 3
  context: "I'm not sure how that could work, but I was just thinking more about brainstorming."

- id: m34-041
  expression: "Maybe we have a way of X, something like that."
  category: idea_diminish
  function: vague_propose
  speaker_role: responder
  difficulty: 3
  context: "Maybe we have a way of de-allocating certain entries in the buffer and just keep the data buffers ready or data buffers waiting, something like that."

- id: m34-042
  expression: "I wouldn't say that either of them were ideal."
  category: soft_negative
  function: polite_negative
  speaker_role: responder
  difficulty: 4
  context: "I wouldn't say that either of them were ideal."
  note: "I wouldn't say" - 가정법 soft negative

- id: m34-043
  expression: "I'll try to give more thoughts. Some of the details that I mentioned probably doesn't make sense this time, but I will think about that."
  category: self_deprecating_commit
  function: humble_commit
  speaker_role: responder
  difficulty: 5
  context: "Yeah, I'll try to give more thoughts. I think some of the details that I mentioned probably doesn't make sense this time, but I will think about that."

# ── 대안 제시 (Alternative Suggestion) ──
- id: m34-044
  expression: "perhaps you might be able to X with Y anyways, right?"
  category: polite_suggestion
  function: alternative_offer
  speaker_role: responder
  difficulty: 5
  context: "perhaps you might be able to decouple this with Devload anyways, right?"
  note: "perhaps" + "might" + "anyways" + "right?" - 4중 완화

- id: m34-045
  expression: "Instead, if you look at the X, the way X is communicated is Y"
  category: alternative_explain
  function: alternative_mechanism
  speaker_role: responder
  difficulty: 4
  context: "Instead, if you look at the Devload, the way Devloads are communicated is Devloads are sent along anything that the device is indicating to the host."

- id: m34-046
  expression: "if you want to do X, that becomes much more Y"
  category: cost_escalation
  function: cost_stating
  speaker_role: responder
  difficulty: 4
  context: "if you want to do it per packet basis, then... having that packet come with just this much information that, hey, this is a fast packet, that's going to be much more inefficient on the protocol side."

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m34-047
  expression: "If you can deliver the X, we can review that."
  category: conditional_action
  function: conditional_commit
  speaker_role: negotiator
  difficulty: 3
  context: "If you can deliver the connector, we can review that."

- id: m34-048
  expression: "Can you share the slides so I can run it by the [team]?"
  category: team_review
  function: team_review_request
  speaker_role: negotiator
  difficulty: 4
  context: "Can you share the slides so I can run it by the [team]?"
  note: "run it by the team" - 한국인이 거의 모르는 표현

- id: m34-049
  expression: "X, can you also please look on advice if Y, if it is possible to add that and how big that lifting would be?"
  category: action_assignment
  function: specific_assignment
  speaker_role: negotiator
  difficulty: 4
  context: "Rita, can you also please look on advice if one to two relationship, if it is possible to add that and how big that lifting would be?"

- id: m34-050
  expression: "Maybe even offline if you have something or something come in your mind, maybe you can send an email or I'll give your thoughts."
  category: follow_up_channel
  function: offline_invite
  speaker_role: negotiator
  difficulty: 3
  context: "Maybe even offline if you have something or something come in your mind, maybe you can send an email or I'll give your thoughts."

- id: m34-051
  expression: "I would definitely do that."
  category: commitment
  function: strong_commit
  speaker_role: responder
  difficulty: 2
  context: "Yeah, I would definitely do that."

- id: m34-052
  expression: "Let us revisit it and if we need it, maybe we can set up a separate off cycle meeting just to discuss more."
  category: off_cycle_meeting
  function: separate_meeting_propose
  speaker_role: negotiator
  difficulty: 4
  context: "Let us revisit it and if we need it, if we need it, maybe we can, we can, we can set up a separate off cycle meeting just to discuss more."
  note: "off cycle meeting" - 정기 외 회의 공식 표현

# ── 가치 표현·마무리 (Value & Closing) ──
- id: m34-053
  expression: "It always helps to discuss this before the consortium discussion because it really helps out to narrow down the realistic choices that we can make to make a good proposal."
  category: meta_value
  function: meeting_value_acknowledge
  speaker_role: presenter
  difficulty: 5
  context: "It always helps to discuss this before the consortium discussion because it really helps out to narrow down the realistic choices that we can make to make a good proposal."
  note: partner 회의 가치 인정 - 관계 강화

- id: m34-054
  expression: "And thank you for talking through this because it wasn't becoming clear to me in the material. So I lost that understanding back when I was reading through it. So good that we talked through that."
  category: gracious_gratitude
  function: honest_thanks
  speaker_role: responder
  difficulty: 5
  context: "And thank you for talking through this because it wasn't becoming clear to me in the material. So I lost that understanding back when I was reading through it. So good that we talked through that."
  note: "good that we talked through that" - 회의 긍정적 마무리

- id: m34-055
  expression: "We already out of time and then I have to attend another meeting."
  category: time_exit
  function: polite_exit
  speaker_role: negotiator
  difficulty: 2
  context: "No, we already out of time and then I have to attend another meeting."

- id: m34-056
  expression: "Yeah, you know how these things are right there to spec and even a slide. I think there's some plus minus tolerance. But beyond that, it'll be hard to slide anything in."
  category: tolerance_language
  function: spec_tolerance
  speaker_role: negotiator
  difficulty: 4
  context: "Yeah, you know how these things are right there to spec and even a slide. I think there's some plus minus tolerance. But beyond that, it'll be hard to slide anything in."
  note: "plus minus tolerance" - 스펙 허용 오차. 기구 논의 필수 어휘

- id: m34-057
  expression: "if connector location is not changed, then without the case, I think we can fit it. But again, it's going to get at your own risk, right? Because I don't know if that will work or not."
  category: hedged_assessment
  function: risk_disclaimer
  speaker_role: responder
  difficulty: 5
  context: "if connector location is not changed, then without the case, I think we can fit it. But again, it's going to get at your own risk, right? Because I don't know if that will work or not."
  note: "at your own risk" - 위험 부담 명시. "I don't know if that will work or not" 솔직 한계
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2025-07-23 08 29 22_EN_AMDCXLsync-extracted.wav` (총 ~분, 3,720단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-29) | 기구 논의 - SK "10mm or 20mm" + AMD "plus minus tolerance" 리뷰 | tolerance 언어, 조건부 액션 | ★★☆ |
| 2 | proposal 프레이밍 (line 60-72) | SK "host could not figure out read latency" + "we propose our proposal is to" | proposal framing 공식 | ★★★ |
| 3 | 명확화 도전 (line 74-86) | AMD "I followed you till the last point. Why do you think X?" + "walk through again from slide two" | 정중한 도전 + 재설명 요청 | ★★★★ |
| 4 | protocol 교정 + 효율 논증 (line 100-115) | AMD "NDR only for type two" + "If the only purpose... big overhead" | 직접 교정 + 비용 논증 | ★★★★ |
| 5 | brainstorm mode (line 153-184) | AMD "I'm thinking aloud, going to say garbage" + "speaking garbage mode" + "As long as we don't get too greedy" | brainstorm marker (가장 가치 높음) | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - protocol 도전 + brainstorm marker 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **proposal pitch + technical defense + brainstorm** register다. SK가 CXL consortium 제출 전 AMD와 사전 리뷰하는 자리. 세 역할 모두 학습해야:
- **발표자 역할 (SK)**: proposal framing, 선행 제약 인정, feedback 초청 - 네가 CXL 컨소시엄에 제안할 때
- **응답자 역할 (AMD)**: 정중한 기술 도전, protocol 교정, brainstorm mode 전환 - 네가 partner proposal을 리뷰할 때
- **협상자 역할 (양측)**: action item 분배, off-cycle meeting 제안, 가치 인정 - 네가 회의 마무리할 때

### Pragmatics (화용론) 핵심
1. **Brainstorm marker**: "I'm thinking aloud here, so I'm going to say garbage here for a minute" - 영어 회의에서 가장 강력한 brainstorm mode 전환 화법. 자기 아이디어를 "garbage"로 견하면서, partner도 방어적으로 듣지 않게 만든다. "I'm still on my speaking garbage mode"로 상태 유지. 이 패턴은 한국어 "생각나는 대로 말해볼게요"보다 훨씬 더 강한 disclaimer다.
2. **"from the X perspective"**: 직접 교정을 할 때 "Y is wrong"이 아니라 "from the protocol perspective, Y is wrong"으로 한정하면 공격이 아니다. 관점을 명시하면 부드럽다. 그리고 "also"를 붙여 "다른 것과 마찬가지로"로 만든다.
3. **"That's all I'm trying to say"**: 공격적으로 들린 발언을 정중하게 마무리하는 화법. "내가 말하려던 건 그게 전부야" - 더 이상 도전 안 하겠다는 신호.
4. **"if you want to solve the problem"**: 비판 후 즉시 constructive 전환. "you're moving the problem, you're not solving the problem" → "if you want to solve the problem, we need to X" - 비판이 개선 제안이 됨.
5. **"Just for the conversation purposes"**: 가정 설정 공식. "let's say X is Y"와 짝. 기술 회의에서 hypothetical을 세울 때 무조건 써라.

### 네가 당장 써야 할 Top 5
1. **"I'm thinking aloud here, so I'm going to say garbage here for a minute"** - brainstorm mode 전환. 가장 중요.
2. **"So sorry, I followed you till the last point. Why do you think X?"** - 정중한 도전
3. **"That's going to be wrong from the X perspective also. That's all I'm trying to say."** - 직접 교정 + 의도 명시
4. **"perhaps you might be able to X with Y anyways, right?"** - 4중 완화 대안 제시
5. **"As long as we don't get too greedy on X, we could try to find a workaround."** - 원칙 설정 + 해결책 가능성

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "생각나는 대로 말해볼게요" | "I'm thinking aloud here, so I'm going to say garbage here for a minute" | 영어는 "garbage"까지 내려가야 충분한 disclaimer |
| "그건 protocol 위반입니다" | "That's going to be wrong from the protocol perspective also" | "from the X perspective"로 한정 - 공격 아님 |
| "왜 그렇게 생각해요?" | "Why do you think it cannot be integrated in CCI?" | "Why is X" 대신 "Why do you think X" - 추론을 묻는 것 |
| "그건 문제를 옮기기만 한 겁니다" | "you're moving the problem, you're not solving the problem" | "moving vs solving" 대비 - 깔끔한 직접 비판 |
| "팀에 검토해 보겠습니다" | "I can run it by the team" | "run it by the team" - 한국인이 모르는 고급 표현 |
| "큰 공사다" | "that may be heavy lifting" | "heavy lifting" 관용구 |
| "따로 회의 잡을까요?" | "maybe we can set up a separate off cycle meeting" | "off cycle meeting" 공식 표현 |
| "이야기해서 다행이다" | "good that we talked through that" | 회의 긍정적 마무리 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 57개 표현 중, 8절 Top 5부터 우선 순지
3. **Audrey 금요일 교정**: 이 교재의 1b절 AMD 도전 화법·2절 brainstorm marker·3절 직접 비판 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 학습**: SK 발표자 입장(1절)과 AMD 응답자 입장(1b절)을 번갈아 연습 - 네가 CXL 컨소시엄에 제안할 때도, partner proposal을 리뷰할 때도 모두 필요

---

*Textbook 34 - AMD CXL sync (2025-07-23). 회의 유형 A (기술 Deep-dive). 표현 DB 57개. 5개 발췌 구간. 작성: 2026-09-01.*
