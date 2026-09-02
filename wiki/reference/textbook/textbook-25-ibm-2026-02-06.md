---
textbook_id: 25
meeting: IBM CXL/Architecture Technical Deep-dive
date: 2026-02-06
type: A (technical deep-dive)
partner: IBM (Patrick, Dave, Kadri)
sk_side: SK Hynix CXL Product Planning, Memory Engineering, Jerry, Steve
duration_words: 7798
audio: repo/webex-audio/2026-02-06 07 59 44_EN_IBM meeting-extracted.wav
transcript: repo/webex-audio/2026-02-06 07 59 44_EN_IBM meeting-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, ibm, cxl, sap-hana, memory-pooling, switch-vs-switchless, lpddr, technical-deepdive, roadmap]
---

# Textbook 25 - IBM CXL/Architecture Technical Deep-dive (2026-02-06)

> **회의 유형**: A (technical deep-dive) - 양쪽이 각자 CXL 아키텍처 stance를 발표하고, 상대가 기술 Q&A로 도전
> **학습 가치**: IBM의 제약 공개 화법(시스템 한계 인정), SK Hynix의 internal discussion 회피, 양측의 정중한 기술 탐지
> **Audrey 관점**: 이 회의는 "mutual technical disclosure + mutual probing" 구조 - 네가 IBM 입장(제약 공개)이든 SK 입장(회피+제안)이든 둘 다 배워야. 특히 IBM의 "우리 시스템이 제약이 많다"를 솔직하게 공개하는 화법이 영어 회의의 핵심 스킬.

---

## 1. 발화 아키텍처 - Patrick의 발표 설계 (5단계)

Patrick(IBM)는 발표를 5단계 구조로 설계한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "제약 공개 + 요청"의 뼈대다. Marvell 회의(Ravi)의 "문제 → 솔루션 → 이유" 구조와 달리, Patrick은 "목표 → 현재 상태 → 미래 로드맵 → 제약 → 결정 시점"으로 전개한다. 이것이 **buyer-side 발표의 공식**이다.

### 단계 1: 목표 선언 (Goal Framing)

Patrick은 제품/로드맵을 설명하기 전에 **목표부터 선언**한다. "우리가 CXL을 왜 하는가"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `our goal in pursuing X has been the hope to achieve Y` | "our goal in pursuing CXL for IBM Power has been the hope to achieve a lower cost per gigabyte in our systems" | 목표 선언 - "hope to achieve"로 방향성 표시 |
| `we're always strongly advocating for X` | "we're always strongly advocating for cost-optimized memory solutions for our key workloads" | 입장 표명 - "strongly advocating"로 요구 근거 |

**Audrey 교훈**: 영어 발표는 "우리가 뭘 원하는가"로 시작해라. "Our goal in pursuing X has been the hope to achieve Y" - 이 공식을 외워. 제안·요구를 할 때, 먼저 목표를 명시하면 상대방이 네 요구의 배경을 이해한다. 한국어로는 "저희는 비용 절감을 원합니다"인데, 영어는 "our goal has been the hope to achieve"로 한 번 더 감싼다. "hope"가 정중함을 만든다.

### 단계 2: 현재 상태 보고 (Current State)

목표 선언 후, "At the moment, in terms of what we're actually testing on hand"로 현재 상태를 보고한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `At the moment, in terms of what we're actually X, we've got Y` | "At the moment, in terms of what we're actually testing on hand, we've got proof of concept adapter cards" | 현재 상태 - "what we're actually X"로 사실 기반 강조 |
| `So, we've got a number of different models of our X` | "So, we've got a number of different models of our P future product" | 제품 라인업 소개 |

### 단계 3: 미래 로드맵 (Future Roadmap)

"And then the mid-range and scale-out models are going to release in 2029"로 시점별 로드맵을 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `our first native support in our X will be Y in Z` | "our first native support in our Power servers will be CXL 2.0 support in our P future product in 2028" | 최초 지원 선언 - "first native support"로 마일스톤 표시 |
| `The high-end release is going to be in X. And then the mid-range and scale-out models are going to release in Y` | "The high-end release is going to be in 2028. And then the mid-range and scale-out models are going to release in 2029" | 단계별 출시 - "going to be / going to release" 반복 |
| `It's going to be CXL 2.0 just because that's what the architecture was when we froze the design` | "It's going to be CXL 2.0 just because that's what the architecture was when we froze the design" | 제약 설명 - "just because"로 불가피함 표시 |

**Audrey 교훈**: "we froze the design"은 하드웨어 설계 고정의 공식 표현이다. "우리가 설계를 고정했을 때 그게 표준이었으니까 CXL 2.0이 됐다" - 불가피한 제약을 설명할 때, "just because that's what the architecture was when we froze the design"을 써라. 책임을 시점으로 돌리는 화법이다.

### 단계 4: 제약 공개 (Constraint Disclosure)

이 단계가 **이 회의의 핵심**. Patrick은 시스템 제약을 솔직하게 공개한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `It's not ideal in terms of the system design` | "It's not ideal in terms of the system design" | 제약 인정 - "not ideal"로 솔직한 한계 공개 |
| `it's very difficult. The systems already have a whole lot of X and we just don't have many Y` | "it's very difficult. The systems already have a whole lot of memory in and we just don't have many half-height, half-length form factors" | 제약 설명 - "whole lot of X / just don't have many Y" 대비 |
| `So, 2028 is a little challenging for CXL design` | "So in that sense, 2028 is a little challenging for CXL design" | "a little challenging" - 직접적이면서도 부드러운 제약 표현 |
| `They'd be half-height, half-length only` | "they'd be half-height, half-length only" | "only"로 제한 강조 |

**Audrey 교훈**: 영어 회의에서 제약을 공개할 때 "It's not ideal"을 써라. "bad"나 "terrible"이 아니라 "not ideal" - 전문가의 솔직한 제약 인정이다. 그리고 "a little challenging" - "어려움"을 "a little"로 줄여서 들리게. 한국어로는 "좀 어렵습니다"인데, 영어는 "a little challenging"이 더 전문적으로 들린다. 제약을 공개하면서도 통제된 인상을 주는 화법이다.

### 단계 5: 결정 시점 + 요청 (Decision Point + Ask)

제약 공개 후, "we've got to make a decision this quarter"로 긴급성을 만들고, 상대에게 요청한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we're at a point now where we've got to make a decision this quarter on how we want to proceed with X` | "we're at a point now for the P-Future high-end product in 2028, we're at a point now where we've got to make a decision this quarter on how we want to proceed with CXL" | 결정 시점 - "got to make a decision this quarter"로 긴급성 |
| `We're really interested in hearing from X on what you'd be able to offer in the Y timeframe` | "We're really interested in hearing from SSSK hynix on what you'd be able to offer in the 2028 timeframe and what you see the CXL market doing over the next few years" | 요청 공식 - "really interested in hearing from you"로 정중한 ask |
| `But that's where we stand in terms of what X has for Y` | "But that's where we stand in terms of what IBM Power has for CXL" | 발표 마무리 - "where we stand"로 현재 위치 요약 |

**Audrey 교훈**: "we've got to make a decision this quarter" - "이번 분기에 결정해야 한다" - 긴급성을 만드는 공식이다. 그리고 바로 "we're really interested in hearing from you"로 연결한다. 긴급성 → 요청. 이 순서가 중요하다. 한국어로는 "빨리 알려주세요"인데, 영어는 "we've got to make a decision this quarter, so we're really interested in hearing from you" - 긴급성의 이유를 먼저 대고 요청한다. 이게 더 설득력 있다.

### Steve의 발표 아키텍처 (보완)

Steve(SK Hynix CXL product planning)는 Patrick 이후에 발표하며, "trend → roadmap → sample → comparison → software" 구조를 쓴다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Jerry already introduced X at the front part of my presentation. So I continue to explain Y` | "Jerry already introduced the technology trend at the front part of my presentation. So I continue to explain the technical trend" | 발표 인계 - "I continue to explain"로 자연스러운 이어받기 |
| `Actually, last year, the CXL memory was focused to X. The main goal is caused by Y. And now Z. The focus has shifted to W` | "Actually, last year, the CXL memory was focused to expand the local memory capacity... And now the AI workloads are glowing. The focus has shifted to NMM inference and KV Cache offloading" | 트렌드 전환 - "last year X / And now Y"로 변화 설명 |
| `Do you have any thoughts?` | "Do you have any thoughts?" | 열린 질문 - 상대 의견 탐지 |
| `Do you have any question in our roadmap?` | "Do you have any question in our roadmap?" | 질문 유도 - "in our roadmap"으로 범위 명시 |

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 양측이 어떻게 약점과 불확실성을 정중하게 포장하는지. 특히 SK Hynix 측의 "internal discussion" 회피와 IBM 측의 "just starting to look at it" 회피가 대비를 이룬다.

### 전략 1: "Internal Discussion" 회피 (SK Hynix)

SK Hynix 측이 가장 자주 쓰는 회피. 구체 수치·아키텍처를 공개하지 않을 때 "internal discussion phase"로 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 상세 아키텍처 공개 거부 | "so I think it is still an internal discussion phase, so I cannot show the details, but if I have an opportunity and we have some, we organized the already internal talk and discussion, so we will propose that architecture and show the detail" | "아직 내부 논의 단계라서 상세는 못 보여드리지만, 기회가 되면 아키텍처를 제안하고 상세를 보여드리겠습니다" |
| 미디어 타입 결정 전 | "No, it is under discussion time. So I cannot show the clear view for that" | "논의 중이라서 명확한 답을 못 드리겠습니다" |
| LP5/LP6 전환 | "Is that with stacking in the packages? Yes, stacking. So many stacking in the package. ... No, it is under discussion time" | "논의 중입니다"로 전환 |

**패턴 공식**: `It is still an internal discussion phase, so I cannot show the details. But if I have an opportunity, we will propose that architecture and show the detail.`

**Audrey 교훈**: "internal discussion phase"는 한국 기업이 회의에서 가장 자주 쓰는 회피다. "I cannot show the details"가 직접적 거부라면, "it is still an internal discussion phase, so I cannot show the details"는 "아직 내부에서 논의 중이라서"라는 이유를 대서 거부를 부드럽게 만든다. 핵심은 "so" - "그래서 못 보여드린다"의 인과관계. 그리고 "but we will propose that architecture"로 미래 약속을 붙여. 거부 뒤에 무조건 미래 약속.

### 전략 2: "Apple to Apple" 비교 회피 (SK Hynix)

비교 수치를 못 줄 때, "apple to apple 비교가 안 된다"로 회피.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR5 vs CXL 비교 | "I don't have the relative cost to the conventional DDI5, I think, because as I mentioned, we should change the media time. Yeah, so I'm not sure we can compare the Apple to Apple, but we will calculate that" | "미디어를 바꿔야 해서 기존 DDR5와 상대 비교가 없습니다. apple to apple 비교가 안 될 수 있지만, 계산해 보겠습니다" |

**패턴 공식**: `I don't have the relative cost to X. I'm not sure we can compare the Apple to Apple, but we will calculate that.`

**Audrey 교훈**: "apple to apple" (정확히는 "apples to apples") 비교는 영어 회의에서 자주 쓰는 표현이다. "같은 조건으로 비교가 안 된다"를 우아하게 표현. "I'm not sure we can compare apples to apples, but we will calculate that" - 비교 안 됨을 인정하면서도 "we will calculate"로 노력 의지를 표시. 수치를 못 줄 때 "I don't know" 대신 써라.

### 전략 3: "Just Starting to Look at It" 회피 (IBM)

Patrick은 IBM의 appliance 계획이 없을 때, "just starting to look at it"로 초기 단계임을 강조.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| CXL appliance 계획 | "I think if we were to pursue a CXL appliance system for our P future in the 2028 2029 timeframe It would likely be an external Appliance, but like I said just starting to look at that so" | "2028-2029에 CXL appliance를 추진한다면 외부 appliance일 텐데, 아직 막 살펴보기 시작한 단계라서" |
| 신뢰성 면책 | "I'm not confident in any of the answers I'm giving here We need to look more internally about what we would want from an appliance as we look at it But I think it's a possibility that we might be interested" | "제가 드리는 답변에 자신이 없습니다. appliance로부터 원하는 것을 내부적으로 더 봐야 합니다. 하지만 관심이 있을 가능성은 있습니다" |
| 의향 표시 | "I think it's a possibility that we might be interested" | "관심이 있을 가능성이 있습니다" |

**패턴 공식**: `We're really just starting to look at it. So I'm not confident in any of the answers I'm giving here. But I think it's a possibility that we might be interested.`

**Audrey 교훈**: "I'm not confident in any of the answers I'm giving here" - 이게 영어 회의에서 자신 없음을 인정하는 가장 정직한 화법이다. 한국어로는 "잘 모르겠습니다"인데, 영어는 "I'm not confident in any of the answers I'm giving"으로 자신의 답변 전체에 대한 신뢰도를 낮춘다. 그리고 "But I think it's a possibility that we might be interested" - "possibility" + "might" 이중 완화어로 의향만 표시. 확약 없이 관심만 보여주는 화법.

### 전략 4: "We'd Have to See" 회피 (IBM)

Dave는 구체 수치를 못 줄 때 "we'd have to see"로 회피.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 대역폭 목표 | "from our end, we'd have to see, you know, we do need a certain level of bandwidth to support SAP HANA, but we'd have to see what we'd actually want from each device" | "저희 쪽에서는 봐야 합니다. SAP HANA 지원을 위해 어느 정도 대역폭은 필요하지만, 각 장치마다 실제로 원하는 건 더 봐야 합니다" |

**패턴 공식**: `We'd have to see what we'd actually want from each device.`

**Audrey 교훈**: "we'd have to see"는 "봐야 한다" - 결정을 미루는 화법이다. "We need X but we'd have to see Y" - 필요는 인정하되 구체 수치는 미룬다. "we'd have to see what we'd actually want" - "실제로 원하는 건 더 봐야 한다" - 자신의 요구사항조차 아직 모른다고 하여 회피의 폭을 넓힌다.

### 전략 5: 제약을 기회로 재프레이밍 (SK Hynix)

Steve는 switch의 latency 한계를 인정하되, "we are trying to co-work with another switch partner"로 해결 의지를 표시.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Switch latency 한계 | "the current CXL switch has some slow latency number... but even though they have a slower latency number, but it is faster than the RDMA network. So, yeah, I mean they are focusing on that point... We are also trying to co-work with the another switch partner. They told me they are insisting that they can reduce the latency number when comparing to the current existing switch vendor. So, yeah, we will evaluate that" | "현재 CXL switch는 latency가 느립니다. 하지만 RDMA보다는 빠릅니다. 또 다른 switch 파트너와 협력 중이며, 그들은 기존 vendor보다 latency를 줄일 수 있다고 주장합니다. 평가해 보겠습니다" |

**패턴 공식**: `The current X has some slow Y. But it is faster than Z. We are also trying to co-work with another partner. They can reduce Y. We will evaluate that.`

**Audrey 교훈**: 제약을 인정하되 즉시 비교 우위("faster than RDMA")로 전환하고, 해결 파트너를 제시. "we will evaluate that"으로 미래 행동을 약속. 이 3단 전환 - 한계 인정 → 비교 우위 → 해결 파트너 - 을 외워.

### 전략 6: "I Don't See Any Reason Why Not" 보증 (IBM)

Patrick은 SAP HANA 지속 지원을 물을 때, 이중 부정으로 확신을 표시.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| SAP HANA 지속 | "generally speaking, we have a high penetration of SAP support across our power portfolio. I don't see any reason why that would not continue" | "일반적으로 Power 포트폴리오 전반에 SAP 지원이 높습니다. 계속되지 않을 이유가 없습니다" |

**패턴 공식**: `We have a high penetration of X across Y. I don't see any reason why that would not continue.`

**Audrey 교훈**: "I don't see any reason why that would not continue" - 이중 부정("not... not continue")으로 강한 확신을 표시. "It will continue"보다 더 신뢰감을 준다. "계속되지 않을 이유가 없다" - 부정의 부정으로 긍정을 만드는 영어 화법. 약속을 직접 안 하면서도 확신을 주는 고급 화법.

---

## 3. 정중한 도전 화법 (양측 질문자)

이 회의에서는 양측이 서로에게 정중하게 기술 도전을 한다. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 직접 탐지형 질문 (Direct Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `How many slots are you considering for the CXL?` | "How many slots are you considering for the CXL? You mentioned that it's a small slot number in 2028" | 직접적 수량 탐지 - 앞 언급 회상 + 질문 |
| `What capacity are you expecting with using X?` | "what capacity are you expecting with using triple HL add-in card from Factor?" | 기대치 탐지 - "what capacity are you expecting" |
| `Is there any target, a minimum target for X?` | "is there any target, a minimum target for lower dollar per gigabyte for IBM side?" | 최소 목표 탐지 - "minimum target"으로 구체화 압박 |

**Audrey 교훈**: "How many slots are you considering?"는 직접적이면서 정중하다. "Why only that many?"가 아니라 "How many are you considering?" - 상대의 계획을 묻되, 비난은 빼는 화법. 수량·목표·기대치를 물을 때 "How many are you considering / What are you expecting / Is there any target" 패턴을 써라.

### 질문 유형 2: 이해 확인형 질문 (Comprehension Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is that an X focused first and then Y is still under discussion? Do I understand correctly?` | "Is that an EDSFF focused first and then add-in card is still under discussion? Do I understand correctly?" | 이해 확인 + "Do I understand correctly?"로 정중 검증 |
| `So that's out of the controller on the host interface?` | "So that's out of the controller on the host interface?" | 짧은 확인 - 기술적 정확성 검증 |

**Audrey 교훈**: "Do I understand correctly?"는 Marvell 회의에서도 본 핵심 화법. 이 회의에서 SK Hynix가 IBM에게 쓴다. "Is that X focused first and then Y under discussion? Do I understand correctly?" - 자기 이해를 먼저 진술하고 상대에게 검증을 요청. 이게 정중한 도전이다.

### 질문 유형 3: 이유 질문 (Reason Inquiry)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Could you please tell me why you are interested in X?` | "Could you please tell me why you are interested in the switch based solution?" | "why are you interested" - 직접적이면서 정중 |
| `Could you please share your any X related plan from now?` | "could you please share your any PQC related plan from now?" | "share your plan" - 계획 공유 요청 |
| `Do you have any thoughts or insight to share on this matter?` | "Do you have any thoughts or insight to share on this matter?" | "thoughts or insight" - 의견 + 통찰 이중 요청 |

**Audrey 교훈**: "Could you please tell me why you are interested in X?"는 "Why do you want X?"보다 훨씬 정중하다. "Could you please" + "tell me why" - 능력 요청 형식으로 완화. 그리고 "Do you have any thoughts or insight to share on this matter?" - "thoughts or insight"로 의견을 물으면 상대는 자기 입장을 설명할 기회를 얻는다. 이게 협조적인 도전이다.

### 질문 유형 4: 타임라인 탐지 (Timeline Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Are these targeted, like you mentioned, X, is that the timeframe where these sorts of solutions might be entering the market?` | "Are these targeted, like you mentioned, 2029, is that the timeframe where these sorts of solutions might be entering the market, you think?" | 타임라인 확인 - "like you mentioned"로 앞 언급 회상 |
| `Do you have any idea when you expect that to be finalized in your roadmap?` | "Do you have any idea when you expect that to be finalized in your roadmap?" | 로드맵 확정 시점 탐지 |
| `Do you have any idea what sort of X they're hoping to get?` | "Do you have any idea what sort of gain they're hoping to get?" | "what sort of" - 구체화 압박 |

**Audrey 교훈**: "Do you have any idea when X?"는 "When will X?"보다 부드럽다. "When will you finalize?"가 직접적이면, "Do you have any idea when you expect that to be finalized?"는 "대략 언제쯤 예상하시는지 아십니까?" - 상대의 추정치를 물어서 압박을 줄인다.

### 질문 유형 5: 기술 사양 확인 (Spec Clarification)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `is that media level?` | "is that media level?" | 짧은 기술 확인 - 측정 기준 탐지 |
| `Is that rewrite workload combined?` | "Is that rewrite workload combined?" | 워크로드 조건 확인 |
| `Is this going to be a buy eight?` | "Is this going to be a buy eight?" | 폼팩터 확인 - "buy eight" (x8) |
| `So then that makes sense because if you're a by Gen six in one direction, okay` | "So then that makes sense because if you're a by Gen six in one direction, okay" | 이해 도출 - "that makes sense because"로 자기 추론 공개 |

**Audrey 교훈**: 기술 회의에서 "is that media level?" 같은 짧은 확인 질문은 필수다. 발표자가 수치를 말할 때, 그 수치의 기준(미디어 레벨? 컨트롤러? 호스트 인터페이스?)을 확인하지 않으면 잘못 이해한다. "Is that X level?"로 기준을 명확히 해라.

### 질문 유형 6: 확인 요청 (Confirmation Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Could you please confirm if the IBM need our evaluation of the sample before ES simply released?` | "Could you please confirm if the IBM need our evaluation of the sample before ES simply released?" | "Could you please confirm if" - 확인 요청 공식 |
| `The timeline is ES is December this year` | "The timeline is ES is December this year" | 타임라인 명시 - 확인을 위한 사실 진술 |

**Audrey 교훈**: "Could you please confirm if X?"는 확인 요청의 공식이다. "Do you need X?"보다 "Could you please confirm if you need X?"가 더 정중. "confirm"이 핵심 - 상대의 답변을 "확인"으로 격상시킨다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

회의 후반, 후속 협상과 action item을 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 결정 시점 명시 | Patrick | "we're at a point now where we've got to make a decision this quarter on how we want to proceed with CXL" | "got to make a decision this quarter" - 긴급성 부여 |
| 요청 표명 | Patrick | "We're really interested in hearing from SSSK hynix on what you'd be able to offer in the 2028 timeframe" | "really interested in hearing from you" - 정중한 요청 |
| 진지함 표시 | Patrick | "I'm very happy to hear that" | "very happy to hear" - 긍정 피드백 |
| 가능성 시사 | Patrick | "that sounds promising" | "sounds promising" - 관심 표시 |
| 내부 검토 약속 | Patrick | "I will talk internally and see if we can look at that because that sounds promising" | "talk internally and see if we can" - 내부 검토 |
| 의향 탐지 | Steve | "could you please, what activity or do you have any feedback from the SAP HANA team to support the SXM memory technology for years over?" | "any feedback from X" - 파트너 동향 탐지 |
| 제안 의향 | Steve | "if we can make the lower cost or the DLAM based CXL memory pooling appliance, we might compete against the ICMS" | "we might compete against X" - 경쟁 의식 공개 |
| 입장 표명 | Patrick | "we have a high penetration of SAP support across our power portfolio. I don't see any reason why that would not continue" | "high penetration" + "don't see any reason why not" - 강한 입장 |

**Audrey 교훈**:
- "we've got to make a decision this quarter" - 긴급성을 만들 때 "got to"를 써라. "need to"보다 "got to"가 더 절박하다.
- "We're really interested in hearing from you" - 요청을 "interest"로 포장. "We want you to tell us"가 아니라 "We're interested in hearing from you" - 듣는 쪽이 주체인 것처럼.
- "that sounds promising" - 관심을 표시할 때 "good"이 아니라 "promising"을 써라. "좋다"가 아니라 "유망하다" - 더 신중하면서도 긍정적.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 내부 논의 후 회신 | Jerry | "let me discuss internally how we can have that stance for both HL and FHHL adding card from Pector and get back to you" | "discuss internally and get back to you" - 내부 논의 + 회신 약속 |
| 후속 확인 약속 | Steve | "Let me check and get back to you" | "check and get back" - 짧은 action item |
| 이메일 후속 | Steve | "I will send this table via email if you have any question about this feature. Just let us know" | "send via email + just let us know" - 후속 채널 |
| 내부 회신 요청 | Steve | "Please talk internally and get back your feedback to DK" | "talk internally and get back your feedback" - 상대에게 action item 부여 |
| 내부 회신 요청 | Steve | "please leave you internally and get back your feedback" | "leave internally" - 내부 검토 요청 |
| 후속 제안 약속 | Jerry | "we will propose that architecture and show the detail" | "will propose and show" - 미래 제안 약속 |
| 전체 피드백 | Patrick | "I think it was very comprehensive. I really appreciate you take time to talk with us" | "very comprehensive" + "really appreciate" - 회의 마무리 |

**Audrey 교훈**:
- "let me discuss internally and get back to you" - 가장 자주 쓰이는 action item 공식. "I'll check"는 약하다. "discuss internally and get back to you" - 내부 논의(행동) + 회신(결과)를 명시.
- "Please talk internally and get back your feedback to DK" - 상대에게 action item을 부여할 때 "Please talk internally and get back"을 써라. 단순히 "let me know"가 아니라 "talk internally" (구체 행동) + "get back your feedback to DK" (회신 대상 명시).
- 회의 마무리는 "I think it was very comprehensive" - "comprehensive"가 핵심. "good"이 아니라 "comprehensive" - "내용이 충실하다"는 전문가 평가.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/메모리/서버 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **CXL 2.0 / 3.1 / 4.0** | CXL 프로토콜 세대 | "our first native support will be CXL 2.0 support in our P future product in 2028. It is CXL 2.0 just because that's what the architecture was when we froze the design" |
| **SAP HANA** | 인메모리 데이터베이스 (SAP) | "our goal in pursuing CXL for IBM Power has been the hope to achieve a lower cost per gigabyte... Particularly for SAP HANA and other potential applications" |
| **in-memory database** | 메모리 기반 DB | "in-memory database applications, very memory intensive" |
| **DDR5 DDIM** | DDR5 DRAM 모듈 | "Power systems support a very large number of DDR5 DDIMs" |
| **EDSFF (E3.S, E1.S)** | 서버 폼팩터 표준 | "in 2029, it'll be half-height, half-length, add-in cards and the E3.S 2T form formats... we are also exploring the E1.S. from factor" |
| **half-height, half-length (HHHL)** | 반높이 반길이 카드 폼팩터 | "the only form factor we'll be able to support would be half-height, half-length add-in cards" |
| **FHHL (full height half length)** | 전높이 반길이 카드 | "there are some customers wanting to have the FHHL adding card from Pector" |
| **triple HL** | (발음) half-height, half-length | "the first one said there is no customer demand for the triple HL from Factor" |
| **sled / drawer** | 서버 모듈 단위 | "that system is in a sled form factor. So, half a drawer is the smallest building block" |
| **add-in card slot** | 확장 카드 슬롯 | "it only supports CXL on its add-in card slot... Only the add-in card slots in the back support CXL" |
| **LPDDR (LP5, LP6)** | 저전력 DRAM | "currently we are exploring the different kinds of adoption of the memory media. I mean, not only the DDR5, but also the LPDDR as well" |
| **3DS (3D stacking)** | 3D 적층 DRAM | "we are not using the 3DS 2i stack so we will use the monodi" |
| **monodie** | 단일 다이 DRAM | "Our whole monodi based one to make the 512 GB. That is one of our options" |
| **KV Cache** | LLM 키-값 캐시 | "what kind of demand for CXL based solutions are you seeing in the AI KV Cache space?" |
| **RDMA** | 원격 직접 메모리 액세스 | "they communicate the package and the shuffle the data across the server via RDMA, NIC card" |
| **NIC** | 네트워크 인터페이스 카드 | "from the RDMA, NIC, the latency number to the CXL based PCI and VR memory pooling system" |
| **switch vs switchless** | CXL 메모리 풀링 아키텍처 | "there are pros and cons between the switch and switch list" |
| **TCO** | 총소유비용 | "from the TCO perspective the switch based architecture offers a long-term advantage" |
| **PQC (post-quantum cryptography)** | 양자내성 암호 | "I Believe IBM also has a security enhancement plan related to PQC... we will support it to PQC from our second CMM" |
| **ES / CS** | 엔지니어링 샘플 / 고객 샘플 | "ES sample is completely same hardware and software with CS. The timeline is ES is December this year" |
| **MP** | 양산 단계 | "Our first-gen 120 KG of ICMM is now MP stage" |
| **CMM (CXL Memory Module)** | CXL 메모리 모듈 | "the second generation 6 cell module has twice the media of the first gen" |
| **HMS DK** | 이종 메모리 소프트웨어 개발 키트 | "heterogeneous memory software develop key watch called the HMS DK" |
| **die count** | 다이 수 (비용 요소) | "our target is reducing die count to like 10%, around 10%" |
| **controller IC** | 컨트롤러 칩 | "the controller is very huge [cost portion]" |
| **TTFT** | 첫 토큰 생성 시간 | "CXL based pooling proven on performance is cut TTFT by almost 9% compared to RDMA" |
| **QPS** | 초당 쿼리 수 | "push it the QPS up by more than seven times" |
| **rigid flex** | Rigid-Flex PCB 기술 | "two PCB with the rigid flux technology to make the 512 GB" |
| **solder down** | 납땜 고정 타입 | "So it's the solder down case" |
| **Gen 5 / Gen 6 PCI** | PCIe 세대 | "we're a Gen 5 PCI link. And so we're already limited there... CXL 4.0 came out in November 2025. It used PCI Gen 6, Gen 7" |
| **by eight (x8)** | PCIe 8레인 | "Is this going to be a buy eight? Yeah, buy eight" |
| **MLC application** | 메모리 지연 측정 앱 | "we use the MLC application on top of the Intel... it's a real measure the number" |
| **ICMS** | NVIDIA KV cache-to-SSS 솔루션 | "NVIDIA announced the IMCS to offloading KV Cache to SSD" |
| **CSP** | 클라우드 서비스 제공자 | "The CSPs evaluating the CXL pooling system and they confirmed that" |
| **IMDB** | 인메모리 DB | "The CXL memory was focused to expand the local memory capacity for IMDB and HPC" |
| **WAC / rack** | 랙 단위 | "they are scaling the memory pools across WAC to build more bigger distributed memory architectures" |
| **MP stage** | 양산 단계 | "Our first-gen 120 KG of ICMM is now MP stage" |
| **bring up** | 하드웨어 초기 구동 | (Marvell 회의와 동일 의미) |
| **tape out** | 칩 설계 완료 | (이 회의에선 미사용, Marvell 회의 참조) |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m25-001
  expression: "our goal in pursuing X has been the hope to achieve Y"
  category: presentation_framing
  function: goal_declaration
  speaker_role: presenter
  difficulty: 4
  context: "our goal in pursuing CXL for IBM Power has been the hope to achieve a lower cost per gigabyte in our systems"
  note: 발표 시작 목표 선언 - "hope to achieve"로 정중한 방향성 표시. buyer-side 발표 공식

- id: m25-002
  expression: "we're always strongly advocating for X"
  category: stance_stating
  function: position_declaration
  speaker_role: presenter
  difficulty: 3
  context: "we're always strongly advocating for cost-optimized memory solutions for our key workloads"
  note: "strongly advocating" - 입장 표명 공식

- id: m25-003
  expression: "At the moment, in terms of what we're actually X, we've got Y"
  category: current_state
  function: factual_reporting
  speaker_role: presenter
  difficulty: 4
  context: "At the moment, in terms of what we're actually testing on hand, we've got proof of concept adapter cards"
  note: "what we're actually X" - 사실 기반 강조

- id: m25-004
  expression: "our first native support in our X will be Y in Z"
  category: roadmap_milestone
  function: first_support
  speaker_role: presenter
  difficulty: 3
  context: "our first native support in our Power servers will be CXL 2.0 support in our P future product in 2028"

- id: m25-005
  expression: "It's going to be X just because that's what the architecture was when we froze the design"
  category: constraint_explanation
  function: inevitability_framing
  speaker_role: presenter
  difficulty: 5
  context: "It's going to be CXL 2.0 just because that's what the architecture was when we froze the design"
  note: "when we froze the design" - 설계 고정 시점 표현. 불가피함을 시점으로 돌리는 화법

- id: m25-006
  expression: "It's not ideal in terms of the system design"
  category: limitation_acknowledgment
  function: honest_constraint
  speaker_role: presenter
  difficulty: 4
  context: "It's not ideal in terms of the system design"
  note: "not ideal" - 전문가의 솔직한 제약 인정. "bad"가 아니라 "not ideal"

- id: m25-007
  expression: "it's very difficult. The systems already have a whole lot of X and we just don't have many Y"
  category: constraint_disclosure
  function: capacity_limitation
  speaker_role: presenter
  difficulty: 4
  context: "it's very difficult. The systems already have a whole lot of memory in and we just don't have many half-height, half-length form factors"
  note: "whole lot of X / just don't have many Y" - 대비 구조로 제약 설명

- id: m25-008
  expression: "X is a little challenging for Y design"
  category: soft_constraint
  function: mild_difficulty
  speaker_role: presenter
  difficulty: 3
  context: "2028 is a little challenging for CXL design"
  note: "a little challenging" - 부드러운 제약 표현. "very difficult"보다 전문적

- id: m25-009
  expression: "we're at a point now where we've got to make a decision this quarter on how we want to proceed with X"
  category: decision_urgency
  function: timeline_pressure
  speaker_role: presenter
  difficulty: 5
  context: "we're at a point now where we've got to make a decision this quarter on how we want to proceed with CXL"
  note: "got to make a decision this quarter" - 긴급성 부여 공식

- id: m25-010
  expression: "We're really interested in hearing from X on what you'd be able to offer in the Y timeframe"
  category: polite_request
  function: ask_formulation
  speaker_role: presenter
  difficulty: 5
  context: "We're really interested in hearing from SSSK hynix on what you'd be able to offer in the 2028 timeframe"
  note: "really interested in hearing from you" - 요청을 "interest"로 포장

- id: m25-011
  expression: "But that's where we stand in terms of what X has for Y"
  category: summary_close
  function: position_summary
  speaker_role: presenter
  difficulty: 3
  context: "But that's where we stand in terms of what IBM Power has for CXL"
  note: "where we stand" - 현재 위치 요약

- id: m25-012
  expression: "Jerry already introduced X at the front part of my presentation. So I continue to explain Y"
  category: handoff_continuation
  function: presentation_handoff
  speaker_role: presenter
  difficulty: 3
  context: "Jerry already introduced the technology trend at the front part of my presentation. So I continue to explain the technical trend"
  note: 발표 인계 - "I continue to explain"로 자연스러운 이어받기

- id: m25-013
  expression: "Actually, last year, the X was focused to Y. The main goal is caused by Z. And now W. The focus has shifted to V"
  category: trend_shift
  function: evolution_narrative
  speaker_role: presenter
  difficulty: 5
  context: "Actually, last year, the CXL memory was focused to expand the local memory capacity... And now the AI workloads are glowing. The focus has shifted to NMM inference and KV Cache offloading"
  note: "last year X / And now Y" - 트렌드 전환 서사

- id: m25-014
  expression: "Do you have any thoughts?"
  category: open_probe
  function: opinion_request
  speaker_role: presenter
  difficulty: 2
  context: "Do you have any thoughts?"

- id: m25-015
  expression: "Do you have any question in our roadmap?"
  category: question_invitation
  function: scoped_check
  speaker_role: presenter
  difficulty: 2
  context: "Do you have any question in our roadmap?"
  note: "in our roadmap" - 범위 명시

# ── 회피·포장 (Hedging & Deflection) ──
- id: m25-016
  expression: "it is still an internal discussion phase, so I cannot show the details"
  category: internal_discussion_deflection
  function: polite_refusal
  speaker_role: presenter
  difficulty: 4
  context: "so I think it is still an internal discussion phase, so I cannot show the details"
  note: 한국 기업 대표 회피 패턴. "internal discussion phase"로 거부를 이유화

- id: m25-017
  expression: "but if I have an opportunity, we will propose that architecture and show the detail"
  category: future_promise
  function: deferred_disclosure
  speaker_role: presenter
  difficulty: 4
  context: "but if I have an opportunity and we have some, we organized the already internal talk and discussion, so we will propose that architecture and show the detail"
  note: 거부 뒤 미래 약속 - "we will propose and show the detail"

- id: m25-018
  expression: "it is under discussion time. So I cannot show the clear view for that"
  category: under_discussion
  function: vague_deflection
  speaker_role: presenter
  difficulty: 3
  context: "No, it is under discussion time. So I cannot show the clear view for that"
  note: "under discussion" + "cannot show the clear view" - 이중 회피

- id: m25-019
  expression: "I don't have the relative cost to X"
  category: precision_disclaimer
  function: data_absence
  speaker_role: presenter
  difficulty: 3
  context: "I don't have the relative cost to the conventional DDI5, I think"

- id: m25-020
  expression: "I'm not sure we can compare the Apple to Apple, but we will calculate that"
  category: comparison_hedging
  function: apples_to_apples_evasion
  speaker_role: presenter
  difficulty: 5
  context: "I'm not sure we can compare the Apple to Apple, but we will calculate that"
  note: "apples to apples" 비교 안 됨 + "we will calculate" 노력 의지

- id: m25-021
  expression: "Let me check and get back to you"
  category: action_item_short
  function: defer_with_promise
  speaker_role: presenter
  difficulty: 3
  context: "Let me check and get back to you"
  note: 가장 짧은 action item 공식

- id: m25-022
  expression: "I forgot the specific number"
  category: forget_disclaimer
  function: memory_lapse
  speaker_role: presenter
  difficulty: 2
  context: "I forgot the specific number"
  note: "I don't know" 대신 "I forgot" - 일시적 기억 장애로 포장

- id: m25-023
  expression: "We're really just starting to look at it"
  category: early_stage_deflection
  function: preliminary_framing
  speaker_role: presenter
  difficulty: 4
  context: "like I said just starting to look at that so"
  note: IBM의 대표 회피 - "just starting"으로 초기 단계임을 강조

- id: m25-024
  expression: "I'm not confident in any of the answers I'm giving here"
  category: confidence_disclaimer
  function: honest_uncertainty
  speaker_role: presenter
  difficulty: 5
  context: "I'm not confident in any of the answers I'm giving here"
  note: 가장 정직한 자신 없음 인정 - "I'm not confident in any of the answers"

- id: m25-025
  expression: "I think it's a possibility that we might be interested"
  category: vague_interest
  function: non_commitment
  speaker_role: presenter
  difficulty: 5
  context: "But I think it's a possibility that we might be interested"
  note: "possibility" + "might" - 이중 완화어로 의향만 표시

- id: m25-026
  expression: "we'd have to see what we'd actually want from each device"
  category: see_what_deflection
  function: deferred_decision
  speaker_role: presenter
  difficulty: 4
  context: "we'd have to see what we'd actually want from each device"
  note: "we'd have to see" - 자기 요구사항조차 모른다고 하여 회피 폭 확대

- id: m25-027
  expression: "I don't see any reason why that would not continue"
  category: double_negative_assurance
  function: strong_continuity
  speaker_role: presenter
  difficulty: 5
  context: "we have a high penetration of SAP support across our power portfolio. I don't see any reason why that would not continue"
  note: 이중 부정 - "not... not continue"으로 강한 확신. 직접 약속 회피하면서 신뢰 부여

- id: m25-028
  expression: "I'm not sure what that means"
  category: polite_incomprehension
  function: clarification_request
  speaker_role: presenter
  difficulty: 3
  context: "I'm not sure what that means, but generally speaking, we have a high penetration of SAP support"
  note: "I don't understand" 대신 "I'm not sure what that means" - 정중한 이해 안 됨

- id: m25-029
  expression: "the current X has some slow Y. But it is faster than Z"
  category: constraint_reframe
  function: limitation_to_advantage
  speaker_role: presenter
  difficulty: 4
  context: "the current CXL switch has some slow latency number... but even though they have a slower latency number, but it is faster than the RDMA network"
  note: 한계 인정 → 비교 우위 전환

- id: m25-030
  expression: "We are also trying to co-work with another partner. They can reduce Y. We will evaluate that"
  category: solution_partner
  function: future_action
  speaker_role: presenter
  difficulty: 4
  context: "We are also trying to co-work with the another switch partner. They told me they are insisting that they can reduce the latency number... we will evaluate that"

# ── 정중한 도전 (Polite Challenge) ──
- id: m25-031
  expression: "How many slots are you considering for the CXL?"
  category: direct_probe
  function: quantity_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "How many slots are you considering for the CXL? You mentioned that it's a small slot number in 2028"

- id: m25-032
  expression: "What capacity are you expecting with using X?"
  category: expectation_probe
  function: target_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "what capacity are you expecting with using triple HL add-in card from Factor?"

- id: m25-033
  expression: "Is there any target, a minimum target for X?"
  category: target_probe
  function: minimum_inquiry
  speaker_role: questioner
  difficulty: 4
  context: "is there any target, a minimum target for lower dollar per gigabyte for IBM side?"
  note: "minimum target"으로 구체화 압박

- id: m25-034
  expression: "Is that an X focused first and then Y is still under discussion? Do I understand correctly?"
  category: comprehension_check
  function: polite_verification
  speaker_role: questioner
  difficulty: 5
  context: "Is that an EDSFF focused first and then add-in card is still under discussion? Do I understand correctly?"
  note: "Do I understand correctly?" - 정중한 검증 공식

- id: m25-035
  expression: "Could you please tell me why you are interested in X?"
  category: reason_inquiry
  function: interest_probe
  speaker_role: questioner
  difficulty: 4
  context: "Could you please tell me why you are interested in the switch based solution?"
  note: "Why do you want X?" 대신 "Could you please tell me why" - 능력 요청 형식

- id: m25-036
  expression: "Do you have any thoughts or insight to share on this matter?"
  category: insight_request
  function: opinion_inquiry
  speaker_role: questioner
  difficulty: 4
  context: "Do you have any thoughts or insight to share on this matter?"
  note: "thoughts or insight" - 의견 + 통찰 이중 요청

- id: m25-037
  expression: "Could you please share your any X related plan from now?"
  category: plan_request
  function: roadmap_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "could you please share your any PQC related plan from now?"

- id: m25-038
  expression: "Do you have any idea when you expect that to be finalized in your roadmap?"
  category: timeline_probe
  function: finalization_inquiry
  speaker_role: questioner
  difficulty: 4
  context: "Do you have any idea when you expect that to be finalized in your roadmap?"
  note: "Do you have any idea when" - "When will X?"보다 부드러운 타임라인 탐지

- id: m25-039
  expression: "Are these targeted, like you mentioned, X, is that the timeframe where Y might be entering the market?"
  category: timeline_confirm
  function: market_entry_probe
  speaker_role: questioner
  difficulty: 4
  context: "Are these targeted, like you mentioned, 2029, is that the timeframe where these sorts of solutions might be entering the market, you think?"

- id: m25-040
  expression: "is that media level?"
  category: spec_clarification
  function: measurement_basis_check
  speaker_role: questioner
  difficulty: 3
  context: "is that media level?"
  note: 측정 기준 확인 - 짧은 기술 확인 질문

- id: m25-041
  expression: "Is that rewrite workload combined?"
  category: spec_clarification
  function: workload_check
  speaker_role: questioner
  difficulty: 3
  context: "Is that rewrite workload combined?"

- id: m25-042
  expression: "Could you please confirm if the X need our Y?"
  category: confirmation_request
  function: polite_verify
  speaker_role: questioner
  difficulty: 4
  context: "Could you please confirm if the IBM need our evaluation of the sample before ES simply released?"
  note: "confirm if" - 확인 요청 공식

- id: m25-043
  expression: "what sort of X might you expect?"
  category: open_probe
  function: expectation_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "Are you able to comment at all about what sort of cost per gigabyte you might expect for the ultra-high capacity?"

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m25-044
  expression: "we've got to make a decision this quarter on how we want to proceed with X"
  category: decision_urgency
  function: timeline_pressure
  speaker_role: negotiator
  difficulty: 5
  context: "we've got to make a decision this quarter on how we want to proceed with CXL"
  note: "got to" - "need to"보다 절박한 긴급성

- id: m25-045
  expression: "I'm very happy to hear that"
  category: positive_feedback
  function: approval
  speaker_role: negotiator
  difficulty: 2
  context: "Okay, well, that's certainly a promising direction from our point of view, since we can focus on cost per gigabyte. So I'm very happy to hear that"

- id: m25-046
  expression: "that sounds promising"
  category: interest_expression
  function: qualified_approval
  speaker_role: negotiator
  difficulty: 3
  context: "I will talk internally and see if we can look at that because that sounds promising"
  note: "good" 대신 "promising" - 신중하면서도 긍정적

- id: m25-047
  expression: "let me discuss internally how we can have that stance and get back to you"
  category: internal_discussion_action
  function: deferred_response
  speaker_role: presenter
  difficulty: 4
  context: "let me discuss internally how we can have that stance for both HL and FHHL adding card from Pector and get back to you"
  note: 가장 자주 쓰이는 action item - "discuss internally and get back"

- id: m25-048
  expression: "Please talk internally and get back your feedback to X"
  category: action_request
  function: assign_action
  speaker_role: presenter
  difficulty: 4
  context: "Please talk internally and get back your feedback to DK"
  note: 상대에게 action item 부여 - "talk internally + get back feedback to X"

- id: m25-049
  expression: "I will send this table via email if you have any question. Just let us know"
  category: follow_up_channel
  function: open_contact
  speaker_role: presenter
  difficulty: 3
  context: "I will send this table via email if you have any question about this feature. Just let us know"

- id: m25-050
  expression: "I think it was very comprehensive. I really appreciate you take time to talk with us"
  category: meeting_close
  function: professional_compliment
  speaker_role: negotiator
  difficulty: 3
  context: "I think it was very comprehensive. I really appreciate you take time to talk with us"
  note: "comprehensive" - "good" 대신 "내용 충실" 평가. 회의 마무리 공식

# ── 발화 채움 표현 (Discourse Markers) ──
- id: m25-051
  expression: "So, we don't have many agenda today. So, it looks like we have only one topic"
  category: meeting_opening
  function: agenda_setting
  speaker_role: presenter
  difficulty: 2
  context: "So, we don't have many agenda today. So, yeah. So, it looks like we have only one topic"
  note: 가벼운 안건 설정 - "don't have many agenda"로 부담 낮춤

- id: m25-052
  expression: "Patrick, do you like to start first or do you want us to..."
  category: turn_offering
  function: speaker_invitation
  speaker_role: presenter
  difficulty: 3
  context: "Patrick, do you like to start first or do you want us to... Yeah, maybe it makes sense for me to start"
  note: "do you like to start" - 발화 순서 양보

- id: m25-053
  expression: "I was hoping to walk you through where we stand with X right now"
  category: meeting_purpose
  function: agenda_state
  speaker_role: presenter
  difficulty: 4
  context: "I was hoping to walk you through where we stand with CXL and IBM Power right now. And then maybe talk about where we go going forward"
  note: "walk you through where we stand" - 회의 목적 진술 공식

- id: m25-054
  expression: "Is it okay if I share the screen?"
  category: permission_request
  function: polite_ask
  speaker_role: presenter
  difficulty: 2
  context: "Is it okay if I share the screen?"
  note: 화면 공유 전 정중한 확인

- id: m25-055
  expression: "Yeah, go ahead, yeah"
  category: permission_grant
  function: approval
  speaker_role: questioner
  difficulty: 1
  context: "Yeah, go ahead, yeah"

- id: m25-056
  expression: "Yeah, take your time"
  category: patience_grant
  function: wait_acknowledgment
  speaker_role: questioner
  difficulty: 2
  context: "Yeah, take your time"
  note: 기다릴 때 "take your time" - "hurry up" 대신 정중한 인내

- id: m25-057
  expression: "so if you can give some the target bandwidth you'll be very helpful for SKHINIC"
  category: helpful_request
  function: value_frame
  speaker_role: questioner
  difficulty: 4
  context: "If you can give some the target bandwidth you'll be very helpful yeah for SKHINIC"
  note: 요청을 "very helpful"로 포장 - 부담 낮춤

- id: m25-058
  expression: "We'll talk and see what we can provide"
  category: non_commitment
  function: soft_defer
  speaker_role: presenter
  difficulty: 3
  context: "We'll talk and see what we can provide"
  note: "we'll talk and see" - 약속 없이 회신만 약속
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-06 07 59 44_EN_IBM meeting-extracted.wav` (총 ~60분, 7,798단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 25-56) | Patrick "our goal in pursuing CXL has been the hope to achieve a lower cost per gigabyte" + 현재 상태 | 발표 시작 목표 선언 + "hope to achieve" 화법 | ★★★ |
| 2 | 제약 공개 (line 84-99) | "It's not ideal in terms of the system design" + slot 수 설명 | 제약 공개 화법 - "not ideal" + "a little challenging" | ★★★ |
| 3 | 결정 시점 (line 80-83) | "we've got to make a decision this quarter" + "really interested in hearing from you" | 긴급성 + 정중한 요청 연결 | ★★★★ |
| 4 | 회피 대비 (line 200-201, 525-535) | SK "internal discussion phase" vs IBM "just starting to look at it" - 양측 회피 화법 비교 | 양측 회피 화법 대비 학습 | ★★★★ |
| 5 | 협상 마무리 (line 519-524, 548-553) | "that would be great if we can get that low" + "I think it was very comprehensive" | 협상 마무리 - 가능성 환영 + 회의 마무리 | ★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 4가 가장 가치 높음 - 결정 시점 화법·양측 회피 대비가 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **mutual technical disclosure + mutual probing** register다. 양쪽이 각자 CXL stance를 발표하고, 상대가 기술 Q&A로 도전하는 구조. 두 역할 모두 학습해야:
- **IBM 역할 (Patrick, Dave)**: 제약 솔직 공개, 결정 시점 명시, 정중한 요청 - 네가 buyer로 파트너에게 요구할 때
- **SK Hynix 역할 (Jerry, Steve)**: internal discussion 회피, 미래 약속, 비교 우위 전환 - 네가 supplier로 파트너의 요구에 대응할 때

### Pragmatics (화용론) 핵심
1. **제약의 솔직 공개**: 영어 회의에서 "It's not ideal"을 쓴다. "bad"가 아니라 "not ideal" - 전문가의 통제된 솔직함. 한국어로는 "좀 아쉽습니다"인데, 영어는 "not ideal"이 더 직접적이면서도 전문적. 제약을 숨기지 말고 공개하되 "not ideal"로 포장.
2. **"internal discussion phase"의 이중 기능**: "I cannot show the details"가 직접 거부라면, "it is still an internal discussion phase, so I cannot show the details"는 (a) 거부의 이유를 대고 (b) "but we will propose later"로 미래 약속을 붙인다. 거부 + 이유 + 미래 약속의 3단 구조.
3. **"just starting to look at it"의 초기 단계 프레이밍**: IBM이 관심은 있되 확약은 안 할 때 쓰는 화법. "We're really just starting" + "I'm not confident in any of the answers" + "But it's a possibility that we might be interested" - 3단 완화. 관심 표시 + 자신 없음 인정 + 가능성 시사.
4. **"apples to apples" 비교 회피**: 비교 수치를 못 줄 때 "I'm not sure we can compare apples to apples" - 비교 불가를 우아하게 선언. "we will calculate that"으로 노력 의지 표시.

### 네가 당장 써야 할 Top 5
1. **"It's not ideal in terms of the system design"** - 제약 솔직 공개
2. **"it is still an internal discussion phase, so I cannot show the details, but we will propose"** - 거부 + 미래 약속
3. **"we've got to make a decision this quarter, so we're really interested in hearing from you"** - 긴급성 + 요청
4. **"I'm not confident in any of the answers I'm giving here. But it's a possibility that we might be interested"** - 자신 없음 + 가능성
5. **"I'm not sure we can compare apples to apples, but we will calculate that"** - 비교 회피 + 노력 의지

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "좀 아쉽습니다" | "It's not ideal in terms of the system design" | 한국어는 "아쉽다"로 끝, 영어는 "not ideal" + 구체 제약 |
| "내부 논의 중이라 자세히는 못 드립니다" | "it is still an internal discussion phase, so I cannot show the details, but we will propose" | 영어는 거부 뒤 "but we will propose" 미래 약속 |
| "이번 분기에 결정해야 합니다" | "we've got to make a decision this quarter" | "got to"가 "need to"보다 절박 |
| "잘 모르겠습니다" | "I'm not confident in any of the answers I'm giving here" | 영어는 자신의 답변 전체 신뢰도를 낮춤 |
| "비교가 안 됩니다" | "I'm not sure we can compare apples to apples" | "apples to apples" - 같은 조건 비교 불가 |
| "시작 단계라서요" | "We're really just starting to look at it" | "just starting" - 초기 단계 프레이밍 |
| "계속될 겁니다" | "I don't see any reason why that would not continue" | 이중 부정으로 강한 확신 |
| "유망합니다" | "that sounds promising" | "good" 대신 "promising" - 신중한 긍정 |
| "괜찮습니다" | "I think it was very comprehensive" | 회의 마무리 - "comprehensive"가 전문가 평가 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 58개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 학습**: IBM 입장(buyer, 제약 공개 + 결정 시점)과 SK 입장(supplier, internal discussion 회피 + 미래 약속)을 번갈아 연습

---

*Textbook 25 - IBM CXL/Architecture Technical Deep-dive (2026-02-06). 회의 유형 A (technical deep-dive). 표현 DB 58개. 5개 발췌 구간. 작성: 2026-09-01.*
