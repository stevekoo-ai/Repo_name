---
textbook_id: 12
meeting: Liqid biweekly (system setup, HPE Discover 2026 CXL chassis, go-to-market)
date: 2026-05-13
type: C (샘플/일정 조율)
partner: Liqid (Triet, Vincent, Daniel Nguyen, Joe, Smith, Thomas)
sk_side: Steve, Jongmin (SK Hynix)
duration_words: 4708
audio: repo/webex-audio/2026-05-13 08 57 57_EN_Liqid_biweekly-extracted.wav
transcript: repo/webex-audio/2026-05-13 08 57 57_EN_Liqid_biweekly-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, liqid, cxl, hpe-discover, sample-coordination, schedule, go-to-market, biweekly]
---

# Textbook 12 - Liqid Biweekly (2026-05-13)

> **회의 유형**: C (샘플/일정 조율) - 하드웨어 출하 일정, 설치 준비 요건, HPE Discover 데모 기기·홍보물, 방문 일정 조율이 핵심
> **학습 가치**: 샘플 수량·출하 일정 협의, 사전 설치 요건 요청, 데모 기기 delivery status 확인, action item 명시, 정중한 go-to-market 탐색
> **Audrey 관점**: Type C 회의는 "언제 어떤 물건이 어디에 도착하는가"를 정확히 협의하는 자리. 네가 파트너 하드웨어를 받아 테스트할 때 이 회의의 화법을 그대로 써라. 특히 "we expect to have everything land in Korea by..." 식의 일정 표현, "could you share some information before the meeting" 식의 사전 요청, "I'll take it that as an action item" 식의 책임 명시가 핵심.

---

## 1. 발화 아키텍처 - Triet의 진행 설계 (5단계)

Triet(Liqid)은 biweekly 상태 점검 회의를 5단계로 진행한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "진행의 뼈대"다.

### 단계 1: 소속 확인·아이스브레이킹 (Roll Call + Small Talk)

본론 전에 참석자를 확인하고 가벼운 안부로 분위기를 연다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think we have everyone on. X, Y, Z, where are you to get started?` | "And I think we have everyone on. Vincent, Smith, Thomas, where are you to get started?" | 참석자 호명 - "where are you"로 부재자 확인 |
| `Thank you for joining the meeting. Especially since it's already late in the workday on the US side.` | "Thank you for joining the meeting. Especially since it's already late in the workday on the US side." | 상대 시간차 인정 - "late in the workday"로 배려 표시 |
| `How was your trip to X?` | "How was your trip to Japan?" | 가벼운 안부 - 출장 직후 아이스브레이킹 |

**Audrey 교훈**: 영어 회의는 "본론부터"가 아니다. "Thank you for joining, especially since it's late on your side" - 상대의 시간 차이를 인정하는 한마디가 참석자의 기분을 바꾼다. 한국어 "수고하십니다"의 역할을 이게 한다. 네가 미국 측과 회의할 때, "I know it's late on your side, thank you for joining"을 반드시 첫마디에 붙여.

### 단계 2: 의제 설정 (Agenda Stating)

참석자 확인 후, "we have two main agenda items"로 의제를 명시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Sure, we have two main agenda items. First, we'd like to discuss X. And second, for Y, we'd like to check Z.` | "Sure, we have two main agenda items. First, we'd like to discuss the preparation for system setup. And second, for HPE Discover 2026, we'd like to check delivery status for the CXL chassis." | 의제 명시 - "First... And second..." 구조 |
| `So, you had mentioned via email that there has not been much progress yet. But let's start with...` | "So, you had mentioned via email that there has not been much progress yet. But let's start with the brief update on the current shipping status." | 이메일 사전 언급 회상 - "you had mentioned"으로 정확성 확보 |
| `And then we can go through the question for our side.` | "And then we can go through the question for our side." | 질문 순서 안내 |

**Audrey 교훈**: "you had mentioned via email that..." - 이 회의에서 Steve가 쓴 화법이다. 이메일로 이미 공유된 사실을 회의에서 다시 끄집어내 정확성을 확보한다. "너 이메일에서 진척 없다고 했지"를 "you had mentioned via email that there has not been much progress"로 정중하게 표현. 한국어 "이메일에서 말씀하신 거"를 영어로는 "you had mentioned via email"로.

### 단계 3: 상태 업데이트 (Status Update)

의제별로 "So for the X, I think..."로 시작, 일정을 구체적으로 보고한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So for the X, I think the Y items have already shipped` | "So for the preparation for system setup, I think the liquid items have already shipped, our chassis has already shipped. So it's already in Korea." | 상태 보고 - "already shipped"로 완료 표시 |
| `we are expected to ship those to X by the end of this week` | "we are waiting on the super micro servers and we are expected to ship those to Korea by the end of this week. That is the target." | 일정 표시 - "expected to ship by..." + "That is the target" |
| `we expect to have everything land in X by the end of next week` | "we expect to have everything land in Korea by the end of next week." | 도착 예정 - "land in X by..." |
| `if everything goes as expected and we don't have any customs issues, then we will have all the items in X by Y` | "if everything goes as expected and we don't have any customs issues, then we will have all the items for the first order in SK Hynix by the end of next week." | 조건부 확정 - "if... then we will have..." |

**Audrey 교훈**: Type C 회의에서 일정은 단정적으로 말하지 않는다. "we are **expected** to ship", "if everything goes as expected", "that is the **target**" - 이 "expected/target" hedge가 중요. 100% 확정이 아님을 명시하면서도 구체적 일정을 준다. 한국어 "이번 주 말쯤 들어올 예정입니다"를 영어로는 "we are expected to ship by the end of this week. That is the target."로.

### 단계 4: 질문 유도·세부 조율 (Question Invitation + Detail Coordination)

각 의제 후 "do you have any specific question"로 상대 질문을 유도하고, 세부 요건을 즉석에서 조율한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Oh, X, do you have any specific question from one through five items? Please feel free to ask.` | "Oh, Jongmin, do you have any specific question from one through five items? Do you have any questions? Please feel free to ask." | 특정 참석자 질문 유도 - "Please feel free to ask" |
| `I'm writing that down right now. We will have the X by the end of the day tomorrow.` | "I'm writing that down right now. We will have the pre-installation requirements, input power, cables required, network environment, IP, and the DIMMs required as well. I will have that by the end of the day tomorrow." | 즉석 action item - "writing that down right now" + 기한 명시 |
| `Let me see. I can check my schedule. Give me one second here.` | "Let me see. I can check my schedule. Give me one second here." | 즉석 스케줄 확인 - "Give me one second" |

### 단계 5: 마무리·action item 정리 (Wrap-up + Action Item Summary)

회의 끝에 action item을 나열하며 책임을 명시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I have several items I need to send right on item number one, number four, number five for the system setup.` | "I have several items I need to send right on item number one, number four, number five for the system setup." | action item 나열 - "items I need to send" |
| `I'll take it that as an actual item and we can discuss it internally.` | "Let me discuss that. I'll take it that as an actual item and we can discuss it internally." | action item 승격 - "take it as an actual item" |
| `We will follow up the action items and see you next meeting.` | "We will follow up the action items and see you next meeting." | 마무리 공식 |

**Audrey 교훈**: 회의 마무리에 action item을 다시 나열하는 것은 Type C 회의의 필수. "I have several items I need to send right on item number one, number four, number five" - 번호까지 명시하며 책임을 정확히 분배. 네가 회의를 마칠 때, "I have X items I need to send"로 action item을 다시 한 번 읽어줘라. 이게 회의록의 역할을 한다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 일정·제약·불확실성을 어떻게 정중하게 포장하는지.

### 전략 1: 의존성 전환 - "우리는 준비됐는데, 상대(Super Micro)가 늦다" (Dependency Pivot)

자기 쪽은 준비됐다는 점을 강조하고, 지연의 원인을 제3자(Super Micro)로 돌린다.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| 서버 지연 | "The most important thing right now, Steve, is we need to make sure the Super Micro server is shipped. Once they ship, then everything we can start to arrange schedule, flight plans, hotel and everything, **but we can't do it without the Super Micro server.** So the good news is that the liquid chassis, the switch, all the other items shipped already, it's in Korea. We're just waiting on Super Micro. Obviously, you know, with the DRAM shortages and the allocation issues, every server vendor right now has been very, very slow on delivery time. So we really appreciate your patience." | "지금 가장 중요한 건 Super Micro 서버가 ship되는 겁니다. 그게 ship되야 일정·항공·호텔 다 잡을 수 있는데, **Super Micro 없이는 불가능합니다.** 좋은 소식은 Liqid chassis·switch 등은 이미 한국에 있다는 거. Super Micro만 기다리는 중. 아시다시피 DRAM 부족·allocation 문제로 모든 서버 벤더가 지연 중입니다. 인내해 주셔서 감사합니다." |

**패턴 공식**: `The most important thing right now is we need to make sure X is shipped. We can't do it without X. The good news is Y shipped already. We're just waiting on X. With the Z shortages, every vendor has been slow. We really appreciate your patience.`

**Audrey 교훈**: 지연의 원인이 자기 쪽이 아닐 때, "we can't do it without X"로 X의 중요성을 강조하고, "the good news is Y shipped already"로 자기 쪽 완료를 부각한다. 그리고 "with the DRAM shortages and the allocation issues"로 업계 공통 문제로 프레이밍 - "우리 탓이 아니라 시장 상황이다". 마지막에 "we really appreciate your patience"로 부드럽게 마무리. 한국어 "시장 상황이라 어쩔 수 없습니다, 양해 부탁드립니다"의 영어 버전.

### 전략 2: 내부 논의로 미루기 (Internal Discussion Deferral)

결정권이 없거나 확답을 줄 수 없을 때, "내부에서 논의하겠다"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| GTM 전략 질문 | "That's fine guys if you could - we don't need an answer today but if you can think about that, please, you know, have some internal discussion and let us know" | "괜찮습니다, 오늘 답 안 주셔도 돼요. 생각해 보시고 내부 논의 좀 하셔서 알려주세요" |
| 데모 위치 결정 | "Let me discuss that. I'll take it that as an actual item and we can discuss it internally." | "논의해 보겠습니다. action item으로 잡고 내부에서 논의하죠" |
| 방문자 확정 | "I'm still working on that, but for sure it will be Daniel, Daniel Nguyen... I'm not exactly sure yet, but that's what we're working on." | "아직 작업 중입니다. 확정인 건 Daniel Nguyen이고, 나머지는 아직 확실치 않지만 진행 중입니다" |

**패턴 공식**: `We don't need an answer today but if you can think about that, have some internal discussion and let us know.` / `I'll take it that as an actual item and we can discuss it internally.`

**Audrey 교훈**: "We don't need an answer today" - 상대에게 즉답 압박을 주지 않는 정중함. "have some internal discussion and let us know" - 내부 논의라는 공식적 미루기. "I'll take it that as an actual item" - 미루되 "action item"으로 승격시켜 책임을 남긴다. 한국어 "내부에서 검토하고 다시 연락드리겠습니다"를 영어로는 "have some internal discussion and let us know"로.

### 전략 3: 기술적 확신의 제한 - "가능할 것 같지만, 확인 필요" (Technical Belief + Architect Caveat)

기술적으로 지원 가능하다고 말하되, 즉시 "건축가가 확인해야"라는 면책을 붙인다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 아키텍처 지원 여부 | "I believe what you're showing here can be supported, but we would need to get some of our architects into the room. And so maybe we can have a follow on meeting to show wiring diagrams and have a deeper discussion. But I believe what you're showing here can be supported in our belief is the same." | "보여주신 게 지원 가능할 것으로 믿습니다. 다만 건축가들을 room에 들여야 합니다. wiring diagram 보여주는 후속 회의를 가지면 좋겠습니다. 하지만 지원 가능하다고 믿습니다." |
| CXL-to-CXL RDMA | "Yeah, I understand. Right, right, right. I understand. So it should be doable. We have to just go do the wiring diagram and study it. But I think if it's CXL to CXL, the answer should be yes." | "네, 이해합니다. 가능해야 합니다. wiring diagram을 작성하고 study해야 합니다. 하지만 CXL-to-CXL이면 답은 yes일 겁니다." |

**패턴 공식**: `I believe X can be supported, but we would need to get our architects into the room. Maybe we can have a follow on meeting to show Y. But I believe X can be supported.`

**Audrey 교훈**: "I believe X can be supported, but..." - 긍정으로 시작하되 "but"로 면책을 붙인다. "we would need to get some of our architects into the room" - 실제 검증을 위한 조건. 그리고 "But I believe X can be supported"로 다시 긍정으로 닫는다. 이 "긍정-but-조건-긍정" 구조가 기술 회의에서 신뢰를 잃지 않으면서도 확언을 피하는 화법이다. "그렇게 될 것 같은데, 내가 건축가한테 한 번 더 확인하겠습니다"의 영어 버전.

### 전략 4: 제품 상태 한정 - "연구 프로토타입" (Product Stage Framing)

상대가 상용화를 탐색할 때, 현재 상태를 "연구 프로토타입"으로 한정하여 기대치를 관리한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| GTM 질문에 대한 답 | "yeah, you know that is a - in as behind the view is a food memory and CXL CXL hybrid memory is a are just a research prototype. So at first we want to show that the reference architecture that is a first our purpose. And is a - Yeah, we haven't decided yet the kind of other products we we build ourselves." | "음, pool memory와 CXL hybrid memory는 연구 프로토타입입니다. 우선 reference architecture를 보여주는 게 첫 목적입니다. 그리고 - 어떤 제품을 만들지는 아직 결정 안 했습니다." |

**패턴 공식**: `X is just a research prototype. So at first we want to show that the reference architecture. That is our first purpose. We haven't decided yet the kind of other products we build ourselves.`

**Audrey 교훈**: 상대가 "이걸 어떻게 market에 가져갈 거냐"고 물을 때, "just a research prototype"으로 현재 상태를 명확히 한다. "we haven't decided yet" - 결정 안 한 것을 솔직히 인정. 한국어 "아직 연구 단계라서 상용화는 논의 중입니다"를 영어로는 "it's just a research prototype. We haven't decided yet the kind of products we build."로.

### 전략 5: 소스코드 미공유 우회 - "사용은 가능하나 공유는 안 됨" (Source Code Boundary)

자기 쪽 소프트웨어를 공유할 수 없다는 제약을 솔직히 말하되, 데모 우회안을 제시한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| coherency 소프트웨어 공유 | "yeah, as a software only, as a cache coherence can be supported by our software, so we can use it. But we cannot share it with our source code. That's the problem." | "소프트웨어 only로 cache coherence는 저희 소프트웨어로 지원 가능합니다. 사용은 가능합니다. 하지만 source code는 공유할 수 없습니다. 그게 문제입니다." |
| 데모 우회 | "That's right, because you can't share the source code with your software coherency. So that means you need to run the demo within SK Hynix." | "맞습니다. source code 공유가 안 되니까, demo를 SK Hynix 내부에서 돌려야 합니다." |

**패턴 공식**: `X can be supported by our software, so we can use it. But we cannot share it with our source code. That's the problem.`

**Audrey 교훈": 자기 쪽 제약을 솔직히 말하되, "we can use it"으로 사용 가능성은 열어둔다. 그리고 상대가 "That's the problem"으로 제약을 인정하면, "that means you need to run the demo within X"로 우회안을 즉시 제시. 이 "제약 인정 - 사용 가능 - 우회안" 흐름이 협상에서 제약을 정중하게 포장하는 화법이다.

---

## 3. 정중한 도전 화법 (질문자의 기술·일정 탐색)

이 회의에서 Steve/Jongmin/Triet이 정중하게 도전하거나 탐색하는 패턴.

### 질문 유형 1: 일정 정확성 탐색 (Schedule Precision Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `But our important information is for number one, because we need to prepare before the system is shipped to our list.` | "But our important information is for number one, because we need to prepare before the system is shipped to our list." | 우선순위 명시 - "important information is for number one, because..." |
| `And could we make some meeting schedule or list next week because we need time to some kinds of reservation` | "And could we make some meeting schedule or list next week because we need time to some kinds of reservation or our meeting room or some kinds of environment?" | 일정 사전 요청 - "because we need time to..." |
| `could you share some information before the meeting through the email?` | "We can make a call on Wednesday, but could you share some information before the meeting through the email?" | 사전 자료 요청 - "before the meeting through the email" |

**Audrey 교훈**: "because we need time to..." - 단순 요청이 아니라 이유를 붙여 설득력을 높인다. "회의실 예약 때문에 시간이 필요하다"를 영어로 명시하는 것. 그리고 "before the meeting through the email" - 회의 전에 이메일로 미리 달라는 정확한 요청. 네가 파트너에게 자료를 미리 받고 싶을 때, "could you share some information before the meeting through the email?"를 써라.

### 질문 유형 2: 샘플 수량·구성 확인 (Sample Configuration Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So we're delivering 20 units of one 28 gigabyte first generation product and also 256 samples.` | "So we're delivering 20 units of one 28 gigabyte first generation product and also, yeah, second, 256 samples." | 수량 명시 - "20 units of 128GB first generation product" |
| `And then transparent cover is being prepared.` | "And then transparent cover is being prepared." | 부속 상태 - "is being prepared" |

**Audrey 교훈**: Type C 회의에서 샘플 수량은 반드시 숫자+단위+세대로 명시한다. "20 units of 128GB first generation product" - 이 정도 정확성이 있어야 다음 회의에서 "그때 말한 20대 말이죠"가 아니라 "128GB 1세대 20대"로 확인된다. 네가 파트너에게 샘플을 요청할 때, "we'd like to request X units of Y GB Z generation product"로 정확히.

### 질문 유형 3: 홍보물·PR 진행 확인 (Promo Material Status Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `as I asked by email, have you had a chance to check the promotion material or video clips or something?` | "So as I asked by email, have you had a chance to check the promotion material or video clips or something?" | 이메일 사전 요청 회상 - "as I asked by email" |
| `have you had a chance to X?` | "have you had a chance to check the promotion material or video clips or something?" | 정중한 진행 확인 - "have you had a chance to..." |

**Audrey 교훈**: "have you had a chance to X?" - 상대가 바쁜 걸 인정하면서 진행 여부를 묻는 정중한 화법. "did you do X?"가 아니라 "have you had a chance to do X?" - "기회가 됐나요?"로 바쁨을 배려. 네가 파트너에게 무언가 확인할 때, "have you had a chance to..."를 반드시 써라. 이메일 회상은 "as I asked by email"로 정확성을 더한다.

### 질문 유형 4: 방문자 구성 확인 (Visit Composition Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Could you confirm who will be joining the visit?` | "Could you confirm who will be joining the visit?" | 방문자 확인 - "Could you confirm" |
| `I'd like to coordinate a set up a session with our CXL related VPs or leaders.` | "Actually, I'd like to coordinate a set up a session with our CXL related VPs or leaders. So it would be a great opportunity to foster our partnership and ensure long term collaboration." | 세션 제안 - "I'd like to coordinate" + 이유 |
| `So I ask you who will be attending this visit.` | "So I ask you who will be attending this visit." | 직접 질문 - "I ask you who" |

**Audrey 교훈**: 방문 일정 조율에서 "Could you confirm who will be joining?"은 핵심 화법. "who is coming?"이 아니라 "who will be joining the visit" - "joining"이 더 정중. 그리고 "I'd like to coordinate a session with our VPs - it would be a great opportunity to foster our partnership" - 단순 요청이 아니라 이유(파트너십 강화)를 붙여 설득력을 높인다. "ensure long term collaboration"은 장기 협력을 명시하는 고급 표현.

### 질문 유형 5: GTM 전략 탐색 (Go-to-Market Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `how is your guys thinking about route to market if we prove that this architecture is attractive and has a lot of performance?` | "how is your guys thinking about route to market if we prove that this architecture is attractive and has a lot of performance?" | GTM 탐색 - "how is your guys thinking about route to market" |
| `Is this a solution that X will potentially bring to market or is it just a reference architecture that people can study?` | "Is this a solution that Hynix will potentially bring to market or is it just a reference architecture that people can study?" | 이분법 질문 - "Is this X or Y?" |
| `Any thoughts there?` | "Any any thoughts there?" | 짧은 의견 요청 |

**Audrey 교훈**: "how is your guys thinking about route to market" - 직접적이면서도 "your guys thinking"으로 부드럽게. "Is this a solution X will bring to market or is it just a reference architecture?" - 이분법으로 상대가 선택하게 만드는 강한 질문. "just a reference architecture"로 한쪽 옵션을 낮춰 상대가 "bring to market" 쪽으로 기울게 만드는 유도 화법. 네가 파트너의 상용화 의향을 탐색할 때 이 이분법을 써라.

### 질문 유형 6: 소프트웨어 준비 상태 확인 (Software Readiness Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `is SK Hynix memory sharing software already available and ready, or is that still in development?` | "is SK Hynix memory sharing software already available and ready, or is that still in development?" | 이분법 준비 확인 - "already available or still in development?" |
| `I just wanted to make sure that you had the coherency software available.` | "So I just wanted to make sure that you had the coherency software available." | 확인 - "I just wanted to make sure" |

**Audrey 교훈**: "is X already available and ready, or is that still in development?" - 두 가지 상태로 나눠 상대가 솔직히 답하게 만드는 화법. "I just wanted to make sure" - 확인 목적임을 명시, 압박감 낮추기. 네가 파트너의 준비 상태를 확인할 때, "is X available or still in development?"로.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

Type C 회의의 핵심 section. 샘플·일정·action item을 정하는 언어.

### 일정 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 도착 예정 | Triet | "we expect to have everything land in Korea by the end of next week" | "land in X by..." - 도착 일정 |
| 조건부 확정 | Triet | "if everything goes as expected and we don't have any customs issues, then we will have all the items in SK Hynix by the end of next week" | "if... then we will have..." - 조건부 |
| 기한 명시 | Triet | "I will have that by the end of the day tomorrow" | "by the end of the day tomorrow" - 정확한 기한 |
| 시간대 조정 | Triet | "if we can do the call at 4pm, so one hour earlier, that would be great" | "one hour earlier, that would be great" - 부드러운 시간 조정 |
| 요일 선택 | Triet | "we can do Thursday, your Thursday or Wednesday?" | "your Thursday or Wednesday?" - 상대 시간대 존중 |
| 의존성 명시 | Triet | "we can't do it without the Super Micro server" | "we can't do it without X" - 의존성 강조 |
| 인내 요청 | Triet | "we really appreciate your patience" | "appreciate your patience" - 지연 사과 |

**Audrey 교훈**:
- "by the end of the day tomorrow" - "내일 영업시간 끝나기 전"의 정확한 기한. "soon"이나 "ASAP"이 아니라 구체적 기한을 주는 것이 Type C의 핵심.
- "your Thursday or Wednesday?" - "your"를 붙여 상대 시간대 기준임을 명시. 한국 시간 기준인지 미국 시간 기준인지 명확히 하는 화법.
- "one hour earlier, that would be great" - 시간 변경을 요청할 때 "that would be great"로 정중하게. "we need to move it earlier"가 아니라 "if we can do X, that would be great".

### 샘플·수량 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 수량 명시 | Triet/Steve | "we're delivering 20 units of one 28 gigabyte first generation product and also 256 samples" | "20 units of 128GB first generation product" - 정확한 수량 |
| 포함물 나열 | Triet | "what's included here will be the CXL chassis. It will have optical cable. It will have our CXL Retimer HBA. It will also include a CXL switch" | "what's included here will be..." - 포함물 명시 |
| 사전 준비 요청 | Jongmin | "we need some detailed information about like input powers or even a cable or network environment" | "we need detailed information about..." - 사전 요건 요청 |
| 연결도 요청 | Jongmin | "please share some kind of system connection diagram to set up the five post and one enclosure and even a switch" | "please share system connection diagram" - 설치 자료 요청 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 즉석 기록 | Triet | "I'm writing that down right now" | "writing that down right now" - 즉석 action |
| 책임 명시 | Triet | "I will work with Vincent and Daniel to send that out this week" | "I will work with X and Y to..." - 책임자 명시 |
| action item 승격 | Steve | "I'll take it that as an actual item and we can discuss it internally" | "take it as an actual item" - action item으로 승격 |
| 후속 약속 | Triet | "I will send you our information, cell phone numbers and that information via email this week" | "I will send you X via email this week" - 구체적 후속 |
| 내부 논의 미루기 | Triet | "if you can think about that, please have some internal discussion and let us know" | "have some internal discussion and let us know" - 정중한 미루기 |
| 마무리 | Steve | "We will follow up the action items and see you next meeting" | "follow up the action items" - 마무리 공식 |

**Audrey 교훈**:
- "I'm writing that down right now" - 상대가 요청하는 즉시 "지금 적고 있다"고 말해 신뢰를 준다. "I'll note that"보다 훨씬 즉각적.
- "I will work with Vincent and Daniel to send that out this week" - 누가(collaborator) 언제(this week) 무엇을 할지 명시. "I'll send it"가 아니라 "I will work with X and Y"로 협업 책임 분배.
- "I'll take it that as an actual item" - "actual item"이라는 표현이 중요. "I'll consider it"가 아니라 "actual item"으로 action item에 포함시킴을 명시.

### FMS 2026 사전 예약 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 사전 요청 | Triet | "if you require the liquid solution demo hardware at the booth, please let us know so we can begin to arrange" | "please let us know so we can begin to arrange" - 사전 예약 요청 |
| 시간 여유 강조 | Triet | "I know FMS isn't until August. But if you need hardware, we'd like to know sooner than possible so that we can make sure we reserve some demo hardware for SK Hynix" | "sooner than possible" - 빠른 확정 요청 |
| 미결정 인정 | Steve | "we are currently discussing in Eternity, but we didn't make some decision. So we share details once we make a direction" | "we didn't make some decision. share details once we make a direction" - 미결정 솔직 인정 |

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/샘플/일정 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **bi-weekly** | 격주 (2주에 1회) | "we don't have a meeting scheduled next week because this is bi-weekly" - 회의 주기 명시 |
| **pre-installation requirements** | 사전 설치 요건 | "We will have the pre-installation requirements, input power, cables required, network environment, IP, and the DIMMs required" - 설치 전 체크리스트 |
| **customs issues** | 통관 문제 | "if we don't have any customs issues, then we will have all the items in SK Hynix" - 국제 배송 리스크 |
| **CXL Retimer HBA** | CXL 리타이머 호스트 버스 어댑터 | "It will have our CXL Retimer HBA" - 데모 기기 구성 요소 |
| **CXL chassis** | CXL 섀시 | "what's included here will be the CXL chassis" - 데모 하드웨어 본체 |
| **first generation product** | 1세대 제품 | "20 units of one 28 gigabyte first generation product" - 제품 세대 명시 |
| **samples** | 샘플 (양산前 제공품) | "256 samples" - 샘플 수량 |
| **transparent cover** | 투명 커버 (데모용) | "And then transparent cover is being prepared" - 데모 전시용 |
| **HPE Discover** | HPE 연례 행사 | "for HPE Discover 2026, we'd like to check delivery status for the CXL chassis" - 행사명 |
| **FMS** (Flash Memory Summit) | 플래시 메모리 서밋 | "for FMS 2026, we are already discussing about the remote demo" - 8월 행사 |
| **press release** | 보도자료 | "he also has already provided a press release leading up to HPE Discover between Liquid and SK Hynix" - PR 활동 |
| **promotion material** | 홍보 자료 | "have you had a chance to check the promotion material or video clips or something?" - 마케팅 자료 |
| **G2 layer / G3.5 layer** | CXL 연결 계층 (직접/네트워크) | "CXL connected at the G2 layer direct connecting into the server and then also CXL at the G3.5 layer where we connect over the network" - CXL 토폴로지 |
| **KV cache hit rate** | KV 캐시 적중률 | "if we can achieve 70% hit rate from KV cache by adding DRAM at the G2 layer, how much can we achieve?" - 성능 지표 |
| **tokens per second** | 초당 토큰 (LLM 처리량) | "at 90% hit rate, we can get a 7x token per second improvement" - 성능 개선 폭 |
| **load time** | 로드 시간 | "the next data we are measuring is load time" - 지표 |
| **sharded database** | 샤딩된 DB | "this is sharded database, meaning if we take a database that's sharded amongst many servers" - DB 워크로드 |
| **reference architecture** | 참조 아키텍처 (상용화 전 단계) | "at first we want to show that the reference architecture that is a first our purpose" - 제품 단계 |
| **research prototype** | 연구 프로토타입 | "food memory and CXL hybrid memory is a are just a research prototype" - 상용화 전 단계 |
| **route to market / go to market** | 시장 진출 경로 | "how is your guys thinking about route to market if we prove that this architecture is attractive" - GTM 전략 |
| **rack scale appliance** | 랙 단위 어플라이언스 | "Rack scale appliances is the right way to approach this" - 아키텍처 접근법 |
| **wiring diagram** | 배선도 | "maybe we can have a follow on meeting to show wiring diagrams and have a deeper discussion" - 기술 검토 자료 |
| **director of professional services** | 전문 서비스 총괄 | "Daniel Nguyen. He is our director of professional services" - 직함 |
| **DRAM shortages and allocation issues** | DRAM 부족·할당 문제 | "with the DRAM shortages and the allocation issues, every server vendor right now has been very, very slow on delivery time" - 시장 상황 |
| **action item** | 액션 아이템 (후속 과제) | "I'll take it that as an actual item" - 회의 후속 과제 |
| **pool memory / food memory** | 풀 메모리 (전사본에선 food/pool 혼용) | "in as behind the view is a food memory and CXL hybrid memory" - SK Hynix 기술 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 진행·의제 설정 (Meeting Facilitation) ──
- id: m12-001
  expression: "I think we have everyone on. X, Y, Z, where are you to get started?"
  category: roll_call
  function: attendance_check
  speaker_role: facilitator
  difficulty: 3
  context: "And I think we have everyone on. Vincent, Smith, Thomas, where are you to get started?"
  note: 참석자 호명 - "where are you"로 부재자 확인

- id: m12-002
  expression: "Thank you for joining the meeting. Especially since it's already late in the workday on the US side."
  category: opening
  function: time_zone_acknowledgment
  speaker_role: facilitator
  difficulty: 4
  context: "Thank you for joining the meeting. Especially since it's already late in the workday on the US side."
  note: 상대 시간차 인정 - "late in the workday on the US side"

- id: m12-003
  expression: "There's not many items to discuss. So there should be a quick meeting."
  category: agenda_framing
  function: scope_setting
  speaker_role: facilitator
  difficulty: 2
  context: "There's not many items to discuss. So, yeah, there should be a quick meeting."

- id: m12-004
  expression: "Sure, we have two main agenda items. First, we'd like to discuss X. And second, for Y, we'd like to check Z."
  category: agenda_stating
  function: agenda_enumeration
  speaker_role: facilitator
  difficulty: 3
  context: "Sure, we have two main agenda items. First, we'd like to discuss the preparation for system setup. And second, for HPE Discover 2026, we'd like to check delivery status for the CXL chassis."

- id: m12-005
  expression: "you had mentioned via email that there has not been much progress yet. But let's start with..."
  category: email_recall
  function: prior_reference
  speaker_role: facilitator
  difficulty: 4
  context: "So, you had mentioned via email that there has not been much progress yet. But let's start with the brief update on the current shipping status."
  note: "you had mentioned via email" - 이메일 사전 언급 회상, 정확성 확보

# ── 일정·출하 (Schedule & Shipping) ──
- id: m12-006
  expression: "the X items have already shipped. So it's already in Korea."
  category: shipping_status
  function: completed_shipment
  speaker_role: partner
  difficulty: 2
  context: "I think the liquid items have already shipped, our chassis has already shipped. So it's already in Korea."

- id: m12-007
  expression: "we are expected to ship those to X by the end of this week. That is the target."
  category: shipping_target
  function: schedule_target
  speaker_role: partner
  difficulty: 3
  context: "we are waiting on the super micro servers and we are expected to ship those to Korea by the end of this week. That is the target."
  note: "expected to ship" + "That is the target" - 확정 아님 명시

- id: m12-008
  expression: "we expect to have everything land in X by the end of next week"
  category: arrival_estimate
  function: arrival_schedule
  speaker_role: partner
  difficulty: 3
  context: "we expect to have everything land in Korea by the end of next week."
  note: "land in X by..." - 도착 일정 표현

- id: m12-009
  expression: "if everything goes as expected and we don't have any customs issues, then we will have all the items in X by Y"
  category: conditional_schedule
  function: conditional_commitment
  speaker_role: partner
  difficulty: 4
  context: "if everything goes as expected and we don't have any customs issues, then we will have all the items for the first order in SK Hynix by the end of next week."
  note: "if... then we will have..." - 조건부 확정, customs risk 명시

- id: m12-010
  expression: "I will have that by the end of the day tomorrow"
  category: deadline_commitment
  function: specific_deadline
  speaker_role: partner
  difficulty: 3
  context: "I will have that by the end of the day tomorrow."
  note: "by the end of the day tomorrow" - 정확한 기한, "soon" 대신 쓸 것

# ── 사전 설치 요건 (Pre-installation) ──
- id: m12-011
  expression: "we need some detailed information about like input powers or even a cable or network environment"
  category: pre_install_request
  function: info_request
  speaker_role: questioner
  difficulty: 3
  context: "we are preparing some of our room for setup system, but we need some detailed information about like input powers or even a cable or network environment"

- id: m12-012
  expression: "We will have the pre-installation requirements, input power, cables required, network environment, IP, and the DIMMs required as well."
  category: pre_install_list
  function: requirement_enumeration
  speaker_role: partner
  difficulty: 3
  context: "We will have the pre-installation requirements, input power, cables required, network environment, IP, and the DIMMs required as well."
  note: 사전 설치 체크리스트 5종 - 외워서 쓸 것

- id: m12-013
  expression: "please share some kind of system connection diagram to set up X"
  category: diagram_request
  function: doc_request
  speaker_role: questioner
  difficulty: 3
  context: "please share some kind of system connection diagram to set up the five post and one enclosure and even a switch"

- id: m12-014
  expression: "could you share some information before the meeting through the email?"
  category: pre_meeting_request
  function: advance_material_request
  speaker_role: questioner
  difficulty: 3
  context: "We can make a call on Wednesday, but could you share some information before the meeting through the email?"

# ── 샘플·데모 기기 (Sample & Demo Hardware) ──
- id: m12-015
  expression: "we're delivering 20 units of one 28 gigabyte first generation product and also 256 samples"
  category: sample_quantity
  function: quantity_stating
  speaker_role: facilitator
  difficulty: 3
  context: "So we're delivering 20 units of one 28 gigabyte first generation product and also, yeah, second, 256 samples."
  note: 수량+용량+세대 명시 - "X units of Y GB Z generation product"

- id: m12-016
  expression: "what's included here will be the X. It will have Y. It will have our Z. It will also include a W"
  category: bom_enumeration
  function: included_items
  speaker_role: partner
  difficulty: 3
  context: "what's included here will be the CXL chassis. It will have optical cable. It will have our CXL Retimer HBA. It will also include a CXL switch"

- id: m12-017
  expression: "we received the chassis back from Japan from the Penguin event. And we inspected everything and everything is good and ready to be shipped"
  category: hardware_status
  function: readiness_confirmation
  speaker_role: partner
  difficulty: 3
  context: "we received the chassis back from Japan from the Penguin event. And we inspected everything and everything is good and ready to be shipped"

- id: m12-018
  expression: "if you require the X at the booth, please let us know so we can begin to arrange"
  category: advance_reservation
  function: early_request
  speaker_role: partner
  difficulty: 4
  context: "if you require the liquid solution demo hardware at the booth, please let us know so we can begin to arrange"

- id: m12-019
  expression: "we'd like to know sooner than possible so that we can make sure we reserve some demo hardware for SK Hynix"
  category: early_request
  function: early_confirmation
  speaker_role: partner
  difficulty: 4
  context: "we'd like to know sooner than possible so that we can make sure we reserve some demo hardware for SK Hynix."

# ── 홍보·PR (Promotion & PR) ──
- id: m12-020
  expression: "have you had a chance to check the promotion material or video clips or something?"
  category: status_check
  function: polite_progress_check
  speaker_role: questioner
  difficulty: 3
  context: "as I asked by email, have you had a chance to check the promotion material or video clips or something?"
  note: "have you had a chance to X?" - 바쁜 상대 진행 확인 정중 화법

- id: m12-021
  expression: "he also has already provided a press release leading up to X between Y and Z"
  category: pr_status
  function: pr_announcement
  speaker_role: partner
  difficulty: 3
  context: "he also has already provided a press release leading up to HPE Discover between Liquid and SK Hynix"

- id: m12-022
  expression: "we wanted to get the draft out this week so that we can edit and approve back and forth before leading up to the show"
  category: pr_process
  function: review_cycle
  speaker_role: partner
  difficulty: 4
  context: "we wanted to get the draft out this week so that we can edit and approve back and forth before leading up to the show"

- id: m12-023
  expression: "we can promote on social media, LinkedIn, so on and so forth"
  category: channel_listing
  function: promotion_channels
  speaker_role: partner
  difficulty: 2
  context: "we can promote on social media, LinkedIn, so on and so forth"

# ── 방문·일정 조율 (Visit Coordination) ──
- id: m12-024
  expression: "I will work with you offline to schedule a session specifically around the deployment and installation"
  category: offline_coordination
  function: side_session
  speaker_role: partner
  difficulty: 4
  context: "I will work with you offline to schedule a session specifically around the deployment and installation."

- id: m12-025
  expression: "could we make some meeting schedule or list next week because we need time to some kinds of reservation"
  category: schedule_request
  function: advance_booking
  speaker_role: questioner
  difficulty: 3
  context: "And could we make some meeting schedule or list next week because we need time to some kinds of reservation or our meeting room"

- id: m12-026
  expression: "we can do Thursday, your Thursday or Wednesday?"
  category: day_selection
  function: timezone_respect
  speaker_role: partner
  difficulty: 3
  context: "we can do, we can do Thursday, your Thursday or Wednesday?"
  note: "your Thursday" - 상대 시간대 기준 명시

- id: m12-027
  expression: "if we can do the call at 4pm, so one hour earlier, that would be great"
  category: time_adjustment
  function: polite_time_request
  speaker_role: partner
  difficulty: 3
  context: "if we can do the call at 4pm, so one hour earlier, that would be great"

- id: m12-028
  expression: "Could you confirm who will be joining the visit?"
  category: visit_probe
  function: attendance_confirmation
  speaker_role: questioner
  difficulty: 3
  context: "And I have a question regarding the visit Hynix plan. Could you confirm who will be joining the visit?"

- id: m12-029
  expression: "I'd like to coordinate a set up a session with our CXL related VPs or leaders. So it would be a great opportunity to foster our partnership and ensure long term collaboration."
  category: session_proposal
  function: partnership_framing
  speaker_role: questioner
  difficulty: 5
  context: "I'd like to coordinate a set up a session with our CXL related VPs or leaders. So it would be a great opportunity to foster our partnership and ensure long term collaboration."
  note: "foster our partnership" + "ensure long term collaboration" - 고급 협력 표현

- id: m12-030
  expression: "I'm still working on that, but for sure it will be X. I'm not exactly sure yet, but that's what we're working on."
  category: partial_confirmation
  function: partial_answer
  speaker_role: partner
  difficulty: 4
  context: "I'm still working on that, but for sure it will be Daniel, Daniel Nguyen... I'm not exactly sure yet, but that's what we're working on."

# ── 의존성·지연 (Dependency & Delay) ──
- id: m12-031
  expression: "The most important thing right now, Steve, is we need to make sure the X is shipped."
  category: dependency_priority
  function: critical_path_stating
  speaker_role: partner
  difficulty: 4
  context: "The most important thing right now, Steve, is we need to make sure the Super Micro server is shipped."

- id: m12-032
  expression: "we can't do it without the X"
  category: dependency
  function: blocker_stating
  speaker_role: partner
  difficulty: 3
  context: "we can't do it without the Super Micro server."

- id: m12-033
  expression: "the good news is the X shipped already, it's in Korea. We're just waiting on Y."
  category: good_news_pivot
  function: positive_emphasis
  speaker_role: partner
  difficulty: 4
  context: "the good news is that the liquid chassis, the switch, all the other items shipped already, it's in Korea. We're just waiting on Super Micro."

- id: m12-034
  expression: "with the DRAM shortages and the allocation issues, every server vendor right now has been very, very slow on delivery time"
  category: market_context
  function: external_attribution
  speaker_role: partner
  difficulty: 4
  context: "Obviously, you know, with the DRAM shortages and the allocation issues, every server vendor right now has been very, very slow on delivery time."
  note: 업계 공통 문제로 프레이밍 - "every server vendor"

- id: m12-035
  expression: "we really appreciate your patience"
  category: delay_apology
  function: soft_apology
  speaker_role: partner
  difficulty: 2
  context: "we really appreciate your patience."

# ── 기술 회피·포장 (Technical Hedging) ──
- id: m12-036
  expression: "I believe what you're showing here can be supported, but we would need to get some of our architects into the room"
  category: belief_caveat
  function: positive_with_condition
  speaker_role: partner
  difficulty: 5
  context: "I believe what you're showing here can be supported, but we would need to get some of our architects into the room."
  note: "I believe X, but we need Y" - 긍정+조건 구조

- id: m12-037
  expression: "maybe we can have a follow on meeting to show wiring diagrams and have a deeper discussion"
  category: follow_on_proposal
  function: deeper_review
  speaker_role: partner
  difficulty: 4
  context: "maybe we can have a follow on meeting to show wiring diagrams and have a deeper discussion."

- id: m12-038
  expression: "Rack scale appliances is the right way to approach this"
  category: architecture_alignment
  function: agreement_stating
  speaker_role: partner
  difficulty: 4
  context: "Rack scale appliances is the right is the right way to approach this."

- id: m12-039
  expression: "what you're showing makes a lot of sense to us"
  category: agreement
  function: validation
  speaker_role: partner
  difficulty: 3
  context: "what you're showing makes a lot of sense to us."

- id: m12-040
  expression: "it should be doable. We have to just go do the wiring diagram and study it. But I think if it's CXL to CXL, the answer should be yes."
  category: technical_hedge
  function: probable_yes
  speaker_role: partner
  difficulty: 4
  context: "it should be doable. We have to just go we have to go do the wiring diagram and study it. But I think if it's CXL to CXL, the answer should be yes."

- id: m12-041
  expression: "we can't take just a box of memory or just a couple of servers, a rack scale solution where everything is architected to be very tightly coupled"
  category: architecture_principle
  function: design_philosophy
  speaker_role: partner
  difficulty: 5
  context: "We can't we can't take just a box of memory or just a couple of servers, a rack scale solution where everything is architected to be very tightly coupled. We think is the right approach."

# ── GTM 탐색 (Go-to-Market Probe) ──
- id: m12-042
  expression: "how is your guys thinking about route to market if we prove that this architecture is attractive and has a lot of performance?"
  category: gtm_probe
  function: strategy_inquiry
  speaker_role: questioner
  difficulty: 5
  context: "how is your guys thinking about route to market if we prove that this architecture is attractive and has a lot of performance?"

- id: m12-043
  expression: "Is this a solution that X will potentially bring to market or is it just a reference architecture that people can study?"
  category: binary_probe
  function: either_or_inquiry
  speaker_role: questioner
  difficulty: 5
  context: "Is this a solution that Hynix will potentially bring to market or is it just a reference architecture that people can study?"
  note: 이분법으로 상대가 선택하게 만드는 강한 질문

- id: m12-044
  expression: "if customer wants to purchase, we want to be able to purchase"
  category: market_intent
  function: commercial_readiness
  speaker_role: partner
  difficulty: 3
  context: "And if customer wants to purchase. We want to we want to enable. Yeah, we want to be able to purchase."

- id: m12-045
  expression: "we don't need an answer today but if you can think about that, please have some internal discussion and let us know"
  category: polite_deferral
  function: no_pressure_deferral
  speaker_role: partner
  difficulty: 4
  context: "That's fine guys if you could we don't need an answer today but if you can think about that, please, you know have some internal discussion and let us know"

- id: m12-046
  expression: "X is just a research prototype. So at first we want to show that the reference architecture. That is a first our purpose. We haven't decided yet the kind of other products we build ourselves."
  category: product_stage
  function: stage_framing
  speaker_role: questioner
  difficulty: 4
  context: "you know that is a in as behind the view is a food memory and CXL hybrid memory is a are just a research prototype. So at first we want to show that the reference architecture. We haven't decided yet the kind of other products we build ourselves."

# ── 소프트웨어·소스코드 (Software & Source Code) ──
- id: m12-047
  expression: "is X already available and ready, or is that still in development?"
  category: readiness_probe
  function: binary_status_check
  speaker_role: questioner
  difficulty: 3
  context: "is SK Hynix memory sharing software already available and ready, or is that still in development?"

- id: m12-048
  expression: "as a software only, X can be supported by our software, so we can use it. But we cannot share it with our source code. That's the problem."
  category: source_code_boundary
  function: constraint_acknowledgment
  speaker_role: questioner
  difficulty: 4
  context: "as a software only, as a cache coherence can be supported by our software, so we can use it. But we cannot share it with our source code. That's the problem."

- id: m12-049
  expression: "I'll take it that as an actual item and we can discuss it internally"
  category: action_item_elevation
  function: item_promotion
  speaker_role: questioner
  difficulty: 4
  context: "Let me discuss that. I'll take it that as an actual item and we can, we can discuss it internally."
  note: "take it as an actual item" - action item으로 승격

# ── 기술 발표 (Technical Presentation) ──
- id: m12-050
  expression: "we are continuing to test two methodologies. One is X and then also Y"
  category: methodology_intro
  function: approach_enumeration
  speaker_role: questioner
  difficulty: 3
  context: "we are continuing to test two methodologies. One is CXL connected at the G2 layer direct connecting into the server and then also CXL at the G3.5 layer where we connect over the network"

- id: m12-051
  expression: "at 90% hit rate, we can get a 7x token per second improvement"
  category: performance_result
  function: metric_stating
  speaker_role: questioner
  difficulty: 3
  context: "at 90% hit rate, we can get more, most of the tokens out of cash and get a 7x token per second improvement."

- id: m12-052
  expression: "We will follow up the action items and see you next meeting."
  category: closing
  function: wrap_up
  speaker_role: facilitator
  difficulty: 2
  context: "We will follow up the action items and see you next meeting."
  note: 회의 마무리 공식
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-05-13 08 57 57_EN_Liqid_biweekly-extracted.wav` (총 ~36분, 4,708단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | line range | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입부 | line 1-29 | 아이스브레킹, 일본 출장 안부, "Thank you for joining, especially late on the US side" | 회의开场 화법, 시간차 배려 | ★★☆ |
| 2 | 의제 설정 + 출하 상태 | line 46-65 | "we have two main agenda items" + "already shipped" + "expected to ship by end of week" | 의제 명시 + 일정 표현 | ★★★ |
| 3 | 사전 설치 요건 + action item | line 69-107 | Jongmin 요청 + Triet "I'm writing that down right now" + pre-install checklist | 요청-즉석 action item 화법 | ★★★★ |
| 4 | 의존성·지연 포장 | line 222-230 | "most important thing - Super Micro", "can't do it without", "DRAM shortages", "appreciate your patience" | 의존성 전환 + 지연 포장 | ★★★★ |
| 5 | GTM 탐색 + 마무리 | line 436-460 | "how is your guys thinking about route to market" + "we don't need an answer today" + "follow up the action items" | GTM 탐색 + 정중한 미루기 + 마무리 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 4가 가장 가치 높음 - action item 화법과 의존성 포장 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **biweekly status coordination** register다. 기술 Deep-dive(A)나 roadmap(B)과 달리, "언제 어떤 물건이 어디에 도착하는가"를 정확히 조율하는 자리. 두 역할 모두 학습해야:
- **진행자 역할 (Steve, SK Hynix)**: 의제 설정, 상태 확인, action item 정리 - 네가 파트너 하드웨어 받을 때
- **파트너 역할 (Triet, Liqid)**: 출하 상태 보고, 지연 포장, 의존성 전환 - 네가 파트너 입장일 때

Type C 회의는 "정확성"이 핵심이다. "soon", "ASAP"이 아니라 "by the end of the day tomorrow", "by the end of next week"로 정확한 기한을 주는 것. 수량도 "20 units of 128GB first generation product"로 세대·용량까지 명시.

### Pragmatics (화용론) 핵심
1. **"expected to" + "That is the target"**: 일정은 단정적으로 말하지 않는다. "we are expected to ship by the end of this week. That is the target." - "expected" hedge + "target"으로 목표임을 명시. 100% 확정이 아님을 표시하면서도 구체적 일정을 준다. 한국어 "이번 주 말쯤 들어올 예정입니다"의 정확한 영어 표현.
2. **"we can't do it without X"**: 의존성을 강조할 때 쓰는 핵심 화법. 자기 쪽은 준비됐는데 상대(또는 제3자)가 안 돼서 못한다는 것을 명시. "the good news is Y shipped already"로 자기 쪽 완료를 부각하고, "with the DRAM shortages"로 업계 공통 문제로 돌린다.
3. **"I'm writing that down right now"**: 상대가 요청하는 즉시 "지금 적고 있다"고 말해 신뢰를 준다. "I'll note that"보다 훨씬 즉각적이고 신뢰감이 있다.
4. **"have you had a chance to X?"**: 상대 진행 상태를 확인할 때 "did you do X?"가 아니라 "have you had a chance to X?" - 바쁜 상대의 시간을 배려하는 정중한 확인 화법.
5. **"we don't need an answer today but... have some internal discussion and let us know"**: 즉답 압박 없이 내부 논의를 요청하는 정중한 미루기. "I'll take it that as an actual item"으로 action item에 남겨 책임을 유지.

### 네가 당장 써야 할 Top 5
1. **"we are expected to ship X by the end of this week. That is the target."** - 일정 보고
2. **"I'm writing that down right now. I will have that by the end of the day tomorrow."** - 즉석 action item
3. **"The most important thing right now is we need to make sure X is shipped. We can't do it without X."** - 의존성 강조
4. **"have you had a chance to X?"** - 정중한 진행 확인
5. **"we don't need an answer today but if you can think about that, have some internal discussion and let us know"** - 정중한 미루기

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "이번 주 말쯤 들어올 예정입니다" | "we are expected to ship by the end of this week. That is the target." | "expected" + "target"으로 목표임을 명시 |
| "통관 문제만 없으면 다음 주 말에 도착합니다" | "if everything goes as expected and we don't have any customs issues, then we will have all the items by the end of next week" | "if... then we will have..." 조건부 |
| "내일까지 정리해서 보내드리겠습니다" | "I will have that by the end of the day tomorrow" | "by the end of the day tomorrow" 정확한 기한 |
| "시장 상황이라 어쩔 수 없습니다, 양해 부탁드립니다" | "with the DRAM shortages and the allocation issues, every server vendor has been very slow. We really appreciate your patience." | 업계 공통 문제로 프레이밍 + "appreciate your patience" |
| "확인해 보셨습니까?" | "have you had a chance to check X?" | "have you had a chance to" - 바쁨 배려 |
| "내부에서 검토하고 다시 연락드리겠습니다" | "we don't need an answer today but have some internal discussion and let us know" | "we don't need an answer today"로 압박 제거 |
| "지금 적어두겠습니다" | "I'm writing that down right now" | "writing that down right now" - 즉석 신뢰 |
| "누가 오시는지 확인해 주세요" | "Could you confirm who will be joining the visit?" | "Could you confirm" - 정중한 확인 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법(의존성 전환, 기술 회피) + 4절 action item 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 일정 협상 화법 차이 체득
5. **Type C 특화**: 샘플 수량("20 units of 128GB first generation product"), 일정("by the end of next week"), 사전 요건("pre-installation requirements: input power, cables, network, IP, DIMMs")의 정확한 표현을 외울 것 - 이게 네가 다음 파트너 회의에서 가장 먼저 쓸 화법이다

---

*Textbook 12 - Liqid Biweekly (2026-05-13). 회의 유형 C (샘플/일정 조율). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
