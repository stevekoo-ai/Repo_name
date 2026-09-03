---
textbook_id: 09
meeting: Penguin (4TB CXL Hybrid Memory Card + KV Cache Server)
date: 2026-06-09
type: A (기술 Deep-dive)
partner: Penguin (Andy, Mark) - Andy references Marvell photonic modules as prior collaboration reference
sk_side: SK Hynix (Jerry, JK based in San Jose, unnamed Korean technical speaker)
duration_words: 3499
audio: repo/webex-audio/2026-06-09 09 13 00_EN_Penguin-extracted.wav
transcript: repo/webex-audio/2026-06-09 09 13 00_EN_Penguin-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, penguin, cxl, hybrid-memory, kv-cache, technical-deepdive, write-through, dax, fpga-to-asic, loan-negotiation]
---

# Textbook 09 - Penguin 4TB CXL Hybrid Memory Card (2026-06-09)

> **회의 유형**: A (기술 Deep-dive) - 양측이 카드 아키텍처, 캐시 모드, 전원 손실 복구, KV cache 적용을 깊이 논의
> **학습 가치**: Andy의 "개념 비교 + 직접 질문" 발화 설계, Mark의 "실패 모드 분석" 도전 화법, SK 측의 "검토 중" 회피 + 조건부 로드맵
> **Audrey 관점**: 이 회의는 "협력적 기술 평가 + 조건부 협상"의 전형. 네가 SK 입장(카드 설명)이든 Penguin 입장(서버 설계 + 질문)이든 둘 다 배워야. 특히 Penguin이 "우리 측 자원을 빌려줄게"로 협상을 여는 화법이 이 회의의 진짜 협상 가치다.

---

## 1. 발화 아키텍처 - Andy의 "개념 비교 + 모드 나열" 설계 (5단계)

이 회의는 textbook 01처럼 한쪽이 발표하는 구조가 아니다. **양측이 각자 자기 설계를 발표하고 상대의 것을 평가**하는 구조다. Andy(Penguin/Marvell side)가 발화를 주도하며, 그의 발화는 5단계 공식으로 설계된다.

### 단계 1: 상대 설계 재해석 (Reinterpretation Check)

Andy는 SK 측 카드를 자기가 이해한 대로 다시 그려보고, "이게 맞느냐"고 먼저 확인한다. **질문이 아니라 "내가 그린 다이어그램"으로 검증**하는 게 핵심.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I redrew this for this meeting just so I could talk through and understand better what you were thinking` | "what we're exploring for our next generation memory AI server here, and I redrew this for this meeting just so I could talk through and understand better what you were thinking" | "내가 다시 그렸다" - 준비성 표시 + 상대 설계 검증 |
| `So am I correct in thinking this is what you're building?` | "So am I correct in thinking this is what you're building? This card here?" | "내 생각이 맞느냐" - 정중한 확인 질문 |
| `that's what you'd like to demonstrate ... Correct?` | "that's what you'd like to demonstrate and potentially demonstrate either super computing or flash memory summit. Correct?" | "Correct?" - 확인형 태그 질문 |

**Audrey 교훈**: 영어 회의에서 상대의 설계나 의도를 확인할 때, "Is this what you mean?"은 약하다. Andy처럼 **"I redrew this for this meeting"** - "내가 이해한 대로 다시 그렸다" - 라고 먼저 말해. 이게 "네 설명을 안 듣고 넘어갔다"가 아니라 "네 설명을 바탕으로 내가 정리했다"는 시그널이다. 그 다음 "am I correct in thinking X?"로 검증. 이 2단 화법을 외워.

### 단계 2: 개념 비교 (Conceptual Comparison)

Andy는 SK 카드를 Marvell의 photonic module에 비교해 설명한다. **자기가 아는 것에 연결해서 이해를 검증**하는 전문가 화법.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `in a weird way, this would be conceptually similar to our X, except that Y` | "in a weird way, this, Andy, just tell me if I'm thinking about this correctly or not, would be conceptually similar to our photonic modules, except that the photonic modules are HBM in front of DIMMs, right?" | "conceptually similar to X, except that Y" - 유사성 + 차이점 |
| `Just tell me if I'm thinking about this correctly or not` | "Andy, just tell me if I'm thinking about this correctly or not" | "내 생각이 맞는지만 말해 달라" - 정중한 검증 초대 |
| `I mean, conceptually, yes. Yeah, you're right. Except in this case, you've got persistence, consistency involved, right?` | (Andy 응답) "I mean, conceptually, yes. Yeah, you're right. Except in this case, you've got persistence, consistency involved, right?" | "Yes, you're right. Except X" - 동의 + 차이 추가 |

**Audrey 교훈**: 새로운 것을 설명하거나 이해할 때, "It's like X"라고만 하면 부정확하다. "It would be conceptually similar to X, except that Y" - "X와 개념적으로 비슷한데, Y가 다르다" - 이 공식을 써. 동의를 받으면서도 차이점을 명시. 그리고 "in a weird way"로 먼저 겸손하게 시작하는 게 Andy의 스타일이다. 회의에서 "this is just like X"라고 단정 짓지 말고, "in a weird way, this would be conceptually similar to X"로 시작해.

### 단계 3: 모드 나열 (Mode Enumeration)

기술적 선택지를 "you could put it in different modes"로 묶어서 나열한다. **한 번에 여러 모드를 보여주는 게 전문가의 설명**이다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `you could put it in different modes, right? Depending on your tolerance per data loss` | "you could put it in different modes, right? Depending on your, your tolerance per, per day loss" | "여러 모드가 있다" + "data loss 허용치에 따라" - 선택지 프레이밍 |
| `If you know you're dealing with a lot of transient data, you might just say, ah, I don't care. I just, just make it a full tier` | "If you know you're dealing with a lot of transient data, you might just say, ah, I don't care. I just, just make it a full tier" | 조건 + 의사결정 예시 |
| `Or you could make it, as you were saying earlier, mark a right through` | "Or you could make it, as you were saying earlier, mark a right through" | "Or you could make it X" - 대안 모드 제시 |

**Audrey 교훈**: 기술 회의에서 "이렇게 해야 합니다"가 아니라 **"you could put it in different modes"** - "여러 모드로 설정할 수 있다" - 로 시작해. 선택지를 주는 게 전문가의 설명이다. 그 다음 "If you know X, you might say Y"로 조건별 의사결정을 보여줘. 한국어로는 "경우에 따라 다릅니다"인데, 영어는 "depending on your tolerance"로 허용치를 명시하고 "If you know X, you might say Y"로 사례를 준다.

### 단계 4: 추론 노출 (Reasoning Out Loud)

Andy는 자기 생각을 회의에 그대로 드러낸다. "If you've got X, then Y. So it's sort of, it may be irrelevant to Z." - **생각 과정을 보여주면서 상대의 반응을 끌어내는 화법**.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If you've got X, right? ... And so it's sort of, it may be irrelevant to worry about Y` | "If you've got, because if you're combining the CXL memory into system RAM, right? ... And so it's sort of, it may be irrelevant to, to worry about these cards from a super cap type of strategy" | "X라면 Y를 걱정하는 게 무의미할 수 있다" - 자기 반박 노출 |
| `getting, unless you're going to be prepared to get the whole thing back up again, do its recovery state` | "getting, unless you're going to be prepared to get the whole thing back up again, do its recovery state" | "unless X" 조건부 전환 |
| `then just having these cards be safe is sort of overkill` | "Then, then just having these cards be safe is sort of overkill" | 결론 도출 - "overkill"로 판단 표시 |

**Audrey 교훈**: 영어 회의에서 완벽하게 정리된 의견만 말할 필요는 없다. Andy처럼 **"If X, then Y. So it's sort of, it may be irrelevant to Z"** - 생각 과정을 그대로 말해. 이게 상대가 "그건 아닌데요"라고 반응하게 만드는 자연스러운 화법이다. 한국어로는 "음, 그러니까요"로 막 시작하는데, 영어는 "If you've got X, right?"로 가정을 먼저 명시하고 "And so it's sort of, it may be irrelevant"로 결론을 끌어내. "sort of"가 판단의 강도를 줄여서 상대가 반박하기 쉽게 만든다.

### 단계 5: 가능성 제안 (Possibility Proposal)

Andy는 "it's not a stretch to think that we could X"로 공동 개발 가능성을 제안한다. **확언하지 않고 "어렵지 않을 것이다"로 여는 화법**.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So it's not a stretch to think that we could make a board in collaboration with SK here that could do what you're saying, right?` | "So it's not a stretch to think that we could make a board in collaboration with SK here that could do what you're saying, right?" | "not a stretch to think that we could X" - 가능성 제안 |
| `we're already contemplating with our current LICs, the Lithium-Ion capacitor design we have, of saving up to 128` | "we're already contemplating with our current LICs, the Lithium-Ion capacitor design we have, of saving up to 128" | "we're already contemplating X" - 진행 중인 연구로 신뢰 부여 |
| `So it's not a stretch for 256 level, because you don't have to back up the 4TB` | "So it's not a stretch for 256 level, because you don't have to back up the 4TB, clearly, the business on black already" | "not a stretch for X" - 기술적 가능성 평가 |

**Audrey 교훈**: "We can do X"는 강한 약속이다. "It's not a stretch to think that we could X" - "X하는 게 큰 무리가 아닐 것이다" - 가 확언을 피하면서 가능성을 여는 화법이다. 회의에서 공동 개발을 제안할 때, "we can build this"가 아니라 **"it's not a stretch to think that we could build this in collaboration with X"**를 써. "contemplating"도 좋은 단어다 - "we're already contemplating X" - "이미 고민하고 있다" - 가 진지함을 전달한다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 양측이 어떻게 약점을 정중하게 포장하는지.

### 전략 1: "검토 중" 회피 (Investigation-Status Deflection)

SK 측이 가장 많이 쓰는 패턴. 명확한 답을 피하면서도 진지함을 유지.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| ASIC 전환 계획 | "Just under investigation and discussion. I mean, just, we just some approved the, the, the feasibility of that card concept for the certain type of the workload or applications and prove it first and then we will move to the ASIC version." | "검토·논의 중입니다. 카드 콘셉트의 타당성을 특정 워크로드/애플리케이션에 대해 승인받았고, 먼저 증명한 뒤 ASIC 버전으로 넘어갈 예정입니다" |
| 대용량 달성 방법 | "currently, under the discussion, how we can achieve the huge scale of the memory capacity" | "현재 논의 중입니다, 어떻게 대용량 메모리 용량을 달성할지" |
| 전원 손실 대응 | "I think we need to prepare some certain momentary power drop case. But I think that there are some procedures to keep that data under the procedure that is back defined." | "순간 정전 대비가 필요하긴 합니다. 단, 데이터를 보존하는 절차가 정의돼 있을 거라고 생각합니다" |

**패턴 공식**: `Just under investigation and discussion. We just approved the feasibility of X. We will prove it first and then move to Y.`

**Audrey 교훈**: 한국어 "검토 중입니다"의 영어 버전이 **"Just under investigation and discussion"**이다. 단순히 "We're considering it"보다 구체적이다 - "investigation"(조사)과 "discussion"(논의)을 함께 쓰면 "우리도 진지하게 보고 있다"는 시그널. 그리고 "we will prove it first and then we will move to Y" - "먼저 증명하고 넘어간다" - 면서 시간순서 로드맵을 주면 거부감이 줄어든다. 네가 SK 입장에서 명확한 답을 못 주겠을 때, "We're under investigation" + 로드맵 순서를 붙여.

### 전략 2: 조건부 로드맵 (Conditional Roadmap)

확약 없이 "조건이 맞으면 다음 단계로"를 반복.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| FPGA에서 ASIC 전환 | "we just some approved the, the feasibility of that card concept for the certain type of the workload or applications and prove it first and then we will move to the ASIC version" | "특정 워크로드/애플리케이션에 대한 카드 콘셉트 타당성을 승인받았고, 먼저 증명한 뒤 ASIC 버전으로 넘어갈 예정" |
| 전원 손실 대비 절차 | "I think that there are some procedures to keep that data under the procedure that is back defined. So I think we should consider that kind of procedure." | "데이터 보존 절차가 정의돼 있을 것으로 생각합니다. 그런 절차를 고려해야 할 것 같습니다" |

**패턴 공식**: `We will prove it first and then we will move to X. I think we should consider Y.`

**Audrey 교훈**: "We will do X"는 약속이다. "We will prove it first and then we will move to X" - "먼저 증명하고 넘어가겠다" - 가 **조건부 로드맵**이다. 증명이 성공하면 넘어간다는 뉘앙스. 그리고 "I think we should consider X" - "고려해야 할 것 같다" - 가 자신의 의견을 약하게 만드는 회피. "We should do X"가 아니라 "I think we should consider X" - 한 단계 더 약하게. 회의에서 약속을 피하고 싶을 때, "We will prove it first and then we will move to X"를 써.

### 전략 3: 자원 부족 + 가능성 열기 (Resource Constraint + Opening)

Penguin 측이 자원이 부족하다고 인정하면서도 "논의는 가능"으로 문을 여는 패턴. **"안 됩니다"로 끝내지 않는 협상 화법**.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| KV cache server 빌려주기 | "We don't have a lot we can just provide to you in your lab, but it is something we can certainly discuss and see if it's something you, for the shows, we can certainly loan, loan something." | "당신 랩에 제공할 여분이 많지 않습니다. 하지만 논의는 가능하고, 전시회용으로는 빌려드릴 수 있을지 검토하겠습니다" |
| 가능성 검토 | "We can look into that, see if we have enough available to loan you." | "검토해 보고, 충분히 빌려드릴 수 있는지 보겠습니다" |
| 이메일 후속 | "we should probably discuss that a little bit more to see if JK feels that that makes sense" | "JK가 의미 있다고 느끼는지 보기 위해 좀 더 논의해야 할 것 같습니다" |

**패턴 공식**: `We don't have a lot we can X. But it is something we can certainly discuss. We can look into that, see if we have enough available to Y.`

**Audrey 교훈**: 자원을 줄 수 없을 때 "We can't do that"는 협상 종료다. **"We don't have a lot we can provide, but it is something we can certainly discuss"** - "많이는 못 주지만, 논의는 가능" - 가 협상을 여는 화법. 그리고 "We can look into that, see if we have enough available to loan you" - "검토해 보고, 충분히 빌려드릴 수 있는지 보겠다" - 가 조건부 약속. "We can" + "see if" 조합이 "we'll try"보다 훨씬 진지하다. 회의에서 자원·일정·인력을 줄 수 없을 때, "We don't have a lot, but it is something we can discuss"를 써.

### 전략 4: 약점 인정 + 맥락으로 재프레이밍 (Concession + Context Reframe)

SK 측이 "전원 손실에 안전하지 않다"는 약점을 인정하되, "전체 시스템 복구 관점에서는 무의미할 수 있다"고 Andy가 재프레이밍.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 전원 손실 미대비 | (SK) "Actually, not at this time." → (Andy) "if that goes away because of a power failure, it's gone. And so it's sort of, it may be irrelevant to worry about these cards from a super cap type of strategy" | (SK) "현재는 아닙니다." → (Andy) "전원 실패 시 시스템 RAM도 날아가는데, 이 카드만 supercap으로 보호하는 건 무의미할 수 있다" |
| tiering 미확정 | (Mark) "it sounds like you're not fully defined yet on the tiering versus caching nature." → (SK) "That's why I don't know the primary concept is the tiered memory." | (Mark) "tiering vs caching 중 아직 확정 안 된 것 같네요." → (SK) "주된 콘셉트는 tiered memory입니다" |

**패턴 공식**: (상대 약점 인정) → (Andy) `If X goes away, it's gone. So it may be irrelevant to worry about Y from a Z strategy.`

**Audrey 교훈**: 상대의 약점을 공격하면 협상이 굳는다. Andy는 **"네 약점을 인정하되, 전체 맥락에서 보면 다른 것도 같이 죽기 때문에 네 카드만 보호하는 건 무의미"** 로 재프레이밍. "It may be irrelevant to worry about X from a Y strategy" - "Y 관점에서 X를 걱정하는 건 무의미할 수 있다" - 가 부드러운 재프레이밍이다. "irrelevant"가 핵심 단어 - "관련 없다"가 아니라 "걱정할 필요 없다"는 뉘앙스. 회의에서 파트너 약점을 다룰 때, "It may be irrelevant to worry about X"로 맥락을 바꿔.

### 전략 5: 검증 초대로 신뢰 구축 (Verification Invitation)

Andy가 "내가 맞게 이해하고 있느냐"고 반복 질문하면서 신뢰를 구축. **정확한 답을 요구하면서도 공격적이지 않은 화법**.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 다이어그램 검증 | "I redrew this for this meeting just so I could talk through and understand better what you were thinking" | "이해를 돕기 위해 이번 회의용으로 다시 그렸습니다" |
| 개념 검증 | "Just tell me if I'm thinking about this correctly or not" | "내 생각이 맞는지만 말해 주세요" |
| 카드 검증 | "So am I correct in thinking this is what you're building? This card here?" | "제가 맞게 이해하고 있는지, 이 카드가 맞나요?" |
| 데모 의도 검증 | "that's what you'd like to demonstrate and potentially demonstrate either super computing or flash memory summit. Correct?" | "FMS나 Supercomputing에서 demo하길 원하시는 거죠, 맞습니까?" |

**패턴 공식**: `I redrew this for this meeting. Just tell me if I'm thinking about this correctly. Am I correct in thinking X? ... Correct?`

**Audrey 교훈**: 회의 시작에 "내가 다이어그램을 다시 그렸다"고 하면, 상대는 "이 사람이 내 설명을 듣고 정리했다"고 느낀다. 그리고 "Just tell me if I'm thinking about this correctly" - "내 생각이 맞는지만 말해 달라" - 가 **질문이 아니라 확인**이라는 시그널. "Am I correct in thinking X?"와 "Correct?" 태그 질문을 조합. 회의에서 상대 설계를 검증할 때, "Is this right?"보다 "Am I correct in thinking X? Correct?"가 훨씬 정중하면서 정확하다.

---

## 3. 정중한 도전 화법 (질문자 화법)

### 질문 유형 1: 보장 질문 (Guarantee Probe)

기술적 보장이 있는지 직접 묻되, "보장되나요?"가 아니라 "보장을 받는 거죠, 아니면 supercap이 있나요?"로 대안을 제시.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `are you guaranteed that you get it right by the time that you're using it or does that have a supercap or something on it to make sure that any last writes got there?` | "are you guaranteed that you get it, you get it right by the time that you're using it or does that have a supercap or something on it to make sure that any last writes got there?" | "보장되나요, 아니면 supercap이 있나요?" - 이진 질문으로 압박 |
| `It's not intended for that. It's more intended just for capacity play, I assume.` | "it's, it's not intended for that. It's more intended just for capacity play, I assume" | "I assume" - 추정 표시로 도전 부드럽게 |

**Audrey 교훈**: "Is it guaranteed?"는 예스/노 질문이라 약하다. **"are you guaranteed that X, or does that have Y?"** - "X가 보장되나요, 아니면 Y가 있나요?" - 가 대안을 제시하는 도전 질문이다. 상대가 둘 중 하나를 골라야 한다. 그리고 "I assume"으로 자기 추정을 표시하면, 상대가 "아닙니다"라고 반박하기 쉽다. 회의에서 보장·조건을 물을 때, "Is X guaranteed, or does Y exist?"를 써.

### 질문 유형 2: 실패 모드 분석 (Failure Mode Analysis)

Mark가 가장 잘 쓰는 화법. 정상 동작이 아니라 **실패 시나리오**를 구체적으로 묻는다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `if you miss, if the RAM is full for any reason, you've saturated the RAM with a lot of sequential writes, then there's a chance that you will start operating more flash speeds instead of memory` | "if you miss, if the RAM is full for any reason, you've saturated the RAM with a lot of sequential writes, then there's a chance that you will start operating more flash speeds instead of memory on the load store operations" | "X 경우에 Y가 될 가능성이 있다" - 실패 모드 명시 |
| `So it's not safe from power loss. Unfortunately, sounds like.` | "So Mark, it's not safe from power loss. Unfortunately, sounds like." | "Unfortunately, sounds like" - 부정적 판단을 부드럽게 전달 |
| `it's, it's not intended for that. It's more intended just for capacity play, I assume.` | "it's, it's not intended for that. It's more intended just for capacity play, I assume" | "I assume" - 추정 표시로 도전 부드럽게 |

**Audrey 교훈**: 기술 회의에서 가장 날카로운 질문은 "이게 되나요?"가 아니라 **"이렇게 실패하면 어떻게 되나요?"** 다. Mark의 "if you miss, if the RAM is full for any reason" - "RAM이 가득 차면 어떻게 되느냐" - 가 실패 모드 분석. 한국어로는 "만약에요"로 시작하는데, 영어는 "If you miss, if X happens, then there's a chance that Y"로 실패 확률까지 명시. 그리고 결론을 "Unfortunately, sounds like"로 부드럽게 내놓는다. 회의에서 파트너 제품을 평가할 때, 정상 동작이 아니라 실패 시나리오를 물어.

### 질문 유형 3: 직접 로드맵 질문 (Direct Roadmap Probe)

Mark와 Andy가 가장 직접적으로 묻는 질문. **"제품화 계획이 있느냐"** 는 정면 도전.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `What is your plan to turn this into a technology or product?` | "So what, what, what is your plan to turn this into a technology or product?" | "계획이 뭡니까?" - 직접 도전 |
| `Is there a plan to make this into an ASIC SK that we can collaborate on?` | "Is there a plan to make this into an ASIC SK that, that we can collaborate on?" | "협력 가능한 ASIC 계획이 있습니까?" - 협업 의사 표시 + 질문 |
| `Or what's your, what's your long-term plan?` | "Or what's your, what's your long-term plan?" | "장기 계획이 뭡니까?" - 연속 도전 |

**Audrey 교훈**: 회의 후반에 "What is your plan to turn this into a technology or product?" - **"이걸 제품화할 계획이 뭡니까?"** - 가 가장 직접적인 도전. 한국어로는 "계획이 어떻게 되시는지요?"로 정중하게 묻는데, 영어는 "What is your plan to turn X into Y?"로 직접 묻는다. "Is there a plan to make this into an ASIC that we can collaborate on?" - "우리가 협력할 수 있는 ASIC 계획이 있느냐" - 가 **협업 의사를 먼저 표시하고 질문**하는 화법. "협력하고 싶은데 계획이 있느냐" - 이게 협상의 시작이다.

### 질문 유형 4: 짧은 확인 (Quick Confirmation)

Mark와 Andy가 자주 쓰는 "right?", "Correct?" 짧은 태그 질문.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Correct?` | "that's what you'd like to demonstrate ... Correct?" | 짧은 확인 - 발표 흐름 유지 |
| `right?` | "the photonic modules are HBM in front of DIMMs, right?" | "right?" - 대화형 확인 |
| `Is that the thinking right now that we use our KB Cache server and showcase that on your booth at Flash Memory Summit and Supercomputing?` | "Is that the thinking right now that we use our KB Cache server and showcase that on your booth at Flash Memory Summit and Supercomputing?" | "Is that the thinking right now" - 현재 계획 확인 |

**Audrey 교훈**: 발표 중 긴 질문은 흐름을 끊는다. "Correct?" - 한 단어로 확인. 그리고 "Is that the thinking right now" - "지금 생각이 그건가요" - 가 **현재 의도를 재확인**하는 정중한 화법. "What's your current thinking?"보다 부드럽다. 회의에서 계획·의도를 확인할 때, "Is that the thinking right now?"를 써.

### 질문 유형 5: 전문 용어 정정 요청 (Terminology Clarification)

끝 부분에서 SK 측이 CX7을 묻고, Andy가 답하는 짧은 패턴. **모르는 용어를 정중하게 묻는 화법**.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `could you explain a little bit more about the CX7?` | "could you explain a little bit more about the CX7?" | "조금 더 설명해 주시겠어요" - 정중한 요청 |
| `What is this CXL IO? Is it, is that a card type or adapter IO?` | "What is this CXL IO? Is it, is that a card type or adapter IO? I mean, what is the, this here?" | "이게 뭡니까? 카드형인가요 어댑터형인가요?" - 이진 질문 |
| `I see. I understand. Thank you.` | "I see. Okay. I understand. Thank you." | 짧은 인정 + 감사 |

**Audrey 교훈**: 모르는 용어가 나오면 "What is X?"가 아니라 **"could you explain a little bit more about X?"** - "X에 대해 좀 더 설명해 주시겠어요" - 가 정중하다. 그리고 "Is it X or Y?"로 이진 질문을 하면 상대가 답하기 쉽다. 답을 들으면 "I see. I understand. Thank you."로 짧게 인정. 이 3단 - 요청, 이진 질문, 인정 - 가 모르는 것을 묻는 정중한 패턴이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 협상은 **Penguin이 자원(KV cache server)을 빌려주는 조건으로 SK와 공동 demo**를 하는 구조. 후속 협상과 action item을 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 진지함 표시 | Andy | "I think, I think we are, we have genuine interest, right?" | "genuine interest" - 진지함의 공식 표현 |
| 가치 발견 | Andy | "I like about this is with only four cards, you've got 16TB already" | "I like about X" - 긍정 평가 표현 |
| 용도 매핑 | Andy | "this would be super interesting for like KV cache, right?" | "this would be super interesting for X" - 용도 제안 |
| 동의 확대 | Andy | "You read my mind exactly" | "내 마음을 읽었네" - 강한 동의 표현 |
| 조건부 자원 제공 | Penguin | "we can certainly loan, loan something. We can look into that, see if we have enough available to loan you" | "we can certainly loan" + "see if we have enough available" - 조건부 제안 |
| 자원 부족 인정 | Penguin | "We don't have a lot we can just provide to you in your lab, but it is something we can certainly discuss" | 부정 + "But" + 가능성 |
| 이메일 후속 | Andy | "I'll follow up with JK as well. And I send him an email just to see if JK is based in San Jose" | "follow up with X" - 후속 채널 명시 |
| 동의 검증 | Andy | "we should probably discuss that a little bit more to see if JK feels that that makes sense" | "see if JK feels that makes sense" - 의사결정자 거치기 |
| 협력 의지 | SK | "I'm looking forward to having good collaboration for DFMS" | "looking forward to having good collaboration for X" - 협력 표현 |
| 논의 지속 | Andy | "Let's keep the discussion going. I will, I'll take it offline on email." | "keep the discussion going" + "take it offline" - 후속 채널 전환 |
| 동기화 제안 | Andy | "Then let's see if we can sync up a little bit more." | "sync up" - 동기화 제안 |
| 실수 사과 | Andy | "Sorry about the confusion." / "no, no, no problem" | 협상 마무리의 정중함 |

**Audrey 교훈**: 
- **"We have genuine interest"** - "genuine"이 핵심. "We're interested"는 약하지만, "genuine interest"는 "진짜 관심이 있다" - 진지함의 공식 표현. 협상을 열 때 써.
- **"You read my mind exactly"** - "내 마음을 읽었네" - 가 강한 동의. "I agree"보다 훨씬 따뜻하고, "exactly"가 확신을 더한다.
- **"We can certainly loan something. We can look into that, see if we have enough available"** - 조건부 자원 제공의 전형. "certainly"로 긍정, "see if"로 조건.
- **"Take it offline on email"** - 회의 중 안 끝난 논의를 이메일로 넘기는 화법. "Take it offline"이 공식 표현.
- **"Sync up a little bit more"** - "좀 더 동기화하자" - 가 협상 후속의 부드러운 표현. "Let's keep in touch"보다 구체적.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 이메일 후속 약속 | Andy | "I'll follow up with JK as well. And I send him an email just to see if JK is based in San Jose" | "follow up with X" + 이메일 채널 |
| 자원 검토 약속 | Penguin | "We can look into that, see if we have enough available to loan you" | "look into that" + "see if" - 검토 약속 |
| 후속 채널 명시 | Andy | "I will, I'll take it offline on email. Then let's see if we can sync up a little bit more" | "take it offline on email" - 채널 명시 |
| 협력 일정 | SK | "I'm looking forward to having good collaboration for DFMS" | "looking forward to having X for Y" - 일정 명시 |

**Audrey 교훈**: 이 회의의 action item은 **"follow up with X on email"** + **"see if we can sync up"** 패턴. "I'll check"는 약하다. **"I'll follow up with JK on email"** - "JK에게 이메일로 후속하겠다" - 가 책임 명시. 그리고 "see if we can sync up" - "동기화할 수 있는지 보겠다" - 가 **다음 미팅을 여는 화법**. 회의에서 다음 스텝을 정할 때, "follow up with X on email" + "see if we can sync up"을 써.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL hybrid memory / KV cache / 전시회 데모 전문 용어.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **CXL hybrid memory card** | DDR5 buffer + flash 결합 CXL 카드 | "4TB CXL memory flash for the hybrid product, which would be the flash and the memory all on one card" - SK 측 카드 콘셉트 |
| **write-through cache** | 쓰기 시 원본 동시 갱신하는 캐시 | "you could make it, as you were saying earlier, mark a right through" / "operate this four terabyte as a 256 in write through cash mode" - 모드 선택 |
| **tiered memory / tiering** | 핫/콜드 데이터 계층화 메모리 | "the primary concept is the tiered memory" / "you tear proactively tear active data to and from the flash" - SK 측 기본 콘셉트 |
| **DAX (Direct Access) memory** | Linux에서 물리적으로 분리된 메모리로 인식 | "you can also declare CXL and these cards as what they're called DAX memory" - CXL 선언 모드 |
| **interleaved memory** | 여러 메모리를 하나의 pool로 묶어 인식 | "We choose to interleave it. So it looks like it's the same as these guys" - 현재 Penguin 설계 |
| **supercap / Lithium-Ion capacitor (LIC)** | 전원 실패 시 데이터 플러시용 축전지 | "we're already contemplating with our current LICs, the Lithium-Ion capacitor design we have, of saving up to 128" - Penguin 자체 설계 |
| **persistence** | 전원 실패 후 데이터 보존 | "you've got persistence, consistency involved, right?" - Andy가 SK 카드의 차이점으로 언급 |
| **transient data** | 일시적 데이터 (손실 허용) | "If you know you're dealing with a lot of transient data, you might just say, ah, I don't care" - 모드 결정 기준 |
| **KV cache server** | LLM 추론 시 KV cache 전용 서버 | "we operate a Valky database on our KV cache server" - Penguin 제품 |
| **Valky** | KV store 데이터베이스 (Penguin 사용) | "we operate a Valky database on our KV cache server. So this is really a Valky plus Ubuntu configuration" - Penguin 스택 |
| **Redis** | in-memory KV store | "for a Redis database, we operate a Valky database on our KV cache server" - 비교 언급 |
| **RDMA** | 원격 직접 메모리 접근 | "we're getting towards a full RDMA transfer in and out about memory" - 전송 기술 |
| **EDSFF** | 서버 폼팩터 (Enterprise SSD) | "they already have the adapter, the converting from the airing card to the EDSFF" - 변환 어댑터. 단, 시장 수용도 낮다고 언급 |
| **AIC card (Add-In Card)** | 확장 카드 (전사 "airing card") | "we are considering having the airing card concept brought up" - 전사 오류 주의 |
| **retimer** | 신호 재생 장치 | "it's just a simple retimer" - CXL IO 설명 |
| **liquid expansion box** | 액체 냉각 확장 섀시 | "the liquid expansion box as a product that Penguin will sell" - Penguin 제품 |
| **FPGA vs ASIC** | 프로토타입 vs 양산 칩 | "It's just FPGA form today ... prove it first and then we will move to the ASIC version" - SK 로드맵 |
| **AI-MFRA** | AI Memory, Fabric, Rack Architectures 행사 | "we have a AI-MFRA demonstration that we're going to run in September" - SK 전시 일정 |
| **FMS (Flash Memory Summit)** | 플래시 메모리 산업 행사 | "demonstrate either super computing or flash memory summit" - 공동 데모 후보 |
| **OCP (Open Compute Project)** | 오픈 하드웨어 행사 | "for the industry event like FMS or Supercomputing, OCP as well" - 데모 후보 |
| **Supercomputing (SC)** | 슈퍼컴퓨팅 행사 | "demonstrate either super computing or flash memory summit" - 데모 후보 |
| **HP Discovery** | HP 서버 행사 | "we will bring its liquid box to the HP Discovery event in June" - SK 일정 |
| **DLM Cache / LM Cache** | LLM 캐시 소프트웨어 | "we've been testing a lot with LLM Cache and KB Cache that configure the DLLM, you know, LM Cache environments" - Penguin 테스트 환경 |
| **RTX 6000** | NVIDIA 워크스테이션 GPU | "we have an RTX 6000 card in there" - Penguin 랩 서버 |
| **CX7 (ConnectX-7)** | NVIDIA 400Gb 이더넷 카드 | "CX7 is the... It's a DME network card. It's the Kinect 7 from NVIDIA" - 네트워크 카드 |
| **field replaceable / recovery state** | 현장 교체 / 복구 상태 | "getting, unless you're going to be prepared to get the whole thing back up again, do its recovery state" - 시스템 복구 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# - 발표 설계 (Speaker Architecture) -
- id: m09-001
  expression: "I redrew this for this meeting just so I could talk through and understand better what you were thinking"
  category: preparation_signal
  function: preparedness_display
  speaker_role: questioner
  difficulty: 5
  context: "what we're exploring for our next generation memory AI server here, and I redrew this for this meeting just so I could talk through and understand better what you were thinking"
  note: "내가 다시 그렸다" - 준비성 표시 + 상대 설계 검증. 회의 시작 화법.

- id: m09-002
  expression: "So am I correct in thinking this is what you're building?"
  category: comprehension_check
  function: polite_verification
  speaker_role: questioner
  difficulty: 4
  context: "So am I correct in thinking this is what you're building? This card here?"

- id: m09-003
  expression: "that's what you'd like to demonstrate ... Correct?"
  category: tag_question
  function: intent_confirm
  speaker_role: questioner
  difficulty: 3
  context: "that's what you'd like to demonstrate and potentially demonstrate either super computing or flash memory summit. Correct?"

- id: m09-004
  expression: "in a weird way, this would be conceptually similar to our X, except that Y"
  category: conceptual_comparison
  function: analogy_with_difference
  speaker_role: expert
  difficulty: 5
  context: "in a weird way, this, Andy, just tell me if I'm thinking about this correctly or not, would be conceptually similar to our photonic modules, except that the photonic modules are HBM in front of DIMMs, right?"
  note: "conceptually similar to X, except that Y" - 유사성 + 차이. 전문가의 개념 비교.

- id: m09-005
  expression: "Just tell me if I'm thinking about this correctly or not"
  category: verification_invite
  function: polite_check
  speaker_role: expert
  difficulty: 4
  context: "Andy, just tell me if I'm thinking about this correctly or not"
  note: "내 생각이 맞는지만 말해 달라" - 정중한 검증 초대

- id: m09-006
  expression: "I mean, conceptually, yes. Yeah, you're right. Except in this case, you've got X"
  category: agree_with_exception
  function: partial_agreement
  speaker_role: expert
  difficulty: 4
  context: "I mean, conceptually, yes. Yeah, you're right. Except in this case, you've got persistence, consistency involved, right?"

- id: m09-007
  expression: "you could put it in different modes, right? Depending on your tolerance per data loss"
  category: mode_enumeration
  function: option_framing
  speaker_role: expert
  difficulty: 4
  context: "you could put it in different modes, right? Depending on your, your tolerance per, per day loss"
  note: 선택지 프레이밍 - 전문가의 설명 화법

- id: m09-008
  expression: "If you know you're dealing with a lot of transient data, you might just say, ah, I don't care"
  category: conditional_decision
  function: scenario_example
  speaker_role: expert
  difficulty: 4
  context: "If you know you're dealing with a lot of transient data, you might just say, ah, I don't care. I just, just make it a full tier"

- id: m09-009
  expression: "Or you could make it, as you were saying earlier, X"
  category: alternative_mode
  function: option_presenting
  speaker_role: expert
  difficulty: 3
  context: "Or you could make it, as you were saying earlier, mark a right through"

- id: m09-010
  expression: "If you've got X, right? And so it's sort of, it may be irrelevant to worry about Y"
  category: reasoning_out_loud
  function: self_refutation
  speaker_role: expert
  difficulty: 5
  context: "If you've got, because if you're combining the CXL memory into system RAM, right? ... And so it's sort of, it may be irrelevant to, to worry about these cards from a super cap type of strategy"
  note: 자기 반박 노출 - 상대의 반응을 끌어내는 화법

- id: m09-011
  expression: "then just having these cards be safe is sort of overkill"
  category: judgment_expression
  function: softened_judgment
  speaker_role: expert
  difficulty: 4
  context: "Then, then just having these cards be safe is sort of overkill"
  note: "sort of overkill" - 부드러운 판단 표현

- id: m09-012
  expression: "So it's not a stretch to think that we could X in collaboration with Y"
  category: possibility_proposal
  function: collaboration_opening
  speaker_role: expert
  difficulty: 5
  context: "So it's not a stretch to think that we could make a board in collaboration with SK here that could do what you're saying, right?"
  note: "not a stretch to think that we could X" - 가능성 제안. 확언 회피.

- id: m09-013
  expression: "we're already contemplating with our current X, the Y design we have, of Z"
  category: ongoing_research
  function: credibility_signal
  speaker_role: expert
  difficulty: 4
  context: "we're already contemplating with our current LICs, the Lithium-Ion capacitor design we have, of saving up to 128"

- id: m09-014
  expression: "So it's not a stretch for X level, because you don't have to back up Y"
  category: feasibility_assessment
  function: technical_judgment
  speaker_role: expert
  difficulty: 4
  context: "So it's not a stretch for 256 level, because you don't have to back up the 4TB, clearly"

# - 회피·포장 (Hedging & Deflection) -
- id: m09-015
  expression: "Just under investigation and discussion"
  category: status_deflection
  function: polite_evasion
  speaker_role: presenter
  difficulty: 4
  context: "Just under investigation and discussion. I mean, just, we just some approved the, the, the feasibility of that card concept"
  note: "검토 중입니다" 영어 버전. investigation + discussion 병용이 진지함 시그널.

- id: m09-016
  expression: "we just approved the feasibility of X for the certain type of the workload, prove it first and then we will move to Y"
  category: conditional_roadmap
  function: phased_commitment
  speaker_role: presenter
  difficulty: 5
  context: "we just some approved the, the, the feasibility of that card concept for the certain type of the workload or applications and prove it first and then we will move to the ASIC version"
  note: 조건부 로드맵 - "증명하고 넘어가겠다"

- id: m09-017
  expression: "currently, under the discussion, how we can achieve X"
  category: ongoing_discussion
  function: vague_roadmap
  speaker_role: presenter
  difficulty: 3
  context: "currently, under the discussion, how we can achieve the huge scale of the memory capacity"

- id: m09-018
  expression: "I think we need to prepare some certain momentary power drop case"
  category: limitation_admission
  function: weakness_acknowledgment
  speaker_role: presenter
  difficulty: 4
  context: "I think we need to prepare some certain momentary power drop case. But I think that there are some procedures to keep that data"

- id: m09-019
  expression: "I think that there are some procedures to keep that data under the procedure that is back defined"
  category: procedural_deflection
  function: vague_assurance
  speaker_role: presenter
  difficulty: 4
  context: "I think that there are some procedures to keep that data under the procedure that is back defined. So I think we should consider that kind of procedure."
  note: "절차가 있을 것" - 구체적 약속 회피

- id: m09-020
  expression: "We don't have a lot we can just provide to you in your lab, but it is something we can certainly discuss"
  category: constraint_with_opening
  function: refusal_with_door
  speaker_role: negotiator
  difficulty: 5
  context: "We don't have a lot we can just provide to you in your lab, but it is something we can certainly discuss and see if it's something you, for the shows, we can certainly loan, loan something."
  note: 부정 + "But" + 가능성. 자원 부족 인정 + 협상 문 열기.

- id: m09-021
  expression: "We can look into that, see if we have enough available to loan you"
  category: conditional_offer
  function: soft_commitment
  speaker_role: negotiator
  difficulty: 4
  context: "We can look into that, see if we have enough available to loan you."
  note: "We can" + "see if" - 조건부 약속의 정형화

- id: m09-022
  expression: "we should probably discuss that a little bit more to see if JK feels that that makes sense"
  category: decision_deferral
  function: decision_maker_reference
  speaker_role: negotiator
  difficulty: 4
  context: "we should probably discuss that a little bit more to see if JK feels that that makes sense"
  note: 의사결정자 거치기 - "see if X feels that makes sense"

- id: m09-023
  expression: "if that goes away because of a power failure, it's gone"
  category: reality_check
  function: blunt_assessment
  speaker_role: expert
  difficulty: 3
  context: "if that goes away because of a power failure, it's gone. And so it's sort of, it may be irrelevant to, to worry about these cards from a super cap type of strategy"

- id: m09-024
  expression: "it may be irrelevant to worry about X from a Y strategy"
  category: reframe
  function: context_shift
  speaker_role: expert
  difficulty: 5
  context: "it may be irrelevant to, to worry about these cards from a super cap type of strategy"
  note: 맥락 재프레이밍 - "irrelevant"가 핵심 단어

- id: m09-025
  expression: "That's why I don't know the primary concept is the tiered memory"
  category: clarification_after_challenge
  function: restate_core
  speaker_role: presenter
  difficulty: 3
  context: "it sounds like you're not fully defined yet on the tiering versus caching nature. That's why I don't know the primary concept is the tiered memory."

# - 정중한 도전 (Polite Challenge) -
- id: m09-026
  expression: "are you guaranteed that you get it right by the time that you're using it or does that have a supercap or something on it to make sure that any last writes got there?"
  category: guarantee_probe
  function: binary_challenge
  speaker_role: questioner
  difficulty: 5
  context: "are you guaranteed that you get it, you get it right by the time that you're using it or does that have a supercap or something on it to make sure that any last writes got there?"
  note: 이진 질문 - 보장 vs 대안. 가장 강한 도전 화법.

- id: m09-027
  expression: "if you miss, if the RAM is full for any reason, you've saturated the RAM with a lot of sequential writes, then there's a chance that you will start operating more flash speeds instead of memory"
  category: failure_mode_analysis
  function: edge_case_probe
  speaker_role: questioner
  difficulty: 5
  context: "if you miss, if the RAM is full for any reason, you've saturated the RAM with a lot of sequential writes, then there's a chance that you will start operating more flash speeds instead of memory on the load store operations"
  note: 실패 모드 분석 - 가장 날카로운 질문 유형

- id: m09-028
  expression: "Unfortunately, sounds like."
  category: softened_negative
  function: gentle_judgment
  speaker_role: questioner
  difficulty: 3
  context: "So Mark, it's not safe from power loss. Unfortunately, sounds like."

- id: m09-029
  expression: "it's not intended for that. It's more intended just for capacity play, I assume"
  category: assumption_statement
  function: inference_check
  speaker_role: questioner
  difficulty: 4
  context: "it's, it's not intended for that. It's more intended just for capacity play, I assume"

- id: m09-030
  expression: "What is your plan to turn this into a technology or product?"
  category: roadmap_probe
  function: direct_challenge
  speaker_role: questioner
  difficulty: 4
  context: "So what, what, what is your plan to turn this into a technology or product?"

- id: m09-031
  expression: "Is there a plan to make this into an ASIC SK that, that we can collaborate on?"
  category: collaboration_probe
  function: partnership_signal
  speaker_role: questioner
  difficulty: 4
  context: "Is there a plan to make this into an ASIC SK that, that we can collaborate on? Or what's your, what's your long-term plan?"
  note: 협업 의사 표시 + 질문 - 협상의 시작

- id: m09-032
  expression: "Is that the thinking right now that we use our X and showcase that on your booth at Y?"
  category: intent_confirm
  function: current_plan_check
  speaker_role: questioner
  difficulty: 4
  context: "Is that the thinking right now that we use our KB Cache server and showcase that on your booth at Flash Memory Summit and Supercomputing?"

- id: m09-033
  expression: "could you explain a little bit more about X?"
  category: terminology_request
  function: polite_clarification
  speaker_role: questioner
  difficulty: 3
  context: "could you explain a little bit more about the CX7?"

- id: m09-034
  expression: "Is it, is that a card type or adapter IO? I mean, what is the, this here?"
  category: binary_question
  function: quick_clarification
  speaker_role: questioner
  difficulty: 3
  context: "What is this CXL IO? Is it, is that a card type or adapter IO? I mean, what is the, this here?"

# - 협상·액션 (Negotiation & Action) -
- id: m09-035
  expression: "I think, I think we are, we have genuine interest, right?"
  category: interest_stating
  function: serious_intent
  speaker_role: negotiator
  difficulty: 4
  context: "I think, I think we are, we have genuine interest, right?"
  note: "genuine interest" - 진지함의 공식 표현. "We're interested"보다 강함.

- id: m09-036
  expression: "I like about this is with only four cards, you've got 16TB already"
  category: value_discovery
  function: positive_evaluation
  speaker_role: negotiator
  difficulty: 3
  context: "what I like about this is with only four cards, you've got 16TB already"

- id: m09-037
  expression: "this would be super interesting for like X, right?"
  category: use_case_mapping
  function: application_suggest
  speaker_role: negotiator
  difficulty: 3
  context: "this would be super interesting for like KV cache, right?"

- id: m09-038
  expression: "You read my mind exactly"
  category: strong_agreement
  function: enthusiastic_align
  speaker_role: negotiator
  difficulty: 3
  context: "You read my mind exactly."
  note: "내 마음을 읽었네" - 강한 동의. "I agree"보다 따뜻.

- id: m09-039
  expression: "we can certainly loan, loan something"
  category: conditional_offer
  function: resource_offer
  speaker_role: negotiator
  difficulty: 4
  context: "we can certainly loan, loan something. We can look into that, see if we have enough available to loan you."

- id: m09-040
  expression: "I'll follow up with X as well. And I send him an email just to see if X is based in Y"
  category: follow_up_commitment
  function: channel_commitment
  speaker_role: negotiator
  difficulty: 3
  context: "I'll follow up with JK as well. And I send him an email just to see if JK is based in San Jose"

- id: m09-041
  expression: "I'm looking forward to having good collaboration for X"
  category: partnership_expression
  function: cooperation_intent
  speaker_role: negotiator
  difficulty: 3
  context: "I'm looking forward to having good collaboration for DFMS"

- id: m09-042
  expression: "Let's keep the discussion going"
  category: continuity_expression
  function: keep_open
  speaker_role: negotiator
  difficulty: 3
  context: "Yeah. Let's keep the discussion going."

- id: m09-043
  expression: "I will, I'll take it offline on email"
  category: channel_shift
  function: move_offline
  speaker_role: negotiator
  difficulty: 4
  context: "I will, I'll take it offline on email. Then let's see if we can sync up a little bit more."
  note: "take it offline on email" - 회의 후 이메일로 넘기는 공식 표현

- id: m09-044
  expression: "let's see if we can sync up a little bit more"
  category: sync_proposal
  function: next_meeting_open
  speaker_role: negotiator
  difficulty: 4
  context: "Then let's see if we can sync up a little bit more."
  note: "sync up" - 동기화 제안. "keep in touch"보다 구체적.

- id: m09-045
  expression: "Sorry about the confusion"
  category: apology
  function: graceful_recovery
  speaker_role: negotiator
  difficulty: 2
  context: "Sorry about the confusion."

- id: m09-046
  expression: "no, no, no problem"
  category: acceptance
  function: dismiss_apology
  speaker_role: negotiator
  difficulty: 2
  context: "no, no, no problem"

# - 도메인 어휘 활용 (Vocabulary in Context) -
- id: m09-047
  expression: "we operate a X database on our Y server"
  category: stack_description
  function: tech_stack
  speaker_role: expert
  difficulty: 3
  context: "we operate a Valky database on our KV cache server. So this is really a Valky plus Ubuntu configuration"

- id: m09-048
  expression: "we're getting towards a full X transfer in and out about memory"
  category: capability_stating
  function: tech_progress
  speaker_role: expert
  difficulty: 4
  context: "we're getting towards a full RDMA transfer in and out about memory"

- id: m09-049
  expression: "we're still building up our X. We don't have a lot we can just provide to you in your lab"
  category: capacity_constraint
  function: resource_reality
  speaker_role: negotiator
  difficulty: 3
  context: "we're still building up our KB Cache servers. We don't have a lot we can just provide to you in your lab"

- id: m09-050
  expression: "is it something we are configured and set up to do"
  category: capability_check
  function: ability_confirm
  speaker_role: negotiator
  difficulty: 3
  context: "So it is something we are configured and set up to do."

- id: m09-051
  expression: "we have to focus less on X because of its, its market acceptance has been low"
  category: market_assessment
  function: market_reality
  speaker_role: presenter
  difficulty: 4
  context: "We, we have to focus less on EDSFF because of its, its market acceptance has been low."

- id: m09-052
  expression: "as far as I know, he has his own software solution to do some offline or the leasing of the X"
  category: third_party_capability
  function: indirect_reference
  speaker_role: presenter
  difficulty: 4
  context: "As far as I know, he has his own software solution to do some offline or the leasing of the the QVC cache data."
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-06-09 09 13 00_EN_Penguin-extracted.wav` (총 ~30분 추정, 3,499단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | line 범위 | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입부 (~01:30) | line 1-15 | Andy가 현재 카드 셋업 설명 + "I redrew this for this meeting" + 4TB 카드 콘셉트 확인 | 발표 시작 화법 + 다이어그램 검증 | ★★☆ |
| 2 | 개념 비교 (~05:00) | line 49-58 | "conceptually similar to our photonic modules, except that..." + write-through cache 보장 질문 | 개념 비교 + 이진 도전 질문 | ★★★ |
| 3 | 실패 모드 분석 (~08:30) | line 84-99 | Mark의 "if the RAM is full for any reason..." + Andy의 "it may be irrelevant to worry about these cards from a super cap type strategy" | 실패 모드 도전 + 맥락 재프레이밍 | ★★★★ |
| 4 | DAX 모드 + 가능성 (~12:00) | line 116-138 | "CXL allows you to declare memory one or two ways" + "it's not a stretch to think that we could make a board in collaboration with SK" | 모드 나열 + 공동 개발 가능성 제안 | ★★★★ |
| 5 | 로드맵 질문 + 협상 (~19:00) | line 183-197 | "What is your plan to turn this into a technology or product?" + SK의 "under investigation" + Penguin의 "we can certainly loan something" | 직접 로드맵 도전 + 조건부 자원 제공 | ★★★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 5가 가장 가치 높음 - 실패 모드 도전과 협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **협력적 기술 평가 + 조건부 협상** register다. 양측이 각자 기술을 발표하고 상대의 것을 평가하며, 동시에 공동 demo와 자원 loan이라는 협상을 진행. 두 역할 모두 학습해야:
- **Andy 역할 (Penguin/Marvell 기술 전문가)**: 개념 비교, 모드 나열, 추론 노출, 가능성 제안 - 네가 파트너 기술을 평가할 때
- **Mark 역할 (Penguin 애플리케이션)**: 실패 모드 분석, 직접 로드맵 질문 - 네가 파트너 제품의 한계를 물을 때
- **SK 측 역할**: "검토 중" 회피, 조건부 로드맵, 절차적 미룸 - 네가 SK 입장에서 답을 피해야 할 때

### Pragmatics (화용론) 핵심
1. **"I redrew this for this meeting"**: 회의 시작에 이 말을 하면, "내가 네 설명을 듣고 정리했다"는 시그널. 상대는 "이 사람이 준비했다"고 느낀다. 회의 첫 5분에 가장 중요한 화법.
2. **"are you guaranteed that X, or does that have Y?"**: 보장을 물을 때 이진 질문이 가장 강하다. "Is it guaranteed?"는 예스/노로 끝나지만, "X보장이 되나요, 아니면 Y가 있나요?"는 상대가 구체적으로 답해야 한다.
3. **"We don't have a lot we can X, but it is something we can certainly discuss"**: 자원·시간·인력을 줄 수 없을 때, "안 됩니다"로 끝내지 말고 "많이는 못 주지만 논의는 가능"으로 문을 열어.
4. **"We can look into that, see if we have enough available"**: 조건부 약속의 정형화. "We can" + "see if" - "할 수 있고, 충분한지 보겠다" - 가 "We'll try"보다 진지.
5. **"it's not a stretch to think that we could X"**: 공동 개발 가능성을 열 때. "We can do X"는 강한 약속이지만, "not a stretch to think that we could X" - "X하는 게 큰 무리가 아닐 것이다" - 가 확언을 피한다.

### 네가 당장 써야 할 Top 5
1. **"I redrew this for this meeting just so I could talk through and understand better what you were thinking"** - 회의 시작 준비성 표시
2. **"Just under investigation and discussion. We will prove it first and then we will move to X"** - 정중한 회피 + 조건부 로드맵
3. **"are you guaranteed that X, or does that have Y?"** - 이진 도전 질문
4. **"We don't have a lot we can X, but it is something we can certainly discuss"** - 자원 부족 + 가능성 열기
5. **"I'll take it offline on email. Let's see if we can sync up a little bit more"** - 후속 채널 전환

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "검토 중입니다" | "Just under investigation and discussion" | 한국어는 한 단어, 영어는 investigation + discussion 병용이 진지함 |
| "다음 단계로 넘어가겠습니다" | "we will prove it first and then we will move to X" | 영어는 "증명하고 넘어간다" - 조건부 로드맵 |
| "자원이 부족합니다" | "We don't have a lot we can X, but it is something we can certainly discuss" | 영어는 부정 + "But" + 가능성 |
| "보장되나요?" | "are you guaranteed that X, or does that have Y?" | 영어는 이진 질문으로 압박 |
| "이메일로 후속하겠습니다" | "I'll take it offline on email. Let's see if we can sync up" | 영어는 "take it offline" + "sync up" - 채널 전환 공식 |
| "이해한 대로 다시 그렸습니다" | "I redrew this for this meeting just so I could talk through and understand better" | 영어는 "talk through and understand" - 과정 명시 |
| "그건 무의미할 수 있습니다" | "it may be irrelevant to worry about X from a Y strategy" | 영어는 "irrelevant" + "from a Y strategy" - 맥락 명시 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **역할 학습**: Andy 화법(평가자)과 SK 화법(회피자)을 번갈아 연습 - 네가 어느 쪽이든 대응 가능하도록

---

*Textbook 09 - Penguin 4TB CXL Hybrid Memory Card (2026-06-09). 회의 유형 A (기술 Deep-dive). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
