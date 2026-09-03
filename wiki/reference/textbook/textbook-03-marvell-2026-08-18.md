---
textbook_id: 03
meeting: Marvell (Structera X / DDR5 expansion + NDP)
date: 2026-08-18
type: B (로드맵/공급 정합) - 초기 할당 A(기술 deep-dive)에서 재분류
partner: Marvell (Crown / Q-lam)
sk_side: SK Hynix (Jerry, Guangxing)
duration_words: 3087
audio: repo/webex-audio/2026-08-18 09 01 10_EN_Marvell-extracted.wav
transcript: repo/webex-audio/2026-08-18 09 01 10_EN_Marvell-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, marvell, structera, ddr5, ndp, near-memory-compute, aic-card, pcb-supply, roadmap-alignment, type-b]
---

# Textbook 03 - Marvell DDR5 Expansion + NDP (2026-08-18)

> **회의 유형**: B (로드맵/공급 정합) - 초기 할당은 A(기술 deep-dive)였으나, 전사본 분석 결과 발표형 기술 deep-dive가 아니라 **파이프라인·폼팩터·스케줄·비즈니스 모델**을 조율하는 정합 회의로 재분류
> **학습 가치**: 고객 파이프라인을 프레이밍하는 화법, 의사결정을 유도하는 질문, 공급망 병목을 정중하게 묻고 미루는 화법, 액션 아이템을 명시하는 마무리
> **Audrey 관점**: 이 회의는 "파이프라인 제안 + 공급 병목 협상"의 전형 - 네가 파트너와 로드맵을 맞출 때 직접 써야 할 화법이 밀집해 있다. Type B이므로 Section 4(협상·액션)가 핵심.

---

## 1. 발화 아키텍처 - Jerry의 회의 설계 (5단계)

Jerry(SK 측)가 이 회의를 어떻게 설계했는지. 발표형 회의가 아니라 **정합 회의**이므로, "발표자 아키텍처"가 아니라 "회의 진행 아키텍처"다. 각 단계마다 고정된 화법 공식이 있다.

### 단계 1: 고객 맥락으로 열기 (Customer Context Opening)

Jerry는 "우리 제품"이 아니라 **"고객이 뭘 원하는지"**로 회의를 연다. 파트너(Marvell)를 "leading partner"로 포지셔닝하면서, 동시에 "빨리 결정해야 한다"는 긴장감을 만든다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Multiple customers started to show a strong interest in X as well as Y` | "Multiple customers and they started to show a strong interest in near memory compute as well as DDR5 memory expansion using AIC card" | 고객 수요로 열기 - "우리 제안"이 아니라 "고객 요청" |
| `the whole objective of this meeting was quickly we can get a line on what do we need to do to enable both` | "the whole objective of this meeting was quickly we can get a line on what do we need to do to enable both" | 회의 목적 명시 - "quickly"로 긴장감 |
| `we will be positioning you as a leading partner` | "we will be positioning you as a leading partner" | 파트너 포지셔닝 - 협력 관계 전제 |
| `we can build a stronger pipeline because everyone is looking for these cards as soon as possible` | "we can build a stronger pipeline because everyone is looking for these cards as soon as possible" | 수요 긴급성 - "as soon as possible" |

**Audrey 교훈**: 영어 정합 회의는 "우리가 뭘 원해요"로 시작하지 않는다. **"고객이 이걸 원한다"**로 시작한다. "Multiple customers started to show a strong interest in X" - 이 공식을 외워. 네가 파트너에게 뭔가를 요청할 때, 요청을 "고객 수요"로 포장하면 설득력이 올라간다. 한국어로는 "고객 요청이 왔습니다"인데, 영어는 "started to show a strong interest"로 수요를 능동적으로 묘사한다.

### 단계 2: 결정 유도 질문 (Decision-Forcing Question)

맥락을 깔고 나서, Jerry는 **"어느 쪽으로 갈 것인가"**를 직접 묻는다. 이게 정합 회의의 핵심 화법.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So what kind of thing are they interested in more, so X or Y?` | "So what kind of thing are they interested in more, so NDP or DDR5 expansion only?" | 양자택일 질문 - 결정을 유도 |
| `we should make the or we should decide to which product we will make` | "the customer wanted to have the both type of the products so we should make the or we should decide to which product we will make" | 의사결정 프레이밍 - "we should decide" |
| `Have to make the decision. Go for both or?` | "Have to make the decision. Go for both or?" | 핵심 결정을 직접 제시 |

**Audrey 교훈**: 정합 회의에서는 "어떻게 생각하세요?"로 끝내면 안 된다. **"X or Y?"**로 양자택일을 제시해야 한다. "So what kind of thing are they interested in more, so NDP or DDR5 expansion only?" - 이 "so X or Y" 구조가 결정을 유도한다. 그리고 "Have to make the decision. Go for both or?" - 주어를 생략하고("We have to" 대신 "Have to") 의사결정의 무게감을 만든다.

### 단계 3: 포지셔닝 제안 (Positioning Proposal)

Jerry는 자기 의견을 "I think"로 열고, **"how I would position that"**으로 포지셔닝을 제안한다. 이게 정합 회의에서 의견을 내는 공식이다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So I think we should have two separate cards, one only for X and one only for Y` | "so I think we should have two separate cards, one only for X and one only for A" | 구체적 포지셔닝 - "one only for X, one only for Y" |
| `this is how I would position that` | "and I think this is how I would position that" | 포지셔닝 명시 - "how I would position" |
| `So for the X we already have the Y. So we can provide those samples to customers first` | "So for the NDP processing near memory we already have the evaluation card from the ventures. So we can provide those samples to customers first" | 현황 기반 제안 - "we already have X, so we can Y" |
| `then doing some evaluation with those cards and then we can make a decision for the future` | "doing some evaluation with those cards and then we can make a decision for the future" | 단계적 의사결정 - "evaluation, then decision" |

**Audrey 교훈**: 영어로 의견을 낼 때 "I want X"가 아니라 **"this is how I would position that"**으로 포장해라. "position"은 비즈니스 영어에서 "어떻게 배치하다"의 의미로, 제안을 "의견"이 아니라 "포지셔닝"으로 프레이밍하면 전문적으로 들린다. 그리고 "we already have X, so we can Y" - 이미 가진 것을 기반으로 다음 단계를 제안하는 구조를 외워.

### 단계 4: 비즈니스 모델 설명 (Business Model Walkthrough)

DDR4 재사용(reuse) 비즈니스 모델을 설명할 때, Jerry는 **"the reason why I'm asking is because..."**로 의도를 명시하고, **"we would like to have a plan to sell a total package"**로 목표를 제시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the reason why I'm asking... is because our marketing team is thinking of having a new business model` | "the reason why I'm asking where I'm talking about the DDI for the commission team... because the our marketing team is thinking of having a new business model" | 의도 설명 - "the reason why"로 질문 배경 |
| `we would like to have a plan to sell a total package, including not only X but Y` | "we would like to have a plan to sell a total package, including not only a link card and our order to DDI for ouRDIM" | 패키지 제안 - "total package" |
| `we can make use of those RDIM for release with the adding card and then we can repack it` | "we can make use of those RDIM for release with with the adding card and then we can repack it" | 비즈니스 흐름 설명 - "make use of X, then repack" |

**Audrey 교훈**: 비즈니스 모델을 설명할 때 "the reason why I'm asking is because..."로 시작하면, 상대방이 "왜 이 질문을 하지?"라고 의아해하지 않고 "이 사람은 맥락이 있구나"라고 느낀다. 그리고 "we would like to have a plan to sell a total package" - "plan"과 "total package"라는 단어가 비즈니스적 진지함을 전달한다. 한국어 "토탈 패키지로 팔고 싶다"의 영어 버전이다.

### 단계 5: 마무리와 후속 (Close and Follow-up)

Jerry는 회의 마무리를 **"I think that we have covered today's agenda"**로 선언하고, 후속 채널을 명시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think that we have covered today's agenda. So let's solve them` | "I think that we have covered today's agenda. So let's solve them. I mean, we have an email, I mean, think offline discussion" | 마무리 선언 - "covered today's agenda" |
| `if we have a more, I mean, deep dive for that, I will set up the other meeting` | "if we have a more, I mean, deep dive for that, I will set up the other meeting" | 후속 회의 예고 - "set up the other meeting" |
| `we can sync up again in about a week` | "we can sync up again in about a week" | 후속 일정 - "sync up" |
| `I would like to hear your proposal and then we can discuss more in detail` | "I would like to hear your proposal and then we can discuss more in detail" | 제안 요청 - "hear your proposal" |

**Audrey 교훈**: 회의 마무리는 "Any questions?"가 아니라 **"I think that we have covered today's agenda"**로 선언적으로 끝내야 한다. 그리고 후속을 "we can sync up again in about a week"으로 명시. "sync up"은 비즈니스 영어에서 "다시 만나 정보 맞추자"의 자연스러운 표현이다. "see you next week"보다 전문적이다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 진짜 학습 가치. 양측이 약점(공급 지연, 정보 부족, 결정 미정)을 어떻게 정중하게 포장하는지.

### 전략 1: 솔직한 한계 인정 + 대안 모색 (Honest Limit + Alternative Search)

Crown(Marvell)이 PCB 공급 문제를 묻는 질문에 "우리도 모른다"를 솔직하게 인정하되, "노력은 하겠다"로 마무리.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| PCB 대체 소싱 가능? | "Absolutely. That is the biggest challenge the whole industry is facing and we are facing to venture. **If we have it, we will support it, but we don't know anybody.**" | "그럼요. 그건 산업 전체가 겪는 가장 큰 과제고 우리도 Venture에 겪고 있습니다. **있으면 지원하겠지만, 아는 곳이 없습니다.**" |
| 후속 액션 | "**let us do a little bit of more homework. We'll talk to some of our internal teams, procurement teams and we'll take an action to follow up.**" | "**좀 더 알아보겠습니다. 내부 조달팀과 이야기하고 후속 액션을 잡겠습니다.**" |

**패턴 공식**: `That is the biggest challenge. If we have it, we will support it, but we don't know anybody. Let us do a little bit of more homework. We'll take an action to follow up.`

**Audrey 교훈**: "I don't know"를 단독으로 쓰면 무책임하다. "If we have it, we will support it, but we don't know anybody" - **솔직한 한계 + 의지 표시**. 그리고 "let us do a little bit of more homework" - "homework"는 비즈니스 영어에서 "좀 더 알아보겠다"의 자연스러운 표현이다. "I'll research"보다 겸손하고 전문적. 마지막으로 "we'll take an action to follow up"로 책임을 명시. 이 3단 구조(한계 인정 - 노력 의지 - 액션 명시)를 외워라.

### 전략 2: 정보 보류 + 타임라인 명시 (Info Withholding + Timeline)

Jerry가 tier-2 고객 이름을 밝히지 않으면서, "2주 후에 알려주겠다"로 타임라인을 준다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| tier-2 고객 이름 | "we are also talking to tier two customers. **Unfortunately, I cannot name those customers yet. Give us another two weeks. Then I will give you the name**" | "tier-2 고객들과도 대화 중입니다. **아쉽게도 아직 고객 이름은 밝힐 수 없습니다. 2주만 더 주세요. 그러면 이름을 알려드리겠습니다.**" |

**패턴 공식**: `Unfortunately, I cannot name those customers yet. Give us another two weeks. Then I will give you the name.`

**Audrey 교훈**: 정보를 못 주겠다고 할 때 "I can't tell you"는 너무 직접적이다. **"Unfortunately, I cannot name those yet. Give us another two weeks."** - "Unfortunately"로 정중함을 표시하고, "yet"으로 "지금은 안 되지만 나중에는" 함의. 그리고 구체적 타임라인("two weeks")을 주면, 상대방이 기다려야 할 이유가 생긴다. 한국어 "아직은 내부 검토 중이라..."의 영어 버전이다.

### 전략 3: 결정 보류 - "더 이야기해야 한다" (Decision Deferral)

Jerry가 DDR4 비즈니스 모델의 타겟을 정하지 못한 상태를 "마케팅팀과 더 논의해야 한다"로 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR4 타겟 결정 | "I need to discuss more, I mean, what kind of a form factor we will drive or we will select the one big hyperscaler... or we will pursue the standard camcorder form factor" | "어떤 폼팩터를 갈지, 한 대형 하이퍼스케일러를 잡을지... 표준 CAM CARD 폼팩터를 추구할지 더 논의해야 합니다" |
| 마케팅팀과 | "I need to I mean, I'm more discussed with our marketing" | "마케팅팀과 더 논의해야 합니다" |

**패턴 공식**: `I need to discuss more with our marketing [team] about X.`

**Audrey 교훈**: 결정을 미룰 때 "We will consider"는 흔해빠졌다. **"I need to discuss more with our marketing"** - 구체적으로 "어느 팀과 논의해야 한다"를 밝히면, 미루는 이유가 조직적 절차로 들린다. 한국어 "내부 검토가 필요합니다"의 영어 버전이지만, 영어는 "검토"가 아니라 "discuss"(논의)로 표현한다.

### 전략 4: 시간 요청 + 협력 제안 (Time Request + Collaboration Offer)

Crown이 DDR4 시장 개척을 위해 "시간을 달라"고 하면서, 동시에 "협력하면 좋겠다"고 제안한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR4 시장 | "If you give us a little bit more time, we also working with Penguin to see what they can do to enable that market as well" | "시간을 좀 더 주시면, Penguin과도 작업 중이니 그 시장을 활성화할 수 있는지 보겠습니다" |
| 협력 제안 | "**I'm happy to have the same discussion with you if you want to if you can help to enable that market that would be awesome**" | "**같은 논의를 기꺼이 하겠습니다. 그 시장을 활성화하는 데 도움 주시면 정말 좋겠습니다**" |

**패턴 공식**: `If you give us a little bit more time, we're also working with X. I'm happy to have the same discussion. If you can help, that would be awesome.`

**Audrey 교훈**: 시간을 달라고 할 때 "Please wait"는 절대 쓰지 마라. **"If you give us a little bit more time"** - "if"로 시작해서 요청을 조건문으로 포장. 그리고 "that would be awesome"은 비즈니스 영어에서 "정말 좋겠다"의 자연스러운 표현이다. "awesome"이 구어체처럼 보이지만, 파트너 회의에서 협력을 제안할 때 쓰면 가벼우면서 진지한 느낌을 준다.

### 전략 5: 병목을 산업 문제로 프레이밍 (Industry-Wide Bottleneck)

Crown이 PCB 부족을 "우리만의 문제가 아니라 산업 전체 문제"로 프레이밍해서 책임을 분산.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| PCB 부족 | "That is the biggest challenge **the whole industry is facing** and we are facing to venture" | "그건 **산업 전체가 겪는** 가장 큰 과제고, 우리도 Venture에 겪고 있습니다" |
| SK측도 동의 | "as we were discussing, it's an industry wide channel" | "논의했듯이, 산업 전체 채널 문제입니다" |

**패턴 공식**: `That is the biggest challenge the whole industry is facing.`

**Audrey 교훈**: 공급 지연을 설명할 때 "We can't do it because of X"는 방어적으로 들린다. **"That is the biggest challenge the whole industry is facing"** - "산업 전체 문제"로 프레이밍하면, "우리 탓이 아니다"를 직접 말하지 않으면서 전달. 이게 정중한 책임 분산 화법이다. 한국어 "업계 다 그렇다"의 영어 버전이지만, 영어는 "the whole industry is facing"으로 능동 구조를 쓴다.

### 전략 6: 타임라인 슬립 인정 (Timeline Slip Acknowledgment)

Jerry가 평가 카드 일정이 Q4로 미뤄진 것을 솔직하게 공지하되, "베스트 케이스였다"로 원래 계획이 낙관적이었음을 함의.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 평가 카드 지연 | "we were supposed to approve the secure that PNM evaluation card... I mean, that was supposed to get the next two months. But as the best case... but the occult apparently mean they cannot... get or they don't have available PCB material at this moment" | "평가 카드를 다음 두 달에 확보하기로 했었습니다. 베스트 케이스로는요. 하지만 지금 PCB 재료가 없습니다" |
| 새 타임라인 | "they can provide the evaluation card. It might be a the Q4 over this year. Maybe I mean, end of this year" | "평가 카드를 제공할 수 있을 겁니다. 올해 Q4, 아마 연말쯤" |

**패턴 공식**: `We were supposed to X next two months, but as the best case, they don't have PCB material at this moment. It might be Q4, maybe end of this year.`

**Audrey 교훈**: 일정이 밀렸을 때 "We are delayed"는 약하다. **"We were supposed to X, but as the best case, Y."** - "원래 X하기로 했었습니다(베스트 케이스로는요)"로 원래 계획이 낙관적이었음을 함의. 그리고 새 타임라인은 "It might be Q4"로 "might"로 불확실성을 표시. 한국어 "일정이 좀 밀렸습니다"보다 영어는 "as the best case"로 원래 계획의 성격(낙관적)을 먼저 정의한다.

---

## 3. 정중한 도전 화법 (질문자 패턴)

양측이 서로 기술적/비즈니스적으로 도전하면서도 정중하게 질문하는 패턴. 네가 직접 써야 할 화법이다.

### 질문 유형 1: 양자택일 결정 질문 (Binary Choice Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So what kind of thing are they interested in more, so X or Y?` | "So what kind of thing are they interested in more, so NDP or DDR5 expansion only?" | 양자택일 - 결정을 유도 |
| `The one thing I'd like to clarify is, X or Y, which one is correct?` | "in case of the expansion card, we need to get more the information such as the specification and then the other tier two. They wanted to have just expansion card, right? Or they are they are interested in the NDP solution to which one is correct" | 확인 + 양자택일 - "which one is correct" |

**Audrey 교훈**: 파트너가 모호하게 말할 때, "What do you want?"이 아니라 **"So X or Y?"**로 양자택일을 제시하면, 상대방은 쉽게 대답할 수 있다. 그리고 "which one is correct" - "맞는 건가요?"로 확인하면, 도전이 아니라 정중한 확인이 된다. 이 "so X or Y?" 구조는 정합 회의에서 가장 자주 쓰는 화법이다.

### 질문 유형 2: 비즈니스 타당성 질문 (Viability Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `do you have kind of a minimum, you know, size for this opportunity to be for you to be viable?` | "Jerry, do you have kind of a minimum, you know, size for this opportunity to be for you to be viable?" | 비즈니스 타당성 - "minimum size", "viable" |

**Audrey 교훈**: 파트너의 비즈니스 의향을 확인할 때 "Is this big enough?"는 직접적이다. **"Do you have a minimum size for this opportunity to be viable?"** - "viable"(타당성 있는)이라는 단어가 비즈니스 영어의 핵심. "이 비즈니스가 성립하려면 최소 규모가 얼마나 됩니까?" - 이 질문은 파트너의 진지함을 테스트하면서도 정중하다.

### 질문 유형 3: 확인식 반복 (Confirmatory Recap)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `your suggestion is I mean getting the just expansion card from the penguin solution. Am I right?` | "your suggestion is I mean getting the just expansion card from the penguin solution. Am I right?" | 확인 - "Am I right?"로 정중 확인 |
| `So we have the information Oracle Penguin they want DDR5 now and X to separate using same add in card for functionality.` | "So we have the information Oracle Penguin they want DDR5 now and X to separate using same add in card for functionality" | 요약 - "we have the information"으로 정리 |

**Audrey 교훈**: 상대방의 말을 요약한 뒤 **"Am I right?"**로 확인하면, 두 가지 효과가 있다. (1) 정확히 이해했는지 확인, (2) 상대방에게 "네가 한 말이 이거다"를 공식화. 이게 정합 회의에서 합의를 만드는 화법이다. "we have the information X, Y, Z" - "정보가 이렇다"로 정리하면, 다음 단계(결정)로 넘어갈 수 있다.

### 질문 유형 4: 기술 제약 탐색 (Technical Constraint Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `how many layers of this PCB is required?` | "So how many layers of this PCB is required?" | 기술 제약 - "layers required" |
| `beyond a certain number of layers, it's specialized technology is required, right?` | "they're like beyond a certain number of layers, right? It's specialized technology is required" | 기술 함의 - "specialized technology required" |
| `There's only a handful of PCB suppliers supply that type of PCBs, right?` | "There's only a handful of PCB suppliers supply that type of PCBs, right?" | 공급망 현실 - "handful of suppliers" |

**Audrey 교훈**: Crown(Marvell)이 SK측에 기술 질문을 할 때, **"how many layers?"**로 구체 수치를 물은 뒤, **"beyond a certain number, specialized technology is required, right?"**로 기술 함의를 확인한다. 이 "수치 물음 - 함의 확인 - right?" 구조는 기술 회의에서 가장 효율적인 질문 패턴이다. "right?"를 붙이면, 상대방이 동의하기 쉽고, 회의가 합의 방향으로 흐른다.

### 질문 유형 5: 대안 소싱 탐색 (Alternative Sourcing Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `If you have some other PCB publication source, can you support to the venture?` | "If you have some other PCB publication source, can you support to the venture?" | 대안 요청 - "can you support" |
| `if you're a fabrication company to get PCB material earlier, then you can fill in the schedule` | "if you're a fabrication company to get PCB material earlier, then you can fill in the schedule. That's the biggest challenge" | 대안의 가치 - "fill in the schedule" |

**Audrey 교훈**: 파트너에게 대안을 부탁할 때 "Can you help?"는 약하다. **"If you have some other source, can you support?"** - "지원할 수 있습니까?"로 구체화. 그리고 "fill in the schedule" - "스케줄을 채우다"로 대안의 비즈니스 가치를 명시. 이게 파트너에게 도움을 요청하면서도, 요청의 가치(스케줄 회복)를 전달하는 화법이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

Type B 회의의 핵심. 로드맵, 타임라인, 볼륨, 액션 아이템을 정하는 언어.

### 협상 화법 - 타임라인 타겟

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 시장 진출 속도 | Jerry | "time to market is important. That's why we were suggesting reusing or leveraging the existing design to offer something" | "time to market is important" - 속도 강조 |
| 타임라인 동의 | Crown | "I also agree with you. The time to market will be very important" | "I also agree" - 합의 형성 |
| 평가 카드 타임라인 | Jerry | "they can provide the evaluation card. It might be a the Q4 over this year. Maybe I mean, end of this year" | "It might be Q4, maybe end of this year" - 타임라인 명시 |
| 후속 일정 | Jerry | "we can sync up again in about a week" | "sync up in about a week" - 후속 약속 |
| 2주 타임라인 | Jerry | "Give us another two weeks. Then I will give you the name" | "Give us another two weeks" - 타임라인 요청 |

### 협상 화법 - 볼륨/파이프라인

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 파이프라인 구축 | Jerry | "we can build a stronger pipeline because everyone is looking for these cards as soon as possible" | "build a stronger pipeline" - 비즈니스 제안 |
| 리딩 파트너 포지션 | Jerry | "we will be positioning you as a leading partner" | "positioning you as a leading partner" - 파트너십 |
| 고객 활성화 | Jerry | "we can take the lead enable customers and then ask customers to purchase these from SSSK hynix" | "take the lead enable customers" - 리딩 역할 |
| 패키지 판매 | Jerry | "we would like to have a plan to sell a total package, including not only a link card and our order to DDI for ouRDIM" | "total package" - 패키지 제안 |

### 협상 화법 - 스펙 푸시백/조정

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 폼팩터 동일 | Crown | "they want the same form factor. So we can exact same form factor what we have" | "same form factor what we have" - 스펙 재사용 |
| 다른 폼팩터 필요 | Jerry | "some might have a different flavor like they wanted to have a smaller than in processing your memory processing card full height" | "different flavor" - 스펙 유연성 |
| 다음 세대에서 | Crown | "in our next generation of product we can discuss how to enable more" | "next generation we can discuss" - 미루기 |
| DDR5 8까지 가능 | Crown | "if you go to the PC with DDR5 you can do up to eight. But the challenge is then you need to have a form factor which is not going to be like this form factor" | "you can do up to X. But the challenge is Y" - 스펙 푸시백 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 액션 명시 | Crown | "we'll take an action to follow up" | "take an action to follow up" - 액션 아이템 |
| 후속 회의 | Jerry | "if we have a more, I mean, deep dive for that, I will set up the other meeting" | "set up the other meeting" - 후속 약속 |
| 이메일 후속 | Jerry | "we have an email, I mean, think offline discussion" | "email, offline discussion" - 후속 채널 |
| 제안 요청 | Jerry | "I would like to hear your proposal and then we can discuss more in detail" | "hear your proposal" - 제안 대기 |
| 내부 논의 | Jerry | "I will also have some discussion with our marketing team" | "discussion with our marketing team" - 내부 액션 |
| 더 알아보기 | Crown | "let us do a little bit of more homework" | "do a little bit of more homework" - 후속 액션 (겸손) |
| 업데이트 약속 | Jerry | "I can have more information and I will update you" | "I will update you" - 정보 갱신 약속 |

**Audrey 교훈** (Type B 핵심):
- **"time to market is important"** - 이 한 문장이 정합 회의의 기조다. 모든 스펙/스케줄 결정의 전제. 회의에서 속도를 강조할 때 반드시 써라.
- **"we can sync up again in about a week"** - "sync up"은 비즈니스 영어 필수 표현. "meet again"보다 가볍고 전문적. 후속 일정을 잡을 때 써라.
- **"we'll take an action to follow up"** - "action"을 명시. 회의에서 "I'll check"는 약하고, "I'll think about it"은 미루는 것. "take an action"은 책임을 지는 공식 표현.
- **"positioning you as a leading partner"** - 파트너십을 제안할 때 "you're our partner"가 아니라 "positioning you as X"로 포장하면, 공식적이고 진지하게 들린다.
- **"we would like to have a plan to sell a total package"** - 비즈니스 제안을 "plan"과 "total package"로 포장하면, 단순한 요청이 아니라 비즈니스 전략으로 들린다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 DDR5/NDP/AIC/PCB 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **NDP** (Near Memory Processing/Compute) | 근메모리 연산 - 메모리 근처에서 데이터 처리 | "the NDP, your NDP solution, I mean they have both functionality, the expansion and the near memory processing" - NDP = 확장 + 근메모리 연산 통합 |
| **AIC card** (Add-In Card) | PCIe 추가 카드 폼팩터 | "DDR5 memory expansion using AIC card" - DDR5 확장용 AIC |
| **Structera X** | Marvell의 DDR5 확장/NDP 칩 | "using your Structera X because some might have a different flavor" - 제품명 |
| **form factor** | 하드웨어 물리 규격 | "What kind of form factor the customer wanted to have" - "form factor wanted to have" |
| **full height, three quarter length** | PCIe 카드 크기 규격 | "we are make it to base based on the the full height the three quarter length" - 카드 규격 |
| **DDR5 expansion** | DDR5 메모리 용량 확장 | "near memory compute as well as DDR5 memory expansion" - "X as well as Y" |
| **evaluation card** | 평가용 보드 (엔지니어링 샘플) | "we already have the evaluation card from the ventures" - "evaluation card from X" |
| **PCB** (Printed Circuit Board) | 인쇄 회로 기판 | "securing over the PCB material will take more time" - "PCB material" |
| **PCB layers** | PCB 레이어 수 (여기선 18) | "how many layers of this PCB is required? It's not exactly, but almost 18, 18 layers" - "layers of PCB" |
| **RDIM** (Registered DIMM) | 서버용 등록 메모리 모듈 | "we can land our memory, we can do this update the memory RDIM to the our end user" - "memory RDIM" |
| **DDI for ouRDIM** | DDR4 RDIMM (재사용 대상) | "reuse of the DDI for ouRDIM with your instructor acts adding cards" - DDR4 재사용 |
| **companion IC** | 동봉/동반 칩 (PCB에 탑재) | "getting the other component companion IC, there will not be a problem" - "companion IC" |
| **tape out** | 칩 설계 완료 (이 회의엔 미등장) | - | - |
| **memory release business** | 메모리 리스(임대) 비즈니스 | "we are also thinking of some kind of a memory release business at this moment" - "memory release business" |
| **decommission team** | 폐기/해제 담당 (여기선 DDR4 퇴역) | "DDI for reuse and decommission to the team" - "decommission to the team" |
| **memory pool** | 메모리 풀링 (CXL) | "we also have some memory pool, the POC and some kind of activity for the memory pool" - "memory pool POC" |
| **POC** (Proof of Concept) | 개념 증명 | "some memory pool, the POC and some kind of activity" - "POC" |
| **hyperscaler** | 대형 클라우드 사업자 | "the most end user and hyperscalar wanting to have their customized adding card" - "customized adding card" |
| **tier two customers** | 2티어 고객 | "we are also talking to tier two customers. Unfortunately, I cannot name those customers yet" - "tier two" |
| **pipeline** | 영업 파이프라인 | "we can build a stronger pipeline because everyone is looking for these cards" - "build a stronger pipeline" |
| **Venture** | (아마 Venture Capital / 벤더) | "we can work with Venture to make sure they start to support" - "work with Venture" |
| **Penguin** | Penguin Solutions (고객/파트너) | "few customers like Oracle and Penguin Solutions are the two" - 고객명 |
| **FMS** (Flash Memory Summit) | 플래시 메모리 서밋 | "what they saw the announcement at FMS, they said the good part you guys are bringing is add-in card" - "announcement at FMS" |
| **PCB fabrication** | PCB 제조/가공 | "if you're a fabrication company to get PCB material earlier, then you can fill in the schedule" - "fabrication company" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 45개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 회의 설계 (Meeting Architecture) ──
- id: m03-001
  expression: "Multiple customers started to show a strong interest in X as well as Y"
  category: context_opening
  function: customer_demand_framing
  speaker_role: sk_side
  difficulty: 4
  context: "Multiple customers and they started to show a strong interest in near memory compute as well as DDR5 memory expansion using AIC card"
  note: 회의를 "고객 수요"로 여는 화법. "우리 제안"이 아니라 "고객 요청"으로 시작

- id: m03-002
  expression: "the whole objective of this meeting was quickly we can get a line on what do we need to do to enable both"
  category: meeting_objective
  function: purpose_stating
  speaker_role: sk_side
  difficulty: 4
  context: "the whole objective of this meeting was quickly we can get a line on what do we need to do to enable both"
  note: "quickly we can get a line on" - 회의 목적 명시 + 긴장감

- id: m03-003
  expression: "we will be positioning you as a leading partner"
  category: partnership
  function: partner_positioning
  speaker_role: sk_side
  difficulty: 4
  context: "we will be positioning you as a leading partner. They can reach out to you to get those information from you"
  note: "positioning you as X" - 파트너십 공식 표현

- id: m03-004
  expression: "we can build a stronger pipeline because everyone is looking for these cards as soon as possible"
  category: pipeline_building
  function: urgency_stating
  speaker_role: sk_side
  difficulty: 3
  context: "we can build a stronger pipeline because everyone is looking for these cards as soon as possible"
  note: "build a stronger pipeline" + "as soon as possible" - 수요 긴급성

- id: m03-005
  expression: "So what kind of thing are they interested in more, so X or Y?"
  category: binary_probe
  function: decision_forcing_question
  speaker_role: sk_side
  difficulty: 4
  context: "So what kind of thing are they interested in more, so NDP or DDR5 expansion only?"
  note: 양자택일 질문 - 결정을 유도하는 핵심 화법

- id: m03-006
  expression: "we should decide to which product we will make"
  category: decision_framing
  function: choice_stating
  speaker_role: sk_side
  difficulty: 3
  context: "the customer wanted to have the both type of the products so we should make the or we should decide to which product we will make"

- id: m03-007
  expression: "Have to make the decision. Go for both or?"
  category: decision_direct
  function: core_choice
  speaker_role: sk_side
  difficulty: 3
  context: "Have to make the decision. Go for both or?"
  note: 주어 생략 - 의사결정 무게감

- id: m03-008
  expression: "So I think we should have two separate cards, one only for X and one only for Y"
  category: positioning_proposal
  function: specific_recommendation
  speaker_role: sk_side
  difficulty: 4
  context: "so I think we should have two separate cards, one only for X and one only for A"
  note: "one only for X, one only for Y" - 구체적 포지셔닝

- id: m03-009
  expression: "this is how I would position that"
  category: positioning
  function: positioning_stating
  speaker_role: sk_side
  difficulty: 4
  context: "and I think this is how I would position that"
  note: "how I would position" - 의견을 "포지셔닝"으로 프레이밍

- id: m03-010
  expression: "for the X we already have the Y. So we can provide those samples to customers first"
  category: status_based_proposal
  function: existing_asset_leveraging
  speaker_role: sk_side
  difficulty: 4
  context: "So for the NDP processing near memory we already have the evaluation card from the ventures. So we can provide those samples to customers first"
  note: "we already have X, so we can Y" - 현황 기반 제안

- id: m03-011
  expression: "then doing some evaluation with those cards and then we can make a decision for the future"
  category: phased_decision
  function: stepwise_approach
  speaker_role: sk_side
  difficulty: 3
  context: "doing some evaluation with those cards and then we can make a decision for the future"
  note: "evaluation, then decision" - 단계적 의사결정

- id: m03-012
  expression: "I think that we have covered today's agenda. So let's solve them"
  category: meeting_close
  function: agenda_completion
  speaker_role: sk_side
  difficulty: 3
  context: "I think that we have covered today's agenda. So let's solve them. I mean, we have an email, I mean, think offline discussion"
  note: "covered today's agenda" - 마무리 선언

- id: m03-013
  expression: "if we have a more deep dive for that, I will set up the other meeting"
  category: follow_up_meeting
  function: future_session
  speaker_role: sk_side
  difficulty: 3
  context: "if we have a more, I mean, deep dive for that, I will set up the other meeting"
  note: "set up the other meeting" - 후속 회의 예고

# ── 회피·포장 (Hedging & Deflection) ──
- id: m03-014
  expression: "Unfortunately, I cannot name those customers yet. Give us another two weeks. Then I will give you the name"
  category: info_withholding
  function: polite_deferral_with_timeline
  speaker_role: sk_side
  difficulty: 5
  context: "we are also talking to tier two customers. Unfortunately, I cannot name those customers yet. Give us another two weeks. Then I will give you the name"
  note: "Unfortunately + yet + timeline" - 정보 보류의 정중 화법

- id: m03-015
  expression: "If we have it, we will support it, but we don't know anybody"
  category: honest_limitation
  function: honest_no_with_willingness
  speaker_role: marvell_side
  difficulty: 5
  context: "If we have it, we will support it, but we don't know anybody"
  note: 솔직한 한계 + 의지 표시 - "I don't know" 대신 쓸 화법

- id: m03-016
  expression: "let us do a little bit of more homework"
  category: defer_with_effort
  function: humble_promise
  speaker_role: marvell_side
  difficulty: 4
  context: "let us do a little bit of more homework. We'll talk to some of our internal teams, procurement teams"
  note: "homework" - "좀 더 알아보겠다"의 자연스러운 비즈니스 표현

- id: m03-017
  expression: "we'll take an action to follow up"
  category: action_item
  function: commitment_formal
  speaker_role: marvell_side
  difficulty: 4
  context: "we'll talk to some of our internal teams, procurement teams and we'll take an action to follow up"
  note: "take an action to follow up" - 책임 명시

- id: m03-018
  expression: "I need to discuss more with our marketing"
  category: internal_deferral
  function: team_based_delay
  speaker_role: sk_side
  difficulty: 3
  context: "I need to I mean, I'm more discussed with our marketing"
  note: 구체적 팀 명시 - 미루는 이유를 조직 절차로

- id: m03-019
  expression: "If you give us a little bit more time, we're also working with X"
  category: time_request
  function: conditional_delay
  speaker_role: marvell_side
  difficulty: 4
  context: "If you give us a little bit more time, we also working with Penguin to see what they can do to enable that market as well"
  note: "if"로 시작 - 요청을 조건문으로 포장

- id: m03-020
  expression: "I'm happy to have the same discussion with you. If you can help, that would be awesome"
  category: collaboration_offer
  function: willing_engagement
  speaker_role: marvell_side
  difficulty: 4
  context: "I'm happy to have the same discussion with you if you want to if you can help to enable that market that would be awesome"
  note: "that would be awesome" - 협력 제안의 자연스러운 표현

- id: m03-021
  expression: "That is the biggest challenge the whole industry is facing"
  category: industry_framing
  function: blame_diffusion
  speaker_role: marvell_side
  difficulty: 5
  context: "That is the biggest challenge the whole industry is facing and we are facing to venture"
  note: "whole industry is facing" - 책임 분산 화법

- id: m03-022
  expression: "We were supposed to X, but as the best case, Y"
  category: timeline_slip
  function: optimistic_plan_acknowledgment
  speaker_role: sk_side
  difficulty: 4
  context: "we were supposed to approve the secure that PNM evaluation card... that was supposed to get the next two months. But as the best case"
  note: "as the best case" - 원래 계획이 낙관적이었음을 함의

- id: m03-023
  expression: "It might be Q4, maybe end of this year"
  category: uncertain_timeline
  function: tentative_schedule
  speaker_role: sk_side
  difficulty: 3
  context: "they can provide the evaluation card. It might be a the Q4 over this year. Maybe I mean, end of this year"
  note: "might + maybe" - 불확실성 이중 표시

- id: m03-024
  expression: "so far, X what we have seen mostly comes from they want to build their own form factor not a IC"
  category: market_insight
  function: observation_stating
  speaker_role: marvell_side
  difficulty: 4
  context: "so far, DDI for what we have seen mostly comes from they want to build their own form factor not a IC"
  note: "so far, what we have seen" - 관찰 기반 발화

- id: m03-025
  expression: "I think that they don't have a specific the volume size of that"
  category: volume_hedging
  function: imprecision_acknowledgment
  speaker_role: sk_side
  difficulty: 3
  context: "I think that they don't have a specific the volume size of that"
  note: 볼륨 부정확성 인정

# ── 정중한 도전 (Polite Challenge) ──
- id: m03-026
  expression: "do you have kind of a minimum, you know, size for this opportunity to be for you to be viable?"
  category: viability_probe
  function: business_seriousness_test
  speaker_role: marvell_side
  difficulty: 5
  context: "Jerry, do you have kind of a minimum, you know, size for this opportunity to be for you to be viable?"
  note: "viable" - 비즈니스 타당성 핵심 단어

- id: m03-027
  expression: "your suggestion is X. Am I right?"
  category: confirmatory_recap
  function: polite_confirmation
  speaker_role: sk_side
  difficulty: 3
  context: "your suggestion is I mean getting the just expansion card from the penguin solution. Am I right?"
  note: "Am I right?" - 정중한 확인

- id: m03-028
  expression: "they wanted to have just X, right? Or they are interested in Y. which one is correct?"
  category: binary_confirmation
  function: either_or_check
  speaker_role: sk_side
  difficulty: 4
  context: "They wanted to have just expansion card, right? Or they are they are interested in the NDP solution to which one is correct"

- id: m03-029
  expression: "how many layers of this PCB is required?"
  category: technical_probe
  function: spec_question
  speaker_role: marvell_side
  difficulty: 3
  context: "So how many layers of this PCB is required?"

- id: m03-030
  expression: "beyond a certain number of layers, it's specialized technology is required, right?"
  category: implication_check
  function: technical_consequence
  speaker_role: marvell_side
  difficulty: 4
  context: "they're like beyond a certain number of layers, right? It's specialized technology is required"
  note: "right?" - 기술 함의 확인

- id: m03-031
  expression: "There's only a handful of PCB suppliers supply that type of PCBs, right?"
  category: supply_reality
  function: market_structure_check
  speaker_role: marvell_side
  difficulty: 4
  context: "There's only a handful of PCB suppliers supply that type of PCBs, right?"

- id: m03-032
  expression: "If you have some other PCB source, can you support to the venture?"
  category: alternative_request
  function: help_solicitation
  speaker_role: sk_side
  difficulty: 4
  context: "If you have some other PCB publication source, can you support to the venture?"
  note: "can you support" - 대안 소싱 요청

- id: m03-033
  expression: "What kind of form factor the customer wanted to have"
  category: spec_probe
  function: requirement_inquiry
  speaker_role: sk_side
  difficulty: 3
  context: "What kind of form factor the customer wanted to have for just expansion card, standard cam card"

- id: m03-034
  expression: "do you have any other data from the X?"
  category: info_request
  function: data_inquiry
  speaker_role: sk_side
  difficulty: 2
  context: "do you have any other data from the, Sorry?"

- id: m03-035
  expression: "Is that okay?"
  category: agreement_check
  function: consent_check
  speaker_role: sk_side
  difficulty: 2
  context: "I would like to hear your proposal and then we can discuss more in detail. Is that okay?"

# ── 협상·액션 (Negotiation & Action) ──
- id: m03-036
  expression: "time to market is important. That's why we were suggesting reusing or leveraging the existing design"
  category: speed_strategy
  function: rationale_for_reuse
  speaker_role: sk_side
  difficulty: 4
  context: "time to market is important. That's why we were suggesting reusing or leveraging the existing, you know, design to offer something"
  note: "time to market is important" - Type B 회의 기조 문장

- id: m03-037
  expression: "I also agree with you. The time to market will be very important"
  category: agreement_stating
  function: consensus_building
  speaker_role: marvell_side
  difficulty: 3
  context: "I also agree with you. The time to market will be very important"

- id: m03-038
  expression: "we can sync up again in about a week"
  category: follow_up_schedule
  function: next_sync
  speaker_role: sk_side
  difficulty: 3
  context: "we can sync up in we can sync up again in about a week"
  note: "sync up" - 비즈니스 영어 필수 표현

- id: m03-039
  expression: "I would like to hear your proposal and then we can discuss more in detail"
  category: proposal_request
  function: ask_for_plan
  speaker_role: sk_side
  difficulty: 4
  context: "I would like to hear your proposal and then we can discuss more in detail"

- id: m03-040
  expression: "we would like to have a plan to sell a total package, including not only X but Y"
  category: package_proposal
  function: bundle_business
  speaker_role: sk_side
  difficulty: 4
  context: "we would like to have a plan to sell a total package, including not only a link card and our order to DDI for ouRDIM"
  note: "total package" - 비즈니스 진지함

- id: m03-041
  expression: "we can take the lead enable customers and then ask customers to purchase these from SSSK hynix"
  category: leadership_claim
  function: role_stating
  speaker_role: sk_side
  difficulty: 4
  context: "we can take the lead enable customers and then ask customers to purchase these from SSSK hynix"

- id: m03-042
  expression: "the whole idea is what do we need to do to enable more customers"
  category: objective_framing
  function: goal_stating
  speaker_role: marvell_side
  difficulty: 4
  context: "the whole idea is what do we need? What do we need to do to enable more customers in that case"

- id: m03-043
  expression: "you can do up to X. But the challenge is Y"
  category: spec_pushback
  function: capability_vs_constraint
  speaker_role: marvell_side
  difficulty: 4
  context: "if you go to the PC with DDR5 you can do up to eight. But the challenge is then you need to have a form factor which is not going to be like this form factor"
  note: "you can do up to X. But the challenge is Y" - 스펙 푸시백 공식

- id: m03-044
  expression: "in our next generation of product we can discuss how to enable more"
  category: next_gen_deferral
  function: future_promise
  speaker_role: marvell_side
  difficulty: 4
  context: "the question becomes in our next generation of product we can discuss how to enable more games probably have a smaller package"

- id: m03-045
  expression: "I can have more information and I will update you"
  category: update_commitment
  function: info_refresh_promise
  speaker_role: sk_side
  difficulty: 3
  context: "same time I can get more wins and I can same time I can have more information and I will update you"

# ── 비즈니스 모델 설명 (Business Model) ──
- id: m03-046
  expression: "the reason why I'm asking is because our marketing team is thinking of having a new business model"
  category: rationale_stating
  function: question_background
  speaker_role: sk_side
  difficulty: 4
  context: "the reason why I'm asking where I'm talking about the DDI for the commission team... because the our marketing team is thinking of having a new business model"
  note: "the reason why I'm asking is because" - 질문 배경 설명

- id: m03-047
  expression: "we can make use of those RDIM for release and then we can repack it"
  category: business_flow
  function: process_description
  speaker_role: sk_side
  difficulty: 4
  context: "we can make use of those RDIM for release with with the adding card and then we can repack it"
  note: "make use of X, then repack" - 비즈니스 흐름

- id: m03-048
  expression: "we can sell another package where we can find the another opportunity"
  category: opportunity_expansion
  function: lifecycle_extension
  speaker_role: sk_side
  difficulty: 4
  context: "we can sell another package where we can find the another the opportunity for the next business, such as the expand expand the the life cycle of the DDI five"

- id: m03-049
  expression: "we are also thinking of some kind of a memory release business at this moment"
  category: business_exploration
  function: tentative_plan
  speaker_role: sk_side
  difficulty: 3
  context: "But we are also thinking of some kind of a memory release business at this moment"
  note: "some kind of" - 비즈니스 탐색의 겸손 표현

- id: m03-050
  expression: "the most end user and hyperscaler wanting to have their customized adding card form factor"
  category: market_observation
  function: customer_preference
  speaker_role: sk_side
  difficulty: 3
  context: "the most end user and hyperscalar wanting to have their customized adding card from factor"

# ── 담화 표지 (Discourse Markers) ──
- id: m03-051
  expression: "from that perspective if you look at it, what they are looking for"
  category: perspective_framing
  function: viewpoint_shift
  speaker_role: sk_side
  difficulty: 3
  context: "So from that perspective if you look at it, what they are looking for, I mean near memory compute as well"

- id: m03-052
  expression: "Just put it in that perspective"
  category: framing_close
  function: viewpoint_summary
  speaker_role: sk_side
  difficulty: 3
  context: "Just put it in that perspective"

- id: m03-053
  expression: "Okay, I see. So I think that we need to more time to digest or to get there"
  category: processing_delay
  function: absorption_acknowledgment
  speaker_role: sk_side
  difficulty: 3
  context: "Okay, okay, I see. So I think that we need to more time to digest or to get there"
  note: "time to digest" - 처리 시간 요청

- id: m03-054
  expression: "we have an email, I mean, think offline discussion"
  category: follow_up_channel
  function: offline_continuation
  speaker_role: sk_side
  difficulty: 2
  context: "we have an email, I mean, think offline discussion"

- id: m03-055
  expression: "we can come up with the plan and we can take the lead to enable this"
  category: commitment_plan
  function: proactive_offer
  speaker_role: sk_side
  difficulty: 4
  context: "we can come up with the plan and we can take the lead to enable this"
  note: "come up with the plan" + "take the lead" - 적극적 제안
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-08-18 09 01 10_EN_Marvell-extracted.wav` (총 ~30분, 3,087단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-7) | 고객 수요 프레이밍 + 회의 목적 + "positioning as leading partner" | 정합 회의 개시 화법 | ★★★ |
| 2 | 결정 질문 (line 9-24) | "what kind of thing are they interested in more, X or Y?" + "two separate cards" 포지셔닝 | 양자택일 질문 + 포지셔닝 제안 | ★★★★ |
| 3 | 정보 보류 (line 83-90) | "I cannot name those customers yet. Give us another two weeks" + "sync up again in about a week" | 정보 보류 + 타임라인 + 후속 일정 | ★★★★ |
| 4 | PCB 병목 (line 167-194) | "If we have it, we will support it, but we don't know anybody" + "let us do a little bit of more homework" + "take an action to follow up" | 솔직한 한계 + 노력 의지 + 액션 명시 | ★★★★★ |
| 5 | 비즈니스 모델 (line 110-135) | "the reason why I'm asking is because..." + "we would like to have a plan to sell a total package" + "viable" 타당성 질문 | 비즈니스 모델 설명 + 타당성 프로브 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4가 가장 가치 높음 - 회피·액션 화법이 밀집. 발췌 2, 5도 Type B 회의의 핵심 패턴 포함

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap alignment + supply negotiation** register다. 발표형 회의가 아니라, 양측이 파이프라인·스케줄·비즈니스 모델을 조율하는 구조. Type B이므로 두 역할 모두 학습해야:
- **SK 측 역할 (Jerry)**: 고객 수요 프레이밍, 결정 유도 질문, 비즈니스 모델 설명, 후속 약속 - 네가 파트너와 로드맵을 맞출 때
- **Marvell 측 역할 (Crown)**: 솔직한 한계 인정, 시간 요청, 협력 제안, 기술 제약 탐색 - 네가 파트너의 입장을 이해하고 질문할 때

### Pragmatics (화용론) 핵심
1. **"the whole industry is facing"**: 공급 지연을 "산업 전체 문제"로 프레이밍. "우리 탓이 아니다"를 직접 말하지 않으면서 책임 분산. 한국어 "업계 다 그렇다"의 영어 버전이지만, 영어는 "the whole industry is facing"으로 능동 구조.
2. **"If we have it, we will support it, but we don't know anybody"**: 솔직한 한계 + 의지. "I don't know"를 단독 쓰지 말고, 의지를 붙여라. 그리고 "let us do a little bit of more homework"로 후속을 약속.
3. **"Unfortunately, I cannot name those yet"**: 정보 보류 시 "yet"이 핵심. "지금은 안 되지만 나중에는" 함의. 그리고 구체적 타임라인("two weeks")을 주면, 상대방이 기다려야 할 이유가 생긴다.
4. **"time to market is important"**: Type B 회의의 기조 문장. 모든 스펙/스케줄 결정의 전제. 속도를 강조할 때 이 한 문장을 먼저 깔아라.
5. **"sync up again in about a week"**: "meet again"보다 가볍고 전문적. 비즈니스 영어에서 후속 일정을 잡을 때 "sync up"을 써라.

### 네가 당장 써야 할 Top 5
1. **"time to market is important"** - Type B 회의 기조 문장. 회의 첫 5분에 깔아라.
2. **"If we have it, we will support it, but we don't know anybody"** - 솔직한 한계 + 의지. 공급/지원 문제에 직면했을 때.
3. **"we can sync up again in about a week"** - 후속 일정 명시. "see you next week" 대신 써라.
4. **"we'll take an action to follow up"** - 액션 아이템 명시. "I'll check" 대신.
5. **"Unfortunately, I cannot name those yet. Give us another two weeks."** - 정보 보류 + 타임라인. 고객명/내부 정보를 못 줄 때.

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "고객 요청이 왔습니다" | "Multiple customers started to show a strong interest in X" | 한국어는 정적, 영어는 "started to show"로 동적 |
| "업계 다 그렇다" | "That is the biggest challenge the whole industry is facing" | 영어는 능동 구조 "is facing" |
| "좀 더 알아보겠다" | "let us do a little bit of more homework" | 영어는 "homework"로 겸손+전문 |
| "2주 후에 알려드리겠다" | "Unfortunately, I cannot name those yet. Give us another two weeks." | "Unfortunately + yet"으로 정중함 |
| "내부 검토가 필요합니다" | "I need to discuss more with our marketing" | 영어는 구체 팀 명시 |
| "시장 진출 속도가 중요합니다" | "time to market is important" | 거의 직역 - 비즈니스 영어 고정 표현 |
| "다음에 다시 만나시죠" | "we can sync up again in about a week" | "sync up"이 비즈니스 영어 자연 표현 |
| "둘 다 할까요?" | "Have to make the decision. Go for both or?" | 영어는 주어 생략 - 무게감 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 55개 표현 중, 8절 Top 5부터 우선 숙지
3. **Type B 특화**: 4절(협상·액션)을 가장 집중적으로 학습. 로드맵/공급 정합 회의에서 직접 쓸 화법이 밀집
4. **Audrey 금요일 교정**: 2절(회피·포장)과 4절(협상)을 중심으로 dump 작성
5. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
6. **역할 학습**: 네가 SK 측(Jerry) 역할을 주로 학습하되, Marvell 측(Crown) 회피 화법도 파트너 입장 이해를 위해 숙지

---

*Textbook 03 - Marvell DDR5 Expansion + NDP (2026-08-18). 회의 유형 B (로드맵/공급 정합) - 초기 A에서 재분류. 표현 DB 55개. 5개 발췌 구간. 작성: 2026-09-01.*
