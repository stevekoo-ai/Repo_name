---
textbook_id: 07
meeting: MSFT CXLpoolingDiscussion
date: 2026-07-09
type: A (기술 Deep-dive) - 후반 20%는 협상(joint POC next steps)
partner: Microsoft (Rajesh - executive sponsor, Ananda - architect, Samir - architect, Shambhi)
sk_side: Sangdong Lee (Research), Jerry (Product Planning), Jongyul Kim/JR Kim (AI System Research, Bay Area)
duration_words: 10825
audio: repo/webex-audio/2026-07-09 09 02 09_EN_MSFT_CXLpoolingDiscussion-extracted.wav
transcript: repo/webex-audio/2026-07-09 09 02 09_EN_MSFT_CXLpoolingDiscussion-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, microsoft, cxl, pooled-memory, kv-cache, ai-infra, joint-poc, technical-deepdive]
---

# Textbook 07 - MSFT CXLpoolingDiscussion (2026-07-09)

> **회의 유형**: A (기술 Deep-dive) - SK가 CXL pooled memory 연구를 깊이 발표, MS가 기술 Q&A로 도전, 후반에는 joint POC 협상
> **학습 가치**: L2 영어 발표자의 구조화 화법 + 원어민 질문자의 정중한 도전·회피·협상 화법
> **Audrey 관점**: 네가 SK 입장에서 MS에 기술 발표하고 협상하는 회의 - 발표자 화법(Sangdo/Jerry/JR)과 질문자 화법(Ananda/Rajesh/Samir) 둘 다 배워야. 특히 MS 측의 "정중한 회피"와 "추상화된 관심 표시"는 미국 대기업 파트너십 협상의 핵심

---

## 1. 발화 아키텍처 - SK 발표자의 4단계 + MS 질문자의 3단계

이 회의는 발표자(SK)와 질문자(MS)의 아키텍처가 다르다. 양쪽 모두 학습해야 - 네가 발표할 때는 SK 패턴, 네가 질문/평가할 때는 MS 패턴.

### 1A. SK 발표자의 4단계 (Sangdo → Jerry → Jongyul)

SK은 한 발표를 3명이 분담한다. 각 단계마다 **고정된 화법 공식**이 있다.

#### 단계 1: 챕터 분할 선언 (Chapter Declaration) - Sangdo

발표 시작 시 챕터 구조를 명시적으로 선언한다. 이게 SK 발표의 뼈대.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we prepared the X chapter, one is the Y, chapter two for the Z, and we'd like to talk about the W` | "we are SKNX prepared the three chapter one is the SKNX perspective about CXL and CXL for the system why that need and chapter two for the chapter two we would like to introduce the SKNX research" | 구조 선언 - 청중에게 roadmap 제시 |
| `could you go to next slide` | "could you go to next slide okay let's next" | 발표 제어 - 화면 전환 요청 |

**Audrey 교훈**: 영어 발표는 시작할 때 "we prepared the X chapter"로 구조를 먼저 보여준다. 청중이 "어디로 가는지" 알면 끝까지 듣는다. 한국어로는 "오늘 이런 내용 말씀드리겠습니다"인데, 영어는 "we prepared three chapters, one is X, two is Y, three is Z"로 명시.

#### 단계 2: 문제 정량화 (Problem Quantification) - Jerry

문제를 "수학적 계산"으로 프레이밍. "어렵다"가 아니라 "300 users × 3 sessions = 900, requires so many memory"로.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we have assumption, there are X users with Y sessions, it requires so many the Z` | "we have assumption I mean there are 300 users yeah with the three sessions at the same time 900 sessions it requires so many the memory capacity" | 정량화된 문제 - 숫자로 위기감 |
| `if the user wanted to have the X, it is more than the tons of Y` | "if the user wanted to have the I mean long long context ranks... it is more than the I mean I mean tons of terabyte" | "tons of X" - 비전문가 수치 과장 |
| `our conclusion is that it needs for the new X to handle that` | "our conclusion is that the it needs for the new memory key year to I mean handle that" | "our conclusion is" - 권위 부여 |

**Audrey 교훈**: "we have assumption, there are X users with Y sessions" - 가정을 명시하고 숫자로 도출. 이게 문제 프레이밍의 영어 공식. 한국어로는 "대충 이 정도 필요합니다"인데, 영어는 "we have assumption"으로 가정을 명시하고 숫자를 댄다. 단, "tons of terabyte"는 비격식 - 기술 발표에선 "on the order of terabytes"가 더 안전.

#### 단계 3: 솔루션-연구 연결 (Solution-to-Research Bridge) - Jerry → Jongyul

솔루션을 "research team will present"으로 연결. 발표자 교체가 자연스럽다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `our research team will present this one` | "we'd like to introduce the SKNX research so SKNX research team will present this one" | 발화자 교체 - "research team will present" |
| `could you please kick off the meeting?` | "Sangdo, could you please kick off the meeting?" | "kick off" - 회의 시작 공식 |
| `could you please...` (명령형 부드럽게) | "could you please kick off the meeting?" / "could you go to next slide" | "could you please" - 부드러운 지시 |

**Audrey 교훈**: 발표자 교체는 "X will present this one"로 깔끔하게. "Could you please kick off?"는 회의 시작을 부드럽게 지시하는 고급 화법.

#### 단계 4: 기술 딥다이브 (Technical Deep-Dive) - Jongyul

JR은 "my team is focusing on X"으로 시작, "we designed this Y"로 아키텍처를 공개, "we already demonstrated Z at last year FMS"로 증거를 댄다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `my team is focusing on X` | "my team is focusing on the sharing and how to share the data with the memory pool" | 팀 포커스 선언 |
| `we designed this X so in the X, so Y, we are trying to use Z` | "we designed this memory centered AI REC system so in the REC system so in the REC as a GPU and so the GPU and CPU server is a compute REC" | "we designed X so in X, Y" - 아키텍처 공개 |
| `we already demonstrated X at last year Y` | "we already demonstrated food memory based the keeping the sharing for the lm serving pd distribution mode at last year last year fms" | 증거 제시 - "already demonstrated at X" |
| `this year we will demonstrate X at Y` | "this year we are preparing the two is the AI system... we will demonstrate it in fms and ocp in this year" | 미래 증거 - "will demonstrate at X" |
| `we already submitted / published the paper` | "this mpi version we already submit already published the paper so i can share it after this meeting" | 학술 권위 - "published the paper" |

**Audrey 교훈**: "we already demonstrated at last year FMS" + "we will demonstrate at FMS and OCP this year" - 이 과거-미래 증거 pair가 연구의 신뢰성을 만든다. 한국어로는 "작년에도 했고 올해도 할 겁니다"인데, 영어는 "already demonstrated at X / will demonstrate at Y"로 학회/컨퍼런스명을 명시.

### 1B. MS 질문자의 3단계 (Ananda → Rajesh → Samir)

MS는 발표를 듣고 3단계로 도전한다. 이게 **네가 배워야 할 원어민 질문 아키텍처**.

#### 단계 1: 비교 트레이드오프 질문 (Comparative Trade-off Probe) - Ananda

Ananda는 "X versus Y in terms of Z"로 비교 질문을 만든다. 단일 질문이 아니라 **비교 프레임**을 먼저 설치.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `have you looked at the trade-offs between X versus Y in terms of Z?` | "have you looked at the trade-offs between sharing with a memory pool versus sharing with shared SSD storage in terms of performance" | 비교 질문 - "trade-offs between X versus Y in terms of Z" |
| `the reason I'm asking is that with X there is always like a Y limitation` | "the reason I'm asking is that with cxl pooling there is always like a radix limitation how much you can share" | "the reason I'm asking is" - 질문 의도 사전 설명 |
| `in the industry we see X as a primary Y, have you studied that?` | "in the industry we see shared storage as a primary KV cache offload right especially in the sharing context have you have you studied that" | "in the industry we see X" - 업계 관행으로 도전 |

**Audrey 교훈**: Ananda의 "have you looked at the trade-offs between X versus Y in terms of Z"는 황금 패턴이다. "X vs Y 비교해 봤어요?"가 아니라 "trade-offs between X versus Y in terms of Z"로 비교 축까지 명시. 그리고 "the reason I'm asking is"로 질문 의도를 먼저 설명 - 이게 공격 안 하면서 압박을 거는 화법. **이 패턴 3개는 무조건 외워라.**

#### 단계 2: 계층적 정보 공개 (Hierarchical Disclosure) - Rajesh

Rajesh는 "I don't know how much I can share honestly, but at the highest level what I can describe is..."로 정보 공개 한계를 먼저 표시하고, 그 다음 "the properties we look for are X, Y, Z"로 열거.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I don't know how much I can share honestly, but...` | "I don't know how much I can share honestly but because a lot of this is very detailed tco calculations" | 정보 한계 면책 - "honestly"로 정직함 표시 |
| `at the highest level what I can describe is that...` | "at the highest level what I can describe is that the properties we look for are..." | 계층 공개 - "highest level"로 범위 제한 |
| `the properties we look for are X, Y, Z` | "the properties we look for are hey can a workload scale its number of users... or can we oversubscribe the cpu resources... or can I use mix and match different types of memory" | "we look for" - 요구사항 추상화 |
| `those are probably the three big big areas` | "those are probably the three big big areas" | "probably" - 단정 피하기; "big big" - 구어 강조 |

**Audrey 교훈**: "I don't know how much I can share honestly, but at the highest level..." - 이게 미국 대기업 임원의 정보 공개 화법이다. "다 말할 수는 없지만, 최상위 수준에서 말하면..." - 한국어로는 "그건 좀 그렇고요"인데, 영어는 "I don't know how much I can share honestly"로 정직함을 먼저 보여주고 "at the highest level"로 범위를 제한. 그 다음 "the properties we look for are"로 추상화된 요구사항만 준다. **이 3단 공식은 협상에서 무조건 외워라.**

#### 단계 3: 추상화된 관심 표시 (Abstracted Interest) - Rajesh/Samir

MS는 "definitely interested"라고 말하되, 즉시 "we just need to jointly evaluate and see"로 조건을 건다. "yes"가 아니라 "yes, but explore".

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are definitely interested in the area` | "I think we are definitely interested in the in the area" | "definitely interested" - 강한 긍정 |
| `I think there is some potential in the right... we just need to jointly evaluate and see` | "I think there is some you know potential value or use cases that's that's very possible here right because your your your baseline is going to be what..." | "some potential" - 약한 긍정 + "jointly evaluate"로 조건 |
| `there are going to be a lot of trade-offs that are required` | "there are going to be a lot of trade-offs right that are required" | "trade-offs that are required" - 어려움 예고 |
| `what we just have to do is we have to just go through some exploration to find out how well can it work` | "what we just have to do is we have to just go through some exploration to find out you know how well can it work" | "go through exploration" - 비구체적 후속 |

**Audrey 교훈**: 미국 대기업의 "yes"는 "we are definitely interested" + "we just need to jointly evaluate and see"의 pair다. 긍정을 주되 즉시 조건을 건다. 한국어 "관심 있습니다, 같이 검토해 봅시다"와 동일한데, 영어는 "definitely"로 시작 강조하고 "just need to"로 약화한다. "yes"로 들리지만 실제로는 "maybe"다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 양쪽 다 약점을 정중하게 포장하는데, MS 쪽이 훨씬 세련됐다.

### 전략 1: L2 영어 과잉 hedge - "I mean" 남용 (SK 패턴, 학습하면 안 되는 패턴)

SK 발표자는 "I mean"을 과도하게 쓴다. 이건 Korean L1 interference - "그니까"의 직역. **이 패턴은 배우지 마라** - 하지만 상대방이 쓸 때 인식해야.

| 상황 | 원문 | 분석 |
|:---|:---|:---|
| 설명 도중 | "I mean we have assumption I mean there are 300 users yeah with the three sessions" | "I mean" 2회 / 1문장 - 설명 신뢰도 하락 |
| 제안 도중 | "I mean we are thinking of having the I mean four eight gpu server and I mean we can have a two the memory appliance" | "I mean" 3회 / 1문장 - 제안 확신 부족 표시 |

**Audrey 교훈**: 네가 발표할 때 "I mean"을 빼라. "I mean"이 빠지면 문장이 단정해진다. "I mean we are thinking of having four gpu servers" → "we are thinking of having four gpu servers" - 이게 원어민 화법. "I mean"은 "그니까"의 직역인데, 영어 원어민은 설명 중에 안 쓴다. 발표 전 녹음해서 "I mean" 개수 세봐라 - 1분에 3개 이상이면 신뢰 하락.

### 전략 2: 정중한 부정 - "I don't have any data" (SK 패턴)

데이터가 없을 때 SK는 "I don't have any idea or the data"로 직접 부정한다. 이건 약한 화법이다.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| NVMe 공유 데이터 질문 | "I don't have any the idea or the data I mean using the the NVMe for this sharing scenario" | "NVMe 공유 시나리오에 대한 아이디어나 데이터가 없습니다" |

**Audrey 교훈**: "I don't have any idea or the data"는 약하다. 더 나은 화법: "we haven't studied that specific scenario yet, but it's worth investigating" - 부정 + future value. 또는 "I can get you the data after the meeting" (Marvell textbook의 Ravi 패턴). 직접 부정은 신뢰를 깎는다.

### 전략 3: 정보 공개 한계 표시 (MS 패턴, 배워야 할 화법)

Rajesh는 "I don't know how much I can share honestly"로 정보 한계를 정직하게 표시. 이게 미국 대기업 임원의 회피 화법.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| TCO 계산 공유 요청 | "I don't know how much I can share honestly but because a lot of this is very detailed tco calculations or a total cost of ownership calculations that we do right" | "얼마나 공유할 수 있을지 모르겠습니다만, 이건 매우 상세한 TCO 계산이라서요" |
| 그 다음 계층적 공개 | "but at the highest level what I can describe is that the properties we look for are..." | "하지만 최상위 수준에서 말씀드리면, 저희가 보는 속성들은..." |

**패턴 공식**: `I don't know how much I can share honestly, but at the highest level what I can describe is that...`

**Audrey 교훈**: "I don't know how much I can share honestly" - "honestly"가 핵심이다. "I can't share"만 하면 거부지만, "I don't know how much I can share honestly"는 정직한 임원의 고민으로 들린다. 그 다음 "at the highest level"로 범위를 제한하고 "what I can describe is"로 공개 의지를 표시. 이 3단이 미국 대기업의 정직한 회피다. 한국어 "그 부분은 좀 그렇고요"의 영어 세련 버전.

### 전략 4: 비구체적 관심 표시 (MS 패턴)

MS는 "definitely interested" + "jointly evaluate"로 긍정과 조건을 pair로 쓴다. "yes"처럼 들리지만 후속 액션이 없다.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| 공동 POC 의향 질문 | "I think we are definitely interested in the in the area I think there is some potential in the right we just need to jointly evaluate and see because there are going to be a lot of trade-offs" | "그 분야에 분명히 관심 있습니다. 잠재력은 있는 것 같아요. 같이 평가해 봐야 할 것 같습니다. trade-off가 많이 필요할 것 같아서요" |

**패턴 공식**: `we are definitely interested in the area. I think there is some potential. we just need to jointly evaluate and see. there are going to be a lot of trade-offs.`

**Audrey 교훈**: "definitely interested"는 "yes"가 아니다. "jointly evaluate and see"가 핵심 - "evaluate"는 "검토하겠다"이고 "see"는 "지켜보겠다"이다. 둘 다 액션이 아니다. 그리고 "there are going to be a lot of trade-offs"로 어려움을 예고 - 이건 거절의 전조다. 미국 대기업이 "trade-offs가 많다"고 하면, "구체적 문제가 있는데 말하기 어렵다"는 뜻. 한국어 "검토해 보겠습니다"의 미국 대기업 버전이 "definitely interested, just need to evaluate, there are trade-offs"다.

### 전략 5: 결정 미루기 - "give us some time" (MS 패턴)

직접 결정을 피하면서 "시간을 달라"고 한다. 이게 정중한 보류.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| POC 의향 최종 질문 | "give us some time to think through it and then maybe yeah sure" | "시간을 좀 주세요, 생각해 보고, 어쩌면, 그럼요" |

**패턴 공식**: `give us some time to think through it and then maybe...`

**Audrey 교훈**: "give us some time to think through it" - "think through"가 핵심. "think"만 하면 가볍지만, "think through"는 "끝까지 생각하겠다"는 진지함. 그리고 "maybe"로 기대를 낮춘다. "yes"가 아니다. "생각해 보겠다"는 거절의 정중한 전단계다.

### 전략 6: 가설적 요구사항 진술 (Hypothetical Requirement) - Rajesh

요구사항을 직접 말하지 않고 "if there is a way where... that would be a lot more..."로 가설로 포장.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| GPU rack 분리 요구 | "if there is a way where this could be on a side rack or a side car rack or something that would be a lot more easily deployable or a bit more easier to deploy than if it is if we have to touch the compute server" | "만약 side rack이나 sidecar rack에 둘 수 있는 방법이 있다면, 그게 훨씬 배포하기 쉬울 것 같습니다. compute server를 만져야 한다면요" |

**패턴 공식**: `if there is a way where X could be Y, that would be a lot more Z than if we have to W.`

**Audrey 교훈**: "we want X on a side rack"이 직접 요구다. Rajesh는 "if there is a way where X could be on a side rack, that would be a lot more easily deployable"로 가설로 포장. "we want"이 아니라 "if there is a way" - 주어를 "we"에서 "way"로 빼서 압박을 줄인다. 그리고 "a lot more easily deployable"로 이유를 대준다. 이게 정중한 요구사항 진술의 황금 패턴이다.

### 전략 7: 5중 hedge - "I'm fairly sure we would want to maybe" (Rajesh)

강한 확신을 5개의 hedge로 감싼다. 이게 MS 임원의 "확실한 요구를 정중하게" 화법.

| 상황 | 원문 | 번역 |
|:---|:---|:---|
| GPU rack 분리 확신 | "I'm fairly sure that we would want to maybe get to a solution where the pooled appliance is not on the on the gpu" | "저희가 pooled appliance가 GPU rack에 있지 않은 솔루션으로 가고 싶을 거라고 꽤 확신합니다, 어쩌면" |

**패턴 공식**: `I'm fairly sure that we would want to maybe get to a solution where X is not Y.`

**Audrey 교훈**: "fairly sure" + "would want to" + "maybe" + "get to" - 4개 hedge. 그리고 "not on the gpu"로 명확한 요구. 이게 "확신 + 정중함"의 영어 화법이다. 한국어 "아마 그렇게 될 것 같긴 한데요"와 비슷한데, 영어는 hedge 4개를 chain으로 쓴다. **이 패턴은 네가 강한 요구를 정중하게 할 때 써라.**

---

## 3. 정중한 도전 화법 (Polite Challenge Patterns)

이 회의에서 MS가 SK에게 기술적으로 도전하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 비교 트레이드오프 질문 (Comparative Trade-off Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `have you looked at the trade-offs between X versus Y in terms of Z?` | "have you looked at the trade-offs between sharing with a memory pool versus sharing with shared SSD storage in terms of performance" | 비교 축 명시 - "trade-offs between X versus Y in terms of Z" |

**Audrey 교훈**: "X vs Y 비교했나요?"가 아니라 "trade-offs between X versus Y in terms of Z"로 비교 축까지 명시. "in terms of performance" - 어떤 관점에서 비교할지를 질문자가 정한다. 이게 정중하면서도 깊은 도전이다.

### 질문 유형 2: 질문 의도 사전 설명 (Reason Prefacing)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the reason I'm asking is that with X there is always like a Y limitation` | "the reason I'm asking is that with cxl pooling there is always like a radix limitation how much you can share right" | 질문 전 의도 설명 - 공격적 뉘앙스 제거 |
| `is it really X or are they looking at Y? the reason I'm asking is that...` | "is it really cxl pooled memory people are looking at or are they looking at network attached memory appliance the reason I'm asking is that with cxl pooling there is always like a radix limitation" | 질문 + 이유 - 구조화된 도전 |

**Audrey 교훈**: "the reason I'm asking is"는 황금 패턴이다. 질문을 하기 전에 "왜 묻는지"를 먼저 설명하면, 상대방은 "이 사람이 도전하나?"가 아니라 "이 사람이 맥락을 알고 있구나"라고 느낀다. 그리고 질문이 더 날카로워도 정중하게 들린다. **"the reason I'm asking is"는 무조건 외워라.**

### 질문 유형 3: 업계 관행으로 도전 (Industry-Norm Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `in the industry we see X as a primary Y, have you studied that?` | "in the industry we see shared storage as a primary KV cache offload right especially in the sharing context have you have you studied that" | "in the industry we see" - 업계 관행으로 도전 |

**Audrey 교훈**: "in the industry we see X" - "업계에서는 X를 봅니다" - 자기 회사 의견이 아니라 "업계"로 권위를 빌린다. "have you studied that"로 상대의 연구 범위를 시험. 이게 직접 "왜 안 했나요?" 대신 "업계에서는 이렇게 하는데 연구하셨나요?"로 정중하게 도전.

### 질문 유형 4: 구조 분해 요청 (Structured Decomposition Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `let's just say X, that's one level of comparison. then the question you mentioned Y, Z is a different comparison` | "let's just say memory media based KV cache offload whether you access it over ethernet or whether you access it over CXL that's one level of comparison right then the question you mentioned in your previous slide that well the capacities are too big... that's a different comparison perhaps" | 비교 축 분해 - "one level of comparison / a different comparison" |

**Audrey 교훈**: "let's just say X, that's one level of comparison. then Y is a different comparison" - 혼란스러운 비교를 두 축으로 분해. 이게 기술 토론에서 "우리가 뭘 비교하고 있는지 정리합시다"의 정중한 화법. "let's just say"로 가정을 설정하고 "that's one level"로 축을 명시. 이게 회의에서 혼란을 잡는 원어민 기술.

### 질문 유형 5: 설명 재요청 (Re-explanation Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `could you explain the X piece as well please?` | "I just want to make sure I'm the fundamentals if you go back to the not the CXL piece could you explain the RDMA piece as well please" | "could you explain X as well please" - 정중한 재설명 요청 |
| `is this a what maybe a X from the Y?` | "is this a what maybe a bi-16 CXL connectivity from the from the CPU on each GPU server connected to a CXL switch" | "is this a what maybe a X" - 추측성 확인 |

**Audrey 교훈**: "could you explain X as well please" - "as well"이 부드럽게 만든다. "explain X"만 하면 명령이지만, "as well please"는 "추가로 설명해 주세요"로 정중. "is this a what maybe a X"는 JR의 영어를 이해 못 했을 때 "혹시 X인가요?"로 추측하면서 확인 - 직접 "이해 못 했습니다"보다 세련.

### 질문 유형 6: 직접 spec 질문 (Direct Spec Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `what is typically the radix of the switch` | "what is typically the radix of the switch what are you guys and this is still within the rack oh yeah in the red in the rack and what connecting what up to eight servers something like that" | "what is typically X" - 전형적 수치 질문 |
| `is this still within the rack?` | "and this is still within the rack oh yeah" | "still within the rack" - 범위 확인 |
| `do you not interleave memory between the devices?` | "when you do this uh behind the switch do you not interleave memory between the devices uh I mean you are talking about the some kind of a management tier the management uh no I just meant like you have a cxl switch you have the cxl devices behind the switch do you interleave memory between them or no" | "do you not interleave X" - 부정 의문문으로 도전 |

**Audrey 교훈**: "do you not interleave X?" - 부정 의문문은 "왜 안 하죠?"의 정중 버전. "do you interleave?"보다 더 도전적이다. "왜 안 했나요?"를 "do you not X?"로 포장. 그리고 "is this still within the rack?"은 범위 확인 - 발표자가 암시하는 범위를 명시적으로 끌어낸다.

### 질문 유형 7: 이해 확인 - "is that what you're thinking?" (Samir)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `so you said X, is that mean you will Y? is that what you're thinking?` | "so are you so you said in-house silicon you're thinking about developing right is that mean you will build your own switch or switch less is it is that what you're thinking" | "is that what you're thinking" - 의도 확인 |
| `so you're talking about the X but perhaps in-house Y, right?` | "so you're talking about the third party switch but perhaps in-house expansion slash you know uh hybrid and devices right these devices this one hybrid time yeah" | "you're talking about X but perhaps Y" - 요약 + 확인 |

**Audrey 교훈**: "is that what you're thinking?" - 상대의 모호한 발언을 명확히 할 때. Samir는 Jerry의 "in-house silicon"이 모호하자 "is that what you're thinking?"로 의도를 끌어낸다. "무슨 뜻인가요?"보다 "is that what you're thinking?"이 정중.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

회의 후반, joint POC 협상과 action item을 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 의향 탐색 | SK | "are you willing to have a intention or interest working with the SK hynix" | "willing to have intention" - 직접 의향 질문 |
| 부드러운 긍정 | MS | "we are definitely interested in the area" | "definitely interested" - 강한 긍정 |
| 조건부 긍정 | MS | "we just need to jointly evaluate and see" | "jointly evaluate" - 공동 평가 |
| 어려움 예고 | MS | "there are going to be a lot of trade-offs that are required" | "trade-offs required" - 어려움 경고 |
| 정중한 보류 | MS | "give us some time to think through it and then maybe" | "give us some time" - 보류 |
| 가설적 요구 | MS | "if there is a way where this could be on a side rack... that would be a lot more easily deployable" | "if there is a way where X, that would be Y" - 가설적 요구 |
| 다중 hedge 요구 | MS | "I'm fairly sure that we would want to maybe get to a solution where the pooled appliance is not on the on the gpu" | "fairly sure / would want to / maybe / get to" - 4중 hedge 요구 |
| 일정 제안 | SK | "one proposal I think can have is like a flash memory submit coming and then maybe... you can have like some kind of meeting" | "one proposal I can have is X" - 일정 제안 |
| 후속 채널 | SK | "please share your feedback and opinion via email and whatever" | "share feedback via email" - 후속 채널 |

**Audrey 교훈**:
- "are you willing to have a intention or interest" - 한국어 "관심 있습니까?"의 직역. 원어민 화법은 "is there interest in exploring a joint POC?"가 자연스럽다. "willing to have intention"은 어색.
- "we are definitely interested" + "we just need to jointly evaluate" - 이 pair가 미국 대기업의 "정중한 maybe"다. 긍정과 조건을 같이 써서 "no"를 "yes, but"로 포장.
- "if there is a way where X, that would be Y" - 요구를 가설로 포장. **이게 가장 중요한 협상 화법이다.**

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 논문 공유 약속 | SK | "I can share it if you guys are interested" | "I can share it" - 비공식적 공유 약속 |
| 논문 요청 | MS | "Jerry please do send the papers right so we can read through them" | "please do send" - 강조 요청 |
| 논문 라우팅 | SK | "give it to sundown or me" / "give it to sundown and sundown oh yeah I'll give it to you" | "give it to X" - 수신자 명시 |
| 내부 논의 약속 | MS | "we can have our internal discussion about it" | "internal discussion" - 내부 논의 |
| FMS 미팅 제안 | SK | "I will talk to the Phyllis and having a conversation opportunity with the FMS" | "have a conversation opportunity at X" - 컨퍼런스 미팅 |
| booth 방문 요청 | SK | "if you are at FMS probably you can visit our booth and we can have either formal or informal chat" | "visit our booth" + "formal or informal chat" - 양쪽 옵션 제공 |

**Audrey 교훈**:
- "please do send" - "do"가 강조. "please send"보다 진지. "do send"는 "꼭 보내주세요"의 영어 버전.
- "give it to sundown or me" - 수신자를 명시하는 게 action item의 핵심. "I'll send"만 하면 책임이 안 드러나지만, "give it to X"는 누가 받을지 명시.
- "internal discussion about it" - MS는 "we'll discuss internally"로 내부 논의를 약속. 이게 "we'll decide"보다 비구체적이고 정중.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/AI infra/Memory pooling 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **CXL pooled memory** | CXL로 다수 노드가 공유하는 메모리 풀 | "is it really cxl pooled memory people are looking at" - Ananda가 개념 질문 |
| **CXL expansion vs pooling** | 단일 노드 메모리 확장 vs 다중 노드 공유 풀 | "right now we are predominantly doing cxl expansion you know we are exploring pooling" - Rajesh가 MS 현황 |
| **switchless / multi-headed** | CXL switch 없이 multi-port 컨트롤러로 직접 연결 | "the multi-headed port based on the memory pool appliance" - Jerry가 아키텍처 옵션 |
| **radix** | CXL switch의 포트 수 | "what is typically the radix of the switch" - Ananda가 spec 질문 |
| **stranded memory** | 사용 못 하고 남는 메모리 | "the one benefit from expansion to pooling is that we don't need to um have stranded memory" - Rajesh가 pooling 가치 |
| **KV cache** | LLM attention key-value 캐시 | "the explosive the KV cache and then we expect that the capacity or the amount of the kvcash I mean they are exceedingly the memory limitation" - Jerry가 문제 프레이밍 |
| **pre-fill / decode disaggregation** | LLM 추론 prefill 단계와 decode 단계를 물리적으로 분리 | "we can share the key value cache data between the pre-fill and decode dpu unit" - Jerry |
| **time to first token (TTFT)** | LLM 첫 토큰 생성 시간 | "the time to first token pretty much stays flat" - JR이 성과 지표 |
| **DPU** (Data Processing Unit) | 네트워크/스토리지 처리 전용 칩 | "their solution is based on DPU and SSD NVMe" - JR이 NVIDIA CMS 비교 |
| **RDMA** (Remote Direct Memory Access) | 원격 직접 메모리 접근 | "we will use a pooled memory based multiple multi-pass RDMA" - JR이 아키텍처 |
| **RDMA NIC** | RDMA 지원 네트워크 카드 | "each GPU server has RDMA network is an RDMA NIC" - JR |
| **NVMe over fabric** | 네트워크로 NVMe 블록 스토리지 접근 | "the blue field 2 cannot support the 32 NVMe SSD" - JR이 POC 교훈 |
| **Blue Field DPU** | NVIDIA의 DPU 제품 | "this box is a blue field DPU based NVMe SSD array" - JR이 NVIDIA CMS 설명 |
| **DAX interface / DAX file system** | 직접 접근 가능한 파일 시스템 인터페이스 | "our food memory is very good with the DAX interface" - JR이 메모리 노출 방식 |
| **in-memory store** | 메모리 기반 key-value/object 저장소 | "we designed a very simple and very fast kibiru interface for the food memory" - JR이 자체 개발 |
| **Redis** | 오픈소스 in-memory key-value store | "we are very high bandwidth compared with the redis" - JR이 벤치마크 |
| **Mooncake** | KV cache 분리 저장 시스템 (Chinese) | "distributed mucade is a mucade is a in-memory idma-based distributed dm storage" - JR이 비교 |
| **NVIDIA Dynamo** | NVIDIA의 LLM 서비스 프레임워크 | "we quickly integrate this gtc dynamo with our is a mass platform" - JR이 통합 |
| **HBM** (High Bandwidth Memory) | GPU 고대역 메모리 | "GPU HBM data can copy to the sensor memory directly by using the RDMA" - JR |
| **DDR5 RDIM** | 서버 메모리 (DDR5 registered DIMM) | "we can accommodate the lp ddr and the ddr five RDIM" - Jerry가 메모리 옵션 |
| **LPDDR** | 저전력 모바일 DRAM | "lp ddr has the very good advantage I mean such as the the density and at the power perspective" - Jerry |
| **memory semantic SSD** | 블록이 아닌 메모리语义로 접근하는 SSD | "what is the difference between a memory semantic SSD versus a traditional NVMe block based" - Ananda |
| **PNM** (Processing-in-Near-Memory) | 메모리 근접 처리 | "we can plug in our the near memory processing the cxl memory motor" - Jerry가 가치 부가 |
| **TCO** (Total Cost of Ownership) | 총 소유 비용 | "a lot of this is very detailed tco calculations" - Rajesh |
| **oversubscribe** | 자원을 명목 용량 초과로 할당 | "can we oversubscribe the cpu resources or computer sources if I had more memory" - Rajesh가 가치 |
| **MPI** (Message Passing Interface) | 분산 메모리 병렬 컴퓨팅 표준 | "we are trying to add the this mpi over the sacks of memory pool to the mpi standard" - JR이 표준화 |
| **MPI standard** | MPI 국제 표준 | "the mpi standard has a signed documentation" - JR |
| **lock** / **internal locking** | 다중 노드 데이터 동기화 락 | "in the food memory with the multiple servers we cannot use a hardware atomic operation that means we cannot use advanced the software rock skin" - JR이 기술 과제 |
| **hardware atomic** | 하드웨어 수준 원자 연산 | "we cannot use a hardware atomic operation" - JR |
| **multi-tenant / multi-turn** | 다중 테넌트 / 다중 대화 | "this is a multi-tone scenario multi-tone scenario so every term second term can be used the first tons of kvc cache" - JR이 KV cache 재사용 |
| **FMS** (Flash Memory Summit) | 플래시 메모리 산업 컨퍼런스 | "we will demonstrate it in fms and ocp in this year" - JR이 로드맵 |
| **OCP** (Open Compute Project) | 오픈 하드웨어 표준화 단체 | "we will demonstrate it in fms and ocp" - JR |
| **POC** (Proof of Concept) | 개념 증명 | "we already have the that uh the pnm device the xl memory and hybrid as the the poc the product" - Jerry |
| **sidecar rack / side rack** | GPU rack과 분리된 보조 rack | "if there is a way where this could be on a side rack or a side car rack" - Rajesh가 배포 요구 |
| **x16 Gen6** | CXL PCIe x16 6세대 대역폭 | "we probably can get away with a single by 16 gen 6 bandwidth per server" - Rajesh가 대역 요구 |
| **nanosecond latency** | 나노초 지연 | "if there was a technology that allows us to get to somewhere within the 300 nanoseconds to 350 nanoseconds I think that would be ideal" - Rajesh가 일반용 lat 요구 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m07-001
  expression: "we prepared the X chapter, one is Y, chapter two is Z, and we'd like to talk about W"
  category: presentation_structure
  function: chapter_declaration
  speaker_role: presenter
  difficulty: 4
  context: "we are SKNX prepared the three chapter one is the SKNX perspective about CXL and CXL for the system why that need and chapter two for the chapter two we would like to introduce the SKNX research"
  note: 발표 구조 선언 - 청중에게 roadmap 제시. SK 발표 시작 공식

- id: m07-002
  expression: "could you please kick off the meeting?"
  category: meeting_control
  function: polite_directive
  speaker_role: presenter
  difficulty: 3
  context: "Sangdo, could you please kick off the meeting?"
  note: "kick off" - 회의 시작 공식. "could you please"로 부드럽게

- id: m07-003
  expression: "could you go to next slide"
  category: presentation_control
  function: slide_transition
  speaker_role: presenter
  difficulty: 2
  context: "could you go to next slide okay let's next"

- id: m07-004
  expression: "our research team will present this one"
  category: speaker_handoff
  function: presenter_transition
  speaker_role: presenter
  difficulty: 3
  context: "we'd like to introduce the SKNX research so SKNX research team will present this one"
  note: 발표자 교체 - "X will present this one"

- id: m07-005
  expression: "we have assumption, there are X users with Y sessions, it requires so many the Z"
  category: problem_quantification
  function: numeric_framing
  speaker_role: presenter
  difficulty: 4
  context: "we have assumption I mean there are 300 users yeah with the three sessions at the same time 900 sessions it requires so many the memory capacity"
  note: 가정 명시 + 숫자 도출. "we have assumption"으로 가정 표시

- id: m07-006
  expression: "it is more than the tons of X"
  category: scale_emphasis
  function: magnitude_stating
  speaker_role: presenter
  difficulty: 3
  context: "it is more than the I mean I mean tons of terabyte"
  note: "tons of" - 비격식 과장. 기술 발표에선 "on the order of X"가 안전

- id: m07-007
  expression: "our conclusion is that it needs for the new X to handle that"
  category: conclusion_stating
  function: solution_framing
  speaker_role: presenter
  difficulty: 4
  context: "our conclusion is that the it needs for the new memory key year to I mean handle that"
  note: "our conclusion is" - 권위 부여 발화

- id: m07-008
  expression: "my team is focusing on X"
  category: team_focus
  function: scope_declaration
  speaker_role: presenter
  difficulty: 3
  context: "my team is focusing on the sharing and how to share the data with the memory pool"

- id: m07-009
  expression: "we designed this X so in the X, so Y, we are trying to use Z"
  category: architecture_unveil
  function: design_description
  speaker_role: presenter
  difficulty: 4
  context: "we designed this memory centered AI REC system so in the REC system so in the REC as a GPU and so the GPU and CPU server is a compute REC"

- id: m07-010
  expression: "we already demonstrated X at last year Y"
  category: evidence_past
  function: credibility_stating
  speaker_role: presenter
  difficulty: 4
  context: "we already demonstrated food memory based the keeping the sharing for the lm serving pd distribution mode at last year last year fms"
  note: 과거 증거 - "already demonstrated at X". 학회/컨퍼런스명 명시

- id: m07-011
  expression: "this year we will demonstrate X at Y"
  category: evidence_future
  function: roadmap_stating
  speaker_role: presenter
  difficulty: 3
  context: "we will demonstrate it in fms and ocp in this year"
  note: 미래 증거 - 과거-미래 증거 pair로 신뢰성 구축

- id: m07-012
  expression: "we already submitted / published the paper"
  category: academic_credibility
  function: publication_evidence
  speaker_role: presenter
  difficulty: 4
  context: "this mpi version we already submit already published the paper so i can share it after this meeting"

- id: m07-013
  expression: "i can share it after this meeting if you are interested"
  category: follow_up_offer
  function: paper_sharing
  speaker_role: presenter
  difficulty: 3
  context: "i can share it after this meeting if you are interested"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m07-014
  expression: "I don't know how much I can share honestly, but at the highest level what I can describe is..."
  category: hierarchical_disclosure
  function: info_boundary_polite
  speaker_role: questioner
  difficulty: 5
  context: "I don't know how much I can share honestly but because a lot of this is very detailed tco calculations... at the highest level what I can describe is that the properties we look for are"
  note: 미국 대기업 임원의 정중한 정보 한계 표시. "honestly" + "at the highest level" 3단 공식

- id: m07-015
  expression: "the properties we look for are X, Y, Z"
  category: requirement_abstraction
  function: abstracted_requirement
  speaker_role: questioner
  difficulty: 5
  context: "the properties we look for are hey can a workload scale its number of users or can we oversubscribe the cpu resources or can I use mix and match different types of memory"
  note: "we look for" - 요구사항 추상화. 구체 수치 대신 속성으로 공개

- id: m07-016
  expression: "those are probably the three big big areas"
  category: enumeration_close
  function: list_summary
  speaker_role: questioner
  difficulty: 3
  context: "those are probably the three big big areas"
  note: "probably" - 단정 피하기; "big big" - 구어 강조

- id: m07-017
  expression: "we are definitely interested in the area"
  category: soft_interest
  function: positive_without_commitment
  speaker_role: questioner
  difficulty: 4
  context: "I think we are definitely interested in the in the area"
  note: "definitely interested" - 강한 긍정이지만 "yes" 아님

- id: m07-018
  expression: "I think there is some potential, we just need to jointly evaluate and see"
  category: hedged_enthusiasm
  function: conditional_positive
  speaker_role: questioner
  difficulty: 5
  context: "I think there is some you know potential value or use cases that's that's very possible here right... we just need to jointly evaluate and see"
  note: "some potential" + "jointly evaluate" - 긍정 + 조건 pair

- id: m07-019
  expression: "there are going to be a lot of trade-offs that are required"
  category: difficulty_warning
  function: obstacle_foreshadow
  speaker_role: questioner
  difficulty: 4
  context: "there are going to be a lot of trade-offs right that are required"
  note: "trade-offs required" - 거절 전조. 미국 대기업 "어렵다"는 신호

- id: m07-020
  expression: "what we just have to do is we have to just go through some exploration to find out how well can it work"
  category: vague_followup
  function: non_specific_next
  speaker_role: questioner
  difficulty: 4
  context: "what we just have to do is we have to just go through some exploration to find out you know how well can it work"
  note: "go through exploration" - 비구체적 후속. "we'll decide"보다 모호

- id: m07-021
  expression: "give us some time to think through it and then maybe"
  category: polite_defer
  function: decision_delay
  speaker_role: questioner
  difficulty: 4
  context: "give us some time to think through it and then maybe yeah sure"
  note: "think through" - 진지한 보류. "maybe"로 기대 낮춤

- id: m07-022
  expression: "if there is a way where X could be Y, that would be a lot more Z than if we have to W"
  category: hypothetical_requirement
  function: polite_demand_via_hypothesis
  speaker_role: questioner
  difficulty: 5
  context: "if there is a way where this could be on a side rack or a side car rack or something that would be a lot more easily deployable... than if it is if we have to touch the compute server"
  note: 가설적 요구 - "we want X"를 "if there is a way where X"로 포장. 황금 패턴

- id: m07-023
  expression: "I'm fairly sure that we would want to maybe get to a solution where X is not Y"
  category: multi_hedge_requirement
  function: hedged_firm_demand
  speaker_role: questioner
  difficulty: 5
  context: "I'm fairly sure that we would want to maybe get to a solution where the pooled appliance is not on the on the gpu"
  note: 4중 hedge + 명확 요구. "fairly sure / would want to / maybe / get to"

- id: m07-024
  expression: "I don't have any the idea or the data"
  category: weak_negation
  function: direct_admission
  speaker_role: presenter
  difficulty: 2
  context: "I don't have any the idea or the data I mean using the the NVMe for this sharing scenario"
  note: 약한 화법 - 배우지 마라. "we haven't studied that yet"이 안전

- id: m07-025
  expression: "I mean X" (과잉 hedge)
  category: l2_disfluency
  function: korean_l1_interference
  speaker_role: presenter
  difficulty: 1
  context: "I mean we have assumption I mean there are 300 users yeah with the three sessions"
  note: 한국어 "그니까" 직역. 발표에서 빼야 할 패턴. 학습 가치 낮음

# ── 정중한 도전 (Polite Challenge) ──
- id: m07-026
  expression: "have you looked at the trade-offs between X versus Y in terms of Z?"
  category: comparative_probe
  function: trade_off_question
  speaker_role: questioner
  difficulty: 5
  context: "have you looked at the trade-offs between sharing with a memory pool versus sharing with shared SSD storage in terms of performance"
  note: 비교 축 명시 질문. 황금 패턴. 무조건 외울 것

- id: m07-027
  expression: "the reason I'm asking is that with X there is always like a Y limitation"
  category: reason_prefacing
  function: intent_explanation
  speaker_role: questioner
  difficulty: 5
  context: "the reason I'm asking is that with cxl pooling there is always like a radix limitation how much you can share"
  note: 질문 의도 사전 설명. "the reason I'm asking is" 황금 패턴

- id: m07-028
  expression: "in the industry we see X as a primary Y, have you studied that?"
  category: industry_norm_challenge
  function: authority_borrow
  speaker_role: questioner
  difficulty: 5
  context: "in the industry we see shared storage as a primary KV cache offload right especially in the sharing context have you have you studied that"
  note: "in the industry we see" - 업계 권위로 도전

- id: m07-029
  expression: "let's just say X, that's one level of comparison. then the question Y is a different comparison"
  category: structured_decomposition
  function: axis_clarification
  speaker_role: questioner
  difficulty: 5
  context: "let's just say memory media based KV cache offload... that's one level of comparison right then the question you mentioned in your previous slide... that's a different comparison perhaps"
  note: 비교 축 분해 - 혼란 잡는 원어민 기술

- id: m07-030
  expression: "could you explain the X piece as well please?"
  category: re_explanation_request
  function: polite_clarification
  speaker_role: questioner
  difficulty: 4
  context: "could you explain the RDMA piece as well please"
  note: "as well please" - 부드러운 재설명 요청

- id: m07-031
  expression: "is this a what maybe a X from the Y?"
  category: tentative_guess
  function: hypothesis_check
  speaker_role: questioner
  difficulty: 3
  context: "is this a what maybe a bi-16 CXL connectivity from the from the CPU on each GPU server connected to a CXL switch"
  note: "what maybe" - 추측성 확인. 이해 못 했을 때 세련된 질문

- id: m07-032
  expression: "what is typically the X?"
  category: direct_spec_probe
  function: typical_value_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "what is typically the radix of the switch what are you guys"
  note: "typically" - 일반적 수치 질문

- id: m07-033
  expression: "is this still within the rack?"
  category: scope_check
  function: boundary_confirm
  speaker_role: questioner
  difficulty: 2
  context: "and this is still within the rack oh yeah in the red in the rack"
  note: 범위 확인 - 발표자가 암시하는 범위 끌어내기

- id: m07-034
  expression: "do you not interleave X between the devices?"
  category: negative_interrogative
  function: challenge_via_negation
  speaker_role: questioner
  difficulty: 4
  context: "do you not interleave memory between the devices uh... do you interleave memory between them or no"
  note: 부정 의문문 - "왜 안 하죠?"의 정중 버전

- id: m07-035
  expression: "so you said X, is that mean you will Y? is that what you're thinking?"
  category: intent_check
  function: ambiguous_clarification
  speaker_role: questioner
  difficulty: 4
  context: "so you said in-house silicon you're thinking about developing right is that mean you will build your own switch or switch less is it is that what you're thinking"
  note: "is that what you're thinking" - 모호한 발언 명확화

- id: m07-036
  expression: "you're talking about the X but perhaps in-house Y, right?"
  category: summary_check
  function: paraphrase_confirm
  speaker_role: questioner
  difficulty: 4
  context: "so you're talking about the third party switch but perhaps in-house expansion slash you know uh hybrid and devices right"

- id: m07-037
  expression: "I just want to make sure I'm the fundamentals"
  category: comprehension_preface
  function: polite_intro
  speaker_role: questioner
  difficulty: 3
  context: "I just want to make sure I'm the fundamentals if you go back to the not the CXL piece could you explain the RDMA piece"
  note: "make sure I'm the fundamentals" - 문법 어색. "make sure I understand the fundamentals"이 자연

- id: m07-038
  expression: "is it really X or are they looking at Y?"
  category: either_or_probe
  function: disjunctive_question
  speaker_role: questioner
  difficulty: 4
  context: "is it really cxl pooled memory people are looking at or are they looking at network attached memory appliance"
  note: "is it X or Y" - 이분법 질문으로 개념 분리

- id: m07-039
  expression: "do you have any question"
  category: question_invitation
  function: turn_yield
  speaker_role: presenter
  difficulty: 2
  context: "so yeah do you have any question"

# ── 협상·액션 (Negotiation) ──
- id: m07-040
  expression: "are you willing to have a intention or interest working with X"
  category: direct_interest_probe
  function: willingness_question
  speaker_role: presenter
  difficulty: 3
  context: "are you willing to have a intention or interest i mean working with the sSSK hynix"
  note: 한국어 직역 - "willing to have intention" 어색. "is there interest in exploring X"이 자연

- id: m07-041
  expression: "one proposal I think can have is like a X coming"
  category: proposal_framing
  function: schedule_suggestion
  speaker_role: presenter
  difficulty: 4
  context: "one proposal I think can have is like a flash memory submit coming and then maybe"
  note: "one proposal I can have is X" - 일정 제안 공식

- id: m07-042
  expression: "please share your feedback and opinion via email"
  category: follow_up_channel
  function: async_commitment
  speaker_role: presenter
  difficulty: 3
  context: "please share your feedback and opinion yeah via email and whatever"

- id: m07-043
  expression: "Jerry please do send the papers"
  category: emphatic_request
  function: action_item_emphasis
  speaker_role: questioner
  difficulty: 3
  context: "Jerry please do send the papers right so we can read through them and think more about the work you have done"
  note: "do send" - "do" 강조. "please send"보다 진지

- id: m07-044
  expression: "give it to sundown or me"
  category: recipient_specify
  function: action_item_routing
  speaker_role: questioner
  difficulty: 2
  context: "give it to sundown or me"
  note: 수신자 명시 - action item 책임 명시

- id: m07-045
  expression: "we can have our internal discussion about it"
  category: internal_discussion
  function: non_commital_next
  speaker_role: questioner
  difficulty: 3
  context: "yeah we can i mean we can i mean have our internal discussion about it yeah after"
  note: "internal discussion" - "we'll decide"보다 비구체적이고 정중

- id: m07-046
  expression: "if you are at X, probably you can visit our booth and we can have either formal or informal chat"
  category: conference_meeting
  function: dual_option_invitation
  speaker_role: presenter
  difficulty: 4
  context: "if you are at fms probably you can you can like a fingers are you uh visit our booth and we can have either formula in formal chat chat"
  note: "formal or informal chat" - 양쪽 옵션 제공으로 부담 낮춤

- id: m07-047
  expression: "I will talk to the X and having a conversation opportunity with Y"
  category: meeting_scheduling
  function: contact_initiative
  speaker_role: presenter
  difficulty: 3
  context: "I will talk to the p-leaf p-leaf and i mean having a conversation opportunity with the fms"

- id: m07-048
  expression: "we will finalize our plan to make that those kind of the poc"
  category: plan_commitment
  function: future_action
  speaker_role: presenter
  difficulty: 3
  context: "we will i mean finalize our the plan i mean to i mean make that uh those kind of the poc uh indeed the system perspective"

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m07-049
  expression: "right now we are predominantly doing X, we are exploring Y"
  category: current_state
  function: status_quo_disclose
  speaker_role: questioner
  difficulty: 4
  context: "right now we are predominantly doing cxl expansion you know we are exploring pooling"
  note: "predominantly doing X, exploring Y" - 현재 + 탐색 pair

- id: m07-050
  expression: "the one benefit from X to Y is that we don't need to have Z"
  category: benefit_stating
  function: value_articulation
  speaker_role: questioner
  difficulty: 4
  context: "the one benefit from expansion to pooling is that we don't need to um have stranded memory"
  note: "benefit from X to Y" - 전환 가치 명시

- id: m07-051
  expression: "if there was a technology that allows us to get to somewhere within X, I think that would be ideal for Y"
  category: spec_target
  function: requirement_via_hypothesis
  speaker_role: questioner
  difficulty: 5
  context: "if there was a technology that allows us to get to somewhere within the 300 nanoseconds to 350 nanoseconds I think that would be ideal for the general purpose use cases"
  note: "if there was a technology that allows us to get to X, that would be ideal" - 가설적 spec 요구

- id: m07-052
  expression: "we probably can get away with a single by 16 gen 6 bandwidth per server"
  category: requirement_estimate
  function: tentative_spec
  speaker_role: questioner
  difficulty: 4
  context: "right now we are assuming we probably can get away with a single by 16 gen 6 bandwidth per server or per socket"
  note: "get away with X" - 최소 요구 표현. "probably can get away with" - 2중 hedge
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-07-09 09 02 09_EN_MSFT_CXLpoolingDiscussion-extracted.wav` (총 10,825단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | line range | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입부 | line 1-13 | 자기소개 + Rajesh "definitely looking forward to this interesting discussion" | 회의 시작 화법 + 임원 인사 | ★★☆ |
| 2 | 문제 프레이밍 | line 17-25 | Jerry "we have assumption, 300 users with 3 sessions" + KV cache 정량화 | 정량화된 문제 프레이밍 + L2 영어 패턴 인식 | ★★★ |
| 3 | MS 비교 질문 | line 35-37, 47-48 | Ananda "trade-offs between memory pool versus shared SSD in terms of performance" + "the reason I'm asking is" | 비교 트레이드오프 질문 + 질문 의도 사전 설명 | ★★★★ |
| 4 | MS 정보 한계 | line 224-228 | Rajesh "I don't know how much I can share honestly, at the highest level what I can describe is..." | 계층적 정보 공개 - 미국 대기업 임원 회피 화법 | ★★★★★ |
| 5 | 협상 마무리 | line 230-237, 274-278 | Rajesh "definitely interested" + "if there is a way where this could be on a side rack" + "fairly sure we would want to maybe get to" | 정중한 긍정 + 가설적 요구 + 4중 hedge 요구 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - MS 회피/협상 화법이 밀집
- 발췌 2는 L2 영어 패턴을 인식하는 용도 - "I mean" 빼고 연습

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **technical pitch (SK) + polite evaluation (MS)** register다. 발표자와 질문자의 영어 수준이 다르다:
- **SK 발표자 (Sangdo/Jerry/JR)**: L2 영어 - "I mean" 과다, 어색한 직역 ("willing to have intention"), 하지만 기술 내용은 깊고 구조화됨. 발표 구조(챕터 분할, 정량화, 증거 제시)는 배울 점.
- **MS 질문자 (Ananda/Rajesh/Samir)**: 원어민 - 세련된 hedge, 계층적 공개, 가설적 요구. **이 회의의 진짜 학습 가치는 MS 쪽 화법이다.**

### Pragmatics (화용론) 핵심
1. **"definitely interested" ≠ "yes"**: MS는 "we are definitely interested in the area" + "we just need to jointly evaluate and see"를 pair로 쓴다. 긍정 + 조건 - "no"를 "yes, but"로 포장. 이게 미국 대기업의 "정중한 maybe"다. **"definitely"는 커밋이 아니다.**
2. **"I don't know how much I can share honestly"**: 정보 한계를 정직하게 표시. "I can't share"는 거부지만 "I don't know how much I can share honestly"는 정직한 임원의 고민. "at the highest level"로 범위 제한.
3. **"if there is a way where X could be Y, that would be a lot more Z"**: 요구를 가설로 포장. "we want X"가 아니라 "if there is a way where X" - 주어를 "we"에서 "way"로 빼서 압박 감소. **이게 정중한 요구의 황금 패턴.**
4. **"the reason I'm asking is"**: 질문 의도 사전 설명. 도전적 질문을 정중한 확인으로 변환. **Marvell textbook의 "Just to make sure I understand correctly"와 pair로 외워라.**
5. **"trade-offs required"**: MS가 "어렵다"고 할 때 쓰는 신호. "no"를 "trade-offs"로 포장. 협상에서 상대가 "trade-offs"를 언급하면, 거절 전조로 들어라.

### 네가 당장 써야 할 Top 5
1. **"have you looked at the trade-offs between X versus Y in terms of Z?"** - 비교 질문 황금 패턴
2. **"the reason I'm asking is that..."** - 질문 의도 사전 설명
3. **"I don't know how much I can share honestly, but at the highest level..."** - 정보 한계 정중 표시
4. **"if there is a way where X could be Y, that would be a lot more Z"** - 가설적 요구
5. **"we are definitely interested, we just need to jointly evaluate and see"** - 정중한 maybe (상대방이 쓸 때 인식)

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "그건 좀 그렇고요" | "I don't know how much I can share honestly, but at the highest level..." | 정직함 표시 → 범위 제한 |
| "관심 있습니다" | "we are definitely interested, we just need to jointly evaluate and see" | "definitely" + 조건 pair |
| "다음에요" | "give us some time to think through it and then maybe" | "think through" 진지함 + "maybe" 기대 낮춤 |
| "왜 안 하죠?" | "do you not interleave X?" | 부정 의문문으로 정중 도전 |
| "X vs Y 비교했나요?" | "have you looked at the trade-offs between X versus Y in terms of Z?" | 비교 축까지 명시 |
| "X rack에 두고 싶어요" | "if there is a way where X could be on a side rack, that would be a lot more easily deployable" | 가설로 포장 |
| "그냥 보내주세요" | "Jerry please do send the papers" | "do" 강조로 진지함 |
| "내부에서 논의하겠습니다" | "we can have our internal discussion about it" | "internal discussion" - 비구체적 |
| "FMS에서 뵙죠" | "if you are at FMS, you can visit our booth and we can have either formal or informal chat" | 양쪽 옵션 제공 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법(MS 패턴) + 3절 도전 화법(Ananda) 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **L2 패턴 인식**: 2절 전략 1("I mean" 남용)은 배우지 말고 **인식**해라 - 네가 발표할 때 빼야 할 패턴
6. **MS 회피 화법 학습**: 2절 전략 3-7은 미국 대기업 파트너십 협상의 핵심 - 상대방이 "definitely interested" + "trade-offs required"를 쓸 때, "yes"가 아니라 "maybe"로 들어라

---

*Textbook 07 - MSFT CXLpoolingDiscussion (2026-07-09). 회의 유형 A (기술 Deep-dive) + 후반 협상. 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
