---
textbook_id: 04
meeting: NVIDIA 2H (GDDR Roadmap, MRDIMM Buffer, MSM/CXL, MRM, LPDDR6)
date: 2026-08-13
type: B (Roadmap/Supply Alignment)
partner: NVIDIA
sk_side: SK Hynix (Yong-jae, John/Song, Won-Ho Shin, Sung-Joo Lee, Jong-myung, Steve, Isangkwon, Hayoung)
duration_words: 10197
audio: repo/webex-audio/2026-08-13 15 38 50_EN_NVIDIA_2H-extracted.wav
transcript: repo/webex-audio/2026-08-13 15 38 50_EN_NVIDIA_2H-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, nvidia, gddr, mrdimm, msm, cxl, mrm, lpddr6, roadmap, supply-alignment]
---

# Textbook 04 - NVIDIA 2H (2026-08-13)

> **회의 유형**: B (Roadmap/Supply Alignment) - 다수의 SK Hynix 발표자가 NVIDIA에 로드맵/샘플/스펙 제안, NVIDIA가 제약/관심도 피드백
> **학습 가치**: 타임라인 표시("we plan to / we are targeting X in Y"), 샘플 요청("can you support X by Y"), 스펙 pushback("we don't think it's feasible with the current architecture"), 부드러운 미루기("we can look into it"), 정직한 한계 인정("frankly the best we can do at the moment")
> **Audrey 관점**: 이 회의는 "공급자 다발 제안 + 고객 제약 피드백"의 전형. 네가 SK 입장에서 NVIDIA에 로드맵을 밀거나, NVIDIA 입장에서 SK 제안을 받을 때 모두 쓰는 화법

---

## 1. 발화 아키텍처 - SK 발표자의 "제안-타임라인-제약" 3단 구조

이 회의는 6명 이상의 SK 발표자가 연달아 제안한다. 각 발표자는 비슷한 3단 구조를 따른다. 이게 네가 따라 배워야 할 "로드맵 발표의 뼈대"다.

### 단계 1: 요구 정합성 프레이밍 (Demand Framing)

제품을 소개하기 전에 **"고객 요구에 부합한다"**로 시작한다. "우리 제품이 좋다"가 아니라 "이 요구에 맞춰 설계했다"로.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `this one just summarizes some technical demand or some requirements for X by era` | "this one just summarizes some technical demand or some requirements for GDDR memory by era and describes what our lineup have evolved to address them" | 요구-제품 연결 - "무엇을 위해 만들었는지" |
| `so to address those demand, we just decided to have X in Y` | "So to address those demand, we just decided to have this silicon in 2027, which is the one C32 gigabyte G7 with the 36 to 40 gigabyte per second" | "to address those demand" - 요구 해결 명시 |
| `the supportable scope based on X has reached its limits` | "the supportable scope based on the G7, I mean, based on the 1D nanometer, has reached its limits" | 한계 선언 - "더 이상 못 함" 명시 |

**Audrey 교훈**: 영어 로드맵 발표는 "우리 기술"으로 시작하지 않는다. **"고객 요구(demand)"**로 시작한다. "to address those demand, we decided to X" - 이 공식을 외워. 회의에서 신규 투자/샘플 제안할 때, "우리가 만들고 싶어서"가 아니라 "그 요구를 해결하기 위해"로 프레이밍하면 설득력이 3배가 된다.

### 단계 2: 타임라인 명시 (Timeline Specification)

제안마다 **구체 분기**를 명시한다. "내년 쯤"이 아니라 "2027 1분기~2분기"로.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we plan to have X with Y, so the timeline would be Z` | "we plan to have some the 5-carbicabit RPC SOCAM with the Buprachit. So the timeline would be a 2027 next year, the course quarter" | timeline 명시 공식 |
| `we already have the schedule maybe this X quarter one and quarter two` | "We already have the schedule maybe this 2027 quarter one and quarter two" | "we already have the schedule" - 일정 확정 표시 |
| `we haven't had any specific schedule yet, but if you have any interest, we can have more discussion` | "we haven't had any some specific schedule yet, but if you, if NVIDIA has some any interest to evaluate this kind of some samples, we can have some more discussion and we can fix some schedule" | 미확정 + 관심 탐색 |

**Audrey 교훈**: 타임라인은 3단계로 표현한다: (1) 확정 - "we plan to / we already have the schedule", (2) 조건부 - "if you have interest, we can fix the schedule", (3) 미확정 - "we haven't had any specific schedule yet". 이 3가지를 상황에 따라 섞어 써라. 한국어 "일정 검토하겠습니다"는 영어로 3가지로 나뉜다.

### 단계 3: 가치 제안 + 제약 인정 (Value + Constraint)

제안 뒤에 항상 **"현재 한계"**를 인정한다. 이게 SK가 정직한 파트너로 보이게 하는 핵심.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `this is frankly the best we can do at the moment with the current X` | "this is frankly the best we can do at the moment with the current modulate note" | 한계 인정 - "frankly"로 정직함 강조 |
| `we don't think it's feasible with the current architecture` | "Maybe 16 kFPS is... We don't think it's feasible with the current architecture, so maybe we have to find some other way" | 스펙 pushback - "안 됨"을 정중하게 |
| `we need some other type like X, different architecture` | "we need some other type like retimer, different architecture" | 대안 제시 - 부정 뒤 "다른 방식" |

**Audrey 교훈**: 영어 로드맵 발표에서 "frankly"는 중요한 단어다. "frankly the best we can do at the moment" - "솔직히 말해 현재로선 최선입니다". 이게 발표자의 정직성을 표시하고, 청중의 신뢰를 얻는다. 한국어 "솔직히"와 달리 영어 "frankly"는 비즈니스 회의에서 한계 인정과 함께 쓰인다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. SK와 NVIDIA 양쪽이 약점/불확실성을 어떻게 정중하게 포장하는지.

### 전략 1: 관심 탐색형 미루기 (Interest-Probing Deferral)

일정을 못 잡을 때, "관심 있으면 논의하자"로 미룬다. 직접 거부가 아니라 고객 의사를 탐색.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 샘플 일정 미확정 | "we haven't had any some specific schedule yet, but if you, if NVIDIA has some any interest to evaluate this kind of some samples, we can have some more discussion and we can fix some schedule for this kind of Buprachit SOCAM samples" | "구체 일정은 아직 없습니다만, NVIDIA에 평가 관심이 있으시면 더 논의해서 일정 잡을 수 있습니다" |

**패턴 공식**: `we haven't had any specific schedule yet, but if you have any interest to evaluate, we can have more discussion and we can fix some schedule.`

**Audrey 교훈**: "일정 못 잡겠다"를 직접 말하지 마라. "if you have any interest" - "관심 있으시면" - 이 조건부로 미룬다. 부담을 고객에게 넘기면서도 거부감 없이. 한국어 "스케줄 조정해 보겠습니다"의 훨씬 세련된 영어 버전이다.

### 전략 2: 정직한 자원 부족 인정 (Honest Resource Constraint)

"할 수 있다"가 아니라 "자원 없다"로 정직하게 거절한다. "we'd love to, but"이 핵심.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| NVIDIA "버퍼 칩 네가 설계할 거냐" 질문 | "we'd love to, but to be honest, we don't have the resources to design it. And I think NVIDIA is the best player. It's a great way to design it because NVIDIA already has C2C-5 and its own memory controller and 5." | "하고 싶지만 솔직히 자원이 없습니다. NVIDIA가 최적입니다. 이미 C2C-5와 메모리 컨트롤러가 있으니까요" |

**패턴 공식**: `we'd love to, but to be honest, we don't have the resources to X. I think Y is the best player. It's a great way because Y already has Z.`

**Audrey 교훈**: "we'd love to, but" - "하고 싶지만" - 이게 거절의 부드러운 시작이다. "we can't"이나 "we won't" 대신 "we'd love to, but"로 시작하면, 거절이 협업 제안으로 바뀐다. 그리고 "to be honest"로 정직함을 강조하고, "Y is the best player"로 상대방을 높여준다. 이 3단 거절-협업 전환 공식은 무조건 외워라.

### 전략 3: 제안을 "검토"로 미루기 (Polite "Will Look Into It")

NVIDIA가 SK 제안을 받고 즉시 답 안 할 때 쓰는 화법. "we can look into it"이 정중한 미루기.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| MSM 제안에 대한 NVIDIA 응답 | "Yeah, but thanks for the proposal. We can look into it." | "제안 감사합니다. 검토해 보겠습니다" |
| redriver 16.0 가능성 | "we will have a look and see if we think with the current redriver DQ only buffer to rank 16.0 is achievable. We will have a look and let you know." | "확인해 보고 가능한지 알려드리겠습니다" |

**패턴 공식**: `thanks for the proposal. we can look into it. / we will have a look and let you know.`

**Audrey 교훈**: "we can look into it" - "검토하겠습니다" - 가장 흔한 정중한 미루기다. "we will consider"보다 비격식적이고, "we will think about it"보다 전문가 느낌이다. 그리고 "we will have a look and let you know" - "확인해 보고 알려드리겠습니다" - 이게 다음 단계의 미루기다. 이 두 개를 상황에 따라 섞어 써라.

### 전략 4: 스펙 pushback - "목적"으로 반박 (Spec Pushback via Purpose)

상대방의 스펙 제안이不合理할 때, "원래 목적"을 들이밀어 정중하게 반박한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| NVIDIA가 작은 RX mask 요구 | "the main reason for why the buffer chip was adopted in the first place was to minimize the loading from the DRAM side, making the SOCAM to operate at its native die speed, right? But making the RX mask back smaller is basically just means the channel can be further degraded and that is not really the purpose of why buffer chip was first shown. So we think it is logical to at least have the same or similar or slightly better RX mask compared to the DRAM." | "버퍼 칩이 채택된 원래 목적은 DRAM 로딩을 줄이는 것이었습니다. RX mask를 작게 만들면 채널이 더 열화될 수 있는데, 이는 버퍼 칩의 목적이 아닙니다. DRAM과 같거나 약간 더 나은 RX mask가 논리적입니다" |

**패턴 공식**: `the main reason for why X was adopted in the first place was to Y, right? But Z means A can be B and that is not really the purpose. So we think it is logical to at least C.`

**Audrey 교훈**: "원래 목적"을 들이미는 게 가장 강력한 정중한 반박이다. "왜 이게 만들어졌는지"를 상기시키고, 상대의 제안이 그 목적에 반한다고 지적한다. "that is not really the purpose" - "그게 목적이 아닙니다" - 이게 polite하지만 단호한 거부다. "no"를 안 쓰면서 거부하는 화법.

### 전략 5: 우선순위 전환 (Priority Reframe)

상대 제안을 "큰 제약이 아니다"로 평가절하. NVIDIA가 SK 제안을 받을 때 자주 쓴다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| MSM 제안에 대한 NVIDIA | "our problem is fitting number of ESO-CAMs on the motherboard. That's the bigger constraint versus adding this new device that will make this module bigger. So I think that's the fundamental constraint." | "우리 문제는 메인보드에 얼마나 많은 SOCAM을 넣을지입니다. 새 디바이스 추가보다 큰 제약이죠. 이게 근본 제약입니다" |

**패턴 공식**: `our problem is X. That's the bigger constraint versus Y. So I think that's the fundamental constraint.`

**Audrey 교훈**: 상대 제안을 "큰 제약이 아니다"로 평가절하하는 화법이다. "versus"로 비교하면서, 상대 제안보다 다른 문제가 더 크다고 프레이밍. "fundamental constraint" - "근본 제약" - 이 단어가 우선순위를 명확히 한다. 한국어 "그것보다 이게 더 중요합니다"의 영어 버전.

### 전략 6: 조건부 검토 제안 (Conditional Evaluation Offer)

채널 모델을 받으면 더 평가하겠다는 조건부 제안. 책임을 NVIDIA에게 넘기면서도 협조적.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| SI 결과에 대한 SK | "So I guess we don't have your LPSYS channel models yet, but if you can share that to us, we could further evaluate, also see what the channel is actually capable of. Yeah, and we can update the numbers based on that" | "LPSYS 채널 모델이 아직 없는데, 공유해 주시면 더 평가할 수 있고, 채널이 실제로 어디까지 가능한지 볼 수 있습니다. 그 기반으로 숫자 업데이트 가능합니다" |

**패턴 공식**: `if you can share X to us, we could further evaluate, also see what Y is actually capable of. we can update Z based on that.`

**Audrey 교훈**: "if you can share X, we could further evaluate" - "공유해 주시면 더 평가하겠습니다" - 책임을 상대에게 넘기면서도 적극적으로 들리는 화법. "could"를 쓰면 더 정중하다. "we can"보다 "we could"가 더 조건부 뉘앙스.

---

## 3. 정중한 도전 화법 (NVIDIA/SK 질문자)

양쪽이 기술적으로 도전하면서도 정중하게 질문하는 패턴.

### 질문 유형 1: 확인형 질문 (Confirmation Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `you mean the X?` | "You mean the buffer die in the LPDDR package?" | 짧은 확인 - 발표 흐름 끊지 않음 |
| `so in this proposal, do you plan to design that X?` | "So in this proposal, do you plan to design that buffer chip?" | 직접적 의도 탐색 |
| `and you're saying this will run without buffer?` | "And you're saying this will run without buffer?" | 확인 - "맞습니까" |

**Audrey 교훈**: "you mean X?" - 짧은 확인 질문은 발표자가 쉽게 대답할 수 있다. 발표 흐름을 끊지 않으면서 핵심을 확인하는 화법. 회의에서 발표자가 말할 때, 꼭 확인하고 싶은 건 "you mean X?"로 짧게 물어라.

### 질문 유형 2: 속도 타겟 탐색 (Speed Target Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `what's the speed you are targeting without the X?` | "What's the speed you are targeting without the base die buffer?" | 타겟 탐색 - "목표가 뭡니까" |
| `how fast do you think we can run?` | "between this logic device and your stack, your four packages, how fast do you think we can run?" | "얼마나 빠르게 가능합니까" |

**Audrey 교훈**: "what's the speed you are targeting" - "타겟 속도가 어떻게 됩니까" - 스펙 질문의 표준 화법이다. "targeting"을 쓰면, "목표"를 물으므로 발표자가 여유 있게 답할 수 있다. "how fast can we run"도 비격식적이고 협력적.

### 질문 유형 3: 부드러운 반대 (Soft Disagreement)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I do understand X, but Y` | "I mean, I do understand that because with the buffer we can pump up the voltage. That is true, but I mean, like just to the fundamentals, the main reason for why the buffer chip was adopted in the first place was to..." | "이해합니다. 맞습니다. 하지만 본질적으로..." |
| `we were a bit worried that X, but it's good to hear that Y is okay` | "we were a bit worried that it's good to hear them videos okay but maybe other SOCs might have a problem" | "걱정했는데 다행입니다" - 우려 표시 |

**Audrey 교훈**: "I do understand X. That is true, but..." - "이해합니다. 맞지만" - 반대하기 전에 상대 주장을 먼저 인정하는 화법. "do understand"와 "That is true"로 상대를 인정하고, "but"로 전환. 한국어 "맞습니다, 그런데요"의 영어 버전인데, 영어는 "That is true"로 한 번 더 인정한다.

### 질문 유형 4: 핵심 제약 질문 (Fundamental Constraint Question)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think that's the fundamental constraint` | "So I think that's the fundamental constraint" | 제약 선언 - 직접적 |
| `I'm not sure this really is...` | "So I'm not sure this really is..." | 회의적 표시 - 정중한 부정 |

**Audrey 교훈**: "I think that's the fundamental constraint" - "근본 제약입니다" - 회의에서 자기 의견을 단호하게 표시하는 화법. "I think"로 의견임을 표시하고, "fundamental constraint"로 격상. 직접적이면서도 "I think"로 부드럽게.

### 질문 유형 5: 자원 부족 정직 인정 (Honest Limitation Acknowledgment)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we'd love to, but to be honest, we don't have the resources` | "we'd love to, but to be honest, we don't have the resources to design it" | 정직한 거절 |
| `I'm not sure this really is...` | (SK 발표자가 자기 제안에 대해) "So I'm not sure this really is..." | 자기 제안에 대한 회의 |

**Audrey 교훈**: "we'd love to, but to be honest, we don't have the resources" - "하고 싶지만 솔직히 자원이 없습니다" - 정직한 거절의 황금 공식. "I don't want to"가 아니라 "we'd love to"로 시작해서 "but to be honest"로 정직함 강조. 이게 신뢰를 유지하면서 거절하는 유일한 방법이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 핵심. Section 4를 가장 깊이 분석한다.

### 타임라인 표시 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 확정 타임라인 | SK | "we plan to have some the 5-carbicabit RPC SOCAM with the Buprachit. So the timeline would be a 2027 next year, the course quarter" | "we plan to / the timeline would be" |
| 샘플 타임라인 | SK | "This will ready for yours in the module CS level... we already have the schedule maybe this 2027 quarter one and quarter two" | "we already have the schedule" |
| 스펙 타임라인 | SK | "we plan to bring this to the committee soon" | action item |
| 조건부 타임라인 | SK | "we haven't had any specific schedule yet, but if you have any interest to evaluate, we can have more discussion" | 조건부 |
| 다음 단계 미루기 | NVIDIA | "we will have a look and let you know" | 부드러운 미루기 |

### 볼륨/샘플 요청 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 요청 | SK | "if NVIDIA has some any interest to evaluate this kind of some samples, we can have some more discussion and we can fix some schedule for this kind of Buprachit SOCAM samples" | 관심 탐색형 |
| 시스템 제공 요청 | SK | "if NVIDIA has a plan to provide us the system in early stage at first" | "plan to provide us X" |
| 실험 바이오스 요청 | SK | "if I can request you some experimental bios, can we see the CE logs? Do you prepare for that experiment?" | "can we see X" - 직접 요청 |
| 평가 결과 공유 요청 | SK | "Please check if that correlates with your internal results. With your internal results as well." | "please check if X correlates with Y" |
| 채널 모델 공유 요청 | SK | "if you can share that to us, we could further evaluate" | "if you can share X, we could Y" |
| 시스템 제공 의향 | NVIDIA | "we're obviously building a lot of. A lot of the teams. We can take the data back to the." | (불완전하지만 긍정) |

### 스펙 pushback 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 비실용 선언 | SK | "Maybe 16 kFPS is... We don't think it's feasible with the current architecture, so maybe we have to find some other way to achieve over 16 kFPS speed with the buffer chip" | "we don't think it's feasible" |
| 대안 제시 | SK | "we need some other type like retimer, different architecture" | "we need some other type like X" |
| 한계 인정 | SK | "this is frankly the best we can do at the moment with the current modulate note" | "frankly the best we can do" |
| 목적 반박 | SK | "that is not really the purpose of why buffer chip was first shown. So we think it is logical to at least have the same or similar" | "not really the purpose" |
| 제안 미루기 | NVIDIA | "we will have a look and see if we think X is achievable" | "we will have a look" |
| 제약 선언 | NVIDIA | "I think that's the fundamental constraint" | "fundamental constraint" |

### 마일스톤 조정 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 일정 변경 통보 | SK | "We haven't had any some specific schedule yet, but if you, if NVIDIA has some any interest..." | 일정 미확정 |
| revision 상태 | SK | "Nowadays the spag is revision 0.5 not fixed 0.7. We are playing a strategy is ready to the 0.5 sample and working sample" | revision 상태 표시 |
| "under consideration" | SK | "we are still under investigation for this kind of some pro planning with the materials" | "under investigation" |
| "aligned with X" 표현 | SK | "our main focus is now on the period from 28 to 231" | 기간 포커스 명시 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| committee 제출 | SK | "we plan to bring this to the committee soon" | "bring to the committee" |
| 후속 액션 | SK | "we will have a look and let you know" | "have a look and let you know" |
| 피드백 요청 | SK | "please give us the feedback if during the committee maybe if possible" | "please give us the feedback" |
| 공동 개발 제안 | SK | "we are collaborating on the code development of the BMC-based model" | "collaborating on X" |
| 후속 채널 | SK | "during our discussion, if any question comes up, we will reach out via email" | "reach out via email" |
| 파트너 협업 | SK | "we can work with your partners" | "work with your partners" |

**Audrey 교훈**:
- "we plan to bring this to the committee soon" - "committee"에 제출하겠다는 action item. 회의록에 명시되면 다음 회의에서 결과가 나온다.
- "we will have a look and let you know" - NVIDIA가 SK 제안을 받을 때 쓰는 미루기. "let you know"가 후속 액션 명시.
- "if any question comes up, we will reach out via email" - 후속 채널 명시 공식. 회의 끝에 꼭 써라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 GDDR/MRDIMM/LPDDR6/CXL 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **GDDR7 (G7)** | 그래픽 DDR 7세대 | "the supportable scope based on the G7 based on the 1D nanometer has reached its limits" - "G7 한계 선언" |
| **1D nanometer** | 다음 세대 공정 노드 | "based on the 1D nanometer process node" - 공정 명시 |
| **bandwidth** | 대역폭 | "bandwidth at least 144 and nearly 160 gigabyte per second" - 스펙 명시 |
| **system guardband** | 시스템 여유분 | "each of the speed should include at least 5% or even more than 10%" - "guardband"로 여유 표시 |
| **MRDIMM** | Multi-Rank DIMM | "the buffer chip design, we don't think it supports 16 kFPS" - MRDIMM 버퍼 칩 한계 |
| **redriver / retimer** | 신호 재구동 칩 | "we need some other type like retimer, different architecture" - redriver 한계, retimer 대안 |
| **SOCAM** | Small Outline CAM (LPDDR 모듈) | "the PCB size and the DM package size and the PCB thickness" - 모듈 스펙 |
| **RPC SOCAM** | Reduced Pin Count SOCAM | "we plan to have some the 5-carbicabit RPC SOCAM with the Buprachit" - 신제품 타임라인 |
| **Buprachit** | (버퍼 칩 코드명) | "the timeline would be a 2027 next year" - 신제품 일정 |
| **buffer chip** | 신호 완화 버퍼 | "the main reason for why the buffer chip was adopted in the first place was to minimize the loading" - 목적 설명 |
| **TWCK2DQ** | WCK-to-DQ 지연 | "TWC kick to DQ I becomes a negative" - 스펙 논의 |
| **RX mask** | 수신 눈 마스크 | "we want to keep a similar RX mask" - 스펙 pushback |
| **TDIVW / VDIVW** | Data Invalid Window | "we are expecting roughly about 0.08 UI buffer budget in terms of TDIVW" - 버퍼 예산 |
| **UI (Unit Interval)** | 비트 시간 단위 | "0.08 UI buffer budget" - 단위 |
| **ZQ Cal** | ZQ 캘리브레이션 | "TZQ Cal 32 is 18 microseconds, but with the four additional buffers, the NZQ numbers actually becomes 36" - 캘리브레이션 시간 |
| **fly by concept** | CK 비행 설계 | "due to the fly by concept of the CK, we see some inevitable WCK2CK gap" - 설계 개념 |
| **MSM (Memory Solution Module)** | SK 제안 메모리 모듈 | "It features a large package mounted on a pluggable module like a SOCAM" - 제품 설명 |
| **C2C / NVLink C2C** | Chip-to-Chip 인터페이스 | "the controller die in the middle consists of memory files, memory controllers, and C2C5 for the connection to the XPU" - 아키텍처 |
| **MRM (Memory Reliability Module)** | SK 메모리 신뢰성 솔루션 | "we developed the memory solution. We proposed some memory which is one of the reading cause of a system failure" - 제품 프레이밍 |
| **DFA (DRAM Fault Analyzer)** | SK 고장 분석기 | "our DLN portal analyzer begins deep analysis" - 도구 설명 |
| **SPPR / HPPR** | Soft/Hard Post Package Repair | "we suggest SPPR during runtime and inspect HPPR to run at the next boot time" - 복구 전략 |
| **bank sparing** | 뱅크 예비 전환 | "we propose bank sparing as the last section, which is comparable to in-pass ADDC technology" - 비교 |
| **page offlining** | 페이지 격리 | "we proceed with recovery by isolating the impacted region from the system using a method called page apply" - 복구 |
| **BMC (Baseboard Management Controller)** | 서버 관리 칩 | "BMC remains unaffected and continues to run" - 독립성 강조 |
| **CE (Correctable Error) / UE (Uncorrectable Error)** | 에러 분류 | "we can report multi-bed CE" - 정책 |
| **PFA (Post Failure Analysis)** | 사후 고장 분석 | "we performed PFA on many more units in Q2" - 품질 활동 |
| **gate angel short** | 게이트 단락 결함 | "gate angel short is 33%, and angel bridge is 23%" - 결함 분류 |
| **EFR (Early Failure Rate)** | 초기 고장률 | "the EFR index has maintained 0 PPM" - 품질 지표 |
| **PPM** | Parts Per Million | "the result is the 48 PPM" - 단위 |
| **CXL pooled memory** | CXL 풀드 메모리 | "we are partially replace existing GPU servers with the CXL pulled memory" - 사용 사례 |
| **RDMA over PCIe** | PCIe 기반 RDMA | "they are considering using the remote RDMA over the lock key" - 연결 옵션 |
| **Dynamo** | AI 인프라 | "It's learning on top of the Dynamo and we also have the good evaluation number" - SW 스택 |
| **LPSYS** | (NVIDIA 시스템) | "we don't have your LPSYS channel models yet" - NVIDIA 자산 |
| **Rosa** | (NVIDIA 시스템) | "system delivery of Rosa in only phase and qualification phase and finally mass production phase" - 시스템 |
| **NVL72** | (NVIDIA 랙) | "120 terabyte of memory capacity and the CXL pulled server is equivalent to one MVL72 rack" - 비교 |
| **capex** | 자본 지출 | "capex drops by 12%" - 비용 절감 |
| **tape out** | 설계 완료 | "we just decided to have this silicon in 2027" - 일정 |
| **engineering sample / ES** | 엔지니어링 샘플 | "the system level pre-evaluation is essential" - 샘플 중요성 |
| **CS / MP** | Characterization Sample / Mass Production | "system delivery of Rosa in only phase and qualification phase and finally mass production phase" - 단계 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 55개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m04-001
  expression: "this one just summarizes some technical demand or some requirements for X by era"
  category: presentation_framing
  function: demand_framing
  speaker_role: presenter
  difficulty: 4
  context: "this one just summarizes some technical demand or some requirements for GDDR memory by era and describes what our lineup have evolved to address them"
  note: 로드맵 발표의 시작 - "요구부터 프레이밍" 공식

- id: m04-002
  expression: "so to address those demand, we just decided to have X in Y"
  category: solution_reveal
  function: demand_to_product
  speaker_role: presenter
  difficulty: 4
  context: "So to address those demand, we just decided to have this silicon in 2027"
  note: "to address those demand" - 요구 해결 명시. 로드맵 발표 공식

- id: m04-003
  expression: "the supportable scope based on X has reached its limits"
  category: limit_declaration
  function: ceiling_acknowledgment
  speaker_role: presenter
  difficulty: 5
  context: "the supportable scope based on the G7, I mean, based on the 1D nanometer, has reached its limits"
  note: 한계 선언 - "더 이상 못 함" 명시. 다음 세대 제안의 도입부

- id: m04-004
  expression: "if there is some kind of X, we would like to say that some kind of Y might be required"
  category: next_gen_proposal
  function: conditional_future
  speaker_role: presenter
  difficulty: 5
  context: "if there is some kind of speed requirement beyond 2030, we would like to say that some kind of the next generation product might be required"
  note: "would like to say that might be required" - 이중 완곡한 미래 제안

- id: m04-005
  expression: "this is our core message"
  category: emphasis
  function: key_point_flag
  speaker_role: presenter
  difficulty: 3
  context: "actually this is core message from us"
  note: 핵심 메시지 표시 - "이게 핵심이다" 명시

- id: m04-006
  expression: "let me move on next"
  category: self_transition
  function: slide_advance
  speaker_role: presenter
  difficulty: 2
  context: "Let me move on next speech."

- id: m04-007
  expression: "do I have any questions?"
  category: question_invitation
  function: slide_end_check
  speaker_role: presenter
  difficulty: 2
  context: "And do I have any questions?"

- id: m04-008
  expression: "could you move on to the next page?"
  category: flow_request
  function: advance_request
  speaker_role: questioner
  difficulty: 2
  context: "Could you move on to the next page?"
  note: 발표자에게 다음 슬라이드 요청 - 정중한 흐름 통제

- id: m04-009
  expression: "please ask anytime feel free"
  category: open_invitation
  function: anytime_questions
  speaker_role: presenter
  difficulty: 3
  context: "So please ask anytime feel free."

- id: m04-010
  expression: "let me start with the background"
  category: framing
  function: context_setting
  speaker_role: presenter
  difficulty: 3
  context: "Let's start with the background."

# ── 타임라인 표시 (Timeline Specification) ──
- id: m04-011
  expression: "we plan to have X, so the timeline would be Y"
  category: timeline_stating
  function: schedule_declaration
  speaker_role: presenter
  difficulty: 4
  context: "we plan to have some the 5-carbicabit RPC SOCAM with the Buprachit. So the timeline would be a 2027 next year, the course quarter"
  note: 타임라인 명시 공식 - "we plan to" + "the timeline would be"

- id: m04-012
  expression: "we already have the schedule maybe this X quarter one and quarter two"
  category: schedule_confirmed
  function: firm_timeline
  speaker_role: presenter
  difficulty: 3
  context: "We already have the schedule maybe this 2027 quarter one and quarter two"

- id: m04-013
  expression: "we haven't had any specific schedule yet, but if you have any interest to evaluate, we can have more discussion"
  category: conditional_schedule
  function: interest_probing_deferral
  speaker_role: presenter
  difficulty: 5
  context: "we haven't had any some specific schedule yet, but if you, if NVIDIA has some any interest to evaluate this kind of some samples, we can have some more discussion and we can fix some schedule"
  note: 관심 탐색형 미루기 - 핵심 화법

- id: m04-014
  expression: "we plan to bring this to the committee soon"
  category: action_item
  function: committee_submission
  speaker_role: presenter
  difficulty: 3
  context: "Yeah, so we plan to bring this to the committee soon."
  note: "bring to the committee" - action item 공식

- id: m04-015
  expression: "we will have a look and let you know"
  category: soft_commitment
  function: polite_deferral
  speaker_role: partner
  difficulty: 3
  context: "We will have a look and see if we think with the current redriver DQ only buffer to rank 16.0 is achievable. We will have a look and let you know."
  note: NVIDIA의 정중한 미루기 - "let you know"가 후속 명시

- id: m04-016
  expression: "we can look into it"
  category: soft_commitment
  function: consideration_deferral
  speaker_role: partner
  difficulty: 2
  context: "Yeah, but thanks for the proposal. We can look into it."
  note: 가장 흔한 정중한 미루기

# ── 회피·포장 (Hedging & Deflection) ──
- id: m04-017
  expression: "we'd love to, but to be honest, we don't have the resources to X"
  category: honest_refusal
  function: resource_constraint_admission
  speaker_role: presenter
  difficulty: 5
  context: "we'd love to, but to be honest, we don't have the resources to design it. And I think NVIDIA is the best player"
  note: 정직한 거절의 황금 공식 - "we'd love to" + "to be honest" + partner 칭찬

- id: m04-018
  expression: "this is frankly the best we can do at the moment with the current X"
  category: limitation_admission
  function: honest_ceiling
  speaker_role: presenter
  difficulty: 5
  context: "this is frankly the best we can do at the moment with the current modulate note"
  note: "frankly"로 정직함 강조 - 한계 인정 공식

- id: m04-019
  expression: "we don't think it's feasible with the current architecture"
  category: spec_pushback
  function: infeasibility_declaration
  speaker_role: presenter
  difficulty: 4
  context: "Maybe 16 kFPS is... We don't think it's feasible with the current architecture, so maybe we have to find some other way"
  note: "we don't think"로 정중한 비실용 선언

- id: m04-020
  expression: "we need some other type like X, different architecture"
  category: alternative_proposal
  function: alternative_after_pushback
  speaker_role: presenter
  difficulty: 4
  context: "we need some other type like retimer, different architecture"
  note: 부정 뒤 대안 제시 - "some other type like X"

- id: m04-021
  expression: "we are still under investigation for this kind of X"
  category: status_hedging
  function: ongoing_research
  speaker_role: presenter
  difficulty: 3
  context: "we are still under investigation for this kind of some pro planning with the materials"
  note: "under investigation" - 진행 중 표시

- id: m04-022
  expression: "thanks for the proposal, we can look into it"
  category: polite_reception
  function: appreciation_deferral
  speaker_role: partner
  difficulty: 3
  context: "Yeah, but thanks for the proposal. We can look into it."
  note: 제안 받아줄 때 - "thanks" + "look into"

- id: m04-023
  expression: "I think that's the fundamental constraint"
  category: priority_declare
  function: root_constraint
  speaker_role: partner
  difficulty: 4
  context: "So I think that's the fundamental constraint."
  note: NVIDIA가 우선순위 명시 - "fundamental constraint"

- id: m04-024
  expression: "our problem is X. That's the bigger constraint versus Y"
  category: priority_reframe
  function: priority_shift
  speaker_role: partner
  difficulty: 5
  context: "our problem is fitting number of ESO-CAMs on the motherboard. That's the bigger constraint versus adding this new device"
  note: 상대 제안 평가절하 - "versus"로 비교

- id: m04-025
  expression: "the main reason for why X was adopted in the first place was to Y, right?"
  category: purpose_recall
  function: original_intent
  speaker_role: presenter
  difficulty: 5
  context: "the main reason for why the buffer chip was adopted in the first place was to minimize the loading from the DRAM side, making the SOCAM to operate at its native die speed, right?"
  note: 원래 목적 상기 - "in the first place"로 강조

- id: m04-026
  expression: "that is not really the purpose of why X was first shown"
  category: polite_refutation
  function: purpose_violation
  speaker_role: presenter
  difficulty: 5
  context: "that is not really the purpose of why buffer chip was first shown"
  note: "no" 안 쓰는 거부 - "not really the purpose"

- id: m04-027
  expression: "we were a bit worried that X, but it's good to hear that Y"
  category: relief_express
  function: worry_to_relief
  speaker_role: presenter
  difficulty: 4
  context: "we were a bit worried that it's good to hear them videos okay but maybe other SOCs might have a problem"
  note: 우려-안도 표시 - "good to hear"

# ── 정중한 도전 (Polite Challenge) ──
- id: m04-028
  expression: "you mean the X?"
  category: quick_confirm
  function: brief_clarification
  speaker_role: questioner
  difficulty: 2
  context: "You mean the buffer die in the LPDDR package?"

- id: m04-029
  expression: "so in this proposal, do you plan to X?"
  category: intent_probe
  function: direct_plan_question
  speaker_role: questioner
  difficulty: 3
  context: "So in this proposal, do you plan to design that buffer chip?"

- id: m04-030
  expression: "and you're saying this will run without X?"
  category: confirmation_probe
  function: claim_confirm
  speaker_role: questioner
  difficulty: 3
  context: "And you're saying this will run without buffer?"

- id: m04-031
  expression: "what's the speed you are targeting without X?"
  category: spec_probe
  function: target_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "What's the speed you are targeting without the base die buffer?"

- id: m04-032
  expression: "how fast do you think we can run?"
  category: capability_probe
  function: feasibility_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "between this logic device and your stack, your four packages, how fast do you think we can run?"

- id: m04-033
  expression: "I do understand X, but Y"
  category: soft_disagreement
  function: acknowledge_then_challenge
  speaker_role: questioner
  difficulty: 5
  context: "I mean, I do understand that because with the buffer we can pump up the voltage. That is true, but I mean, like just to the fundamentals..."
  note: 반대 전 상대 인정 - "do understand" + "That is true"

- id: m04-034
  expression: "I'm not sure this really is..."
  category: skeptical_hedge
  function: polite_doubt
  speaker_role: presenter
  difficulty: 4
  context: "So I'm not sure this really is..."

- id: m04-035
  expression: "if you can share X to us, we could further evaluate"
  category: conditional_request
  function: collaborative_eval
  speaker_role: presenter
  difficulty: 4
  context: "if you can share that to us, we could further evaluate, also see what the channel is actually capable of"
  note: 조건부 협업 제안 - "could"로 더 정중

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m04-036
  expression: "if NVIDIA has some any interest to evaluate, we can have more discussion"
  category: interest_probe
  function: collaborative_open
  speaker_role: presenter
  difficulty: 4
  context: "if you, if NVIDIA has some any interest to evaluate this kind of some samples, we can have some more discussion"

- id: m04-037
  expression: "if NVIDIA has a plan to provide us X in early stage"
  category: sample_request
  function: direct_sample_ask
  speaker_role: presenter
  difficulty: 4
  context: "if NVIDIA has a plan to provide us the system in early stage at first"

- id: m04-038
  expression: "if I can request you some experimental X, can we see Y?"
  category: experiment_request
  function: pilot_ask
  speaker_role: presenter
  difficulty: 4
  context: "If I can request you some experimental bios, can we see the CE logs?"

- id: m04-039
  expression: "please check if that correlates with your internal results"
  category: validation_request
  function: cross_check
  speaker_role: presenter
  difficulty: 3
  context: "Please check if that correlates with your internal results."

- id: m04-040
  expression: "we are collaborating on the code development of X"
  category: collaboration_stating
  function: joint_dev
  speaker_role: presenter
  difficulty: 4
  context: "we are collaborating on the code development of the BMC-based model"

- id: m04-041
  expression: "during our discussion, if any question comes up, we will reach out via email"
  category: follow_up_channel
  function: contact_commitment
  speaker_role: negotiator
  difficulty: 3
  context: "during our discussion, if any question comes up, we will reach out via email"

- id: m04-042
  expression: "we can work with your partners"
  category: partner_collab
  function: extended_collaboration
  speaker_role: negotiator
  difficulty: 3
  context: "Yeah, we can work with your partners."

- id: m04-043
  expression: "please give us the feedback if during the committee maybe if possible"
  category: feedback_request
  function: input_ask
  speaker_role: presenter
  difficulty: 3
  context: "please give us the feedback if during the committee maybe if possible"

- id: m04-044
  expression: "the reason why we are developing X is because of you, you know that, right?"
  category: subtle_pressure
  function: accountability_recall
  speaker_role: negotiator
  difficulty: 5
  context: "the reason that we are developing LTPs is that 60, you know, 32 gigabit in that timeline is because of you. You know that, right?"
  note: 부드러운 압박 - "because of you" + "you know that, right?" - 위험하지만 효과적

- id: m04-045
  expression: "this is a natural starting point for that discussion"
  category: validation
  function: proposal_endorse
  speaker_role: partner
  difficulty: 4
  context: "Yeah, I think this is a natural starting point for that discussion."

- id: m04-046
  expression: "at a high level, we have similar views on X"
  category: alignment_stating
  function: agreement_signal
  speaker_role: partner
  difficulty: 4
  context: "Yeah, I think at a high level, we have similar views on G7."

- id: m04-047
  expression: "so far, it's what I have today right now"
  category: status_close
  function: presentation_end
  speaker_role: presenter
  difficulty: 3
  context: "So far, it's what I have today right now."

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m04-048
  expression: "the supportable scope based on X has reached its limits"
  category: limit_stating
  function: tech_ceiling
  speaker_role: presenter
  difficulty: 4
  context: "the supportable scope based on the G7 based on the 1D nanometer has reached its limits"

- id: m04-049
  expression: "according to the system guardband that X requires"
  category: spec_compliance
  function: requirement_ref
  speaker_role: presenter
  difficulty: 4
  context: "according to the system guardband that NVIDIA requires, each of the speed should include at least 5% or even more than 10%"

- id: m04-050
  expression: "we want to keep X as is, but we just want to release Y"
  category: spec_negotiation
  function: keep_and_request
  speaker_role: presenter
  difficulty: 4
  context: "we want to keep the TWCK2CK offset spec as is, but we just want to reduce the amount of time... we just want to ask for a bigger sweep range during training"
  note: 스펙 협상 - "keep X, ask for Y"

- id: m04-051
  expression: "the main reason for why X was adopted in the first place"
  category: purpose_recall
  function: original_intent
  speaker_role: presenter
  difficulty: 4
  context: "the main reason for why the buffer chip was adopted in the first place was to minimize the loading from the DRAM side"

# ── 발화 채움 표현 (Discourse Markers) ──
- id: m04-052
  expression: "so just to recap what we've discussed"
  category: recap
  function: summary_transition
  speaker_role: presenter
  difficulty: 3
  context: "So just to recap what we've discussed."

- id: m04-053
  expression: "as I mentioned before"
  category: back_reference
  function: prior_recall
  speaker_role: presenter
  difficulty: 2
  context: "as I mentioned before, the enough space to put that six-step memory system in the GPU lag"

- id: m04-054
  expression: "let me comment one thing"
  category: interjection
  function: polite_insert
  speaker_role: presenter
  difficulty: 3
  context: "So, so, so, Hayoung, so let me, let me, let me comment one thing."

- id: m04-055
  expression: "the purpose of this proposal is very simple, right?"
  category: simplification
  function: complexity_reduction
  speaker_role: presenter
  difficulty: 4
  context: "we can, we can remove the best thousands of numbers, but anyhow, we had a lot of, the purpose of this proposal is very simple, right?"
  note: 복잡한 제안을 "simple"로 정리 - 청중 이해 돕기
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-08-13 15 38 50_EN_NVIDIA_2H-extracted.wav` (총 ~90분, 10,197단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | GDDR 로드맵 (line 40-60) | "to address those demand, we decided to X in 2027" + "G7 reached its limits" | 요구 프레이밍 + 한계 선언 + 타임라인 명시 | ★★★ |
| 2 | MRDIMM 버퍼 한계 (line 84-88) | "we don't think it's feasible with the current architecture" + "we need some other type like retimer" | 스펙 pushback + 대안 제시 | ★★★★ |
| 3 | 스펙 pushback - 목적 반박 (line 289-292) | "the main reason for why buffer chip was adopted... that is not really the purpose" | "목적"으로 정중하게 반박 | ★★★★ |
| 4 | MSM 자원 부족 인정 (line 434-437) | "we'd love to, but to be honest, we don't have the resources... NVIDIA is the best player" | 정직한 거절 + 파트너 칭찬 | ★★★★ |
| 5 | LPDDR6 샘플 요청 협상 (line 663-700) | "system delivery of Rosa in dev/qual/MP phase" + "we can send the better samples to NVIDIA" | 샘플 요청 + 협상 양보 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 정직한 거절 + 협상 양보 화법이 밀집
- 발췌 3은 가장 정치적으로 민감한 "목적 반박" 화법

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **multi-presenter roadmap pitch + customer constraint feedback** register다. 6명 이상의 SK 발표자가 연달아 제안하고, NVIDIA가 제약/관심도를 피드백하는 구조. 두 역할 모두 학습해야:
- **SK 발표자 역할**: 요구 프레이밍, 타임라인 명시, 한계 인정, 정중한 거절 - 네가 NVIDIA에 로드맵 밀 때
- **NVIDIA 역할**: 관심 표시, 제약 선언, 제안 미루기, 우선순위 전환 - 네가 파트너 제안 받을 때

### Pragmatics (화용론) 핵심
1. **"we'd love to, but to be honest"**: 정직한 거절의 황금 공식. "no"를 안 쓰면서 거절. "we'd love to"로 의지 표시, "to be honest"로 정직함, 그리고 partner 칭찬으로 협력 의지 유지.
2. **"frankly the best we can do at the moment"**: 한계 인정의 정직함. "frankly"가 비즈니스 회의에서 신뢰를 만드는 단어. 한국어 "솔직히"보다 비즈니스 맥락에서 더 강력.
3. **"that is not really the purpose"**: "no"를 안 쓰는 거부. "목적"을 들이밀어 상대 제안이 본래 의도에 반한다고 지적. 가장 정치적인 정중한 반박.
4. **"we will have a look and let you know"**: NVIDIA의 정중한 미루기. "let you know"가 후속 액션 명시 - 단순 "we'll think about it"보다 책임감 있게 들림.
5. **"if you have any interest to evaluate, we can have more discussion"**: 관심 탐색형 미루기. 책임을 고객에게 넘기면서도 거부감 없이. 로드맵 제안의 핵심 화법.

### 네가 당장 써야 할 Top 5
1. **"we'd love to, but to be honest, we don't have the resources"** - 정직한 거절
2. **"this is frankly the best we can do at the moment"** - 한계 인정
3. **"the main reason for why X was adopted in the first place... that is not really the purpose"** - 목적 반박
4. **"we will have a look and let you know"** - 정중한 미루기
5. **"to address those demand, we decided to X in Y"** - 로드맵 발표 공식

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "검토해 보겠습니다" | "we will have a look and let you know" | "let you know"가 후속 명시 |
| "솔직히 최선입니다" | "this is frankly the best we can do at the moment" | "frankly"가 정직함 강조 |
| "하고 싶지만 자원이 없습니다" | "we'd love to, but to be honest, we don't have the resources" | "we'd love to"로 의지 표시 |
| "그게 목적이 아닙니다" | "that is not really the purpose" | "not really"로 부드럽게 |
| "그건 근본 제약입니다" | "I think that's the fundamental constraint" | "I think"로 의견 표시 |
| "관심 있으시면 논의하죠" | "if you have any interest to evaluate, we can have more discussion" | "interest to evaluate"로 구체화 |
| "이 요구에 맞춰 설계했습니다" | "to address those demand, we decided to X" | "address those demand"로 연결 |
| "다음에 알려드리겠습니다" | "we will have a look and let you know" | "have a look"이 더 구체적 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 55개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 4절 협상 화법(특히 정직한 거절·스펙 pushback) 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **역할별 학습**: SK 발표자 화법(1·2절)과 NVIDIA 고객 화법(3·4절)을 번갈아 연습

---

*Textbook 04 - NVIDIA 2H (2026-08-13). 회의 유형 B (Roadmap/Supply Alignment). 표현 DB 55개. 5개 발췌 구간. 작성: 2026-09-01.*
