---
textbook_id: 05
meeting: NVIDIA 1H (HBM4E/HBM4 ATI samples, Revision BB, HBM5 roadmap)
date: 2026-08-13
type: C (sample/schedule coordination) - confirmed after reading
partner: NVIDIA (Rubin / Rubin Ultra platform owners, NVDA side)
sk_side: SK Hynix HBM Business Enabling, HBM5 design, US on-site engineers, Eun-sang (on-site lead), Danny (HBM Business Enabling Team)
duration_words: 4638
audio: repo/webex-audio/2026-08-13 11 03 28_EN_NVIDIA_1H-extracted.wav
transcript: repo/webex-audio/2026-08-13 11 03 28_EN_NVIDIA_1H-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, nvidia, hbm4e, hbm4-ati, hbm5, revision-bb, sample-coordination, schedule-pull-in]
---

# Textbook 05 - NVIDIA 1H: HBM4E/HBM4 ATI samples, Revision BB, HBM5 (2026-08-13)

> **회의 유형**: C (sample/schedule coordination) - SK Hynix가 NVIDIA에 sample schedule·volume·pull-in 요청을 조율하는 회의
> **학습 가치**: 일정 조율(volume/timeline pull-in, ES/CS/MP 언어), 정중한 push-back, sample 목적 framing, 두 엔지니어링 조직간 milestone alignment
> **Audrey 관점**: 이 회의는 "공급자-고객 일정 협상"의 전형 - 네가 SK Hynix 입장(NVIDIA에 sample·schedule 요청)에서든 NVIDIA 입장(타이트한 timeline push-back)에서든 둘 다 배워야. 특히 "we would like to propose pull-in"과 "we cannot delay our overall schedule" 같은 정중한 push-back이 핵심

---

## 1. 발화 아키텍처 - SK 측 발표자의 일정 조율 설계 (5단계)

이 회의는 SK Hynix가 NVIDIA에 sample plan과 schedule을 발표하며 조율하는 구조. 발표자(Danny 중심, 일정 담당자)는 5단계 구조로 발표를 설계한다. 각 단계마다 **고정된 화법 공식**이 있다.

### 단계 1: 상황 정합 (Status Alignment)

발표자는 먼저 "이전에 합의한 것"을 회상하며 시작한다. 새 제안을 하기 전, 양측의 합의 지점을 먼저 확인.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `a couple of ago we discussed X at max and also embedded confirmed Y` | "a couple of ago we discussed 16 gigabytes per second at max and also embedded confirmed the eight high state SPOR" | 과거 합의 회상 - "a couple of [weeks] ago"로 이전 대화 인용 |
| `Yeah no difference we basically we think` | "Yeah no difference we basically we think" | 차이 없음 확인 - 변경 없음 표시 |
| `one additional request from our side is that X` | "one additional request from our side is that the also the testing revision PB for the higher speed" | "additional request" - 새 요청을 "추가"로 포장 |

**Audrey 교훈**: 영어 협상 발표는 "새 요청"으로 시작하지 않는다. **"이전에 합의한 것"**으로 시작한다. "a couple of [weeks] ago we discussed X" - 이 공식을 외워. 회의에서 새 요청을 할 때, 먼저 "저번에 합의한 부분은 이거고, 그 위에 additional request가 있다"로 포장해야 한다. 한국어 "저번에 말씀드린 건 그대로고요, 하나 추가하자면"의 영어 버전.

### 단계 2: Sample 계획 제시 (Sample Plan Reveal)

sample type(ES/CS), 수량, 시점을 나열하며, "purpose"를 명시해 sample의 쓰임새를 frame.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we will ship initial sample X on Y, which is going to be our first initial sample for Z` | "we will ship initial sample 1KES on 18th of August, which is, yeah, that's going to be our first initial sample for HBM4 ATI" | sample type + 시점 + "first initial" 강조 |
| `the purpose of [us/you] providing the sample is to verify X` | "the purpose of your providing the sample is to verify our baseline performance validation" | sample 목적 framing - "purpose is to verify" |
| `we'd like to see how much fmax we can achieve on the system level` | "we'd like to see how much fmax we can achieve on the system level" | 기대 효과 - "how much X we can achieve" |

**Audrey 교훈**: sample을 보낼 때 "we will ship X on Y"는 기본이고, 반드시 **"purpose is to verify Z"**를 붙여. 단순 sample 전달이 아니라 "검증 목적"을 명시해야 상대방이 sample의 활용 방식을 이해한다. 그리고 "we'd like to see how much X we can achieve" - 기대 효과를 "보고 싶다"로 표현. "we expect X"보다 "we'd like to see"가 더 협조적이다.

### 단계 3: 수량·시점 분할 (Volume & Timeline Split)

수량을 한 번에 아니라 분할 배송으로 제안하며, 상대방 부담을 줄이는 "steady flow"로 포장.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we plan to split this into X units for Y weeks so that it could provide a steady flow on your Z` | "we plan to split this into 500 units for six weeks so that it could provide a steady flow on your [build]" | 분할 배송 + "steady flow" - 부담 완화 포장 |
| `our previous plan is to ship every X by end of Y` | "our previous plan is to ship every 3k by end of October" | 이전 계획 회상 - 비교 기준 제시 |
| `we're trying to pull in as much as possible and make it even` | "we're trying to pull in as much as possible and make it even" | "pull in" - 일정 앞당기기 + "make it even" - 균등 분배 |

**Audrey 교훈**: "pull in"은 반도체 일정 협상의 핵심 동사다. "앞당기다" - 한국어. "We're trying to pull in as much as possible" - "최대한 앞당기려 하고 있습니다". 그리고 "make it even" - "균등하게 분배하다". 분할 배송을 제안할 때 "steady flow"라는 명사를 써. "규칙적 흐름"이라는 포장으로, 상대방의 ramp 부담을 완화한다.

### 단계 4: 상대방 일정과 alignment 명시 (Customer Alignment)

자신의 sample plan이 상대방 timeline과 맞물린다는 것을 명시하며, "align" 동사를 반복 사용.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we also wanted to align the closing deal schedule with our X ramping up plan` | "we also wanted to align the closing deal schedule with our a time ramping up plan" | "align X with Y" - 일정 정렬 공식 |
| `we are targeting April MP for this HPM for a time` | "we are targeting April MP. For this HPM for a time" | "targeting X MP" - 양산 목표 명시 |
| `we'd like to know if this sample support plan is good enough or competitive enough to make sure and to be aligned with your X` | "we'd like to know if this sample support plan is good enough or competitive enough to make sure and to be aligned with your ruby no truck [Rubin Ultra] close bill [close build]" | "good enough or competitive enough" - 자체 평가 요청 |
| `once we have a new update or new feedback from X team, yeah, we'd like, yeah, we will definitely try our best to adjust our sample plan` | "once we have a new update or new feedback from a video team, yeah, we'd like, yeah, we will definitely try our best to adjust our sample plan" | 유연성 표시 - "definitely try our best to adjust" |

**Audrey 교훈**: "align X with Y" - 일정 협상의 가장 중요한 동사. "맞추다" - 한국어. "align the closing deal schedule with our ramping up plan" - "close build 일정을 우리 ramp-up plan에 맞추고 싶다". 그리고 "we'd like to know if this plan is good enough or competitive enough" - 자체 평가를 상대방에게 부탁하는 화법. "충분한가요?"라고 직접 묻는 것보다 "good enough or competitive enough"로 평가 기준을 명시하면 더 진지하게 들린다.

### 단계 5: 후속 협의 약속 (Follow-up Commitment)

발표 끝에 "we will keep checking", "we are going to keep updating"으로 지속 협의 약속.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we need to keep the discussion and for X schedule` | "we we need to keep the discussion and for customer HM5 schedule" | "keep the discussion" - 협의 지속 약속 |
| `we are going to keep checking the overall progress with them` | "we are going to keep checking the overall progress with them" | "keep checking" - 진행 모니터링 약속 |
| `we are also keep updating our schedule` | "we are also keep updating our schedule" | "keep updating" - 지속 갱신 약속 |
| `we'd like, yeah, we will definitely try our best to adjust our sample plan or related things` | "we'd like, yeah, we will definitely try our best to adjust our sample plan or yeah, some, yeah, related things" | "definitely try our best to adjust" - 유연성 + 진지함 |

**Audrey 교훈**: 일정 협상 발표의 끝은 "keep V-ing" 패턴 - "keep the discussion", "keep checking", "keep updating". "계속 하겠다" - 한국어. 영어는 "keep V-ing"으로 지속성을 강조. 그리고 "definitely try our best to adjust" - "adjust" 동사가 핵심. "변경하겠다"가 아니라 "조정하겠다" - 부담이 적고 유연하게 들린다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 양측이 일정 부담·스펙 한계를 어떻게 정중하게 포장하는지.

### 전략 1: 한계 인정 + 사유 명시 (Limitation with Reason)

SK 측은 "16 Gbps 보장 못 함"을 인정하되, 즉시 "core die speed limits"로 사유를 명시하고 "lower bin" 대안을 제시.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| 16 Gbps 보장 불가 | "the speed we discussed 16 people second SF max but that's not that we meant that we can deliver 16 gigabit PS without any rules so we are targeting we we our design target of our IP is targeting for 16 people but due to the core die speed limits there will be another lower bin for example 14.4 gigapis for customer HM4E" | "16 Gbps를 논의했지만, 16 Gbps를 어떤 규칙 없이 deliver한다는 뜻은 아닙니다. 우리 IP 설계 타겟은 16이지만, core die speed limits 때문에 14.4 Gbps 같은 lower bin이 있을 겁니다" |

**패턴 공식**: `That's not that we meant that we can deliver X without any rules. Our design target is X, but due to Y limits, there will be a lower bin for example Z.`

**Audrey 교훈**: "보장 못 함"을 말할 때 "we can't"으로 시작하지 마라. "That's not that we meant that we can deliver X without any rules" - "규칙 없이 deliver한다는 뜻은 아니었습니다" - 부정을 과거 합의의 정정으로 포장. 그리고 "due to Y limits" - 한계 원인을 명시. 한국어 "core die 속도 때문에 어렵습니다"의 영어 버전이 "due to the core die speed limits"다. "limit" 명사가 전문가 뉘앙스.

### 전략 2: 수치 미확정 회피 (Number Not Ready)

스펙 비율을 묻는 질문에 "we are not ready to say the number right now"로 정중하게 회피.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| BB 분할 비율 | "we still want need to see the revision BB reserve right now so it's really we we are not ready to say the number right now" | "BB 결과를 봐야 합니다. 지금은 수치를 말할 준비가 안 됐습니다" |

**패턴 공식**: `We still need to see X. We are not ready to say the number right now.`

**Audrey 교훈**: 수치를 모를 때 "I don't know"는 약하다. "We are not ready to say the number right now" - "지금은 수치를 말할 준비가 안 됐습니다" - "모른다"가 아니라 "준비가 안 됐다"로 포장. 그리고 "still need to see X"로 사유를 먼저 제시. 회의에서 정확한 수치를 피하고 싶을 때 이 패턴을 써.

### 전략 3: "정말 그렇고 싶지만" 무게감 부여 (Sincerity Hedging)

NVIDIA 측이 "we really want to see X"를 반복하며 요청의 무게감을 더하고, SK 측은 "we understand"로 공감 후 push-back.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| BB 결과 조기 확인 요청 | "we'd like to see the revision BB result as soon as possible. And not just for the NPI perspective, we'd like to see the speed result as well for five months" | "BB 결과를 최대한 빨리 보고 싶습니다. NPI 관점뿐 아니라, 5개월 동안 speed 결과도 보고 싶습니다" |
| SK 공감 후 push-back | "We understand. But revision BB is... it would be better if we can get the result by end of October... But it seems a little bit delayed. So it may not be possible." | "이해합니다. 하지만 BB는... 10월 말까지 결과를 얻으면 더 좋겠지만... 조금 지연되어 가능하지 않을 수 있습니다" |

**패턴 공식**: `[요청 측] we'd like to see X as soon as possible, not just for Y, we'd like to see Z as well` → `[응답 측] We understand. But it would be better if we can get X by Y. But it seems a little bit delayed. So it may not be possible.`

**Audrey 교훈**: 요청을 강화할 때 "as soon as possible"을 쓰되, "not just for X, we'd like to see Y as well"로 이유를 덧붙여. 단순 "빨리요"가 아니라 "NPI 때문만 아니라 speed도 보고 싶다" - 이유가 둘이면 설득력이 두 배. 응답 측은 "We understand"로 먼저 공감하고, "But"로 push-back. "It seems a little bit delayed" - "조금 지연되어" - "little bit"로 부드럽게. "So it may not be possible" - "불가능할 수 있다" - "can't"가 아니라 "may not be possible"로 가능성 부정.

### 전략 4: "우리 마음은 그렇지만" 무력화 (Concession Softening)

NVIDIA 측이 SK의 pull-in 제안에 "we hope that you can utilize our X"로 의무를 완화하려 시도.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| pull-in 요청 무력화 | "We still... We hope that you can utilize our... From working sample, November, end of November, you can... Should be CES. More than quarter." | "11월 말 working sample을 활용하시길 바랍니다. CES까지, 분기 넘게" |

**패턴 공식**: `We hope that you can utilize our X. From Y timeline, you can [achieve Z].`

**Audrey 교훈**: 상대의 pull-in 요청을 거절할 때 "we can't" 대신 "we hope that you can utilize X" - "X를 활용하시길 바랍니다" - 거절을 "활용 제안"으로 포장. "hope" 동사가 핵심 - 요청을 강제하지 않고 "희망"으로 표현. 회의에서 거절할 때 이 패턴을 써.

### 전략 5: 위험 분산 주장 (Risk Distribution Argument)

NVIDIA 측이 revision AA와 BB의 공통성을 주장하며, AA에서 발견된 이슈가 BB에도 해당한다는 논리로 AA 시험 정당화.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| AA 시험 정당화 | "just think it, just hypothetically, if there is an issue without, if there is an issue in the rapid A or rapid B, if there is an issue in the rapid A, that issue will be also probably in the rapid B as well. So we want to clarify all the risks in the rapid A as well" | "가정해 봅시다. rev A나 rev B에 이슈가 있다면, rev A의 이슈는 rev B에도 있을 겁니다. 그래서 rev A의 모든 위험을 clarify하고 싶습니다" |

**패턴 공식**: `Just hypothetically, if there is an issue in X, that issue will be probably in Y as well. So we want to clarify all the risks in X as well.`

**Audrey 교훈**: "just hypothetically" - "가정해 봅시다" - 가정법으로 공격을 부드럽게. 그리고 "we want to clarify all the risks in X" - "모든 위험을 clarify하고 싶다" - "테스트하겠다"가 아니라 "위험을 clarify하겠다" - 목적을 "위험 관리"로 포장. 회의에서 추가 요청을 정당화할 때, "위험 분산" 논리를 써.

### 전략 6: 비용 관점 전환 (Cost Reframe)

NVIDIA 측이 "비즈니스 관점에서 초기 점검이 비용을 줄인다"는 논리로 요청을 강화.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 초기 시험 정당화 | "Mentally, I agree. But, you know, this business wise, checking the board staff in the beginning, reduced all the costs" | "정신적으로는 동의합니다. 하지만 비즈니스 관점에서, 초기에 보드를 점검하면 모든 비용이 줄어듭니다" |

**패턴 공식**: `Mentally, I agree. But business wise, checking X in the beginning, reduced all the costs.`

**Audrey 교훈**: "Mentally, I agree" - "정신적으로는 동의" - 한국어로는 어색하지만, 영어로는 "이론적으로는 동의하지만 실무적으로는"의 뉘앙스. "business wise" - "비즈니스 관점에서" - 기술 논리를 비즈니스 논리로 전환. 회의에서 기술 동의를 확보한 후, 비용 논리로 밀어붙일 때 "business wise"를 써.

---

## 3. 정중한 도전 화법 (질문자의 기술 probe)

이 회의의 질문은 "정중한 일정 probe"가 중심. SK 측이 NVIDIA의 timeline 요구를 probe하고, NVIDIA 측이 SK의 sample plan을 점검.

### 질문 유형 1: 이전 합의 회상형 (Prior Agreement Recall)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `a couple of [weeks] ago we discussed X at max and also embedded confirmed Y` | "a couple of ago we discussed 16 gigabytes per second at max and also embedded confirmed the eight high state SPOR" | 과거 합의 인용 - 현재 제안의 정당성 확보 |

**Audrey 교훈**: 회의에서 "저번에 합의한 것"을 인용하면 발언의 정당성이 확보된다. "a couple of [weeks] ago we discussed X" - "몇 주 전에 X를 논의했고" - 이 회의에서 SK 측이 가장 자주 쓴 화법. 한국어 "저번에 말씀하신 거"의 영어 버전.

### 질문 유형 2: 추가 요청 포장 (Additional Request Softening)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `one additional request from our side is that X` | "one additional request from our side is that the also the testing revision PB for the higher speed" | "additional" - 새 요청을 "추가"로 포장 |

**Audrey 교훈**: 새 요청을 할 때 "we want X"가 아니라 "one additional request from our side is X" - "우리 측 추가 요청 하나는 X입니다" - "추가"로 부담을 완화. "from our side" - "우리 측에서" - 요청 주체를 명시하되, "we want"의 직접성을 피한다.

### 질문 유형 3: 가정법 probe (Hypothetical Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `just think it, just hypothetically, if there is an issue in X, that issue will be also probably in Y` | "just think it, just hypothetically, if there is an issue without, if there is an issue in the rapid A or rapid B, if there is an issue in the rapid A, that issue will be also probably in the rapid B as well" | 가정법으로 공격 부드럽게 |

**Audrey 교훈**: "just hypothetically" - "가정해 봅시다" - 공격적 질문을 정중하게 만드는 핵심 화법. "if there is an issue in X, that issue will be probably in Y" - 가정법으로 논리를 제시. 한국어 "만약 그렇다면"의 영어 버전이 "just hypothetically, if X"다. 회의에서 도전적 질문을 할 때, 이 말을 먼저 붙여.

### 질문 유형 4: "필요하면 더" 유연성 표시 (Volume Flexibility)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `if you want to have another sample or more sample over X, we can revisit our numbers` | "If you want to have another sample or more sample over revision BB, we can revisit our numbers" | "revisit our numbers" - 수량 재협의 암시 |
| `if you need more, then we can discuss internally and get back to you` | "If you need more, then we can discuss internally and get back to you" | "discuss internally and get back" - 내부 논의 후 회신 |

**Audrey 교훈**: 수량 협상에서 "if you need more" - "더 필요하시면" - 유연성을 먼저 표시. "we can revisit our numbers" - "수량을 다시 볼 수 있습니다" - "재협의하겠다"의 정중한 표현. "revisit" 동사가 핵심 - "재검토하다". 그리고 "discuss internally and get back to you" - "내부 논의 후 회신" - 회의에서 자주 쓰는 follow-up 화법.

### 질문 유형 5: "이해가 맞는지 확인" (Understanding Check)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `but if our understanding is not correct, please...` | "But if our understanding is not correct, please..." | "이해가 틀리면 알려달라" - 정중한 확인 |
| `please let us know if it's wrong, so that we can prepare the engineer resource to bring up the RUPT test vehicle` | "please let us know if it's wrong, so that we can prepare the engineer resource to bring up the RUPT test vehicle" | "틀리면 알려달라, 우리가 준비할 수 있게" - 목적 명시 |

**Audrey 교훈**: "if our understanding is not correct, please [let us know]" - "이해가 틀리면 알려달라" - 상대방 정보를 확인할 때 쓰는 정중 화법. "틀리면"으로 시작하면 상대방이 "내 설명이 부족했나?"라고 느끼지 않는다. 그리고 "so that we can prepare X" - "우리가 X를 준비할 수 있게" - 확인의 목적을 명시하면 더 진지하게 들린다.

### 질문 유형 6: 우선순위 probe (Priority Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `please let us know your priority or your...` | "So please let us know your priority or your... Yeah, sure" | "우선순위를 알려달라" - 자원 배분 협의 |

**Audrey 교훈**: 여러 작업이 겹칠 때 "please let us know your priority" - "우선순위를 알려달라" - 직접적이면서 정중. 회의에서 자원 한계를 협의할 때, 우선순위를 묻는 것이 갈등을 줄인다. 한국어 "어떤 것을 먼저 할까요?"의 영어 버전이 "please let us know your priority"다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 핵심 - 일정 협상, pull-in 요청, milestone coordination.

### 4.1 Pull-in 요청 화법 (Pull-in Request)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| pull-in 배경 설명 | SK | "we already got the request to put in our over final IP drop schedule by two months and based on your roadmap we also need to put in our CS timeline by maybe three months I guess" | "우리 IP drop schedule을 2개월 앞당기라는 요청을 받았고, 로드맵 기준 CS timeline도 3개월 앞당겨야 합니다" |
| 조건부 가능 시사 | SK | "if the bump bump map and specification fix as we expected then we can have a room to put in our overall design" | "bump map과 spec이 예상대로 fix되면, 전체 design을 앞당길 여유가 있습니다" |
| "room to" 여유 표시 | SK | "we can have a room to put in our overall design" | "room to X" - "X할 여유" - 가능성 시사 |
| "we are targeting" timeline 명시 | SK | "we are targeting the April's 27" | "4월 27일 타겟" - 목표 시점 명시 |

**Audrey 교훈**:
- "pull in X by Y" - "X를 Y만큼 앞당기다" - 반도체 일정 협상의 핵심 동사. "pull in by two months" - "2개월 앞당기다".
- "we can have a room to X" - "X할 여유가 있다" - 조건부 가능성 시사. "yes"가 아니라 "room"으로 가능성을 열어둬.
- "we are targeting X" - "X를 타겟하고 있다" - 목표 시점 명시 공식. "we will"보다 "we are targeting"이 더 협상적 - 목표는 바뀔 수 있다는 뉘앙스.

### 4.2 Push-back 화법 (Polite Refusal)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 일정 유지 선언 | SK | "currently we are keep our schedule but anyhow there are lots of all the design phase work between NVIDIA and HSSK hynix" | "현재 schedule을 유지하고 있지만, NVIDIA와 SK Hynix 사이에 design phase 작업이 많습니다" |
| 조건부 가속 | SK | "if the bump bump map and specification fix as we expected then we can have a room to put in our overall design" | "bump map과 spec이 fix되면 design을 앞당길 여유가 있습니다" |
| 부정 + 사유 | SK | "putting in the revision BB schedule is not possible due to the early effect processing and early delete time" | "BB schedule을 앞당기는 것은 early effect processing과 early delete time 때문에 불가능합니다" |
| "we cannot delay" 한계 명시 | NV | "But we cannot delay our overall revision BB schedule. So we are going to release our meta-layer without revision AA result so that we can meet the overall revision BB schedule." | "하지만 전체 BB schedule을 delay할 수 없습니다. 그래서 AA 결과 없이 meta-layer를 release하여 BB schedule을 맞추겠습니다" |

**Audrey 교훈**:
- "we are keep our schedule" - "schedule을 유지하고 있습니다" - 직접적 거절. "but anyhow there are lots of work"로 사유를 붙여.
- "is not possible due to X" - "X 때문에 불가능합니다" - 부정 + 사유의 정중한 거절 공식.
- "we cannot delay our overall X schedule" - "전체 X schedule을 delay할 수 없습니다" - 한계 명시. "we can't"보다 "we cannot delay"가 더 단호하면서 정중.

### 4.3 Sample 요청·수량 협상 (Sample Request)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| hot run 요청 | NV | "one request on this one KES sample is to we are asking for a hot run for the course build because getting early fit back from this lot would let us reflect it into the November ramping up samples" | "1K ES sample에 대한 요청 하나는 course build에 hot run을 요청합니다. 이 lot의 early feedback을 November ramping up sample에 반영할 수 있게" |
| "we are asking for" 요청 | NV | "we are asking for a hot run for the course build" | "we are asking for X" - 요청 공식 |
| 이유-효과 연결 | NV | "getting early fit back from this lot would let us reflect it into the November ramping up samples" | "early feedback을 November sample에 반영" - 요청의 정당화 |
| 수량 분할 제안 | SK | "we plan to split this into 500 units for six weeks so that it could provide a steady flow on your [build]" | "500개씩 6주로 분할하여 귀사 build에 steady flow를 제공" |
| 더 필요시 재협의 | SK | "If you need more, then we can discuss internally and get back to you" | "더 필요하시면 내부 논의 후 회신" |

**Audrey 교훈**:
- "we are asking for X" - "X를 요청합니다" - 요청의 공식적 표현. "we want"보다 "asking for"가 더 정중.
- "getting early feedback would let us reflect it into Y" - "early feedback을 Y에 반영할 수 있습니다" - 요청의 효과를 명시. 요청을 할 때는 반드시 "왜 필요한지" 효과를 붙여.
- "steady flow" - "규칙적 흐름" - 분할 배송의 포장. "500 units for six weeks" - 수량과 기간을 명시.

### 4.4 Alignment·follow-up 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| alignment 요청 | SK | "we also wanted to align the closing deal schedule with our a time ramping up plan because we are targeting April MP" | "closing deal schedule을 우리 ramping up plan에 align하고 싶습니다. 4월 MP 타겟이기 때문" |
| 자체 평가 요청 | SK | "we'd like to know if this sample support plan is good enough or competitive enough to make sure and to be aligned with your ruby no truck close bill" | "이 sample plan이 귀사 Rubin Ultra close build에 align되기에 충분한지/경쟁력 있는지 알고 싶습니다" |
| 후속 협의 약속 | SK | "we are going to keep checking the overall progress with them and then we are also keep updating our schedule" | "전체 진행을 keep checking하고 schedule을 keep updating하겠습니다" |
| feedback 환영 | SK | "the speed back about this ruby no truck HPM for a time would be very appreciated" | "Rubin Ultra HBM4 ATI에 대한 speed feedback은 매우 감사하겠습니다" |
| 유연성 표시 | SK | "once we have a new update or new feedback from a video team, yeah, we'd like, yeah, we will definitely try our best to adjust our sample plan or yeah, some, yeah, related things" | "NVIDIA 팀의 새 update/feedback이 오면 sample plan을 adjust하기 위해 최선을 다하겠습니다" |

**Audrey 교훈**:
- "align X with Y" - "X를 Y에 맞추다" - 일정 협상의 핵심 동사. "align the closing deal schedule with our ramping up plan" - "close build 일정을 우리 ramp-up plan에 맞추다".
- "good enough or competitive enough" - "충분한가/경쟁력 있는가" - 자체 평가를 요청할 때 기준을 명시.
- "would be very appreciated" - "매우 감사하겠습니다" - feedback 요청의 정중한 표현.
- "definitely try our best to adjust" - "adjust하기 위해 최선을 다하겠습니다" - "definitely" + "try our best"로 진지함을 두 배.

### 4.5 Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 내부 논의 후 회신 | SK | "we can discuss internally and get back to you" | "discuss internally and get back" - 내부 논의 후 회신 |
| 후속 회의 약속 | SK | "we need to we have another ongoing discussion with the go down team for the detailed milestone for customer HM5" | "고다운 팀과 detailed milestone에 대해 또 다른 논의가 필요합니다" |
| "we will update" 약속 | SK | "Yeah, we will update again. Yeah, all the things." | "모든 것에 대해 다시 update하겠습니다" |
| "we will keep checking" | SK | "we are going to keep checking the overall progress with them" | "전체 진행을 keep checking하겠습니다" |

**Audrey 교훈**: 회의에서 "I'll check"는 약하다. "we can discuss internally and get back to you" - "내부 논의 후 회신" - 책임 명시. "we will update again" - "다시 update하겠습니다" - 지속 갱신 약속. "we will keep checking" - "계속 확인하겠습니다" - 모니터링 약속. 이 세 가지 "future commitment" 동사를 외워.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 HBM/sample/schedule 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **ES** (Engineering Sample) | 엔지니어링 샘플 (초기 검증용) | "we will ship initial sample 1KES on 18th of August" - "1K ES" - 1,000개 ES |
| **CS** (Customer Sample) | 고객 제공 샘플 | "the following sample batches will be CS grade samples from starting September" - "CS grade samples" |
| **MP** (Mass Production) | 양산 | "we are targeting April MP" - "targeting X MP" |
| **bring up** | 하드웨어 초기 구동 검증 | "the additional engineer support for the bring up stage" - "bring up stage" |
| **revision AA / BB** | 칩 리비전 (세대) | "we can update our speed up in portion with revision BB which will be happened in end of this year" - "revision X" |
| **pull in** | 일정 앞당기기 | "we're trying to pull in as much as possible and make it even" - "pull in X" |
| **ramp up** | 양산 전 증산 | "getting early fit back from this lot would let us reflect it into the November ramping up samples" - "ramping up samples" |
| **tape out** | 칩 설계 완료·제조 의뢰 | (간접) "final IP drop schedule" - "IP drop" |
| **DTS** | Design Test Schedule | "we will update the DTS schedule" - "DTS schedule" |
| **bump map** | 범프 배치도 (패키징 설계) | "if the bump bump map and specification fix as we expected" - "bump map fix" |
| **core die** | HBM의 핵심 로직 다이 | "due to the core die speed limits there will be another lower bin" - "core die speed limits" |
| **TSP** (Through-Silicon Via) | 실리콘 관통 비아 | "we wouldn't use the T-SWI at that area. That's why we move the T-SWI from the top edge to the center" - "T-SWI location" |
| **PDN** (Power Distribution Network) | 전력 분배망 | "our stack PDN result, you can see the dramatically reduced numbers" - "stack PDN" |
| **meta-layer** | 칩 설계의 메타 계층 | "we are going to release our meta-layer without revision AA result" - "meta-layer release" |
| **working sample** | 동작 샘플 (ES 이후) | "we will ship out our working sample revision of AA soon, end of August" - "working sample revision of AA" |
| **ATE** (Automated Test Equipment) | 자동 테스트 장비 | "we'd like to see how much fmax we can achieve on the system level and see if we can, if there's anything we'd like, we can adjust or optimize between compared ATE and SET level" - "ATE and SET level" |
| **hot run** | 우선 lot 처리 | "one request on this one KES sample is to we are asking for a hot run for the course build" - "ask for a hot run" |
| **NPI** (New Product Introduction) | 신제품 도입 | "not just for the NPI perspective, we'd like to see the speed result as well" - "NPI perspective" |
| **bin** | 같은 제품의 스피드 등급 | "due to the core die speed limits there will be another lower bin for example 14.4 gigapis" - "lower bin" |
| **steady flow** | 규칙적 배송 흐름 | "it could provide a steady flow on your [build]" - "provide a steady flow" |
| **close build** | NVIDIA 측 build 마감 | "to be aligned with your ruby no truck close bill [build]" - "close build" |
| **fmax** | 최대 동작 주파수 | "we'd like to see how much fmax we can achieve on the system level" - "how much fmax we can achieve" |
| **TMR** (Timing Register) | 타이밍 레지스터 설정 | "if we set the TMRS at the middle of the common timing zone, we can secure both that up and hold margin" - "set the TMRS" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 일정 조율 발표 (Schedule Coordination Presentation) ──
- id: m05-001
  expression: "a couple of [weeks] ago we discussed X at max and also embedded confirmed Y"
  category: prior_agreement_recall
  function: alignment_anchor
  speaker_role: presenter
  difficulty: 4
  context: "a couple of ago we discussed 16 gigabytes per second at max and also embedded confirmed the eight high state SPOR"
  note: 과거 합의 인용 - 현재 제안의 정당성 확보. 회의 시작 화법

- id: m05-002
  expression: "one additional request from our side is that X"
  category: additional_request
  function: request_softening
  speaker_role: presenter
  difficulty: 4
  context: "one additional request from our side is that the also the testing revision PB for the higher speed"
  note: 새 요청을 "추가"로 포장. "we want" 대신 "additional request from our side"

- id: m05-003
  expression: "we will ship initial sample X on Y, which is going to be our first initial sample for Z"
  category: sample_plan_reveal
  function: sample_announcement
  speaker_role: presenter
  difficulty: 3
  context: "we will ship initial sample 1KES on 18th of August, which is going to be our first initial sample for HBM4 ATI"

- id: m05-004
  expression: "the purpose of providing the sample is to verify X"
  category: purpose_framing
  function: sample_justification
  speaker_role: presenter
  difficulty: 4
  context: "the purpose of your providing the sample is to verify our baseline performance validation"
  note: sample 목적 framing - 단순 전달이 아니라 "검증 목적" 명시

- id: m05-005
  expression: "we'd like to see how much X we can achieve on the system level"
  category: expectation_stating
  function: outcome_focus
  speaker_role: presenter
  difficulty: 4
  context: "we'd like to see how much fmax we can achieve on the system level"
  note: "we expect X" 대신 "we'd like to see how much X we can achieve" - 협조적 기대 표현

- id: m05-006
  expression: "we plan to split this into X units for Y weeks so that it could provide a steady flow on your Z"
  category: volume_split
  function: burden_softening
  speaker_role: presenter
  difficulty: 5
  context: "we plan to split this into 500 units for six weeks so that it could provide a steady flow on your [build]"
  note: 분할 배송 + "steady flow" - 상대 부담 완화 포장

- id: m05-007
  expression: "our previous plan is to ship every X by end of Y"
  category: previous_plan_recall
  function: comparison_anchor
  speaker_role: presenter
  difficulty: 3
  context: "our previous plan is to ship every 3k by end of October"

- id: m05-008
  expression: "we're trying to pull in as much as possible and make it even"
  category: pull_in_request
  function: schedule_acceleration
  speaker_role: presenter
  difficulty: 4
  context: "we're trying to pull in as much as possible and make it even"
  note: "pull in" - 반도체 일정 협상 핵심 동사. "make it even" - 균등 분배

- id: m05-009
  expression: "we also wanted to align the X schedule with our Y ramping up plan"
  category: alignment_request
  function: schedule_alignment
  speaker_role: presenter
  difficulty: 5
  context: "we also wanted to align the closing deal schedule with our a time ramping up plan"
  note: "align X with Y" - 일정 협상 가장 중요한 동사

- id: m05-010
  expression: "we are targeting X MP for this Y"
  category: target_milestone
  function: production_goal
  speaker_role: presenter
  difficulty: 3
  context: "we are targeting April MP. For this HPM for a time"
  note: "we are targeting X MP" - 양산 목표 명시. "we will"보다 협상적

- id: m05-011
  expression: "we'd like to know if this sample support plan is good enough or competitive enough to be aligned with your X"
  category: self_evaluation_request
  function: customer_assessment
  speaker_role: presenter
  difficulty: 5
  context: "we'd like to know if this sample support plan is good enough or competitive enough to make sure and to be aligned with your ruby no truck close bill"

- id: m05-012
  expression: "we will definitely try our best to adjust our sample plan"
  category: flexibility_commitment
  function: adaptive_promise
  speaker_role: presenter
  difficulty: 4
  context: "we will definitely try our best to adjust our sample plan or yeah, some, yeah, related things"
  note: "definitely try our best to adjust" - 진지함 + 유연성

- id: m05-013
  expression: "we are going to keep checking the overall progress with them"
  category: follow_up_commitment
  function: monitoring_promise
  speaker_role: presenter
  difficulty: 3
  context: "we are going to keep checking the overall progress with them"

- id: m05-014
  expression: "we need to keep the discussion and for X schedule"
  category: ongoing_discussion
  function: continuous_coordination
  speaker_role: presenter
  difficulty: 3
  context: "we we need to keep the discussion and for customer HM5 schedule"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m05-015
  expression: "That's not that we meant that we can deliver X without any rules"
  category: limitation_acknowledgment
  function: spec_correction
  speaker_role: presenter
  difficulty: 5
  context: "that's not that we meant that we can deliver 16 gigabit PS without any rules"
  note: 한계 인정 - 과거 합의의 정정으로 포장. "we can't" 대신 정중한 정정

- id: m05-016
  expression: "Our design target is X, but due to Y limits, there will be a lower bin for example Z"
  category: limitation_with_reason
  function: spec_alternative
  speaker_role: presenter
  difficulty: 5
  context: "our design target of our IP is targeting for 16 people but due to the core die speed limits there will be another lower bin for example 14.4 gigapis for customer HM4E"
  note: 한계 인정 + 사유 + 대안 제시의 3단 구조

- id: m05-017
  expression: "we are not ready to say the number right now"
  category: number_evasion
  function: precise_refusal
  speaker_role: presenter
  difficulty: 4
  context: "we still want need to see the revision BB reserve right now so it's really we we are not ready to say the number right now"
  note: "I don't know" 대신 "not ready to say the number" - 정중한 회피

- id: m05-018
  expression: "we still need to see X"
  category: precondition_stating
  function: dependency_evasion
  speaker_role: presenter
  difficulty: 3
  context: "we still want need to see the revision BB reserve right now"

- id: m05-019
  expression: "We understand. But it would be better if we can get X by Y. But it seems a little bit delayed. So it may not be possible."
  category: empathic_pushback
  function: polite_refusal
  speaker_role: negotiator
  difficulty: 5
  context: "We understand. But revision BB is... it would be better if we can get the result by end of October... But it seems a little bit delayed. So it may not be possible."
  note: 공감 + push-back 공식. "may not be possible"로 가능성 부정

- id: m05-020
  expression: "we cannot delay our overall X schedule"
  category: firm_boundary
  function: hard_limit
  speaker_role: negotiator
  difficulty: 5
  context: "But we cannot delay our overall revision BB schedule"
  note: 단호한 한계 명시. "we can't"보다 "we cannot delay"가 정중하면서 단호

- id: m05-021
  expression: "we hope that you can utilize our X"
  category: concession_softening
  function: refusal_repackage
  speaker_role: negotiator
  difficulty: 4
  context: "We still... We hope that you can utilize our... From working sample, November, end of November"
  note: 거절을 "활용 제안"으로 포장. "hope" 동사가 핵심

- id: m05-022
  expression: "just hypothetically, if there is an issue in X, that issue will be also probably in Y as well"
  category: hypothetical_probe
  function: risk_argument
  speaker_role: questioner
  difficulty: 5
  context: "just think it, just hypothetically, if there is an issue in the rapid A or rapid B, if there is an issue in the rapid A, that issue will be also probably in the rapid B as well"
  note: 가정법으로 공격 부드럽게. "just hypothetically" - 정중한 도전

- id: m05-023
  expression: "we want to clarify all the risks in X as well"
  category: risk_clarification
  function: request_justification
  speaker_role: questioner
  difficulty: 4
  context: "So we want to clarify all the risks in the rapid A as well"
  note: "테스트하겠다"가 아니라 "위험을 clarify하겠다" - 목적을 "위험 관리"로 포장

- id: m05-024
  expression: "Mentally, I agree. But business wise, checking X in the beginning, reduced all the costs"
  category: cost_reframe
  function: business_argument
  speaker_role: questioner
  difficulty: 5
  context: "Mentally, I agree. But, you know, this business wise, checking the board staff in the beginning, reduced all the costs"
  note: 기술 동의 후 비용 논리로 전환. "business wise" - 비즈니스 관점

- id: m05-025
  expression: "we have confidence in X, but as you know, we always need time to optimize in the system level"
  category: confidence_hedge
  function: optimization_need
  speaker_role: negotiator
  difficulty: 4
  context: "we have confidence in RIPs and BB, but as you know, we always need time to optimize in the system level"

# ── 정중한 도전 (Polite Challenge) ──
- id: m05-026
  expression: "but if our understanding is not correct, please..."
  category: understanding_check
  function: polite_verification
  speaker_role: questioner
  difficulty: 4
  context: "But if our understanding is not correct, please..."
  note: 상대방 정보 확인 - "틀리면 알려달라"

- id: m05-027
  expression: "please let us know if it's wrong, so that we can prepare X"
  category: verification_with_purpose
  function: preparation_justification
  speaker_role: questioner
  difficulty: 4
  context: "please let us know if it's wrong, so that we can prepare the engineer resource to bring up the RUPT test vehicle"
  note: "so that we can prepare X" - 확인의 목적 명시

- id: m05-028
  expression: "please let us know your priority or your..."
  category: priority_probe
  function: resource_allocation
  speaker_role: questioner
  difficulty: 3
  context: "So please let us know your priority or your... Yeah, sure"
  note: 여러 작업 겹칠 때 우선순위 협의

- id: m05-029
  expression: "if you want to have another sample or more sample over X, we can revisit our numbers"
  category: volume_flexibility
  function: renegotiation_offer
  speaker_role: presenter
  difficulty: 4
  context: "If you want to have another sample or more sample over revision BB, we can revisit our numbers"
  note: "revisit our numbers" - 수량 재협의 암시

- id: m05-030
  expression: "if you need more, then we can discuss internally and get back to you"
  category: internal_escalation
  function: deferred_response
  speaker_role: presenter
  difficulty: 3
  context: "If you need more, then we can discuss internally and get back to you"

- id: m05-031
  expression: "we'd like to see the X result as soon as possible"
  category: urgency_request
  function: priority_emphasis
  speaker_role: questioner
  difficulty: 3
  context: "we'd like to see the revision BB result as soon as possible"

- id: m05-032
  expression: "not just for the X perspective, we'd like to see Y as well"
  category: multi_reason_request
  function: justification_stacking
  speaker_role: questioner
  difficulty: 4
  context: "not just for the NPI perspective, we'd like to see the speed result as well for five months"
  note: 이유 덧붙이기 - 설득력 두 배

- id: m05-033
  expression: "the speed feedback about X would be very appreciated"
  category: feedback_request
  function: polite_ask
  speaker_role: presenter
  difficulty: 3
  context: "the speed back about this ruby no truck HPM for a time would be very appreciated"

# ── 협상·액션 (Negotiation) ──
- id: m05-034
  expression: "we already got the request to put in our X schedule by Y months"
  category: pull_in_context
  function: external_pressure
  speaker_role: negotiator
  difficulty: 4
  context: "we already got the request to put in our over final IP drop schedule by two months"
  note: pull-in 요청의 배경 설명 - 외부 압력 명시

- id: m05-035
  expression: "if the X and specification fix as we expected then we can have a room to put in our overall design"
  category: conditional_acceleration
  function: conditional_possibility
  speaker_role: negotiator
  difficulty: 5
  context: "if the bump bump map and specification fix as we expected then we can have a room to put in our overall design"
  note: "have a room to X" - X할 여유가 있다. 조건부 가능성 시사

- id: m05-036
  expression: "currently we are keep our schedule but anyhow there are lots of work between X and Y"
  category: schedule_status
  function: hold_with_reason
  speaker_role: negotiator
  difficulty: 4
  context: "currently we are keep our schedule but anyhow there are lots of all the design phase work between NVIDIA and HSSK hynix"

- id: m05-037
  expression: "we are going to release our meta-layer without X result so that we can meet the overall Y schedule"
  category: tradeoff_decision
  function: schedule_priority
  speaker_role: negotiator
  difficulty: 5
  context: "we are going to release our meta-layer without revision AA result so that we can meet the overall revision BB schedule"
  note: "so that we can meet" - 일정 우선 결정. trade-off 명시

- id: m05-038
  expression: "one request on this X is to we are asking for a hot run for the Y"
  category: priority_request
  function: hot_run_ask
  speaker_role: negotiator
  difficulty: 4
  context: "one request on this one KES sample is to we are asking for a hot run for the course build"
  note: "we are asking for X" - 요청 공식. "we want" 대신 정중

- id: m05-039
  expression: "getting early feedback from this lot would let us reflect it into the X"
  category: request_justification
  function: benefit_chain
  speaker_role: negotiator
  difficulty: 5
  context: "getting early fit back from this lot would let us reflect it into the November ramping up samples"
  note: 요청의 효과 명시 - "early feedback을 Y에 반영"

- id: m05-040
  expression: "we can discuss internally and get back to you"
  category: internal_discussion
  function: deferred_commitment
  speaker_role: negotiator
  difficulty: 3
  context: "we can discuss internally and get back to you"

- id: m05-041
  expression: "we have another ongoing discussion with the X team for the detailed milestone for Y"
  category: parallel_coordination
  function: parallel_track
  speaker_role: negotiator
  difficulty: 4
  context: "we need to we have another ongoing discussion with the go down team for the detailed milestone for customer HM5"

- id: m05-042
  expression: "Yeah, we will update again. Yeah, all the things."
  category: update_commitment
  function: follow_up_promise
  speaker_role: presenter
  difficulty: 2
  context: "Yeah, we will update again. Yeah, all the things."

- id: m05-043
  expression: "we are also keep updating our schedule"
  category: continuous_update
  function: schedule_maintenance
  speaker_role: presenter
  difficulty: 3
  context: "we are also keep updating our schedule"

# ── 발화 채움·전환 (Discourse Markers) ──
- id: m05-044
  expression: "Okay next customer X"
  category: topic_transition
  function: section_open
  speaker_role: presenter
  difficulty: 2
  context: "Okay next customer HM4E a couple of ago we discussed"

- id: m05-045
  expression: "So the most of slide already touched a couple of so go so let me recap quickly and touch some update items"
  category: recap_transition
  function: recap_and_update
  speaker_role: presenter
  difficulty: 4
  context: "So the most of slide already touched a couple of so go so let me recap quickly and touch some update items"

- id: m05-046
  expression: "Okay, let's move on to the next page."
  category: slide_transition
  function: next_slide
  speaker_role: presenter
  difficulty: 2
  context: "Okay, let's move on to the next page."

- id: m05-047
  expression: "Yeah, let me check these status."
  category: status_check
  function: self_check
  speaker_role: presenter
  difficulty: 2
  context: "Yeah, I think I understand we are preparing but let me check these status"

- id: m05-048
  expression: "Can you follow me on that?"
  category: comprehension_check
  function: understanding_verify
  speaker_role: presenter
  difficulty: 4
  context: "Can you follow me on that?"
  note: 발표 중 이해 점검 - "이해가 따라가요?"

- id: m05-049
  expression: "so in that case, just think it, just hypothetically"
  category: hypothetical_opening
  function: assumption_setup
  speaker_role: questioner
  difficulty: 4
  context: "You know what, in that case, just think it, just hypothetically"

- id: m05-050
  expression: "We are going to do it."
  category: firm_commitment
  function: affirmative_repeat
  speaker_role: negotiator
  difficulty: 2
  context: "We're going to do it. We're going to do it. We're going to do it."
  note: 반복으로 강한 의지 표시 - 단호한 긍정

- id: m05-051
  expression: "Definitely, definitely the real world checkup, with some kind of learnings from the previous generation"
  category: learning_emphasis
  function: experience_basis
  speaker_role: negotiator
  difficulty: 4
  context: "Definitely, definitely the real world checkup, with some kind of learnings from the previous generation"

- id: m05-052
  expression: "we'd like to do our best from the support"
  category: support_commitment
  function: best_effort
  speaker_role: presenter
  difficulty: 3
  context: "we would like to do our best from the support"
  note: "do our best" - 최선을 다하겠다. support에 대한 약속
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-08-13 11 03 28_EN_NVIDIA_1H-extracted.wav`
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입 - HM4E 일정 합의 (line 1-15) | "a couple of ago we discussed 16 Gbps at max" + "one additional request" | 과거 합의 회상 + 추가 요청 포장 | ★★★ |
| 2 | BB schedule 발표 (line 17-25) | "design target is 16, but due to core die speed limits, lower bin 14.4" + "not ready to say the number" | 한계 인정 + 사유 명시 + 수치 회피 | ★★★★ |
| 3 | HBM4 ATI sample plan (line 161-200) | Danny 발표 - "we will ship 1K ES on 18th" + "purpose is to verify" + "steady flow" | sample plan 발표 + 목적 framing + 분할 배송 | ★★★ |
| 4 | BB push-back (line 87-99) | "We understand. But... it may not be possible" + "we cannot delay our overall BB schedule" | 공감 push-back + 단호한 한계 | ★★★★ |
| 5 | Pull-in 요청 + alignment (line 26-31, 219-227) | "we already got the request to pull in by two months" + "align the closing deal schedule" + "good enough or competitive enough" | pull-in 요청 + alignment + 자체 평가 요청 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - push-back/협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **schedule negotiation + sample coordination** register다. SK Hynix가 NVIDIA에 sample plan을 발표하고 timeline을 조율하는 구조. 두 역할 모두 학습해야:
- **발표자 역할 (SK Hynix)**: sample plan 발표, pull-in 제안, alignment 요청 - 네가 파트너에 sample을 제안할 때
- **협상자 역할 (양측)**: push-back, 조건부 가속, 한계 명시 - 네가 timeline을 협상할 때

### Pragmatics (화용론) 핵심
1. **"pull in"의 무게**: "pull in X by Y months" - "X를 Y개월 앞당기다" - 반도체 일정 협상의 가장 중요한 동사. "We're trying to pull in as much as possible" - "최대한 앞당기려 하고 있습니다" - 노력을 표시하되 결과는 보장하지 않는 화법.
2. **"align X with Y"의 정중성**: "align the closing deal schedule with our ramping up plan" - "close build 일정을 우리 ramp-up plan에 맞추다" - "맞춰달라"는 요구를 "맞추고 싶다"로 포장.
3. **"we cannot delay"의 단호함**: "we cannot delay our overall revision BB schedule" - "전체 BB schedule을 delay할 수 없습니다" - "can't"가 아니라 "cannot" + "delay"로 단호하면서 정중.
4. **"if our understanding is not correct, please"의 정중 확인**: "틀리면 알려달라" - 상대방 정보를 확인하되, 상대방이 틀렸다는 뉘앙스를 피하는 화법.

### 네가 당장 써야 할 Top 5
1. **"a couple of [weeks] ago we discussed X"** - 과거 합의 회상
2. **"we are targeting X MP"** - 양산 목표 명시
3. **"we'd like to align X with Y"** - 일정 정렬 요청
4. **"We understand. But... it may not be possible"** - 공감 push-back
5. **"if you need more, then we can discuss internally and get back to you"** - 내부 논의 후 회신

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "저번에 합의한 건 그대로고요" | "a couple of [weeks] ago we discussed X" | 과거 합의를 "a couple of ago"로 간결히 |
| "하나 추가하자면" | "one additional request from our side is X" | "추가"로 부담 완화 |
| "core die 속도 때문에 어렵습니다" | "due to the core die speed limits, there will be a lower bin" | "한계" 명사로 사유 명시 |
| "지금은 수치 말할 수 없습니다" | "we are not ready to say the number right now" | "모른다"가 아니라 "준비 안 됐다" |
| "이해합니다. 하지만 어렵습니다" | "We understand. But... it may not be possible" | "may not be possible"로 가능성 부정 |
| "전체 schedule을 delay할 수 없습니다" | "we cannot delay our overall X schedule" | "cannot delay" - 단호하면서 정중 |
| "내부 논의 후 회신드리겠습니다" | "we can discuss internally and get back to you" | "discuss internally and get back" |
| "최대한 앞당기겠습니다" | "we're trying to pull in as much as possible" | "pull in" - 반도체 일정 핵심 동사 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·4절 협상 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **일정 협상 특화**: 이 회의는 sample/schedule coordination 전용 교재 - "pull in", "align", "targeting MP", "steady flow", "revisit our numbers" 등 반도체 일정 협상 어휘를 집중 숙지

---

*Textbook 05 - NVIDIA 1H (2026-08-13). 회의 유형 C (sample/schedule coordination). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
