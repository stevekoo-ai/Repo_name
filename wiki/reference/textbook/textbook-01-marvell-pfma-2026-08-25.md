---
textbook_id: 01
meeting: Marvell PFMA
date: 2026-08-25
type: A (기술 Deep-dive)
partner: Marvell (Ravi Mahatme, KS Shin, Steve Martin, Charles)
sk_side: DM App Engineering, App Performance, System/Memory Research, Product Training, Sunjoo Kim, Kangmin
duration_words: 6844
audio: repo/webex-audio/2026-08-25 08 00 59_EN_Marvell-extracted.wav
transcript: repo/webex-audio/2026-08-25 08 00 59_EN_Marvell-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, marvell, cxl, pfma, photonic-fabric, kv-cache, technical-deepdive]
---

# Textbook 01 - Marvell PFMA (2026-08-25)

> **회의 유형**: A (기술 Deep-dive) - 한쪽이 제품 아키텍처를 깊이 발표, 상대가 기술 Q&A로 도전
> **학습 가치**: 발표자의 설명 설계 구조, 약점 포장 화법, 질문자의 정중한 도전
> **Audrey 관점**: 이 회의는 "제품 pitch + 기술 defense"의 전형 - 네가 Marvell 입장이든 SK 입장이든 둘 다 배워야

---

## 1. 발화 아키텍처 - Ravi의 발표 설계 (6단계)

Ravi Mahatme는 발표를 6단계 구조로 설계한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "설명의 뼈대"다.

### 단계 1: 맥락 설정 (Problem Framing)

Ravi는 제품을 소개하기 전에 **문제부터 프레이밍**한다. "우리 제품이 좋다"가 아니라 "이 문제가 제일 어렵다"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we feel that X is now the hardest problem in Y` | "So we feel that KV cache is now the hardest problem in LLM inference" | 긴장감 생성 - "hardest problem"으로 문제 격상 |
| `X is a solvable problem, but Y is very difficult because...` | "Compute is a solvable problem, but KV cache management is very difficult because..." | 대비 구조 - 쉬운 것 vs 어려운 것 |
| `there is no good place in the memory hierarchy, right?` | "there is no good place in the memory hierarchy, right?" | 수사의문으로 청중 동의 끌어내기 |

**Audrey 교훈**: 영어 발표는 "제품"으로 시작하지 않는다. **"문제"**로 시작한다. "We feel that X is the hardest problem in Y" - 이 공식을 외워. 회의에서 네가 제안할 때도, 제품부터 말하지 말고 문제부터 프레이밍해.

### 단계 2: 솔루션 제시 (Solution Reveal)

문제를 프레이밍한 후, "So for that"으로 솔루션을 연결한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So for that, X has what we call the Y or Z` | "So for that, Marvell has what we call the Photonic Fabric Memory Appliance or PFMA" | 솔루션 공식 - "what we call"이 제품명에 권위 부여 |
| `So this is a X and it supports Y with Z` | "So this is a rack-mountable pod-scale memory appliance and it supports CXL 3.1 with dynamic capacity allocation" | 스펙 패턴 - "this is a X and it supports Y" |

**Audrey 교훈**: "what we call"은 제품명을 처음 소개할 때 쓰는 권위 부여 화법이다. "Marvell has what we call the PFMA" - 제품명을 마치 이미 알려진 것처럼 포장한다. 네가 신제품을 소개할 때 써.

### 단계 3: 이유 나열 (Reason Enumeration)

수사의문문으로 문을 열고, "The first reason is..."로 이유를 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So why a X for Y?` | "So why a shared memory tier for KVcache?" | 수사의문 - 이유 설득 전 개시 |
| `The first reason is X. So today Y... But what that means is...` | "The first reason is cross node KV reuse. So today KVcache is kept... But what that means is..." | "So today... But what that means is..." - 현상 vs 의미 구조 |
| `whereas if you have X, Y` | "But whereas if you have a cross tier, cross node KV tier available, any XPU... can start processing" | "whereas"로 대비 - 전문가의 논리 전환 |
| `So that essentially improves X because Y` | "So that essentially improves the performance... because any processor that is free can pick up the work" | "So that essentially" - 결론 도출 공식 |

**Audrey 교훈**: "The first reason is... The other benefit is... So which is why we feel that..." - 이 3단 이유 나열 구조를 외워. 회의에서 의견 관철할 때, 이유를 3개 나열하면 설득력이 3배가 된다. 한국어로는 "그리고요"로 연결하는데, 영어로는 "The first reason is / The other benefit is / So which is why"로 단계를 명시해야.

### 단계 4: 스펙 딥다이브 (Technical Detail)

"Marvell is building two ASICs"로 시작, "So the differentiation of the unique property of Marvell's X IP is that..."로 차별점을 강조.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So the differentiation of X is that it is Y` | "So the differentiation of the unique property of Marvell's Photonic Fabric IP is that it is thermally stable" | 차별점 강조 공식 |
| `So all the X is in the middle of the Y` | "So all the optical IO is in the middle of the chip" | 설계 의도 설명 |
| `And which means the X is completely free and we have put Y on the Z edge` | "And which means the beachfront is completely free and we have put two HBM controllers on the south edge" | "which means"로 결과 연결 |

### 단계 5: 질문 유도 (Question Invitation)

매 슬라이드 끝에 Ravi는 같은 공식으로 문을 연다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Any questions on this slide?` | "Any questions on this slide?" | 직접적 질문 유도 |
| `Okay, I'll keep going.` | (대답 없을 때) "Okay, I'll keep going." | 침묵 처리 -尷尬하지 않게 넘어가는 화법 |
| `So I will pause here if there are any questions on this slide.` | "So I will pause here if there are any questions on this slide." | "I will pause here" - 고급 질문 유도 |

**Audrey 교훈**: "Any questions?"는 초보자용이다. Ravi는 "So I will pause here if there are any questions on this slide"를 쓴다 - "pause here"가 더 여유 있고 전문가 느낌이다. 그리고 대답 없으면 "Okay, I'll keep going"으로 자연스럽게 넘어간다. 이 "keep going" 전환을 외워.

### 단계 6: 전환 (Transition)

새 주제로 넘어갈 때 "So going to X, so as I said, there are Y"를 쓴다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So going to the X, so as I said, there are Y` | "So going to the connectivity options, so as I said, there are two options to connect" | "as I said"로 앞 언급 회상 + 전환 |
| `So how we build the X is we take Y` | "So how we build the switch is we take a photonic interposer" | "how we build X is we take Y" - 공정 설명 공식 |

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. Ravi가 약점을 어떻게 정중하게 포장하는지. 이것이 네가 회의에서 직접 써야 할 화법이다.

### 전략 1: 부정 → "But" → 대안 (Negation-But-Alternative)

가장 중요한 패턴. "지원 안 함"을 인정하되, 즉시 대안을 제시한다.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| GPU Direct 미지원 | "this appliance today doesn't support GPU direct. **But** Marvell also has this PCI switch from the XConn acquisition, which supports GPU direct. **So with that switch, we can make the appliance talk directly to the GPU if required.**" | "오늘은 GPU direct 지원 안 합니다. **하지만** XConn 인수한 PCI switch가 있어서 지원합니다. **그 스위치로 GPU direct 연결 가능합니다.**" |

**패턴 공식**: `X today doesn't support Y. But we also have Z. So with Z, we can do Y if required.`

**Audrey 교훈**: 영어 회의에서 "안 됩니다"는 절대 단독으로 끝내지 마라. "X doesn't support Y. But we have Z." - 부정 뒤에 무조건 "But + 대안"을 붙여. 이게 전문가의 정중한 거절/회피다. 한국어로는 "안 됩니다" 한 다음 "그런데요"로 넘어가는데, 영어는 "But"의 타이밍이 즉각이다.

### 전략 2: 다음 세대로 미루기 (Next-Generation Deferral)

현재 한계를 "첫 제품"으로 프레이밍하고, 다음 제품에서 해결하겠다고 약속.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| CXL cache coherency 미지원 | "we can definitely discuss it for our next generation product. So this is just the first generation product that we made. Definitely, if you require that in the next product, we can, I can talk to the engineering team" | "다음 세대 제품에서는 논의 가능합니다. 이건 첫 제품이니까요. 다음 제품에 필요하시면, 엔지니어링팀과 이야기하겠습니다" |

**패턴 공식**: `We can definitely discuss it for our next generation. So this is just the first generation. If you require that in the next product, I can talk to the engineering team.`

**Audrey 교훈**: "definitely"를 미루는 앞에 써라 - "we can **definitely** discuss it" - "definitely"가 미루는 것을 부드럽게 만든다. "다음에 하겠다"의 거부감을 낮추는 화법이다. 한국어 "검토해 보겠습니다"의 영어 버전이 "we can definitely discuss it for our next generation"이다.

### 전략 3: 정확성 면책 + 대략값 제시 (Precision Disclaimer)

정확한 수치를 모를 때, "I can get you X, but"로 면책하면서 대략값을 준다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 상세 전력 수치 | "I can get you the breakdown, but the optical link itself, is about 2.4 picojoule per bit, just for the link and about 0.7 picojoule for the laser. So the link total is about 3.1 picojoule per bit." | "상세 내역은 전달해 드릴 수 있습니다만, 광학 링크 자체는 약 2.4 pJ/bit, 레이저가 약 0.7 pJ. 링크 총합 약 3.1 pJ/bit 입니다" |
| ASIC 전력 | "the memory ASIC... is, I would think about 200 to 225 watts. I can take an action item to follow up on the detailed power numbers" | "메모리 ASIC은 대략 200-225W 정도 생각합니다. 상세 전력 수치는 action item으로 후속하겠습니다" |

**패턴 공식**: `I can get you the breakdown, but X is about Y. I can take an action item to follow up on the detailed Z.`

**Audrey 교훈**: 수치를 모를 때 "I don't know"는 절대 쓰지 마라. "I can get you the breakdown, but..." - "정확한 건 후에 드리겠지만, 대략은 이 정도입니다." 이게 전문가의 정확한 회피다. 그리고 "I would think about X"로 추정치를 표시하고, "I can take an action item to follow up"로 책임을 명시한다. "action item"은 회의에서 중요한 단어다 - 다음에 하겠다는 약속의 공식적 표현.

### 전략 4: 경쟁자 질문 희석 (Competitor Dilution)

경쟁자 동향을 묻는 위험한 질문을, 구체 언급 없이 "interest"로 포괄한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 경쟁자 관심도 | "we've been talking to all hyperscalers and all memory vendors. And now in the last few months with memory being very critical and KVcache being very critical with agent work loads, there is new interest in innovative solutions to address the KVcache problem." | "모든 하이퍼스케일러, 모든 메모리 벤더와 대화 중입니다. 최근 몇 달간 메모리가 매우 중요해지면서, KVcache 문제 해결에 새로운 관심이 있습니다" |

**패턴 공식**: `We've been talking to all X and all Y. There is new interest in innovative solutions to address Z.`

**Audrey 교훈**: 구체 경쟁자 이름을 대지 않는다. "all hyperscalers and all memory vendors"로 포괄. 그리고 "there is new interest" - 능동태("X is interested")가 아니라 "there is interest"로 추상화. 이게 정보 빼내지 않으면서 협조적으로 들리게 하는 화법이다.

### 전략 5: 제한을 기회로 재프레이밍 (Constraint-as-Opportunity)

제품 한계를 "첫 제품"으로 프레이밍하되, "이제 수요 있으니 가속"으로 전환.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 용량 확장 질문 | "This is just the first generation product that we started working on about three years ago. **But now that there is demand for this market, we can accelerate the roadmap and increase the both memory capacity, the optical bandwidth as well as the radix.**" | "이건 3년 전 시작한 첫 제품입니다. **하지만 이제 시장 수요가 있으니, 로드맵을 가속해서 용량·대역폭·radix 모두 늘릴 수 있습니다.**" |

**패턴 공식**: `This is just the first generation. But now that there is demand, we can accelerate the roadmap and increase X, Y as well as Z.`

**Audrey 교훈**: "But now that there is demand" - "이제 수요가 있으니" - 제한을 시장 상황으로 돌리고, "we can accelerate"로 적극성을 표시. 한국어 "시장 상황을 보고 결정하겠습니다"의 훨씬 적극적 영어 버전이다.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 기술적으로 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 이해 확인형 질문 (Comprehension Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Just to make sure I understand correctly, I have a quick question. Does the X fully support Y?` | "Just to make sure I understand correctly, I have a quick question. Does the PFMA fully support all CXL protocol features, especially the support memory sharing function?" | "이해를 확인하기 위해" - 정중한 전제 + 질문 |

**Audrey 교훈**: "Just to make sure I understand correctly"는 회의에서 가장 유용한 화법 중 하나다. 질문을 하기 전에 이 말을 붙이면, 상대방은 "내 설명이 부족했나?"라고 생각하지 않고 "이 사람이 꼼꼼하구나"라고 느낀다. 그리고 질문이 도전적으로 보이지 않는다. **이 한 문장은 무조건 외워라.**

### 질문 유형 2: 미래 계획 탐색 (Future Plan Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Do you have a plan to support X in the future?` + `we would like to have Y` | "Do you have a plan to support the hardware, the coherency in the future? ... we would like to have some the hardware-based cache coherency" | "미래 지원 계획 있습니까?" + "저희는 X를 원합니다" - 의향 표시 |

**Audrey 교훈**: "Do you have a plan to support X?"는 단순 질문이다. 거기에 "we would like to have Y"를 붙이면, 질문이 아니라 **요구**가 된다. "저희가 원하는 게 있는데, 지원할 계획 있습니까?" - 이게 협상의 시작이다. 한국어로는 "저희도 그거 필요합니다"인데, 영어는 "we would like to have"로 정중하게 밀어붙인다.

### 질문 유형 3: 이유 질문 (Reason Question)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `And is there any reason to X?` | "And is there any reason to select that ratio with the HBM and the RDIM?" | "이유가 있습니까?" - 직접적이면서 정중 |
| `Does there any reason you X?` | "Does there any reason you put the HBM3e in a 2 pH per mm module?" | "Does there any reason" - 설계 의도 탐색 |

**Audrey 교훈**: "Why did you X?"는 공격적으로 들린다. "Is there any reason to X?"는 같은 의미인데 정중하다. "왜 그렇게 했습니까?"가 아니라 "그렇게 한 이유가 있습니까?" - 주어를 "you"에서 "reason"으로 빼서 비난감을 줄인다.

### 질문 유형 4: 겸손한 비교 질문 (Humble Comparison)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I'm not familiar with that, but is that the similar X with the one that we are familiar with?` | "I'm not familiar with that, but that is the similar interposure with the one that we are familiar with, like organic interposure or the glass interposure?" | "잘 모르겠지만, 우리가 아는 X와 비슷한 건가요?" - 겸손 + 비교 |

**Audrey 교훈**: 모르는 것이 있을 때 "I don't know"는 약하다. "I'm not familiar with that, but is that the similar X with Y?" - "잘 모르겠지만, 우리가 아는 것과 비슷한가요?" - 모르는 걸 인정하면서도, 자기가 아는 것에 연결해서 질문한다. 이게 전문가의 겸손한 학습 화법이다.

### 질문 유형 5: 확인식 짧은 질문 (Quick Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Those are for the X?` | "So what about the eight lanes of the illumination fibers? Those are for the laser?" | 짧은 확인 - 발표 흐름 끊지 않음 |
| `The bandwidth stays the same, right?` | "The bandwidth stays the same, right? Because the bandwidth is the optical bandwidth." | "right?"로 확인 - 대화형 |

**Audrey 교훈**: 발표 중에 긴 질문을 하면 흐름을 끊는다. "Those are for the laser?" - 짧은 확인식 질문은 발표자가 쉽게 대답할 수 있다. 이게 발표자를 존중하는 화법이다. 회의에서 발표자가 말할 때, 꼭 확인하고 싶은 건 "X, right?"로 짧게 물어라.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

회의 후반, 후속 협상과 action item을 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 문제 제기 + 솔루션 연결 | SK | "We are hoping Marvell's PFMA technology can help address the on-rack deployment bottleneck" | "We are hoping X can help address Y" - 부드러운 협상 |
| 결정 미루기 | SK | "We are thinking internally based on what you shared. And during our discussion, if any question comes up, we will reach out via email" | "We are thinking internally" - 결정 보류의 정중 표현 |
| 진지함 표시 | SK | "We are looking forward to follow up with the actionable collaboration proposal soon" | "actionable" + "soon" - 진지함 + 시점 명시 |
| 제안 | Ravi | "if you want to do an evaluation, we can work with Penguin to help set you up with appliance and server in your labs" | "we can work with X to help set you up" - 제안 공식 |

**Audrey 교훈**: 
- "We are hoping X can help address Y" - 이게 회의에서 요구하는 화법이다. "We want X"가 아니라 "We are hoping X can help address Y" - 요구를 "도움"으로 포장.
- "We are thinking internally" - 결정을 미룴 때 써라. "We will consider"보다 "We are thinking internally"이 더 진지하게 들린다.
- "actionable collaboration proposal" - "actionable"을 붙여라. "proposal"만 하면 모호하지만, "actionable proposal"은 "실행 가능한 제안"으로 진지함이 전달된다.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 책임 명시 | Ravi | "I can take an action item to follow up on the detailed power numbers" | "take an action item" - 책임 명시 공식 |
| 액션 연결 | Ravi | "I can take an action item to follow up on the detailed power numbers, but it's about 200 to 225 watts" | 대략값 + 후속 액션 |

**Audrey 교훈**: 회의에서 "I'll check"는 약하다. "I can take an action item to follow up on X" - 이게 action item의 공식적 표현이다. 회의록에 "action item"이 명시되면 책임이 있는 것이다. 네가 회의에서 다음에 무언가 하기로 했으면, "I'll take an action item to..."를 써라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/광학/메모리 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **PFMA** (Photonic Fabric Memory Appliance) | Marvell의 광학 메모리 어플라이언스 | "Marvell has what we call the Photonic Fabric Memory Appliance or PFMA" - 제품명 소개 시 "what we call" |
| **radix** | 스위치/패브릭의 포트 수 (여기선 16) | "our Gen1 appliance has a radix of 16" - "radix of N" |
| **FAU** (Fiber Attached Unit) | 광섬유 연결 장치 | "we put an FAU, a fiber attached FAU. And this FAU has 40 fibers" - 약어 풀이 패턴 |
| **photonic interposer** | 광학 컴포넌트 탑재 실리콘 기판 | "we take a photonic interposer, a pick. So this is an optical process" - "a X, a Y" 동의어 제시 |
| **write-through cache** | 쓰기 시 원본 동시 갱신하는 캐시 | "HBM can act as a cache, as a write through cache for the DDR" - "act as a X, as a Y" |
| **hardware semaphore** | 하드웨어 수준 동기화 메커니즘 | "we have hardware semaphores built in for software enable coherency" |
| **dynamic capacity allocation** | CXL 3.1의 동적 용량 할당 | "it supports CXL 3.1 with dynamic capacity allocation" - "X with Y" |
| **session affinity** | 세션이 특정 서버에 종속되는 성질 | "you have to have session affinity" - 부정적 뉘앙스 |
| **hit rate** | 캐시 적중률 | "you're going to get a very high hit rate on the KV cache" |
| **time to first token** | LLM 첫 토큰 생성 시간 | "the time to first token pretty much stays flat" |
| **bring up** | 하드웨어 초기 구동 검증 | "We expect engineering samples and bring up to start in Q4" |
| **tape out** | 칩 설계 완료·제조 의뢰 | "we've taped out the silicon earlier this year" |
| **POC** (Proof of Concept) | 개념 증명 | "we will start with the customer POCs working with Penguin" |
| **field replaceable** | 현장 교체 가능 | "this ELS is field replaceable and kept away from the memory" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 55개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m01-001
  expression: "we feel that X is now the hardest problem in Y"
  category: presentation_framing
  function: problem_escalation
  speaker_role: presenter
  difficulty: 4
  context: "So we feel that KV cache is now the hardest problem in LLM inference"
  pattern: "we feel that X is now the hardest problem in Y"
  note: 제품 소개 전 문제를 프레이밍 - 가장 권위 있는 발표 시작 화법

- id: m01-002
  expression: "X is a solvable problem, but Y is very difficult because..."
  category: presentation_framing
  function: contrast_setup
  speaker_role: presenter
  difficulty: 4
  context: "Compute is a solvable problem, but KV cache management is very difficult because..."

- id: m01-003
  expression: "So for that, X has what we call the Y"
  category: presentation_reveal
  function: solution_introduction
  speaker_role: presenter
  difficulty: 5
  context: "So for that, Marvell has what we call the Photonic Fabric Memory Appliance or PFMA"
  note: "what we call" - 제품명에 권위 부여. 신제품 소개 공식

- id: m01-004
  expression: "So this is a X and it supports Y with Z"
  category: presentation_spec
  function: spec_listing
  speaker_role: presenter
  difficulty: 3
  context: "So this is a rack-mountable pod-scale memory appliance and it supports CXL 3.1 with dynamic capacity allocation"

- id: m01-005
  expression: "So why a X for Y?"
  category: presentation_transition
  function: rhetorical_question
  speaker_role: presenter
  difficulty: 3
  context: "So why a shared memory tier for KVcache?"

- id: m01-006
  expression: "The first reason is X. So today Y... But what that means is..."
  category: presentation_reasoning
  function: reason_enumeration
  speaker_role: presenter
  difficulty: 4
  context: "The first reason is cross node KV reuse. So today KVcache is kept... But what that means is..."

- id: m01-007
  expression: "whereas if you have X, Y"
  category: logical_contrast
  function: expert_transition
  speaker_role: presenter
  difficulty: 5
  context: "But whereas if you have a cross tier, cross node KV tier available, any XPU can start processing"

- id: m01-008
  expression: "So that essentially improves X because Y"
  category: conclusion_draw
  function: consequence_stating
  speaker_role: presenter
  difficulty: 4
  context: "So that essentially improves the performance... because any processor that is free can pick up the work"

- id: m01-009
  expression: "So the differentiation of X is that it is Y"
  category: differentiation
  function: unique_value
  speaker_role: presenter
  difficulty: 5
  context: "So the differentiation of the unique property of Marvell's Photonic Fabric IP is that it is thermally stable"

- id: m01-010
  expression: "Any questions on this slide?"
  category: question_invitation
  function: direct_check
  speaker_role: presenter
  difficulty: 2
  context: "Any questions on this slide?"

- id: m01-011
  expression: "Okay, I'll keep going."
  category: silence_handling
  function: awkwardness_recovery
  speaker_role: presenter
  difficulty: 3
  context: (대답 없을 때) "Okay, I'll keep going."
  note: 침묵 처리 -尷尬하지 않게 넘어가는 화법. 필수.

- id: m01-012
  expression: "So I will pause here if there are any questions on this slide."
  category: question_invitation
  function: expert_pause
  speaker_role: presenter
  difficulty: 4
  context: "So I will pause here if there are any questions on this slide."
  note: "Any questions?"보다 여유 있는 전문가 화법

- id: m01-013
  expression: "So going to the X, so as I said, there are Y"
  category: transition
  function: topic_shift
  speaker_role: presenter
  difficulty: 4
  context: "So going to the connectivity options, so as I said, there are two options to connect"

- id: m01-014
  expression: "So how we build the X is we take Y"
  category: process_explanation
  function: build_step
  speaker_role: presenter
  difficulty: 3
  context: "So how we build the switch is we take a photonic interposer"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m01-015
  expression: "X today doesn't support Y. But we also have Z. So with Z, we can do Y if required."
  category: negation_but_alternative
  function: polite_refusal_with_alternative
  speaker_role: presenter
  difficulty: 5
  context: "this appliance today doesn't support GPU direct. But Marvell also has this PCI switch from the XConn acquisition, which supports GPU direct. So with that switch, we can make the appliance talk directly to the GPU if required."
  note: 가장 중요한 회피 패턴. 부정 뒤에 무조건 "But + 대안"

- id: m01-016
  expression: "we can definitely discuss it for our next generation product"
  category: next_gen_deferral
  function: polite_delay
  speaker_role: presenter
  difficulty: 5
  context: "we can definitely discuss it for our next generation product. So this is just the first generation product"
  note: "definitely"로 미루는 것을 부드럽게. "검토해 보겠습니다" 영어 버전

- id: m01-017
  expression: "this is just the first generation product that we made"
  category: first_gen_framing
  function: limitation_excuse
  speaker_role: presenter
  difficulty: 3
  context: "this is just the first generation product that we made"

- id: m01-018
  expression: "if you require that in the next product, I can talk to the engineering team"
  category: commitment_soft
  function: conditional_promise
  speaker_role: presenter
  difficulty: 4
  context: "Definitely, if you require that in the next product, we can, I can talk to the engineering team"

- id: m01-019
  expression: "I can get you the breakdown, but X is about Y"
  category: precision_disclaimer
  function: precise_evasion
  speaker_role: presenter
  difficulty: 5
  context: "I can get you the breakdown, but the optical link itself, is about 2.4 picojoule per bit"
  note: 수치 모를 때 "I don't know" 대신 쓰는 정확한 회피

- id: m01-020
  expression: "I would think about X to Y"
  category: estimate_hedging
  function: approximate_value
  speaker_role: presenter
  difficulty: 4
  context: "the memory ASIC... is, I would think about 200 to 225 watts"

- id: m01-021
  expression: "I can take an action item to follow up on X"
  category: action_item
  function: commitment_formal
  speaker_role: presenter
  difficulty: 4
  context: "I can take an action item to follow up on the detailed power numbers"
  note: "I'll check" 대신 "take an action item" - 책임 명시 공식

- id: m01-022
  expression: "we've been talking to all X and all Y"
  category: competitor_dilution
  function: vague_competitor_reference
  speaker_role: presenter
  difficulty: 4
  context: "we've been talking to all hyperscalers and all memory vendors"

- id: m01-023
  expression: "there is new interest in innovative solutions to address X"
  category: interest_abstraction
  function: passive_interest_stating
  speaker_role: presenter
  difficulty: 4
  context: "there is new interest in innovative solutions to address the KVcache problem"
  note: 능동태 대신 "there is interest"로 추상화

- id: m01-024
  expression: "But now that there is demand, we can accelerate the roadmap"
  category: constraint_reframe
  function: limitation_to_opportunity
  speaker_role: presenter
  difficulty: 5
  context: "But now that there is demand for this market, we can accelerate the roadmap and increase the both memory capacity, the optical bandwidth as well as the radix"

# ── 정중한 도전 (Polite Challenge) ──
- id: m01-025
  expression: "Just to make sure I understand correctly, I have a quick question."
  category: comprehension_check
  function: polite_preface
  speaker_role: questioner
  difficulty: 5
  context: "Just to make sure I understand correctly, I have a quick question. Does the PFMA fully support all CXL protocol features?"
  note: 가장 유용한 정중 질문 화법. 무조건 외울 것.

- id: m01-026
  expression: "Do you have a plan to support X in the future?"
  category: future_probe
  function: plan_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "Do you have a plan to support the hardware, the coherency in the future?"

- id: m01-027
  expression: "we would like to have X"
  category: requirement_stating
  function: polite_demand
  speaker_role: questioner
  difficulty: 4
  context: "we would like to have some the hardware-based cache coherency"
  note: "we want" 대신 "we would like to have" - 정중한 요구

- id: m01-028
  expression: "Is there any reason to X?"
  category: reason_inquiry
  function: design_intent_probe
  speaker_role: questioner
  difficulty: 4
  context: "And is there any reason to select that ratio with the HBM and the RDIM?"
  note: "Why did you X?" 대신 정중한 화법

- id: m01-029
  expression: "Does there any reason you X?"
  category: reason_inquiry
  function: design_intent_probe
  speaker_role: questioner
  difficulty: 3
  context: "Does there any reason you put the HBM3e in a 2 pH per mm module?"

- id: m01-030
  expression: "I'm not familiar with that, but is that the similar X with Y?"
  category: humble_comparison
  function: learning_question
  speaker_role: questioner
  difficulty: 5
  context: "I'm not familiar with that, but that is the similar interposure with the one that we are familiar with?"

- id: m01-031
  expression: "Those are for the X?"
  category: quick_confirm
  function: flow_preserving_check
  speaker_role: questioner
  difficulty: 2
  context: "So what about the eight lanes of the illumination fibers? Those are for the laser?"
  note: 발표 흐름 끊지 않는 짧은 확인

- id: m01-032
  expression: "The X stays the same, right?"
  category: tag_question
  function: conversational_confirm
  speaker_role: questioner
  difficulty: 3
  context: "The bandwidth stays the same, right? Because the bandwidth is the optical bandwidth."

- id: m01-033
  expression: "I have one question."
  category: question_opening
  function: turn_taking
  speaker_role: questioner
  difficulty: 2
  context: "I have one question. And what is what is the estimated size of this appliance box?"

- id: m01-034
  expression: "Just to make sure I understand correctly" (독립 사용)
  category: comprehension_check
  function: polite_preface_standalone
  speaker_role: questioner
  difficulty: 5
  context: "Just to make sure I understand correctly, I have a quick question."

# ── 협상·액션 (Negotiation) ──
- id: m01-035
  expression: "We are hoping X can help address Y"
  category: soft_demand
  function: polite_request
  speaker_role: negotiator
  difficulty: 4
  context: "We are hoping Marvell's PFMA technology can help address the on-rack deployment bottleneck"
  note: "We want X" 대신 "We are hoping X can help address Y" - 요구를 도움으로 포장

- id: m01-036
  expression: "We are thinking internally based on what you shared"
  category: decision_deferral
  function: polite_delay
  speaker_role: negotiator
  difficulty: 4
  context: "We are thinking internally based on what you shared"
  note: 결정 미루기 - "We will consider"보다 진지

- id: m01-037
  expression: "We are looking forward to follow up with the actionable collaboration proposal soon"
  category: commitment_expression
  function: serious_intent
  speaker_role: negotiator
  difficulty: 5
  context: "We are looking forward to follow up with the actionable collaboration proposal soon"
  note: "actionable" + "soon" - 진지함 표시

- id: m01-038
  expression: "if you want to do an evaluation, we can work with X to help set you up"
  category: offer
  function: proposal
  speaker_role: presenter
  difficulty: 4
  context: "if you want to do an evaluation, we can work with Penguin to help set you up with appliance and server in your labs"

- id: m01-039
  expression: "during our discussion, if any question comes up, we will reach out via email"
  category: follow_up_channel
  function: communication_commitment
  speaker_role: negotiator
  difficulty: 3
  context: "during our discussion, if any question comes up, we will reach out via email"

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m01-040
  expression: "X has what we call the Y or Z"
  category: product_naming
  function: authority_naming
  speaker_role: presenter
  difficulty: 4
  context: "Marvell has what we call the Photonic Fabric Memory Appliance or PFMA"

- id: m01-041
  expression: "a X, a Y" (동의어 제시)
  category: synonym_gloss
  function: term_clarification
  speaker_role: presenter
  difficulty: 3
  context: "we take a photonic interposer, a pick. So this is an optical process"

- id: m01-042
  expression: "X act as a Y, as a Z"
  category: role_explanation
  function: function_clarification
  speaker_role: presenter
  difficulty: 3
  context: "HBM can act as a cache, as a write through cache for the DDR"

- id: m01-043
  expression: "X with Y" (기능 부연)
  category: feature_attachment
  function: spec_detailing
  speaker_role: presenter
  difficulty: 2
  context: "it supports CXL 3.1 with dynamic capacity allocation"

- id: m01-044
  expression: "we expect X to start in Y"
  category: timeline_stating
  function: schedule
  speaker_role: presenter
  difficulty: 3
  context: "We expect engineering samples and bring up to start in Q4"

- id: m01-045
  expression: "we've taped out the X earlier this year"
  category: milestone
  function: dev_stage
  speaker_role: presenter
  difficulty: 4
  context: "we've taped out the silicon earlier this year"

- id: m01-046
  expression: "we are targeting a public demo of this around X"
  category: target_milestone
  function: future_demo
  speaker_role: presenter
  difficulty: 3
  context: "we are targeting a public demo of this around OFC GTC in March"

- id: m01-047
  expression: "we hope to achieve X in Y"
  category: production_target
  function: timeline
  speaker_role: presenter
  difficulty: 3
  context: "we hope to achieve production qualification in the second half of next year"

# ── 발화 채움 표현 (Discourse Markers in Use) ──
- id: m01-048
  expression: "So, yeah, as I mentioned"
  category: discourse_marker
  function: reference_back
  speaker_role: presenter
  difficulty: 2
  context: "So, yeah, as I mentioned that I think that we invited our DLM application engineering"

- id: m01-049
  expression: "that the reason why we are coming here and wanting to hear about your plan"
  category: intent_stating
  function: meeting_purpose
  speaker_role: questioner
  difficulty: 3
  context: "That's the reason why we are coming here and wanting to hear about your plan"

- id: m01-050
  expression: "at any point, please feel free to stop and ask any questions"
  category: question_invitation
  function: open_invitation
  speaker_role: presenter
  difficulty: 3
  context: "And at any point, please feel free to stop and ask any questions that you may have"

- id: m01-051
  expression: "please let me know if there is no interest"
  category: polite_close
  function: graceful_exit
  speaker_role: presenter
  difficulty: 4
  context: "Please let me know if there are any more questions here or if there is no interest"
  note: 관심 없을 경우의 정중한 퇴로 - 직접적이면서도 부드러운 화법

- id: m01-052
  expression: "I think the content is absolutely excellent"
  category: compliment
  function: positive_feedback
  speaker_role: questioner
  difficulty: 2
  context: "I think the content is absolutely excellent"

- id: m01-053
  expression: "So it's possible to share today's presentation"
  category: request
  function: polite_ask
  speaker_role: questioner
  difficulty: 3
  context: "So, yeah, it's possible to share today's presentation"

- id: m01-054
  expression: "if there are follow up questions, please feel free to email me"
  category: follow_up_channel
  function: open_contact
  speaker_role: presenter
  difficulty: 3
  context: "if there are follow up questions, please feel free to email me"

- id: m01-055
  expression: "we can work on the next steps"
  category: next_step
  function: forward_move
  speaker_role: presenter
  difficulty: 2
  context: "And then we can work on the next steps"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-08-25 08 00 59_EN_Marvell-extracted.wav` (총 ~57분, 6,844단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 53-66) | Ravi 자기소개 + 발표 목적 + "feel free to stop and ask" | 발표자开场 화법 | ★★☆ |
| 2 | 문제 프레이밍 (line 67-80) | "KV cache is now the hardest problem" + 메모리 계층 설명 | 문제 프레이밍 공식 | ★★★ |
| 3 | 솔루션 제시 (line 81-104) | "So for that, Marvell has what we call PFMA" + 스펙 나열 | 솔루션 공식 + 스펙 패턴 | ★★★ |
| 4 | 질문-대답 (line 174-194) | SK "Do you have a plan to support coherency" + Ravi "next generation" 회피 | 정중 도전 + 회피 화법 | ★★★★ |
| 5 | 협상 마무리 (line 543-554) | "We are hoping PFMA can help address" + "actionable collaboration proposal soon" | 협상 마무리 화법 | ★★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 회피/협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **technical pitch + defense** register다. 발표자가 제품을 설명하고, 청중이 기술적으로 도전하는 구조. 두 역할 모두 학습해야:
- **발표자 역할 (Ravi)**: 설명 설계, 회피 포장, 질문 유도 - 네가 제품 설명할 때
- **질문자 역할 (SK)**: 정중 도전, 기능 확인, 요구사항 표시 - 네가 파트너 제품 평가할 때

### Pragmatics (화용론) 핵심
1. **부정의 "But" 연결**: 영어 회의에서 "안 됩니다"는 단독 금지. "X doesn't support Y. But we have Z." - 부정 뒤에 무조건 대안. 한국어 "안 됩니다, 그런데요"와 타이밍이 다름 - 영어는 "But"가 즉각.
2. **"definitely"의 미루기**: "we can definitely discuss it for next generation" - "definitely"가 미루는 것을 부드럽게 만듦. "다음에 하겠다"의 거부감 낮추기.
3. **"Just to make sure I understand correctly"**: 질문 전 이 말을 붙이면, 도전적 질문이 정중한 확인이 됨. 이 회의에서 SK 측이 가장 잘 쓴 화법.

### 네가 당장 써야 할 Top 5
1. **"Just to make sure I understand correctly"** - 질문 전무조건
2. **"X today doesn't support Y. But we have Z"** - 부정+대안
3. **"we can definitely discuss it for our next generation"** - 정중한 미루기
4. **"I can take an action item to follow up on X"** - 책임 명시
5. **"We are hoping X can help address Y"** - 정중한 요구

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "안 됩니다" | "X doesn't support Y. But we have Z" | 한국어는 부정으로 끝, 영어는 "But" 즉시 |
| "검토해 보겠습니다" | "we can definitely discuss it for next generation" | "definitely"로 긍정 포장 |
| "왜 그렇게 했습니까?" | "Is there any reason to X?" | 주어를 "you"에서 "reason"으로 |
| "저희도 필요합니다" | "we would like to have X" | "want" 대신 "would like to have" |
| "다음에 확인하겠습니다" | "I can take an action item to follow up" | "check" 대신 "action item" |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 55개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 5절 회피 화법·3절 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득

---

*Textbook 01 - Marvell PFMA (2026-08-25). 회의 유형 A (기술 Deep-dive). 표현 DB 55개. 5개 발췌 구간. 작성: 2026-09-02.*
