---
textbook_id: 14
meeting: AMD (CXL 3.1 verification sample, AMD platform eval, Turin to Venice transition)
date: 2026-04-22
type: C (샘플/일정 조정) - Type C 유지. 회의 전반부가 샘플 출하(FOC, 30 units, VP 에스컬레이션)와 일정(B0 실리콘 5월, Venice 전환, 런칭 후 프로모션) 조정이 주를 이룸. 후반에 P0 슬롯 리부트 이슈 디버깅(Type D 요소)과 Venice 로드맵 정렬(Type B 요소)이 포함되나, 핵심 기조는 "샘플·일정 조정"임.
partner: AMD (Kitan/Ke-Tung, AMD 보드 담당자, AMD VP 에스컬레이션 대상)
sk_side: SK hynix CXL App Engineering (Yun-Jong), 제품/협업 코디네이터, Chin-Sung Kim (CXL hybrid 발의자)
duration_words: 3659
audio: repo/webex-audio/2026-04-22 08 06 38_EN_AMD-extracted.wav
transcript: repo/webex-audio/2026-04-22 08 06 38_EN_AMD-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, amd, cxl, cxl-3.1, venice, turin, b0-silicon, sample-coordination, foc, platform-eval, type-c]
---

# Textbook 14 - AMD (CXL 3.1 verification sample, Turin to Venice transition) (2026-04-22)

> **회의 유형**: C (샘플/일정 조정) - 샘플 출하 조정(FOC, 수량 협의), CPU 플랫폼 전환(Turin->Venice), B0 실리콘 일정, 프로모션 데이터 공개 시점
> **학습 가치**: 파트너와의 샘플 수량/비용 협상, "우리는 고객이 아닌 파트너다"는 관계 프레이밍, 일정 지연·공급 제약의 정중한 전달, 디버깅 정보 수집 화법
> **Audrey 관점**: 이 회의는 SK hynix가 AMD에 "샘플을 받아야 하는 쪽"이자 "CXL 디바이스를 제공하는 쪽" 양쪽 역할을 다룬다. 네가 파트너사와 샘플/일정/비용을 조율할 때 직접 써야 할 화법이 밀집해 있다. 특히 "partnership, not customer" 프레이밍과 "let me talk with my VP and get back to you" 에스컬레이션 화법은 무조건 익혀야 한다.

---

## 1. 발화 아키텍처 - SK 코디네이터의 4단계 회의 운영

이 회의는 SK 측 코디네이터가 agenda를 순차적으로 넘기며 운영한다. 각 단계마다 **고정된 화법 공식**이 있다.

### 단계 1: 샘플 상태 확인 (Sample Status Check)

코디네이터는 "ready to shift"로 상태를 보고하고, 즉시 "but we need to peel(PO)"로 조건을 건다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we ready to shift the X now completely the preparation of Y` | "we ready to shift the validation sample now completely the preparation of the previous sample" | 준비 완료 보고 - "ready to shift"로 진행 상태 표시 |
| `But we need to X. For sure. X is required for Y` | "But we need to peel. For sure. Peel is required for sample shipment to return." | 조건 부여 - "For sure"로 필수성 강조 |

**Audrey 교훈**: 샘플 출하를 보고할 때 "we are ready to shift"로 진행 상태를 먼저 보여주고, "But we need to PO. For sure."로 필수 조건을 즉시 건다. "For sure"가 조건의 강제성을 부드럽게 만든다. 한국어로는 "PO 필요합니다"인데, 영어는 "For sure"를 붙여서 "이건 정말 필요해요"라는 뉘앙스를 준다.

### 단계 2: 가격 불만 제기 (Price Pushback)

AMD 측이 SK hynix CXL 디바이스 가격 인상에 불만을 제기하는 구간. "partnership, not customer" 프레이밍이 핵심.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `you guys keep raising the price, right?` | "you guys keep raising the price, right? Right now it's at $6,000" | 반복적 불만 - "keep ~ing"로 패턴 비난 |
| `it's not helping us, right?` | "I mean, it's not helping us, right?" | 부정적 영향 진술 - "not helping us" |
| `the budget was already sorted last year. Now we have to go redo the budget, right?` | "the budget was already sorted last year. Now we have to go redo the budget, right?" | 예산 재작업 부담 호소 |
| `this is a partnership, right? We are not a customer` | "this is a partnership, right? We are not a customer" | 관계 재정의 - "partnership, not customer" |
| `you guys are treating us like a customer, which is not helping, right?` | "you guys are treating us like a customer, which is not helping, right?" | 행동 비판 - "treating us like a customer" |

**Audrey 교훈**: "We are not a customer" - 이 한 문장이 파트너 협상의 핵심 무기다. "우리는 고객이 아니라 파트너다"라고 선언하면, 상대방의 가격 인상·단순 공급 관계 행동을 "파트너십에 어긋난다"고 프레이밍할 수 있다. 한국어로는 "우린 파트너 아닙니까"인데, 영어는 "We are not a customer"로 먼저 부정한 뒤 "this is a partnership"으로 긍정을 제시하는 구조가 더 강하다. "treating us like a customer"는 행동을 직접 비판하는 화법이다 - "고객 취급한다"는 말은 매우 직접적이지만 "which is not helping"으로 한 번 희석한다.

### 단계 3: 에스컬레이션 약속 (Escalation Commitment)

AMD 담당자는 "Let me talk with our VP"로 에스컬레이션을 약속하고, "stay tuned"로 후속을 약속한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?` | "Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?" | 에스컬레이션 + 후속 약속 + 동의 확인 |
| `some of them I can shift them out as the FOC, but the rest of them, at any time we talk with my VP and the stakeholder` | "some of them, yeah, I can shift them out, yeah, as the FOC, the free of charge, but the rest of them, at any time we talk, yeah, with my VP and the stakeholder" | 부분 승인 + 나머지 에스컬레이션 - "some of them I can, but the rest I need to talk" |
| `stay tuned and I will give you my feedback` | "stay tuned and I will give you my feedback" | 후속 약속 - "stay tuned" |

**Audrey 교훈**: "Let me talk with our VP and I will give you my feedback soon" - 이게 에스컬레이션의 정석이다. "I'll check"가 아니라 "Let me talk with our VP"로 구체적 에스컬레이션 대상을 명시하고, "I will give you my feedback soon"으로 시점을 약속한다. "Is it OK for you?"로 동의까지 구한다. "stay tuned"은 회의에서 "기다려주세요"를 자연스럽게 말하는 화법이다.

### 단계 4: 평가 결과 전환 (Evaluation Transition)

샘플 논의가 끝나면 "OK, let's move on to the next slide"로 전환하고, "Are there any other updates beside these above items?"로 상태를 확인한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|
| `OK, let's move on to the next slide` | "OK, let's move on to the next slide" | 주제 전환 공식 |
| `Are there any other updates beside these above items?` | "Are there any other updates beside these above items?" | 추가 정보 탐색 - "beside these above items" |
| `No further updates, you know, I think the team is going to continue their testing` | "No further updates, you know, I think the team is going to continue their testing. But there is no new updates." | 상태 보고 - "No further updates" + "team is going to continue" |

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. AMD 측이 약점(공급 부족, 가격 인상, 이슈 미보고)을 어떻게 정중하게 포장하는지, 그리고 SK 측이 불만을 어떻게 정중하게 제기하는지.

### 전략 1: 부분 승인 + 나머지 에스컬레이션 (Partial Grant + Rest Escalation)

한 번에 전부 승인하지 않고, 일부는 승인하고 나머지는 "VP와 논의"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| FOC 샘플 수량 | "some of them, yeah, I can shift them out, yeah, as the FOC, the free of charge, but the rest of them, at any time we talk, yeah, with my VP and the stakeholder. So stay tuned and I will give you my feedback." | "일부는 FOC로 출하할 수 있습니다. 나머지는 VP와 스테이크홀더와 논의 후 피드백 드리겠습니다. 기다려주세요" |

**패턴 공식**: `Some of them I can shift out as FOC, but the rest of them, I need to talk with my VP and the stakeholder. Stay tuned and I will give you my feedback.`

**Audrey 교훈**: "전부 안 됩니다"가 아니라 "일부는 할 수 있고, 나머지는 VP와 논의하겠습니다"로 부분 승인 + 에스컬레이션. 이게 파트너 회의에서 "거절을 부드럽게 하는" 핵심 화법이다. 한국어로는 "일부는 가능하고, 나머지는 내부 확인 후 회신드리겠습니다"인데, 영어는 "some of them I can, but the rest I need to talk with my VP"로 구체적 에스컬레이션 대상을 명시한다. "stay tuned"가 "기다려주세요"의 자연스러운 영어 표현이다.

### 전략 2: 공급 제약을 시장 상황으로 돌리기 (Supply Constraint Externalization)

B0 실리콘 5월 가능을 알리면서 "supply constraint is pretty bad"로 외부 요인을 강조한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| B0 실리콘 일정 | "it's looking like sometime in May. Sometime May. Yeah, it's just right now this, the supply constraint is, is pretty bad. So, we just don't have, we are not getting as many CPUs as we were supposed to get because of the way for availability." | "5월 중 어느 시점입니다. 지금 공급 제약이 꽤 심합니다. wafer 가용성 문제로 예정만큼 CPU를 받지 못하고 있습니다" |

**패턴 공식**: `It's looking like sometime in X. The supply constraint is pretty bad right now. We are not getting as many Y as we were supposed to get because of Z availability.`

**Audrey 교훈**: "5월에 가능합니다"만 말하면 상대가 "왜 이렇게 늦리냐"고 묻는다. 그래서 "supply constraint is pretty bad"를 먼저 깔고, "we are not getting as many CPUs as we were supposed to get"로 "원래 더 받아야 하는데 못 받고 있다"고 설명한다. "we were supposed to get"이 핵심이다 - "원래 이렇게 받기로 했었다"를 past expectation으로 표현해서 책임을 wafer 가용성으로 돌린다. 한국어 "시장 상황이라 어쩔 수 없습니다"보다 훨씬 구체적이고 설득력 있다.

### 전략 3: 이슈 미보고를 "이상 없음"으로 포장 (No-News-as-Good-News)

기능 테스트 결과를 공개 안 하면서 "이상 없으면 보고 안 한다"는 논리로 포장한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 기능 테스트 결과 비공개 | "If there is a problem, we'll report it, but we don't usually release any test results for the feature testing. Because feature testing, basically, they'll go test the feature if it works. They'll check off, they move to the next feature, right? If it doesn't work, then we're going to call you" | "문제 있으면 보고합니다. 하지만 기능 테스트 결과는 보통 공개 안 합니다. 기능 테스트는 작동하면 체크하고 다음으로 넘어가니까요. 안 되면 그때 연락드리겠습니다" |

**패턴 공식**: `If there is a problem, we'll report it, but we don't release test results for X. If it doesn't work, then we're going to call you.`

**Audrey 교훈**: "우리가 결과 안 공개한다"는 부정적 메시지를 "문제 있으면 보고하니까, 안 보고되면 이상 없다는 뜻"으로 재프레이밍. "If there is a problem, we'll report it"이 핵심 - 조건문 "If"로 "문제 없으면"의 경우를 자연스럽게 포함. 한국어 "이상 없으면 별도 보고 안 합니다"의 영어 버전인데, 영어는 "If there is a problem, we'll report it"로 긍정 조건을 먼저 제시해서 더 부드럽다.

### 전략 4: 프로모션 데이터 사전 공개 거절 (Pre-Launch Data Refusal)

런칭 전 성능 데이터 공개 요청을 "we'll have to wait till after the launch"로 정중히 거절하고, "we don't want to showcase something and then go back and say we have to change"로 이유를 댄다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 런칭 전 성능 데이터 공개 | "No. Yeah, we'll have to wait till after the launch." + "we don't want to showcase something and then we go back and say, oh, we have to change because we didn't get the best performance the first time. So, it's better to provide the best performance the first time." | "아뇨, 런칭 후에 기다려야 합니다. 한 번 보여주고 나서 "바꿔야 한다"고 할 순 없으니까요. 처음부터 최고 성능으로 보여주는 게 낫습니다" |

**패턴 공식**: `We'll have to wait till after the launch. We don't want to showcase something and then go back and say we have to change. It's better to provide the best performance the first time.`

**Audrey 교훈**: "No"라고 직접 거절한 뒤 "we don't want to showcase something and then go back and say we have to change"로 "다시 바꾸는 상황을 만들고 싶지 않다"는 이유를 댄다. 이게 거절을 정당화하는 화법이다. "It's better to provide the best performance the first time"로 긍정 대안을 제시. 한국어 "런칭 전엔 어렵습니다"보다 훨씬 설득력 있다 - "우리가 첫인상을 중요하게 생각한다"는 뉘앙스이기 때문.

### 전략 5: 약어 풀이로 전문성 표시 (Acronym Glossing)

LDE 같은 약어를 물어보면 "link disable enable"로 풀어서 설명하며 전문성을 표시한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| LDE 설명 | "Oh, so it's link disable enable. So we have a tool, right, that will disable the link and re-enable it." | "LDE는 link disable enable입니다. 링크를 비활성화했다가 다시 활성화하는 도구가 있습니다" |

**패턴 공식**: `Oh, so it's X (full form). So we have a tool that will Y.`

**Audrey 교훈**: 약어를 물어볼 때 "It's LDE, you know"가 아니라 "It's link disable enable"로 full form을 먼저 제시. 그리고 "So we have a tool that will disable the link and re-enable it"로 기능을 설명. 이게 전문성을 보이는 화법이다. 모르는 약어를 물어보면 full form으로 답하고, 구체적 기능을 붙여라.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 기술적으로 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 추가 정보 탐색 (Additional Update Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Are there any other updates beside these above items?` | "Are there any other updates beside these above items?" | "이 항목 외에 다른 업데이트 있습니까?" - 정중한 추가 탐색 |
| `No further updates, you know, I think the team is going to continue their testing. But there is no new updates.` | "No further updates, you know, I think the team is going to continue their testing. But there is no new updates." | 부정 보고 + 진행 상태 표시 |

**Audrey 교훈**: "Are there any other updates beside these above items?" - "beside these above items"가 핵심이다. "Any other updates?"만 하면 너무 포괄적이지만, "위 항목 외에"로 범위를 좁히면 상대가 "이 항목들은 봤고, 그 외에 새 게 있느냐"는 질문 의도를 정확히 파악한다. 회의에서 이전 항목들을 리뷰한 뒤 추가 정보를 물을 때 써라.

### 질문 유형 2: 정확한 수치/버전 요구 (Specific Value Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `which version you used for the BIOS and BMC?` | "which version you used for the BIOS and BMC?" | 버전 확인 - 직접적이면서 정중 |
| `when will be the available for the delivery, the B0 silicon?` | "when will be the available for the delivery, the B0 silicon?" | 일정 확인 - 구체적 일정 요구 |
| `How many, how many systems do you guys have?` | "How many, how many systems do you guys have?" | 수량 확인 - "you guys"로 비격식 |

**Audrey 교훈**: "which version you used for X" - "what version"이 아니라 "which version"이 더 정확하다. "어떤 버전을 쓰셨습니까?" - 버전이 여러 개일 때 "which"를 쓴다. 회의에서 상대가 특정 버전을 썼다고 할 때 "which version you used for X"로 확인해라.

### 질문 유형 3: 조건 확인 (Condition Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Do you have any concern or other relevant opinions regarding this?` | "I would appreciate it if you could provide any concern or other relevant opinions regarding this. This means that we want to change the, from Turin to Venice." | "이에 대해 우려나 의견 있습니까?" - 정중한 의향 탐색 |
| `Is it right?` | "Is it right, Yun-Jeong?" | 짧은 확인 - 발언 검증 |
| `Am I correct?` | "Am I correct?" | "제가 맞습니까?" - 자신의 이해 검증 |
| `do you agree that the changes, the CPU from the Turin to Venice for this evaluation, is it right?` | "do you agree that the changes, the CPU from the Thuring to Venice for this evaluation, is it right?" | "동의하십니까?" - 결정 동의 요구 |

**Audrey 교훈**: "I would appreciate it if you could provide any concern or other relevant opinions regarding this" - 이게 정중한 의향 탐색의 정석이다. "우려 있습니까?"가 아니라 "우려나 의견 주시면 감사하겠습니다" - "I would appreciate it if you could"로 감사를 먼저 표현. 회의에서 상대의 동의를 구할 때 "Do you agree that X is right?"로 직접 물어라. "is it right?"로 끝나는 짧은 확인은 회의 흐름을 끊지 않으면서 검증하는 화법이다.

### 질문 유형 4: 이슈 보고 (Issue Report)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `when we do the memory test like GSA in P0 slot, the link, our link is very unstable. So it, the system hurts and reboot. So we can't go on the memory test in P0 slot.` | "when we do the memory test like GSA in P0 slot, the link, our link is very unstable. So it, the system hurts and reboot. So we can't go on the memory test in P0 slot." | 이슈 보고 - 원인-증상-결과 구조 |
| `after one hour, it, the system reboots` | "when we run about up to one hour, it, the system reboots" | 시간 조건 - "up to one hour" |
| `there is no any BIOS log when system reboots. So it overrides the log.` | "actually there is no, any BIOS log when system reboots. So it overrides the log." | 증상 부연 - 로그 미존재 |

**Audrey 교훈**: 이슈를 보고할 때 "when we do X, the link is very unstable. So the system hurts and reboot. So we can't go on the Y" - 3단 구조로 보고한다. 1) 조건(when we do X), 2) 증상(the link is unstable, system reboots), 3) 결과(we can't go on the test). 이게 디버깅 회의에서 이슈를 명확히 전달하는 공식이다. 한국어 "P0 슬롯에서 GSA 돌리면 리부트됩니다"보다 훨씬 구조적이다.

### 질문 유형 5: 디버깅 정보 요구 (Debug Info Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `do you have any kernel or the BIOS log, even if they don't have any clue or evidence?` | "do you have any kernel or the BIOS log, even if they don't have any clue or evidence?" | 로그 요구 - "even if they don't have any clue"로 단서 없어도 요구 |
| `I need to know the BIOS version. I need to know the BMC version. I need to know what FV, FPGA version you are using` | "I need to know the BIOS version. I need to know the BMC version. I need to know what FV, FPGA version you are using" | 정보 요구 - "I need to know" 반복 |

**Audrey 교훈**: "I need to know X"를 반복하는 게 정보 요구의 직접적 화법. "Could you please share"같은 간접 화법도 좋지만, 디버깅에 필요한 정보는 "I need to know"로 직접 요구해야 한다. 그리고 "even if they don't have any clue or evidence" - "단서가 없어도"로 조건을 완화해서, "아무것도 없어도 보내주세요"라고 부탁하는 화법이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 핵심. 샘플 수량·비용·일정 협상과 action item을 정하는 언어.

### 샘플 협상 화법 (Type C 핵심)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| FOC 요청 | SK | "I thought these are part of the free samples that were agreed in the QTR" | "QTR에 합의한 무료 샘플的一部分" - 사전 합의 호소 |
| VP 합의 회상 | SK | "The last QTR, your VP agreed with AMD VP Amit that they would be sending free CXL devices" | "지난 QTR, 귀사 VP가 AMD VP Amit와 무료 CXL 디바이스 전송 합의" - 과거 합의 명시 |
| 부분 승인 | AMD | "some of them I can shift them out as the FOC, but the rest of them, at any time we talk with my VP and the stakeholder" | "일부는 FOC로, 나머지는 VP와 논의" - 부분 승인 + 에스컬레이션 |
| 후속 약속 | AMD | "stay tuned and I will give you my feedback" | "stay tuned" - 후속 약속 |
| VP 직접 에스컬레이션 경고 | SK | "If he says no, then I'll have to Amit reach out to him directly" | "VP가 아니면 Amit가 직접" - 상위 에스컬레이션 암시 |
| PO 보낸 사실 | SK | "We sent you a PO for the three units because that was outside of what, outside of the three units you're sending" | "3 units는 별도 PO" - 비용 처리 명시 |
| 이해관계 부각 | SK | "it is in your best interest, right, that you provide the samples so that we can put it into our well, you know, volume validation" | "your best interest" - 상대 이익으로 프레이밍 |

**Audrey 교훈**:
- "these are part of the free samples that were agreed in the QTR" - 과거 합의를 "agreed in the QTR"로 명시하면 상대가 부인하기 어렵다. 회의에서 약속 이행을 요구할 때 "이전에 합의한 것"을 먼저 인용해라.
- "your VP agreed with AMD VP Amit" - 구체적 이름까지 명시하면 더 강력하다. "누가 누구와 합의했다"를 명시.
- "it is in your best interest that you provide the samples" - "우리가 필요하다"가 아니라 "당신 이익에 부합한다"로 프레이밍. 이게 협상의 핵심 화법이다.
- "stay tuned"는 회의에서 "기다려주세요"의 자연스러운 영어 표현이다. "please wait"보다 훨씬 자연스럽다.

### 일정 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| B0 일정 질문 | SK | "when will be the available for the delivery, the B0 silicon?" | 구체적 일정 요구 |
| 일정 답변 | AMD | "it's looking like sometime in May" | "5월 중 어느 시점" - 모호 일정 |
| 공급 제약 설명 | AMD | "the supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get because of the wafer availability" | 외부 요인 - wafer 가용성 |
| 일정 재확인 | SK | "you telling me late May, right?" | "5월 말이죠?" - 확인 |
| 정확한 날짜 부인 | AMD | "I don't have a specific date, but it is out about more than a month" | "정확한 날짜 없음, 한 달 이상" |
| 시스템 수량 확인 | AMD | "how many, how many systems do you guys have?" | 상대 보유 수량 확인 |
| 확인 약속 | AMD | "I will check it with our engineers. After checking it, I will let you know, get back to you" | "확인 후 회신" - 표준 후속 약속 |

**Audrey 교훈**:
- "it's looking like sometime in May" - "sometime"이 핵심이다. "in May"만 하면 너무 확정적이고, "we don't know"는 너무 무책임. "sometime in May"가 "5월 중 어느 시점"으로 적당히 모호하면서 책임감 있는 표현.
- "I don't have a specific date, but it is out about more than a month" - 정확한 날짜를 모를 때 "I don't have a specific date, but ~"로 면책하면서 대략적 범위를 준다. "about more than a month"로 "한 달 이상"의 대략 범위 제시.
- "I will check it with our engineers and get back to you" - 일정 확인의 표준 화법. "I'll check"보다 "I will check with our engineers"로 구체적 확인 대상을 명시.

### 플랫폼 전환 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 전환 제안 | SK | "we are considering to switch to Venice, from Turin, to proceed with the evaluation" | "Venice로 전환 검토" - 정중한 전환 제안 |
| 이유 설명 | SK | "the concerns about the performances differences and due to the limitations of the Turin, the support for the CXL 2.0 and PCIe Gen 5" | "Turin의 CXL 2.0/PCIe Gen 5 제약" - 기술적 이유 |
| 동의 요구 | SK | "do you agree that the changes, the CPU from the Turin to Venice for this evaluation, is it right?" | "동의하십니까?" - 결정 동의 |
| 동의 표시 | AMD | "Yeah, I think it makes sense. I think you've done enough testing on Turin with the CXL 2.0, right? You probably want to show the new thing." | "makes sense" - 동의 + 이유 부연 |

**Audrey 교훈**:
- "we are considering to switch to X, from Y" - 전환 제안의 정중한 화법. "we will switch"가 아니라 "we are considering to switch"로 "검토 중"이라는 여지를 둔다.
- "I think it makes sense" - 동의의 자연스러운 표현. "I agree"보다 "it makes sense"가 더 전문가적이다. "이치에 맞다"는 뜻으로, 단순 동의가 아니라 "이유를 듣고 보니 타당하다"는 뉘앙스.

### 프로모션 데이터 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 사전 공개 요청 | SK | "If we would like to show and share the data before launch of your Venice, is it possible?" | "런칭 전 공개 가능?" - 정중한 요청 |
| 거절 | AMD | "No. Yeah, we'll have to wait till after the launch." | "아뇨, 런칭 후 기다려야" - 직접 거절 |
| 이유 | AMD | "we don't want to showcase something and then we go back and say, oh, we have to change because we didn't get the best performance the first time" | "다시 바꿀 수 없다" - 이유 |
| 대안 제시 | AMD | "you could do a joint announcement, maybe that might be okay to do, but you would need our legal, MD legal to approve it" | "joint announcement + legal 승인" - 조건부 대안 |
| 일정 조정 | SK | "I think we haven't decided yet to which event to be built aim for. June timeframe is HP Discovery, but not right time. August timeframe might be possible. Maybe it's getting close to launch, but it's not there." | "이벤트 미결정. 6월 HP Discovery는 이르고, 8월이 가능할 듯" - 일정 분석 |

**Audrey 교훈**:
- "If we would like to X, is it possible?" - 요청을 "If" 조건문으로 감싸면 정중하다. "We would like to X"만 하면 요구가 되지만, "If we would like to X, is it possible?"은 "만약 우리가 X하고 싶다면, 가능합니까?"로 탐색적 질문이 된다.
- "you could do a joint announcement, maybe that might be okay to do, but you would need our legal to approve it" - 거절에 대안을 제시하는 화법. "joint announcement"라는 대안을 주되 "legal approval"이라는 조건을 건다. "No" 다음에 "but you could do X"가 오면 거절이 협상으로 전환된다.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 디버깅 정보 공유 약속 | SK | "we will share the infrastructure environment and the log, what we have, if it is possible" | "공유하겠습니다" - 정보 공유 약속 |
| 정보 요구 목록 | AMD | "I need to know the BIOS version. I need to know the BMC version. I need to know what FV, FPGA version you are using. I also need to know how much memory is in the system" | "I need to know" 반복 - 정보 요구 |
| 후속 채널 | SK | "if you have any update with the time, please share with us" | "업데이트 있으면 공유 부탁" - 후속 채널 |
| 다음 미팅 연기 | SK | "Can we do it in the next meeting? We can arrange the quick meeting." | "다음 미팅에서" - 정중한 연기 |
| 다음 미팅 데이터 공유 약속 | SK | "I will share our test results on AMD-based Venice" | "Venice 테스트 결과 공유" - 구체적 약속 |

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/CPU 플랫폼/검증 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **FOC** (Free of Charge) | 무료 제공 샘플 | "I can shift them out as the FOC, the free of charge" - 약어 풀이 패턴 |
| **QTR** (Quarterly Technical Review) | 분기 기술 검토 회의 | "the free samples that were agreed in the QTR" - 사전 합의 회의 |
| **PO** (Purchase Order) | 구매 주문서 | "We sent you a PO for the three units" - 비용 처리 명시 |
| **VP** (Vice President) | 부사장 | "Let me talk with our VP and I will give you my feedback" - 에스컬레이션 대상 |
| **LDE** (Link Disable Enable) | PCIe 링크 비활성화/재활성화 테스트 | "it's link disable enable. So we have a tool that will disable the link and re-enable it" - 약어 풀이 |
| **GSA** (Global System Abort?/Graphics/System Agent) | 24시간 시스템 안정성 테스트 | "this 24 hour GSA test" - 장시간 스트레스 테스트 |
| **SBR** | System Boot Reset (또는 유사 부트 테스트) | "the SBR, LDE, Link Training, the GSA" - 검증 항목 나열 |
| **stepping** | CPU 실리콘 리비전 (A0, B0) | "the stepping B version? The CPU version?" / "A0 stepping" / "B0 silicon" - 리비전 표시 |
| **B0 silicon** | 두 번째 실리콘 리비전 (성능 튜닝 적용) | "we need the B0 silicon CPU for this evaluation" / "it's tuned only for functionality" - 성능 vs 기능 |
| **A0 silicon** | 첫 실리콘 리비전 (기능 검증용) | "our CRB board is based on the A0 silicon based" - 초기 리비전 |
| **Turin** | AMD CPU 코드명 (CXL 2.0, PCIe Gen 5) | "we projected has the different interfaces" / "limitations of the Turin, the support for the CXL 2.0" - 구형 플랫폼 |
| **Venice** | AMD 차세대 CPU 코드명 (CXL 3.1 지원 예정) | "we are considering to switch to Venice, from Turin" - 신형 플랫폼 |
| **CRB** (Customer Reference Board) | AMD 고객 참조 보드 | "our CRB board is based on the A0 silicon" - 평가 보드 |
| **backplane** | 보드 간 연결 패널 | "the one is the backplane. Another one is based on the PCI" - 인터페이스 종류 |
| **pre-ES1** | Pre-Engineering Sample 1 (초기 엔지니어링 샘플) | "we planned to conduct the evaluation using the pre-ES1 128 gigabyte, the extended format" - 샘플 단계 |
| **BIOS** | Basic Input/Output System | "we use 74B, which was the latest release BIOS" - 버전 명시 |
| **BMC** | Baseboard Management Controller | "I need to know the BMC version" - 디버깅 정보 |
| **FV** (FPGA Version?) | FPGA 펌웨어 버전 | "I need to know what FV, FPGA version you are using" - 디버깅 정보 |
| **NUMA node** | Non-Uniform Memory Access 노드 | "it will show up as a CXL 3.1 memory in NUMA node" - CXL 메모리 매핑 |
| **PCIe Gen 6** | 6세대 PCIe (Turin 미지원, Venice 지원 예정) | "we expect that the device will link up at gen 6 rate" - 링크 속도 |
| **link training** | PCIe 링크 초기화 협상 과정 | "the SBR, LDE, Link Training, the GSA" - 검증 항목 |
| **ePVB** | (보드/플랫폼 검증) | "Our ePVB passed all the tests" - 검증 통과 |
| **HP Discovery** | HP 고객 행사 (6월) | "in June timeframe, there are just some customer events such as the HP discovery" - 프로모션 후보 |
| **OFC** (Optical Fiber Conference?) | 광통신 행사 | (line 226 문맥상 행사명) - 프로모션 타겟 |
| **CRD** (Customer Requirement Document?) | 고객 요구 문서 | "it's included. Part of the initial CRD" - 비용 포함 근거 |
| **joint announcement** | 공동 발표 | "you could do a joint announcement, but you would need our legal to approve it" - 공동 PR 조건 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 샘플 협상 (Sample Negotiation) ──
- id: m14-001
  expression: "we ready to shift the X now completely the preparation of Y"
  category: sample_status
  function: readiness_report
  speaker_role: coordinator
  difficulty: 3
  context: "we ready to shift the validation sample now completely the preparation of the previous sample"
  note: 샘플 준비 완료 보고 - "ready to shift"로 진행 상태

- id: m14-002
  expression: "But we need to X. For sure. X is required for Y"
  category: condition_setting
  function: mandatory_requirement
  speaker_role: coordinator
  difficulty: 4
  context: "But we need to peel. For sure. Peel is required for sample shipment to return."
  note: "For sure"로 필수 조건 강조 - 부드러운 강제

- id: m14-003
  expression: "I thought these are part of the free samples that were agreed in the QTR"
  category: prior_agreement
  function: precedent_invocation
  speaker_role: questioner
  difficulty: 4
  context: "I thought these are part of the free samples that were agreed in the QTR"
  note: 과거 합의 호소 - "agreed in the QTR"로 사전 합의 명시

- id: m14-004
  expression: "your VP agreed with X VP that they would be sending free Y"
  category: prior_agreement
  function: specific_person_invocation
  speaker_role: questioner
  difficulty: 5
  context: "The last QTR, your VP agreed with AMD VP Amit that they would be sending free CXL devices"
  note: 구체적 이름 명시 - "VP agreed with VP"로 합의 당사자 명시

- id: m14-005
  expression: "Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?"
  category: escalation
  function: escalation_commitment
  speaker_role: partner
  difficulty: 4
  context: "Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?"
  note: 에스컬레이션 정석 - 구체적 대상 + 시점 + 동의 확인

- id: m14-006
  expression: "some of them I can shift them out as the FOC, but the rest of them, I need to talk with my VP and the stakeholder"
  category: partial_grant
  function: partial_approval_with_escalation
  speaker_role: partner
  difficulty: 5
  context: "some of them, yeah, I can shift them out, yeah, as the FOC, the free of charge, but the rest of them, at any time we talk, yeah, with my VP and the stakeholder"
  note: 부분 승인 + 나머지 에스컬레이션 - 핵심 회피 화법

- id: m14-007
  expression: "stay tuned and I will give you my feedback"
  category: follow_up_promise
  function: natural_wait_request
  speaker_role: partner
  difficulty: 3
  context: "So stay tuned and I will give you my feedback"
  note: "기다려주세요"의 자연스러운 영어 - "please wait"보다 자연스러움

- id: m14-008
  expression: "We sent you a PO for the three units because that was outside of the three units you're sending"
  category: cost_clarification
  function: payment_basis
  speaker_role: questioner
  difficulty: 4
  context: "We sent you a PO for the three units because that was outside of what, outside of the three units you're sending"
  note: 비용 처리 명시 - "outside of X"로 범위 구분

- id: m14-009
  expression: "it is in your best interest, right, that you provide the samples so that we can put it into our volume validation"
  category: interest_framing
  function: partner_benefit_reframe
  speaker_role: questioner
  difficulty: 5
  context: "it is in your best interest, right, that you provide the samples so that we can put it into our well, you know, volume validation"
  note: "your best interest" - 상대 이익으로 프레이밍. 협상 핵심

- id: m14-010
  expression: "If he says no, then I'll have Amit reach out to him directly"
  category: escalation_threat
  function: higher_escalation_hint
  speaker_role: questioner
  difficulty: 5
  context: "If he says no, then I'll have Amit reach out to him directly"
  note: 상위 에스컬레이션 암시 - "VP가 아니면 VP 직접"

# ── 가격 불만 (Price Pushback) ──
- id: m14-011
  expression: "you guys keep raising the price, right?"
  category: price_complaint
  function: pattern_criticism
  speaker_role: partner
  difficulty: 3
  context: "you guys keep raising the price, right? Right now it's at $6,000"
  note: "keep ~ing"로 반복적 패턴 비난

- id: m14-012
  expression: "it's not helping us, right?"
  category: negative_impact
  function: harm_stating
  speaker_role: partner
  difficulty: 2
  context: "I mean, it's not helping us, right?"
  note: 부정적 영향 진술 - "not helping us"

- id: m14-013
  expression: "the budget was already sorted last year. Now we have to go redo the budget, right?"
  category: budget_burden
  function: rework_complaint
  speaker_role: partner
  difficulty: 4
  context: "the budget was already sorted last year. Now we have to go redo the budget, right?"
  note: 예산 재작업 부담 호소 - "redo the budget"

- id: m14-014
  expression: "this is a partnership, right? We are not a customer"
  category: relationship_framing
  function: partnership_declaration
  speaker_role: partner
  difficulty: 5
  context: "this is a partnership, right? We are not a customer"
  note: 파트너 협상 핵심 무기 - "We are not a customer". 무조건 외울 것

- id: m14-015
  expression: "you guys are treating us like a customer, which is not helping, right?"
  category: behavior_criticism
  function: action_critique
  speaker_role: partner
  difficulty: 5
  context: "you guys are treating us like a customer, which is not helping, right?"
  note: 행동 비판 - "treating us like a customer" + "which is not helping"으로 희석

- id: m14-016
  expression: "for enablement, you know, you need to work with us"
  category: enablement_demand
  function: collaboration_requirement
  speaker_role: partner
  difficulty: 4
  context: "for enablement, you know, you need to work with us"
  note: "enablement" - 기술 활성화를 위한 협력 요구

# ── 평가 결과 (Evaluation Status) ──
- id: m14-017
  expression: "Are there any other updates beside these above items?"
  category: additional_probe
  function: scoped_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "Are there any other updates beside these above items?"
  note: "beside these above items" - 범위 좁혀 정중 탐색

- id: m14-018
  expression: "No further updates, you know, I think the team is going to continue their testing"
  category: status_report
  function: negative_report_with_ongoing
  speaker_role: partner
  difficulty: 3
  context: "No further updates, you know, I think the team is going to continue their testing. But there is no new updates."
  note: 부정 보고 + 진행 상태 - "No further updates" + "team is going to continue"

- id: m14-019
  expression: "if you run into an issue, we are going to reach out to you for help"
  category: issue_handling
  function: conditional_request
  speaker_role: partner
  difficulty: 4
  context: "If you run into an issue, we are going to reach out to you for help, or to understand if you're having a problem."
  note: 조건문으로 도움 요청 - "If you run into an issue, we will reach out"

- id: m14-020
  expression: "so far, I haven't had any problems from any of the validation teams"
  category: status_report
  function: clean_status
  speaker_role: partner
  difficulty: 3
  context: "So far, I haven't had any problems from any of the validation teams"
  note: "so far" - 현재까지 이상 없음

# ── 약어 풀이 (Acronym Glossing) ──
- id: m14-021
  expression: "Oh, so it's X (full form). So we have a tool that will Y"
  category: acronym_glossing
  function: full_form_explanation
  speaker_role: partner
  difficulty: 4
  context: "Oh, so it's link disable enable. So we have a tool, right, that will disable the link and re-enable it"
  note: 약어 full form 제시 + 구체적 기능 설명

- id: m14-022
  expression: "we run that test 35,000 times, and every time it should show up as X"
  category: test_description
  function: stress_test_volume
  speaker_role: partner
  difficulty: 4
  context: "we run that test 35,000 times, and every time it should show up as PCIe gen 6 speed and CXL 3.1 and show up in the memory address space"
  note: "35,000 times" - 반복 횟수로 신뢰성 표시

# ── 정중한 질문 (Polite Challenge) ──
- id: m14-023
  expression: "which version you used for the BIOS and BMC?"
  category: version_probe
  function: specific_value_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "which version you used for the BIOS and BMC?"
  note: "what version" 대신 "which version" - 버전이 여러 개일 때

- id: m14-024
  expression: "I would appreciate it if you could provide any concern or other relevant opinions regarding this"
  category: opinion_inquiry
  function: polite_concern_probe
  speaker_role: questioner
  difficulty: 5
  context: "I would appreciate it if you could provide any concern or other relevant opinions regarding this. This means that we want to change the, from Turin to Venice."
  note: "I would appreciate it if you could" - 정중한 의향 탐색 정석

- id: m14-025
  expression: "do you agree that X, is it right?"
  category: agreement_seek
  function: decision_confirmation
  speaker_role: questioner
  difficulty: 3
  context: "do you agree that the changes, the CPU from the Thuring to Venice for this evaluation, is it right?"
  note: 결정 동의 요구 - "do you agree that X is right?"

- id: m14-026
  expression: "Am I correct?"
  category: self_verification
  function: understanding_check
  speaker_role: questioner
  difficulty: 2
  context: "Am I correct?"
  note: 자신의 이해 검증 - 짧은 확인

- id: m14-027
  expression: "Is it right?"
  category: quick_confirm
  function: short_verification
  speaker_role: questioner
  difficulty: 2
  context: "Is it right, Yun-Jeong?"
  note: 발화 검증 - 회의 흐름 끊지 않는 짧은 확인

# ── 이슈 보고 (Issue Report) ──
- id: m14-028
  expression: "when we do X, the link, our link is very unstable. So the system hurts and reboot. So we can't go on the Y"
  category: issue_report
  function: condition_symptom_result
  speaker_role: questioner
  difficulty: 5
  context: "when we do the memory test like GSA in P0 slot, the link, our link is very unstable. So it, the system hurts and reboot. So we can't go on the memory test in P0 slot."
  note: 이슈 보고 3단 구조 - 조건/증상/결과. 디버깅 회의 핵심 화법

- id: m14-029
  expression: "when we run about up to one hour, it, the system reboots"
  category: time_condition
  function: temporal_threshold
  speaker_role: questioner
  difficulty: 4
  context: "when we run about up to one hour, it, the system reboots"
  note: 시간 조건 - "up to one hour"로 시간 임계값

- id: m14-030
  expression: "there is no any BIOS log when system reboots. So it overrides the log"
  category: symptom_detail
  function: missing_evidence
  speaker_role: questioner
  difficulty: 4
  context: "actually there is no, any BIOS log when system reboots. So it overrides the log."
  note: 증상 부연 - 로그 미존재. "overrides the log"로 증상 부연

- id: m14-031
  expression: "are you able to capture a log?"
  category: debug_request
  function: log_request
  speaker_role: partner
  difficulty: 3
  context: "But, um, are you able to capture a log?"
  note: 로그 요구 - "are you able to"로 정중한 요청

# ── 디버깅 정보 요구 (Debug Info Request) ──
- id: m14-032
  expression: "you send me an email on this so we can investigate"
  category: debug_coordination
  function: investigation_request
  speaker_role: partner
  difficulty: 4
  context: "you know, you send me an email on this so we can investigate"
  note: "send me an email so we can investigate" - 디버깅 조율

- id: m14-033
  expression: "do you have any kernel or the BIOS log, even if they don't have any clue or evidence?"
  category: log_request
  function: evidence_request
  speaker_role: partner
  difficulty: 4
  context: "do you have any kernel or the BIOS log, even if they don't have any clue or evidence?"
  note: "even if they don't have any clue" - 단서 없어도 요구

- id: m14-034
  expression: "I need to know X. I need to know Y. I need to know Z"
  category: info_demand
  function: repeated_requirement
  speaker_role: partner
  difficulty: 4
  context: "I need to know the BIOS version. I need to know the BMC version. I need to know what FV, FPGA version you are using. I also need to know how much memory is in the system"
  note: "I need to know" 반복 - 디버깅 정보 직접 요구

- id: m14-035
  expression: "I will check it with our engineers. After checking it, I will let you know, get back to you"
  category: follow_up_promise
  function: check_and_revert
  speaker_role: partner
  difficulty: 3
  context: "I will check it with our engineers. After checking it, I will let you know, get back to you"
  note: "확인 후 회신" 표준 화법 - "check with engineers" + "get back to you"

- id: m14-036
  expression: "we will share the infrastructure environment and the log, what we have, if it is possible"
  category: info_share_promise
  function: conditional_share
  speaker_role: questioner
  difficulty: 3
  context: "we will share the infrastructure environment and the log, what we have, if it is possible"
  note: "if it is possible" 조건부 공유 약속

- id: m14-037
  expression: "is it fully populated or is it? How many memory sticks do you have?"
  category: config_inquiry
  function: population_check
  speaker_role: partner
  difficulty: 3
  context: "Is it fully populated or is it? You know, how many memory sticks do you have?"
  note: 구성 확인 - "fully populated" + "how many sticks"

# ── 플랫폼 전환 (Platform Transition) ──
- id: m14-038
  expression: "we are considering to switch to X, from Y, to proceed with the evaluation"
  category: platform_switch
  function: polite_transition_proposal
  speaker_role: coordinator
  difficulty: 4
  context: "we are considering to switch to Venice, from Turin, to proceed with the evaluation"
  note: 정중한 전환 제안 - "considering to switch"로 여지

- id: m14-039
  expression: "the concerns about the performances differences and due to the limitations of the X, the support for the Y"
  category: technical_justification
  function: reason_for_switch
  speaker_role: coordinator
  difficulty: 4
  context: "the concerns about the performances differences and due to the limitations of the Turin, the support for the DX2, 0, before zero and the PCI Gen 5"
  note: 기술적 이유 제시 - "limitations of X, the support for Y"

- id: m14-040
  expression: "I think it makes sense. I think you've done enough testing on X, right? You probably want to show the new thing"
  category: agreement_with_reason
  function: reasonable_agreement
  speaker_role: partner
  difficulty: 5
  context: "Yeah, I think it makes sense. I think you've done enough testing on Thuring with the CXL 2.0, right? You probably want to show the new thing."
  note: "makes sense" 동의 + 이유 부연. "I agree"보다 전문가적

# ── 일정 협상 (Schedule Negotiation) ──
- id: m14-041
  expression: "it's looking like sometime in May"
  category: vague_schedule
  function: approximate_timing
  speaker_role: partner
  difficulty: 3
  context: "it's looking like sometime in May. Sometime May."
  note: "sometime in X" - 적당히 모호하면서 책임감 있는 일정

- id: m14-042
  expression: "the supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get because of the wafer availability"
  category: supply_constraint
  function: external_attribution
  speaker_role: partner
  difficulty: 5
  context: "the supply constraint is, is pretty bad. So, we just don't have, we are not getting as many CPUs as we were supposed to get because of the way for availability."
  note: 외부 요인 돌리기 - "we were supposed to get"이 핵심 (과거 기대치)

- id: m14-043
  expression: "I don't have a specific date, but it is out about more than a month"
  category: date_evasion
  function: approximate_range
  speaker_role: partner
  difficulty: 4
  context: "I don't have a specific date, but it is out about more than a month"
  note: 정확한 날짜 부인 + 대략 범위 - "about more than a month"

- id: m14-044
  expression: "how many, how many systems do you guys have?"
  category: quantity_inquiry
  function: inventory_check
  speaker_role: partner
  difficulty: 2
  context: "But how many, how many systems do you guys have?"
  note: "you guys" - 비격식 수량 확인

- id: m14-045
  expression: "do I have to buy for your B0 silicon CPU? Is it right?"
  category: cost_inquiry
  function: payment_check
  speaker_role: questioner
  difficulty: 3
  context: "And maybe, do I have to buy for your B0 silicon CPU? Is it right?"
  note: 비용 발생 여부 직접 질문

- id: m14-046
  expression: "No, it's included. Part of the initial CRD"
  category: cost_clarification
  function: inclusion_confirmation
  speaker_role: partner
  difficulty: 3
  context: "No, it's included. Part of the initial CRD, yeah."
  note: 비용 포함 명시 - "part of the initial CRD"

# ── 프로모션 데이터 (Promotion Data) ──
- id: m14-047
  expression: "If we would like to X, is it possible?"
  category: polite_request
  function: conditional_inquiry
  speaker_role: questioner
  difficulty: 4
  context: "If we would like to show and share the data before launch of your Venice, is it possible?"
  note: "If" 조건문으로 감싼 정중한 요청

- id: m14-048
  expression: "No. Yeah, we'll have to wait till after the launch"
  category: polite_refusal
  function: direct_decline
  speaker_role: partner
  difficulty: 3
  context: "No. Yeah, we'll have to wait till after the launch."
  note: 직접 거절 - "No" + "we'll have to wait till after X"

- id: m14-049
  expression: "we don't want to showcase something and then we go back and say, oh, we have to change because we didn't get the best performance the first time"
  category: refusal_justification
  function: reason_for_decline
  speaker_role: partner
  difficulty: 5
  context: "we don't want to showcase something and then we go back and say, oh, we have to change because you know, we did, we didn't get the best performance the first time"
  note: 거절 이유 - "다시 바꿀 수 없다"는 논리

- id: m14-050
  expression: "it's better to provide the best performance the first time"
  category: positive_alternative
  function: quality_priority
  speaker_role: partner
  difficulty: 4
  context: "So, it's better to provide the best performance the first time"
  note: 긍정 대안 - "처음부터 최고로"

- id: m14-051
  expression: "you could do a joint announcement, maybe that might be okay to do, but you would need our legal to approve it"
  category: conditional_alternative
  function: alternative_with_condition
  speaker_role: partner
  difficulty: 5
  context: "Maybe if we were to do something, then, you know, you could do a joint, joint announcement, maybe that might be okay to do, but you would need our legal, MD legal to approve it"
  note: 거절에 대안 제시 - "you could do X, but you would need Y"

- id: m14-052
  expression: "I think we haven't decided yet to which event to be built aim for"
  category: undecided_target
  function: open_schedule
  speaker_role: questioner
  difficulty: 4
  context: "I think we haven't decided yet to which event to be built aim for"
  note: "아직 결정 안 함" - 일정 미확정 표현

# ── 이슈 미보고 포장 (No-News-as-Good-News) ──
- id: m14-053
  expression: "If there is a problem, we'll report it, but we don't usually release any test results for the feature testing"
  category: no_news_framing
  function: negative_as_positive
  speaker_role: partner
  difficulty: 5
  context: "If there is a problem, we'll report it, but we don't usually, we don't release any test results for the feature testing"
  note: "문제 있으면 보고하니, 안 보고되면 이상 없다" - 부정을 긍정으로 재프레이밍

- id: m14-054
  expression: "if it doesn't work, then we're going to call you because you're going to be asking you why something didn't work"
  category: issue_escalation
  function: conditional_contact
  speaker_role: partner
  difficulty: 4
  context: "If it doesn't work, then you know, we're going to call you because you're going to be asking you why something didn't work, right?"
  note: 조건문으로 도움 요청 - "if it doesn't work, we'll call you"

- id: m14-055
  expression: "we're not saying that it's your endpoint, but it's to seek help in terms of understanding what the problem might be"
  category: blame_deflection
  function: non_accusatory_help
  speaker_role: partner
  difficulty: 5
  context: "And then we not saying that it's your endpoint, but it's to seek help in terms of understanding what the problem might be"
  note: 비난 회피 - "we're not saying it's your X, but to seek help"

- id: m14-056
  expression: "your device has been stable and they have not run into any issues"
  category: positive_status
  function: clean_report
  speaker_role: partner
  difficulty: 3
  context: "your, your device has been stable and they have not run into any issues"
  note: 긍정 상태 보고 - "stable" + "not run into any issues"

- id: m14-057
  expression: "Can we do it in the next meeting? We can arrange the quick meeting"
  category: deferral
  function: polite_postponement
  speaker_role: coordinator
  difficulty: 3
  context: "Can we do it in the next meeting? We can arrange the quick meeting. This agenda will be shared in the next meeting with Rita"
  note: 정중한 연기 - "next meeting" + "quick meeting"

- id: m14-058
  expression: "do you have any other things to talk more?"
  category: closing_check
  function: final_round
  speaker_role: coordinator
  difficulty: 2
  context: "Do you have any other things to talk more?"
  note: 회의 마무리 확인 - "any other things to talk more?"

- id: m14-059
  expression: "No, I don't. Let's finish today's meeting"
  category: meeting_close
  function: explicit_close
  speaker_role: partner
  difficulty: 2
  context: "No, I don't. Let's finish today's meeting"
  note: 회의 종료 선언 - "Let's finish today's meeting"

- id: m14-060
  expression: "Thank you for your support and look forward to the collaboration"
  category: closing_compliment
  function: partnership_reaffirmation
  speaker_role: questioner
  difficulty: 3
  context: "Thank you for your support and look forward to the collaboration"
  note: 협력 재확인 - "look forward to the collaboration"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-04-22 08 06 38_EN_AMD-extracted.wav` (총 ~38분, 3,659단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-37) | 샘플 출하 준비 + FOC 협상 + "Let me talk with our VP" 에스컬레이션 | 샘플 협상 + 에스컬레이션 화법 | ★★★ |
| 2 | 가격 불만 (line 38-52) | "you guys keep raising the price" + "this is a partnership, we are not a customer" | 가격 불만 + partnership 프레이밍 | ★★★★ |
| 3 | 평가 결과 (line 53-121) | "Are there any other updates?" + LDE 약어 풀이 + "If there is a problem, we'll report it" 회피 | 정중 탐색 + 이슈 미보고 포장 | ★★★ |
| 4 | 이슈 보고 (line 122-199) | P0 슬롯 리부트 이슈 + "I need to know" 디버깅 정보 요구 | 이슈 보고 3단 구조 + 디버깅 조율 | ★★★★ |
| 5 | 플랫폼 전환 (line 200-335) | Turin->Venice 전환 + B0 5월 + "we'll have to wait till after the launch" 프로모션 거절 | 일정 협상 + 거절 화법 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 2, 4, 5가 가장 가치 높음 - 가격 불만/이슈 보고/거절 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **coordination + negotiation** register다. 샘플/일정/비용을 조율하면서, 가격 불만을 제기하고, 플랫폼 전환을 협상하는 구조. 두 역할 모두 학습해야:
- **SK 코디네이터 역할**: 사전 합의 호소, 정중한 불만, 동의 요구 - 네가 파트너에 요구할 때
- **AMD 담당자 역할**: 부분 승인, 에스컬레이션, 공급 제약 설명, 직접 거절 - 네가 파트너 요구를 처리할 때

### Pragmatics (화용론) 핵심
1. **"partnership, not customer" 프레이밍**: "We are not a customer"로 관계를 재정의하면, 가격 인상·단순 공급 행동을 "파트너십 위반"으로 프레이밍할 수 있다. 이게 협상의 가장 강력한 무기. "고객 취급한다"는 비판은 직접적이지만 "which is not helping"으로 희석.
2. **부분 승인 + 에스컬레이션**: "Some of them I can, but the rest I need to talk with my VP" - 전부 거절하지 않고 일부 승인 후 나머지를 에스컬레이션. 거절을 부드럽게 만드는 핵심 화법. "stay tuned"가 자연스러운 "기다려주세요".
3. **공급 제약 외부화**: "the supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get" - "we were supposed to get" (과거 기대치)이 핵심. "원래 이렇게 받기로 했었다"를 past expectation으로 표현해서 책임을 wafer 가용성으로 돌린다.
4. **"If" 조건문으로 정중 요청**: "If we would like to X, is it possible?" - "We want X"가 아니라 "If we would like to X"로 요청을 조건문으로 감싸면 탐색적 질문이 된다. 거절에도 "you could do X, but you would need Y"로 대안+조건 제시.
5. **이슈 미보고를 긍정으로 포장**: "If there is a problem, we'll report it, but we don't release test results" - 부정(결과 비공개)을 "문제 있으면 보고하니, 안 보고되면 이상 없다"는 긍정 논리로 재프레이밍.

### 네가 당장 써야 할 Top 5
1. **"this is a partnership, right? We are not a customer"** - 관계 재정의. 파트너 협상 핵심 무기
2. **"Let me talk with our VP. And then I will give you my feedback soon. Is it OK for you?"** - 에스컬레이션 정석
3. **"some of them I can shift out as FOC, but the rest I need to talk with my VP"** - 부분 승인 + 에스컬레이션
4. **"it's looking like sometime in May. The supply constraint is pretty bad"** - 일정 모호화 + 외부 요인
5. **"If there is a problem, we'll report it, but we don't release test results"** - 부정을 긍정으로 포장

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "우린 파트너 아닙니까" | "this is a partnership, right? We are not a customer" | 영어는 부정("not a customer")을 먼저, 긍정("partnership")을 나중 |
| "내부 확인 후 회신드리겠습니다" | "Let me talk with our VP and I will give you my feedback soon. Is it OK for you?" | 영어는 구체적 대상(VP) + 시점(soon) + 동의 확인까지 |
| "일부는 가능하고 나머지는 검토하겠습니다" | "some of them I can shift out as FOC, but the rest I need to talk with my VP" | 영어는 에스컬레이션 대상 명시 |
| "5월쯤 가능합니다, 시장 상황이라" | "sometime in May. The supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get" | 영어는 "we were supposed to get"으로 과거 기대치 명시 |
| "이상 없으면 별도 보고 안 합니다" | "If there is a problem, we'll report it, but we don't release test results" | 영어는 "If there is a problem" 조건문으로 긍정 포장 |
| "왜 이렇게 늦리냐" | "the supply constraint is pretty bad. We are not getting as many CPUs as we were supposed to get" | 영어는 비난 회피 - 외부 요인(wafer)으로 돌림 |
| "런칭 전엔 어렵습니다" | "we'll have to wait till after the launch. We don't want to showcase something and then go back and say we have to change" | 영어는 거절 + 이유("다시 바꿀 수 없다") + 긍정 대안("처음부터 최고로") |
| "다음에 합시다" | "Can we do it in the next meeting? We can arrange the quick meeting" | 영어는 제안형 의뢰 - "Can we do it" |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 60개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 4절 샘플 협상·2절 회피 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 분담**: 이 회의는 SK가 "요구하는 쪽"이자 "제공하는 쪽" 양쪽 역할 - 두 관점 모두 연습

---

*Textbook 14 - AMD (CXL 3.1 verification sample, Turin to Venice transition) (2026-04-22). 회의 유형 C (샘플/일정 조정). 표현 DB 60개. 5개 발췌 구간. 작성: 2026-09-01.*
