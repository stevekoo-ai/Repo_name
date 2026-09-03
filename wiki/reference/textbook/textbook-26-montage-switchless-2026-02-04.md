---
textbook_id: 26
meeting: Montage switchless CXL expander technical deep-dive
date: 2026-02-04
type: A (technical deep-dive) - confirmed
partner: Montage (memory controller vendor, switchless multi-head CXL expander proposal)
sk_side: SK Hynix (CXL/memory pooling architecture evaluation)
duration_words: 6013
audio: repo/webex-audio/2026-02-04 10 02 50_EN_Montage_switchless-extracted.wav
transcript: repo/webex-audio/2026-02-04 10 02 50_EN_Montage_switchless-extracted-rag-corrected.txt
created: 2026-09-02
tags: [textbook, english, montage, cxl, switchless, multi-head, memory-pooling, expander, technical-deepdive]
---

# Textbook 26 - Montage switchless CXL expander (2026-02-04)

> **회의 유형**: A (기술 Deep-dive) - confirmed. Montage가 switchless multi-head CXL memory expander 컨셉을 설명하고, SK Hynix가 기술 Q&A로 도전.
> **학습 가치**: 발표자가 "아직 planning 단계"임을 계속 강조하는 hedging, 질문자가 "I also have a similar opinion"으로 동의하며 도전하는 한국식 정중 도전, 양측이 모두 한정어(subjunctive hedging)를 과도하게 써서 만드는 공손한 기술 대화.
> **Audrey 관점**: 이 회의는 Marvell textbook 01과 짝을 이룬다. 01은 "완성된 제품 pitch + defense", 이 회의는 "미완성 컨셉트 + 공동 탐색". 발표자가 아직 디자인 플랜 단계이기 때문에 회피가 더 잦고, 질문자가 의견을 제시하며 동의를 도출하는 화법이 두드러진다. 양쪽 모두 영어가 non-native라서 겸손·한정어가 밀집된 것도 특징. 네가 파트너 컨셉트를 평가하는 회의에서 직접 써야 할 화법이 여기에 있다.

---

## 1. 발화 아키텍처 - Montage 발표자의 설명 설계 (5단계)

Montage 발표자는 발표라기보다 "대화형 컨셉트 walkthrough"로 구성한다. 발표 자료가 있지만, 계속 질문을 끌어내고 동의를 확인하며 진행한다. 이게 non-native 발표자의 안전 발화 전략이다. 각 단계마다 **고정된 화법 공식**이 있다.

### 단계 1: 문제 프레이밍 (Ecosystem Complaint Framing)

Montage 발표자는 자기 제안을 꺼내기 전에 **"고객이 불만이다"**로 시작한다. 자기 의견을 직접 말하지 않고, 시장 불만을 인용한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `At this moment, X is not so good` | "At this moment, Switch is not so good, a metaphor of the ecosystem or the performance itself" | 부정 전제 - "지금 안 좋다"로 긴장감 설정 |
| `X currently is the only one who can provide a Y` | "S-Con currently is the only one renderer who can provide a Switch" | 단일 공급자 = 위험 프레이밍 |
| `X also complained that the current Y is not so good in performance` | "Alibaba also complained that the current memory box is not so good in performance" | 타사 불만 인용 - 자기 의견에 타사 권위 빌리기 |

**Audrey 교훈**: 영어 발표에서 "내 생각엔"으로 시작하면 약하다. "X complained that Y is not so good" - 타사 불만을 인용하라. 이게 non-native 발표자가 자기 의견에 힘을 싣는 가장 효율적 화법이다. "I think the switch is not good"이 아니라 "Alibaba complained that the switch is not good" - 비난 주체를 빼서 자기를 보호하면서 시장 상황을 강조한다. 네가 파트너 제품을 평가할 때 "고객이 불만이다"로 시작하는 화법을 외워라.

### 단계 2: 대안 제시 (Alternative Reveal via "So that's why")

문제를 프레이밍한 후 "So that's why we are considering"으로 자기 제안을 연결한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So, that's why we are considering to design a new product based on our existing designs` | "that's why we are considering to design a new product based on our existing designs to build a new multi-head device" | "considering" - 아직 결정 아님을 표시 |
| `we believe with the integrated design and this X device can provide better benefits, no matter from Y, Z and W` | "we believe with the integrated design and this multi-head device can provide better, more benefits, no matter from the latency, the cost and the power" | "no matter from X, Y, Z" - 3개 축 동시 나열 |

**Audrey 교훈**: "considering"이 이 회의의 핵심 동사다. "planning"도 아니고 "decided"도 아닌 "considering" - "고려 중"이라는 한정어가 발표자에게 여유를 준다. 파트너에게 아직 플랜임을 표시하면서도 진지함은 전달하는 화법. "we believe X can provide better benefits, no matter from A, B, C" - 3개 축을 한 번에 나열해서 설득력을 높이는 패턴. 한국어로는 "여러 면에서 장점이 있습니다"인데, 영어는 축을 명시해서 "latency, cost, power"로 한정하는 게 더 강하다.

### 단계 3: 의향 탐색 (Demand Validation Probe)

Montage 발표자는 자기 플랜이 확정되지 않았음을 반복하며, 고객 수요를 탐색한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are also engaging with some X customers to see if they are in this proposal and if we have enough demand from those guys and we can kick off this project` | "we are also engaging with some China top CSP customers to see if they are in this proposal and if we have enough demand from those guys and we can kick off this project" | "if...if...and" - 조건 연쇄로 플랜 가중 검증 |
| `basically, it is still in planning and some features might change depending on the communication with those big customers` | "basically, it is still in planning and some features might change depending on the communication with those big customers" | "still in planning" + "might change" - 이중 한정 |

**Audrey 교훈**: "we can kick off this project" - "kick off"는 프로젝트 시작의 일상 동사다. 회의에서 "we can start"보다 "we can kick off"가 더 비즈니스 영어스럽다. 그리고 "if we have enough demand from those guys" - "those guys"로 비격식 표현. 공식 발표에서는 쓰지 말지만, 1:1 회의에서는 친밀감을 만드는 데 유용. 네가 파트너와 1:1로 깊게 이야기할 때는 "those guys"로 무장해제 가능.

### 단계 4: 스펙 나열 (Spec Walkthrough)

발표 자료를 따라가며, "So 8 channel DDR on the backside, 1 DPC, 8000 and 2 DPC, 6400" 식으로 스펙을 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So from the feature set, currently we are planning a total of X and can be configured by Y or even by Z` | "So from the feature set, currently we are planning a total 64 lanes on the front side and can be configured by 8 port or even by 16 port" | "currently we are planning" - "현재 플랜" 한정어 + 스펙 나열 |
| `Yeah, this is a, you know, as the current Alibaba Gen one` | "And for the topology, yeah, this is a, you know, as the current Alibaba Gen one" | "you know" - 비격식 채움 + Alibaba 비교로 권위 부여 |

### 단계 5: 질문 유도 (Question Invitation)

Montage 발표자는 발표 중간중간 질문을 끌어낸다. 끝에서는 "I did too much talk. So anyone any question from the SK hynix?"로 마무리.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `since you already have the slides in hand, so I can quickly go through this one` | "since you already have the slides in hand, so I can quickly go through this one" | "quickly go through" - 발표 속도 조절 |
| `I did too much talk. So anyone any question from the SK hynix?` | "I did too much talk. So anyone any question from the SK hynix?" | 자기 비하 + 질문 유도 - "too much talk"으로 상대 발화 공간 확보 |

**Audrey 교훈**: "I did too much talk" - 문법적으로는 틀렸지만 (정확한 영어는 "I've been talking too much" 또는 "I talked too much"), 이 비격식 자기 비하가 회의 분위기를 부드럽게 만든다. 네가 영어로 발표 후 "I did too much talking, any questions?"라고 하면, 듣는 사람이 질문하기 편해진다. 정확한 문법보다 **pragmatic 효과**가 중요한 예. 다만 정식 발표에서는 "I've been talking for a while, let me open it up for questions"가 더 안전하다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 발표자가 "아직 플랜임"을 계속 강조하며 약점을 포장하고, 질문자가 동의하며 도전하는 패턴. 양쪽 모두 non-native라서 한정어가 과도하게 밀집된 것도 특징.

### 전략 1: "Still in planning" 반복 (Status Hedging)

Montage 발표자는 회의 내내 "still in planning"을 반복하며 모든 스펙에 한정을 건다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 프로젝트 상태 | "basically, it is still in planning and some features might change depending on the communication with those big customers in China or even in the US" | "기본적으로 아직 플랜 단계이고, 중국이나 미국의 대형 고객과의 대화에 따라 일부 기능은 바뀔 수 있습니다" |
| 기능 지원 | "URL and PPR we are considering to support it as well. So it is still in planning, but we evaluate some design effort and we think they might be supported" | "URL과 PPR도 지원을 검토 중입니다. 아직 플랜 단계지만, 설계 노력을 평가해 보니 지원 가능할 것 같습니다" |

**패턴 공식**: `It is still in planning. Some features might change depending on X. But we are considering to support Y and we think it might be supported.`

**Audrey 교훈**: "still in planning" + "might" + "considering" - 삼중 한정. 발표자는 이걸로 모든 것에 빠져나갈 여지를 만든다. 영어 회의에서 확언을 피하고 싶을 때 "still in planning" + "might" 조합을 외워라. 한국어 "검토 중입니다"의 영어 버전이 "still in planning, but we think it might be supported"다. 다만 너무 남발하면 "이 사람은 아무것도 결정 못 하나"로 들리니, 중요한 건에는 쓰되 세부 사항에는 확언을 섞어라.

### 전략 2: 대안 복수 유지 (Multiple Option Hedging)

한 기능에 대해 "둘 다 지원 가능"이라며 선택을 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| ECC 엔진 선택 | "we are considering to put all of them in our chip so we can configure to use anyone" / "the both options and then the user can choose one of them" | "두 엔진 모두 칩에 넣을 수 있도록 검토 중이어서, 사용자가 어느 쪽이든 선택할 수 있습니다" |

**패턴 공식**: `We are considering to put all of them in our chip. The user can choose one of them. It's an option.`

**Audrey 교훈**: "It's an option" - 이 한마디가 결정을 미루는 전문가 화법이다. "둘 다 넣을 수 있으니, 사용자가 고르세요" - 발표자는 결정을 피하면서도 "유연성"으로 포장한다. 회의에서 결정을 미루고 싶을 때 "It's an option" 또는 "we can configure to use either one"을 써라. "we haven't decided"보다 훨씬 전문가 느낌.

### 전략 3: 고객 의존 회피 (Customer-Dependent Deflection)

기술적 어려움을 "고객 애플리케이션에 달렸다"로 돌린다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 공유 메모리 비율 | "we don't have exact number because we don't know what's the application running on top of that" / "it really depends on the application because we don't want to see all the links are running the BI request and response, but the real data access is very limited" | "정확한 수치는 없습니다. 애플리케이션을 모르니까요. 링크가 모두 BI 요청으로 돌아가는데 실제 데이터 접근이 제한되는 건 원치 않습니다" |

**패턴 공식**: `We don't have exact number because we don't know what's the application running on top of that. It really depends on the application.`

**Audrey 교훈**: "It really depends on the application" - 영어 회의에서 가장 자주 쓰이는 회피 화법 중 하나. 기술적 한계를 "애플리케이션에 달렸다"로 돌려서, 자기 책임을 줄인다. 이건 정당한 회피이기도 하다 - 진짜 애플리케이션에 달려 있으니까. 다만 "we don't have exact number because we don't know"는 솔직하지만 약하다. 더 강한 버전은 "the exact number depends on the application profile, which we'd need to characterize with you"다. 네가 파트너에게 "수치를 못 주겠다"고 할 때는 "depends on the application"으로 포장해라.

### 전략 4: 타사 의견 빌려오기 (Third-Party Authority Borrowing)

Intel과의 대화를 인용하며 자기 설계의 정당성을 확보한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| SNU filter 설계 | "we have been talking to Intel for a long time regarding the BI and smooth filter design... when we talk to Intel, we realize that maybe in a real application, the best way is to put a small portion" | "Intel과 오래 이야기했는데... 실제 애플리케이션에서는 작은 영역만 공유하는 게 최선이라는 걸 깨달았습니다" |

**패턴 공식**: `We have been talking to X for a long time regarding Y. We realize that maybe in a real application, the best way is to Z.`

**Audrey 교훈**: "we have been talking to Intel" - Intel이라는 권위를 빌려서 자기 설계 의견을 뒷받침한다. 영어 회의에서 "내 의견"보다 "X와 대화해 보니"가 더 강하다. 네가 설계 의견을 관철할 때, 타사와의 대화를 인용하라. "We've been talking to Intel/NVIDIA/Microsoft and we realize that..." - 이 패턴은 한국어 회의에서도 쓰이지만 영어에서는 더 빈번하다. 단, 실제로 대화한 경우에만 써라 - 거짓말은 들킨다.

### 전략 5: "I'm not sure" + 대안 제시 (Uncertainty Plus Pivot)

확신이 없을 때 "I'm not sure"로 인정하되, 즉시 방향을 돌린다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Xconn/Marvell 전환 영향 | "I don't know if this will impact Alibaba's plan for next generation" / "S-Con is acquired by Marvell" | "Alibaba 차세대 플랜에 영향이 있을지는 모르겠습니다. S-Con이 Marvell에 인수됐으니까요" |
| Panacea 스위치 샘플 | "I have no idea about as far as I know, they will have that" | "제가 아는 한, 그들은 그것을 가질 예정이지만 정확히는 모르겠습니다" |

**패턴 공식**: `I'm not sure / I don't know if X. But as far as I know, Y.`

**Audrey 교훈**: "I don't know"를 단독으로 쓰지 마라. "I don't know, but as far as I know, X" - 모르는 걸 인정하면서도 아는 만큼은 제시. 이게 non-native 발표자의 정직한 회피 화법이다. "I'm not sure"는 영어 회의에서 가장 안전한 표현 중 하나다 - 부정확한 정보로 잘못 말하는 것을 피하면서, 협조적으로 들린다.

### 전략 6: 동의하며 도전 (Agree-Then-Challenge)

발표자가 "I also have a similar opinion"으로 동의한 뒤 자기 의견을 덧붙인다. **이 회의에서 SK Hynix 질문자가 가장 많이 쓴 패턴**이다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 공유 메모리 영역 | "Yeah, I also had a similar opinion. I mean, before I met the Alibaba Cloud team, but Alibaba Cloud team told me they require a huge memory area" | "저도 비슷한 의견이었습니다. Alibaba Cloud 만나기 전엔요. 근데 그들은 공유용으로 엄청 큰 메모리 영역이 필요하다고 하더군요" |
| switchless 구현 | "I also have a similar opinion. I mean, like you. So the actual latency adder is introduced by this crossbar" | "저도 비슷한 의견입니다. 당신처럼요. 실제 latency 추가분은 이 crossbar에서 발생하니까요" |

**패턴 공식**: `I also have a similar opinion. I mean, like you. So...` 또는 `Yeah, I also had a similar opinion. But X told me Y.`

**Audrey 교훈**: 이게 이 회의의 **가장 중요한 화법**이다. "I also have a similar opinion" - 동의로 시작해서 자기 의견을 덧붙이는 한국식 정중 도전. 발표자를 공격하지 않으면서 다른 관점을 제시한다. "I agree, but..."보다 "I also have a similar opinion"이 더 부드럽다. 네가 파트너와 기술 의견이 다를 때, "I also have a similar opinion"으로 시작하면 상대가 방어하지 않고 들어준다. 그리고 "X told me Y"로 타사를 인용하면 더 강해진다. **이 패턴은 무조건 외워라.**

---

## 3. 정중한 도전 화법 (SK Hynix 질문자)

SK Hynix 질문자가 기술적으로 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다. 이 회의에서는 Marvell textbook 01보다 "동의하며 도전" 패턴이 훨씬 두드러진다.

### 질문 유형 1: 이해 확인형 질문 (Comprehension Check via Restatement)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So it means that X, right?` | "So it means that memory box should have the RDIM product, I mean, not the CXL device, right?" | "그러면 메모리 박스는 CXL 디바이스가 아니라 RDIM 제품을 써야 한다는 거죠?" - 재진술로 확인 |
| `So it means that, regardless of our decisions, we have to collaborate, co-work for the co-validation between our IOD and product and your multi-head controller. Am I correct?` | (line 487) | "Am I correct?" - 확인형 질문의 마침표 |

**Audrey 교훈**: "So it means that X, right?" - 발표자가 말한 걸 재진술하면서 확인하는 화법. 이게 가장 정중한 도전 형태다. 발표자가 잘못 말했으면 "아, 제가 잘못 들었나요?"로 자연스럽게 정정하게 만든다. 그리고 "Am I correct?"를 끝에 붙이면, 발표자가 "Yes" 또는 "No, actually..."로 답해야 한다. Marvell textbook의 "Just to make sure I understand correctly"와 같은 기능이지만 더 짧은 버전. 회의에서 발표자가 길게 설명하면, "So it means that X, right?"로 짧게 재진술하며 확인해라.

### 질문 유형 2: "Am I correct?" 확인형 (Confirmation Tag)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `X. Am I correct?` | "the reference, the memory pooling box will have the four multi-head controllers. Am I correct?" / "the SSSK hynix is interested in multi-head controller? And if we have any plan to make the memory box, am I correct?" | "Am I correct?" - 확인 tag |

**Audrey 교훈**: "Am I correct?"는 "right?"보다 조금 더 격식 있고, 발표자가 "Yes/No"로 명확히 답해야 한다. 발표자의 의도를 확인하거나, 자기 이해를 검증할 때 써라. 질문이라기보다 "확인"이라서 발표자가 방어적으로 반응하지 않는다. 회의에서 중요한 사실을 명확히 할 때, "X. Am I correct?"로 닫아라.

### 질문 유형 3: 동의 + 재포장 도전 (Agree and Repackage)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Yeah, but as you mentioned X, I believe they will, I mean, much better. I mean, but the latency number rather than the switch, and but you only have the fixed, the port number` | "Yeah, but as you mentioned that or from your slide that and I mean, it will be the faster way because you already have a good experience and the design ready from your controller product and just adding the more port" | "맞는데, 슬라이드에도 있듯이 더 빠른 길일 것 같습니다. 이미 컨트롤러 제품에서 설계가 준비되어 있으니까요" - 동의 + 장점 재포장 |
| `I totally agree with your opinion. That switch list has a better latency number in the performance wise. And then we also have approved it, switched this prototype` | "I totally agree with your opinion. That switch list has a better latency number in the performance wise" | "완전 동의합니다. switchless가 latency 성능이 더 좋다는 거" - "totally agree"로 강한 동의 |

**Audrey 교훈**: "I totally agree with your opinion" - 동의를 먼저 주고, 그 다음에 자기 의견을 덧붙인다. 이 패턴은 발표자를 칭찬하면서도 자기 관점을 제시하는 고급 화법이다. "I agree with X. But Y"보다 "I agree with X. And we also have Z"가 더 협조적이다. 회의에서 파트너 의견에 부분 동의할 때, "I totally agree with your opinion on X"로 시작하면, 그 다음에 다른 점을 말해도 상대가 듣는다.

### 질문 유형 4: 이유 탐색형 (Reason Probe via "What is the reason")

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `But is there any specific reason why you lower the 6400?` | "But Gen3 can support up to the 8000. But is there any specific reason why you lower the 6400?" | "specific reason why" - 설계 의도 탐색 |
| `But why are you considering the 4 nanometer?` | "But why are you considering the 4 nanometer? I mean, provide better performance and lower power, especially the power because this is a huge chip" | 스스로 답을 제시하며 확인 |

**Audrey 교훈**: "But is there any specific reason why X?" - Marvell textbook의 "Is there any reason to X?"와 같은 패턴이지만 "specific"이 붙어 더 정밀하다. "Why did you X?"는 공격적이지만, "Is there any specific reason why you X?"는 정중하다. 회의에서 설계 결정을 도전할 때 써라. 그리고 발표자가 대답하기 전에 자기 추측을 제시하면, 발표자는 "Yes, exactly"로 답하기 편해진다 - 이게 "답을 알면서 질문하기" 화법이다.

### 질문 유형 5: 타사 의견 인용 도전 (Third-Party Opinion Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `One other thing is I heard that when I had some discussion opportunity with the other CXL controller partner, the implementation of the memory sharing, I mean, based on with using the BI and the SNU filter with switch list case, technically it will be very difficult to support the hardware cache coherency. Are you agree with that opinion?` | (line 92-93) | "다른 컨트롤러 파트너가 switchless에서 하드웨어 cache coherency 구현이 어렵다고 하던데, 동의하십니까?" - 타사 의견 인용 도전 |

**Audrey 교훈**: 이게 **이 회의에서 가장 강한 도전 화법**이다. "Are you agree with that opinion?" - 문법적으로는 틀렸지만 (정확한 영어는 "Do you agree with that opinion?"), 타사 의견을 인용하면서 발표자에게 "동의하십니까?"로 직접 물었다. 발표자는 "What's the reason I don't quite understand this conclusion?"로 반문하며 방어한다. 타사 의견을 빌려오면, 자기가 공격하는 게 아니라 "다른 사람이 이렇게 말했는데, 어떻게 생각하세요?"가 되어 더 강하다. 네가 파트너 기술을 도전할 때, "다른 파트너가 X라고 하던데, 동의하십니까?"로 물어라. 단, 문법은 "Do you agree with that opinion?"로 정확히 써라.

### 질문 유형 6: 미래 계획 탐색 (Future Plan Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Do you have a plan to support X in the future?` | (이 회의에서는 명시적 사용 없음, 그러나 "will you make this kind of a reference platform after having the real silicon?"가 유사) | 미래 계획 탐색 |
| `Will you make that kind of prototype reference?` | "Will you make that kind of prototype reference?" / "Oh, will you have a plan to support ADDR?" | "Will you make" + "have a plan to support" |

**Audrey 교훈**: "Will you make X?"와 "Do you have a plan to support Y?" - 미래 계획을 묻는 두 가지 형태. "Will you make"는 직접적이고, "Do you have a plan to support"는 더 정중하다. 회의에서 파트너의 로드맵을 물을 때, "Do you have a plan to support X in the future?"가 가장 안전하다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의는 "planning phase" 회의라서 공식적 협상보다는 **상호 탐색**이 주다. 그래서 협상 화법보다는 "의향 표시"와 "후속 약속"이 중심이다.

### 협상·의향 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 의향 표시 | SK | "So yeah, we are interested in that kind of solution" | "interested in that kind of solution" - 부드러운 의향 표시 |
| 결정 미루기 | SK | "But as I mentioned in only this meeting, so we need to compare the pros and cons between the switch and switch list pooling system" | "compare the pros and cons between X and Y" - 결정 미루기의 정당화 |
| 타임라인 압박 | SK | "And then could you please share your timeline again?" / "Our challenge is to take all this product in true form this year" | "challenge is to take X in true form this year" - 타임라인 압박의 정중한 표현 |
| 공동 작업 필요성 강조 | SK | "So it means that we, regardless of our decisions, we have to collaborate, co-work for the co-validation between our IOD and product and your multi-head controller. Am I correct?" | "regardless of our decisions, we have to collaborate" - 결정과 무관한 협력 필요성 강조 |
| 진지함 표시 | SK | "But I think that because we are memory suppliers, so if we have some new sales point, unique sales point, and we can reduce the TCO level in the system level design from SK-Hynix, and if we have a strong competitiveness, I think that it might be reasonable" | "unique sales point" + "reduce TCO" - 비즈니스 가치 제시 |

**Audrey 교훈**:
- "we are interested in that kind of solution" - "관심 있다"는 의향 표시. 회의에서 "we want X"가 아니라 "we are interested in"이 더 정중하고 여유 있다. 약한 관심처럼 들리지만, 사실은 강한 신호다 - "관심 없으면 안 나온다"는 비즈니스 관례.
- "compare the pros and cons between X and Y" - 결정을 미룰 때 쓰는 정당화. "아직 비교해야 합니다" - 한국어 "검토해 보겠습니다"의 영어 버전이지만, "compare the pros and cons"가 더 구체적이라서 더 진지하게 들린다.
- "regardless of our decisions, we have to collaborate" - 이게 협상의 핵심 문장이다. "우리 결정과 무관하게 협력해야 한다" - 발표자의 플랜이 결정되든 안 되든, 공동 검증은 필요하다는 점을 못 박는다. 회의에서 협력을 확약할 때 "regardless of X, we have to Y"를 써라.
- "unique sales point" + "reduce TCO" - 비즈니스 가치를 제시하는 두 가지 축. 기술 회의에서 비즈니스 언어를 섞으면 발표자에게 "이 사람은 비즈니스까지 생각하는구나"로 들린다.

### Action Item / 후속 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 채널 약속 | 공통 | "let's keep in touch" / "Talk to you later" | 비격식 후속 약속 |
| 타사 대안 공유 | SK | "Yeah, we can keep an eye on that because yeah, because we are not able to get the Sconn new switch. So there's other alternatives from Panacea. Maybe we can try to do some interoperability test with our G3 device" | "keep an eye on" + "do some interoperability test" - 구체적 후속 제안 |
| 정보 교환 제의 | SK | "But we are also trying to discuss the Marvell. So, but I think that it is still the migration from the Xconn to Marvell" | 경쟁사 동향 공유 - 신뢰 구축 |

**Audrey 교훈**: 이 회의에는 공식 action item이 거의 없다. "let's keep in touch"로 끝나는 게 특징 - planning phase 회의라서, 다음 단계가 정해지지 않았다. 다만 SK Hynix가 "Panacea 대안을 지켜보자"며 구체적 후속을 제시하는 건 주목할 만하다. "keep an eye on X" - "지켜보자"는 회의에서 후속을 약속하는 부드러운 화법이다. "monitor"보다 일상적이고, "track"보다 비격식적이다. 회의에서 "we'll keep an eye on that"로 후속을 약속해라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/memory pooling 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **switchless** | CXL 스위치 없이 다중 호스트를 메모리에 직접 연결하는 아키텍처 | "the other one is similar to your proposal, the Switch-List" (전사 오기 - "switchless"를 "switch list"로 잘못 전사) |
| **multi-head device** | 다중 호스트 포트를 가진 CXL 메모리 익스팬더 | "build a new multi-head device to fulfill the memory pooling applications" - "multi-head"가 이 회의의 핵심 명사 |
| **memory pooling** | 다수 호스트가 공유 메모리 풀에 접근하는 CXL 사용 모델 | "prove the memory pooling system and its advantage in the data center level" - "memory pooling applications" |
| **S-Con / S-Conn** | switching 컨트롤러 (정확한 이름 불명확, 아마도 XConn/상용 CXL 스위치 IP) | "S-Con currently is the only one renderer who can provide a Switch" |
| **RDIM** (Registered DIMM) | 레지스터드 DRAM 모듈 | "it will be RDIM support because it will be built in the memory box" - CXL 디바이스가 아니라 RDIM 사용 |
| **DPC** (DIMM Per Channel) | 채널당 DIMM 수 | "1 DPC, 8000 and 2 DPC, 6400" - 1 DPC는 8000 MT/s, 2 DPC는 6400 MT/s |
| **SNU filter** (Snoop Filter Unit) | 다중 호스트 캐시 일관성을 위한 스눕 필터 | "the only gap from the switch list fabric and SNU filter will be the 40 to 60 nanoseconds" - SNU filter가 latency 추가분 원인 |
| **BI** (Back invalidate) | 캐시 무효화 요청 - 다른 호스트의 캐시를 무효화 | "if all the spaces are shared by A host, and there are a lot of random access, there will be a lot of BI requests and response on the link" |
| **crossbar data fabric** | Montage 자체 설계한 유연한 데이터 패브릭 | "this is our own design for a very flexible crossbar data fabric" |
| **fabric manager** | CXL 패브릭 자원 관리 소프트웨어 스택 | "who will make it the fabric manager stack, software stack? You?" |
| **open BMC** | 오픈 소스 BMC 소프트웨어 스택 | "we will have some reference design based on the open BMC" |
| **CDFP** (Cable Direct Fabric Protocol / 400G form factor) | 전기 동케이블 커넥터 폼팩터 | "the majority of the current server system are using the CDFP. So we will build a design with the CDFP" - 광케이블 아님, "regular electrical, the copper cable" |
| **ADDR** (Advanced DRAM ECC by Microsoft) | Microsoft 제안 ECC 알고리즘 | "we are also considering the proposal from Microsoft... ADDR... we are considering to put all of them in our chip" |
| **Reed-Solomon** | 기존 ECC 엔진 | "maybe you change it to the ECC engine from the Reed-Solomon to the ADDR?" - 두 옵션 비교 |
| **URL / PPR** | Uncorrectable Error Logging / Post Package Repair - 메모리 RAS 기능 | "URL and PPR we are considering to support it as well" |
| **tape out / full take-out** | 칩 설계 완료·제조 의뢰 | "we have to do the full take-out" - "full mask" (셔틀 아닌 전체 마스크) 의 의미 |
| **POC** (Proof of Concept) | 개념 증명 프로토타입 | "we will build a POC based on our current Gen3 device" |
| **CXL metadata** | CXL 2.0/3.0 디바이스 메타데이터 | "we just supported the metadata of the CXL 2.0 and CXL 3.0" |
| **PCIe mode** | CXL 디바이스를 PCIe 모드로 동작시키는 기능 | "we can also make it to work as a PCIe mode, not only a CXL mode" - GPU가 CXL 미지원인 환경 대응 |
| **mailbox command** | CXL 디바이스 관리용 명령 인터페이스 | "they cannot use the mailbox command" - PCIe 모드의 제약 |
| **shuttle** | 다수 칩이 한 마스크를 공유하는 소량 생산 방식 | "we cannot do shuttle with this big size... we have to do the full take-out" - 칩이 커서 shuttle 불가 |
| **6 nanometer / 4 nanometer** | TSMC 공정 노드 | "depends on we are going to use the 6 nanometer or the 4 nanometer... if we go with 4 nanometer, then the power can be saved" |
| **IOD** (I/O Die) | CPU/SoC의 I/O 컨트롤러 다이 | "the IOD should be required... we have to collaborate, co-work for the co-validation between our IOD and product and your multi-head controller" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m26-001
  expression: "At this moment, X is not so good"
  category: problem_framing
  function: negative_premise
  speaker_role: presenter
  difficulty: 3
  context: "At this moment, Switch is not so good, a metaphor of the ecosystem or the performance itself"
  note: 부정 전제로 발표 시작 - "지금 안 좋다"로 긴장감 설정

- id: m26-002
  expression: "X currently is the only one who can provide a Y"
  category: problem_framing
  function: single_vendor_risk
  speaker_role: presenter
  difficulty: 3
  context: "S-Con currently is the only one renderer who can provide a Switch"
  note: 단일 공급자 = 위험 프레이밍

- id: m26-003
  expression: "X also complained that the current Y is not so good in performance"
  category: third_party_complaint
  function: borrowed_authority
  speaker_role: presenter
  difficulty: 4
  context: "Alibaba also complained that the current memory box is not so good in performance"
  note: 타사 불만 인용 - 자기 의견에 타사 권위 빌리기

- id: m26-004
  expression: "that's why we are considering to design a new product based on our existing designs"
  category: alternative_reveal
  function: solution_link
  speaker_role: presenter
  difficulty: 4
  context: "that's why we are considering to design a new product based on our existing designs to build a new multi-head device"
  note: "considering" - 아직 결정 아님 표시

- id: m26-005
  expression: "we believe with the integrated design, this X can provide better benefits, no matter from Y, Z and W"
  category: benefit_enumeration
  function: three_axis_persuasion
  speaker_role: presenter
  difficulty: 5
  context: "we believe with the integrated design and this multi-head device can provide better, more benefits, no matter from the latency, the cost and the power"
  note: "no matter from X, Y, Z" - 3개 축 동시 나열

- id: m26-006
  expression: "we are also engaging with some X customers to see if they are in this proposal"
  category: demand_validation
  function: market_probe
  speaker_role: presenter
  difficulty: 4
  context: "we are also engaging with some China top CSP customers to see if they are in this proposal and if we have enough demand from those guys and we can kick off this project"
  note: "if...if...and" 조건 연쇄로 플랜 가중 검증

- id: m26-007
  expression: "if we have enough demand from those guys, we can kick off this project"
  category: conditional_kickoff
  function: project_start_signal
  speaker_role: presenter
  difficulty: 3
  context: "if we have enough demand from those guys and we can kick off this project"

- id: m26-008
  expression: "it is still in planning and some features might change depending on X"
  category: status_hedging
  function: planning_disclaimer
  speaker_role: presenter
  difficulty: 4
  context: "basically, it is still in planning and some features might change depending on the communication with those big customers"
  note: "still in planning" + "might change" - 이중 한정. 회의에서 가장 자주 쓰는 회피

- id: m26-009
  expression: "since you already have the slides in hand, I can quickly go through this one"
  category: pace_control
  function: walkthrough_setup
  speaker_role: presenter
  difficulty: 3
  context: "since you already have the slides in hand, so I can quickly go through this one"

- id: m26-010
  expression: "I did too much talk. So anyone any question from X?"
  category: question_invitation
  function: self_deprecation_close
  speaker_role: presenter
  difficulty: 3
  context: "I did too much talk. So anyone any question from the SK hynix?"
  note: 비격식 자기 비하 + 질문 유도. pragmatic 효과 큼

# ── 회피·포장 (Hedging & Deflection) ──
- id: m26-011
  expression: "it is still in planning, but we evaluate some design effort and we think they might be supported"
  category: triple_hedging
  function: conditional_support
  speaker_role: presenter
  difficulty: 4
  context: "URL and PPR we are considering to support it as well. So it is still in planning, but we evaluate some design effort and we think they might be supported"
  note: "considering" + "still in planning" + "might" - 삼중 한정

- id: m26-012
  expression: "we are considering to put all of them in our chip so we can configure to use anyone"
  category: multiple_option_hedging
  function: decision_deferral
  speaker_role: presenter
  difficulty: 4
  context: "we are considering to put all of them in our chip so we can, we can, we can configure to use anyone"

- id: m26-013
  expression: "the both options and then the user can choose one of them. It's an option."
  category: option_presentation
  function: user_choice_deferral
  speaker_role: presenter
  difficulty: 3
  context: "currently are you considering having the both options and then the user can choose one of them. Yeah, exactly. Okay. It's an option."
  note: "It's an option" - 결정 미루는 전문가 화법

- id: m26-014
  expression: "we don't have exact number because we don't know what's the application running on top of that"
  category: customer_dependent_deflection
  function: technical_limit_blame_app
  speaker_role: presenter
  difficulty: 4
  context: "We don't have exact number because we don't know what's the application running on top of that"
  note: 기술적 어려움을 "애플리케이션에 달렸다"로 돌리는 회피

- id: m26-015
  expression: "it really depends on the application because we don't want to see X"
  category: application_dependency
  function: constraint_justification
  speaker_role: presenter
  difficulty: 4
  context: "it really depends on the application because we don't want to see all the links are running the BI request and response, but the real data access is very limited"
  note: "It really depends on the application" - 영어 회의 가장 빈번 회피 화법

- id: m26-016
  expression: "we have been talking to X for a long time regarding Y"
  category: third_party_authority
  function: borrowed_design_validation
  speaker_role: presenter
  difficulty: 5
  context: "we actually we have been talking to Intel for a long time regarding the BI and smooth filter design"
  note: Intel 권위 빌려서 자기 설계 정당화

- id: m26-017
  expression: "we realize that maybe in a real application, the best way is to Z"
  category: insight_from_dialog
  function: design_conclusion
  speaker_role: presenter
  difficulty: 4
  context: "when we talk to Intel, we realize that maybe in a real application, the best way is to put a small portion"
  note: "we realize that maybe" - 대화에서 깨달은 것을 인용

- id: m26-018
  expression: "I don't know if this will impact X"
  category: uncertainty_stated
  function: honest_unknown
  speaker_role: presenter
  difficulty: 3
  context: "I don't know if this will impact Alibaba's plan for next generation"
  note: "I don't know" 단독 금지 - 뒤에 "but as far as I know" 붙이기

- id: m26-019
  expression: "I have no idea about, as far as I know, X"
  category: knowledge_boundary
  function: bounded_admission
  speaker_role: presenter
  difficulty: 3
  context: "I have no idea about as far as I know, they will have that"

- id: m26-020
  expression: "so far, we don't see any problem to support X"
  category: capability_claim
  function: positive_capability
  speaker_role: presenter
  difficulty: 4
  context: "So far, we don't see any problem to support the hardware sharing by these switch list cutting heads when we talk to you for this idea"

- id: m26-021
  expression: "we will do some trade off to see if we can put all of them in this chip"
  category: tradeoff_commitment
  function: design_decision_pending
  speaker_role: presenter
  difficulty: 4
  context: "we will do some trade off to see if we can put all of them in the, in the, in this chip"
  note: "do some trade off" - 설계 결정 미루는 기술적 화법

- id: m26-022
  expression: "I'm not sure, but I think X"
  category: hedged_opinion
  function: soft_judgment
  speaker_role: presenter
  difficulty: 3
  context: "I'm not sure the, I mean, really in the customer and the user, I mean, have a plan to make the, that kind of the system architecture"

# ── 정중한 도전 (Polite Challenge) ──
- id: m26-023
  expression: "So it means that X, right?"
  category: restatement_check
  function: comprehension_via_restate
  speaker_role: questioner
  difficulty: 4
  context: "So it means that memory box should have the RDIM product, I mean, not the CXL device, right?"
  note: 재진술로 확인 - 가장 정중한 도전 형태

- id: m26-024
  expression: "X. Am I correct?"
  category: confirmation_tag
  function: explicit_validation
  speaker_role: questioner
  difficulty: 3
  context: "the reference, the memory pooling box will have the four multi-head controllers. Am I correct?"

- id: m26-025
  expression: "I also have a similar opinion. I mean, like you."
  category: agree_then_challenge
  function: korean_polite_challenge
  speaker_role: questioner
  difficulty: 5
  context: "I also have a similar opinion. I mean, like you. So the actual latency adder is introduced by this crossbar"
  note: 이 회의의 가장 중요한 화법. 동의로 시작해서 자기 의견 제시

- id: m26-026
  expression: "Yeah, I also had a similar opinion. But X told me Y."
  category: agree_with_counter_evidence
  function: polite_contradiction
  speaker_role: questioner
  difficulty: 5
  context: "Yeah, I also had a similar opinion. I mean, before I met the Alibaba Cloud team, but Alibaba Cloud team told me they require a huge memory area"
  note: 동의 + 타사 증거로 정중한 반박

- id: m26-027
  expression: "I totally agree with your opinion. That X has Y."
  category: strong_agreement
  function: validation_before_push
  speaker_role: questioner
  difficulty: 4
  context: "I totally agree with your opinion. That switch list has a better latency number in the performance wise"
  note: "totally agree" - 강한 동의로 발표자 칭찬 후 자기 의견

- id: m26-028
  expression: "But is there any specific reason why you X?"
  category: reason_probe
  function: design_intent_question
  speaker_role: questioner
  difficulty: 4
  context: "But Gen3 can support up to the 8000. But is there any specific reason why you lower the 6400?"
  note: "specific reason why" - "Why did you X?" 대신 정중한 화법

- id: m26-029
  expression: "But why are you considering X? I mean, provide better Y and lower Z"
  category: answer_assisted_question
  function: prompt_with_hint
  speaker_role: questioner
  difficulty: 4
  context: "But why are you considering the 4 nanometer? I mean, provide better performance and lower power"
  note: 답을 알면서 질문하기 - 발표자가 "Yes, exactly"로 답하기 편하게

- id: m26-030
  expression: "I heard that when I had some discussion opportunity with the other X partner, Y. Are you agree with that opinion?"
  category: third_party_probe
  function: strongest_challenge
  speaker_role: questioner
  difficulty: 5
  context: "I heard that when I had some discussion opportunity with the other CXL controller partner... it will be very difficult to support the hardware cache coherency. Are you agree with that opinion?"
  note: 타사 의견 인용 도전 - 회의에서 가장 강한 도전. 단 "Do you agree"가 문법적 정확

- id: m26-031
  expression: "What's the reason I don't quite understand this conclusion?"
  category: counter_probe
  function: deflect_challenge
  speaker_role: presenter
  difficulty: 4
  context: "What's the reason I don't quite understand this conclusion? I mean, remember all the details of the backup reason why they told me the kind of the opinion?"
  note: 도전을 받았을 때 되묻는 방어 화법

- id: m26-032
  expression: "I'm not familiar with that, but is that the similar X with Y?"
  category: humble_comparison
  function: learning_question
  speaker_role: questioner
  difficulty: 5
  context: (Marvell textbook와 유사, 이 회의에서는 명시 사용 없으나 패턴 학습용 포함)

- id: m26-033
  expression: "Will you make X?"
  category: direct_future_probe
  function: commitment_check
  speaker_role: questioner
  difficulty: 2
  context: "Will you make that kind of prototype reference?"

- id: m26-034
  expression: "Oh, will you have a plan to support X?"
  category: plan_probe
  function: roadmap_question
  speaker_role: questioner
  difficulty: 3
  context: "Oh, will you have a plan to support ADDR?"

- id: m26-035
  expression: "Is it possible to support the X because it is based on Y?"
  category: feasibility_probe
  function: technical_possibility
  speaker_role: questioner
  difficulty: 4
  context: "Is it possible to support the smooth filter and the BI because it is based on the R-Dim?"

# ── 협상·액션 (Negotiation) ──
- id: m26-036
  expression: "we are interested in that kind of solution"
  category: interest_signal
  function: soft_intent
  speaker_role: negotiator
  difficulty: 3
  context: "So yeah, we are interested in that kind of solution"
  note: "we want X" 대신 "we are interested in" - 정중한 의향 표시

- id: m26-037
  expression: "we need to compare the pros and cons between X and Y"
  category: decision_deferral
  function: justified_delay
  speaker_role: negotiator
  difficulty: 4
  context: "we need to compare the pros and cons between the switch and switch list pooling system"
  note: 결정 미루기 정당화 - "검토해 보겠습니다" 영어 버전

- id: m26-038
  expression: "our challenge is to take all this product in true form this year"
  category: timeline_pressure
  function: polite_urgency
  speaker_role: negotiator
  difficulty: 4
  context: "Our challenge is to take all this product in true form this year"

- id: m26-039
  expression: "could you please share your timeline again?"
  category: timeline_request
  function: direct_ask
  speaker_role: negotiator
  difficulty: 2
  context: "And then could you please share your timeline again?"

- id: m26-040
  expression: "regardless of our decisions, we have to collaborate, co-work for the co-validation between X and Y"
  category: collaboration_commitment
  function: decision_independent_partnership
  speaker_role: negotiator
  difficulty: 5
  context: "regardless of our decisions, we have to collaborate, co-work for the co-validation between our IOD and product and your multi-head controller. Am I correct?"
  note: 협상 핵심 문장 - 결정과 무관한 협력 확약

- id: m26-041
  expression: "if we have some unique sales point, and we can reduce the TCO level in the system level design from X, I think that it might be reasonable"
  category: business_value
  function: value_proposition
  speaker_role: negotiator
  difficulty: 5
  context: "if we have some new sales point, unique sales point, and we can reduce the TCO level in the system level design from SK-Hynix, and if we have a strong competitiveness, I think that it might be reasonable"
  note: "unique sales point" + "reduce TCO" - 비즈니스 가치 제시

- id: m26-042
  expression: "we can keep an eye on that"
  category: follow_up_soft
  function: monitoring_promise
  speaker_role: negotiator
  difficulty: 3
  context: "Yeah, we can keep an eye on that because yeah, because we are not able to get the Sconn new switch"

- id: m26-043
  expression: "maybe we can try to do some interoperability test with our X device"
  category: concrete_follow_up
  function: specific_next_step
  speaker_role: negotiator
  difficulty: 3
  context: "Maybe we can try to do some interoperability test with our G3 device"

- id: m26-044
  expression: "let's keep in touch"
  category: informal_close
  function: soft_follow_up
  speaker_role: both
  difficulty: 1
  context: "And yeah, let's keep in touch"

- id: m26-045
  expression: "is it solid plan or still under discussion?"
  category: commitment_check
  function: plan_status_question
  speaker_role: questioner
  difficulty: 4
  context: "And so is it solid plan or still under discussion? It's still under discussion."

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m26-046
  expression: "we can kick off this project"
  category: project_verb
  function: project_start
  speaker_role: presenter
  difficulty: 2
  context: "if we have enough demand from those guys and we can kick off this project"
  note: "kick off" - 비즈니스 영어 일상 동사

- id: m26-047
  expression: "we cannot do shuttle with this big size, we have to do the full take-out"
  category: silicon_manufacturing
  function: tape_out_constraint
  speaker_role: presenter
  difficulty: 4
  context: "this chip will be a huge chip and we cannot, cannot do shuttle with this big size... we have to do the full take-out"
  note: shuttle vs full mask - 칩이 크면 shuttle 불가

- id: m26-048
  expression: "the latency adder is introduced by X"
  category: technical_attribution
  function: component_blame
  speaker_role: both
  difficulty: 4
  context: "the actual latency adder is introduced by this crossbar in the SNU filter"

- id: m26-049
  expression: "the only gap from X will be Y"
  category: delta_specification
  function: difference_quantify
  speaker_role: presenter
  difficulty: 4
  context: "the only gap from the switch list fabric and SNU filter will be the 40 to 60 nanoseconds"

- id: m26-050
  expression: "we will build a design with the X"
  category: design_commitment
  function: tech_selection
  speaker_role: presenter
  difficulty: 3
  context: "we will build a design with the CDFP"

# ── 담화 표지 (Discourse Markers) ──
- id: m26-051
  expression: "yeah, you can skip the rest of them"
  category: pacing_control
  function: time_saving
  speaker_role: questioner
  difficulty: 2
  context: "Oh, no, no, no, you can skip the rest of them. Yeah, I understand totally"
  note: 질문자가 발표 속도 조절 - 친밀감 표시

- id: m26-052
  expression: "I think you are very familiar with those contents"
  category: audience_assessment
  function: skip_permission
  speaker_role: presenter
  difficulty: 3
  context: "I think you are very familiar with those contents"
  note: 청중 수준 평가 후 스킵 - 발표자 유연성
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-04 10 02 50_EN_Montage_switchless-extracted.wav` (총 ~50분 추정, 6,013단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-15) | 발표자 "Switch is not so good" + Alibaba 불만 인용 + multi-head 제안 | 타사 불만 인용 발화 공식 | ★★★ |
| 2 | POC 설명 (line 33-50) | "we also have the POC, the prototype of the switch list" + "we don't like to prove the memory pooling system" | POC 설명 + 목적 나열 | ★★★ |
| 3 | 동의하며 도전 (line 70-90) | "I also had a similar opinion. But Alibaba told me..." + "we can have some fixed area for sharing" | 한국식 정중 도전 화법 | ★★★★ |
| 4 | 타사 의견 도전 (line 92-115) | "다른 컨트롤러 파트너가 switchless에서 cache coherency 어렵다고 하던데, 동의하십니까?" + 발표자 방어 | 가장 강한 도전 + 방어 | ★★★★★ |
| 5 | 협상 마무리 (line 487-560) | "regardless of our decisions, we have to collaborate" + "we are interested in that kind of solution" + timeline 비교 | 협상 의향 표시 + 협력 확약 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 4가 가장 가치 높음 - 동의하며 도전 + 타사 의견 도전 화법 밀집
- 발췌 4는 이 회의의 하이라이트 - "Are you agree with that opinion?"가 나오는 곳

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **"planning phase technical dialogue"** register다. Marvell textbook 01이 "완성된 제품 pitch + defense"였다면, 이 회의는 "미완성 컨셉트 + 공동 탐색"이다. 이 차이가 화법을 다르게 만든다:
- **발표자 역할 (Montage)**: "still in planning" 회피 과다, 타사 권위 빌리기, "considering" 한정어 남발 - 아직 플랜임을 계속 강조
- **질문자 역할 (SK Hynix)**: "I also have a similar opinion" 동의하며 도전, 타사 의견 인용, "Am I correct?" 확인형 질문 - 발표자를 공격하지 않으면서 기술 검증

양쪽 모두 non-native 영어 사용자라서, 문법적 비틀림이 잦지만 **pragmatic 효과는 정확**하다. 예: "I did too much talk" (문법 틀림, 하지만 자기 비하+질문 유도 효과는 정확), "Are you agree with that opinion?" (문법 틀림, 하지만 도전 효과는 정확).

### Pragmatics (화용론) 핵심
1. **동의하며 도전**: "I also have a similar opinion"으로 시작하면, 그 다음에 다른 의견을 말해도 발표자가 방어하지 않는다. 이게 한국어 회의에서 "맞습니다, 그런데요"의 영어 버전. "I agree, but..."보다 "I also have a similar opinion. But X told me Y"가 훨씬 부드럽다.
2. **타사 의견 인용 도전**: 자기가 공격하는 게 아니라 "다른 파트너가 이렇게 말했는데, 동의하십니까?"로 물으면, 발표자는 타사 의견에 반박해야 하니 공격 난이도가 올라간다. 이 회의에서 가장 강한 도전.
3. **"still in planning" 삼중 한정**: "considering" + "still in planning" + "might" - 발표자가 이걸로 모든 것에 빠져나갈 여지를 만든다. 회의에서 확언을 피하고 싶을 때 쓰되, 너무 남발하면 "결정 못 하는 사람"으로 들리니 중요한 건에는 확언을 섞어라.
4. **"It's an option"으로 결정 미루기**: "둘 다 지원 가능, 사용자가 고르세요" - 결정을 "유연성"으로 포장하는 고급 화법.
5. **타사 권위 빌리기**: "we have been talking to Intel" - 자기 설계 의견을 Intel과의 대화로 뒷받침. "내 의견"보다 "X와 대화해 보니"가 더 강하다.

### 네가 당장 써야 할 Top 5
1. **"I also have a similar opinion. But X told me Y."** - 동의하며 도전하는 한국식 정중 도전
2. **"So it means that X, right?"** - 재진술로 확인하는 정중한 도전
3. **"we don't have exact number because we don't know what's the application running on top of that"** - 기술적 회피의 정석
4. **"regardless of our decisions, we have to collaborate"** - 결정과 무관한 협력 확약
5. **"it is still in planning and some features might change depending on X"** - planning phase 회피 화법

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "맞습니다, 그런데요" | "I also have a similar opinion. But X told me Y." | 한국어는 "그런데" 한 단어, 영어는 "similar opinion"으로 동의 명시 |
| "다른 파트너가 어렵다고 하던데요" | "I heard that when I had some discussion opportunity with the other X partner, Y. Are you agree with that opinion?" | 타사 의견 인용 + 직접 질문 |
| "검토 중입니다" | "it is still in planning and some features might change depending on X" | 영어가 더 구체적 - "depending on"으로 이유 명시 |
| "둘 다 가능합니다" | "the both options and then the user can choose one of them. It's an option." | 영어는 "It's an option"으로 마침 |
| "결정 무관하게 협력해야 합니다" | "regardless of our decisions, we have to collaborate, co-work for the co-validation" | "regardless of" - 명시적 전제 |

### 이 회의와 Marvell textbook 01의 비교
| 차원 | Marvell 01 (2026-08-25) | Montage 26 (2026-02-04) |
|:---|:---|:---|
| 제품 상태 | 완성 제품 (tape out 완료, ES Q4) | 미완성 컨셉트 (still in planning) |
| 발표자 회피 | "next generation" 미루기 + "definitely" 부드럽게 | "still in planning" 삼중 한정 + "It's an option" |
| 질문자 도전 | "Just to make sure I understand correctly" 정중 전제 | "I also have a similar opinion" 동의하며 도전 |
| 협상 | "We are hoping X can help address Y" 부드러운 요구 | "regardless of our decisions, we have to collaborate" 협력 확약 |
| 비즈니스 가치 | "actionable collaboration proposal soon" | "unique sales point" + "reduce TCO" |
| 언어 모델 | native 비즈니스 영어 | non-native 영어, pragmatic 정확 |

**Audrey 종합**: Marvell 01은 "완성된 제품을 파는" 회의, Montage 26은 "미완성 컨셉트를 탐색하는" 회의다. 두 가지 상황에서 네가 써야 할 화법이 다르다. 완성 제품을 평가할 때는 "Just to make sure I understand correctly"로 정중 도전. 미완성 컨셉트를 탐색할 때는 "I also have a similar opinion"으로 동의하며 도전. 두 textbook을 짝으로 학습해라.

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법(특히 "still in planning" 삼중 한정) + 3절 동의하며 도전 화법("I also have a similar opinion") 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **Marvell 01과 짝 학습**: 이 교재는 Marvell textbook 01과 짝을 이룬다 - 01은 완성 제품 pitch, 26은 미완성 컨셉트 탐색. 두 가지 회의 상황에서 써야 할 화법이 다름을 비교 학습

---

*Textbook 26 - Montage switchless CXL expander (2026-02-04). 회의 유형 A (기술 Deep-dive) - confirmed. 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-02.*
