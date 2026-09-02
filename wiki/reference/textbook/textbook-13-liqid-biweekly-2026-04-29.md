---
textbook_id: 13
meeting: Liqid biweekly (HPE Discover prep, Liqid system delivery, CXL roadmap, KV Cache)
date: 2026-04-29
type: C (sample/schedule coordination) - confirmed
partner: Liqid (Sumit, Thomas, Paulino)
sk_side: Steve (Product Planning/App Engineering), Jongmin (App Engineering), CPCP (Memory System Research)
duration_words: 4522
audio: repo/webex-audio/2026-04-29 08 52 22_EN_Liqid_biweekly-extracted.wav
transcript: repo/webex-audio/2026-04-29 08 52 22_EN_Liqid_biweekly-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, liqid, cxl, hpe-discover, fms, kv-cache, schedule-coordination, sample-request, roadmap]
---

# Textbook 13 - Liqid Biweekly (2026-04-29)

> **회의 유형**: C (sample/schedule coordination) - 격주 biweekly 운영회의. 샘플 수량·배송 일정·타임라인 조율이 본질. KV cache 성능 분석은 agenda tail의 기술 업데이트로, 본 질이 아님.
> **학습 가치**: 격주 회의의 agenda 운영, 수량/일정 요청, "we'll check internally" 협상, 공동 demo/white paper action item 합의, KV cache 캐시 hit rate 성능 논증.
> **Audrey 관점**: 이 회의는 "coordination + gentle push"의 전형. 네가 SK 측 coordinator일 때 쓸 화법이 밀집. agenda 4개를 순회하며 각 item마다 "let's move on to the next"로 전환하고, 요청은 직접적으로, 거절은 "let us discuss internally"로 포장한다.

---

## 1. 발화 아키텍처 - Steve의 agenda 운영 (4단계)

Steve가 biweekly 운영회의를 여는 구조. 격주 회의의 본질은 "agenda 순회 + 각 item 합의 + action item 캡처"다.

### 단계 1: Agenda 개시 (Agenda Opening)

회의 시작 시 agenda를 개조식으로 나열한다. "Let's get started" 뒤 "today, agenda are N items"로 구조화.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `since we haven't met before, so I guess straight to the point to save your time` | "Actually, since we haven't met before, so I guess straight to the point to save your time" | 새 참가자(Paulino)에게 배려 + 효율性 표시 |
| `So today, Agenda are four items. First, we will discuss...` | "So today, Agenda are four items. First, we will discuss the preparation for the HPD showcase. And second, we'll check the current status..." | 번호 부여 + 동사 부여 (discuss/check/share) |
| `Let's move on to the first item.` | "Let's move on to the first item." | 전환 공식 - agenda 단위 이동 |

**Audrey 교훈**: 회의 시작에 "today, agenda are N items"로 개조식 나열은 기본이다. 핵심은 각 item에 **동사**를 부여하는 것 - "discuss / check / share". 한국어는 "첫 번째는 HPE showcase 준비입니다"로 명사로 끝나도 되지만, 영어는 "we will discuss / we will check / I will share"로 동사를 명시해야 action이 된다. 그리고 "straight to the point to save your time" - 새 참가자에게 "시간 아껴drably 직접 가겠다"는 배려 화법을 외워.

### 단계 2: 항목별 질문/요청 (Item-Level Ask)

각 agenda item마다 Steve는 **상황 설명 → 직접 질문**의 2단 구조를 쓴다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `As you know, X only supports Y. So I've asked Z to prepare...` | "As you know, the SK Hynix 6CXL product only supports E3.S form factor. So I've asked Trit to prepare an adapter for E3.S" | "As you know"로 공유 context 가정 + 요청 사유 설명 |
| `So how many adapters can you provide for this setup? Can you answer this?` | "So how many adapters can you provide for this setup? Can you answer this?" | 수량 직접 질문 - "how many"로 명시적 요청 |
| `So would it be possible for Liqid to deliver directly to our event booth?` | "So would it be possible for a Liqid to delivery the directory to our event booth?" | "would it be possible" - 정중한 가능성 탐색 |
| `If not, I will check internally how to arrange the delivery.` | "If not, I will check internally how to arrange the delivery." | plan B 명시 - "if not, I will"로 대안 책임 |

**Audrey 교훈**: 수량/일정 요청은 직접적으로. "how many can you provide?" - 한국어 "몇 개 가능할까요?"의 영어 버전이다. 그리고 "would it be possible for X to Y?" - 가능성을 탐색하는 정중한 요청 화법. 뒤에 "If not, I will check internally"을 붙이면, 거절에 대비한 plan B를 보여주어 상대방의 부담을 줄인다. 이게 coordination 회의의 핵심 화법이다.

### 단계 3: 항목 전환 (Item Transition)

각 item이 끝나면 "Let's move on to next"로 전환한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Let's move on to next.` | "Let's move on to next." | 항목 전환 공식 |
| `Let's move on to the next page.` | "Let's move on to the next page." | 슬라이드/문서 기반 전환 |
| `Okay, and next, shift to the showcase agenda.` | "Okay, and next, shift to the showcase agenda." | "shift to X" - 주제 명시 전환 |
| `The next item is the joint promotion.` | "the next item is the joint promotion" | "next item is X" - agenda 재개 |

**Audrey 교훈**: "Let's move on"은 기본이고, "shift to X"가 좀 더 explicit한 전환 화법이다.韩国어 "다음으로 넘어가시죠"의 영어 버전. 회의 진행자라면 이 "move on / shift to / next item is" 세 가지 전환 공식을 돌려 써라. 같은 표현만 반복하면 기계적으로 들린다.

### 단계 4: 합의·action item 캡처 (Agreement Capture)

각 item 끝에 action item을 명시적으로 합의한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So if you agree, let's make it an action item for today.` | "So if you agree, let's make it an action item for today." | action item 합의 - "let's make it an action item" |
| `And going to iron out the details in the next few meetings.` | "And going to iron out the details in the next few meetings." | "iron out the details" - 세부 사항 조율 표현 |
| `What's your thoughts on this?` | "What's your thoughts on this?" | 동의 구하기 - "what's your thoughts" |
| `After we take the liquid rack, we immediately start to prepare the remote demo. So please help to set up this showcase.` | "After we take the liquid rack, we immediately start to prepare the remote demo. So please help to set up this showcase." | "please help to set up" - 협조 요청 |

**Audrey 교훈**: "let's make it an action item" - 이 표현이 coordination 회의의 핵심이다. 합의된 사항을 "action item"으로 명시하면 회의록에 책임이 남는다. "iron out the details"는 "세부 사항을 다듬다" - 회의에서 자주 쓰는 고급 표현이다. 한국어 "세부 사항은 다음 회의에서 조율하죠"의 영어 버전.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 진짜 학습 가치. Liqid 측이 일정/자원 한계를 어떻게 정중하게 포장하는지.

### 전략 1: "let us discuss internally" (Internal Discussion Deferral)

가장 자주 쓰는 회피. 추가 자원 요청을 즉시 거절하지 않고 "내부 논의"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| San Jose에 Liqid box 추가 설치 요청 | "Yeah, let us discuss internally. It's easier to run the demo from the liquid lab if we have to ship everything to the Hynex facility in San Jose. There's a lot involved. It's not just the liquid chassis, there's servers and networking and everything else." | "네, 내부 논의해 보겠습니다. San Jose로 보내려면 liquid lab에서 demo 돌리는 게 더 쉽습니다. chassis만이 아니라 서버·네트워크 등 다 들어가니까요" |
| 추가 구매 예산 확인 | "But understood on the ask, we will go check internally." | "요청은 이해했습니다. 내부에서 확인하겠습니다" |
| 양측 확인 합의 | "Okay, if you can check on your side, we will check on our side." | "그쪽에서 확인해 주시면, 저희도 확인하겠습니다" |

**패턴 공식**: `Let us discuss internally. It's not just X, there's Y and everything else. But understood on the ask, we will go check internally.`

**Audrey 교훈**: "let us discuss internally"는 "검토해 보겠습니다"의 영어 버전이지만, 뒤에 **이유**를 붙인다 - "It's not just X, there's Y"로 왜 어려운지 설명. 한국어는 "검토해 보겠습니다"로 끝내도 되지만, 영어는 "It's a lot involved"로 구체적 어려움을 제시해야 정중하게 들린다. 그리고 "understood on the ask" - "요청은 이해했습니다"로 상대방의 요청을 인정하되, "we will check internally"로 결정을 미룬다.

### 전략 2: 대안 제시로 회피 (Alternative Redirect)

직접 거절 대신 "이건 어떠세요?"로 방향을 바꾼다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| San Jose 설치 대신 Colorado 원격 access 제안 | "So would it be possible for you guys to come to our Colorado facility and set up the demo there, and then we can provide you guys remote access? Is that an option?" | "Colorado facility에 와서 demo setup 하시면, remote access 제공해 드릴까요? 이건 가능할까요?" |
| Las Vegas 직송 제안 | "I think maybe the best option and we'll confirm the logistics is we can ship it maybe directly to the show in Las Vegas. Or we can ship it to your facility ahead of the show." | "가장 좋은 옵션은 Las Vegas 행사장 직송입니다. 아니면 행사 전에 your facility로 보낼 수도 있습니다" |

**패턴 공식**: `Would it be possible for you to X? Is that an option?`

**Audrey 교훈**: "Is that an option?" - "이것도 옵션인가요?" - 대안을 제시하고 상대방에게 선택권을 넘기는 화법. 거절이 아니라 "대안 제안"으로 들리게 한다. "would it be possible for you to X"는 정중한 제안 공식이다. 이걸 외워.

### 전략 3: 일정 한정을 "safer assumption"으로 포장

불확실 일정을 보수적으로 발표하여 기대치를 낮춘다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| CXL Gen 3 Atlas II 일정 | "Our full Atlas II systems for testing at the end of this year, at the earliest, but more than likely it's going to be Q1 of next year before we have physical systems" | "Atlas II full system은 올해 말 earliest, 하지만 more than likely Q1 next year" |
| GA 일정 | "The goal is, GA is going to be next year in 27. It's going to be the second half of 27. So first samples, end of Q4 this year, more than likely Q1 of next year." | "GA는 27년 second half. 첫 샘플은 올해 Q4 말, more than likely Q1 next year" |
| 일정 가정 확인 | "I think that's the safer assumption." | "그게 safer assumption입니다" |

**패턴 공식**: `At the earliest X, but more than likely Y. I think that's the safer assumption.`

**Audrey 교훈**: "more than likely" - "아마도" - 일정을 보수적으로 발표하는 화법. "at the earliest"로 최선 케이스를 말하고, "more than likely"로 실제 기대치를 낮춘다. 그리고 "that's the safer assumption" - "그게 더 안전한 가정입니다" - 일정을 확정짓지 못하는 상황에서 상대방의 기대를 관리하는 화법. 일정을 약속할 때 무조건 "safer assumption" 쪽으로 발표해라.

### 전략 4: 비용 탓으로 미루기 (Cost-Based Deferral)

일정 가속을 비용 투자 문제로 돌린다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Atlas II 일정 가속 가능성 | "It's a function of how quickly we pay for expedited development. So we know the design we're building. We know how we're going to build it... It's just a function of how much do we want to invest in expediting the development." | "expedited development에 얼마나 빨리 지불하느냐의 문제입니다. 설계는 압니다. 구축 방법도 압니다. 얼마나 투자하느냐의 문제입니다" |
| 비용 추가 시 조기 수령 | "If we decided to spend more earlier, then it's possible for us to get the chassis sooner. But in the current timeline, without spending the extra expedited fees with Acton, more than likely it's going to be Q1." | "더 일찍 쓰기로 하면 chassis를 빨리 받을 수 있습니다. 하지만 현재 timeline에서는 Q1" |

**패턴 공식**: `It's a function of how much we want to invest in expediting. If we decided to spend more earlier, it's possible to get X sooner.`

**Audrey 교훈**: "It's a function of X" - "X의 함수입니다" - 일정을 의사결정/투자 문제로 프레이밍. "우리 마음대로 안 됩니다"가 아니라 "얼마나 투자하느냐에 달렸습니다"로 듣는 사람에게 선택권을 넘긴다. 한국어 "예산 문제입니다"의 영어 버전. 그리고 "expedited fees" - "expedited"는 "가속 처리"의 업계 용어.

### 전략 5: 자원 한정 인정 + 협조 의사 표시 (Resource-Acknowledge + Cooperate)

자원이 부족하다는 것을 인정하되, "돕고 싶다"는 의사를 강조한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 추가 시스템 지원 | "We want to help you guys. We want to enable the testing. We can go ask for discounts and all of that kind of stuff. We want to help you guys as much as possible here." | "도와드리고 싶습니다. testing enable하고 싶습니다. discount 요청도 해볼 수 있습니다. 최대한 돕고 싶습니다" |
| BIOS 확보 노력 | "We have Super Micro. Now we have a Dell BIOS in-house. Cisco is working on a BIOS for us. And as you guys know, HPE already has a BIOS, but that's only in their labs." | "Super Micro 있고, Dell BIOS도 이제 in-house로 받았습니다. Cisco도 작업 중입니다. HPE는 자체 lab에만 있습니다" |

**패턴 공식**: `We want to help you guys. We want to enable X. We can go ask for Y. But as mentioned, it's more than Z.`

**Audrey 교훈**: "We want to help"를 반복하는 것 - Liqid가 거절하려는 게 아니라 "돕고 싶다"는 의사를 강조. "enable the testing" - "testing을 가능하게 하다" - 이 동사가 중요하다. 그리고 "we can go ask for discounts" - 할인 요청도 해볼 수 있다고 제안. 거절을 "최대한 노력"으로 포장하는 화법이다.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 일정/자원을 협상하면서 정중하게 도전하는 패턴.

### 질문 유형 1: 수량 직접 질문 (Quantity Direct Ask)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So how many adapters can you provide for this setup? Can you answer this?` | "So how many adapters can you provide for this setup? Can you answer this?" | "how many"로 수량 명시 요청 |
| `We know that the Liqid solution will be shipped in the May time frame. So, you want to check that if there are any kinds of issues or you want to recheck the schedule?` | "We know that the Liqid solution will be shipped in the May time frame. So, you want to check that if there are any kinds of issues or you want to recheck the schedule?" | 일정 재확인 - "recheck the schedule" |

**Audrey 교훈**: "how many"는 직접적이지만 coordination 회의에서는 적절. "Can you answer this?"를 붙여서 "대답 가능할까요?"로 답을 요구. 한국어 "몇 개 가능한지 답변 주실 수 있을까요?"와 동일한 화법. 일정 재확인은 "we know X is planned for Y, so we want to recheck if there are any issues" - "알고 있지만 재확인하고 싶다"로 정중하게 일정을 검증한다.

### 질문 유형 2: 가능성 탐색 (Possibility Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is there any possibility that Liqid box can be landed to the Solet, which is located in San Jose?` | "Is there any possibility that liquid box can be landed to the solet, which is located in San Jose? For one set" | "Is there any possibility" - 가능성 탐색 |
| `Is there other R&D that could be done on the liquid chassis in San Jose?` | "Is there other R&D that could be done on the liquid chassis in San Jose?" | 추가 용도 제안 - "Is there other X" |
| `Maybe if there's broader use for the chassis in San Jose beyond FMS, maybe it would make sense for a purchase of gear for San Jose?` | "Maybe if there's broader use for the chassis in San Jose beyond FMS, maybe it would make sense for a purchase of gear for San Jose?" | "would make sense for X" - 정중한 제안 |

**Audrey 교훈**: "Is there any possibility that X can Y?" - 가능성을 탐색하는 정중한 질문. "Would it make sense for X?" - "X가 의미 있을까요?" - 추가 투자를 유도하는 화법. SK 측이 Liqid에게 추가 자원을 요청할 때 직접 "주세요"가 아니라 "가능성 있는가요? 의미 있을까요?"로 정중하게 밀어붙인다.

### 질문 유형 3: 조건부 합의 (Conditional Agreement)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If the schedule is fixed, please share the schedule to our site.` | "If the schedule is fixed, please share the schedule to our site." | "if X, please Y" - 조건부 후속 요청 |
| `If not, I will check internally how to arrange the delivery.` | "If not, I will check internally how to arrange the delivery." | plan B 명시 - 책임 분배 |
| `If you don't have any transparent plastic covers, let us check if we can make that plastic cover by the other vendor.` | "If you don't have any transparent plastic covers, let us check if we can make that plastic cover by the otheRDIM" | "If you don't, let us check if we can" - 대안 책임 분담 |

**Audrey 교훈**: "If X, please Y" - 조건부 후속 요청. 일정이 고정되면 공유해 달라. 투명 커버가 없으면 다른 vendor로 만들어 보겠다. 이 "if not, we will" 구조는 책임을 양측이 나누는 화법이다. Liqid에게만 떠넘기지 않고 "our side에서도 검토하겠다"는 표시. coordination 회의에서 중요한 화법.

### 질문 유형 4: 의견 요청형 제안 (Opinion-Seeking Proposal)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So what do you think about preparing a remote demo scenario for FMS?` | "So what do you think about preparing a remote demo scenario for FMS?" | "what do you think about X" - 의견 요청형 제안 |
| `What's your thoughts on this?` | "What's your thoughts on this?" | "what's your thoughts" - 동의 구하기 |
| `Once we are done with any validation, how about we publish a joint white paper?` | "Once we are done with any validation, how about we publish a joint white paper?" | "how about we X" - 제안 |

**Audrey 교훈**: "what do you think about X" / "how about we X" - 제안을 의견 요청으로 포장. "우리 합시다"가 아니라 "어떻게 생각하시나요?" / "하는 게 어떨까요?"로 상대방 동의를 끌어낸다. coordination 회의에서 합의를 만드는 화법이다. 특히 "how about we publish a joint white paper" - 이게 action item 합의의 출발점.

### 질문 유형 5: 시점 명시 요청 (Timeline Pin-Down)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So there will be Q1 next year?` | "So there will be Q1 next year?" | 짧은 확인 - 일정 pin-down |
| `Oh, it's going to be Q1. Okay, the temporal target is Q1, right?` | "Oh, it's going to be Q1. Okay, the temporal target is Q1, right?" | "temporal target" - 일정 목표 명시 |
| `By August, your system in Korea will surely be deployed, and we will have a system in the US also.` | "So by August, your system in Korea will surely be deployed, and we will have a system in the US also." | "by X, Y will surely be Z" - 일정 확약 요구 |

**Audrey 교훈**: "temporal target is Q1, right?" - "temporal target"은 고급 표현. 일정을 "temporal target"으로 명시하면, 단순 확인이 아니라 공식적 일정 합의로 들린다. 그리고 "by August, system will surely be deployed" - "surely"로 확약을 요구. coordination 회의에서 일정을 pin-down하는 핵심 화법.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

### 샘플/일정 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 수량 요청 | Steve | "So how many adapters can you provide for this setup?" | "how many" 직접 질문 |
| 샘플 추가 제안 | Liqid | "In addition to ordering, we will also try to provide some additional samples for the show. So we will be able to provide you guys the 10 adapter samples for the show." | "In addition to X, we will try to Y" - 추가 제공 |
| 배송지 결정 | Liqid | "I think maybe the best option and we'll confirm the logistics is we can ship it maybe directly to the show in Las Vegas. Or we can ship it to your facility ahead of the show" | "best option" + "or" - 복수 옵션 제시 |
| 일정 창 확인 | Liqid | "Normally for these shows, there's a window of time. It cannot arrive earlier than some date. It must arrive before another date. We just need those specifics and we should be able to hit that." | "window of time" + "we should be able to hit that" - 배송 창 명시 |
| 일정 재확인 | Steve | "If the schedule is fixed, please share the schedule to our site." | 조건부 후속 요청 |

### 일정/타임라인 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 일정 가속 가능성 탐색 | Steve | "If we decided to spend more earlier, then it's possible for us to get the chassis sooner. But in the current timeline, without spending the extra expedited fees with Acton, more than likely it's going to be Q1." | 비용 탓 일정 미루기 |
| GA 일정 발표 | Liqid | "The goal is, GA is going to be next year in 27. It's going to be the second half of 27." | "GA is going to be X" - GA 일정 |
| 일정 가정 확인 | Steve | "Oh, it's going to be Q1. Okay, the temporal target is Q1, right?" | "temporal target" - 일정 합의 |
| 일정 안전 가정 | Liqid | "I think that's the safer assumption." | "safer assumption" - 보수적 일정 |
| CXL Gen3 일정 | Liqid | "CXL 3.X, we will not have out. I mean, the first point of testing will be the actual RDKs that Marvell provides. So you guys can get those RDKs for Marvell. We will get those RDKs for Marvell." | "first point of testing" - 단계적 일정 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| Action item 합의 | Steve | "So if you agree, let's make it an action item for today." | "make it an action item" - 공식 합의 |
| 세부 조율 | Steve | "And going to iron out the details in the next few meetings." | "iron out the details" - 세부 조율 |
| 다음 회의 발표 요청 | Steve | "Next time, the next meeting, please prepare the presentation. I will invite more related person." | "please prepare X" - 다음 회의 준비 요청 |
| biweekly 유지 | Liqid | "I'm glad we are getting the bi-weekly meeting set up. I think this will allow us to make good progress towards HPE Discover." | biweekly 운영 합의 |
| 후속 채널 | Liqid | "Please just keep us posted so we can prepare the material." | "keep us posted" - 후속 의사소통 |
| 공동 white paper | Steve | "Once we are done with any validation, how about we publish a joint white paper? It would be a great way to show the memory pooling market what we have achieved." | "joint white paper" - 공동 산출물 합의 |
| 합의 동의 | Liqid | "That would be great, Steve. The best thing we can do right now is publish data for the industry. So we would welcome the chance to work with you guys on collecting the data and making a white paper." | "we would welcome the chance" - 환영 표현 |

**Audrey 교훈**:
- "let's make it an action item for today" - 이 표현이 coordination 회의의 핵심. 합의된 사항을 공식 action item으로 명시.
- "iron out the details" - "다듬다" - 세부 사항을 다음 회의에서 조율하겠다는 정중한 표현.
- "we would welcome the chance to work with you" - 동의의 고급 표현. "Yes" 대신 "we would welcome"으로 적극적 동의 표시.
- "keep us posted" - "진행 상황을 알려달라" - 후속 의사소통 요청의 표준 표현.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/Liqid/HPE Discover 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **E3.S** | 서버용 EDSFF 폼팩터 | "the SK Hynix 6CXL product only supports E3.S form factor" - 폼팩터 제약 명시 |
| **adapter** | 폼팩터 변환 보드 | "I've asked Trit to prepare an adapter for E3.S" - adapter 준비 요청 |
| **chassis** | 시스템 프레임/케이스 | "could you please provide your chassis dimensions?" - chassis 치수 요청 |
| **HPE Discover** | HPE 연례 행사 (6월 Vegas) | "It is the week of June 15th is when HPE Discover is" - 행사 일정 명시 |
| **FMS** | Flash Memory Summit (8월) | "for FMS in August, we can demonstrate the liquid pooling system" - FMS 공동 demo 합의 |
| **RDK** (Reference Design Kit) | Marvell 참조 설계 키트 | "the first point of testing will be the actual RDKs that Marvell provides" - RDK로 단계적 검증 |
| **Atlas II** | Liqid의 CXL Gen 3 시스템 | "Our full Atlas II systems for testing at the end of this year, at the earliest" - Atlas II 일정 |
| **GA** (General Availability) | 제품 일반 출시 | "The goal is, GA is going to be next year in 27. It's going to be the second half of 27" - GA 일정 |
| **expedited development** | 가속 개발 (추가 비용) | "It's a function of how quickly we pay for expedited development" - 비용 탓 일정 |
| **CXL 2.X Gen 5** | CXL 2.0 / PCIe Gen 5 | "on current CXL 2.X Gen 5, we should start immediately" - 현재 세대 GA |
| **CXL 3.X / Gen 6** | CXL 3.0 / PCIe Gen 6 | "CXL 3.X, we will not have out" - 차세대 미출시 |
| **G2 / G2.5 / G3.5** | CXL 연결 계층 (Dynamo 기준) | "where do we connect CXL? Do we connect it at the G2.5 layer or do we connect it at the G3.5 layer?" - 연결 계층 논쟁 |
| **Dynamo** | NVIDIA의 LLM 추론 엔진 | "as far as Dynamo is concerned, there is no measurable impact" - Dynamo 관점 |
| **KV cache hit rate** | KV 캐시 적중률 | "the hit rate is a direct correlation to tokens per second" - hit rate↔tokens/sec 비례 |
| **tokens per second** | 초당 토큰 생성 수 | "we go from about 350 tokens per second to over 2,000 tokens per second" - 성능 수치 |
| **token per watt / per dollar** | 와트당/달러당 토큰 | "Only three things count for AI. Token per second, token per watt and token per dollar" - 성능 지표 3종 |
| **NVL 72** | NVIDIA NVL72 랙 시스템 | "NVL 72 is a four and a half million dollar rack of infrastructure" - 랙 가격 |
| **memory pooling** | 메모리 풀링 (CXL 핵심 기능) | "show the memory pooling market what we have achieved" - 풀링 시장 |
| **memory sharing** | 메모리 공유 (다중 GPU 접근) | "what memory sharing at G2 looks like. Nobody has done that before" - 미개척 영역 |
| **white paper** | 공동 기술 백서 | "how about we publish a joint white paper?" - 공동 산출물 |
| **BIOS** | Basic I/O System | "we also have now a BIOS from the Dell team" - BIOS 확보 |
| **Super Micro / Dell / Cisco / HPE** | 서버 벤더 | "We have Super Micro. Now we have a Dell BIOS in-house. Cisco is working on a BIOS for us" - 다중 벤더 |
| **remote demo** | 원격 데모 | "what do you think about preparing a remote demo scenario for FMS?" - 원격 demo 합의 |
| **joint showcase** | 공동 전시 | "preparing the joint showcase for the year's major industry events" - 공동 전시 |
| **biweekly** | 격주 회의 | "I'm glad we are getting the bi-weekly meeting set up" - 운영 회의 체계 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 57개. IDs use prefix m13.

```yaml
# ── Agenda 운영 (Agenda Management) ──
- id: m13-001
  expression: "since we haven't met before, so I guess straight to the point to save your time"
  category: opening_framing
  function: efficiency_focused_opening
  speaker_role: coordinator
  difficulty: 4
  context: "Actually, since we haven't met before, so I guess straight to the point to save your time"
  note: 새 참가자 배려 + 효율성 표시 - coordination 회의 opening 화법

- id: m13-002
  expression: "So today, Agenda are N items. First, we will discuss..."
  category: agenda_opening
  function: structured_agenda
  speaker_role: coordinator
  difficulty: 3
  context: "So today, Agenda are four items. First, we will discuss the preparation for the HPD showcase. And second, we'll check the current status..."
  note: 동사 부여 패턴 - discuss/check/share

- id: m13-003
  expression: "Let's move on to the first item."
  category: transition
  function: item_shift
  speaker_role: coordinator
  difficulty: 2
  context: "Let's move on to the first item."

- id: m13-004
  expression: "Let's move on to next."
  category: transition
  function: item_shift
  speaker_role: coordinator
  difficulty: 2
  context: "Let's move on to next."

- id: m13-005
  expression: "Okay, and next, shift to the X agenda."
  category: transition
  function: explicit_topic_shift
  speaker_role: coordinator
  difficulty: 3
  context: "Okay, and next, shift to the showcase agenda."

- id: m13-006
  expression: "The next item is X."
  category: transition
  function: agenda_resume
  speaker_role: coordinator
  difficulty: 2
  context: "the next item is the joint promotion"

# ── 항목별 요청 (Item-Level Ask) ──
- id: m13-007
  expression: "As you know, X only supports Y. So I've asked Z to prepare..."
  category: context_setting
  function: shared_context_assumption
  speaker_role: coordinator
  difficulty: 4
  context: "As you know, the SK Hynix 6CXL product only supports E3.S form factor. So I've asked Trit to prepare an adapter for E3.S"
  note: "As you know"로 공유 context 가정

- id: m13-008
  expression: "So how many X can you provide for this setup? Can you answer this?"
  category: quantity_ask
  function: direct_quantity_request
  speaker_role: coordinator
  difficulty: 3
  context: "So how many adapters can you provide for this setup? Can you answer this?"
  note: coordination 회의에서 수량 직접 질문 - "Can you answer this?"로 답 요구

- id: m13-009
  expression: "So would it be possible for X to Y?"
  category: possibility_probe
  function: polite_possibility_check
  speaker_role: coordinator
  difficulty: 4
  context: "So would it be possible for a Liqid to delivery the directory to our event booth?"
  note: 정중한 가능성 탐색

- id: m13-010
  expression: "If not, I will check internally how to arrange X."
  category: plan_b
  function: alternative_responsibility
  speaker_role: coordinator
  difficulty: 4
  context: "If not, I will check internally how to arrange the delivery."
  note: plan B 명시 - 책임 분배

- id: m13-011
  expression: "I'd like to check X"
  category: request_soft
  function: polite_check
  speaker_role: coordinator
  difficulty: 2
  context: "And I also, I'd like to check the chassis cover material"

- id: m13-012
  expression: "Based on the portal on the screen, could you lend the same one showing the picture?"
  category: visual_reference
  function: visual_request
  speaker_role: coordinator
  difficulty: 3
  context: "Based on the portal on the screen, could you lend the same one showing the picture?"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m13-013
  expression: "let us discuss internally"
  category: internal_deferral
  function: polite_delay
  speaker_role: partner
  difficulty: 4
  context: "Yeah, let us discuss internally. It's easier to run the demo from the liquid lab if we have to ship everything to the Hynex facility in San Jose."
  note: "검토해 보겠습니다"의 영어 버전. 뒤에 이유 필수

- id: m13-014
  expression: "It's not just X, there's Y and everything else."
  category: complexity_emphasis
  function: scope_expansion
  speaker_role: partner
  difficulty: 4
  context: "It's not just the liquid chassis, there's servers and networking and everything else."
  note: 단일 요청의 복잡성 강조 - 거절 회피

- id: m13-015
  expression: "But understood on the ask, we will go check internally."
  category: ask_acknowledgment
  function: request_acknowledge_then_defer
  speaker_role: partner
  difficulty: 5
  context: "But understood on the ask, we will go check internally."
  note: 요청 인정 + 결정 미루기 - 핵심 회피 패턴

- id: m13-016
  expression: "Would it be possible for you guys to X? Is that an option?"
  category: alternative_redirect
  function: alternative_proposal
  speaker_role: partner
  difficulty: 5
  context: "So would it be possible for you guys to come to our Colorado facility and set up the demo there, and then we can provide you guys remote access? Is that an option?"
  note: 대안 제시 + 선택권 이양

- id: m13-017
  expression: "at the earliest X, but more than likely Y"
  category: conservative_schedule
  function: expectation_management
  speaker_role: partner
  difficulty: 4
  context: "Our full Atlas II systems for testing at the end of this year, at the earliest, but more than likely it's going to be Q1 of next year"
  note: 일정 보수 발표 패턴

- id: m13-018
  expression: "I think that's the safer assumption."
  category: assumption_hedge
  function: conservative_confirmation
  speaker_role: partner
  difficulty: 4
  context: "I think that's the safer assumption."
  note: 일정 가정 보수화 - "safer assumption"

- id: m13-019
  expression: "It's a function of how much we want to invest in expediting X"
  category: cost_deferral
  function: investment_framing
  speaker_role: partner
  difficulty: 5
  context: "It's a function of how quickly we pay for expedited development... It's just a function of how much do we want to invest in expediting the development."
  note: 일정 가속을 비용 투자 문제로 프레이밍

- id: m13-020
  expression: "If we decided to spend more earlier, then it's possible for us to get X sooner."
  category: conditional_acceleration
  function: cost_timeline_link
  speaker_role: partner
  difficulty: 4
  context: "If we decided to spend more earlier, then it's possible for us to get the chassis sooner."

- id: m13-021
  expression: "We want to help you guys. We want to enable X."
  category: cooperation_emphasis
  function: willingness_stating
  speaker_role: partner
  difficulty: 3
  context: "We want to help you guys. We want to enable the testing. We can go ask for discounts and all of that kind of stuff."
  note: 거절을 "최대한 노력"으로 포장

- id: m13-022
  expression: "We can go ask for discounts and all of that kind of stuff."
  category: discount_offer
  function: concession_signal
  speaker_role: partner
  difficulty: 3
  context: "We can go ask for discounts and all of that kind of stuff."

- id: m13-023
  expression: "We will go check internally."
  category: internal_check
  function: deferral_short
  speaker_role: partner
  difficulty: 3
  context: "But understood on the ask, we will go check internally."

# ── 정중한 도전 (Polite Challenge) ──
- id: m13-024
  expression: "Is there any possibility that X can Y?"
  category: possibility_probe
  function: polite_request_exploration
  speaker_role: questioner
  difficulty: 4
  context: "Is there any possibility that liquid box can be landed to the solet, which is located in San Jose?"
  note: "주세요" 대신 "가능성 있나요?" - 정중한 추가 자원 요청

- id: m13-025
  expression: "Is there other R&D that could be done on X in Y?"
  category: broader_use_probe
  function: expanded_use_question
  speaker_role: questioner
  difficulty: 4
  context: "Is there other R&D that could be done on the liquid chassis in San Jose?"

- id: m13-026
  expression: "Maybe if there's broader use for X beyond Y, maybe it would make sense for Z?"
  category: investment_justification
  function: purchase_rationale
  speaker_role: questioner
  difficulty: 5
  context: "Maybe if there's broader use for the chassis in San Jose beyond FMS, maybe it would make sense for a purchase of gear for San Jose?"
  note: "would make sense" - 투자 정당화 화법

- id: m13-027
  expression: "If the schedule is fixed, please share the schedule to our site."
  category: conditional_followup
  function: conditional_request
  speaker_role: questioner
  difficulty: 3
  context: "If the schedule is fixed, please share the schedule to our site."

- id: m13-028
  expression: "If you don't have X, let us check if we can Y by Z."
  category: alternative_responsibility_share
  function: plan_b_share
  speaker_role: questioner
  difficulty: 4
  context: "If you don't have any transparent plastic covers, let us check if we can make that plastic cover by the other vendor."
  note: 책임 분담 화법

- id: m13-029
  expression: "So what do you think about preparing X for Y?"
  category: opinion_seeking_proposal
  function: proposal_as_opinion
  speaker_role: questioner
  difficulty: 3
  context: "So what do you think about preparing a remote demo scenario for FMS?"

- id: m13-030
  expression: "What's your thoughts on this?"
  category: agreement_check
  function: consent_seek
  speaker_role: questioner
  difficulty: 2
  context: "What's your thoughts on this?"

- id: m13-031
  expression: "how about we publish a joint X?"
  category: proposal
  function: joint_output_proposal
  speaker_role: questioner
  difficulty: 3
  context: "Once we are done with any validation, how about we publish a joint white paper?"

- id: m13-032
  expression: "the temporal target is Q1, right?"
  category: timeline_pin
  function: schedule_confirmation
  speaker_role: questioner
  difficulty: 4
  context: "Oh, it's going to be Q1. Okay, the temporal target is Q1, right?"
  note: "temporal target" - 일정 목표 명시

- id: m13-033
  expression: "By X, Y will surely be Z"
  category: timeline_assertion
  function: deployment_confirmation
  speaker_role: questioner
  difficulty: 4
  context: "So by August, your system in Korea will surely be deployed, and we will have a system in the US also."

- id: m13-034
  expression: "We know that X will be shipped in the Y time frame. So, we want to recheck..."
  category: schedule_recheck
  function: assumption_verify
  speaker_role: questioner
  difficulty: 3
  context: "We know that the Liqid solution will be shipped in the May time frame. So, you want to check that if there are any kinds of issues or you want to recheck the schedule?"

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m13-035
  expression: "So if you agree, let's make it an action item for today."
  category: action_item_capture
  function: formal_agreement
  speaker_role: coordinator
  difficulty: 4
  context: "So if you agree, let's make it an action item for today."
  note: coordination 회의 핵심 - action item 합의

- id: m13-036
  expression: "And going to iron out the details in the next few meetings."
  category: detail_refinement
  function: future_detail_work
  speaker_role: coordinator
  difficulty: 4
  context: "And going to iron out the details in the next few meetings."
  note: "iron out the details" - 세부 사항 조율

- id: m13-037
  expression: "We would welcome the chance to work with you guys on X"
  category: agreement_welcome
  function: enthusiastic_consent
  speaker_role: partner
  difficulty: 4
  context: "So we would welcome the chance to work with you guys on collecting the data and making a white paper."
  note: "Yes" 대신 "we would welcome" - 적극적 동의

- id: m13-038
  expression: "The best thing we can do right now is X"
  category: priority_stating
  function: action_priority
  speaker_role: partner
  difficulty: 4
  context: "The best thing we can do right now is publish data for the industry."

- id: m13-039
  expression: "Please just keep us posted so we can prepare the material."
  category: followup_request
  function: status_update_request
  speaker_role: partner
  difficulty: 3
  context: "Please just keep us posted so we can prepare the material. We can order the servers so that we can move quickly for you guys."
  note: "keep us posted" - 후속 의사소통

- id: m13-040
  expression: "I'm glad we are getting the bi-weekly meeting set up. I think this will allow us to make good progress towards X."
  category: cadence_affirm
  function: meeting_cadence_agreement
  speaker_role: partner
  difficulty: 4
  context: "I'm glad we are getting the bi-weekly meeting set up. I think this will allow us to make good progress towards HPE Discover."
  note: biweekly 운영 합의

- id: m13-041
  expression: "Next time, the next meeting, please prepare X. I will invite more related person."
  category: next_meeting_request
  function: preparation_assignment
  speaker_role: coordinator
  difficulty: 3
  context: "Next time, the next meeting, please prepare the presentation. I will invite more related person."

- id: m13-042
  expression: "let's wrap up a bit early today and meet again in two weeks"
  category: meeting_close
  function: cadence_confirm
  speaker_role: coordinator
  difficulty: 3
  context: "Yes, let's wrap up a bit early today and meet again in two weeks."

- id: m13-043
  expression: "Excuse me. Before we start, just to let everyone know, in half an hour, I have a conflict for another meeting."
  category: time_constraint_notice
  function: early_exit_notice
  speaker_role: participant
  difficulty: 4
  context: "Excuse me. Before we start, just to let everyone know, in half an hour, I have a conflict for another meeting. If the meeting goes past 30 minutes, I will have to step aside. I apologize in advance."
  note: 회의 시작 시 이탈 예고 - 정중한 시간 제한 통지

- id: m13-044
  expression: "If the meeting goes past 30 minutes, I will have to step aside. I apologize in advance."
  category: early_exit
  function: graceful_exit_notice
  speaker_role: participant
  difficulty: 4
  context: "If the meeting goes past 30 minutes, I will have to step aside. I apologize in advance."

# ── 일정/샘플 언어 (Schedule & Sample) ──
- id: m13-045
  expression: "We are expecting our sample for X at the end of this month."
  category: sample_schedule
  function: sample_timeline
  speaker_role: partner
  difficulty: 3
  context: "We are expecting our sample for the first adapter at the end of this month."

- id: m13-046
  expression: "If the desire is to fill the complete box for the show, we will work towards that pull."
  category: show_target
  function: show_preparation
  speaker_role: partner
  difficulty: 3
  context: "If the desire is to fill the complete box for the show, we will work towards that pull."

- id: m13-047
  expression: "In addition to ordering, we will also try to provide some additional samples for the show."
  category: sample_additional
  function: extra_sample_offer
  speaker_role: partner
  difficulty: 3
  context: "In addition to ordering, we will also try to provide some additional samples for the show."

- id: m13-048
  expression: "Normally for these shows, there's a window of time. It cannot arrive earlier than some date. It must arrive before another date."
  category: shipping_window
  function: delivery_window_spec
  speaker_role: partner
  difficulty: 4
  context: "Normally for these shows, there's a window of time. It cannot arrive earlier than some date. It must arrive before another date. We just need those specifics and we should be able to hit that."
  note: 행사 배송 창 명시

- id: m13-049
  expression: "We just need those specifics and we should be able to hit that."
  category: delivery_commitment
  function: window_commitment
  speaker_role: partner
  difficulty: 3
  context: "We just need those specifics and we should be able to hit that."

- id: m13-050
  expression: "I will let you know."
  category: info_promise
  function: short_commitment
  speaker_role: coordinator
  difficulty: 1
  context: "Okay. I will let you know."

# ── KV Cache 기술 발표 (Technical Update) ──
- id: m13-051
  expression: "from the Dynamo layer, when you're looking at CXL from the G2 layer in Dynamo, Dynamo cannot tell whether it is speaking to system DRAM or whether it is speaking to CXL memory."
  category: technical_finding
  function: layer_transparency
  speaker_role: partner
  difficulty: 5
  context: "Even though the latency is twice as high or three times as high compared to onboard DRAM, even in that five, six hundred nanosecond latency range, as far as Dynamo is concerned, there is no measurable impact"
  note: KV cache 발표 - CXL 메모리 투명성

- id: m13-052
  expression: "The hit rate is a direct correlation to X"
  category: technical_correlation
  function: metric_linkage
  speaker_role: partner
  difficulty: 4
  context: "The hit rate is a direct correlation to tokens per second."

- id: m13-053
  expression: "Only three things count for AI. Token per second, token per watt and token per dollar."
  category: principle_stating
  function: guiding_principle
  speaker_role: partner
  difficulty: 4
  context: "Remember, only three things matter. Only three things count for AI. Token per second, token per watt and token per dollar. That is the only thing that counts."
  note: Liqid의 AI 성능 원칙 - 핵심 발언

- id: m13-054
  expression: "Our position is X is not any slower. It's the same level of performance."
  category: position_stating
  function: position_assert
  speaker_role: partner
  difficulty: 4
  context: "Our position is it's not any slower. It's the same level of performance."

- id: m13-055
  expression: "We should no longer call it X. We should just call it Y. There's no performance difference."
  category: renaming_proposal
  function: terminology_repositioning
  speaker_role: partner
  difficulty: 5
  context: "Our opinion is we should no longer call it G2.5. We should just call it G2. There's no performance difference. We're doing ourselves a disservice by calling it G2.5."
  note: 용어 재정의 제안 - G2.5 → G2

- id: m13-056
  expression: "We're doing ourselves a disservice by calling it X."
  category: self_harm_framing
  function: terminology_criticism
  speaker_role: partner
  difficulty: 5
  context: "We're doing ourselves a disservice by calling it G2.5. We should just call it G2 and let somebody else argue that it's not G2, that it's slower somehow."

- id: m13-057
  expression: "let somebody else argue that X"
  category: argument_shift
  function: burden_of_proof_shift
  speaker_role: partner
  difficulty: 5
  context: "let somebody else argue that it's not G2, that it's slower somehow. Let them prove it"
  note: "입증 책임을 상대에게" - 고급 협상 화법
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-04-29 08 52 22_EN_Liqid_biweekly-extracted.wav` (총 ~40분, 4,522단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | line range | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입부 (line 82-97) | line 82-97 | Steve agenda 4개 개조식 나열 + "straight to the point" | agenda 운영 화법 | ★★☆ |
| 2 | HPE Discover 샘플 요청 (line 96-127) | line 96-127 | "how many adapters can you provide" + transparent cover 협상 | 수량 요청 + 조건부 plan B | ★★★ |
| 3 | 일정 협상 (line 215-239) | line 215-239 | Atlas II Q1 next year + "safer assumption" + 비용 탓 미루기 | 일정 협상 + 회피 화법 | ★★★★ |
| 4 | San Jose 자원 요청 (line 255-291) | line 255-291 | "Is there any possibility" + "let us discuss internally" + 대안 제시 | 정중 도전 + 회피 | ★★★★ |
| 5 | KV cache 발표 + G2.5 재정의 (line 336-386) | line 336-386 | "Only three things count for AI" + "we should no longer call it G2.5" | 기술 발표 + 원칙 선언 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 4가 가장 가치 높음 - 일정 협상·자원 회피 화법이 밀집
- 발췌 5는 KV cache 기술 발표 - Type C 회의의 기술 업데이트 segment

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **coordination + gentle push** register다. 격주 biweekly 운영회의로, agenda 4개를 순회하며 각 item마다 요청-응답-합의를 반복. 두 역할 모두 학습해야:
- **Coordinator 역할 (Steve)**: agenda 운영, 수량/일정 직접 요청, action item 합의 - 네가 파트너와 일정 조율할 때
- **Partner 역할 (Liqid)**: 일정/자원 한계 회피, 대안 제시, "let us discuss internally" - 네가 일정이 안 맞을 때 정중하게 미룰 때

### Pragmatics (화용론) 핵심
1. **"let us discuss internally"**: "검토해 보겠습니다"의 영어 버전이지만, 단독 사용 금지. 뒤에 반드시 **이유**를 붙인다 - "It's not just X, there's Y"로 왜 어려운지 설명. 그리고 "understood on the ask"로 요청을 인정. 이 3단 구조(let us + 이유 + understood)가 회피의 정석.
2. **"would it be possible for you to X? Is that an option?"**: 거절이 아니라 **대안 제안**으로 방향을 바꾸는 화법. "Is that an option?"이 핵심 - 선택권을 상대에게 넘긴다.
3. **"safer assumption"**: 일정을 보수적으로 발표하는 화법. "at the earliest X, more than likely Y"로 기대치를 낮추고, "that's the safer assumption"으로 합의. 일정 약속할 때 무조건 이 패턴 써라.
4. **"let's make it an action item for today"**: coordination 회의의 핵심 합의 공식. 합의된 사항을 공식 action item으로 명시. 회의록에 책임이 남는다.
5. **"Only three things count for AI"**: 원칙 선언 화법. KV cache 발표에서 Liqid가 성능 원칙을 선언. 기술 발표의 마무리로 원칙을 명시하면 설득력이 크다.

### 네가 당장 써야 할 Top 5
1. **"let us discuss internally. It's not just X, there's Y"** - 정중한 회피 + 이유
2. **"would it be possible for you to X? Is that an option?"** - 대안 제시
3. **"at the earliest X, more than likely Y. That's the safer assumption."** - 보수적 일정
4. **"let's make it an action item for today"** - action item 합의
5. **"If the schedule is fixed, please share the schedule to our site."** - 조건부 후속

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "검토해 보겠습니다" | "let us discuss internally. It's not just X, there's Y" | 한국어는 이유 생략, 영어는 이유 필수 |
| "그럼 어떠세요?" | "Would it be possible for you to X? Is that an option?" | "Is that an option?"로 선택권 이양 |
| "아마 Q1쯤" | "at the earliest X, more than likely Y. That's the safer assumption." | "safer assumption"으로 보수화 명시 |
| "action item으로 합시다" | "let's make it an action item for today" | "for today"로 회의 단위 명시 |
| "일정 잡히면 공유 주세요" | "If the schedule is fixed, please share the schedule to our site" | "If X, please Y"로 조건부 |
| "다음 회의에서 다듬죠" | "going to iron out the details in the next few meetings" | "iron out the details" - 고급 표현 |
| "괜찮습니다" | "we would welcome the chance to work with you" | "Yes" 대신 "welcome"으로 적극 동의 |
| "시간 부족시 먼저 가겠습니다" | "If the meeting goes past 30 minutes, I will have to step aside. I apologize in advance." | "step aside" + "apologize in advance" - 정중 이탈 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 57개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 긑요일 교정**: 이 교재의 2절 회피 화법·3절 정중 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **Type C 특화**: 1절 agenda 운영·4절 action item 합의 화법을 coordination 회의에서 직접 적용

---

*Textbook 13 - Liqid Biweekly (2026-04-29). 회의 유형 C (sample/schedule coordination). 표현 DB 57개. 5개 발췌 구간. 작성: 2026-09-01.*
