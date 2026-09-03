---
textbook_id: 36
meeting: Google (Google CXL/AI memory technical deep-dive)
date: 2025-06-10
type: A (기술 Deep-dive)
partner: Google (Structera team - presenter + Jerry Lee)
sk_side: SK hynix CXL/AI memory team, Sung-dong, Jerry Lee (SK side)
duration_words: 2794
audio: repo/webex-audio/2025-06-10 08 36 16_EN_Google-extracted.wav
transcript: repo/webex-audio/2025-06-10 08 36 16_EN_Google-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, google, cxl, ai-memory, compression, structera, marvell, technical-deepdive, graded-dram, double-chip-kill]
---

# Textbook 36 - Google CXL/AI Memory Technical Deep-dive (2025-06-10)

> **회의 유형**: A (기술 Deep-dive) - Google이 CXL 압축 메모리 제품의 기능을 깊이 발표, SK hynix가 기술 Q&A
> **학습 가치**: 발표자의 "기능-이유-제약" 3단 설명 구조, 제약을 기회로 재프레이밍, 양보-협상 화법
> **Audrey 관점**: 이 회의는 Google이 SK hynix에게 CXL 압축 메모리를 "sell"하는 자리. 발표자가 "Google exclusive" 기능을 강조하면서도 "Marvell과 논의하라"고 선을 긋는 점이 핵심. 발표자의 정중한 디펜스 + 질문자의 확인형 도전이 모두 들어있다

---

## 1. 발화 아키텍처 - Google 발표자의 설명 설계 (5단계)

Google 발표자는 각 기능을 5단 구조로 설명한다. 각 단계마다 **고정된 화법 공식**이 있다.

### 단계 1: 이전 발표 회수 + 전환 (Recap-Transition)

새 기능으로 넘어갈 때 이전 주제를 1줄로 요약하고 "Anyway, let me push on"으로 넘어간다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Anyway, let me push on to the next feature.` | "Anyway, let me push on to the next feature. This is a compression feature on the fly dictionary." | 침묵 없는 단절 - "push on"으로 발표 주도권 유지 |
| `And then I just have one more feature and that is X` | "And then I just have one more feature and that is numeric compression." | "one more"로 마지막임을 예고 - 청중 집중 유도 |
| `And this is compelling because it can give us X` | "And this is compelling because it can give us higher uptime." | "compelling because" - 가치 판매 공식 |

**Audrey 교훈**: 발표에서 "Let's move on"은 너무 평범하다. "Anyway, let me **push on** to the next feature" - "push on"이 발표자가 주도한다는 뉘앙스. 그리고 기능을 소개하자마자 "compelling because X"로 가치를 연결한다. "이 기능은 X입니다"가 아니라 "이 기능은 X because Y" - 설명과 가치를 한 문장에.

### 단계 2: 제약 전제 → 문제 제기 (Constraint → Problem)

기능을 소개하기 전에 **제약조건**을 먼저 세운다. " dictionaries는 좋지만, 보안 문제가 있다"로 문제를 프레이밍.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `However, there are very significant X concerns with Y` | "However, there are very significant security concerns with using a dictionary in that dictionary can be considered to have PII" | "However, significant concerns" - 제약을 무겁게 프레이밍 |
| `there are lots of cases where we would like to be using X, but we can't` | "So there are lots of cases where we would like to be using dictionaries for compression, but we can't" | "would like to but can't" - 욕구-제약 대비 |
| `And the way we get around that restriction on this device is X` | "And the way we get around that restriction on this device is the device builds the dictionary on the fly" | "get around that restriction" - 솔루션 등장 공식 |

**Audrey 교훈**: 영어 발표는 "기능"으로 시작하지 않는다. **"제약"**으로 시작한다. "We would like to use X, but we can't. And the way we get around that restriction is Y" - 이 3단 구조가 제약을 솔루션으로 전환하는 공식. "get around"는 "회피하다/우회하다"인데, 발표에서는 "제약을 해결하다"의 뉘앙스. "solve"보다 훨씬 세련된 표현.

### 단계 3: 차별성 강조 (Differentiation)

"Google exclusive"를 강조하면서, baseline 기능은 Marvell에게 물어보라고 선을 긋는다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `that's not a Google exclusive feature` → `the Google exclusive feature here is X` | "Entropy encoding will be available to anyone... But the Google exclusive feature here is numeric compression" | "exclusive"로 차별성 명시 - "anyone vs Google" 대비 |
| `That's something you should get from Marvell.` | "That's something you should get from Marvell." | baseline 책임 회피 - "Marvell에게 물어보라" |
| `this is one of the things that we do that is gonna give us significantly higher X` | "this is one of the things that we do that is gonna give us significantly higher compression ratios" | "one of the things we do" - Google만의 가치 함축 |

**Audrey 교훈**: "Google exclusive feature" - 발표자가 자기 회사만의 차별성을 강조할 때 쓰는 공식. "anyone can get X, but the exclusive feature is Y"로 대비 구조. 그리고 모르는 건 솔직히 "That's something you should get from Marvell"로 넘긴다. 영어 회의에서 "I don't know"는 약하고, "you should get that from X"는 책임의 주체를 명시하는 정중한 회피다.

### 단계 4: 질문 유도 + 정체 확인 (Question Clarification)

질문을 받으면 즉시 "When you say X, I'm not sure I know"로 범위를 좁힌다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `When you say X, I'm not sure that I know, are you Y?` | "When you say evaluation test program, I'm not sure that I know, are you, what kind of evaluation are we talking about, at what stage of the design" | "When you say X" - 질문 용어의 범위 좁히기 |
| `are we talking about performance, are we talking about functionality, are we talking about manufacturing` | "are we talking about performance, are we talking about functionality, are we talking about manufacturing, or are we talking about design?" | 4개 반복 - 질문 분류 위한 체크리스트 |
| `I think it's probably something that you want to talk to Marvell about.` | "I think it's probably something that you want to talk to Marvell about." | 책임 전가 - 정중한 "Marvell로 가주세요" |

**Audrey 교훈**: 질문을 받았을 때 "What do you mean?"은 공격적으로 들린다. "When you say X, I'm not sure I know, are you talking about A, B, or C?" - "X라고 하셨는데, A/B/C 중 어떤 건지요?" - 질문자가 자기 질문을 더 구체화하도록 유도하는 고급 화법. 그리고 "are we talking about X"를 3-4번 반복하면, 질문자가 스스로 답을 찾게 된다.

### 단계 5: 다음 단계 제안 (Next-Step Proposal)

회의 마무리에 "I think we should set up a three way discussion"으로 구체적 다음 단계를 제안.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think we should set up a three way discussion with X` | "I think we should set up a three way discussion with Marvell and in particular discuss schedule" | "three way discussion" - 구체적 다음 단계 |
| `I think X should go off and think about Y and come back and let us know` | "I think SK hynix should go off and think about the features that you saw today and come back and let us know what your priorities are" | "go off and think about" - 상대에게 action item 부여 |
| `And we can negotiate next level of detail on a business arrangement` | "And we can negotiate next level of detail on a business arrangement that enables those features for you" | "next level of detail" - 협상 단계 명시 |
| `I think the best way would be for X to come back and let us know Y` | "I think the best way would be for SK hynix to come back and let us know what properties you see as feasible in a graded media" | "the best way would be for X to" - 정중한 지시 |

**Audrey 교훈**: 회의 마무리의 핵심은 "누가, 뭘, 언까지"를 명시하는 것. "I think we should set up a three way discussion" - 3자 회의 제안. "I think X should go off and think about Y" - 상대에게 과제 부여. "go off and think about"는 "가서 생각해오라"인데, 영어로는 정중한 명령. "negotiate next level of detail" - 다음 회의의 목적이 "detail negotiation"임을 명시.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. Google 발표자가 제약·경쟁·책임을 어떻게 정중하게 포장하는지.

### 전략 1: 제약을 솔루션으로 재프레이밍 (Constraint-as-Solution)

가장 중요한 패턴. "데이터가 덜 들어간다"는 제약을 "double chip kill" 기능으로 재프레이밍.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| 18%가 아니라 15%만 쓴다는 한계 | "when we said 15% on the prior slide, that actually could have been 18%. But instead we are taking advantage of some of that extra capacity to do double chip kill. And this is compelling because it can give us higher uptime." | "15%라고 했지만 사실 18% 가능합니다. **하지만** 그 여유 용량으로 double chip kill을 합니다. 그리고 이게 higher uptime을 줍니다" |

**패턴 공식**: `X could have been Y. But instead we are taking advantage of that to do Z. And this is compelling because...`

**Audrey 교훈**: 영어 회의에서 제약을 말할 때 "we lost 3%"는 절대 쓰지 마라. "We are **taking advantage of** that extra capacity to do X" - "잃은 게 아니라 활용한 것이다"로 재프레이밍. 그리고 "this is compelling because Y"로 가치를 붙인다. 이게 전문가의 제약 포장이다. 한국어로는 "손해 본 게 아니라 그걸로 다른 걸 했습니다"인데, 영어는 "taking advantage of" 한 단어로 끝난다.

### 전략 2: 범용 기능은 경쟁사에, 차별 기능은 자기 것 (Commodity-vs-Exclusive Split)

경쟁사가 다 가진 기능은 "anyone", 자기만의 기능은 "Google exclusive"로 명확히 선을 긋는다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Entropy encoding은 범용, numeric compression은 Google 전용 | "Entropy encoding will be available to anyone that is buying it. **But** the Google exclusive feature here is numeric compression, which is to say it is a compression scheme that works well with numeric data types." | "Entropy encoding은 누구나 사용 가능. **하지만** Google exclusive 기능은 numeric compression입니다. numeric 데이터 타입에 잘 작동하는 압축 방식" |
| Baseline은 Marvell 책임 | "I'm not talking to you about the baseline features of the Structera device. That's something you should get from Marvell." | "Structera device의 baseline 기능은 논의 안 합니다. Marvell에게 받으세요" |

**패턴 공식**: `X will be available to anyone. But the Google exclusive feature here is Y. That's something you should get from Z.`

**Audrey 교훈**: 자기 회사만의 가치를 강조하려면, 범용 기능과 차별 기능을 **대비**시켜라. "X is available to anyone, but the exclusive feature is Y" - 이 대비 구조가 차별성을 명확히 만든다. 그리고 baseline은 책임 소재를 명시 - "you should get that from Marvell" - 모르는 걸 인정하면서 책임을 넘기는 정중한 화법.

### 전략 3: 트레이드오프 인정 + 상한선 설정 (Trade-off Acknowledgment)

graded DRAM 수용 질문에 "가능하지만 품질 하한선이 있다"로 정중하게 선을 긋는다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| graded DRAM 품질 기준 | "We're not going to want terribly unreliable DRAM, right? even with double chip kill. So it's gonna be a space where we're going to expect that we've still done all the testing." | "터무니없이 불안정한 DRAM은 원하지 않습니다. double chip kill이 있어도요. 그래서 여전히 모든 테스트를 마친 제품이어야 합니다" |

**패턴 공식**: `We're not going to want terribly X. even with Y. So it's gonna be a space where we're going to expect Z.`

**Audrey 교훈**: "거절"을 "space"로 포장하는 고급 화법. "안 됩니다"가 아니라 "it's gonna be a space where we expect X" - "X를 기대하는 영역이 될 것입니다" - 가능성은 열어두되 조건을 단다. "terribly"는 "매우"인데, 부정 문장에서 쓰면 "터무니없이"의 뉘앙스. "We're not going to want terribly unreliable DRAM" - 이 한 문장이 품질 하한선을 설정한다.

### 전략 4: 회피의 정중함 - "I can't imagine a scenario" (Polite Impossibility)

불가능한 시나리오를 부드럽게 부정한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Server 간 telemetry 교환 불필요 | "it would be possible for Server A to read data over CXL and then Server B to talk to Server A over the network, but **I can't imagine a scenario where that would be useful**" | "Server A가 CXL로 데이터 읽고 Server B가 네트워크로 Server A와 대화하는 건 가능하지만, **유용한 시나리오는 상상이 안 됩니다**" |

**패턴 공식**: `X is possible, but I can't imagine a scenario where that would be useful.`

**Audrey 교훈**: "That's useless"는 공격적이다. "I can't imagine a scenario where that would be useful" - "유용한 시나리오를 상상할 수 없다" - 불가능을 자기 인지의 한계로 포장. "쓸모없다"가 아니라 "제가 상상을 못 합니다"로 겸손함을 유지. 이게 영어의 정중한 부정.

### 전략 5: 가설 시나리오 제시로 설득력 확보 (Hypothetical Scenario)

graded DRAM이 아니라 DIMM 단위 fall-out 시나리오를 "you could even imagine"으로 제시.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DIMM 단위 fall-out 활용 | "you could even imagine a scenario where we had, where it was not for graded DRAMs so much as DIMs, right? If you had already packaged everything as a dim and you had fall out where you realized, oh, there's exactly one bad DRAM on this dim, but the rest of the dim is okay, then we could imagine still using that dim in some configuration on this card" | "상상해 보세요. graded DRAM이 아니라 DIMM 시나리오. 이미 DIMM으로 패키징했는데 DRAM 하나만 불량이고 나머지는 정상이라면, 그 DIMM을 이 카드의 어떤 구성으로든 사용할 수 있습니다" |

**패턴 공식**: `you could even imagine a scenario where X. If you had Y, then we could imagine still using Z.`

**Audrey 교훈**: "imagine"을 두 번 쓰는 발표 화법. "you could even imagine a scenario where X" - 청중을 가설 시나리오로 초대. 그리고 "we could imagine still using Z" - 가능성을 열어둔 채로 마무리. "we could do X"보다 "we could imagine using X"가 훨씬 부드럽고 설득적. 발표에서 가설을 제시할 때 써라.

---

## 3. 정중한 도전 화법 (SK hynix 측 질문자)

SK hynix 측이 기술적으로 도전하면서도 정중하게 질문하는 패턴.

### 질문 유형 1: 이해 확인형 질문 (Comprehension Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If I understand you correctly.` | "If I understand you correctly." | 정중한 전제 - 질문 전 확인 |
| `Just to make sure, X is Y, am I correct?` | "It's your idea, am I correct?" | "am I correct?"로 확인 |
| `So how do you X?` | "So how do you exchange the telemetry data between Server A and Server B?" | "how do you" - 메커니즘 탐색 |

**Audrey 교훈**: "If I understand you correctly" 한 줄이면 질문이 도전이 아니라 확인이 된다. 그리고 "am I correct?"는 답을 유도하는 부가의문문. "맞습니까?"보다 "제가 이해한 게 맞나요?"가 훨씬 정중하다.

### 질문 유형 2: 기술 제약 탐색 (Technical Constraint Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Are they dynamic computation during run or it's a good time to create it?` | "Are they dynamic computation during run or it's a good time to create it?" | "A or B" - 선택지 질문으로 답 범위 좁히기 |
| `Do you have any quality criteria for using of X?` | "Do you have any quality criteria for using of graded DRAM?" | "quality criteria" - 기준 탐색 |
| `May I get some prior to them?` + `So what do you think about the priority?` | "May I get some prior to them? So what do you think about the priority?" | "priority" - 우선순위 탐색 |

**Audrey 교훈**: "Are they X or Y?" - 선택지 질문은 답을 쉽게 만든다. 발표자가 "Yes/No"로 답할 수 있게 유도. 그리고 "May I get X?"는 "Can I have X?"보다 정중. "priority"는 회의에서 가장 자주 쓰이는 단어 중 하나 - "우선순위가 뭡니까?"로 의사결정 정보를 캐낸다.

### 질문 유형 3: 가설 시나리오 제안 (Hypothetical Proposal)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If SK hynix provide X, is it possible to make Y version?` | "If SK hynix provide longevity of DDR4, is it possible to make this DDR4 version of this present?" | "If X, is it possible to Y?" - 가설 제안 |
| `This is sort of just ideas.` | "This is sort of just ideas. If SK hynix provide longevity of DDR4..." | "sort of just ideas" - 아이디어임을 먼저 밝힘 |

**Audrey 교훈**: "If X, is it possible to Y?" - 가설을 제시하고 가능성을 묻는 화법. 그리고 "This is sort of just ideas"로 먼저 겸손하게 밝힌다 - "그냥 아이디어 수준입니다" - 아이디어가 거절당해도 체면이 살기 때문. 회의에서 가설을 제안할 때 이 화법을 써라.

### 질문 유형 4: 다음 단계 질문 (Next-Step Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So what can be the next step to meet the Google schedule?` | "So what can be the next step to meet the Google schedule?" | "next step to meet" - 구체적 다음 단계 요구 |
| `I'd like to have a quick question.` | "I'd like to have a quick question. Thank you for your presentation today, but I'd like to ask who gonna make the evaluation test program for this?" | "I'd like to have a quick question" + 감사 + "but" - 정중한 질문 전환 |
| `Thank you for your presentation today, but I'd like to ask X` | "Thank you for your presentation today, but I'd like to ask who gonna make the evaluation test program for this?" | "Thank you, but" - 감사 후 도전 |

**Audrey 교훈**: "Thank you for X, but I'd like to ask Y" - 감사 후 "but"로 도전. "but"가 감사를 도전으로 전환시킨다. 회의에서 발표자에게 어려운 질문을 할 때, 먼저 감사를 표현하고 "but"로 전환. 그리고 "next step to meet the Google schedule" - "Google 일정을 맞추기 위한 다음 단계" - 상대의 일정을 존중하면서 구체적 액션을 요구.

### 질문 유형 5: 확인-반복-동의 (Confirm-Repeat-Agree)

SK 측이 이해를 확인하고 동의를 표현하는 패턴.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Okay, I see.` | "Okay, I see." (반복 사용) | "I see" - 이해 확인 |
| `I can imagine that.` | "I can imagine that." (반복 사용) | "imagine" - 동의 표현 |
| `That is the beauty of it.` | (Google 발표자가 SK 동의를 유도하며) "That is the beauty of it. That they think that they are the only ones in the world." | "the beauty of it" - 장점 강조 |

**Audrey 교훈**: "I see"는 영어 회의에서 가장 자주 쓰이는 동의 표현. "I understand"는 무겁고, "OK"는 가볍다. "I see"가 적당. 그리고 "I can imagine that" - "상상이 됩니다" - 발표자의 설명을 추적하고 있음을 표현.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

회의 후반, 다음 단계와 우선순위를 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 단일 공급 경고 | Google | "it is part of the reason that we're talking about dual source, honestly, is that we see this as mission critical for all of our platforms" | "dual source" - 공급 다변화 명시, "mission critical" - 중요성 강조 |
| 조건부 단일 공급 | Google | "your willingness to build a board that uses DIMMs that we go qualify with other customers puts us in a space where we may be able to do single source through you guys" | "puts us in a space where we may" - 가능성 열어둠 |
| 우선순위 부여 | Google | "if I had to say right now, I would say two capacities, like 576 and 1152, both of those being high volume" | "if I had to say right now" - 임시 답변 표시 |
| 과제 부여 | Google | "I think SK hynix should go off and think about the features that you saw today and come back and let us know what your priorities are" | "go off and think about" - action item 부여 |
| 협상 단계 명시 | Google | "And we can negotiate next level of detail on a business arrangement that enables those features for you" | "next level of detail" - 구체화 단계 |
| 일정 제안 | SK | "if we have a three way meeting with Marvell, so it could be in July or... That would be fine." | "in July or" - 일정 탐색 |

**Audrey 교훈**:
- "dual source"는 회의에서 매우 중요한 단어 - "공급 다변화"의 영어 공식. "We're talking about dual source because this is mission critical" - 중요성을 강조하면서 공급 다변화 필요성을 정당화.
- "puts us in a space where we may be able to do X" - "우리가 X를 할 수 있는 영역으로 우리를 놓는다" - 가능성을 여는 고급 화법. "we can do X"보다 훨씬 조건적이고 정중.
- "if I had to say right now" - "지금 당장 말해야 한다면" - 임시 답변임을 표시. 회의에서 확정 없이 답을 줄 때 써라.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 과제 명시 | Google | "I think SK hynix should go off and think about the features that you saw today and come back and let us know what your priorities are" | "go off and think about" - 과제 명시 |
| 최선 방법 제안 | Google | "I think the best way would be for SK hynix to come back and let us know what properties you see as feasible in a graded media" | "the best way would be for X to Y" - 정중한 지시 |
| 트레이드오프 이해 | Google | "And we would want to understand what the trade-off is between price and reliability there" | "trade-off between X and Y" - 협상 변수 명시 |
| 후속 액션 수용 | SK | "I'll get back to you." | "I'll get back to you" - 후속 약속 |
| 내부 논의 후 재회의 | SK | "it's kind of really discussed inside and then we're gonna discuss level two. Then we're gonna have a meeting with Google again." | "discuss level two" - 단계화 명시 |
| 후속 채널 열기 | Google | "if you have questions about it in the future, by all means, let me know and we'll address it as best we can" | "by all means" - 적극적 초대 |

**Audrey 교훈**: 회의에서 "I'll check"는 약하다. "I'll get back to you" - "다시 연락드리겠습니다" - 후속 약속의 공식. 그리고 "the best way would be for X to Y" - "X가 Y하는 게 최선일 것입니다" - 정중한 지시의 공식. "you should do X"보다 훨씬 부드럽고 권위적.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/AI 메모리/압축 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **double chip kill** | 칩 2개 연속 불량까지 허용하는 ECC 기능 | "we are taking advantage of some of that extra capacity to do double chip kill" - "do X" 동사 활용 |
| **graded DRAM** | 등급별로 분류된 DRAM (품질 차등) | "if there was a scenario where SK hynix has graded DRAM that they would be interested in selling to Google" - "graded" 형용사 |
| **chunk size** | ECC 한 단위가 담당하는 데이터 크기 | "if we can increase the chunk size from the single cache one 64 bytes to 128 bytes" - "increase from X to Y" |
| **on the fly dictionary** | 런타임에 실시간 생성되는 압축 사전 | "the device builds the dictionary on the fly and the dictionary contents never leave the chip" - "on the fly" 부사구 |
| **PII** (Personally Identifiable Information) | 개인 식별 정보 | "dictionary can be considered to have PII, personally identifiable information" - 약어 풀이 |
| **per job compression parameters** | 작업별 압축 매개변수 | "this is essentially a mechanism that lets software come in and tag specific data payloads" - "lets X do Y" |
| **numeric compression** | 수치 데이터 타입 최적화 압축 | "the Google exclusive feature here is numeric compression" - "exclusive"로 차별성 |
| **entropy encoding** | Huffman 등 엔트로피 기반 인코딩 | "we'll have entropy encoding, so which is to say like Huffman encoding on top of LZ4" - "so which is to say" 동의어 |
| **mantissa / exponent / sign** | 부동소수점 구성 요소 | "it is aware of the data type and the locations of things like mantissa, exponent and sign for different data types" - "things like X, Y and Z" |
| **LZ4** | 무손실 압축 알고리즘 | "our first generation product very much relied on LZ4 for compression" - "rely on X for Y" |
| **2X compression ratio** | 2배 압축 비 | "we were targeting a 2X compression ratio" - "target X" 동사 |
| **DDR5 / DDR4** | 차세대/구세대 DRAM 표준 | "this is not 15% capacity anymore with DDR4 because there are fewer ECC bits in DDR4 than there is in DDR5" - 비교 구문 |
| **three DIMMs per channel** | 채널당 DIMM 3개 | "it is six channels and supports three DIMMs per channel" - "X per Y" |
| **CXL pool** | CXL로 공유되는 메모리 풀 | "Server A continuously monitors the pool to see how much free space there is" - "monitor the pool" |
| **free list** | 가용 용량 목록 | "Server can communicate over CXL to get the remaining capacity from their free list" - "from X free list" |
| **variable capacity** | 압축률 따라 변하는 가용 용량 | "the variable capacity is, is absolutely a drawback of using compression" - "drawback of X" |
| **necessary evil** | 필요한 악 | "It is a necessary evil that the host has to be able to deal with" - "necessary evil" 관용구 |
| **dual source** | 이중 공급처 | "we're talking about dual source, honestly, is that we see this as mission critical" - "dual source" |
| **single source** | 단일 공급처 | "we may be able to do single source through you guys, but we need to figure that out" - "single source through X" |
| **JDM** (Joint Design Manufacturer) | 공동 설계 제조사 | "the board that we have being built by a JDM" - "built by X" |
| **graded media** | 등급별 매체 (graded DRAM) | "let us know what properties you see as feasible in a graded media" - "feasible in X" |
| **DPM** (Defects Per Million) | 백만당 결함 수 | "it's really a trade off between the cost and DPM" - "trade off between X and Y" |
| **three way discussion** | 3자 회의 | "I think we should set up a three way discussion with Marvell" - "set up a X discussion with Y" |
| **fall out** | 불량 발생 | "you had fall out where you realized, oh, there's exactly one bad DRAM on this dim" - "fall out where X" |
| **engineering samples** | 엔지니어링 샘플 | (문맥에서 언급) - "samples"로 사전 테스트용 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m36-001
  expression: "Anyway, let me push on to the next feature."
  category: presentation_transition
  function: speaker_control
  speaker_role: presenter
  difficulty: 3
  context: "Anyway, let me push on to the next feature. This is a compression feature on the fly dictionary."
  note: "push on" - 발표자 주도권 유지. "move on"보다 능동적

- id: m36-002
  expression: "And then I just have one more feature and that is X"
  category: presentation_pacing
  function: final_preview
  speaker_role: presenter
  difficulty: 3
  context: "And then I just have one more feature and that is numeric compression."
  note: "one more"로 마지막임 예고 - 청중 집중 유도

- id: m36-003
  expression: "And this is compelling because it can give us X"
  category: value_proposition
  function: benefit_stating
  speaker_role: presenter
  difficulty: 4
  context: "And this is compelling because it can give us higher uptime."
  note: 기능-가치 연결 공식 - "compelling because"

- id: m36-004
  expression: "However, there are very significant X concerns with Y"
  category: constraint_framing
  function: problem_escalation
  speaker_role: presenter
  difficulty: 4
  context: "However, there are very significant security concerns with using a dictionary in that dictionary can be considered to have PII"
  note: 제약을 무겁게 프레이밍 - "significant concerns"

- id: m36-005
  expression: "there are lots of cases where we would like to be using X, but we can't"
  category: constraint_framing
  function: desire_constraint
  speaker_role: presenter
  difficulty: 4
  context: "So there are lots of cases where we would like to be using dictionaries for compression, but we can't"

- id: m36-006
  expression: "And the way we get around that restriction on this device is X"
  category: solution_reveal
  function: constraint_solution
  speaker_role: presenter
  difficulty: 5
  context: "And the way we get around that restriction on this device is the device builds the dictionary on the fly"
  note: "get around that restriction" - 제약 해결 공식. "solve"보다 세련됨

- id: m36-007
  expression: "this is one of the things that we do that is gonna give us significantly higher X"
  category: differentiation
  function: value_emphasis
  speaker_role: presenter
  difficulty: 4
  context: "this is one of the things that we do that is gonna give us significantly higher compression ratios"

- id: m36-008
  expression: "X will be available to anyone that is buying it. But the Y exclusive feature here is Z"
  category: differentiation
  function: commodity_vs_exclusive
  speaker_role: presenter
  difficulty: 5
  context: "Entropy encoding will be available to anyone that is buying it. But the Google exclusive feature here is numeric compression"
  note: "anyone vs exclusive" - 차별성 명시 대비 구조

- id: m36-009
  expression: "That's something you should get from Marvell."
  category: responsibility_redirect
  function: polite_redirect
  speaker_role: presenter
  difficulty: 4
  context: "I'm not talking to you about the baseline features of the Structera device. That's something you should get from Marvell."
  note: "I don't know" 대신 "you should get that from X" - 책임 주체 명시

- id: m36-010
  expression: "When you say X, I'm not sure that I know, are you Y?"
  category: question_clarification
  function: scope_narrowing
  speaker_role: presenter
  difficulty: 5
  context: "When you say evaluation test program, I'm not sure that I know, are you, what kind of evaluation are we talking about"
  note: 질문 용어 범위 좁히기 - "What do you mean?" 대신 정중한 화법

- id: m36-011
  expression: "are we talking about X, are we talking about Y, are we talking about Z?"
  category: question_clarification
  function: checklist_repeat
  speaker_role: presenter
  difficulty: 4
  context: "are we talking about performance, are we talking about functionality, are we talking about manufacturing, or are we talking about design?"
  note: 반복으로 질문 분류 - 3-4회 반복 시 질문자가 자체 정리

- id: m36-012
  expression: "I think it's probably something that you want to talk to X about."
  category: responsibility_redirect
  function: polite_handoff
  speaker_role: presenter
  difficulty: 4
  context: "I think it's probably something that you want to talk to Marvell about."

# ── 회피·포장 (Hedging & Deflection) ──
- id: m36-013
  expression: "X could have been Y. But instead we are taking advantage of that to do Z."
  category: constraint_reframe
  function: limitation_to_opportunity
  speaker_role: presenter
  difficulty: 5
  context: "when we said 15% on the prior slide, that actually could have been 18%. But instead we are taking advantage of some of that extra capacity to do double chip kill."
  note: 가장 중요한 재프레이밍 패턴 - "taking advantage of"로 제약을 솔루션으로

- id: m36-014
  expression: "We're not going to want terribly X, right? even with Y."
  category: polite_refusal
  function: floor_setting
  speaker_role: presenter
  difficulty: 5
  context: "We're not going to want terribly unreliable DRAM, right? even with double chip kill."
  note: "terribly" - 부정 문장에서 "터무니없이" 뉘앙스. 품질 하한선 설정

- id: m36-015
  expression: "So it's gonna be a space where we're going to expect X"
  category: conditional_acceptance
  function: floor_expression
  speaker_role: presenter
  difficulty: 4
  context: "So it's gonna be a space where we're going to expect that we've still done all the testing."
  note: "거절"을 "space"로 포장 - 가능성 열고 조건 단다

- id: m36-016
  expression: "X is possible, but I can't imagine a scenario where that would be useful."
  category: polite_impossibility
  function: soft_negation
  speaker_role: presenter
  difficulty: 5
  context: "it would be possible for Server A to read data over CXL... but I can't imagine a scenario where that would be useful"
  note: "useless" 대신 "can't imagine useful scenario" - 자기 인지 한계로 포장

- id: m36-017
  expression: "you could even imagine a scenario where X"
  category: hypothetical_invitation
  function: scenario_invite
  speaker_role: presenter
  difficulty: 4
  context: "you could even imagine a scenario where we had, where it was not for graded DRAMs so much as DIMs, right?"

- id: m36-018
  expression: "we could imagine still using X in some configuration on this card"
  category: hypothetical_possibility
  function: possibility_open
  speaker_role: presenter
  difficulty: 4
  context: "then we could imagine still using that dim in some configuration on this card"
  note: "we could do X"보다 "we could imagine using X" - 부드럽고 설득적

- id: m36-019
  expression: "the variable capacity is, is absolutely a drawback of using X"
  category: limitation_acknowledgment
  function: honest_limit
  speaker_role: presenter
  difficulty: 4
  context: "the variable capacity is, is absolutely a drawback of using compression, right?"
  note: "absolutely a drawback" - 한계 인정. 솔직함이 신뢰를 만듦

- id: m36-020
  expression: "It is a necessary evil that the host has to be able to deal with X"
  category: limitation_acceptance
  function: necessary_evil_framing
  speaker_role: presenter
  difficulty: 5
  context: "It is a necessary evil that the host has to be able to deal with the fact that sometimes his data is compressible 1.5X and sometimes his data is compressible 3X"
  note: "necessary evil" - 관용구. 불가피한 제약 인정

- id: m36-021
  expression: "That is the beauty of it."
  category: value_emphasis
  function: feature_celebration
  speaker_role: presenter
  difficulty: 3
  context: "That is the beauty of it. That they think that they are the only ones in the world."
  note: "beauty of it" - 장점 강조 관용구

- id: m36-022
  expression: "I keep saying X because it's very important that Y"
  category: emphasis_repeat
  function: importance_flag
  speaker_role: presenter
  difficulty: 4
  context: "I keep saying beyond what you need for compression because it's very important that the compression use case can tolerate the variable capacity already"
  note: "I keep saying X because" - 반복의 정당화

# ── 정중한 도전 (Polite Challenge) ──
- id: m36-023
  expression: "If I understand you correctly."
  category: comprehension_check
  function: polite_preface
  speaker_role: questioner
  difficulty: 4
  context: "If I understand you correctly."
  note: 가장 유용한 정중 질문 화법. 질문 전 한 줄

- id: m36-024
  expression: "It's your idea, am I correct?"
  category: comprehension_check
  function: tag_question
  speaker_role: questioner
  difficulty: 3
  context: "It's your idea, am I correct?"

- id: m36-025
  expression: "Are they X or it's a good time to Y?"
  category: binary_question
  function: scope_narrowing
  speaker_role: questioner
  difficulty: 3
  context: "Are they dynamic computation during run or it's a good time to create it?"

- id: m36-026
  expression: "Do you have any quality criteria for using of X?"
  category: criteria_inquiry
  function: standard_probe
  speaker_role: questioner
  difficulty: 3
  context: "Do you have any quality criteria for using of graded DRAM?"

- id: m36-027
  expression: "May I get some prior to them? So what do you think about the priority?"
  category: priority_inquiry
  function: decision_info_probe
  speaker_role: questioner
  difficulty: 4
  context: "May I get some prior to them? So what do you think about the priority? I just know you cannot decide right now, but I'd like to know the priority."
  note: "I know you cannot decide right now, but" - 결정 못 한다는 걸 인정하면서도 정보 요구

- id: m36-028
  expression: "If SK hynix provide X, is it possible to make Y version?"
  category: hypothetical_proposal
  function: scenario_propose
  speaker_role: questioner
  difficulty: 4
  context: "If SK hynix provide longevity of DDR4, is it possible to make this DDR4 version of this present?"

- id: m36-029
  expression: "This is sort of just ideas."
  category: humble_preface
  function: idea_disclaimer
  speaker_role: questioner
  difficulty: 3
  context: "This is sort of just ideas. If SK hynix provide longevity of DDR4..."
  note: "sort of just ideas" - 거절 대비 겸손 전제

- id: m36-030
  expression: "I'd like to have a quick question."
  category: question_opening
  function: turn_taking
  speaker_role: questioner
  difficulty: 2
  context: "I'd like to have a quick question."

- id: m36-031
  expression: "Thank you for your presentation today, but I'd like to ask X"
  category: thank_then_challenge
  function: polite_challenge
  speaker_role: questioner
  difficulty: 4
  context: "Thank you for your presentation today, but I'd like to ask who gonna make the evaluation test program for this?"
  note: 감사 후 "but"로 도전 전환

- id: m36-032
  expression: "So what can be the next step to meet the Google schedule?"
  category: next_step_probe
  function: action_demand
  speaker_role: questioner
  difficulty: 4
  context: "So what can be the next step to meet the Google schedule?"
  note: "next step to meet X schedule" - 상대 일정 존중하면서 액션 요구

- id: m36-033
  expression: "So how do you X between Y and Z?"
  category: mechanism_inquiry
  function: how_question
  speaker_role: questioner
  difficulty: 3
  context: "So how do you exchange the telemetry data between Server A and Server B?"

- id: m36-034
  expression: "It's hard to understand about that point."
  category: honest_confusion
  function: admission
  speaker_role: questioner
  difficulty: 3
  context: "It's hard to understand about that point."
  note: 모르는 것 솔직하게 표현 - "I don't understand"보다 정중

- id: m36-035
  expression: "Okay, I see."
  category: understanding_marker
  function: comprehension_signal
  speaker_role: questioner
  difficulty: 2
  context: "Okay, I see." (반복 사용)
  note: 회의에서 가장 자주 쓰이는 동의 표현

- id: m36-036
  expression: "I can imagine that."
  category: agreement_marker
  function: tracking_signal
  speaker_role: questioner
  difficulty: 3
  context: "I can imagine that." (반복 사용)

# ── 협상·액션 (Negotiation) ──
- id: m36-037
  expression: "we're talking about dual source, honestly, is that we see this as mission critical"
  category: sourcing_strategy
  function: diversification_justification
  speaker_role: negotiator
  difficulty: 5
  context: "it is part of the reason that we're talking about dual source, honestly, is that we see this as mission critical for all of our platforms"
  note: "dual source" + "mission critical" - 공급 다변화 정당화

- id: m36-038
  expression: "puts us in a space where we may be able to do X"
  category: possibility_open
  function: conditional_possibility
  speaker_role: negotiator
  difficulty: 5
  context: "puts us in a space where we may be able to do single source through you guys, but we need to figure that out"
  note: "we can do X"보다 조건적이고 정중

- id: m36-039
  expression: "if I had to say right now, I would say X"
  category: tentative_answer
  function: provisional_response
  speaker_role: negotiator
  difficulty: 4
  context: "if I had to say right now, I would say two capacities, like 576 and 1152, both of those being high volume"
  note: 임시 답변 표시 - 확정 없이 답을 줄 때

- id: m36-040
  expression: "I think we should set up a three way discussion with X"
  category: next_step_proposal
  function: meeting_proposal
  speaker_role: negotiator
  difficulty: 4
  context: "I think we should set up a three way discussion with Marvell and in particular discuss schedule"

- id: m36-041
  expression: "I think X should go off and think about Y and come back and let us know"
  category: action_item_assignment
  function: task_assignment
  speaker_role: negotiator
  difficulty: 5
  context: "I think SK hynix should go off and think about the features that you saw today and come back and let us know what your priorities are"
  note: "go off and think about" - 정중한 과제 부여

- id: m36-042
  expression: "And we can negotiate next level of detail on a business arrangement"
  category: negotiation_stage
  function: stage_specification
  speaker_role: negotiator
  difficulty: 4
  context: "And we can negotiate next level of detail on a business arrangement that enables those features for you"
  note: "next level of detail" - 협상 단계 명시

- id: m36-043
  expression: "I think the best way would be for X to come back and let us know Y"
  category: polite_directive
  function: best_way_directive
  speaker_role: negotiator
  difficulty: 5
  context: "I think the best way would be for SK hynix to come back and let us know what properties you see as feasible in a graded media"
  note: "you should do X" 대신 "the best way would be for X to Y" - 정중한 지시

- id: m36-044
  expression: "And we would want to understand what the trade-off is between X and Y"
  category: trade-off_inquiry
  function: variable_identification
  speaker_role: negotiator
  difficulty: 4
  context: "And we would want to understand what the trade-off is between price and reliability there"
  note: "trade-off between X and Y" - 협상 변수 명시

- id: m36-045
  expression: "I'll get back to you."
  category: follow_up_commitment
  function: response_promise
  speaker_role: negotiator
  difficulty: 2
  context: "I'll get back to you."
  note: "I'll check" 대신 - 후속 약속 공식

- id: m36-046
  expression: "we're gonna discuss level two. Then we're gonna have a meeting with X again."
  category: stage_planning
  function: next_meeting_preview
  speaker_role: negotiator
  difficulty: 3
  context: "it's kind of really discussed inside and then we're gonna discuss level two. Then we're gonna have a meeting with Google again."

- id: m36-047
  expression: "if you have questions about it in the future, by all means, let me know"
  category: open_contact
  function: standing_invitation
  speaker_role: presenter
  difficulty: 4
  context: "if you have questions about it in the future, by all means, let me know and we'll address it as best we can"
  note: "by all means" - 적극적 초대 관용구

- id: m36-048
  expression: "and we'll address it as best we can"
  category: best_effort_promise
  function: effort_commitment
  speaker_role: presenter
  difficulty: 3
  context: "if you have questions about it in the future, by all means, let me know and we'll address it as best we can"
  note: "as best we can" - 최선 노력 약속

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m36-049
  expression: "X very much relied on Y for Z"
  category: dependency_stating
  function: historical_fact
  speaker_role: presenter
  difficulty: 3
  context: "our first generation product very much relied on LZ4 for compression"
  note: "rely on X for Y" - 의존 관계 표현

- id: m36-050
  expression: "X works well with Y data types"
  category: capability_stating
  function: use_case_fit
  speaker_role: presenter
  difficulty: 3
  context: "it is a compression scheme that works well with numeric data types"

- id: m36-051
  expression: "X can layer on on top of the other features"
  category: layering_capability
  function: composability
  speaker_role: presenter
  difficulty: 4
  context: "this is actually something that can layer on on top of the other features, right? Which is to say we can do numeric compression and then do LZ4 on top of that"
  note: "layer on top of" - 기능 조합 가능 표현

- id: m36-052
  expression: "it is aware of X and the locations of things like Y, Z for different data types"
  category: capability_description
  function: feature_detailing
  speaker_role: presenter
  difficulty: 4
  context: "it is aware of the data type and the locations of things like mantissa, exponent and sine for different data types"
  note: "it is aware of X" - 장치의 인지 능력 표현
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2025-06-10 08 36 16_EN_Google-extracted.wav` (총 ~28분, 2,794단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 7-15) | "double chip kill" - 15% vs 18% 재프레이밍 | 제약을 솔루션으로 포장 | ★★★★ |
| 2 | 기능 설명 (line 31-36) | "on the fly dictionary" - 보안 제약 + 솔루션 | "get around that restriction" 화법 | ★★★★ |
| 3 | 차별성 강조 (line 43-49) | "Google exclusive" + "anyone vs exclusive" 대비 | 차별성 명시 화법 | ★★★ |
| 4 | 메커니즘 설명 (line 96-110) | Server A/B "they never do" + "the beauty of it" | 정중한 부정 + 가치 강조 | ★★★★ |
| 5 | 협상 마무리 (line 154-170) | "three way discussion" + "go off and think about" + "best way would be" | 협상·과제 부여 화법 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 1, 4, 5가 가장 가치 높음 - 제약 재프레이밍·정중한 부정·협상 화법 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **technical pitch + defense** register다. Google 발표자가 CXL 압축 메모리 기능을 설명하고, SK hynix가 기술적으로 검증·탐색하는 구조. 두 역할 모두 학습해야:
- **발표자 역할 (Google)**: 기능-이유-제약-솔루션 4단 설명, 차별성 강조, 책임 소재 명시, 정중한 과제 부여 - 네가 제품 설명할 때
- **질문자 역할 (SK hynix)**: 이해 확인, 가설 제안, 우선순위 탐색, 다음 단계 요구 - 네가 파트너 제품 평가할 때

### Pragmatics (화용론) 핵심
1. **"taking advantage of" 재프레이밍**: 영어 회의에서 제약을 말할 때 "we lost X"는 금지. "We are taking advantage of that to do Y" - "잃은 게 아니라 활용한 것이다". 이게 전문가의 제약 포장.
2. **"anyone vs exclusive" 대비**: 자기 회사 차별성을 강조할 때, 범용 기능과 차별 기능을 대비시킨다. "X is available to anyone, but the exclusive feature is Y" - 이 대비 구조가 차별성을 명확히 만든다.
3. **"I can't imagine a scenario where that would be useful"**: 불가능을 자기 인지의 한계로 포장. "That's useless"는 공격적이고 "I can't imagine"는 겸손하다.
4. **"the best way would be for X to Y"**: 정중한 지시 공식. "you should do X"보다 훨씬 부드럽고 권위적.
5. **"When you say X, are you talking about A, B, or C?"**: 질문을 받았을 때 범위를 좁히는 화법. "What do you mean?"은 공격적으로 들린다.

### 네가 당장 써야 할 Top 5
1. **"X could have been Y. But instead we are taking advantage of that to do Z."** - 제약을 솔루션으로 재프레이밍
2. **"When you say X, I'm not sure I know, are you talking about A, B, or C?"** - 질문 범위 좁히기
3. **"That's something you should get from Marvell."** - 정중한 책임 전가
4. **"I can't imagine a scenario where that would be useful."** - 정중한 불가능 표현
5. **"I think the best way would be for X to come back and let us know Y."** - 정중한 과제 부여

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "손해 봤습니다" | "we are taking advantage of that to do X" | 한국어는 손실, 영어는 "활용"으로 재프레이밍 |
| "모르겠습니다" | "That's something you should get from Marvell" | "I don't know" 대신 책임 주체 명시 |
| "쓸모없습니다" | "I can't imagine a scenario where that would be useful" | 자기 인지 한계로 포장 |
| "X 하세요" | "the best way would be for X to Y" | "you should" 대신 "best way would be" |
| "다음에 확인하겠습니다" | "I'll get back to you" | "check" 대신 "get back to" |
| "이중 공급합니다" | "we're talking about dual source because this is mission critical" | 중요성으로 정당화 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·4절 협상 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 학습**: 발표자(Google) 화법은 "제품 설명할 때", 질문자(SK hynix) 화법은 "파트너 제품 평가할 때" - 두 역할 모두 학습

---

*Textbook 36 - Google CXL/AI Memory Technical Deep-dive (2025-06-10). 회의 유형 A (기술 Deep-dive). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
