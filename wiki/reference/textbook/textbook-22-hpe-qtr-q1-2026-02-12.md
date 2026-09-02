---
textbook_id: 22
meeting: HPE QTR Q1
date: 2026-02-12
type: B (roadmap/supply alignment)
partner: HPE (Eric, Dan, Stuart, Michael, Dennis)
sk_side: Doyeon Kim (DDR5 roadmap), Steve Gu (CXL/HMSDK), Jerry, Yongjun, Soh (SOCAM)
duration_words: 10507
audio: repo/webex-audio/2026-02-12 09 34 28_EN_HPE_QTR_Q1-extracted.wav
transcript: repo/webex-audio/2026-02-12 09 34 28_EN_HPE_QTR_Q1-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, hpe, qbr, ddr5, ddr6, mrdim, socam, cxl, roadmap, supply-alignment, ecc, sddc]
---

# Textbook 22 - HPE QTR Q1 (2026-02-12)

> **회의 유형**: B (Roadmap/Supply alignment) - 분기 단위 QBR, SK하이닉스가 로드맵/샘플/양산 일정을 발표하고 HPE가 기술적 타당성·스케줄·스펙 의견 제시
> **학습 가치**: 로드맵 발표자의 "timeline target + recommendation" 구조, HPE의 정중한 가정 도전, 포지션 보류/확정 협상 화법, action item의 유머러스한 수용
> **Audrey 관점**: 이 회의는 "로드맵 pitch + 스펙 협상 + 포지션 조율"의 전형 - Type B에서 Section 4(협상)가 핵심이지만, Microsoft 제안 도전 부분은 Type A급 도전 화법의 보석이 섞여 있다. 둘 다 배워야.

---

## 1. 발화 아키텍처 - Doyeon의 로드맵 발표 설계 (6단계)

Doyeon Kim은 분기 로드맵을 발표할 때 6단계 고정 구조를 사용한다. 이게 네가 매분기 HPE에 보고할 때 그대로 쓸 수 있는 "로드맵 발표의 뼈대"다.

### 단계 1: 변경점 프레이밍 (What's New Framing)

로드맵 전체를 반복하지 않고, "지난번과 같은데 한 가지 다른 점"으로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the all the contents is all the same except X` | "the all the contents is all the same except 24 gigabits" | 변경점 단일화 - 청중의 주의 집중 |
| `So, let's touch more detail.` | "So, let's touch more detail." | 깊이 들어가겠다는 전환 신호 |
| `Actually, I share the X last week.` | "Actually, I share the Q1 short term world map last week." | 사전 공유 언급 - 중복 회피 |

**Audrey 교훈**: 분기 로드맵을 발표할 때 "모든 걸 다시 설명"하지 마라. "지난번과 같은데 X만 다릅니다"로 시작하면, 청중은 변경점에 주의를 집중한다. 이게 로드맵 발표의 첫 공식이다. 한국어 "지난번과 동일하고요, 한 가지만 말씀드리면"의 영어 버전이 "the contents is all the same except X"다.

### 단계 2: 기술 노드 전환 (Tech Node Transition)

"현재 1anm, 2H 2026부터 1Cnm"로 노드 마이그레이션을 명시.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `our main technology is right now is X` | "our main technology is right now is 1anm" | 현재 상태 명시 |
| `from second half, 2026, our main technology will be X` | "from second half, 2026, we our main technology will be 1C nanometer" | 전환 시점 명시 |
| `we deliver to HPE to process sustaining work with our X` | "we deliver to HPE to process sustaining work with our 1C nanometer" | HPE 작업 유형 연결 (sustaining) |

**Audrey 교훈**: 기술 노드 마이그레이션은 "현재 X, 시점 Y부터 Z" 공식으로 말해. "right now is X / from Y, will be Z" - 이게 공급업체가 노드 전환을 발표하는 정석이다. "right now"와 "from Y"의 시점 대비가 명확해야 HPE가 자기 스케줄에 반영할 수 있다.

### 단계 3: 샘플 준비 상태 (Sample Readiness)

"샘플은 X 시점에 준비, Y 시점에 납품"의 timeline target.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we expect the sample will be ready in end of X timeframe` | "we expect the sample will be ready in end of February timeframe" | 샘플 준비 timeline target |
| `we will deliver to HPE all the of X timeframe` | "we will deliver to HPE all the of March timeframe" | 납품 timeline |
| `we will deliver to HPE as soon as possible.` | "we will deliver to HPE as soon as possible." | 긴급 납기 표현 |
| `Not only X, but also Y and Z` | "Not only 64 gigabyte, but also 32 gigabyte, 2 rank by 8 and 16 gigabyte, 1 rank by 8." | 확대 적용 명시 |

**Audrey 교훈**: "sample will be ready in end of X timeframe" - "timeframe"을 붙이는 게 중요하다. "end of February"만 하면 너무 확정적이고, "end of February timeframe"이면 여유가 있다. 그리고 "we will deliver"로 납품 책임을 명시. 이게 Type B 로드맵 발표의 핵심 화법이다.

### 단계 4: 권고 (Recommendation)

SK하이닉스가 HPE에게 "1Cnm로 가세요"라고 권고.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are highly recommended to proceed our X for HPE Y project` | "we are highly recommended to proceed our 1C nanometer 8000 for HPE Venice project and EMR project" | 권고 - "highly recommended" |
| `please consider positively to migrate to X as soon as possible` | "please consider positively to migrate to 1C nanometer as soon as possible" | 적극 전환 요청 |
| `1C nanometer can save for power around X` | "1C nanometer can save for power around 10% or 12%." | 정량적 이익 |

**Audrey 교훈**: "we are highly recommended to proceed X" - 권고의 공식. "we recommend X"보다 "we are highly recommended to proceed X"가 더 강하다. 그리고 "please consider positively to migrate" - "consider positively"가 "검토해 주세요"의 적극적 영어 버전. 한국어 "긍정 검토 부탁드립니다"의 직역이지만, 영어로는 이게 자연스럽다.

### 단계 5: 질문 유도 (Question Invitation)

각 페이지 끝에 간단히.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Any questions so far here?` | "Any questions so far here?" | 중간 점검 |
| `Any question?` | "Any question?" | 페이지 끝 확인 |
| `If no questions, then go to the next slide.` | "If no questions, then go to the next slide." | 침묵 처리 - 자연스러운 넘김 |

### 단계 6: 사후 권고 반복 (Closing Reinforcement)

발표 마지막에 다시 한번 권고.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `please consider positively to migrate to X as soon as possible` | (closing) "please consider positively to migrate to 1C nanometer as soon as possible." | 마지막 강조 |

**Audrey 교훈**: 로드맵 발표는 "변경점 - 노드 - 샘플 - 권고 - 질문 - 권고 반복"의 6단계다. 이 뼈대를 외워. 매분기 QBR에서 Doyeon이 이 구조를 그대로 쓴다. 네가 발표할 때도 이 순서를 지켜.

---

## 1.5. Eric의 도전 발화 아키텍처 (별도 부록 - Microsoft 제안 도전)

이 회의의 도전 화법 보석은 Doyeon의 발표가 아니라 Eric의 Microsoft 제안 도전에 있다. Type A급 도전 화법이 섞여 있어서 별도로 정리한다.

### Eric의 5단계 도전 구조

| 단계 | 화법 공식 | 원문 | 기능 |
|:---|:---|:---|:---|
| 1. 수식 인정 + 가정 도전 | `all of their math is correct, but trying to determine if the base assumption is valid` | "Do we believe that the Microsoft solution is, all of their math is correct, but trying to determine if the base assumption is valid." | "수식은 맞는데 가정이 틀리면 의미 없다" - 가장 고급 도전 |
| 2. 논리적 귀결 | `If the base assumption is not valid, then it doesn't matter.` | "If the base assumption is not valid, then it doesn't matter. If you do the math right, you still may not have a correct answer." | 논리적 귀결 강조 |
| 3. 정량화 도전 | `when you say X, that's not a quantifiable measurement. That's qualitative.` | "Well, when you say good enough, that's not a quantifiable measurement. That's qualitative." | "good enough"를 정성적이라 공격 |
| 4. 스케일 확장 | `if one server takes X, 100 servers means Y` | "if one server with that failure mode takes 100 years to crack before it gets an uncorrectable error... 100 servers, that means I will have multiple servers fail every month." | 단일 서버를 데이터센터 스케일로 확장 |
| 5. 포지션 고수 | `until I decide otherwise, my position is X is required` | "until I decide otherwise, my position is 2P3 is required." | 결정 전까지 기본 포지션 유지 |

**Audrey 교훈**: Eric의 "math correct / assumption invalid" 도전이 이 회의의 최고 보석이다. "수식은 맞는데 가정이 틀리면 답이 틀린다" - 이 2단 도전을 외워. 한국의 기술 회의에서도 Microsoft나 Intel의 제안을 도전할 때 이 공식을 쓸 수 있다. "그 분의 수식은 맞는데, 전제가 맞는지 확인이 필요합니다" - 이게 영어로 "all of their math is correct, but trying to determine if the base assumption is valid"다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 진짜 학습 가치. 포지션을 미루고, 모르는 걸 인정하고, 결정을 보류하는 화법.

### 전략 1: 수식 인정 + 가정 도전 (Math-Yes-Assumption-No)

Eric이 Microsoft 제안을 도전할 때 쓴 가장 고급 화법.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Microsoft 제안 도전 | "Do we believe that the Microsoft solution is, **all of their math is correct, but trying to determine if the base assumption is valid. If the base assumption is not valid, then it doesn't matter. If you do the math right, you still may not have a correct answer.**" | "Microsoft 수식은 모두 맞습니다. **하지만 기본 가정이 유효한지 판단하려는 중입니다. 가정이 유효하지 않으면, 수식이 맞아도 정답이 아닙니다.**" |

**패턴 공식**: `All of their math is correct, but trying to determine if the base assumption is valid. If the base assumption is not valid, then it doesn't matter.`

**Audrey 교훈**: 상대의 제안을 도전할 때 "틀렸다"고 직접 말하지 마라. "수식은 맞는데 가정을 확인 중이다" - 이게 가장 고급 도전이다. 왜냐면 상대의 작업을 인정하면서도, 더 근본적인 수준에서 도전하기 때문. "you're wrong"이 아니라 "your assumption may not hold" - 이게 영어 도전의 정석.

### 전략 2: 주장과 거리 두기 (Distancing from Claim)

Microsoft의 주장을 인용하되, 동조하지 않는다는 것을 명시.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 12년 주장 인용 | "If you read their presentation, **they are claiming that** if a DRAM is completely dead, then they claim that it will take 12 years before you have an uncorrected memory error." | "발표 자료를 읽어보면, **그들의 주장은** DRAM이 완전히 죽어도 12년 걸린다고 합니다." |
| 주장과 거리 | "I'm not sure if it is really correct. **Just be stating their claim.**" | "정말 맞는지 모르겠습니다. **그들의 주장을 말하는 것뿐입니다.**" |
| 가정 부여 | "So if I believe that assertion, **I'm not saying that I do.**" | "그 주장을 믿는다면, **제가 믿는다는 건 아닙니다.**" |

**패턴 공식**: `They are claiming that X. Just be stating their claim. I'm not saying that I do (believe it).`

**Audrey 교훈**: 상대의 주장을 인용할 때 "they claim" / "they are claiming"을 써라. "they say"가 아니라 "they claim"이 거리 두기다. 그리고 "I'm not saying that I do" - "제가 동의한다는 건 아닙니다" - 인용 다음에 바로 이 문장을 붙여. 이게 "인용 = 동의"가 되는 것을 막는 화법이다. 한국어 "그쪽에서 그렇게 주장하는데요, 저는 판단 보류합니다"의 영어 버전.

### 전략 3: 모름 인정 + 후속 액션 (Honest Ignorance + Follow-up)

모르는 걸 솔직히 인정하되, "확인하겠다"로 마무리.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| SK 모름 인정 | "I need to go back and check with the... Right. I need to go back and check with the data." | "확인해 봐야겠습니다. 데이터 확인하겠습니다." |
| 미래 오류율 모름 | "frankly speaking, **it's very difficult to estimate** what will be the correctable errors for the future future devices." | "솔직히 말씀드리면, **매우 추정하기 어렵습니다**" |
| 완전 부인 | "in terms of how much, how many, what percent will be increased, **we have no idea on that.**" | "얼마나, 몇 퍼센트 증가할지 **전혀 예측이 안 됩니다.**" |

**패턴 공식**: `Frankly speaking, it's very difficult to estimate X. We have no idea on that.`

**Audrey 교훈**: 한국 회의에서 "모릅니다"는 약해 보인다. 하지만 영어에서 "frankly speaking, it's very difficult to estimate"는 솔직함의 표현이다. "we have no idea"는 더 강한 부인 - 그런데 이게 약한 게 아니라 "정직한 엔지니어"로 들린다. 단, "I don't know"로 끝내지 말고 "I need to go back and check"로 후속을 붙여야 한다.

### 전략 4: 포지션 보류 (Position Hold)

결정 전까지 기본 포지션을 유지하겠다는 명시.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 포지션 고수 | "So until I decide otherwise, **my position is 2P3 is required.**" | "다른 결정을 내릴 때까지, **제 포지션은 2P3 필수입니다.**" |
| 포지션 불변 | "My position is unchanged from previous **until I decide that I am satisfied with their numbers that I believe them.**" | "이전과 동일합니다, **그들의 수치에 만족할 때까지.**" |
| 수식은 동의 | "I've seen their calculations. **I don't have arguments with how they calculate after they make their assumptions.** What I don't know if I agree with yet are the assumptions." | "수식은 봤습니다. **어떻게 계산하는지는 동의합니다.** 동의 안 하는 건 가정입니다." |

**패턴 공식**: `Until I decide otherwise, my position is X is required. My position is unchanged until I decide that I am satisfied with Y.`

**Audrey 교훈**: 포지션을 미룰 때 "we will consider"는 약하다. "Until I decide otherwise, my position is X" - "다른 결정을 내릴 때까지 X가 제 포지션입니다" - 이게 명확한 보류다. 그리고 "I don't have arguments with X / What I don't know if I agree with yet are Y" - 동의하는 것과 동의 안 하는 것을 분리. 이게 협상의 정밀한 화법이다.

### 전략 5: 조심스러운 포지션 표명 (Careful Position Statement)

여러 플랫폼이 엇갈려 포지션을 신중하게 말해야 할 때.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| MRDIM 포지션 | "I have to be very careful with my position **because I know I have at least one platform that is planning to use Gen 3 MRDIM.** But I have other platforms that are planning to use LP MRDIM. But I believe those platforms will command a higher shipping volume." | "포지션 말에 조심스러워야 합니다, **한 플랫폼은 Gen 3 MRDIM 계획이니까요.** 하지만 다른 플랫폼들은 LP MRDIM이고, 그쪽이 출하량이 더 많을 겁니다." |
| 부분 동의 | "me as a simple engineer, that might be okay. **Procurement might have a different answer.**" | "엔지니어로서는 괜찮을 수 있습니다. **조달 쪽은 다를 답을 할 수 있습니다.**" |
| 의향 표시 | "I personally prefer the LP MRDIM because I think it's a better, more power efficient story. **But I can't say absolutely no MRDIM for HPE simply because I know I have a platform team that wants it.**" | "개인적으로는 LP MRDIM 선호합니다. **하지만 HPE가 MRDIM 안 된다고 절대 말할 수는 없습니다, 원하는 플랫폼 팀이 있으니까요.**" |

**패턴 공식**: `I have to be very careful with my position because X. But I believe Y. I personally prefer Z. But I can't say absolutely no W simply because...`

**Audrey 교훈**: 여러 사내 이해관계자가 엇갈릴 때 "I have to be very careful with my position because..."로 시작해라. 이게 정치적 민감함을 인정하는 화법이다. 그리고 "me as a simple engineer" - "단순 엔지니어로서" - 자기 권한의 한계를 명시하면서, 다른 부서(Procurement)가 다를 수 있다는 걸 미리 방어. "I can't say absolutely no X" - "절대 안 �다고 말할 수 없다" - 이게 권한 한계를 인정하는 정중한 화법이다.

### 전략 6: 유머로 action item 회피 (Humorous Deflection)

action item을 받아들이되 유머로 책임의 무게를 줄인다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Michael의 action item | "I would say yes, but **I know I will probably forget by tomorrow. I do not have SDDC.** I will contact Michael once again." | "그러죠, **근데 내일쯤 잊어버릴 겁니다. 제 뇌에는 SDDC가 없거든요.** Michael한테 다시 연락하겠습니다." |
| 자가调侃 | "My brain does not have SDDC. **So I know I will forget.**" | "제 뇌에는 SDDC가 없어서, **잊어버릴 걸 압니다.**" |

**패턴 공식**: `I would say yes, but I know I will probably forget by tomorrow. I do not have SDDC.`

**Audrey 교훈**: 이게 회의에서 유머가 어떻게 쓰이는지의 보석이다. Eric이 자기 뇌를 "SDDC 없는 DIMM"에 비유 - 기술 회의에서 기술 용어로 자가调侃. 이런 유머는 (1) action item을 받아들이고, (2) 동시에 자기가 잊을 수 있다는 걸 미리 면책, (3) 분위기를 희석. 한국 회의에서 "제 뇌에 SDDC가 없어서요"는 안 통하지만, 영어 회의에서는 이런 기술 유머가 프로다운 분위기를 만든다. 외워서 써라.

### 전략 7: 데이터 부재의 정중한 요청 (Polite Data Request)

어려운 수치 요청을 "이렇게 어려운 걸 요청하는데"로 전제.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 2DPC 전력 추정 요청 | "I know I'm asking for something very difficult that you might not be able to provide, **but any guidance can be helpful.**" | "제가 매우 어려운 걸 요청하는 거 압니다, **하지만 어떤 가이드라도 도움이 됩니다.**" |
| 보수적 추정이라도 | "Even if it is a very high, even if it's a very conservative, high estimate that is probably way too high, **it's better than no estimate.**" | "매우 보수적이고 과대 추정이라도, **아예 없는 것보다 낫습니다.**" |
| 비판적 강조 | "I can't tell you how critical this data is to us." | "이 데이터가 우리에게 얼마나 중요한지 말로 다 못합니다." |

**패턴 공식**: `I know I'm asking for something very difficult, but any guidance can be helpful. Even if it's a conservative estimate, it's better than no estimate.`

**Audrey 교훈**: 어려운 요청을 할 때 "I know I'm asking for something very difficult"를 먼저 붙여라. 상대가 거절하기 어렵게 만드는 화법이다. 그리고 "any guidance can be helpful" - "어떤 가이드라도" - 요청의 문을 넓힌다. 그리고 "better than no estimate" - "아예 없는 것보다 낫다" - 상대의 완벽주의를 방어. 이 3단 화법을 외워. 수치 요청할 때 무조건 이렇게 해.

---

## 3. 정중한 도전 화법 (Polite Challenge Patterns)

HPE가 SK하이닉스의 데이터와 Microsoft의 주장을 도전하는 패턴. 네가 HPE 입장이든 SK 입장이든 둘 다 배워야.

### 질문 유형 1: 가정 도전형 (Assumption Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `all of their math is correct, but trying to determine if the base assumption is valid` | "all of their math is correct, but trying to determine if the base assumption is valid" | 수식 인정 + 가정 도전 - 가장 고급 |
| `If the base assumption is not valid, then it doesn't matter.` | "If the base assumption is not valid, then it doesn't matter." | 논리적 귀결 강조 |
| `If you do the math right, you still may not have a correct answer.` | "If you do the math right, you still may not have a correct answer." | 수식만으로는 부족함을 강조 |

**Audrey 교훈**: "math correct / assumption invalid" - 이 2단 도전을 외워. 상대의 수식을 도전하면 기싸움이 되지만, 가정을 도전하면 기술 논의가 된다. 이게 고급 도전의 비결이다.

### 질문 유형 2: 정량화 요구형 (Quantification Demand)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `when you say X, that's not a quantifiable measurement. That's qualitative.` | "when you say good enough, that's not a quantifiable measurement. That's qualitative." | "good enough"를 정성적이라 공격 |
| `what might be good enough for some may not be good enough for other` | "what might be good enough for some may not be good enough for other" | 상대적 기준 지적 |
| `is it good enough at the X level or is it good enough at the Y level?` | "is it good enough at the server level or is it good enough at the data center level?" | 스케일 구분 요구 |

**Audrey 교훈**: "good enough"는 영어 회의에서 가장 많이 쓰이는 도전 대상이다. "good enough for whom? at what scale?" - 이렇게 구체화를 요구하는 게 정량화 도전이다. "that's qualitative"이라고 지적하면, 상대는 수치를 내놓거나 주장을 약화해야 한다.

### 질문 유형 3: 스케일 확장형 (Scale Expansion)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `if one server takes X, 100 servers means Y` | "if one server with that failure mode takes 100 years to crack... 100 servers, that means I will have multiple servers fail every month" | 단일 스케일을 데이터센터 스케일로 |
| `what if I have a quality excursion that I have 100 servers with that same failure?` | "what if I have a quality excursion that I have 100 servers in my data center with that same failure?" | 품질 편차 시나리오 제시 |
| `12 years divided by 100` | "So that's now 12 years divided by 100. So I'm still going to have multiple servers crash per year" | 수식으로 도전 |

**Audrey 교훈**: Eric의 스케일 확장이 도전의 핵심이다. "1대가 100년 걸리면 100대는 매월 고장" - 단일 수치를 전체 스케일로 환산하면, "good enough"의 가정이 무너진다. 이게 기술 도전의 수식이다. "if X takes Y, then N times X takes Y/N" - 이 스케일 도전을 외워.

### 질문 유형 4: 반대 증거형 (Counter-Evidence)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `they are claiming that it is good enough for them. But we are hearing from the other customers, non-Microsoft. It's not really true.` | "But they are claiming that it is good enough for them. But we are hearing from the other customers, non-Microsoft. It's not really true." | Microsoft 주장 vs 다른 고객 실증 |
| `something tells me that SSSK hynix has data on far more DIMMs than Microsoft does.` | "something tells me that SSSK hynix has data on far more DIMMs than Microsoft does. Because you ship DIMMs to people more than just Microsoft." | SK 데이터의 권위 부여 |

**Audrey 교훈**: "But we are hearing from the other customers, non-Microsoft. It's not really true." - 반대 증거를 "other customers"로 포괄. 구체 이름 안 대고 "다른 고객들"로. 그리고 "something tells me that X has data on far more Y than Z" - "X가 Z보다 훨씬 더 많은 데이터가 있을 것 같다" - 이게 상대의 권위를 인정하면서 도전을 유도하는 화법이다. Eric이 SK를 도전하려는 게 아니라, SK를 Microsoft에 대한 counter-weight로 쓰는 것이다.

### 질문 유형 5: 확인식 짧은 질문 (Quick Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is that one good enough?` | "Is that one good enough?" (16-bit version에 대해) | 짧은 도전 |
| `Is the right statement?` | "Is it the right statement?" - SK가 HPE 포지션 요약 확인 | 포지션 요약 확인 |
| `Your position has not been changed yet, right?` | "your position has not been changed yet, right?" | "right?"로 포지션 고정 |

**Audrey 교훈**: 발표 흐름을 끊지 않는 짧은 도전. "Is that one good enough?" - 3단어로 도전. 발표자가 쉽게 대답할 수 있고, 도전의 핵심이 명확하다. 회의에서 긴 도전을 하기 전에, 이런 짧은 확인으로 시작해라.

### 질문 유형 6: 포지션 탐색 (Position Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `what will be your position?` | "what will be your position?" - SK가 HPE 포지션 직접 질문 | 포지션 직접 요청 |
| `from the whole HP perspective, when do you think it will be the time that you will fix your position` | "from the whole HP perspective, when do you think it will be the time that you will fix your position, including the engineer side and the sourcing side, procurement side, when it will be?" | 결정 시점 요청 - 부서별 |
| `if SSSK hynix will only offer one, I think there's more business opportunity with X` | "if SSSK hynix will only offer one, I think there's more business opportunity with LPM or DIM" | 비즈니스 영향으로 포지션 암시 |

**Audrey 교훈**: "when do you think it will be the time that you will fix your position" - 이게 파트너의 결정 시점을 묻는 공식이다. "fix your position"이 핵심 - "포지션을 확정하다"의 영어 표현. 그리고 부서별(엔지니어링, 조달)을 명시하면, 상대가 "단순 엔지니어로서는..." 식으로 답을 한정하게 된다. Eric이 실제로 그렇게 답했다. 질문의 틀을 만들면 답이 그 틀 안에서 나온다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

**Type B 핵심 섹션**. 로드맵/스케줄/샘플/포지션 협상의 모든 화법이 여기 있다.

### 협상 화법 - 타임라인 타겟

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 준비 timeline | SK | "we expect the sample will be ready in end of February timeframe" | timeline target 공식 |
| 납품 timeline | SK | "we will deliver to HPE all the of March timeframe" | 납기 확정 |
| CS 완료 | SK | "the CS for the one to one 92 gigabyte module has been completed" | 완료 상태 보고 |
| 양산 시작 | SK | "mass production will begin in April" | 마일스톤 |
| CS 시점 | SK | "scheduled to provide the CS by the end of March" | CS schedule target |
| 양산 시점 | SK | "begin mass production in Bay next year" | 양산 timeline |

**패턴 공식**: `we expect the sample will be ready in X timeframe. we will deliver to HPE in Y timeframe. mass production will begin in Z.`

**Audrey 교훈**: Type B 회의에서 "timeframe"을 붙이는 게 핵심이다. "end of February"만 하면 너무 확정적이고, "end of February timeframe"이면 여유가 있다. SK가 매번 "timeframe"을 붙이는 걸 보면, 이게 일정 약속의 완충제다. 네가 timeline을 말할 때 무조건 "timeframe"을 붙여.

### 협상 화법 - 권고와 응답

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 적극 권고 | SK | "we are highly recommended to proceed our 1C nanometer 8000 for HPE Venice project and EMR project" | 권고 공식 |
| 동의 + 조건 | HPE | "I agree with you, we need to get 1C as soon as we can. **If we cannot do it in NPI, then we will have to work through the sustaining lab to see how quickly after Venice launch it can be added.**" | 조건부 동의 |
| 긴급성 인정 | HPE | "I agree. It is urgent." | 긴급성 명시 |
| 후속 액션 | HPE | "we will analyze our schedule and see if we can get it into the NPI qual" | 후속 조사 약속 |
| 신중한 답변 보류 | HPE | "I want to give the NPI team enough time to do their due diligence in analyzing the schedule **rather than give you an answer tonight and find out I was wrong.**" | 답변 보류 + 사유 |

**패턴 공식**: `I agree with you, we need to get X as soon as we can. If we cannot do it in Y, then we will have to work through Z. I want to give the team enough time to do due diligence rather than give you an answer tonight and find out I was wrong.`

**Audrey 교훈**: "rather than give you an answer tonight and find out I was wrong" - 이게 답변 보류의 황금 공식이다. "오늘 답하고 내일 틀렸다는 걸 알게 되는 것보다, 팀에게 시간을 주겠다" - 신중함을 미덕으로 포장. 한국어 "내부 검토 후 답변드리겠습니다"의 훨씬 구체적이고 설득력 있는 영어 버전. 외워.

### 협상 화법 - 포지션 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 포지션 요약 확인 | SK | "your preference is LP MRDIM. So, your position has not been changed yet, right?" | "right?"로 포지션 고정 |
| 포지션 신중 표명 | HPE | "I have to be very careful with my position because I know I have at least one platform that is planning to use Gen 3 MRDIM" | 조심스러운 포지션 |
| 부서별 한계 | HPE | "me as a simple engineer, that might be okay. **Procurement might have a different answer.**" | 부서별 분리 |
| 개인 선호 vs 회사 포지션 | HPE | "I personally prefer the LP MRDIM... **But I can't say absolutely no MRDIM for HPE** simply because I know I have a platform team that wants it." | 개인 vs 회사 분리 |
| 비즈니스 영향 | HPE | "if SSSK hynix will only offer one, I think there's more business opportunity with LPM or DIM" | 비즈니스로 포지션 암시 |

**패턴 공식**: `I have to be very careful with my position because X. I personally prefer Y. But I can't say absolutely no Z simply because W. There's more business opportunity with Y.`

**Audrey 교훈**: 포지션 협상에서 "me as a simple engineer" - "단순 엔지니어로서" - 자기 권한의 한계를 명시하는 게 핵심. 그러면 상대는 "그럼 procurement에 물어봐야겠네"라고 다음 단계를 파악한다. 그리고 "I personally prefer X. But I can't say absolutely no Y" - 개인 의견과 회사 포지션을 분리. 이게 조직의 복잡성을 정중하게 반영하는 화법이다. 네가 SK 입장에서 HPE에 "no"를 말할 때, "I personally agree but our platform team may have different view"로 부서를 분리해.

### 협상 화법 - 결정 시점 요청

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 결정 시점 요청 | SK | "when do you think it will be the time that you will fix your position, including the engineer side and the sourcing side, procurement side, when it will be?" | 부서별 결정 시점 |
| 결정 미정 인정 | HPE | "the actual POR, we haven't even created that POR internally yet" | POR 미정 인정 |
| 후속 시점 | HPE | "for LPM or DIM, this is DMR follow-on. So it's going to be a while." | 시점 회피 - "a while" |
| 후속 시점 2 | HPE | "for Gen 3 MRDIM, that is Venice follow-on. So again, it's going to be a while." | 동일 패턴 반복 |

**패턴 공식**: (요청) `when do you think it will be the time that you will fix your position?` (응답) `the actual POR, we haven't even created that POR internally yet. It's going to be a while.`

**Audrey 교훈**: "It's going to be a while" - "시간 좀 걸릴 겁니다" - 결정 시점을 회피하는 정중한 화법. "we haven't even created that POR internally yet" - "POR 자체를 아직 안 만들었다" - 더 솔직한 회피. 이 두 개를 연달아 쓰면, "결정 시점 안 정해졌다"는 게 명확해진다.

### 협상 화법 - 샘플 수량 및 용량 조율

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 수량 상한 | HPE | "what I would do is I would look at our, what we have talked about for RDIM, and that would be the max number. We wouldn't ask for more samples than we do for RDIM." | 샘플 상한 설정 |
| 비교 기준 | HPE | "also look at the sample quantities we've asked for for Gen 2 MRDIM. That would give you a sample quantity." | 비교 기준 제시 |
| 용량 관심 | HPE | "LPM or DIM doesn't support a 32 gigabyte, so it would be 64 and 128 at least." | 용량 명시 |
| nice-to-have | HPE | "256 maybe might be nice to have. But at this point, I don't have direct customer data that pushes me there." | "nice to have" - 우선순위 낮음 |
| 일정/수량 미정 | HPE | "we're still trying to get some further definition on that time frame in the quantity." | 미정 인정 |

**패턴 공식**: `We wouldn't ask for more samples than we do for X. Also look at the sample quantities we've asked for for Y. That would give you a sample quantity. Z would be 64 and 128 at least. W maybe might be nice to have.`

**Audrey 교훈**: "nice to have" - 영어 협상에서 매우 중요한 표현. "있으면 좋지만 필수는 아니다" - 우선순위를 낮추는 정중한 화법. "I don't have direct customer data that pushes me there" - "고객 데이터가 없어서" - 이유까지 붙이면 더 정중. 네가 HPE에 뭔가를 제안할 때, "이건 nice to have입니다"라고 먼저 우선순위를 낮추면, HPE가 부담 없이 검토할 수 있다.

### 협상 화법 - 샘플 요청 교환

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 밀도 질문 | SK | "Oh, which density do you need?" | 용량 확인 |
| 긴급 고객 명시 | HPE | "I think that one is looking for 192 gigabyte. Michael correct me if I'm wrong. This is a Zeta's request." | 특정 고객 명시 |
| 일정 안내 | HPE | "You can work with Michael to get the exact schedule they've been discussing directly with him on sample availability." | 담당자 연결 |
| 샘플 요청 요청 | SK | "then please provide us your sample request." | 공식 요청 |
| action item 수락 | HPE | "Okay, connection item. We'll do that." | 수락 |
| 미정 확인 | HPE | "we're still trying to get some further definition on that time frame in the quantity" | 미정 인정 |

**Audrey 교훈**: 샘플 협상의 정석: (1) "which density do you need?" - 용량 확인, (2) 특정 고객/플랫폼 명시 - "This is a Zeta's request", (3) 담당자 연결 - "work with Michael", (4) 공식 요청 - "please provide us your sample request", (5) 수락 - "we'll do that". 이 5단계를 외워. 샘플 요청은 "please provide us your sample request"로 공식화해야 action item이 된다.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| action item 부여 | SK | "Michael, will you take an action item for us to chat with our thermal guys and see if they'd be willing to have a discussion with SK Heinecks." | "take an action item" - 부여 공식 |
| 유머 수락 | HPE | "I would say yes, but I know I will probably forget by tomorrow. I do not have SDDC." | 유머 + 수락 |
| 자가提醒 | HPE | "I will contact Michael once again." | 자가 후속 약속 |
| 책임 수락 | SK | "So let me check the real measurement data for at 6400 speeds to 1DPC and 2DPC. Yep. And get back to you." | 후속 약속 |
| 업데이트 시점 | SK | "we will give you more updates in Q2 timeframe after we have discussion with RCD Bander and also the FCC Bander" | 시점 + 전제 조건 |
| 후속 채널 | HPE | "if there are follow up questions, please feel free to email me" (유사) | 이메일 채널 개방 |
| 마무리 감사 | HPE | "Thank you very much SKINX for a very productive discussion. We really appreciate it." | 정식 마무리 |

**Audrey 교훈**: "take an action item" - 회의에서 책임을 부여하는 공식. "will you take an action item to X" - 이렇게 물어봐야 공식 action item이 된다. 그리고 Eric의 유머 수락 "I do not have SDDC" - action item을 수용하되, 자기가 잊을 수 있다는 걸 유머로 면책. 이게 고급 action item 수락 화법이다. "I will contact Michael once again"으로 자가 후속까지 붙이면 완벽.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 DDR5/DDR6/MRDIM/CXL/ECC 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **SDDC** (Single Device Data Correction) | 단일 DRAM 칩故障까지 정정하는 ECC | "we will require up to actual SDDC" - "actual SDDC"로 강조 |
| **SDC** (Silent Data Corruption) | 감지 못 하는 데이터 오염 | "we still say never silent data corruption. Never. That is a bad word in servers." - "never" 반복 강조 |
| **UE** (Uncorrectable Error) | 정정 불가능 오류 | "the UE and SDC rate during some certain amount of years" |
| **on-die ECC** | DRAM 칩 내부 ECC | "I will not support any motion that removes on die ECC or that exposes on die ECC" - "exposes" - 노출(=제거) |
| **metadata bits** | ECC 추적용 추가 비트 | "you need more metadata carved up. As a result, you will have reduction in capacity" - "carved up" - 할당됨 |
| **2DPC / 1DPC** (DIMMs Per Channel) | 채널당 DIMM 수 | "2DPC adds ODT power, but it reduces speed" - trade-off 설명 |
| **ODT** (On-Die Termination) | 온다이 종단 | "2DPC adds ODT power" - 전력 증가 원인 |
| **FIT rate** (Failures In Time) | 시간당 고장률 | "ECC protects us not just from fit rate failures" |
| **quality excursion** | 품질 편차 사건 | "what if I have a quality excursion that I have 100 servers in my data center with that same failure?" |
| **POR** (Plan of Record) | 확정 계획 | "the actual POR, we haven't even created that POR internally yet" - 미정 인정 |
| **NPI** (New Product Introduction) | 신제품 도입 | "if we cannot do it in NPI, then we will have to work through the sustaining lab" |
| **sustaining** | 양산 유지보수 | "process sustaining work with our 1C nanometer" - 1Cnm 도입 작업 |
| **EOL** (End of Life) | 단종 | "we released 4800 team or EOL in December 2025" |
| **CS** (Customer Sample) | 고객 샘플 | "CS will follow in February next year" |
| **ES** (Engineering Sample) | 엔지니어링 샘플 | "the ES sample will provide this September" |
| **EVV board** (Evaluation Board) | 평가 보드 | "HP received an EVV board in December last year" |
| **MRDIM** (Multi-Rank DIMM) | 다중 랭크 고속 DIMM | "Gen 3 MRDIM" vs "LP MRDIM" - 두 가지 세대 경쟁 |
| **LP MRDIM** (Low-Power MRDIM) | 저전력 MRDIM | "LP MRDIM offers better TCO than GEN3 MRDIM from the power consumption perspective" |
| **SOCAM** (Small Outline CAM) | 소형 폼팩터 메모리 모듈 | "LP five so cam" / "LP six so cam" |
| **CXL CMM** (CXL Memory Module) | CXL 메모리 모듈 | "our first gen 228GB CMM is currently in mass production" |
| **CXL 3.1** | CXL 3.1 사양 | "the second gen 256GB CMM support 6L 3.1 over PCI gen 6" |
| **HMSDK** (Heterogeneous Memory SDK) | SK 개발 이기종 메모리 SDK | "HMSDK is the heterogeneous memory software development kit" |
| **interweaving** | 메모리 인터리빙 | "interweaving between main memory and 6-series memory" |
| **software tiering** | 소프트웨어 메모리 계층화 | "software tiering function gets needed to support multi-threading" |
| **KV cache** | LLM 키-값 캐시 | "the key value cache data offloading into the CXL memory" |
| **by 4 / by 8** (x4 / x8) | DRAM 디바이스 폭 | "by 8 for MRDIMS N2 to, since it offers a better power consumption" |
| **1anm / 1Cnm** | DRAM 공정 노드 | "from second half, 2026, our main technology will be 1C nanometer" |
| **RCD vendor** (Register Clock Driver) | RCD 칩 공급업체 | "we have discussion with RCD Bander and also the FCC Bander" |
| **CXL by 4 / by 8 mode** | CXL 폭 모드 | "we definitely want a CXL device to be able to operate in by four mode" |
| **thermal resistance** | 열저항 | "the thermal resistance is going to be going to increase because as we go to DDR6" |
| **CDC** (Cubic Dimension Capacity?) | 용량 밀도 기법 | "We can achieve a CDC with 2dPC" |
| **2P3** | 2페이지 3단? (포지션 표현) | "my position is 2P3 is required" - Eric의 기본 포지션 |
| **RAS** (Reliability, Availability, Serviceability) | 신뢰성/가용성/서비스성 | "they valued RAS more than performance" |
| **warranty** | 보증 | "we can calculate our warranty for servers... you guys can calculate your warranty for DIMMs" |
| **downtime** | 서버 정지 시간 | "they claim that they cost them $3 million a minute in downtime" |
| **failover** | 장애 조치 | "you can structure your server nodes in a failover manner" |
| **POR that CPU** | CPU를 POR에 등록 | "if we do POR that particular CPU" - 동사로 사용 |
| **kick the tires** | 가볍게 평가해보다 | "we have kicked the tires on an appliance" - 비유적 표현 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 55개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 로드맵 발표 아키텍처 (Roadmap Presentation) ──
- id: m22-001
  expression: "the all the contents is all the same except X"
  category: roadmap_framing
  function: what_new_framing
  speaker_role: presenter
  difficulty: 3
  context: "the all the contents is all the same except 24 gigabits"
  note: 분기 로드맵 발표 첫 공식 - 변경점 단일화

- id: m22-002
  expression: "So, let's touch more detail."
  category: roadmap_transition
  function: depth_signal
  speaker_role: presenter
  difficulty: 2
  context: "So, let's touch more detail."

- id: m22-003
  expression: "our main technology is right now is X. from second half, Y, our main technology will be Z"
  category: tech_node_transition
  function: node_migration
  speaker_role: presenter
  difficulty: 3
  context: "our main technology is right now is 1anm. And from second half, 2026, our main technology will be 1C nanometer"
  note: 기술 노드 마이그레이션 공식 - "right now X / from Y will be Z"

- id: m22-004
  expression: "we expect the sample will be ready in end of X timeframe"
  category: timeline_target
  function: sample_readiness
  speaker_role: presenter
  difficulty: 3
  context: "we expect the sample will be ready in end of February timeframe"
  note: "timeframe"을 붙여 여유 확보 - Type B 핵심

- id: m22-005
  expression: "we will deliver to HPE all the of X timeframe"
  category: delivery_commitment
  function: ship_timeline
  speaker_role: presenter
  difficulty: 3
  context: "we will deliver to HPE all the of March timeframe"

- id: m22-006
  expression: "we are highly recommended to proceed our X for HPE Y project"
  category: recommendation
  function: strong_recommend
  speaker_role: presenter
  difficulty: 4
  context: "we are highly recommended to proceed our 1C nanometer 8000 for HPE Venice project and EMR project"
  note: "highly recommended" - 권고 강도 높임

- id: m22-007
  expression: "please consider positively to migrate to X as soon as possible"
  category: recommendation
  function: migration_request
  speaker_role: presenter
  difficulty: 3
  context: "please consider positively to migrate to 1C nanometer as soon as possible"
  note: "consider positively" - "긍정 검토"의 적극적 영어 버전

- id: m22-008
  expression: "Not only X, but also Y and Z"
  category: expansion
  function: scope_extension
  speaker_role: presenter
  difficulty: 2
  context: "Not only 64 gigabyte, but also 32 gigabyte, 2 rank by 8 and 16 gigabyte, 1 rank by 8."

- id: m22-009
  expression: "we will deliver to HPE as soon as possible."
  category: urgent_delivery
  function: expedited_commit
  speaker_role: presenter
  difficulty: 2
  context: "we will deliver to HPE as soon as possible."

- id: m22-010
  expression: "the CS for the X has been completed and mass production will begin in Y"
  category: milestone_report
  function: status_report
  speaker_role: presenter
  difficulty: 3
  context: "the CS for the one to one 92 gigabyte module has been completed and mass production will begin in April"

- id: m22-011
  expression: "mass production will begin in X"
  category: production_target
  function: timeline
  speaker_role: presenter
  difficulty: 2
  context: "mass production will begin in Bay next year"

- id: m22-012
  expression: "Any questions so far here?"
  category: question_invitation
  function: midpoint_check
  speaker_role: presenter
  difficulty: 2
  context: "Any questions so far here?"

- id: m22-013
  expression: "If no questions, then go to the next slide."
  category: silence_handling
  function: natural_transition
  speaker_role: presenter
  difficulty: 2
  context: "If no questions, then go to the next slide."

# ── 도전 화법 (Challenge) ──
- id: m22-014
  expression: "all of their math is correct, but trying to determine if the base assumption is valid"
  category: assumption_challenge
  function: math_yes_assumption_no
  speaker_role: challenger
  difficulty: 5
  context: "Do we believe that the Microsoft solution is, all of their math is correct, but trying to determine if the base assumption is valid"
  note: 가장 고급 도전 - 수식 인정 + 가정 도전. 무조건 외울 것.

- id: m22-015
  expression: "If the base assumption is not valid, then it doesn't matter."
  category: logical_consequence
  function: conclusion_draw
  speaker_role: challenger
  difficulty: 4
  context: "If the base assumption is not valid, then it doesn't matter."

- id: m22-016
  expression: "If you do the math right, you still may not have a correct answer."
  category: logical_consequence
  function: math_insufficiency
  speaker_role: challenger
  difficulty: 5
  context: "If you do the math right, you still may not have a correct answer."
  note: "수식이 맞아도 정답이 아닐 수 있다" - 도전의 핵심 명제

- id: m22-017
  expression: "when you say X, that's not a quantifiable measurement. That's qualitative."
  category: quantification_demand
  function: qualitative_attack
  speaker_role: challenger
  difficulty: 4
  context: "when you say good enough, that's not a quantifiable measurement. That's qualitative."

- id: m22-018
  expression: "what might be good enough for some may not be good enough for other"
  category: relativity_argument
  function: relative_standard
  speaker_role: challenger
  difficulty: 4
  context: "what might be good enough for some may not be good enough for other"

- id: m22-019
  expression: "is it good enough at the X level or is it good enough at the Y level?"
  category: scale_challenge
  function: scale_distinction
  speaker_role: challenger
  difficulty: 4
  context: "is it good enough at the server level or is it good enough at the data center level?"

- id: m22-020
  expression: "if one server takes X, N servers means Y"
  category: scale_expansion
  function: datacenter_scale
  speaker_role: challenger
  difficulty: 5
  context: "if one server with that failure mode takes 100 years to crack before it gets an uncorrectable error, or one server with that failure mode takes a year, 100 servers, that means I will have multiple servers fail every month"
  note: 단일 스케일을 데이터센터 스케일로 확장 - 도전의 수식

- id: m22-021
  expression: "what if I have a quality excursion that I have N servers with that same failure?"
  category: scenario_probe
  function: worst_case
  speaker_role: challenger
  difficulty: 5
  context: "what if I have a quality excursion that I have 100 servers in my data center with that same failure?"

- id: m22-022
  expression: "they are claiming that X. But we are hearing from the other customers, non-Y. It's not really true."
  category: counter_evidence
  function: customer_counter
  speaker_role: challenger
  difficulty: 4
  context: "But they are claiming that it is good enough for them. But we are hearing from the other customers, non-Microsoft. It's not really true."

- id: m22-023
  expression: "something tells me that X has data on far more Y than Z does."
  category: authority_grant
  function: counter_weight
  speaker_role: challenger
  difficulty: 5
  context: "something tells me that SSSK hynix has data on far more DIMMs than Microsoft does. Because you ship DIMMs to people more than just Microsoft."
  note: 상대를 counter-weight로 활용 - "something tells me"로 직감 표현

# ── 회피·포장 (Hedging & Deflection) ──
- id: m22-024
  expression: "they are claiming that X"
  category: distancing
  function: claim_attribution
  speaker_role: challenger
  difficulty: 3
  context: "they are claiming that if a DRAM is completely dead, then they claim that it will take 12 years"
  note: "they claim" - 동조 거리 두기. "they say"보다 강한 거리.

- id: m22-025
  expression: "Just be stating their claim."
  category: distancing
  function: disclaimer
  speaker_role: challenger
  difficulty: 4
  context: "I'm not sure if it is really correct. Just be stating their claim."
  note: 인용 = 동의 아님을 명시

- id: m22-026
  expression: "I'm not saying that I do."
  category: distancing
  function: belief_disclaimer
  speaker_role: challenger
  difficulty: 4
  context: "So if I believe that assertion, I'm not saying that I do."

- id: m22-027
  expression: "I need to go back and check with the data."
  category: honest_ignorance
  function: follow_up_promise
  speaker_role: presenter
  difficulty: 3
  context: "I need to go back and check with the data."

- id: m22-028
  expression: "frankly speaking, it's very difficult to estimate X"
  category: honest_ignorance
  function: difficulty_admit
  speaker_role: presenter
  difficulty: 4
  context: "frankly speaking, it's very difficult to estimate what will be the correctable errors for the future future devices"

- id: m22-029
  expression: "we have no idea on that."
  category: honest_ignorance
  function: total_unknown
  speaker_role: presenter
  difficulty: 3
  context: "in terms of how much, how many, what percent will be increased, we have no idea on that."

- id: m22-030
  expression: "until I decide otherwise, my position is X is required"
  category: position_hold
  function: default_position
  speaker_role: challenger
  difficulty: 5
  context: "until I decide otherwise, my position is 2P3 is required"
  note: "until I decide otherwise" - 결정 전까지 기본 포지션 유지. 무조건 외울 것.

- id: m22-031
  expression: "my position is unchanged from previous until I decide that I am satisfied with X"
  category: position_hold
  function: unchanged_position
  speaker_role: challenger
  difficulty: 5
  context: "My position is unchanged from previous until I decide that I am satisfied with their numbers that I believe them."

- id: m22-032
  expression: "I don't have arguments with how they calculate after they make their assumptions. What I don't know if I agree with yet are the assumptions."
  category: position_split
  function: agree_disagree_split
  speaker_role: challenger
  difficulty: 5
  context: "I've seen their calculations. I don't have arguments with how they calculate after they make their assumptions. What I don't know if I agree with yet are the assumptions."
  note: 동의/비동의 분리 - 협상의 정밀 화법

# ── 포지션 협상 (Position Negotiation) ──
- id: m22-033
  expression: "I have to be very careful with my position because X"
  category: careful_position
  function: sensitivity_acknowledge
  speaker_role: negotiator
  difficulty: 5
  context: "I have to be very careful with my position because I know I have at least one platform that is planning to use Gen 3 MRDIM"
  note: 정치적 민감함 인정 - 고급 포지션 화법

- id: m22-034
  expression: "me as a simple engineer, that might be okay. Procurement might have a different answer."
  category: authority_limit
  function: department_split
  speaker_role: negotiator
  difficulty: 4
  context: "me as a simple engineer, that might be okay. Procurement might have a different answer."

- id: m22-035
  expression: "I personally prefer X. But I can't say absolutely no Y simply because Z"
  category: personal_vs_company
  function: position_split
  speaker_role: negotiator
  difficulty: 5
  context: "I personally prefer the LP MRDIM... But I can't say absolutely no MRDIM for HPE simply because I know I have a platform team that wants it."

- id: m22-036
  expression: "if SSSK hynix will only offer one, I think there's more business opportunity with X"
  category: business_leverage
  function: implicit_push
  speaker_role: negotiator
  difficulty: 4
  context: "if SSSK hynix will only offer one, I think there's more business opportunity with LPM or DIM"

- id: m22-037
  expression: "from the whole HP perspective, when do you think it will be the time that you will fix your position"
  category: position_probe
  function: decision_timeline_request
  speaker_role: presenter
  difficulty: 4
  context: "from the whole HP perspective, when do you think it will be the time that you will fix your position, including the engineer side and the sourcing side, procurement side"

- id: m22-038
  expression: "the actual POR, we haven't even created that POR internally yet"
  category: decision_deferral
  function: por_undecided
  speaker_role: negotiator
  difficulty: 4
  context: "But the actual POR, we haven't even created that POR internally yet."
  note: "POR 자체를 아직 안 만들었다" - 솔직한 회피

- id: m22-039
  expression: "It's going to be a while."
  category: time_deferral
  function: vague_timeline
  speaker_role: negotiator
  difficulty: 3
  context: "for LPM or DIM, this is DMR follow-on. So it's going to be a while."

- id: m22-040
  expression: "We wouldn't ask for more samples than we do for X"
  category: sample_cap
  function: quantity_limit
  speaker_role: negotiator
  difficulty: 4
  context: "We wouldn't ask for more samples than we do for RDIM."

- id: m22-041
  expression: "X maybe might be nice to have. But at this point, I don't have direct customer data that pushes me there."
  category: priority_lower
  function: nice_to_have
  speaker_role: negotiator
  difficulty: 4
  context: "256 maybe might be nice to have. But at this point, I don't have direct customer data that pushes me there."
  note: "nice to have" - 우선순위 낮추는 정중 화법

- id: m22-042
  expression: "please provide us your sample request."
  category: formal_request
  function: sample_request
  speaker_role: presenter
  difficulty: 2
  context: "then please provide us your sample request."

# ── 협상 응답 (Negotiation Response) ──
- id: m22-043
  expression: "I agree with you, we need to get X as soon as we can. If we cannot do it in Y, then we will have to work through Z"
  category: conditional_agreement
  function: agree_with_condition
  speaker_role: negotiator
  difficulty: 5
  context: "I agree with you, we need to get 1C as soon as we can. If we cannot do it in NPI, then we will have to work through the sustaining lab to see how quickly after Venice launch it can be added."

- id: m22-044
  expression: "I want to give the NPI team enough time to do their due diligence rather than give you an answer tonight and find out I was wrong."
  category: deferral_with_reason
  function: careful_delay
  speaker_role: negotiator
  difficulty: 5
  context: "I want to give the NPI team enough time to do their due diligence in analyzing the schedule rather than give you an answer tonight and find out I was wrong."
  note: 답변 보류의 황금 공식. 무조건 외울 것.

- id: m22-045
  expression: "we will analyze our schedule and see if we can get it into the NPI qual"
  category: investigate_promise
  function: follow_up_commit
  speaker_role: negotiator
  difficulty: 3
  context: "we will analyze our schedule and see if we can get it into the NPI qual"

- id: m22-046
  expression: "we will give you more updates in Q2 timeframe after we have discussion with X"
  category: update_promise
  function: timeline_commit
  speaker_role: presenter
  difficulty: 3
  context: "we will give you more updates in Q2 timeframe after we have discussion with RCD Bander and also the FCC Bander"

- id: m22-047
  expression: "Many of these, we continue to have discussions with more customers. So my answer could change tomorrow with additional customer input."
  category: position_volatility
  function: change_disclosure
  speaker_role: negotiator
  difficulty: 4
  context: "Many of these, we continue to have discussions with more customers. So my answer could change tomorrow with additional customer input."
  note: 포지션 변동성 사전 공지 - 정직한 화법

# ── Action Item 화법 ──
- id: m22-048
  expression: "will you take an action item for us to X"
  category: action_item_assign
  function: formal_assignment
  speaker_role: presenter
  difficulty: 4
  context: "Michael, will you take an action item for us to chat with our thermal guys and see if they'd be willing to have a discussion with SK Heinecks."

- id: m22-049
  expression: "I would say yes, but I know I will probably forget by tomorrow. I do not have SDDC."
  category: humorous_acceptance
  function: action_item_accept
  speaker_role: negotiator
  difficulty: 5
  context: "I would say yes, but I know I will probably forget by tomorrow. I do not have SDDC."
  note: 유머 + action item 수락. 자가调侃으로 책임 무게 줄임.

- id: m22-050
  expression: "My brain does not have SDDC. So I know I will forget."
  category: self_deprecation
  function: memory_disclaimer
  speaker_role: negotiator
  difficulty: 4
  context: "My brain does not have SDDC. So I know I will forget."

- id: m22-051
  expression: "I will contact Michael once again."
  category: self_follow_up
  function: personal_commit
  speaker_role: negotiator
  difficulty: 2
  context: "I will contact Michael once again."

- id: m22-052
  expression: "let me check the real measurement data for X and get back to you"
  category: data_follow_up
  function: data_commit
  speaker_role: presenter
  difficulty: 3
  context: "So let me check the real measurement data for at 6400 speeds to 1DPC and 2DPC. Yep. And get back to you."

# ── 정중한 데이터 요청 (Polite Data Request) ──
- id: m22-053
  expression: "I know I'm asking for something very difficult that you might not be able to provide, but any guidance can be helpful."
  category: difficult_request
  function: polite_preface
  speaker_role: negotiator
  difficulty: 5
  context: "I know I'm asking for something very difficult that you might not be able to provide, but any guidance can be helpful."
  note: 어려운 요청의 정중 전제. 무조건 외울 것.

- id: m22-054
  expression: "Even if it's a very conservative, high estimate that is probably way too high, it's better than no estimate."
  category: accept_conservative
  function: imperfect_accept
  speaker_role: negotiator
  difficulty: 4
  context: "Even if it is a very high, even if it's a very conservative, high estimate that is probably way too high, it's better than no estimate."

- id: m22-055
  expression: "I can't tell you how critical this data is to us."
  category: importance_emphasis
  function: critical_stress
  speaker_role: negotiator
  difficulty: 3
  context: "I can't tell you how critical this data is to us. Memory thermals have become a significant challenge."

# ── 마무리 (Closing) ──
- id: m22-056
  expression: "Thank you very much SKINX for a very productive discussion. We really appreciate it. And we look forward to the next one and for our further engagement on the actions."
  category: closing
  function: formal_close
  speaker_role: negotiator
  difficulty: 3
  context: "Thank you very much SKINX for a very productive discussion. We really appreciate it. And we look forward to the next one and for our further engagement on the actions."

- id: m22-057
  expression: "if there are follow up questions, please feel free to contact me"
  category: follow_up_channel
  function: open_contact
  speaker_role: presenter
  difficulty: 2
  context: "if you have any questions after the meeting, please feel free to contact me"

- id: m22-058
  expression: "we have kicked the tires on an appliance. Right now, it is not POR."
  category: evaluation_status
  function: informal_evaluation
  speaker_role: negotiator
  difficulty: 4
  context: "I know that we have kicked the tires on an appliance. Right now, it is not POR."
  note: "kick the tires" - 자동차 타이어 차듯 가볍게 평가 - 비유적 표현

# ── 도메인 특화 (CXL/메모리) ──
- id: m22-059
  expression: "CXL is primarily a capacity expansion. And MRDim is primarily a bandwidth expansion."
  category: market_segment
  function: segment_definition
  speaker_role: negotiator
  difficulty: 4
  context: "our view on CXL is it is primarily a capacity expansion. And MRDim is primarily a bandwidth expansion."

- id: m22-060
  expression: "I can see AI uses for both."
  category: balanced_view
  function: dual_use_acknowledge
  speaker_role: negotiator
  difficulty: 3
  context: "And so I can see AI uses for both."
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-12 09 34 28_EN_HPE_QTR_Q1-extracted.wav` (총 ~854 lines, 10,507단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 라인 범위 | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입 - Microsoft 도전 (line 16-25) | 16-25 | Eric: "all math correct, but assumption valid?" + "if base assumption not valid, doesn't matter" | 가장 고급 도전 화법 - math/assumption 분리 | ★★★★★ |
| 2 | 정량화 도전 (line 25-52) | 25-52 | "good enough - not quantifiable" + 100 servers scale expansion + quality excursion 시나리오 | 정량화 요구 + 스케일 확장 도전 | ★★★★ |
| 3 | Doyeon 로드맵 발표 (line 280-360) | 280-360 | "contents same except 24Gb" + "1Cnm main from 2H 2026" + "sample ready end of Feb" + "highly recommended" | Type B 로드맵 발표 6단계 전체 | ★★★ |
| 4 | MRDIM 포지션 협상 (line 444-504) | 444-504 | "I have to be careful with my position" + "me as simple engineer" + "if only offer one, more business with LP" | 포지션 협상 + 부서 한계 명시 | ★★★★ |
| 5 | action item 유머 (line 226-235) | 226-235 | Michael action item + "I do not have SDDC" + "my brain does not have SDDC" | action item 유머 수락 - 회의 분위기 희석 | ★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 1, 4가 가장 가치 높음 - 도전/포지션 협상 화법이 밀집
- 발췌 3은 Type B 발표자의 뼈대 - 매분기 QBR 발표 전 필수 복습

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap pitch + spec negotiation + position coordination** register다. 세 가지 발화 역할이 섞여 있다:
- **로드맵 발표자 (Doyeon, Steve Gu)**: timeline target + recommendation + question invitation - 네가 매분기 HPE에 발표할 때
- **기술 도전자 (Eric)**: math/assumption 도전 + 정량화 요구 + 스케일 확장 - 네가 Microsoft/Intel 제안을 도전할 때
- **포지션 협상자 (Eric, Michael)**: careful position + 부서 한계 + 개인 vs 회사 분리 - 네가 사내 다수 부서 의견을 조율할 때

### Pragmatics (화용론) 핵심

1. **"Math correct / Assumption invalid"**: 영어 도전의 최고급 화법. 상대 수식을 인정하면서 가정을 도전 - 기싸움 없이 기술 논의. "you're wrong"이 아니라 "your assumption may not hold". 이게 Eric이 Microsoft를 12년 주장까지 도전한 핵심 화법.

2. **"Until I decide otherwise, my position is X"**: 결정 보류의 명확한 공식. "we will consider"는 약하고, "I'll think about it"은 너무 비격식. "until I decide otherwise"가 포지션을 명시하면서 결정을 미루는 정중하고 단호한 화법.

3. **"timeframe"의 완충**: "end of February timeframe" - "timeframe"을 붙이면 일정에 여유가 생긴다. "end of February"만 하면 약속이고, "timeframe"이면 가이드. SK가 매번 이걸 붙이는 게 일정 약속의 완충제. 네가 timeline을 말할 때 무조건 "timeframe"을 붙여.

4. **"nice to have"**: 우선순위를 낮추는 정중한 화법. "256 might be nice to have. But I don't have direct customer data that pushes me there." - 욕구를 표현하되, 필수가 아님을 명시. 협상에서 부담을 줄이는 화법.

5. **"I do not have SDDC"**: 기술 회의에서 기술 용어로 자가调侃. "내 뇌에 SDDC가 없다" - action item을 수용하되 자기가 잊을 수 있다는 걸 유머로 면책. 분위기를 희석하면서 책임은 인정. 이게 고급 action item 수락 화법이다.

### 네가 당장 써야 할 Top 5
1. **"all of their math is correct, but trying to determine if the base assumption is valid"** - 수식 인정 + 가정 도전 (Microsoft/Intel 제안 도전 시)
2. **"until I decide otherwise, my position is X is required"** - 포지션 보류 (HPE 포지션 요청 시)
3. **"I have to be very careful with my position because X. But I can't say absolutely no Y"** - 조심스러운 포지션 (다 부서 의견 엇갈릴 때)
4. **"I want to give the team enough time to do due diligence rather than give you an answer tonight and find out I was wrong"** - 답변 보류 + 사유
5. **"I know I'm asking for something very difficult, but any guidance can be helpful"** - 어려운 데이터 요청의 정중 전제

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "수식은 맞는데 가정이 틀린 것 같습니다" | "all of their math is correct, but trying to determine if the base assumption is valid" | 한국어는 직접 "틀린 것 같다", 영어는 "trying to determine if valid"로 탐색형 |
| "검토해 보겠습니다" | "until I decide otherwise, my position is X is required" | 한국어는 미루기만, 영어는 기본 포지션 명시 + 결정 미루기 |
| "업젼으로 회의해 보겠습니다" | "me as a simple engineer, that might be okay. Procurement might have a different answer." | 한국어는 부서 언급만, 영어는 자기 권한 한계 + 타 부서 명시 |
| "팀에 시간 주겠습니다" | "I want to give the NPI team enough time to do due diligence rather than give you an answer tonight and find out I was wrong" | 한국어는 짧게, 영어는 사유까지 붙여 설득력 강화 |
| "어려운 요청인데요" | "I know I'm asking for something very difficult, but any guidance can be helpful" | 한국어는 사과, 영어는 어려움 인정 + 도움 가능성 강조 |
| "다음에 답변드리겠습니다" | "I do not have SDDC. I will contact Michael once again." | 한국어는 건조, 영어는 유머로 분위기 희석 |
| "있으면 좋겠습니다" | "X maybe might be nice to have. But I don't have direct customer data that pushes me there." | 한국어는 짧게, 영어는 "nice to have" + 이유 명시 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 60개 표현 중, 8절 Top 5부터 우선 숙지
3. **Type B 발표자 훈련**: 매분기 QBR 1주 전, 발췌 3(Doyeon 로드맵 발표)을 매일 반복
4. **도전 화법 훈련**: Microsoft/Intel 제안 도전이 필요할 때, 발췌 1, 2(Eric 도전)를 집중 shadowing
5. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
6. **Audrey 금요일 교정**: 2절 회피 화법(m22-024 ~ m22-032)과 4절 포지션 협상(m22-033 ~ m22-047)을 중심으로 dump 작성
7. **유머 훈련**: 2절 전략 6의 "I do not have SDDC" - 기술 회의에서 자가调侃 유머를 연습

---

*Textbook 22 - HPE QTR Q1 (2026-02-12). 회의 유형 B (Roadmap/Supply alignment). 표현 DB 60개. 5개 발췌 구간. 작성: 2026-09-01.*
