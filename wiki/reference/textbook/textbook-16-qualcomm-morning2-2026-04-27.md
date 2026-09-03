---
textbook_id: 16
meeting: Qualcomm Morning2 (Mobile DLM Roadmap + LPDDR6 PIM)
date: 2026-04-27
type: B (Roadmap/Supply Alignment)
partner: Qualcomm (CoCom team, Amir, Ben, Michael)
sk_side: SK Hynix Mobile DLM, Application Engineering, NSP team
duration_words: 11080
audio: repo/webex-audio/2026-04-27 11 04 15_EN_Qualcomm_Morning2-extracted.wav
transcript: repo/webex-audio/2026-04-27 11 04 15_EN_Qualcomm_Morning2-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, qualcomm, lpddr6, lpddr5x, pim, mobile, roadmap, supply, alignment, negotiation]
---

# Textbook 16 - Qualcomm Morning2 (2026-04-27)

> **회의 유형**: B (Roadmap/Supply Alignment) - SK Hynix가 메모리 로드맵을 발표하고 Qualcomm이 고객으로서 피드백·정정 요구
> **학습 가치**: 로드맵 정렬 요청, 타임라인 협상, 스펙 푸시백, 공급 제약 프레이밍, 협업 제안
> **Audrey 관점**: 이 회의는 "vendor roadmap pitch + customer pushback + collaboration setup"의 3단 구조. 네가 SK 입장에서 Qualcomm 같은 고객사에 로드맵을 설득할 때, 그리고 고객사 피드백을 정중하게 받아낼 때 모두 쓸 화법이다.

---

## 1. 발화 아키텍처 - SK 발표자의 로드맵 설계 (4단계)

이 회의에서 SK Hynix 발표자는 로드맵 정렬을 위해 **고정된 4단계 구조**로 발표한다. Marvell 회의와 다른 점: 제품 설명이 아니라 **정렬 요청**이 목적. 그래서 "이유 → 제안 → 정렬 요청" 구조가 된다.

### 단계 1: 키 메시지 예고 (Key Message Signaling)

발표자는 "3개의 키 메시지"가 있다고 먼저 선언한다. 이게 로드맵 발표의 첫 뼈대.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Before we get into the details, I'm going to share three key messages with X team` | "Before we get into the details, I'm going to share three key messages with CoCom team" | 구조 예고 - "3개 키 메시지"로 청중 준비 |
| `First one is that we plan to X with our first gen Y by end of this June` | "First one is that we plan to come from the speed extension beyond 10.7 Gbps with our first gen LPC6 by end of this June" | 타임라인 목표 명시 - "by end of this June" |
| `Our second message is that we would like to propose that X stays at Y` | "our second message is that we would like to propose that SM8975 plus which is SM88B75 stays at 12.8 gigabitress for even maximum speed" | 제안 명시 - "we would like to propose that" |
| `Our third message is that we propose to continue X on your Y` | "our third message is that we propose to continue LP 5x support on your 2028 flagship and premium tier" | 제안 명시 - "we propose to continue X on Y" |

**Audrey 교훈**: 로드맵 발표는 "3 key messages"로 시작한다. "Before we get into the details, I'm going to share three key messages" - 이 한 문장이 발표의 방향을 잡는다. 한국어로는 "오늘 3가지 말씀드리겠습니다"인데, 영어는 "three key messages with X team"으로 청중을 명시한다. 그리고 각 메시지를 "First one / Our second message / Our third message"로 번호 매겨. 이 번호 매기기가 로드맵 발표의 기본 뼈대다.

### 단계 2: 근거 제시 (Justification)

제안 후 즉시 "The reason is simple"으로 근거를 연결한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The reason is simple. X is very limited.` | "The reason is simple. LP 6 supply flexibility is very limited." | "The reason is simple" - 근거 도출 공식 |
| `So our mobile products X have to compete with that kind of Y` | "So our mobile products LP 6 have to compete with that kind of server product" | 공급 경합 설명 |
| `And on top of that, this kind of situation is expected to continue through X` | "And on top of that, this kind of situation is expected to continue through 2027" | 지속성 프레이밍 - "expected to continue through X" |
| `So to have this X risk, Y should remain available on Z` | "So to have this LP 6 supply risk, LP 5x memory option should remain available on even on 2028 flagship and premium tier" | 위험 → 대안 요구 연결 |

**Audrey 교훈**: "The reason is simple"은 근거를 시작하는 강력한 공식이다. 복잡한 설명 전에 "The reason is simple. X is very limited."로 핵심을 한 방에 준다. 그리고 "expected to continue through X"로 상황이 일시적이 아님을 강조. 마지막으로 "So to have this X risk, Y should remain available"로 위험 → 대안의 논리를 완성. 이 3단 - 한계 → 지속 → 대안 - 구조를 외워. 공급 제약을 설득할 때 이 뼈대가 필요하다.

### 단계 3: 정렬 요청 (Alignment Request)

근거 후 "we want to align X with Y"로 정렬 요청으로 넘어간다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Based on this confirmation, we want to align X, not only X, but also Y` | "Based on this confirmation, we want to align SM8975, not only SM8975, but also SM8975 on our first gen LPC6" | 정렬 요청 - "not only X, but also Y" 확장 |
| `If there is any opportunity for X, we would like to leave you with the feasibility together in Y` | "If there is any opportunity for higher speed above 10.7 Gbps, even on SM8975, we would like to leave you with the feasibility together in the second half of this year" | 부드러운 푸시 - "leave you with the feasibility together" |
| `If this happens, we believe it will strengthen one of the X value prop over Y` | "we believe it will strengthen one of the LPC6 value prop over the LPC5X" | 가치 제안 강화 - "value prop over Y" |

**Audrey 교훈**: "we want to align X with Y"는 정렬 요청의 기본 공식. 거기에 "not only X, but also Y"를 붙이면 요청 범위가 확장된다 - 정렬을 더 많이 요구하는데 공격적으로 들리지 않는다. 그리고 "we would like to leave you with the feasibility together" - "가능성을 함께 검토해 달라" - 이게 부드러운 푸시의 고급 화법이다. "we want you to do X"가 아니라 "leave you with the feasibility"로 검토 책임을 상대에게 맡기면서도 정렬을 요구한다.

### 단계 4: 협업 제안 (Collaboration Proposal)

회의 후반에는 협업을 제안하는 별도 구조가 나온다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Since like X is the first time technology for you guys and also us, we would like to do some kind of collaboration in the pre-circuit stage` | "Since like PIM is the first day first time technology for you guys and also us for us. We would like to do some kind of collaboration in the pre-circuit stage" | 협업 제안 - "first time technology for both"로 동기 부여 |
| `So what we expect from from you would be X` | "So what we expect from from you would be you can try to use our emulator and integrate into your prototype" | 기대 명시 - "what we expect from you would be" |
| `Let us know what you think.` | "Let us know what you think." | 제안 마무리 - 직접적이면서 열린 질문 |

**Audrey 교훈**: 협업 제안은 "X is first time technology for both of us"로 시작한다 - "둘 다 처음이라 같이 하자"는 동기 부여. 그리고 "what we expect from you would be X"로 구체적 기대를 명시. 마지막 "Let us know what you think."으로 반응을 요청. 이 3단 - 동기 → 기대 → 반응 요청 - 구조를 협업 제안에 써라.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

Type B 회의의 핵심. 로드맵 발표자가 불확실성과 제한을 어떻게 정중하게 포장하는지. 이게 네가 직접 써야 할 화법이다.

### 전략 1: 목표 + 면책 (Target + Disclaimer)

타겟을 말하되 즉시 "to be confirmed"로 면책. 가장 자주 쓰는 패턴.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 12.8 Gbps 타겟 | "to be honest, at this time we are often this big or at least our target is to reach 12.8. **But that's to be confirmed.**" | "솔직히 지금 우리 타겟은 12.8 도달입니다. **하지만 확인 필요합니다.**" |
| PIM 스피드 정정 | "I don't know. For the PIM we're targeting for 12.6. I'm sorry." | "잘 모르겠습니다. PIM은 12.6 타겟입니다. 죄송합니다." - 즉시 정정 |
| 검증 미확정 | "I'm not double confirmed and I'm going to update it. So the weekly, the five weekly meeting." | "이중 확인은 안 됐고 업데이트하겠습니다. 주간 미팅에서." |

**패턴 공식**: `Our target is to reach X. But that's to be confirmed. I'm not double confirmed and I'm going to update it.`

**Audrey 교훈**: 로드맵 발표에서 "확정"은 위험하다. "Our target is X. But that's to be confirmed." - 타겟은 말하되 "to be confirmed"로 면책. 이게 로드맵 발표자의 기본 자세다. 그리고 "I'm not double confirmed"로 더 강하게 면책할 수도 있다. 한국어 "검토 중입니다"의 영어 버전이 "that's to be confirmed"다. 절대 "we will do X"라고 단언하지 마라 - "our target is X, but to be confirmed"로 포장.

### 전략 2: 딜레마 공개 (Dilemma Disclosure)

제한을 "우리의 선택"이 아니라 "시장 상황의 딜레마"로 프레이밍.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 24 vs 48 gigabit 선택 | "we have honestly, we have some dilemma now because the market is very shorty. So the price is going up continuously." | "솔직히 지금 딜레마가 있습니다. 시장이 매우 불안정해서 가격이 계속 오르고 있어서." |
| NVIDIA 내부 논의 | "So even NVIDIA has some internal discussion, whether they can use 48 gigabyte based like 768 gigabyte solution. So we are worrying about that." | "그래서 NVIDIA도 내부 논의 중입니다, 48GB 기반 768GB 솔루션 쓸지. 걱정입니다." |
| 프로젝트 드롭 가능성 | "They may drop this 48 gigabyte based product project. So we are still under discussion how to manage this, our 24 and 48 gigabyte." | "48GB 기반 프로젝트를 드롭할 수도 있습니다. 그래서 24와 48 관리 방법 논의 중입니다." |

**패턴 공식**: `We have some dilemma now because the market is X. So even Y has internal discussion. They may drop Z. We are still under discussion how to manage this.`

**Audrey 교훈**: "우리가 안 합니다"가 아니라 "딜레마가 있습니다"로 프레이밍. "We have some dilemma now because X" - 이게 제한을 시장 탓으로 돌리는 화법이다. 그리고 "even NVIDIA has internal discussion"으로 업계 리더도 같은 고민이라는 점을 끌어들여 정당화. 한국어 "시장 상황이 안 좋아서요"의 영어 버전이 "we have some dilemma now because the market is very shorty"다. "shorty"는 비표준적이지만 회의에서 쓰인 표현 - 실제로는 "volatile"이 더 자연스럽다.

### 전략 3: 우선순위 프레이밍 (Priority Framing)

지연을 "우선순위 문제"로 프레이밍. "안 합니다"가 아니라 "더 중요한 게 있습니다".

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| LP5x CS 지연 | "generally, I think that's the spring of this delay. And we go, editor, priority, better event. The customer demand is the most higher priority." | "일반적으로 이 지연의 이유는요, 우선순위입니다. 고객 수요가 더 높은 우선순위입니다." |
| LP6 not highest priority | "we will be working on LP6 as well. We are not going to give it up on this because there might be some designs coming up later on. But it's just not the highest priority." | "LP6도 작업합니다. 포기 안 합니다, 나중에 디자인 나올 수 있으니까. 다만 최우선은 아닙니다." |
| SoC 5HPM 경합 | "Because participation, the efficiency is being off. Many these tools is more prioritized at the 5F now." | "참여, 효율이 떨어지고 있어서요. 5F 쪽이 더 우선순위입니다." |

**패턴 공식**: `We will be working on X as well. We are not going to give it up. But it's just not the highest priority.`

**Audrey 교훈**: "우리가 안 합니다" 대신 "최우선이 아닐 뿐"으로 포장. "We are not going to give it up on this. But it's just not the highest priority." - 포기는 안 하되 우선순위가 아님을 명시. 이게 정중한 지연 설명이다. "No"를 안 하면서 "Not now"를 하는 화법. 한국어 "지금은 좀 어렵습니다"의 영어 버전이 "it's just not the highest priority"다.

### 전략 4: 데이터 부족 미루기 (Insufficient Data Deferral)

결정을 "데이터 더 필요"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 데이터센터 PIM 스펙 | "we do not see immediate need for the spec development or that profile right now. So we need to have some more internal review inside the timeline." | "지금 스펙 개발이나 프로필의 즉각적 필요는 안 보입니다. 타임라인 내 더 내부 검토가 필요합니다." |
| 부동소수점 결정 | "So for data center, we probably have to go to floating point. We can do the respective element, but I'm not so sure about the product side." | "데이터센터는 부동소수점으로 가야 할 겁니다. 제품 쪽은 확신이 없습니다." |
| 로해머 패턴 미확정 | "But we'll need to see. We'll need to see if there is a unique Rohammer patterns in different applications." | "더 봐야 합니다. 다른 애플리케이션에 고유한 RowHammer 패턴이 있는지." |

**패턴 공식**: `We do not see immediate need for X right now. We need to have some more internal review. We'll need to see if there is Y.`

**Audrey 교훈**: "We do not see immediate need for X right now" - "지금 당장 X 필요성을 못 봅니다" - 이게 정중한 미루기다. 거기에 "We need to have some more internal review"로 내부 검토 핑계. 한국어 "좀 더 검토해 보겠습니다"의 영어 버전. "We'll need to see"를 반복 사용하면 더 강한 미루기가 된다 - "We'll need to see. We'll need to see if there is Y." 반복이 망설임을 전달.

### 전략 5: Not Finalized Yet (Hedged Confirmation)

확정은 아니지만 현재는 yes - 미래 변경 여지를 열어둔다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 24GB 다이 계획 | "So we have 24 gigabit DAI planned in 29 time frame." | "24Gb 다이는 29 타임프레임에 계획되어 있습니다." |
| 확정 아님 | "Not finalized yet, but yes, at this point, yes." | "최종 확정은 아니지만, 현 시점에서는 yes." |
| 1D 기반 48Gb 모바일 불가 | "The die size of it too large to fit in this Pekizehite." | "다이 사이즈가 패키지 Z-height에 맞추기엔 너무 큽니다." - 물리적 한계로 단정 |

**패턴 공식**: `Not finalized yet, but yes, at this point, yes.`

**Audrey 교훈**: "Not finalized yet, but yes, at this point, yes." - 이게 로드맵 발표자의 핵심 회피 화법이다. "Yes"를 두 번 반복하면서도 "Not finalized"로 빠져나갈 길을 만든다. 한국어 "현재로선 그렇습니다"와 같은 뉘앙스. 절대 "We will do it"이라고 단언하지 마라 - "at this point, yes"로 시간 한정.

---

## 3. 정중한 도전 화법 (Qualcomm 측 고객)

Qualcomm이 SK Hynix 로드맵에 정중하게 도전하는 패턴. **네가 고객사 입장에서 파트너를 밀어붙일 때** 써야 할 화법이다.

### 질문 유형 1: 고객 수요 검증 (Customer Demand Validation)

제안의 시장성을 직접 묻는 도전.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So given that, do you guys see a customer, a mutual customer that is going to ask for it?` | "So given that, do you guys see a customer, a mutual customer that is going to ask for it?" | "고객이 있습니까?" - 공동 고객 존재 여부로 도전 |
| `For you guys to request an alignment on that, do you guys see somebody that is interested in it?` | "For you guys to request an alignment on that, do you guys see somebody that is interested in it?" | "관심 있는 사람 봅니까?" - 정렬 요청의 근거 검증 |
| `Not even just X, but just at even Y, right?` | "Not even just 8975, 10.7 plus, but just at even 10.7, 5.3 wages, right?" | 범위 확장 - "그것뿐 아니라 X도요" |

**Audrey 교훈**: "do you guys see a customer that is going to ask for it?" - 이게 고객 입장에서 가장 강력한 도전이다. 제안의 현실성을 시장 수요로 검증. "관심 있습니까?"가 아니라 "고객을 봅니까?"로 밀어붙인다. 네가 파트너 제안을 평가할 때, "is there a customer for this?"를 물어봐라 - 가장 날카로운 정중 도전이다.

### 질문 유형 2: 스펙 푸시백 (Spec Pushback)

스펙 제안에 대해 "이 정도 차이면 안 됩니다"로 밀어붙이기.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think in order for it to work even though it's very small delta there has to be no delta` | "I think in order for it to work even though it's very small delta there has to be no delta" | "작은 차이도 차이면 안 됩니다" - 정밀 스펙 요구 |
| `Even if it's like one or two percent that'll just throw people over because now they have seen like X going to Y` | "Even if it's like one or two percent that'll just throw people over because now they have seen like LP 5x going to 100x" | "1-2% 차이도 고객 이탈시킵니다" - 민감도 경고 |
| `We might just kill it all together is what I'm saying.` | "We might just kill it all together is what I'm saying." | "전체를 죽일 수도 있습니다" - 극단 경고 |
| `But it's already super pricing on the memory supply itself. So you got to be mindful of that.` | "But it's already super pricing on the memory supply itself. So you got to be mindful of that." | "가격 이미 높으니 주의하세요" - 시장 경고 |

**Audrey 교훈**: "in order for it to work, there has to be no delta" - "작동하려면 차이가 없어야 합니다" - 이게 스펙 푸시백의 정수. "조금 차이 나도 괜찮다"가 아니라 "no delta"로 밀어붙인다. 그리고 "kill it all together" - "전체를 죽일 수도 있다" - 극단적 표현으로 심각성 전달. 한국어 "조금만 차이 나도 안 됩니다"의 영어 버전. "you got to be mindful of that" - "주의해야 합니다" - 부드러운 경고로 마무리.

### 질문 유형 3: 놓친 세그먼트 지적 (Missed Segment Callout)

로드맵의 빈 구멍을 직접 지적.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `in my mind, you missed the main segment of 12 gigabyte` | "in my mind, you missed the main segment of 12 gigabyte" | "주요 세그먼트를 놓쳤습니다" - 직접 지적 |
| `I think you overlooked that we needed 12 gigabyte right now` | "I think you overlooked that we needed 12 gigabyte right now" | "지금 12GB 필요한 거 놓치셨습니다" - 시점 강조 |
| `That's also a good point.` | "That's also a good point." (SK 측 수용) | 상대 인정 - "good point" |

**Audrey 교훈**: "you missed the main segment of X" - "X 메인 세그먼트를 놓쳤다" - 직접적이면서도 "in my mind"로 겸손하게. "I think you overlooked that we needed X right now" - "지금 X 필요한 거 놓치셨다" - "overlooked"가 실수를 정중하게 지적하는 단어. "You forgot"가 아니라 "you overlooked"이 전문가 화법. 그리고 상대가 수용하면 "That's also a good point"로 인정해라 - 양쪽 다 이 화법을 써.

### 질문 유형 4: 강한 부정 (Strong Denial)

확실한 "No"를 요구할 때.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is there any possibility that my later client decides to support the QCX or the QCX?` | "Is there any possibility that my later client decides to support the QCX or the QCX?" | 가능성 탐색 |
| `Absolutely not.` | "Absolutely not." (SK 응답) | "절대 없습니다" - 강한 부정 |

**Audrey 교훈**: "Absolutely not." - 이 회의에서 SK 측이 가장 강하게 부정한 답. "No"보다 강하다. 가능성을 완전히 차단할 때만 써라. 일반적인 "No"는 "I don't think so"로 부드럽게, "절대 안 됩니다"는 "Absolutely not"으로. 둘 다 외워.

### 질문 유형 5: 시간배열 검증 (Timeline Cadence Check)

로드맵 타임라인의 현실성을 따지는 질문.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So usually your cadences that we get parts by September of the previous year` | "So usually your cadences that we get parts by September of the previous year" | 관행 명시 - "보통 9월에 받습니다" |
| `anything later than that jeopardize the program in general` | "anything later than that jeopardize the program in general. So that you guys know." | "그보다 늦으면 프로그램 위태롭습니다" - 경고 |
| `So generally, can we expect like one quarter ahead of the CS timeline? It will be ES availability` | "So generally, can we expect like one quarter ahead of the CS timeline? It will be ES availability or more than one quarter?" | 샘플 타이밍 확인 - "한 분기 앞서나요?" |

**Audrey 교훈**: "anything later than that jeopardize the program in general" - "그보다 늦으면 프로그램이 위태로워집니다" - 이게 타임라인 압박의 공식. "jeopardize"가 핵심 동사. "늦으면 안 됩니다"가 아니라 "jeopardize the program"으로 위험을 명시. 그리고 "So that you guys know"로 정보 공유의 의도를 표시 - 공격이 아니라 알림이라는 프레이밍. 타임라인을 밀어붙일 때 "X jeopardize Y"를 써라.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

**Type B 회의의 핵심**. 타임라인 타겟, 볼륨 요청, 스펙 푸시백, 마일스톤 조정의 언어.

### 4.1 타임라인 타겟 언어 (Timeline Targets)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 타겟 명시 | SK | "we plan to come from the speed extension beyond 10.7 Gbps with our first gen LPC6 by end of this June" | "by end of this June" - 명확한 시점 |
| 정렬 요청 | SK | "Based on this confirmation, we want to align SM8975 on our first gen LPC6" | "Based on this confirmation" - 확인 후 정렬 |
| 제안 | SK | "we propose to continue LP 5x support on your 2028 flagship and premium tier" | "we propose to continue X on Y" |
| 미래 가능성 | SK | "we would like to leave you with the feasibility together in the second half of this year" | "leave you with the feasibility" - 부드러운 푸시 |
| 타겟 유지 | SK | "we propose that SM8975 plus which is SM88B75 stays at 12.8 gigabitress" | "stays at X" - 현재 상태 유지 제안 |
| 가용 시점 | SK | "our LP 6x 14.4 for mobile product is expected to be available in the first half of 2029 timeframe" | "expected to be available in X" - 예상 |
| 타겟 속도 | SK | "we're targeting for 12.6" | "targeting for X" - 타겟 표시 |
| ES vs CS | SK | "ES sample maybe two months earlier than CS sample. Two months." | "two months earlier than X" - 샘플 간격 |

### 4.2 볼륨/샘플 요청 언어 (Volume/Sample Requests)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 밀리석 조정 요구 | QC | "So if we miss that timeline, we can push it back a couple of months" | "push it back a couple of months" - 유예 요청 |
| CS 타임라인 | QC | "So generally, can we expect like one quarter ahead of the CS timeline?" | "can we expect X ahead of Y" - 기대 확인 |
| working sample 정의 | QC | "So what's the process in between?" | 프로세스 질문 |
| WS vs ES 구분 | QC | "And then what's your notion for the working sample versus ES sample?" | "notion for X versus Y" - 구분 요청 |
| 밀리석 캐던스 | QC | "So we have shared our cadences year over year to align parts." | "cadences year over year" - 관행 설명 |
| 밀리석 위험 | QC | "anything later than that jeopardize the program in general" | "jeopardize the program" - 위험 경고 |

### 4.3 스펙 푸시백 언어 (Spec Pushback)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 차이 허용 불가 | QC | "even though it's very small delta there has to be no delta" | "no delta" - 정밀 요구 |
| 자화자살 경고 | QC | "We might just kill it all together is what I'm saying." | "kill it all together" - 극단 경고 |
| 비교 무효화 | QC | "I think that just pales in comparison to the overall LP D6 pricing scheme" | "pales in comparison to X" - 비교 약화 |
| 가격 경고 | QC | "But it's already super pricing on the memory supply itself. So you got to be mindful of that." | "you got to be mindful of that" - 부드러운 경고 |
| 시장 궤적 | QC | "Given the way the market trajectory is happening for a price in person." | "market trajectory" - 시장 흐름 인용 |
| 과거 사례 | QC | "we've not seen that trend looking at LP 5x you know history" | "we've not seen that trend" - 전례 부재 |

### 4.4 마일스톤 조정 언어 (Milestone Coordination)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 제안 인지 | QC | "Point noted." | "Point noted" - 간결한 인지 |
| 가치 인정 | QC | "We can understand the value proposition." | "understand the value proposition" - 가치 인정 |
| 미확정 표시 | QC | "I think that was our original plan and we are not locked on to 14.4 yet" | "not locked on to X yet" - 미확정 |
| 제안 성격 | QC | "It's just a proposal that we're thinking along those lines." | "along those lines" - 방향성 표시 |
| 조건부 추론 | QC | "So if the price is stabilized towards the end of 47, then 28 designs would see a lot more LP6 attachment" | "if X, then Y" - 조건부 예측 |
| 정렬 의존 | QC | "we will have to of course align with you guys on that as to what you're seeing" | "align with you guys on that" - 정렬 의존 |

### 4.5 협업 액션 (Collaboration Action Items)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 협업 제안 | SK | "we would like to do some kind of collaboration in the pre-circuit stage" | "in the pre-circuit stage" - 단계 명시 |
| 기대 명시 | SK | "what we expect from you would be you can try to use our emulator" | "what we expect from you would be X" - 기대 명시 |
| 엔지니어 파견 | SK | "we can dispatch our engineer to your lab on site" | "dispatch our engineer to your lab" - 파견 제안 |
| 회의 빈도 | SK | "we can do like a regular meeting not like aside from XR" | "regular meeting aside from X" - 별도 회의 |
| 제안 마무리 | SK | "Let us know what you think." | "Let us know what you think" - 반응 요청 |
| 검토 약속 | QC | "I'm sure we will take a look at this and we'll get back" | "take a look and get back" - 검토 약속 |
| 협업 가치 | QC | "certainly seems useful for us to collaborate" | "seems useful for us to collaborate" - 가치 인정 |
| 순서 명시 | QC | "the first step for us. Yeah. Once we finish that you know and we just doing the validation then we can jump into this." | "first step for us" - 순서 명시 |
| 1:1 제안 | QC | "we can set up like some one on one meeting can share details with each other" | "one on one meeting can share details" - 1:1 제안 |
| 항상 열림 | QC | "we are always open for that" | "always open for that" - 개방성 표시 |

### 4.6 입력 수용 언어 (Input Internalization)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 입력 수용 | QC | "So thanks for sharing that. We'll take that. We'll internalize that." | "internalize that" - 내재화 표시 |
| 검토 약속 | QC | "We'll take it back and discuss it with the validation team" | "take it back and discuss with X" - 검토 약속 |
| 데이터 요청 | QC | "So there's some additional data that you can share with us that will help us in our decision" | "help us in our decision" - 의사결정 지원 |
| 고려 표시 | QC | "That's something that we could consider." | "could consider" - 고려 표시 |
| 의견 요청 | SK | "this is again, an area where we would like your opinion and your insight on" | "would like your opinion and your insight on" - 의견 요청 |

**Audrey 교훈**: Type B 회의에서 가장 중요한 액션 화법:
1. **"Point noted."** - 제안을 인지하는 가장 간결한 표현. 한국어 "알겠습니다"보다 훨씬 프로다.
2. **"We'll take that. We'll internalize that."** - 입력을 받아들인다는 강한 표시. "internalize"가 단순 "understand"보다 깊이 있음.
3. **"We are always open for that."** - 협업 의사 표시. "we can"이 아니라 "always open"이 더 강하다.
4. **"the first step for us"** - 순서를 명시할 때. "지금 당장"이 아니라 "첫 단계로"로 밀어붙이는 화법.
5. **"We'll need to see."** - 결정 미루기 반복. 두 번 쓰면 강한 미루기.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 LPDDR6/모바일/패키징 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **LP5X / LP6** | LPDDR5X / LPDDR6 (모바일 DRAM 세대) | "we propose to continue LP 5x support on your 2028 flagship" - 세대 전환 논의 핵심 |
| **SM8975 / SM8975+ / 8B75** | Qualcomm Snapdragon SoC 코드명 | "we propose that SM8975 plus which is SM88B75 stays at 12.8 gigabitress" - SoC-메모리 정렬 |
| **1C / 1C9 / 1D** | DRAM 공정 노드 (1xCnm, 1x.D nm) | "our LP 6 product is built on one C9 for both first gen and the second gen" - 공정 노드 |
| **5HPM** | 5세대 High Performance Memory (HBM) | "server oriented products like either 5HPM, LP 5x SOCAM" - 서버 메모리 |
| **CS (Customer Sample)** | 고객 샘플 - 양산 전 단계 | "ES sample maybe two months earlier than CS sample" - ES vs CS 간격 |
| **ES (Engineering Sample)** | 엔지니어링 샘플 - 초기 검증용 | "the oldest ES will be two months earlier than the CS sample" |
| **working sample** | 동작 샘플 - 첫 실리콘 기반 | "for walking sample, based on false silicon, we can usually make the working sample" - "false silicon"은 transcribe 오류 (first silicon) |
| **bring up** | 하드웨어 초기 구동 검증 | "we are going to continue with LP6. Bring up because we need that for our chip as well" |
| **POR (Plan of Record)** | 공식 계획 | "then we missed all the POR validations" - 공식 검증 일정 |
| **PIM (Processing In Memory)** | 메모리 내장 처리 | "we are going to move on to QCX Pim agenda" - PIM 로드맵 |
| **JEDEC** | 반도체 표준화 기구 | "we really want to start data centers over profile discussion in JEDEC" - 스펙 표준화 |
| **VDDQ / VFS** | 전압 / 전압-주파수 스케일링 | "3D 2C level can be used at 1.0V at up to 5.3 GHz, meaning the VFS H is not required" |
| **WCK** | 클럭 신호 (LPDDR) | "WCK buffer is linked to WCK frequency mode" - WCK 모드 |
| **PABT** | (PDABT) Pre-Amble Active Time | "the direct effect for PDABT is 256, but our first 10 APC 6 can relax up to 512" - 타이밍 완화 |
| **RowHammer** | DRAM 보안 취약점 | "there will be no legacy Rohammer mitigations. Only PREC" - RowHammer 완화 |
| **PREC** | (Pseudo Refresh for RowHammer) | "We're relying on PREC protocol" - 새 완화 방식 |
| **Z-height** | 패키지 두께 | "Z-Hide is smaller than before" - Z-height (transcription: Z-Hide) |
| **COP / SiP** | Chip-on-PCB / System-in-Package | "50 COV, the other market, your local market is of the side by side set" - 패키지 형태 |
| **Pop / discrete** | Package-on-Package / 개별 패키지 | "your pure part selection right for 16 gigabyte" - PoP 선택 |
| **563 board** | 5.6.3 채널 패키지 | "we have some slides on the 563 board" - 6채널 패키지 |
| **518 ball** | 5x18 볼 패키지 | "518 ball Pekizehite, fitting is not feasible" - 볼 배열 |
| **value prop** | 가치 제안 | "it will strengthen one of the LPC6 value prop over the LPC5X" |
| **cadences** | 제품 출시 주기 | "we have shared our cadences year over year to align parts" |
| **exclusive / exclusivity** | 독점성 | "unless we have a mutual customer that we can work with for exclusivity" |
| **delta** | 차이 (스펙 차이) | "even though it's very small delta there has to be no delta" |
| **SOCAM** | SoC + Memory (통합) | "192 gigabyte SOCAM actually is a sweet spot for us" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m16-001
  expression: "Before we get into the details, I'm going to share three key messages with X team"
  category: structure_signaling
  function: agenda_preview
  speaker_role: presenter
  difficulty: 4
  context: "Before we get into the details, I'm going to share three key messages with CoCom team"
  note: 로드맵 발표의 시작 공식. "3 key messages"로 청중 준비.

- id: m16-002
  expression: "First one is that we plan to X with our first gen Y by end of this June"
  category: timeline_target
  function: target_with_deadline
  speaker_role: presenter
  difficulty: 4
  context: "First one is that we plan to come from the speed extension beyond 10.7 Gbps with our first gen LPC6 by end of this June"
  note: 타임라인 타겟 - "by end of this June" 명확한 시점.

- id: m16-003
  expression: "Based on this confirmation, we want to align X, not only X, but also Y"
  category: alignment_request
  function: scope_expansion
  speaker_role: presenter
  difficulty: 5
  context: "Based on this confirmation, we want to align SM8975, not only SM8975, but also SM8975 on our first gen LPC6"
  note: "not only X, but also Y"로 정렬 요청 확장.

- id: m16-004
  expression: "If there is any opportunity for X, we would like to leave you with the feasibility together in Y"
  category: soft_push
  function: feasibility_request
  speaker_role: presenter
  difficulty: 5
  context: "If there is any opportunity for higher speed above 10.7 Gbps, even on SM8975, we would like to leave you with the feasibility together in the second half of this year"
  note: "leave you with the feasibility together" - 부드러운 푸시 고급 화법.

- id: m16-005
  expression: "If this happens, we believe it will strengthen one of the X value prop over Y"
  category: value_proposition
  function: benefit_framing
  speaker_role: presenter
  difficulty: 4
  context: "we believe it will strengthen one of the LPC6 value prop over the LPC5X"

- id: m16-006
  expression: "Our second message is that we would like to propose that X stays at Y"
  category: proposal_stating
  function: status_proposal
  speaker_role: presenter
  difficulty: 4
  context: "our second message is that we would like to propose that SM8975 plus which is SM88B75 stays at 12.8 gigabitress for even maximum speed"

- id: m16-007
  expression: "Our third message is that we propose to continue X on your Y"
  category: proposal_stating
  function: continuation_proposal
  speaker_role: presenter
  difficulty: 4
  context: "our third message is that we propose to continue LP 5x support on your 2028 flagship and premium tier"

- id: m16-008
  expression: "The reason is simple. X is very limited."
  category: justification
  function: direct_reasoning
  speaker_role: presenter
  difficulty: 4
  context: "The reason is simple. LP 6 supply flexibility is very limited."
  note: "The reason is simple" - 근거 도출 공식. 핵심 한 방.

- id: m16-009
  expression: "this kind of situation is expected to continue through X"
  category: duration_framing
  function: persistence_stating
  speaker_role: presenter
  difficulty: 3
  context: "this kind of situation is expected to continue through 2027"

- id: m16-010
  expression: "So to have this X risk, Y should remain available on Z"
  category: risk_alternative
  function: risk_to_solution
  speaker_role: presenter
  difficulty: 4
  context: "So to have this LP 6 supply risk, LP 5x memory option should remain available on even on 2028 flagship and premium tier"

- id: m16-011
  expression: "So this is our roadmap plans."
  category: conclusion
  function: roadmap_close
  speaker_role: presenter
  difficulty: 2
  context: "That is our roadmap plans."

# ── 회피·포장 (Hedging & Deflection) ──
- id: m16-012
  expression: "Our target is to reach X. But that's to be confirmed."
  category: target_disclaimer
  function: target_with_hedge
  speaker_role: presenter
  difficulty: 5
  context: "at least our target is to reach 12.8. But that's to be confirmed."
  note: 로드맵 발표의 핵심 회피. 타겟 + "to be confirmed".

- id: m16-013
  expression: "I'm not double confirmed and I'm going to update it"
  category: correction_hedge
  function: uncertainty_acknowledgment
  speaker_role: presenter
  difficulty: 4
  context: "I'm not double confirmed and I'm going to update it. So the weekly, the five weekly meeting."

- id: m16-014
  expression: "We have honestly, we have some dilemma now because the market is very X"
  category: dilemma_disclosure
  function: market_blame
  speaker_role: presenter
  difficulty: 5
  context: "we have honestly, we have some dilemma now because the market is very shorty. So the price is going up continuously."
  note: 제한을 "시장 딜레마"로 프레이밍. "shorty"는 비표준 (volatile 권장).

- id: m16-015
  expression: "We are not going to give it up on this. But it's just not the highest priority."
  category: priority_framing
  function: polite_delay
  speaker_role: presenter
  difficulty: 5
  context: "We are not going to give it up on this because there might be some designs coming up later on. But it's just not the highest priority."
  note: "No" 대신 "not highest priority" - 정중한 지연.

- id: m16-016
  expression: "We do not see immediate need for X right now"
  category: soft_deferral
  function: polite_no
  speaker_role: presenter
  difficulty: 4
  context: "we do not see immediate need for the spec development or that profile right now"

- id: m16-017
  expression: "We need to have some more internal review inside the timeline"
  category: internal_review
  function: delay_with_reason
  speaker_role: presenter
  difficulty: 3
  context: "So we need to have some more internal review inside the timeline"

- id: m16-018
  expression: "Not finalized yet, but yes, at this point, yes."
  category: hedged_confirmation
  function: temporal_yes
  speaker_role: presenter
  difficulty: 4
  context: "Not finalized yet, but yes, at this point, yes."
  note: "at this point, yes" - 시간 한정 yes.

- id: m16-019
  expression: "But it's to be confirmed. We need more detailed studies."
  category: disclaimer_repeat
  function: uncertainty_emphasis
  speaker_role: presenter
  difficulty: 3
  context: "But it's to be confirmed. We need more detailed studies."

- id: m16-020
  expression: "We'll need to see if there is X in Y"
  category: future_seeing
  function: deferred_decision
  speaker_role: presenter
  difficulty: 3
  context: "We'll need to see if there is a unique Rohammer patterns in different applications"

# ── 정중한 도전 (Polite Challenge) ──
- id: m16-021
  expression: "So given that, do you guys see a customer, a mutual customer that is going to ask for it?"
  category: demand_validation
  function: market_reality_check
  speaker_role: questioner
  difficulty: 5
  context: "So given that, do you guys see a customer, a mutual customer that is going to ask for it?"
  note: 고객 수요로 제안 검증 - 가장 강력한 정중 도전.

- id: m16-022
  expression: "For you guys to request an alignment on that, do you guys see somebody that is interested in it?"
  category: interest_check
  function: alignment_justification
  speaker_role: questioner
  difficulty: 4
  context: "For you guys to request an alignment on that, do you guys see somebody that is interested in it?"

- id: m16-023
  expression: "in order for it to work even though it's very small delta there has to be no delta"
  category: spec_pushback
  function: precision_demand
  speaker_role: questioner
  difficulty: 5
  context: "I think in order for it to work even though it's very small delta there has to be no delta"
  note: "no delta" - 정밀 스펙 요구 공식.

- id: m16-024
  expression: "We might just kill it all together is what I'm saying."
  category: extreme_warning
  function: program_risk
  speaker_role: questioner
  difficulty: 4
  context: "We might just kill it all together is what I'm saying."

- id: m16-025
  expression: "But it's already super pricing on the memory supply itself. So you got to be mindful of that."
  category: market_warning
  function: price_caution
  speaker_role: questioner
  difficulty: 4
  context: "But it's already super pricing on the memory supply itself. So you got to be mindful of that."

- id: m16-026
  expression: "I think that just pales in comparison to X"
  category: comparison_dilution
  function: argument_weakening
  speaker_role: questioner
  difficulty: 4
  context: "I think that just pales in comparison to the overall LP D6 pricing scheme right that the pricing the price premium"
  note: "pales in comparison to X" - 상대 인자 약화.

- id: m16-027
  expression: "we've not seen that trend looking at X history"
  category: precedent_absence
  function: pattern_challenge
  speaker_role: questioner
  difficulty: 4
  context: "we've not seen that trend looking at LP 5x you know history"

- id: m16-028
  expression: "in my mind, you missed the main segment of X"
  category: gap_callout
  function: oversight_direct
  speaker_role: questioner
  difficulty: 5
  context: "in my mind, you missed the main segment of 12 gigabyte"

- id: m16-029
  expression: "I think you overlooked that we needed X right now"
  category: oversight_callout
  function: timing_emphasis
  speaker_role: questioner
  difficulty: 5
  context: "I think you overlooked that we needed 12 gigabyte right now"
  note: "overlooked" - 정중한 실수 지적.

- id: m16-030
  expression: "Absolutely not."
  category: strong_denial
  function: absolute_no
  speaker_role: questioner
  difficulty: 2
  context: "Is there any possibility that my later client decides to support the QCX? Absolutely not."

- id: m16-031
  expression: "anything later than that jeopardize the program in general"
  category: timeline_warning
  function: risk_explicit
  speaker_role: questioner
  difficulty: 5
  context: "anything later than that jeopardize the program in general. So that you guys know."
  note: "jeopardize the program" - 타임라인 압박 공식.

- id: m16-032
  expression: "So that you guys know."
  category: information_framing
  function: non_aggressive_warning
  speaker_role: questioner
  difficulty: 3
  context: "anything later than that jeopardize the program in general. So that you guys know."

# ── 협상·액션 (Negotiation) ──
- id: m16-033
  expression: "Point noted."
  category: acknowledgment
  function: concise_acceptance
  speaker_role: questioner
  difficulty: 2
  context: "Point noted."
  note: 간결한 인지 - "알겠습니다"보다 프로.

- id: m16-034
  expression: "We can understand the value proposition."
  category: value_acknowledgment
  function: validation
  speaker_role: questioner
  difficulty: 3
  context: "So that is 28. We can understand the value proposition."

- id: m16-035
  expression: "I think that was our original plan and we are not locked on to X yet"
  category: not_committed
  function: openness_signaling
  speaker_role: questioner
  difficulty: 4
  context: "I think that was our original plan and we are not locked on to 14.4 yet"

- id: m16-036
  expression: "It's just a proposal that we're thinking along those lines."
  category: directional_proposal
  function: thinking_state
  speaker_role: questioner
  difficulty: 4
  context: "It's just a proposal that we're thinking along those lines."

- id: m16-037
  expression: "if the price is stabilized towards the end of X, then Y designs would see a lot more Z"
  category: conditional_prediction
  function: market_conditional
  speaker_role: questioner
  difficulty: 4
  context: "So if the price is stabilized towards the end of 47, then 28 designs would see a lot more LP6 attachment"

- id: m16-038
  expression: "we will have to of course align with you guys on that as to what you're seeing"
  category: alignment_dependency
  function: coordination
  speaker_role: questioner
  difficulty: 3
  context: "we will have to of course align with you guys on that as to what you're seeing"

- id: m16-039
  expression: "we can expect like one quarter ahead of the X timeline"
  category: timeline_query
  function: cadence_check
  speaker_role: questioner
  difficulty: 3
  context: "So generally, can we expect like one quarter ahead of the CS timeline?"

- id: m16-040
  expression: "ES sample maybe two months earlier than CS sample"
  category: sample_timing
  function: gap_stating
  speaker_role: presenter
  difficulty: 3
  context: "ES sample maybe two months earlier than CS sample. Two months."

- id: m16-041
  expression: "So thanks for sharing that. We'll take that. We'll internalize that."
  category: input_internalization
  function: deep_acceptance
  speaker_role: questioner
  difficulty: 4
  context: "So thanks for sharing that. We'll take that. We'll internalize that."
  note: "internalize that" - 깊은 수용 표시.

- id: m16-042
  expression: "We'll take it back and discuss it with the X team"
  category: review_commitment
  function: follow_up_promise
  speaker_role: questioner
  difficulty: 3
  context: "We'll take it back and discuss it with the validation team"

- id: m16-043
  expression: "That's something that we could consider."
  category: soft_openness
  function: consideration_signal
  speaker_role: questioner
  difficulty: 3
  context: "That's something that we could consider."

- id: m16-044
  expression: "certainly seems useful for us to collaborate"
  category: collaboration_value
  function: value_recognition
  speaker_role: questioner
  difficulty: 4
  context: "certainly seems useful for us to collaborate"

- id: m16-045
  expression: "I'm sure we will take a look at this and we'll get back"
  category: review_deferral
  function: polite_review
  speaker_role: questioner
  difficulty: 3
  context: "I'm sure we will take a look at this and we'll get back"

- id: m16-046
  expression: "the first step for us"
  category: sequencing
  function: step_ordering
  speaker_role: questioner
  difficulty: 3
  context: "the first step for us. Yeah. Once we finish that you know and we just doing the validation then we can jump into this."

- id: m16-047
  expression: "we are always open for that"
  category: openness_stating
  function: availability_signal
  speaker_role: questioner
  difficulty: 2
  context: "we are always open for that"

- id: m16-048
  expression: "we can set up like some one on one meeting can share details with each other"
  category: direct_meeting
  function: focused_session
  speaker_role: questioner
  difficulty: 3
  context: "we can set up like some one on one meeting can share details with each other"

- id: m16-049
  expression: "we can dispatch our engineer to your lab on site"
  category: resource_offer
  function: deployment_proposal
  speaker_role: presenter
  difficulty: 5
  context: "we can dispatch our engineer to your lab on site. We can do like emulation there."

# ── 의견 요청·협업 (Opinion Solicitation) ──
- id: m16-050
  expression: "this is again, an area where we would like your opinion and your insight on"
  category: opinion_request
  function: input_solicitation
  speaker_role: presenter
  difficulty: 4
  context: "this is again, an area where we would like your opinion and your insight on, because you are doing both"

- id: m16-051
  expression: "So there's some additional data that you can share with us that will help us in our decision"
  category: data_request
  function: decision_support
  speaker_role: questioner
  difficulty: 4
  context: "So there's some additional data that you can, or the information that you can share with us that will help us in our decision"

- id: m16-052
  expression: "Let us know what you think."
  category: response_invitation
  function: open_close
  speaker_role: presenter
  difficulty: 2
  context: "Let us know what you think."
  note: 제안 마무리 - 직접적이면서 열린 질문.
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-04-27 11 04 15_EN_Qualcomm_Morning2-extracted.wav` (총 11,080단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 라인 범위 | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입부 | line 17-22 | "Before we get into details, three key messages" + 첫 메시지 (스피드 연장) | 로드맵 발표 시작 공식 - "three key messages" | ★★☆ |
| 2 | 스펙 푸시백 | line 96-103 | Qualcomm "even small delta, no delta" + "kill it all together" + "mindful of that" | 스펙 푸시백 화법 - 극단 경고 + 시장 경고 | ★★★★ |
| 3 | 딜레마 공개 | line 278-285 | SK "we have some dilemma now" + NVIDIA 내부 논의 + "worrying about that" | 회피 화법 - 시장 딜레마 프레이밍 | ★★★ |
| 4 | 놓친 세그먼트 | line 230-234 | Qualcomm "you missed the main segment of 12 gigabyte" + SK "That's also a good point" | 정중 도전 + 수용 - "overlooked" + "good point" | ★★★★ |
| 5 | 협업 제안 | line 871-891 | SK "first time technology for both" + "what we expect from you" + QC "certainly seems useful" | 협업 제안 - 동기 부여 + 기대 명시 + 수용 | ★★★ |

**사용법**:
- 월: 발췌 1 (로드맵 발표 시작), 화: 발췌 2 (스펙 푸시백), 수: 발췌 3 (딜레마), 목: 발췌 4 (정중 도전), 금: 발췌 5 (협업 제안)
- 발췌 2, 4가 가장 가치 높음 - 협상·도전 화법이 밀집
- 일일 루틴의 ①②③④⑤⑥에 발췌를 넣어 사용

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **vendor roadmap pitch + customer pushback** register다. Marvell 회의와 반대 방향:
- **vendor 역할 (SK)**: 로드맵 발표, 정렬 요청, 제한 포장 - 네가 SK 입장에서 파트너사에 로드맵 설득할 때
- **customer 역할 (Qualcomm)**: 수요 검증, 스펙 푸시백, 시간배열 압박 - 네가 고객사로서 파트너를 평가/밀어붙일 때

두 역할 모두 학습해야. 특히 **customer 역할**은 네가 평소에 덜 연습하는 화법이다.

### Pragmatics (화용론) 핵심
1. **"Point noted."의 간결함**: 한국어 "네, 알겠습니다"는 길다. 영어는 "Point noted." 두 단어로 끝. 이 간결함이 권위를 만든다. 회의에서 제안을 받을 때 "Okay, I understand"가 아니라 "Point noted."를 써라.
2. **"no delta"의 정밀성**: 스펙 협상에서 "조금 차이도 안 됩니다"가 아니라 "no delta"로 수학적 정밀함을 표시. 이게 엔지니어의 권위다. "delta"라는 단어 하나가 스펙 푸시백의 핵심.
3. **"jeopardize the program"의 위험 명시**: "늦으면 안 됩니다"가 아니라 "jeopardize the program"으로 위험을 구체화. "jeopardize"가 타임라인 압박의 핵심 동사.
4. **"internalize that"의 깊이**: "understand"보다 깊다. "We'll take that. We'll internalize that." - 받아들여서 내재화한다. 입력을 진지하게 받아들인다는 강한 표시.
5. **"leave you with the feasibility"**: "X를 검토해 달라"가 아니라 "feasibility를 함께 남겨두자" - 검토 책임을 공유하면서도 정렬을 요구. 매우 고급 화법.

### 네가 당장 써야 할 Top 5
1. **"Before we get into the details, I'm going to share three key messages"** - 로드맵 발표 시작
2. **"Point noted."** - 제안 인지 (간결함 = 권위)
3. **"even though it's very small delta there has to be no delta"** - 스펙 푸시백
4. **"Our target is to reach X. But that's to be confirmed."** - 타겟 + 면책
5. **"We'll take that. We'll internalize that."** - 입력 수용

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "알겠습니다" | "Point noted." | 한국어는 길게, 영어는 두 단어로 권위 |
| "검토 중입니다" | "Our target is X. But that's to be confirmed." | 타겟은 말하되 면책 |
| "시장이 안 좋아서요" | "we have some dilemma now because the market is very X" | "딜레마"로 프레이밍 |
| "지금은 좀 어렵습니다" | "it's just not the highest priority" | "No" 대신 "not highest priority" |
| "좀만 차이 나도 안 됩니다" | "even small delta, there has to be no delta" | "no delta"로 수학적 정밀 |
| "늦으면 안 됩니다" | "anything later than that jeopardize the program" | "jeopardize"로 위험 명시 |
| "놓치셨습니다" | "you missed the main segment of X" | "in my mind"로 겸손 + 직접 |
| "검토해 보겠습니다" | "We'll take it back and discuss it with the X team" | "take it back"으로 검토 이동 |
| "협업합시다" | "certainly seems useful for us to collaborate" | "seems useful"로 부드러운 긍정 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 4절 협상 화법 + 3절 정중 도전 화법을 중심으로 dump 작성
4. **역할 바꿔 연습**: 이 회의는 vendor/customer 두 역할 모두 학습 - partner사에 로드맵 설득할 때는 1절 발표 구조 + 2절 회피 화법, 고객사로 파트너 평가할 때는 3절 도전 화법 + 4절 푸시백 언어 사용
5. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득 - 특히 "Point noted"의 간결함과 "no delta"의 정밀함

---

*Textbook 16 - Qualcomm Morning2 (2026-04-27). 회의 유형 B (Roadmap/Supply Alignment). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
