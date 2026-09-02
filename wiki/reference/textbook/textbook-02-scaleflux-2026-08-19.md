---
textbook_id: 02
meeting: Scaleflux
date: 2026-08-19
type: B (로드맵/공급 맞춤) - 재분류 (초기 A에서 B로 변경)
partner: Scaleflux (Scaleflux BD lead, Young)
sk_side: SK Hynix (Jerry, Sayada, Matthew, memory system research group)
duration_words: 4423
audio: repo/webex-audio/2026-08-19 09 08 05_EN_Scaleflux-extracted.wav
transcript: repo/webex-audio/2026-08-19 09 08 05_EN_Scaleflux-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, scaleflux, cxl, controller, roadmap, negotiation, nre, mou, supply-alignment, pooling, compression]
---

# Textbook 02 - Scaleflux (2026-08-19)

> **회의 유형**: B (로드맵/공급 맞춤) - 초기 할당은 A(기술 Deep-dive)였으나 본문 분석 결과 재분류
> **재분류 사유**: 기술 내용보다 로드맵/샘플 타임라인, NRE/MOU 비용 분담, exclusive feature 협상, RFQ 요구, 프로젝트 우선순위 조정이 대두. Section 4(협상)가 핵심 학습 가치.
> **학습 가치**: 파트너가 로드맵을 발표하고, SK 측이 샘플 타임라인·스펙·비용 분담을 협상하는 전형적 공급 맞춤 회화
> **Audrey 관점**: 이 회의는 "로드맵 pitch + 조건부 협상"의 전형. 발표자가 NRE·MOU·exclusive를 정중하게 밀고, SK 측이 정중하게 요구사항을 표현하는 구조. 둘 다 배워야.

---

## 1. 발화 아키텍처 - Scaleflux 발표자의 로드맵 설계 (7단계)

Scaleflux 발표자는 로드맵을 7단계 구조로 설계한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "로드맵 설명의 뼈대"다.

### 단계 1: 샘플 타임라인 앵커 (Sample Timeline Anchor)

발표자는 회의 첫 문장부터 샘플 시점을 고정한다. 제품 설명보다 타임라인이 먼저.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Samples will be given in the first phase one by four or sometime in Q4` | "Samples will be given in the first phase one by four or sometime in Q4 and we'll be very happy to provide a couple of samples to SK hynix if they are interested" | 타임라인 앵커 + 의향 탐색 |
| `we'll be very happy to provide a couple of samples to X if they are interested` | (동일) | "happy to" + "if interested" - 조건부 제안 |

**Audrey 교훈**: 로드맵 회의는 "제품이 좋다"로 시작하지 않는다. **"샘플이 Q4에 나온다"**로 시작한다. 그리고 "if interested"를 붙여 의향을 탐색한다. "we'll be happy to provide samples if interested" - 이 공식을 외워. 샘플 제공은 항상 조건부로 포장한다.

### 단계 2: 특정 고객 맞춤 프레이밍 (Custom-Customer Framing)

제품이 특정 hyperscaler 맞춤임을 먼저 밝히고, 범용성을 제한한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `this was designed for a very specific use case for a very specific hyperscalers` | "But this was designed for a very specific use case for a very specific hyperscalers" | "very specific" 반복 - 기대치 관리 |
| `this is designed for the database use case` | "So this is designed for the database use case. And probably you guys all know who is the hyperscaler" | 용도 한정 + 고객 암시 |

**Audrey 교훈**: "very specific"를 두 번 쓰면, "이 제품은 너를 위해 만든 게 아니다"를 정중하게 전달한다. 한국어 "특정 고객 맞춤입니다"보다 훨씬 강한 제한 신호. 그러나 "if interested, we can do quickly"로 다시 열어둔다. 닫고 여는 리듬을 배워라.

### 단계 3: 프로젝트 상태 공식화 (Project Status Formula)

각 프로젝트의 진척도를 퍼센트와 동사로 고정한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the compression one is almost 95% locked and loaded` | "the compression one is almost 95% locked and loaded" | "locked and loaded" - 확정 상태 표현 |
| `we have already kicked off that project` | "We will, we have already kicked off that project" | "kicked off" - 진행 중 표시 |
| `the pooling project specs will be finalized` | "we believe that by Q1 timeframe, the pooling project specs will be finalized" | "will be finalized by Q1" - 미래 확정 |
| `this project is not on the roadmap today because we don't have any customer asking for this project` | (동일) | 부정을 솔직히 - 로드맵 미포함 사유 |

**Audrey 교훈**: "locked and loaded"는 군사 용어에서 온 비즈니스 표현이다 - "완전 준비됐다, 확정됐다". "95% locked and loaded"는 "거의 확정"을 강하게 표현. "kicked off"는 프로젝트 시작의 표준 동사. 이 세 동사(locked and loaded / kicked off / will be finalized)로 프로젝트 상태를 단계별로 표현한다.

### 단계 4: 요구사항-우선 스탠스 (Requirements-First Stance)

발표자는 가장 중요한 협상 화법으로 "네 스펙을 먼저 내놔라"를 반복한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `if we know what is your requirement, what is your RFQ, then we can be helpful to you` | "if we know what is your requirement, what is your RFQ, then we can be helpful to you" | 조건부 도움 - RFQ 전제 |
| `if we don't know it, then we don't know what really we can help you with` | "If we don't know it, then we don't know what really we can help you with" | 부정으로 압박 |
| `if you have finalized your RFQ, you have finalized your specs, then it's much easier for me and my team to respond to that` | (동일) | "much easier" - 협력 유도 |
| `it will be very, very helpful if you give us your specs` | "it will be very, very helpful if you give us your specs. Then I can be helpful and respond very quickly" | "very, very" 반복 - 간절함 |

**Audrey 교훈**: 이게 이 회의의 핵심 협상 화법이다. 발표자는 "we can help you"를 반복하되, 매번 "if you give us your RFQ/specs"라는 조건을 붙인다. 도움을 조건으로 포장하는 화법. 한국어 "스펙 주시면 검토하겠습니다"와 비슷하지만, 영어는 "we can be helpful **if** you give us your RFQ"로 조건을 앞에 둔다. 네가 파트너에게 뭘 요구할 때, "if you give us X, we can be helpful"로 포장해라.

### 단계 5: NRE와 비용 분담 프레이밍 (NRE & Cost-Sharing Framing)

비용을 요구하되, "분담"으로 포장해서 부담을 줄인다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `both of these projects will require NRE and we are going to get NRE from these hyperscalers` | "both of these projects will require NRE and we are going to get NRE from these hyperscalers" | NRE 요구 + 타 고객 사례 |
| `we are willing to put some cost ourselves` | "we are willing to put, you know, good portion of that cost ourselves" | "willing to put" - 분담 의지 |
| `we don't ask SK hynix to put all the cost` | "we don't ask, we don't expect, we don't need all the cost related to this one" | 삼중 부정 - 부담 완화 |
| `let's share some cost for each other` | "let's share some cost for each other" | "share the burden" - 분담 제안 |
| `that will require MOU` | "And that will require MOU" | MOU - 형식적 약정 요구 |

**Audrey 교훈**: NRE(Non-Recurring Engineering) 비용을 요구할 때 "we need X"가 아니라 "we are willing to put some cost ourselves"로 시작한다. "우리도 돈 넣겠다"를 먼저 말하면, 상대방이 거절하기 어렵다. 그리고 "we don't ask, we don't expect, we don't need all the cost" - 삼중 부정으로 부담을 세 번 줄인다. 한국어 "비용 분담하죠"의 영어 버전이 "let's share some cost for each other"다.

### 단계 6: Exclusivity 공개 (Exclusivity Disclosure)

경쟁 고객의 exclusive feature를 솔직하게 공개하고, 조건부 공유를 제안한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `it is very likely that it is going to be a custom SOC for them` | "It is very likely that it is going to be a custom SOC for them because we are asking them for a lot of NRE to do the project without them" | "very likely" - 확률로 포장 |
| `with the exception of those firmware features, we will not be able to sell those features to anybody` | "With the exception of those firmware features, we will not be able to sell those features to anybody" | "with the exception of" - 예외 명시 |
| `you can block or disable the exclusive feature by the firmware and you can sell that to the other customer` | (Jerry 확인) "You can block or disable the exclusive feature by the firmware" | 펌웨어 차단 - 해결책 |
| `without their permission, we will not be able to share that` | "without their permission, we will not be able to share that" | NDA 전제 - 책임 전가 |
| `before we finalize everything and it goes behind the curtain, we can have a review with SK hynix` | "Let's say before we finalize everything and it goes behind the curtain, we can have a review with SK hynix and SK hynix can decide whether they want to work with us on that or not" | "behind the curtain" - 마감 전 기회 창 |

**Audrey 교훈**: "behind the curtain"은 이 회의의 가장 강력한 비유다 - "한 번 커튼 뒤로 들어가면 꺼낼 수 없다"는 긴장감. "그 전에 리뷰하자"가 협상의 시간 압박을 만든다. 네가 파트너에게 "지금 결정 안 하면 나중에 못 한다"를 전할 때, "before it goes behind the curtain"을 써라. 직접적이면서도 극적으로 들린다.

### 단계 7: 솔직한 트랙레코드 (Honest Track Record)

발표자는 마지막에 자신의 실패 기록을 솔직하게 공개하며, 협력 진지함을 표현한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `my track record with SK hynix is not very good. In the last four years, I have not won a single project` | "And my track record, my success track record with the SK hynix is not very good. In the last four years, I have not won a single project. So I want to be careful. How can I be helpful?" | 솔직한 실패 인정 + "how can I be helpful" - 협력 의지 |

**Audrey 교훈**: "my track record is not very good" - 자기 평가를 솔직하게 하는 화법은 신뢰를 만든다. "I have not won a single project" - 구체적 숫자로 실패를 인정. 그리고 "So I want to be careful. How can I be helpful?" - 실패를 인정하고 즉시 협력 의지로 전환. 이게 진정성 있는 영업 화법이다. 한국어 "실적이 좋지 않습니다"는 약하지만, 영어 "I have not won a single project in four years"는 구체적이라 오히려 강하다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. Scaleflux 발표자가 약점·제한·거절을 어떻게 정중하게 포장하는지.

### 전략 1: "everything is possible" + 조건 (Open-But-Conditional)

가장 중요한 패턴. "가능하다"고 열되, 즉시 조건을 붙여 실질적 약속은 회피한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DRAM cache 지원 가능성 | "Look, everything is possible. We need to know what are we building because if we know what is your requirement, what is your RFQ, then we can be helpful to you" | "가능합니다. 다만 무엇을 만들지 알아야 합니다. 요구사항·RFQ를 알면 도움을 드릴 수 있습니다" |

**패턴 공식**: `Everything is possible. We need to know what are we building. If we know your requirement/RFQ, then we can be helpful.`

**Audrey 교훈**: "everything is possible"는 "yes"가 아니다. "yes, **if**"다. 한국어 "가능합니다, 다만 조건이 있습니다"와 같다. 영어 회의에서 "Is it possible?"에 "everything is possible"로 답하면, 긍정적으로 들리면서 책임은 지지 않는다. 핵심은 "We need to know what are we building" - 공을 상대에게 넘긴다.

### 전략 2: 무관한 제안 거절 (Irrelevant-Exercise Rejection)

과거의 무관한 미팅 패턴을 지적하며, 협력의 조건을 요구한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 진지한 의향 없는 미팅 | "Otherwise, it's, you know, exercise that I come and show you something and then you give me some feedback and then we go quiet for next few months. We don't talk to each other. It doesn't help you. It doesn't help us." | "그렇지 않으면, 제가 와서 보여드리고 피드백 받고 몇 달간 연락 안 하는 상황이 됩니다. 서로에게 도움이 안 됩니다" |

**패턴 공식**: `It's exercise that I come and show you something and then we go quiet for next few months. It doesn't help you. It doesn't help us.`

**Audrey 교훈**: "exercise"는 "운동"이 아니라 "공허한 행사"라는 뉘앙스다. "그냥 미팅만 하는 건 의미 없다"는 정중한 항의. "It doesn't help you. It doesn't help us." - "you"와 "us"를 병렬로 써서, 내 이익이 아니라 "우리"의 문제로 프레이밍. 이게 불만을 협력 제안으로 포장하는 화법이다. 한국어 "서로 시간 낭비입니다"보다 세련됐다.

### 전략 3: 로드맵 미포함 솔직 인정 (Off-Roadmap Honesty)

제품이 로드맵에 없음을 솔직히 인정하고, 고객 수요를 조건으로 건다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Aspen Next 프로젝트 | "this project is not on the roadmap today because we don't have any customer asking for this project" | "이 프로젝트는 현재 로드맵에 없습니다. 고객 요청이 없어서요" |
| 해결책 | "if there's an interest in this one, then we'll be happy to work with that customer and see how should we work with that" | "관심 있으시면, 고객과 협력하겠습니다" |

**패턴 공식**: `This is not on the roadmap today because we don't have any customer asking for this. If there's an interest, we'll be happy to work with that customer.`

**Audrey 교훈**: "not on the roadmap today" - "today"를 붙여 "지금은 없지만 바뀔 수 있다"는 뉘앙스. "because we don't have any customer asking" - 사유를 고객 부재로 돌리며, "네가 고객이 되면 바뀐다"를 암시. 이게 솔직하면서도 협상의 문을 여는 화법이다.

### 전략 4: NDA 책임 전가 (NDA Deflection)

스펙 공유를 거절하되, "타 고객 NDA"를 이유로 자기 책임이 아님을 표시한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Pooling 아키텍처 공유 | "I'm not sure how much of the architecture I can share with you when it is approved... The pooling will be a bit more difficult because it's a very different... without their permission, we will not be able to share that" | "승인되면 얼마나 공유할 수 있을지... pooling은 더 어렵습니다. 타 고객 허락 없이는 공유 불가합니다" |

**패턴 공식**: `I'm not sure how much of X I can share. Without their permission, we will not be able to share that. We will see when you are here.`

**Audrey 교훈**: "I'm not sure"는 모른다는 게 아니라 "공유할 수 없다"는 정중한 거절. "without their permission" - "their"를 써서 책임을 타 고객에게 전가. 자기가 거절하는 게 아니라 NDA 때문이라고 프레이밍. 그리고 "we will see when you are here" - 미래의 모호한 약속으로 마무리. 한국어 "NDA 때문에 공유하기 어렵습니다"의 세련된 영어 버전.

### 전략 5: 리소스 경쟁으로 긴장감 (Resource-Competition Urgency)

두 빅 프로젝트가 리소스를 다 잡을 것이라고 경고하며, 지금 결정할 것을 압박한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 프로젝트 우선순위 | "once we get involved into the second big project, then that will suck all the engineering resources" | "두 번째 빅 프로젝트에 들어가면 엔지니어링 리소스를 다 잡아먹습니다" |
| 시급성 | "if you have interest in this project, please let us know as soon as possible" | "관심 있으시면 최대한 빨리 알려주세요" |
| 판단 시점 | "it will be good to make a judgment call early on whether there's something SK hynix wants to be part of it or no" | "SK hynix이 참여할지 조기 판단하는 게 좋습니다" |

**패턴 공식**: `Once we get involved into the next big project, that will suck all the engineering resources. If you have interest, please let us know as soon as possible. Make a judgment call early on.`

**Audrey 교훈**: "suck all the engineering resources" - "suck"은 강한 동사다. "리소스를 다 빨아먹는다" - 자원 경쟁을 시각적으로 표현. 이게 "지금 안 하면 나중에 못 한다"는 시간 압박의 정중한 영어 버전. 한국어 "일정이 빡빡합니다"보다 훨씬 강한 압박. 그러나 "please let us know" + "make a judgment call"로 결정을 상대에게 맡기는 척 한다. 압박+존중의 조합.

### 전략 6: 솔직한 실패 인정 (Honest Failure Admission)

자신의 실적 부진을 솔직히 인정하며, 진지함으로 신뢰를 회복한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 4년간 무실적 | "my track record with SK hynix is not very good. In the last four years, I have not won a single project. So I want to be careful. How can I be helpful?" | "SK hynix과 실적이 좋지 않습니다. 4년간 단 하나도 못 따냈습니다. 조심하고 싶습니다. 어떻게 도움드릴까요?" |

**패턴 공식**: `My track record with X is not very good. In the last Y years, I have not won a single project. So I want to be careful. How can I be helpful?`

**Audrey 교훈**: 자기 실패를 인정하는 화법은 신뢰의 역설이다 - 약해 보이면서 오히려 강하다. "I have not won a single project" - 구체적 숫자(0)가 진정성을 만든다. 그리고 "How can I be helpful?" - 실패를 인정하고 즉시 협력 의지로 전환. 이게 영업의 진정성 화법이다. 한국어 "실적이 별로입니다"는 자살이지만, 영어 "I have not won a single project in four years"는 솔직함이 신뢰가 된다.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 로드맵·스펙·타임라인을 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 확인형 질문 (Am I Correct?)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Am I correct?` | "you mentioned that the Aspen or Aspen next, we will not have the compression functionality. Am I correct?" | "Am I correct?" - 확인형 질문의 핵심 화법 |
| `That's correct?` (발표자 확인) | "That's correct. Yes." | 발표자가 확인해 주는 패턴 |

**Audrey 교훈**: "Am I correct?"는 "내가 맞게 이해했나요?"를 짧게 만든 화법. 질문을 "내 이해가 맞는지 확인"으로 포장하면, 도전이 아니라 확인이 된다. 발표자는 "That's correct. Yes."로 쉽게 동의. 이게 로드맵 회의에서 스펙을 도전하는 가장 부드러운 화법이다.

### 질문 유형 2: 차이점 탐색 (Difference Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `what is the difference between X and Y?` | "what is the difference between those?... only different things are the compression, the pooling and the speed" | "difference between" - 비교 질문 |
| `So what is the difference between those?` (반복) | "So what is the difference between those?" | 같은 패턴 반복 사용 |

**Audrey 교훈**: "what is the difference between X and Y?"는 제품 비교 질문의 표준. "어떤 게 더 낫다"가 아니라 "차이가 뭐냐"로 물으면, 발표자가 자기 제품 한계를 스스로 드러내게 만든다. 이게 정중한 도전이다.

### 질문 유형 3: 범위 확인 (Scope Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So based on our specific requirements, you can help us, but now you guys are just focusing on the, not focusing on the DDM cache structure, right? Not in the scope currently, right?` | (동일 원문) | "right?" 연속 - 범위 한정 확인 |
| `Is it feasible generally?` | "Is it feasible generally?" | "generally" - 가능성 탐색 |

**Audrey 교훈**: "Not in the scope currently, right?" - "현재 scope 밖이죠?"로 발표자가 인정하게 만드는 화법. "right?"를 붙이면 질문이 아니라 확인이 된다. 발표자는 "That's correct. Yes."로 쉽게 동의. 이게 로드맵 회의에서 스펙 한계를 확인하는 가장 효율적 화법이다.

### 질문 유형 4: 기능 요구 (Feature Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we would like to have that feature, yeah, for your pine next` | "We would like to have that feature, yeah, for your pine next" | "would like to have" - 정중한 요구 |
| `we love to move from the software to the hardware cache coherence` | "we love to move from the software to the hardware cache coherence" | "love to move" - 방향성 표현 |
| `the BI, the backing validate, will be essential` | "So that BI, the backing validate, will be essential" | "will be essential" - 필수 요구 |

**Audrey 교훈**: "we would like to have X"는 정중한 요구의 표준. "we want"이 아니라 "would like to have". 그리고 "will be essential"로 필수성을 표시. "love to move from X to Y" - 현재 상태에서 목표 상태로의 전환을 표현. 이게 로드맵 회의에서 요구사항을 밀어붙이는 정중한 화법이다.

### 질문 유형 5: POC/전략 제안 (POC/Strategy Proposal)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are exploring, we want to explore and we want to make this some POC` | "So we are exploring, we want to explore and we want to make this some POC for the some other, I mean, adding card form factor, for the pooling, the pooled memory system" | "we are exploring / we want to explore" - 의향 표현 |
| `we also have our own software stack based on the KV cache sharing capability` | (동일) | 자산 공개 - 협상 카드 |

**Audrey 교훈**: "we are exploring, we want to explore" - "exploring"을 두 번 써서 의향을 강조. 그리고 "we also have our own software stack" - 자기 자산을 공개하며 협상 카드로 쓴다. "우리도 소프트웨어 스택이 있다"는 건 "우리도 가져올 게 있다"는 시그널. 이게 협상에서 양방향 가치 교환을 제안하는 화법이다.

### 질문 유형 6: 미팅 후속 제안 (Follow-Up Proposal)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `let me have some internal discussion and let's have a sync up meeting for that` | "let me have some internal discussion and let's have a sync up meeting for that" | "sync up meeting" - 후속 미팅 제안 |
| `I will update you if we fix some technical specs` | "I will update you if we fix some technical specs for the future UCG" | "update you if" - 조건부 후속 |

**Audrey 교훈**: "sync up meeting"은 후속 미팅의 표준 표현. "follow-up meeting"보다 가볍고 빈번한 뉘앙스. "let's have a sync up" - "sync up"이 동사처럼 쓰인다. 그리고 "I will update you if we fix X" - 조건부 후속 약속. "update you"는 "알려드리겠다"의 비즈니스 표준.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 **핵심 섹션** (Type B 회의이므로). 로드맵/공급 맞춤의 협상 언어.

### 4.1 타임라인 타겟 (Timeline Targets)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 타임라인 | Scaleflux | "We will be ready to give you samples sometime in Q4. Q4 this year" | "sometime in Q4" - 분기 단위 타임라인 |
| 테이프아웃 타겟 | Scaleflux | "We plan to tape it out sometime Q2 early next year and then move on to the pooling project" | "plan to tape out sometime Q2" - 개발 마일스톤 |
| 스펙 확정 타겟 | Scaleflux | "we believe that by Q1 timeframe, the pooling project specs will be finalized" | "by Q1 timeframe" - 시점 명시 |
| 펌웨어 확정 | Scaleflux | "We are going to completely finalize the firmware requirements. Sometime in September" | "finalize X sometime in September" - 월 단위 타겟 |
| 샘플 세부 시점 | SK | "Q4 means not late Q4. It's the only or middle Q4. Am I correct?" | "not late Q4, middle Q4" - 시점 확인 |

**Audrey 교훈**: 타임라인 표현의 위계: "sometime in Q4"(분기) > "sometime in September"(월) > "middle Q4"(분기 내 세분). 발표자는 "sometime"으로 여유를 두지만, SK 측은 "not late Q4, middle Q4"로 세분해서 묶는다. 네가 타임라인을 받을 때, "sometime Q4"는 "Q4 어느 때"인지 확인해라 - "not late Q4, right?"로.

### 4.2 볼륨/샘플 요청 (Sample Requests)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 제공 의향 | Scaleflux | "we'll be very happy to provide a couple of samples to SK hynix if they are interested" | "couple of samples" + "if interested" |
| 1by8 추가 요청 | SK | "Do you have a plan to make the 2, 1 by 8 after evaluation of 1 by 4?" | "Do you have a plan to make X after Y?" - 후속 요청 |
| 1by8 가능 확인 | Scaleflux | "absolutely we can do 1 by 8. That is not an issue" | "absolutely we can do" + "not an issue" - 강한 긍정 |
| 1by4 우선 | Scaleflux | "1 by 4 samples will come sooner than 1 by 8" | "sooner than" - 순서 명시 |

**Audrey 교훈**: "Do you have a plan to make X after Y?" - 후속 제품 의향을 묻는 표준. 발표자는 "absolutely we can do X. That is not an issue" - "absolutely" + "not an issue"로 강하게 긍정. 그러나 "sooner than"으로 순서를 명시. 네가 샘플을 요청할 때, "Do you have a plan to make X after Y?"로 후속까지 묻고, "sooner than"으로 순서를 확인해라.

### 4.3 스펙 푸시백 (Spec Pushback)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 스펙 한정 | Scaleflux | "this was designed for a very specific use case for a very specific hyperscalers" | "very specific" 반복 - 기대치 관리 |
| 미지원 명시 | Scaleflux | "Those are the things that are not supported on aspen next today. They are outside of the scope" | "outside of the scope" - 명시적 제외 |
| 커스텀 전제 | Scaleflux | "both of these projects will require NRE and we are going to get NRE from these hyperscalers. Without that, it will be very difficult for us to do all by ourselves" | "without that, very difficult" - NRE 전제 |
| 요구사항 전제 | Scaleflux | "if you have finalized your RFQ, you have finalized your specs, then it's much easier for me and my team to respond to that" | "if you have finalized X, much easier" - 스펙 전제 |

**Audrey 교훈**: 스펙 푸시백의 3단계: (1) "very specific"으로 기대치 낮추기, (2) "outside of the scope"로 명시적 제외, (3) "without NRE, very difficult"로 비용 전제. 이게 파트너가 요구를 거절하는 정중한 화법. 네가 스펙을 푸시백할 때, "outside of the scope today"로 오늘 한계를 명시하고, "without X, very difficult"로 조건을 건다.

### 4.4 비용 분담 협상 (Cost-Sharing Negotiation)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| NRE 요구 | Scaleflux | "both of these projects will require NRE and we are going to get NRE from these hyperscalers" | "will require NRE" - 비용 요구 |
| 분담 의지 | Scaleflux | "we are willing to put, you know, good portion of that cost ourselves" | "willing to put" - 분담 의지 |
| 부담 완화 | Scaleflux | "we don't ask SK hynix to put all the cost" | "don't ask... all the cost" - 부담 완화 |
| 분담 제안 | Scaleflux | "let's share some cost for each other" | "share some cost" - 분담 제안 |
| 부담 공유 | Scaleflux | "some costs so we can share the burden" | "share the burden" - 부담 공유 표현 |
| MOU 요구 | Scaleflux | "And that will require MOU" | "require MOU" - 형식적 약정 |

**Audrey 교훈**: 비용 분담 협상의 공식: (1) "will require NRE"로 비용 필요성 명시, (2) "we are willing to put a good portion ourselves"로 자기 부담 표시, (3) "we don't ask you to put all the cost"로 상대 부담 완화, (4) "let's share some cost" / "share the burden"로 분담 제안, (5) "require MOU"로 형식화. 이 5단계를 외워. 한국어 "비용 분담하죠"의 5배 정교한 영어 버전이다.

### 4.5 Exclusive Feature 협상 (Exclusive Feature Negotiation)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| Exclusive 공개 | Scaleflux | "it is very likely that it is going to be a custom SOC for them" | "very likely custom SOC" - exclusive 예고 |
| 펌웨어 차단 | Scaleflux | "with the exception of those firmware features, we will not be able to sell those features to anybody" | "with the exception of" - 예외 명시 |
| 차단 해결책 | Jerry | "You can block or disable the exclusive feature by the firmware and you can sell that MC700 to the other customer" | "block or disable by firmware" - 해결책 제안 |
| 사전 리뷰 제안 | Scaleflux | "before we finalize everything and it goes behind the curtain, we can have a review with SK hynix and SK hynix can decide whether they want to work with us on that or not" | "behind the curtain" - 사전 기회 창 |
| 판단 촉구 | Scaleflux | "it will be good to make a judgment call early on whether there's something SK hynix wants to be part of it or no" | "judgment call early on" - 조기 결정 촉구 |

**Audrey 교훈**: exclusive feature 협상의 핵심은 "before it goes behind the curtain"이라는 시간 압박. "한 번 커튼 뒤로 가면 못 꺼낸다" - 이 비유가 결정 시급성을 만든다. 그리고 "judgment call early on" - "early on"이 "빨리"의 정중한 표현. "decide whether you want to be part of it or no" - 결정을 상대에게 맡기는 척하면서 압박. 이게 exclusive 협상의 마스터 화법이다.

### 4.6 액션 아이템 (Action Items)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 미팅 | SK | "let me have some internal discussion and let's have a sync up meeting for that" | "sync up meeting" - 후속 약속 |
| 스펙 업데이트 | SK | "I will update you if we fix some technical specs" | "update you if" - 조건부 후속 |
| 연락 유지 | 양측 | "we will keep in touch" | "keep in touch" - 가벼운 후속 |
| OCP 전 연락 | Scaleflux | "I hope to speak with you before the OCP" | "speak with you before X" - 시점 명시 후속 |

**Audrey 교훈**: 이 회의의 action item은 구체적이지 않다 - "sync up meeting", "update you if", "keep in touch". 이게 로드맵 회의의 전형 - 구체적 책임보다 "계속 대화하자"가 액션. 그러나 "speak with you before OCP"는 시점이 명확한 후속. 네가 action item을 잡을 때, "sync up meeting"으로 가볍게 시작하고, "speak before X"로 시점을 명시해라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/컨트롤러/로드맵 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **Aspen** | Scaleflux 1세대 CXL 컨트롤러 | "the first available Aspen will be the original Aspen" - 제품 코드명 |
| **Aspen Next** | Aspen + cache + LPDDR5 파생 | "Aspen next is mostly Aspen but with the cache. Cache and the LPDDR5 support" - 파생 제품 설명 |
| **MC700** | Scaleflux 6-Series pooling 칩 | "the 6-Series pooling from your load map. MC700" - 제품명 |
| **by four / by eight** | NAND 채널 폭 (x4, x8) | "the by four means that it looks like the more focusing on the NVMe" - 폭별 용도 |
| **NRE** (Non-Recurring Engineering) | 일회성 개발 비용 | "both of these projects will require NRE" - 비용 요구 |
| **MOU** (Memorandum of Understanding) | 양해 각서 | "And that will require MOU" - 형식적 약정 |
| **RFQ** (Request for Quote) | 견적 요청서 | "if we know what is your requirement, what is your RFQ, then we can be helpful" - 요구사항 전제 |
| **tape out** | 칩 설계 완료·제조 의뢰 | "we plan to tape it out sometime Q2 early next year" - 개발 마일스톤 |
| **locked and loaded** | 완전 준비됨·확정됨 | "the compression one is almost 95% locked and loaded" - 상태 표현 |
| **kicked off** | 프로젝트 시작됨 | "we have already kicked off that project" - 진행 상태 |
| **bring up** | 하드웨어 초기 구동 검증 | "We are bringing it up. We are making sure that it meets all of our requirements" - 검증 단계 |
| **pooling** | 메모리 풀링 (CXL shared memory) | "the pooling project specs will be finalized" - 로드맵 프로젝트 |
| **compression** | 데이터 압축 기능 | "the compression one is almost 95% locked and loaded" - 기능명 |
| **backing validate** | CXL 백킹 저장소 검증 | "backing validate will be a requirement of that and we will support it" - 요구사항 |
| **prefetch** | 데이터 사전 읽기 | "it can prefetch and read data from the NAND media" - 캐시 기능 |
| **SOC** (System on Chip) | 단일 칩 시스템 | "it is going to be a custom SOC for them" - 커스텀 칩 |
| **custom SOC** | 고객 맞춤형 칩 | "very likely that it is going to be a custom SOC for them" - exclusive 전제 |
| **4DPC** (4 DIMMs Per Channel) | 채널당 4 DIMM | "4DPC" - 밀도 스펙 (발음 혼동 주의) |
| **2DPC** (2 DIMMs Per Channel) | 채널당 2 DIMM | "4 channel, 2DPC" - 정정된 스펙 |
| **E3 form factor** | EDSFF E3 서버 폼팩터 | "we will start building E3 form factors or maybe I see card" - 물리 형태 |
| **FMS** (Flash Memory Summit) | 플래시 메모리 서밋 | "this is a chip that how announced at FMS" - 전시회 |
| **OCP** (Open Compute Project) | 오픈 컴퓨트 프로젝트 | "I hope to speak with you before the OCP" - 행사 시점 |
| **test dev** | 테스트 개발 | "gives enough data point for test dev" - 검증 단계 |
| **SOCAM** | SoC 어벤더bles (소켓 어벤더블 메모리?) | "it depends on the SOCAMS situation" - 공급 상황 변수 |
| **UCG** | Use Case Group (?) | "what is the target, UCG or application for this architecture?" - 용도 분류 |
| **NDA** (Non-Disclosure Agreement) | 비밀유지계약 | "without their permission, we will not be able to share that" - NDA 전제 |
| **Penguin** | (마벨 예에서 언급, 본 회의 미사용) | - | - |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 50개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 로드맵 발표 (Roadmap Presentation) ──
- id: m02-001
  expression: "Samples will be given in the first phase one by four or sometime in Q4"
  category: timeline_anchor
  function: sample_timeline
  speaker_role: presenter
  difficulty: 3
  context: "Samples will be given in the first phase one by four or sometime in Q4 and we'll be very happy to provide a couple of samples to SK hynix if they are interested"
  note: 로드맵 회의 첫 문장 - 타임라인 앵커

- id: m02-002
  expression: "we'll be very happy to provide a couple of samples to X if they are interested"
  category: sample_offer
  function: conditional_sample
  speaker_role: presenter
  difficulty: 3
  context: "we'll be very happy to provide a couple of samples to SK hynix if they are interested"
  note: "happy to" + "if interested" - 조건부 샘플 제공

- id: m02-003
  expression: "this was designed for a very specific use case for a very specific hyperscalers"
  category: scope_limiting
  function: expectation_management
  speaker_role: presenter
  difficulty: 4
  context: "But this was designed for a very specific use case for a very specific hyperscalers"
  note: "very specific" 반복 - 기대치 관리

- id: m02-004
  expression: "the compression one is almost 95% locked and loaded"
  category: project_status
  function: status_confirmation
  speaker_role: presenter
  difficulty: 4
  context: "the compression one is almost 95% locked and loaded"
  note: "locked and loaded" - 확정 상태 군사 유래 표현

- id: m02-005
  expression: "we have already kicked off that project"
  category: project_status
  function: in_progress
  speaker_role: presenter
  difficulty: 3
  context: "We will, we have already kicked off that project"
  note: "kicked off" - 프로젝트 시작 표준 동사

- id: m02-006
  expression: "we believe that by Q1 timeframe, the X specs will be finalized"
  category: timeline_target
  function: future_finalization
  speaker_role: presenter
  difficulty: 4
  context: "we believe that by Q1 timeframe, the pooling project specs will be finalized"
  note: "by Q1 timeframe" - 시점 명시

- id: m02-007
  expression: "this project is not on the roadmap today because we don't have any customer asking for this project"
  category: off_roadmap
  function: honest_status
  speaker_role: presenter
  difficulty: 4
  context: "this project is not on the roadmap today because we don't have any customer asking for this project"
  note: "today" - 현재 한정, 고객 요청 조건 암시

- id: m02-008
  expression: "we plan to tape it out sometime Q2 early next year"
  category: milestone_target
  function: dev_schedule
  speaker_role: presenter
  difficulty: 3
  context: "We plan to tape it out sometime Q2 early next year and then move on to the pooling project"

- id: m02-009
  expression: "we are going to completely finalize the firmware requirements sometime in September"
  category: milestone_target
  function: spec_finalization
  speaker_role: presenter
  difficulty: 3
  context: "We are going to completely finalize the firmware requirements. Sometime in September"

# ── 요구사항-우선 스탠스 (Requirements-First Stance) ──
- id: m02-010
  expression: "if we know what is your requirement, what is your RFQ, then we can be helpful to you"
  category: conditional_help
  function: rfq_prerequisite
  speaker_role: presenter
  difficulty: 5
  context: "if we know what is your requirement, what is your RFQ, then we can be helpful to you"
  note: 이 회의의 핵심 협상 화법 - 도움을 조건으로 포장

- id: m02-011
  expression: "if we don't know it, then we don't know what really we can help you with"
  category: conditional_refusal
  function: pressure_via_negation
  speaker_role: presenter
  difficulty: 4
  context: "If we don't know it, then we don't know what really we can help you with"

- id: m02-012
  expression: "if you have finalized your RFQ, you have finalized your specs, then it's much easier for me and my team to respond to that"
  category: conditional_help
  function: spec_prerequisite
  speaker_role: presenter
  difficulty: 4
  context: "if you have finalized your RFQ, you have finalized your specs, then it's much easier for me and my team to respond to that"

- id: m02-013
  expression: "it will be very, very helpful if you give us your specs"
  category: request
  function: spec_request
  speaker_role: presenter
  difficulty: 3
  context: "it will be very, very helpful if you give us your specs. Then I can be helpful and respond very quickly"
  note: "very, very" 반복 - 간절함 표현

- id: m02-014
  expression: "everything is possible. We need to know what are we building"
  category: open_conditional
  function: yes_if
  speaker_role: presenter
  difficulty: 5
  context: "Look, everything is possible. We need to know what are we building"
  note: "everything is possible"는 yes가 아니라 "yes, if"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m02-015
  expression: "it's exercise that I come and show you something and then you give me some feedback and then we go quiet for next few months"
  category: irrelevant_rejection
  function: diplomatic_complaint
  speaker_role: presenter
  difficulty: 5
  context: "Otherwise, it's, you know, exercise that I come and show you something and then you give me some feedback and then we go quiet for next few months. We don't talk to each other."
  note: "exercise" = 공허한 행사. 불만을 협력 제안으로 포장

- id: m02-016
  expression: "it doesn't help you. It doesn't help us"
  category: mutual_interest
  function: parallel_negation
  speaker_role: presenter
  difficulty: 4
  context: "It doesn't help you. It doesn't help us."
  note: "you"와 "us" 병렬 - 내 이익 아닌 "우리" 문제로 프레이밍

- id: m02-017
  expression: "I'm not sure how much of the architecture I can share with you when it is approved"
  category: nda_deflection
  function: polite_refusal
  speaker_role: presenter
  difficulty: 4
  context: "I'm not sure how much of the architecture I can share with you when it is approved"

- id: m02-018
  expression: "without their permission, we will not be able to share that"
  category: nda_deflection
  function: blame_shift
  speaker_role: presenter
  difficulty: 4
  context: "without their permission, we will not be able to share that"
  note: "their" - 책임을 타 고객에게 전가

- id: m02-019
  expression: "we will see, you know, when you are here"
  category: vague_promise
  function: future_deflection
  speaker_role: presenter
  difficulty: 3
  context: "But we will see, you know, when you are here"

- id: m02-020
  expression: "once we get involved into the second big project, then that will suck all the engineering resources"
  category: resource_urgency
  function: time_pressure
  speaker_role: presenter
  difficulty: 5
  context: "once we get involved into the second big project, then that will suck all the engineering resources"
  note: "suck all the resources" - 강한 시각적 압박

- id: m02-021
  expression: "if you have interest in this project, please let us know as soon as possible"
  category: urgency_request
  function: decision_pressure
  speaker_role: presenter
  difficulty: 4
  context: "if you have interest in this project, please let us know as soon as possible"

- id: m02-022
  expression: "it will be good to make a judgment call early on whether there's something X wants to be part of it or no"
  category: decision_urge
  function: early_judgment
  speaker_role: presenter
  difficulty: 5
  context: "it will be good to make a judgment call early on whether there's something SK hynix wants to be part of it or no"
  note: "judgment call early on" - 조기 결정 촉구

- id: m02-023
  expression: "my track record with X is not very good. In the last Y years, I have not won a single project"
  category: honest_admission
  function: trust_building
  speaker_role: presenter
  difficulty: 5
  context: "my track record with the SK hynix is not very good. In the last four years, I have not won a single project"
  note: 솔직한 실패 인정 - 신뢰의 역설

- id: m02-024
  expression: "So I want to be careful. How can I be helpful?"
  category: pivot_to_help
  function: failure_to_collaboration
  speaker_role: presenter
  difficulty: 4
  context: "So I want to be careful. How can I be helpful?"

# ── NRE / 비용 분담 (Cost-Sharing) ──
- id: m02-025
  expression: "both of these projects will require NRE and we are going to get NRE from these hyperscalers"
  category: nre_request
  function: cost_requirement
  speaker_role: presenter
  difficulty: 4
  context: "both of these projects will require NRE and we are going to get NRE from these hyperscalers"

- id: m02-026
  expression: "without that, it will be very difficult for us to do all by ourselves"
  category: nre_justification
  function: cost_reason
  speaker_role: presenter
  difficulty: 4
  context: "Without that, I think it will be very difficult for us to do all by ourselves because as you know, these are very, very expensive chips"

- id: m02-027
  expression: "we are willing to put a good portion of that cost ourselves"
  category: cost_sharing
  function: burden_sharing
  speaker_role: presenter
  difficulty: 4
  context: "we are willing to put, you know, good portion of that cost ourselves"
  note: "willing to put" - 분담 의지 표시

- id: m02-028
  expression: "we don't ask, we don't expect, we don't need all the cost related to this one"
  category: burden_reduction
  function: triple_negation
  speaker_role: presenter
  difficulty: 5
  context: "we don't ask, we don't expect, we don't need all the cost related to this one"
  note: 삼중 부정 - 부담 완화 강조

- id: m02-029
  expression: "let's share some cost for each other"
  category: cost_sharing
  function: sharing_proposal
  speaker_role: presenter
  difficulty: 3
  context: "let's share some cost for each other"

- id: m02-030
  expression: "some costs so we can share the burden"
  category: cost_sharing
  function: burden_sharing
  speaker_role: presenter
  difficulty: 3
  context: "some costs so we can share the burden"

- id: m02-031
  expression: "And that will require MOU"
  category: formal_commitment
  function: mou_requirement
  speaker_role: presenter
  difficulty: 3
  context: "And that will require MOU"

# ── Exclusive Feature 협상 ──
- id: m02-032
  expression: "it is very likely that it is going to be a custom SOC for them"
  category: exclusive_disclosure
  function: custom_soc_warning
  speaker_role: presenter
  difficulty: 4
  context: "It is very likely that it is going to be a custom SOC for them because we are asking them for a lot of NRE"

- id: m02-033
  expression: "with the exception of those firmware features, we will not be able to sell those features to anybody"
  category: exclusive_feature
  function: feature_lock
  speaker_role: presenter
  difficulty: 4
  context: "With the exception of those firmware features, we will not be able to sell those features to anybody"

- id: m02-034
  expression: "you can block or disable the exclusive feature by the firmware"
  category: firmware_block
  function: workaround
  speaker_role: questioner
  difficulty: 4
  context: "You can block or disable the exclusive feature by the firmware and you can sell that MC700 to the other customer"

- id: m02-035
  expression: "before we finalize everything and it goes behind the curtain, we can have a review with X"
  category: time_window
  function: pre_lock_review
  speaker_role: presenter
  difficulty: 5
  context: "Let's say before we finalize everything and it goes behind the curtain, we can have a review with SK hynix and SK hynix can decide whether they want to work with us on that or not"
  note: "behind the curtain" - 이 회의의 가장 강력한 비유

# ── 정중한 도전 (Polite Challenge) ──
- id: m02-036
  expression: "Am I correct?"
  category: confirmation_check
  function: verify_understanding
  speaker_role: questioner
  difficulty: 2
  context: "you mentioned that the Aspen or Aspen next, we will not have the compression functionality. Am I correct?"

- id: m02-037
  expression: "what is the difference between X and Y?"
  category: difference_probe
  function: comparison
  speaker_role: questioner
  difficulty: 3
  context: "what is the difference between those?"

- id: m02-038
  expression: "Not in the scope currently, right?"
  category: scope_confirm
  function: limit_verify
  speaker_role: questioner
  difficulty: 3
  context: "now you guys are just focusing on the, not focusing on the DDM cache structure, right? Not in the scope currently, right?"

- id: m02-039
  expression: "Is it feasible generally?"
  category: feasibility_probe
  function: possibility_check
  speaker_role: questioner
  difficulty: 2
  context: "Is it feasible generally?"

- id: m02-040
  expression: "we would like to have that feature for your pine next"
  category: feature_request
  function: polite_demand
  speaker_role: questioner
  difficulty: 4
  context: "We would like to have that feature, yeah, for your pine next"

- id: m02-041
  expression: "we love to move from the software to the hardware cache coherence"
  category: direction_stating
  function: transition_request
  speaker_role: questioner
  difficulty: 4
  context: "we love to move from the software to the hardware cache coherence"

- id: m02-042
  expression: "the X will be essential"
  category: requirement_stating
  function: essential_demand
  speaker_role: questioner
  difficulty: 3
  context: "So that BI, the backing validate, will be essential"

- id: m02-043
  expression: "we are exploring, we want to explore and we want to make this some POC"
  category: intent_stating
  function: exploration_signal
  speaker_role: questioner
  difficulty: 4
  context: "we are exploring, we want to explore and we want to make this some POC for the some other, I mean, adding card form factor, for the pooling"

- id: m02-044
  expression: "we also have our own software stack based on the X capability"
  category: asset_disclosure
  function: negotiation_card
  speaker_role: questioner
  difficulty: 4
  context: "we also have our own software stack and I mean, it's based on the KV cache sharing capability"

# ── 타임라인 / 샘플 (Timeline & Sample) ──
- id: m02-045
  expression: "Q4 means not late Q4. It's the only or middle Q4. Am I correct?"
  category: timeline_confirm
  function: time_narrowing
  speaker_role: questioner
  difficulty: 4
  context: "Q4 means not late Q4. It's the only or middle Q4. Am I correct?"
  note: "sometime Q4"를 "middle Q4"로 세분 - 시점 확정

- id: m02-046
  expression: "Do you have a plan to make the X after evaluation of Y?"
  category: follow_up_plan
  function: subsequent_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "Do you have a plan to make the 2, 1 by 8 after evaluation of 1 by 4?"

- id: m02-047
  expression: "absolutely we can do X. That is not an issue"
  category: strong_confirm
  function: strong_yes
  speaker_role: presenter
  difficulty: 3
  context: "absolutely we can do 1 by 8. That is not an issue"

- id: m02-048
  expression: "X samples will come sooner than Y"
  category: sequence_stating
  function: order_confirm
  speaker_role: presenter
  difficulty: 3
  context: "1 by 4 samples will come sooner than 1 by 8"

# ── 후속 / 액션 (Follow-Up) ──
- id: m02-049
  expression: "let me have some internal discussion and let's have a sync up meeting for that"
  category: follow_up
  function: sync_meeting
  speaker_role: questioner
  difficulty: 3
  context: "let me have some internal discussion and let's have a sync up meeting for that"
  note: "sync up meeting" - 후속 미팅 표준 표현

- id: m02-050
  expression: "I will update you if we fix some technical specs"
  category: conditional_followup
  function: update_promise
  speaker_role: questioner
  difficulty: 3
  context: "I will update you if we fix some technical specs for the future UCG"

- id: m02-051
  expression: "I hope to speak with you before the OCP"
  category: time_anchored_followup
  function: event_anchored
  speaker_role: presenter
  difficulty: 3
  context: "I hope to speak with you before the OCP"
  note: 행사 시점 기반 후속 - 구체적 시점

- id: m02-052
  expression: "we will keep in touch"
  category: light_followup
  function: contact_promise
  speaker_role: both
  difficulty: 1
  context: "we will keep in touch"

- id: m02-053
  expression: "if not, then that is okay"
  category: graceful_exit
  function: no_pressure
  speaker_role: presenter
  difficulty: 3
  context: "If not, then that is okay. You let us know what are your specs, and we will be happy to give you a response on that"
  note: 관심 없을 경우 정중한 퇴로

- id: m02-054
  expression: "you let us know what are your specs, and we will be happy to give you a response on that"
  category: open_offer
  function: standing_offer
  speaker_role: presenter
  difficulty: 3
  context: "You let us know what are your specs, and we will be happy to give you a response on that"

- id: m02-055
  expression: "Please let us know as soon as possible"
  category: urgency_request
  function: time_pressure
  speaker_role: presenter
  difficulty: 2
  context: "if you have interest in this project, please let us know as soon as possible"

- id: m02-056
  expression: "we are not there yet"
  category: status_honest
  function: current_limit
  speaker_role: presenter
  difficulty: 3
  context: "We are not there yet"
  note: 솔직한 현재 상태 인정

- id: m02-057
  expression: "to be honest, to be very frank with you"
  category: honesty_preface
  function: candid_stating
  speaker_role: presenter
  difficulty: 3
  context: "to be honest, to be very frank with you, our RDIM is now going to be very busy with the two projects"
  note: "to be honest" + "to be very frank" - 이중 솔직 전제

- id: m02-058
  expression: "this is something that we can do very, very quickly if someone is interested in that"
  category: easy_project
  function: low_effort_offer
  speaker_role: presenter
  difficulty: 3
  context: "this is something that we can do very, very quickly if someone is interested in that"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-08-19 09 08 05_EN_Scaleflux-extracted.wav` (총 ~30분, 4,423단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-15) | "Samples will be given in Q4" + "very specific use case" | 타임라인 앵커 + 기대치 관리 | ★★ |
| 2 | 요구사항 스탠스 (line 86-92) | "everything is possible" + "if we know your RFQ" + "exercise" 항의 | 요구사항-우선 스탠스 + 정중 항의 | ★★★★ |
| 3 | NRE/비용 분담 (line 184-209) | "will require NRE" + "willing to put cost ourselves" + "share the burden" | 비용 분담 5단계 화법 | ★★★★ |
| 4 | Exclusive 협상 (line 196-199) | "behind the curtain" + "judgment call early on" | exclusive 시간 압박 화법 | ★★★★★ |
| 5 | 마무리 (line 337-405) | "track record not good" + "MOU" + "speak before OCP" | 솔직한 트랙레코드 + 후속 약정 | ★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 각 단계에 발췌를 넣어 사용
- 발췌 2, 4가 가장 가치 높음 - 요구사항 스탠스·exclusive 협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap pitch + conditional negotiation** register다. 발표자가 로드맵을 설명하고, 조건부로 협상을 여는 구조. 두 역할 모두 학습해야:
- **발표자 역할 (Scaleflux)**: 타임라인 앵커, 요구사항-우선 스탠스, NRE/비용 분담, exclusive 공개, 솔직한 트랙레코드 - 네가 파트너에게 로드맵을 설명할 때
- **질문자 역할 (SK Hynix)**: 확인형 질문, 차이점 탐색, 범위 확인, 기능 요구, POC 제안 - 네가 파트너 로드맵을 평가할 때

### Pragmatics (화용론) 핵심
1. **"everything is possible" + "if"**: 영어 회의에서 "Is it possible?"에 "everything is possible"로 답하면, 긍정적으로 들리면서 책임은 회피. 핵심은 "We need to know what are we building" - 공을 상대에게 넘긴다. "yes, if"의 화법.
2. **"if you give us your RFQ, we can be helpful"**: 도움을 조건으로 포장. "we can help you"를 반복하되 매번 "if you give us your RFQ"라는 조건을 붙인다. 도움을 주는 척하면서 요구사항을 받아내는 화법.
3. **"behind the curtain"**: "한 번 커튼 뒤로 가면 못 꺼낸다" - exclusive 협상의 시간 압박 비유. "그 전에 리뷰하자"가 결정 시급성을 만든다. 이게 정중하면서도 강한 압박 화법.
4. **"we are willing to put a good portion ourselves"**: 비용 분담에서 자기 부담을 먼저 말하면 상대방이 거절하기 어렵다. "we don't ask you to put all the cost" 삼중 부정으로 부담 완화.
5. **"I have not won a single project in four years"**: 자기 실패를 구체적 숫자로 인정하면, 오히려 신뢰가 생긴다. "How can I be helpful?"로 즉시 협력 의지로 전환.

### 네가 당장 써야 할 Top 5
1. **"Everything is possible. We need to know what are we building"** - yes, if 회피
2. **"if you give us your RFQ, we can be helpful"** - 도움을 조건으로 포장
3. **"before it goes behind the curtain, we can have a review"** - 시간 압박 협상
4. **"we are willing to put a good portion ourselves"** - 비용 분담 의지
5. **"Am I correct?" / "Not in the scope currently, right?"** - 정중한 도전

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "가능합니다" | "Everything is possible. We need to know what are we building" | 한국어는 "가능"으로 끝, 영어는 "if" 조건 |
| "스펙 주시면 검토하겠습니다" | "if you give us your RFQ, we can be helpful" | 도움을 조건으로 포장 |
| "NRE 필요합니다" | "will require NRE. We are willing to put a good portion ourselves" | 비용 요구 전 자기 부담 먼저 |
| "지금 결정 안 하면 나중에 안 됩니다" | "before it goes behind the curtain, we can have a review" | "behind the curtain" 비유가 압박을 극적으로 |
| "실적이 별로입니다" | "I have not won a single project in four years" | 구체적 숫자가 진정성 |
| "scope 밖입니다" | "Not in the scope currently, right?" | "right?"로 확인형 질문 |
| "차이가 뭡니까?" | "what is the difference between X and Y?" | "difference between" 표준 |
| "후속 미팅 합시다" | "let's have a sync up meeting for that" | "sync up"이 가벼운 후속 표현 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 58개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법(특히 "everything is possible" + "exercise" 항의)·4절 비용 분담 5단계·4절 exclusive 협상 "behind the curtain"을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 연습**: 발표자 역할(Scaleflux)과 질문자 역할(SK)을 번갈아 연습 - 둘 다 실전에서 써야

---

*Textbook 02 - Scaleflux (2026-08-19). 회의 유형 B (로드맵/공급 맞춤, A에서 재분류). 표현 DB 58개. 5개 발췌 구간. 작성: 2026-09-01.*
