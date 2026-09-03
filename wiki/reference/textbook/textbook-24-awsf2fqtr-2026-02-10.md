---
textbook_id: 24
meeting: AWS F2F QTR Q1 2026
date: 2026-02-10
type: B (Roadmap/Supply Alignment)
partner: AWS (Ashik - TPM, David Derrick - CPU/Memory Perf & Quality, Sean Wang - Malta, others)
sk_side: Ellie (BCM Marketing), Sang-Woon (DRAM Product Planning), Eugene (Server MP), Jongwon, Sunny, SH, Sung-mook, Sung-kwang, Heeyoung, Hyun-soo, Pyeong-jin, Jerry, Bobby (Memory Quality)
duration_words: 15458
audio: repo/webex-audio/2026-02-10 09 04 53_EN_AWSF2FQTR_Q12026-extracted.wav
transcript: repo/webex-audio/2026-02-10 09 04 53_EN_AWSF2FQTR_Q12026-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, aws, quarterly-review, roadmap, supply, dram, hbm, rdim, mrdim, speed-negotiation, capacity-allocation, type-b]
---

# Textbook 24 - AWS F2F QTR Q1 2026 (2026-02-10)

> **회의 유형**: B (Roadmap/Supply Alignment) - 분기별 대면 회의에서 로드맵·공급·속도·용량·PMIC 벤더 조정
> **학습 가치**: 협상 언어(수량 요청, pull-in 요구, speed pushback), 공급 제약 회피 화법, 정중한 도전과 직접적 요구의 병행
> **Audrey 관점**: 이 회의는 "공급자(SK) vs 최고 고객(AWS)"의 전형. AWS가 공급을 요구하고 SK가 제약을 설명하는 구조. Ashik의 직접성과 SK의 정중한 회피가 함께 등장. 네가 AWS 입장(요구자)이든 SK 입장(공급자)이든 둘 다 배워야.

---

## 1. 발화 아키텍처 - 발표자·질문자 구조 (4단계 + 5단계)

이 회의는 한 명의 발표자가 아니라 **여러 SK 발표자가 번갈아 발표**하고, AWS의 Ashik이 주 질문자로 도전하는 구조. 각 역할마다 고정 화법 공식이 있다.

### SK 발표자 구조 (3단계)

#### 단계 1: 시장 상황 프레이밍 (Market Framing)

Ellie(BMC Marketing)이 시장 분위기를 프레이밍하며 시작. "수요가 폭증하는데 공급이 못 따라간다"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Starting in Q4 last year, we have seen a dramatic acceleration in X` | "Starting in Q4 last year, we have seen a dramatic acceleration in DRAM demand" | 시장 상황을 극적 표현("dramatic acceleration")으로 프레이밍 |
| `The key driver for this accelerated demand is X, which requires much more Y` | "The key driver for this accelerated demand is the emergence of agentic AI, which requires much more computing power" | 원인 규명 - "key driver"로 수요 증가의 정당성 부여 |
| `the total supply capacity has increased only by a single digit percent, compared to demand surging at mid-20 percent` | "the total supply capacity has increased only by a single digit percent, compared to demand surging at mid-20 percent" | 대비 구조 - "only by X, compared to Y surging at Z" - 공급 부족을 수치로 정당화 |

**Audrey 교훈**: 공급자가 "공급이 부족합니다"라고 말할 때, 단독으로 말하지 않는다. "수요는 mid-20% 증가인데 공급은 single digit%만 증가" - 숫자로 대비를 만들어 "어쩔 수 없다"를 프레이밍한다. 네가 공급 제약을 설명할 때 이 "대비 구조"를 써라.

#### 단계 2: 제약 나열 (Constraint Enumeration)

공급 제약을 2가지로 나열: "First of all... The second constraint is..."

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `First of all, there is a critical shortage of X` | "First of all, if you look at the left side, there is a critical shortage of clean room space" | 첫 번째 제약 - "critical shortage"으로 격상 |
| `The second constraint is X` | "The second constraint is HBM" | 두 번째 제약 - 명시적 나열 |
| `based on our current schedule, no new major fabs are anticipated to open until 2028` | "Based on our current schedule, no new major fabs are anticipated to open until 2028" | 시점 명시 - "until 2028"으로 장기 제약 강조 |
| `pulling in these schedules is structurally very difficult` | "pulling in these schedules is structurally very difficult" | "structurally very difficult" - 구조적 불가능함 강조 |

#### 단계 3: 노력 표명 (Effort Statement)

제약을 설명한 후, "we are making two kinds of efforts"로 노력을 표명.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are making two kinds of efforts` | "We are making two kinds of efforts" | 노력 나열의 시작 공식 |
| `The first one is to increase X through Y` | "The first one is to increase DRAM bit through Yongin Fab and our more CAPEX" | 첫 번째 노력 - CAPEX 투자 |
| `The second one is we are trying to make more X through Y` | "The second one is we are trying to make more server through the application mix, like from mobile PCN to server" | 두 번째 노력 - mix 변경 |
| `we are having a discussion internally maximizing our capacity to provide you better support` | "we are having a discussion internally maximizing our capacity to provide you better support" | "having a discussion internally" - 진지함 표현 |

**Audrey 교훈**: "we are making efforts"만 하면 약하다. "two kinds of efforts"로 나열하고, 각 effort마다 구체적 행동(용인 파브, mix 변경)을 붙인다. "we are having a discussion internally"는 "내부적으로 논의 중" - 한국어 "검토 중"의 영어 버전이지만, "internally"를 붙여 "진지하게 논의 중"임을 강조한다.

### AWS 질문자 구조 (Ashik의 5단계 도전)

Ashik은 질문할 때 5단계 공식을 따른다. 이게 네가 배워야 할 "정중하지만 단호한 도전"의 뼈대다.

#### 단계 1: 이해 확인 (Comprehension Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Help me understand what the message is` | "Help me understand what the message is and what you're saying, but help me understand a bit more about what you mean by development of 24/48" | "Help me understand" - 도전을 학습으로 포장 |
| `I think I understand your perspective` | "I think I understand your perspective" | 상대방 인정 후 도전 |
| `So I think I understand that you are going to be very top heavy` | "So I think I understand that you are going to be very top heavy as far as customer demand" | 이해 확인 후 질문 |

#### 단계 2: 기술적 판단 제시 (Technical Judgment)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `technically, you should have the flexibility to make X` | "technically, you should have the flexibility to make a 24 or 48 if we have to have it" | "technically"로 기술적 사실을 분리 |
| `there's nothing unique about that dim` | "there's nothing unique about that dim or even in the back end process" | 기술적 한계가 아님을 지적 - 정중한 도전 |
| `given enough lead time, you should be able to support it` | "given enough lead time, you should be able to support it because there's nothing unique about that dim" | 조건부 능력 인정 - "given enough lead time" |

#### 단계 3: 인정 + 그러나 (Acknowledge-But)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I acknowledge and I fully understand` | "That, that I acknowledge and I fully understand. I understand when the world's super constrained on capacity, you want to be as efficient as possible. I'm 100% with you." | 3중 인정 - "acknowledge" + "fully understand" + "100% with you" |
| `I totally acknowledge that. I'm just trying to understand` | "I totally acknowledge that. I'm just trying to understand or clarify my understanding" | 인정 후 "just trying to"로 도전을 학습으로 포장 |

#### 단계 4: 직접적 요구 (Direct Demand)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I want to be very direct with you guys` | "I want to be very direct with you guys. There's no specific timeline." | 직접성 선언 - "very direct"로 화법 전환 |
| `I want to be as transparent as possible` | "I want to be as transparent as possible" | 투명성 선언 |
| `I have a need for about 50,000 by December` | "I have a need for about 50,000 by December of 2026" | 수량+시점 직접 명시 |
| `If a pull-in is absolutely not possible, then please increase your volume support` | "If a pull-in is absolutely not possible, then please increase your volume support for AWS" | 조건부 요구 - "if not X, then Y" |

#### 단계 5: 유연성 표시 + 마무리 (Flexibility + Close)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `That was just an investigation` | "That was just an investigation. We can stay the 8800 parts. That's ideal, that's preferred." | 도전 후 후퇴 - "just an investigation"으로 공격 무장해제 |
| `I'm keeping my hopes up` | "I'm keeping my hopes up, but I'm just saying this is an older DAI" | 희망 표시 + 현실 인정 |
| `Without Hynix, we cannot survive` | "Without Hynix, we cannot survive. So I think we can discuss it." | 의존성 인정 - 파트너십 강조 |

**Audrey 교훈**: Ashik의 5단계 구조를 외워라. 1) 이해 확인 → 2) 기술적 판단 → 3) 인정 → 4) 직접 요구 → 5) 유연성 표시. 이 5단계가 "정중하지만 단호한 도전"의 완결된 공식이다. 한국어로는 "그러고요, 그런데요"로 도전하는데, 영어는 "Help me understand"로 시작해서 "I want to be very direct"로 전환한 뒤 "That was just an investigation"으로 무장해제하는 게 훨씬 세련되다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 진짜 학습 가치. SK가 공급 제약을 어떻게 정중하게 포장하는지, AWS가 요구를 어떻게 직·간접적으로 밀어붙이는지.

### 전략 1: "under consideration" - 결정 미루기 (Decision Deferral)

SK가 결정을 미룰 때 가장 많이 쓰는 화법. "아직 결정 안 했다"를 "검토 중"으로 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 256GB MRDIM Gen2 | "All the options under consideration. It is not fixed yet." | "모든 옵션이 검토 중입니다. 아직 확정 안 됐습니다" |
| MRDIM 128GB GV6 | "But there are probably 128 gigabyte MRDIM needs for the GV6. But it is not under considered. It is all under consideration, not fixed yet." | "GV6에 128GB MRDIM 필요할 수 있습니다. 아직 검토 중, 확정 아닙니다" |

**패턴 공식**: `X is under consideration. It is not fixed yet.`

**Audrey 교훈**: "under consideration"은 "검토 중"의 공식적 영어 표현이다. "We are considering"보다 수동태 "under consideration"이 더 공식적이고 거리감이 있다. "not fixed yet"을 붙여 "아직 결정 안 됐다"를 명시. 한국어 "검토 중"의 정확한 영어 버전. 로드맵 회의에서 가장 자주 등장한다.

### 전략 2: "we are having a discussion internally" - 내부 논의 중 (Internal Discussion)

구체적 약속을 피하면서 진지함은 표시하는 화법.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 용량 증설 논의 | "So yes, we are having a discussion internally maximizing our capacity to provide you better support" | "내부적으로 용량을 최대화해 더 나은 지원을 제공하기 위해 논의 중입니다" |
| 공급 우선순위 | "We are making some plans to support AWS and other customers and as you said earlier, we are prioritizing our supply and I believe AWS is among our top priorities" | "AWS 지원 계획 중, AWS가 최우선 순위에 있습니다" |

**패턴 공식**: `We are having a discussion internally to X. I believe Y is among our top priorities.`

**Audrey 교훈**: "We will consider"은 약하다. "We are having a discussion internally"이 더 진지하다 - "discussion"이 진행형이라 "지금 논의 중"임을 강조. 그리고 "I believe X is among our top priorities" - "I believe"로 개인적 확신을 표시, "among our top priorities"로 최우선이지만 유일하지는 않음을 포장. "AWS가 최우선"이라고 직접 말하지 않고 "among our top priorities"로 복수 우선순위를 만든다.

### 전략 3: "let us take action item" - 책임 미루기 (Action Item Deferral)

답변을 못할 때 "action item"으로 후속 약속.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Rambus PMIC 질문 | "I think we are not ready to answer you about this topic. So let us take action item." | "이 주제에 대해 아직 답변할 준비가 안 됐습니다. action item으로 받겠습니다" |
| 데이터 공개 | "We will take an action to see what we can disclose." | "공개 가능한 범위를 확인하는 action을 취하겠습니다" |

**패턴 공식**: `We are not ready to answer about X. Let us take action item.`

**Audrey 교훈**: "I don't know"는 절대 쓰지 마라. "We are not ready to answer" - "준비가 안 됐다"로 회피. 그리고 "let us take action item"으로 후속을 약속. "action item"은 회의에서 책임을 명시하는 공식 표현 - 다음에 대답하겠다는 약속의 공식.

### 전략 4: 구조적 제약 강조 (Structural Constraint)

공급 증설이 "구조적으로" 어렵다는 프레이밍.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 파브 일정 당기기 | "Given the massive cut-backs and increased lead time for construction and ramp-up, pulling in these schedules is structurally very difficult" | "대규모 감축과 건설·램프업 리드타임 증가로 인해 일정을 당기는 것은 구조적으로 매우 어렵습니다" |
| 1D 나노미터 개발 | "The DRAM industry, the 1D nanometer is very, very difficult to develop. And then because of that, we cannot give the commitment, the schedule of 1D nanometer" | "1D 나노미터는 매우 매우 개발이 어렵습니다. 그래서 schedule을 commit할 수 없습니다" |

**패턴 공식**: `Given X, pulling in Y is structurally very difficult. We cannot give the commitment.`

**Audrey 교훈**: "구조적으로 어렵다" - "structurally very difficult"는 "우리가 안 해서"가 아니라 "구조적으로 불가능하다"로 프레이밍. "cannot give the commitment" - "약속할 수 없다"로 명시. 회의에서 일정을 당길 수 없을 때 이 화법을 써라. "어렵습니다"만 하면 "노력이 부족해서"로 들린다. "structurally difficult"는 "구조적 한계"로 돌린다.

### 전략 5: 부정을 기술적 사실로 포장 (Technical Justification of Negation)

"안 됩니다"를 기술적 이유로 설명.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 512GB 미개발 | "We absolutely have no information and demand from the customer right now. Is it only reason or is there any technical bottleneck you have for making 5 to 10? It has or 3DS for high circuitry built in. So it has a technical capability embedded for our 32 gigabit base. The problem is there is no demand." | "현재 고객 요청이 전혀 없습니다. 기술적 능력은 있습니다 - 32기가비트 베이스에 3DS 기술이 내장되어 있습니다. 문제는 수요가 없다는 것입니다" |
| 9.6Gbps 우려 | "The truth is that 9.6 gigapies is very negative for SK Hynix. Because the original EOS speed, the 8.8 gigapies is under the 9.2 gigapies, the potential problem to support that speed." | "9.6Gbps는 SK하이닉스에 매우 부정적입니다. 8.8Gbps조차 9.2Gbps 아래에서 속도 지원에 잠재적 문제가 있습니다" |

**패턴 공식**: `We have no demand from customer. The technical capability is there. The problem is there is no demand.`

**Audrey 교훈**: "안 됩니다"가 아니라 "기술적 능력은 있는데 수요가 없다"로 포장. "기술적으로 가능하지만 사업적으로 안 한다"는 뉘앙스. 상대방의 "기술적 bottleneck이 있나요?" 질문에 "기술은 있는데 수요가 없다"로 답. 이게 공급자의 정중한 거절 - "안 해서"가 아니라 "수요가 없어서"라고 한다.

### 전략 6: AWS의 "just an investigation" 후퇴 (Probing Retreat)

AWS가 도전한 후, 공격을 무장해제하는 화법.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 8000 vs 8800 탐색 | "I just assumed that there was a possibility that 8800 might have had worse yield than 8000, that way there could have been a potential to get like more 8000 parts. That was just an investigation. We can stay the 8800 parts. That's ideal, that's preferred." | "8800이 8000보다 yield가 나빠서 8000을 더 받을 수 있을지 탐색했을 뿐입니다. 그냥 조사였습니다. 8800이 이상적이고 선호됩니다" |

**패턴 공식**: `I just assumed there was a possibility. That was just an investigation. X is ideal, that's preferred.`

**Audrey 교훈**: 도전한 뒤 후퇴할 때 "That was just an investigation" - "그냥 조사였다"로 공격을 무장해제. 그리고 "That's ideal, that's preferred"로 원래 요구가 맞다고 확인. 이게 도전-후퇴 공식 - 공격적으로 탐색하고, 결과가 안 좋으면 "그냥 조사"로 물러난다. 네가 파트너에게 탐색적 질문을 할 때, 이 화법으로 안전하게 후퇴할 수 있다.

---

## 3. 정중한 도전 화법 (AWS 측 질문자)

Ashik과 David가 기술적으로 도전하면서도 정중하게 질문하는 패턴. 네가 직접 써야 할 화법이다.

### 질문 유형 1: "Help me understand" - 학습으로 포장한 도전

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Help me understand what the message is` | "Help me understand what the message is and what you're saying, but help me understand a bit more about what you mean by development of 24/48" | "이해를 돕기 위해" - 도전을 학습으로 포장 |
| `Help me understand a bit more about what you mean by X` | "Help me understand a bit more about what you mean by development of 24/48" | "X의 의미를 더 설명해 달라" - 정중한 추가 설명 요구 |

**Audrey 교훈**: "Why are you doing X?"는 공격적이다. "Help me understand what you mean by X"는 같은 의미인데 학습으로 포장. "Help me understand"는 이 회의에서 Ashik의 시그니처 화법 - 여러 번 반복. **이 표현은 무조건 외워라.** 질문을 하기 전 "Help me understand"로 시작하면, 상대는 "도전당하고 있다"가 아니라 "도와달라고 한다"로 인식한다.

### 질문 유형 2: 기술적 사실 지적 (Technical Fact Statement)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `technically, you should have the flexibility to make X` | "technically, you should have the flexibility to make a 24 or 48 if we have to have it" | "기술적으로는 가능해야 한다" - 정중한 도전 |
| `there's nothing unique about X` | "there's nothing unique about that dim or even in the back end process" | "특별한 게 없다" - 기술적 한계 아님 지적 |
| `you should have no technical or even operational limitation to support it` | "you should have no technical or even operational limitation to support it. I think you're correct." | "기술적/운영적 한계가 없어야 한다" - 강한 도전 |

**Audrey 교훈**: "You can do it"은 공격적이다. "You should have the flexibility to do it"이 더 정중하면서 단호. "technically"를 붙여 "기술적 사실"을 분리 - "내 의견"이 아니라 "기술적 사실"로 도전. 그리고 "there's nothing unique about X"로 한계가 없음을 지적. 이게 엔지니어의 도전 - 감정이 아니라 사실로.

### 질문 유형 3: 조건부 요구 (Conditional Demand)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If a pull-in is absolutely not possible, then please increase your volume support` | "If a pull-in is absolutely not possible, then please increase your volume support for AWS" | "if not X, then Y" - 이중 요구 |
| `If there's any way you can improve your supportability for X, then we'll have the ability to take them` | "If there's any way you can improve your supportability for 128 gigabytes, specifically 128 gigabytes, then we'll have the ability to take them" | "any way"로 가능성 탐색 |
| `Is there a way to increase that quantity to 15K total?` | "Is there a way to increase that quantity to 15K total?" | "Is there a way" - 정중한 수량 요구 |

**Audrey 교훈**: "We need more"보다 "If a pull-in is absolutely not possible, then please increase your volume support"가 훨씬 세련된 협상. "absolutely not possible"로 상대의 한계를 인정하면서, "then please increase"로 대안을 제시. 이게 협상의 "if-then" 구조 - "A가 안 되면 B를 해 달라".

### 질문 유형 4: 직·간접 전환 (Direct-Indirect Switch)

Ashik은 "I want to be very direct"로 직접성을 선언한 후 직접 요구, 그리고 다시 "just an investigation"으로 간접으로 복귀.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I want to be very direct with you guys` | "I want to be very direct with you guys. There's no specific timeline. We haven't PR'd it yet." | 직접성 선언 - 화법 전환 신호 |
| `I want to be as transparent as possible` | "I want to be as transparent as possible. There's no specific timeline." | 투명성 선언 |
| `I just want to be very clear` | "I just want to be very clear. I didn't say speed is not important." | 오해 정정 - "very clear"로 선언 |

**Audrey 교훈**: 보통은 간접 화법("Help me understand")으로 도전하다, 핵심 요구에서는 "I want to be very direct"로 전환. 이 "직·간접 전환"이 고급 협상 화법이다. 항상 간접만 하면 요구가 안 통하고, 항상 직접만 하면 공격적으로 보인다. 핵심에서만 "very direct"로 전환하라.

### 질문 유형 5: 의존성 강조 (Dependency Assertion)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Who is the biggest customer using the memory?` | "Who is the biggest customer using the memory? If you think about our scale and if we use that specific AWS custom DRAM with that scale?" | 수사의문 - "우리가 제일 큰 고객"을 암시 |
| `Without Hynix, we cannot survive` | "Without Hynix, we cannot survive. So I think we can discuss it." | 의존성 인정 - 파트너십 강조 |
| `I think SK also needs to think about that` | "I think SK also needs to think about that" | "SK도 생각해 봐야 한다" - 정중한 압력 |

**Audrey 교훈**: "Who is the biggest customer?" - 수사의문으로 자신의 위치를 암시. 직접 "우리가 제일 크다"가 아니라 "Who is the biggest?"로 상대가 인식하게 만든다. 그리고 "Without Hynix, we cannot survive" - 의존성을 인정하면서 파트너십을 강조. "우리 없으면 안 된다"가 아니라 "너희 없으면 우리 못 산다"로 상대의 가치를 인정. 이게 협상에서 상대를 존중하면서도 영향력을 행사하는 화법이다.

### 질문 유형 6: 주의 환기형 질문 (Cautionary Question)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I get worried when I see X` | "I get worried when I see, like, just a handful of customers and then there is not much left as far as the overall capacity goes" | "걱정된다" - 정중한 경고 |
| `I had an idea of what is to happen, but it is still concerning regardless` | "I had an idea of what is to happen, but it is still concerning regardless, right?" | "여전히 우려된다" - 우려 지속 |
| `I want one Hynix team to not assume that anything's baked in stone` | "I want one Hynix team to not assume that anything's baked in stone" | "확정된 것으로 가정하지 마라" - 경고 |

**Audrey 교훈**: "I get worried when I see X" - "X를 보면 걱정된다"로 우려를 표시. "concerning"은 "우려스럽다"의 정중한 표현. 그리고 "anything's baked in stone" - "확정된 것으로 가정하지 마라" - "baked in stone"은 "확정된"의 관용구 (돌에 새겨진 것처럼). 회의에서 "이건 아직 확정 아니야, 가정하지 마"라고 할 때 써라.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 핵심. Type B 회의에서 가장 중요한 섹션. 로드맵·공급 협상의 언어.

### 수량·시점 요구 (Volume-Timeline Demand)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 수량+시점 직접 명시 | AWS | "I have a need for about 50,000 by December of 2026" | "I have a need for N by date" - 수량 요구 공식 |
| 부분 지원 요청 | AWS | "if you continue to do like 10,000 units per month, that'd be awesome" | "if you do X, that'd be awesome" - 부드러운 요구 |
| 초기 수량 확인 | AWS | "And what quantity can you support? Initially, the quantity is 7.5K for RDT plus free Rackbill" | "what quantity can you support?" - 직접 질문 |
| 수량 증가 요청 | AWS | "Is there a way to increase that quantity to 15K total?" | "Is there a way to increase" - 정중한 증량 요청 |
| 부분 지원 허용 | AWS | "I think a partial quantity support throughout Q4 will also help" | "partial quantity support will also help" - 유연성 표시 |

**Audrey 교훈**: 수량 요구는 "I have a need for N by date"로 직접. "We want N"이 아니라 "I have a need for N" - "need"를 명사로 써서 요구를 객관화. 그리고 "that'd be awesome"으로 부드러운 요구. "awesome"은 회의에서 쓰기엔 캐주얼하지만, 파트너 회의에서 부드러운 요청의 끝에 쓰면 친밀감을 준다.

### Pull-in 요구 (Schedule Pull-in Request)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| Pull-in 직접 요청 | AWS | "I'm going to still request you to pull in the 8800 128 gigabyte schedule as much as possible" | "request you to pull in X" - pull-in 요청 공식 |
| 조건부 pull-in | AWS | "If a pull-in is absolutely not possible, then please increase your volume support for AWS" | "if not pull-in, then increase volume" - 이중 요구 |
| Pull-in 시점 확인 | AWS | "When you say pull in, you mean pull in from what date to what date? What's the target date?" | "from what date to what date" - 구체적 시점 추궁 |
| Pull-in 성과 인정 | AWS | "I appreciate the high-next team's effort in sort of making a comeback, especially for the high-capacity stuff" | "appreciate the effort in making a comeback" - 노력 인정 |

**Audrey 교훈**: "Pull in"은 일정을 앞당기는 공식 표현. "We want it earlier"가 아니라 "pull in the schedule" - 산업 표준 용어. 그리고 "as much as possible"로 "될 수 있는 한"을 붙여 정중하게. 그리고 pull-in이 안 되면 volume을 늘려달라는 "if-then" 구조 - "A가 안 되면 B를 해 달라"는 협상의 기본 공식.

### "aligned with" - 타임라인 정렬 (Timeline Alignment)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 정렬 확인 | SK | "our schedule is aligned with your AP teams" | "aligned with" - 일정 정렬 확인 |
| 정렬 명시 | SK | "What I'm saying aligned means our RDD support disability, I think we are aligned with that" | "aligned means X" - 정렬 의미 정의 |
| 정렬 요청 | AWS | "I want SK be aligned with our plan and then marching forward together" | "be aligned with" - 정렬 요구 |
| 정렬 의지 | AWS | "we want to be really aligned with you guys" | "be really aligned" - 강조 |
| 정렬 부족 지적 | AWS | "So that means misaligned already" | "misaligned" - 정렬 안 됨 지적 |

**Audrey 교훈**: "aligned with"는 Type B 회의의 핵심 단어. "우리 일정이 맞다"가 아니라 "aligned with" - 산업 표준. "Our schedule is aligned with X" - "우리 일정이 X와 정렬되어 있다". 그리고 "marching forward together" - "함께 전진하자" - 정렬의 목적을 "함께"로 포장. 네가 파트너와 일정을 맞출 때 "We are aligned with your schedule"을 써라.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| Action item 선언 | SK | "Let us take action item. Because we are using your Rambus. I agree with you. We need to have at least three vendors just in case" | "let us take action item" - 후속 약속 |
| 데이터 공개 action | AWS | "We will take an action to see what we can disclose" | "take an action to see what we can" - 가능성 action |
| 이메일 요청 | AWS | "Can you send us the email through the Khalil or someone else that we can promote with it?" | "send us the email through X" - 커뮤니케이션 채널 지정 |
| 장기 예측 공유 | AWS | "I'm going to have Khalil, who's our supply manager, send you guys an email with a long-term forecast" | "send an email with a long-term forecast" - 장기 가이던스 요청 |
| 내부 확인 약속 | SK | "We will check that actually we faced lack of volume amount. So we try to communicate with a sales team" | "we will check + try to communicate" - 후속 약속 |

**Audrey 교훈**: "I'll check"는 약하다. "Let us take action item"이 공식적. 그리고 action item은 구체적이어야 - "take an action to see what we can disclose" - "공개 가능한 범위를 확인하는 action". 커뮤니케이션 채널을 명시하는 것도 중요 - "send us the email through Khalil"로 담당자 지정. 회의에서 "누가 언제까지 무엇을"을 명시하는 게 action item의 본질.

### 긍정 피드백 화법 (Positive Reinforcement)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 감사 표현 | AWS | "I wanted to start with a thank you. I appreciate the high-next team's effort in sort of making a comeback" | "start with a thank you" + "appreciate the effort" |
| 결과 칭찬 | AWS | "That's beautiful. That's really good" | "beautiful" + "really good" - 강한 긍정 |
| 방향 지지 | AWS | "I think that's a good idea. Yes" | "good idea" - 방향 승인 |
| 유연성 인정 | AWS | "That's actually better because if you're supporting us with the existing DAI, that means you have more flexibility" | "actually better" - 제안을 수용하며 더 나은 점 발견 |

**Audrey 교훈**: 협상에서 긍정 피드백은 필수. "start with a thank you" - 감사로 시작하면 상대가 협조적. "That's beautiful. That's really good." - 강한 긍정은 상대를 지원하고 싶게 만든다. 한국어로는 "좋습니다" 한 번이지만, 영어는 "beautiful" "really good" "actually better"로 여러 번 긍정.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 DRAM/로드맵/공급 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **bit penalty** | HBM이 conventional DRAM 대비消耗하는 bit 비율 | "HBM-3 has a three-fold bit penalty than conventional DRAM, while HBM-4 has much more bit penalty" - HBM이 용량 소모 크다고 설명 |
| **bit growth** | bit 단위 출하 증가율 | "leading to an upward revision in overall DRAM bit growth" - 수요 증가 지표 |
| **clean room space** | 반도체 팹의 청정실 공간 | "there is a critical shortage of clean room space" - 공급 제약 원인 |
| **pull in** | 일정을 앞당기다 | "We pulled in the Fab opening schedule of Yongin from October 27 to April" - 일정 단축 |
| **ramp up** | 생산량 점진 증가 | "we are trying to make a fast ramp up of Yongin Fab" - 양산 가속 |
| **wafer out** | 웨이퍼 생산 시작 (wafer 출력) | "this October means the wafer out, not the Fab opening" - 생산 시작 시점 명시 |
| **POR** (Plan of Record) | 확정 계획 | "We don't want to be in a situation that if we from high-speed are not 9.6, it becomes no way out" - 계획 고정성 |
| **MPI** (Mass Production Introduction) | 양산 도입 자격 | "whether you guys are going to take our CS 8800 for sustaining for MPI" - 양산 자격 |
| **CS** (Customer Sample) | 고객 샘플 | "We are preparing CS in May this year" - 샘플 제공 시점 |
| **sustaining car** | 양산 후 지속 생산 | "next year, probably we do a sustaining car only" - 지속 생산 |
| **EOL** (End of Life) | 제품 단종 | "When is the MDAI's EOL timeline you guys thinking?" - 단종 시점 질문 |
| **ADAI / MDAI / JDAI / DDAI** | SK의 DRAM die 코드명 (세대별) | "ADAI is 1C nanometer, JDAI is 1D nanometer" - 세대 구분 |
| **RCD** (Register Clock Driver) | RDIMM의 명령/클록 드라이버 | "JEDEC doesn't discuss about 9.6 gigabits, RCD spec" - 스펙 부재 지적 |
| **PMIC** (Power Management IC) | 전원 관리 칩 | "We struggled with the PMI problem for the last four years" - 품질 이슈 |
| **MRDIM** (Multi-Rank DIMM) | 다중 랭크 DIMM (Intel) | "256 gigabyte MRDIM Gen2 is under consideration" - 로드맵 |
| **TBD** (To Be Determined) | 미정 | "In case of 32 gigabit, it's TBD" - 결정 미정 |
| **1DPC** (1 DIMM Per Channel) | 채널당 DIMM 1개 | "we are using 1DPC memory configuration" - 메모리 구성 |
| **2DPC** | 채널당 DIMM 2개 | "Basically, we had 2 DPC. Once we go to the generation, we will move to 1 DPC" - 변화 |
| **head node** | AI 서버의 제어 노드 | "we are using previous generation, very stable servers to meet the capacity need for high capacity memory" - 안정성 중시 |
| **EOS speed** (End of Spectrum) | 해당 세대 최종 속도 | "we wanted to consolidate to the 9.2 gigapies, the EOS speed of the DDR5" - 속도 정합 |
| **tape out** | 칩 설계 완료 | "test chips that are going to be fabled in this year, Q2 sometime" - 테스트 칩 제조 |
| **baked in stone** | 확정된, 변경 불가능한 | "I want one Hynix team to not assume that anything's baked in stone" - 미확정 강조 |
| **AFR** (Annual Failure Rate) | 연간 고장률 | "if one of the PMI vendors turned out to be failing with high AFR" - 품질 우려 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 시장 프레이밍 (Market Framing) ──
- id: m24-001
  expression: "Starting in Q4 last year, we have seen a dramatic acceleration in X"
  category: market_framing
  function: dramatic_opening
  speaker_role: presenter
  difficulty: 4
  context: "Starting in Q4 last year, we have seen a dramatic acceleration in DRAM demand"
  note: "dramatic acceleration" - 시장 상황을 극적으로 프레이밍

- id: m24-002
  expression: "The key driver for this accelerated demand is X, which requires much more Y"
  category: market_framing
  function: cause_identification
  speaker_role: presenter
  difficulty: 4
  context: "The key driver for this accelerated demand is the emergence of agentic AI, which requires much more computing power"

- id: m24-003
  expression: "the total supply capacity has increased only by a single digit percent, compared to demand surging at mid-20 percent"
  category: supply_constraint
  function: contrast_justification
  speaker_role: presenter
  difficulty: 5
  context: "the total supply capacity has increased only by a single digit percent, compared to demand surging at mid-20 percent"
  note: 대비 구조 - "only by X, compared to Y surging at Z" - 공급 부족 정당화

- id: m24-004
  expression: "there is a critical shortage of X"
  category: constraint_stating
  function: shortage_emphasis
  speaker_role: presenter
  difficulty: 3
  context: "there is a critical shortage of clean room space"

- id: m24-005
  expression: "pulling in these schedules is structurally very difficult"
  category: structural_constraint
  function: impossibility_framing
  speaker_role: presenter
  difficulty: 5
  context: "Given the massive cut-backs and increased lead time for construction and ramp-up, pulling in these schedules is structurally very difficult"
  note: "structurally very difficult" - 구조적 불가능 강조

- id: m24-006
  expression: "we are making two kinds of efforts"
  category: effort_statement
  function: effort_enumeration
  speaker_role: presenter
  difficulty: 3
  context: "We are making two kinds of efforts. The first one is to increase DRAM bit through Yongin Fab. The second one is we are trying to make more server through the application mix"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m24-007
  expression: "X is under consideration. It is not fixed yet."
  category: decision_deferral
  function: polite_pending
  speaker_role: presenter
  difficulty: 4
  context: "All the options under consideration. It is not fixed yet."
  note: "under consideration" + "not fixed yet" - 결정 미루기 공식

- id: m24-008
  expression: "we are having a discussion internally to X"
  category: internal_discussion
  function: serious_pending
  speaker_role: presenter
  difficulty: 4
  context: "we are having a discussion internally maximizing our capacity to provide you better support"
  note: "having a discussion internally" - "검토 중"의 진지한 영어 버전

- id: m24-009
  expression: "I believe X is among our top priorities"
  category: priority_stating
  function: priority_without_exclusivity
  speaker_role: presenter
  difficulty: 4
  context: "I believe AWS is among our top priorities, so we are making our best to increase supply for AWS"
  note: "among our top priorities" - 최우선이지만 유일하지 않음을 포장

- id: m24-010
  expression: "we are not ready to answer about X. Let us take action item."
  category: action_item_deferral
  function: formal_deferral
  speaker_role: presenter
  difficulty: 4
  context: "I think we are not ready to answer you about this topic. So let us take action item."
  note: "I don't know" 대신 "not ready to answer" + action item

- id: m24-011
  expression: "We will take an action to see what we can disclose"
  category: action_item
  function: disclosure_action
  speaker_role: presenter
  difficulty: 4
  context: "We will take an action to see what we can disclose"

- id: m24-012
  expression: "the technical capability is there. The problem is there is no demand"
  category: technical_justification
  function: capability_without_demand
  speaker_role: presenter
  difficulty: 5
  context: "It has or 3DS for high circuitry built in. So it has a technical capability embedded for our 32 gigabit base. The problem is there is no demand."
  note: 기술적 능력은 있으나 수요 부재 - 정중한 거절

- id: m24-013
  expression: "we cannot give the commitment, the schedule of X"
  category: commitment_refusal
  function: schedule_commitment_refusal
  speaker_role: presenter
  difficulty: 4
  context: "The DRAM industry, the 1D nanometer is very, very difficult to develop. And then because of that, we cannot give the commitment, the schedule of 1D nanometer"

- id: m24-014
  expression: "it could reduce the fab utilization ratio and supply flexibility"
  category: constraint_explanation
  function: operational_impact
  speaker_role: presenter
  difficulty: 4
  context: "supporting multiple speed target would require preparing two different projects in our site. So it could reduce the fab utilization ratio and supply flexibility"

# ── 정중한 도전 (Polite Challenge - AWS) ──
- id: m24-015
  expression: "Help me understand what the message is"
  category: comprehension_check
  function: challenge_as_learning
  speaker_role: questioner
  difficulty: 5
  context: "Help me understand what the message is and what you're saying, but help me understand a bit more about what you mean by development of 24/48"
  note: Ashik의 시그니처 화법. 도전을 학습으로 포장. 무조건 외울 것.

- id: m24-016
  expression: "technically, you should have the flexibility to make X"
  category: technical_judgment
  function: polite_challenge
  speaker_role: questioner
  difficulty: 5
  context: "technically, you should have the flexibility to make a 24 or 48 if we have to have it"

- id: m24-017
  expression: "there's nothing unique about X"
  category: technical_fact
  function: limitation_denial
  speaker_role: questioner
  difficulty: 4
  context: "there's nothing unique about that dim or even in the back end process"

- id: m24-018
  expression: "you should have no technical or even operational limitation to support it"
  category: technical_judgment
  function: strong_polite_challenge
  speaker_role: questioner
  difficulty: 5
  context: "you should have no technical or even operational limitation to support it. I think you're correct."

- id: m24-019
  expression: "given enough lead time, you should be able to support it"
  category: conditional_capability
  function: conditional_acknowledgment
  speaker_role: questioner
  difficulty: 4
  context: "given enough lead time, you should be able to support it because there's nothing unique about that dim"

- id: m24-020
  expression: "I acknowledge and I fully understand"
  category: acknowledgment
  function: triple_acknowledgment
  speaker_role: questioner
  difficulty: 4
  context: "That, that I acknowledge and I fully understand. I understand when the world's super constrained on capacity, you want to be as efficient as possible. I'm 100% with you."
  note: 3중 인정 - "acknowledge" + "fully understand" + "100% with you"

- id: m24-021
  expression: "I'm just trying to understand or clarify my understanding"
  category: comprehension_check
  function: challenge_softening
  speaker_role: questioner
  difficulty: 4
  context: "I totally acknowledge that. I'm just trying to understand or clarify my understanding"

- id: m24-022
  expression: "That was just an investigation"
  category: probing_retreat
  function: disarm_attack
  speaker_role: questioner
  difficulty: 4
  context: "That was just an investigation. We can stay the 8800 parts. That's ideal, that's preferred."
  note: 도전 후 후퇴 - "그냥 조사"로 공격 무장해제

# ── 직접 요구 (Direct Demand) ──
- id: m24-023
  expression: "I want to be very direct with you guys"
  category: directness_declaration
  function: register_switch
  speaker_role: questioner
  difficulty: 4
  context: "I want to be very direct with you guys. There's no specific timeline. We haven't PR'd it yet."
  note: 간접 → 직접 전환 신호

- id: m24-024
  expression: "I want to be as transparent as possible"
  category: transparency_declaration
  function: honesty_signal
  speaker_role: questioner
  difficulty: 4
  context: "I want to be as transparent as possible. There's no specific timeline."

- id: m24-025
  expression: "I just want to be very clear"
  category: clarity_declaration
  function: correction_signal
  speaker_role: questioner
  difficulty: 3
  context: "I just want to be very clear. I didn't say speed is not important."

- id: m24-026
  expression: "I have a need for about N by date"
  category: volume_demand
  function: direct_quantity_request
  speaker_role: questioner
  difficulty: 4
  context: "I have a need for about 50,000 by December of 2026"
  note: "We want N" 대신 "I have a need for N" - 요구를 객관화

- id: m24-027
  expression: "If a pull-in is absolutely not possible, then please increase your volume support"
  category: conditional_demand
  function: if_then_demand
  speaker_role: questioner
  difficulty: 5
  context: "If a pull-in is absolutely not possible, then please increase your volume support for AWS"
  note: "if not X, then Y" - 이중 요구 공식

- id: m24-028
  expression: "I'm going to still request you to pull in X as much as possible"
  category: pull_in_request
  function: schedule_demand
  speaker_role: questioner
  difficulty: 4
  context: "I'm going to still request you to pull in the 8800 128 gigabyte schedule as much as possible"

- id: m24-029
  expression: "Is there a way to increase that quantity to N total?"
  category: volume_increase_request
  function: polite_increase_ask
  speaker_role: questioner
  difficulty: 3
  context: "Is there a way to increase that quantity to 15K total?"

- id: m24-030
  expression: "if you continue to do like N units per month, that'd be awesome"
  category: soft_demand
  function: friendly_request
  speaker_role: questioner
  difficulty: 3
  context: "if you continue to do like 10,000 units per month, that'd be awesome"

- id: m24-031
  expression: "a partial quantity support throughout Q4 will also help"
  category: partial_support
  function: flexibility_expression
  speaker_role: questioner
  difficulty: 3
  context: "I think a partial quantity support throughout Q4 will also help"

# ── 의존성·파트너십 (Dependency & Partnership) ──
- id: m24-032
  expression: "Who is the biggest customer using the memory?"
  category: rhetorical_pressure
  function: position_implication
  speaker_role: questioner
  difficulty: 5
  context: "Who is the biggest customer using the memory? If you think about our scale and if we use that specific AWS custom DRAM with that scale?"
  note: 수사의문으로 자신의 위치 암시

- id: m24-033
  expression: "Without Hynix, we cannot survive"
  category: dependency_acknowledgment
  function: partnership_emphasis
  speaker_role: questioner
  difficulty: 3
  context: "Without Hynix, we cannot survive. So I think we can discuss it."
  note: 의존성 인정 - 파트너십 강조

- id: m24-034
  expression: "I think SK also needs to think about that"
  category: gentle_pressure
  function: consideration_demand
  speaker_role: questioner
  difficulty: 4
  context: "If you think about our scale and if we use that specific AWS custom DRAM with that scale? I think SK also needs to think about that"

- id: m24-035
  expression: "I want one Hynix team to not assume that anything's baked in stone"
  category: assumption_warning
  function: non_finality_warning
  speaker_role: questioner
  difficulty: 5
  context: "However, things change and our decisions change because we have to consider many other variables before we actually align on a POR. So I want one Hynix team to not assume that anything's baked in stone."

# ── 우려 표시 (Concern Expression) ──
- id: m24-036
  expression: "I get worried when I see X"
  category: concern_expression
  function: polite_warning
  speaker_role: questioner
  difficulty: 4
  context: "I get worried when I see, like, just a handful of customers and then there is not much left as far as the overall capacity goes"

- id: m24-037
  expression: "it is still concerning regardless"
  category: concern_persistence
  function: ongoing_worry
  speaker_role: questioner
  difficulty: 3
  context: "I had an idea of what is to happen, but it is still concerning regardless, right?"

# ── 긍정 피드백 (Positive Reinforcement) ──
- id: m24-038
  expression: "I wanted to start with a thank you"
  category: gratitude_opening
  function: positive_start
  speaker_role: questioner
  difficulty: 3
  context: "I wanted to start with a thank you. I appreciate the high-next team's effort in sort of making a comeback, especially for the high-capacity stuff"

- id: m24-039
  expression: "I appreciate the effort in making a comeback"
  category: appreciation
  function: effort_recognition
  speaker_role: questioner
  difficulty: 4
  context: "I appreciate the high-next team's effort in sort of making a comeback, especially for the high-capacity stuff"

- id: m24-040
  expression: "That's beautiful. That's really good."
  category: strong_positive
  function: enthusiastic_approval
  speaker_role: questioner
  difficulty: 2
  context: "That's beautiful. That's really good."

- id: m24-041
  expression: "That's actually better because X"
  category: unexpected_positive
  function: silver_lining
  speaker_role: questioner
  difficulty: 4
  context: "That's actually better because if you're supporting us with the existing DAI, that means you have more flexibility and you might be able to give us more parts"

# ── 타임라인 정렬 (Timeline Alignment) ──
- id: m24-042
  expression: "our schedule is aligned with X"
  category: alignment_stating
  function: schedule_alignment
  speaker_role: presenter
  difficulty: 3
  context: "our schedule is aligned with your AP teams"
  note: "aligned with" - Type B 회의 핵심 단어

- id: m24-043
  expression: "I want SK be aligned with our plan and then marching forward together"
  category: alignment_request
  function: partnership_alignment
  speaker_role: questioner
  difficulty: 5
  context: "I want SK be aligned with our plan and then marching forward together"

- id: m24-044
  expression: "we want to be really aligned with you guys"
  category: alignment_intent
  function: alignment_emphasis
  speaker_role: presenter
  difficulty: 3
  context: "The reason why we are asking this kind of activity to you guys, we want to be really aligned with you guys"

- id: m24-045
  expression: "So that means misaligned already"
  category: misalignment_stating
  function: gap_identification
  speaker_role: questioner
  difficulty: 3
  context: "So that means misaligned already"

# ── 기술 협상 (Technical Negotiation) ──
- id: m24-046
  expression: "we want to have the technical leaders in this market"
  category: leadership_declaration
  function: strategic_intent
  speaker_role: questioner
  difficulty: 4
  context: "We want to have the technical leaders in this market. Then I just want to SK understand our strategy"

- id: m24-047
  expression: "I would like to suggest SK Hynix keep opening your eyes on X"
  category: suggestion
  function: soft_recommendation
  speaker_role: questioner
  difficulty: 4
  context: "I would like to suggest SK Hynix keep opening your eyes on the 5 to 10 gigabyte"

- id: m24-048
  expression: "We should not close the door on that"
  category: option_preservation
  function: openness_demand
  speaker_role: questioner
  difficulty: 4
  context: "And that's why I think what I'm going to say is, we should not close the door on that"

- id: m24-049
  expression: "Let's not go there"
  category: topic_deflection
  function: polite_redirect
  speaker_role: questioner
  difficulty: 3
  context: "Let's not go there. Let's think about this way."

# ── 커뮤니케이션·액션 (Communication & Action) ──
- id: m24-050
  expression: "Can you send us the email through X that we can promote with it?"
  category: channel_specification
  function: communication_request
  speaker_role: questioner
  difficulty: 3
  context: "Can you send us the email through the Khalil or someone else that we can promote with it?"

- id: m24-051
  expression: "I'm going to have X send you guys an email with a long-term forecast"
  category: forecast_sharing
  function: guidance_provision
  speaker_role: questioner
  difficulty: 4
  context: "I'm going to have Khalil, who's our supply manager, send you guys an email with a long-term forecast of all the 8800 speed, dim speed requirements"

- id: m24-052
  expression: "please continue to execute on that date"
  category: execution_request
  function: commitment_reinforcement
  speaker_role: questioner
  difficulty: 3
  context: "Just please continue to execute on that date. And we'll find a way to actually put you on our platforms"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-10 09 04 53_EN_AWSF2FQTR_Q12026-extracted.wav` (총 약 2시간, 15,458단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입 시장 분석 (line 137-174) | Ellie의 시장 프레이밍 - "dramatic acceleration" + 공급 제약 대비 구조 | 시장 상황 프레이밍 공식 | ★★☆ |
| 2 | 24/48GB 협상 (line 313-348) | Ashik "Help me understand" + "technically you should have flexibility" + SK "the problem is there is no demand" | 정중 도전 + 기술적 사실 도전 | ★★★★ |
| 3 | 8800 수량 협상 (line 424-450) | Ashik "I want to be very direct" + "pull in" 요구 + "if not pull-in, then increase volume" | 직접 요구 + 조건부 요구 | ★★★★ |
| 4 | 9.6Gbps 협상 (line 580-620) | AWS "we want technical leadership" + SK "the truth is 9.6 is very negative" + Ashik "we want to be aligned" | 방향성 제시 + 기술적 우려 + 정렬 요구 | ★★★★ |
| 5 | 256GB 수량 요구 (line 1145-1149) | Ashik "I have a need for about 50,000 by December" + 부분 지원 요청 + "that'd be awesome" | 수량+시점 직접 요구 + 부드러운 마무리 | ★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 그림자 연습에 발췌를 넣어 사용
- 발췌 2, 3, 4가 가장 가치 높음 - 정중 도전·직접 요구·협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **supply negotiation + roadmap alignment** register다. 공급자(SK)가 제약을 설명하고, 최고 고객(AWS)이 요구를 밀어붙이는 구조. 두 역할 모두 학습해야:
- **공급자 역할 (SK)**: 시장 프레이밍, 제약 정당화, "under consideration" 회피, action item deferral - 네가 공급 제약을 설명할 때
- **요구자 역할 (AWS)**: "Help me understand" 도전, 직·간접 전환, 수량+시점 요구, 의존성 강조 - 네가 파트너에게 요구할 때

### Pragmatics (화용론) 핵심
1. **"Help me understand"**: 이 회의에서 Ashik의 시그니처 화법. "Why are you doing X?"를 "Help me understand what you mean by X"로 포장. 도전을 학습으로 포장하면, 상대는 방어하지 않고 설명하려 한다. **이 한 문장은 무조건 외워라.**
2. **"under consideration" + "not fixed yet"**: Type B 회의의 핵심 회피 패턴. "검토 중, 확정 아님" - 결정을 미루면서 진지함은 표시. 한국어 "검토 중"과 정확히 일치.
3. **직·간접 전환**: 보통은 "Help me understand"로 간접 도전, 핵심 요구에서 "I want to be very direct"로 직접 전환, 요구 후 "That was just an investigation"으로 간접 복귀. 이 3단계 전환이 고급 협상 화법.
4. **"aligned with"**: Type B 회의의 핵심 단어. "일정이 맞다"가 아니라 "aligned with" - 산업 표준. "marching forward together"와 결합하면 "정렬해서 함께 전진하자"는 파트너십 표현.
5. **"I have a need for N by date"**: 수량+시점을 직접 명시. "We want N"이 아니라 "I have a need for N" - "need"를 명사로 써서 요구를 객관화. 협상에서 가장 중요한 화법.

### 네가 당장 써야 할 Top 5
1. **"Help me understand what you mean by X"** - 도전을 학습으로 포장
2. **"I want to be very direct with you guys"** - 핵심 요구에서 직접성 선언
3. **"I have a need for N by date"** - 수량+시점 직접 요구
4. **"If a pull-in is absolutely not possible, then please increase your volume support"** - 조건부 이중 요구
5. **"under consideration. It is not fixed yet"** - 결정 미루기 공식

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "왜 그렇게 합니까?" | "Help me understand what you mean by X" | "Why" → "Help me understand" - 도전을 학습으로 |
| "검토 중" | "under consideration. It is not fixed yet" | "검토 중" + "확정 아님"을 명시 |
| "내부적으로 논의 중" | "we are having a discussion internally" | "having a discussion"이 진행형 - 진지함 |
| "확정된 것으로 가정하지 마" | "don't assume that anything's baked in stone" | "baked in stone" - 돌에 새겨진 것처럼 확정 |
| "50,000개 필요합니다" | "I have a need for about 50,000 by December" | "We want" 대신 "I have a need for" - 객관화 |
| "빨리 해 주세요" | "request you to pull in the schedule as much as possible" | "pull in" - 산업 표준 용어 |
| "안 됩니다" | "the technical capability is there. The problem is there is no demand" | 기술적 능력 인정 + 수요 부재로 거절 |
| "그냥 조사였습니다" | "That was just an investigation" | 도전 후 후퇴 - 공격 무장해제 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 도전 화법·4절 협상 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **Type B 특화**: 이 교재는 Type B(로드맵/공급 조정) 회의 교재. 수량 요구("I have a need for N"), pull-in 요구("pull in the schedule"), 정렬 요구("aligned with"), 결정 미루기("under consideration")를 중점 학습

---

*Textbook 24 - AWS F2F QTR Q1 2026 (2026-02-10). 회의 유형 B (Roadmap/Supply Alignment). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
