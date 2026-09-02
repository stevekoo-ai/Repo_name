---
textbook_id: 23
meeting: AWS (Amazon Web Services CXL/memory roadmap discussion)
date: 2026-02-10
type: B (roadmap/supply alignment)
partner: AWS (John, Jacob, AWS performance team)
sk_side: SK Hynix (Eugene, Juwan, Rachel, product planning, memory solution)
duration_words: 7697
audio: repo/webex-audio/2026-02-10 09 09 09_EN_AWS-extracted.wav
transcript: repo/webex-audio/2026-02-10 09 09 09_EN_AWS-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, aws, cxl, mrdim, lp-mrdim, validation, roadmap, supply-alignment, ddr5, ddr6]
---

# Textbook 23 - AWS CXL/Memory Roadmap (2026-02-10)

> **회의 유형**: B (roadmap/supply alignment) - 타임라인 조정, 벤더 선정, 스펙 푸시백, 마일스톤 정렬이 주를 이룸
> **학습 가치**: AWS가 SK Hynix에 일정 당김(prompt to pull in), 벤더 다변화 요구, 스펙 한계 추궁, CXL 도입 의향 탐색을 하는 전형적 roadmap 협상. SK는 validation 일정, PMIC 벤더 포트비율(기밀), MRDIM vs LP MRDIM 선택 근거를 설명하고 방어.
> **Audrey 관점**: 이 회의는 "고객이 일정·스펙·범위를 밀어붙이고, 공급자가 일정 정렬·기밀 회피·차세대 선택 근거로 방어"하는 협상의 교과서. 네가 AWS 입장이든 SK 입장이든 둘 다 배워야. 특히 Type B 핵심인 Section 4(negotiation/timeline language)에 집중.

---

## 1. 발화 아키텍처 - John(AWS)의 질문 설계 (5단계)

AWS 측 John은 roadmap 협상에서 5단계 질문 설계로 SK를 밀어붙인다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 고객 입장에서 파트너를 평가할 때 써야 할 "도전의 뼈대"다.

### 단계 1: 직접 도전 (Direct Challenge Opening)

John은 회의 첫 질문부터 직접적으로 밀어붙인다. "왜 안 쓰냐"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Why you guys decided not to use X? Do you have any big concern with it?` | "Why you guys decided not to use Rambus do you have any big concern with it?" | 직접 도전 - "왜 안 써?" + "큰 우려 있어?" 이중 질문 |
| `Can you explain why SK is supporting it? What is the benefit, what could be benefit for me?` | "Can you explain why SK is supporting it? What is the benefit for what could be benefit for me?" | 근거 요구 + "나한테 이득이 뭔데?" 자기 관점 전환 |

**Audrey 교훈**: 영어 roadmap 협상은 한국어 "왜 그렇게 하셨어요?"와 다르다. "Why you guys decided not to use X" - 주어를 "you guys"로 집단 지정, 결정의 책임을 조직에 물어 개인 공격을 피한다. 그리고 "do you have any big concern" - "concern"라는 단어로 우려를 표현. "Why didn't you"는 공격적이지만 "Why you decided not to"는 결정의 합리성을 묻는다. 이 차이를 외워.

### 단계 2: 정렬 확인 (Alignment Verification)

John은 SK가 제시한 일정이 Intel/AWS와 정렬되어 있는지 집요하게 확인한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is that aligned with Intel?` | "is this one is based on the dmr PRQ schedule, so if you have some earlier schedule for your... Yes, this is correct" | 정렬 확인 - "Intel과 맞아?" |
| `I want to finish all Intel memory validation before Intel hit PRQ` | "I want to finish all Intel memory validation before Intel hit PRQ This our shift left for DMR servers" | 자기 일정 노출 + "shift left"로 당김 요구 |
| `So do you think that our SOC validation case is aligned with your server roadmap now?` | "do you think that our SSC validates case you are aligned with your your server and relax now?" | 정렬 재확인 - 도전적 질문 |

**Audrey 교훈**: "Is that aligned with X?" - roadmap 협상의 핵심 질문. SK가 "Yes, this is correct"로 확인하면, John은 다음 단계로 넘어간다. "aligned with X"는 그냥 "matches X"보다 전문적 - 두 로드맵이 축을 맞춘다는 의미. 네가 파트너 일정을 평가할 때 무조건 써라.

### 단계 3: 일정 당김 요구 (Pull-in Request)

John은 SK의 일정이 느리면 "당겨라"고 밀어붙인다. 단, 정중하게.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `You ask us to pull in the schedule and the Q2 is okay` | "you ask us to pull in the schedule and the queue to is okay" | "pull in" - 일정 당김 요구 승인 |
| `I was communicating the AMD to support, but I haven't got the final answer` | "I was communicating the MD to supportive, but I haven't got the final answer" | 자기 역할 노출 - "내가 AMD에 압력 넣고 있다" |
| `So you know that's a view understand our schedules` | "So you know that's a view understand our schedules" | "우리 일정 이해했어?" - 동의 끌어내기 |

**Audrey 교훈**: "pull in the schedule" - 일정을 앞당기라는 요구. 한국어 "일정을 앞당겨주세요"의 전문 영어 버전. "pull in"은 roadmap 협상에서 가장 자주 쓰는 동사. 반대는 "push out" (일정 미루기). 네가 "빨리 해달라"고 할 때 "make it faster"가 아니라 "pull in the schedule"을 써라.

### 단계 4: 스펙 한계 추궁 (Spec Limitation Probe)

John은 SK가 제안한 스펙의 한계를 집요하게 캐묻는다. "가능은 한데 현실적이냐"로 몰아간다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is there any feasibility or not? You said yes, but in terms of cost, it's not realistic. Is that right?` | "is there any feasibility or not? You said yes, but in terms of cost. It's not realistic Is that right?" | 가능성 확인 + 비용 현실성 도전 - "이거 맞아?" |
| `That's why I keep asking this` | "That's why I keep asking the clarification" | 반복 질문의 정당화 - "그래서 계속 묻는 거야" |
| `We need a solution for high capacity units` | "we need a solution for high capacity units So mldm can support providers high bandwidth as well as I copy the options" | 요구 명시 - "우리는 고용량 솔루션이 필요해" |

**Audrey 교훈**: "Is there any feasibility or not?" - "가능한가 아닌가?" 이분법 질문. SK가 "yes"라고 대답하면, John은 즉시 "but in terms of cost, it's not realistic, is that right?"로 비현실성을 확인. 이게 "가능은 한데 안 한다는 거지?"를 정중하게 몰아가는 화법. "That's why I keep asking" - 반복 질문이 집요함이 아니라 명확화라는 프레임.

### 단계 5: 정중한 종결/보류 (Polite Close / Defer)

John은 답이 안 나오면 "오늘은 여기까지"로 정중하게 종결한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We don't have an answer today` | "No, thanks. We don't have an answer today" | 솔직한 보류 - "오늘 답 없어" |
| `We don't want to take too much of your lunch time` | "we don't want to take too much of your lunch time" | 정중한 종결 - 시간 배려 프레임 |
| `Why don't we call it a today` | "why don't we call it a today" | 회의 종료 제안 - "오늘은 여기까지" |

**Audrey 교훈**: "We don't have an answer today" - 답이 없을 때 솔직하게 인정. "We will check and follow up"으로 이어야 한다. 그리고 "we don't want to take too much of your lunch time" - 상대 시간 배려를 핑계로 회의를 종결. 한국어 "시간 다 됐네요"의 정중 영어 버전. "call it a day"는 "오늘은 여기까지 하자"는 관용구.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. SK 측(Eugene, Juwan)이 AWS의 도전을 어떻게 정중하게 회피하는지. Type B 협상에서 가장 많이 쓰는 화법이다.

### 전략 1: 기밀 회피 + 후속 약속 (Confidential Deflection)

가장 중요한 패턴. 답할 수 없는 질문은 "기밀"로 거부하고, 후속을 약속한다.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| 벤더 포트비율 | "That's a confidential information. So we can talk with... We try to utilize your old supplies. So that means still Vanessa's portion is very low, but you're trying to..." | "기밀 정보입니다. 공급사를 활용하려 합니다. Vanessa(Rambus) 비중은 여전히 낮지만, 늘리려 하고 있습니다" |

**패턴 공식**: `That's a confidential information. We try to utilize X. So that means Y is low, but we're trying to...`

**Audrey 교훈**: 영어 회의에서 "말할 수 없습니다"는 "I can't tell you"가 아니다. "That's a confidential information" - 기밀이라는 객관적 이유로 거부. 그리고 즉시 "we try to utilize X"로 부분 답변을 준다. "전부 말할 순 없지만, 이건 말해줄게" - 이게 정중한 회피다. 한국어 "그건 내부 사정이라"의 영어 버전이 "That's a confidential information"이다.

### 전략 2: 미결정 선언 (Undecided Declaration)

확답을 피하면서 "아직 결정 안 됐다"로 시간을 번다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| GA 일정 변경 | "But we haven't decided if we gonna change our G goal or not. Okay, if we decided I will share with you. So the current people are in GA Q1 is the... Yes, that's our goal. She can be changed later." | "G 목표 변경 여부는 아직 결정 안 했습니다. 결정되면 공유하겠습니다. 현재 GA Q1이 목표인데, 바뀔 수 있습니다" |

**패턴 공식**: `We haven't decided if X or not. If we decided, I will share with you. That's our goal, but it can be changed later.`

**Audrey 교훈**: "We haven't decided if X or not" - "아직 결정 안 했습니다"의 정중한 선언. "if we decided, I will share"로 후속 약속. "That's our goal, but it can be changed later" - 목표는 있되 확정은 아니라는 프레임. 한국어 "아직 정해진 건 없습니다"의 영어 버전이 "we haven't decided yet"인데, "if we decided, I will share"를 붙여야 전문가로 들린다.

### 전략 3: 부분 답변 + 모니터링 약속 (Partial Answer + Monitoring)

정확한 수치를 모를 때, 아는 것만 주고 "계속 확인하겠다"로 넘긴다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Intel validation 상세 일정 | "As of today, I'm sorry. I don't have that much of detailed data. But we will keep monitoring the progress. That's why I asked when you guys ship the sims. Then we can keep monitoring the progress of Intel site. We have a Weekly meeting with Intel. We'll keep checking the status." | "오늘 기준 상세 데이터는 없습니다. 계속 모니터링하겠습니다. 그래서 sims 출하 시점을 물은 겁니다. Intel과 주간 미팅이 있어 계속 확인하겠습니다" |

**패턴 공식**: `As of today, I don't have that much of detailed data. But we will keep monitoring the progress. We have a weekly meeting with X.`

**Audrey 교훈**: "I don't know"는 절대 쓰지 마라. "As of today, I don't have that much of detailed data" - "오늘 기준 상세 데이터가 없습니다"가 훨씬 전문적. 그리고 "we will keep monitoring" + "we have a weekly meeting with X" - 모니터링 체계를 보여주면 상대가 안심한다. "I'll check" 한마디보다 "we have a weekly meeting, we'll keep checking"이 신뢰를 준다.

### 전략 4: 고객 가치 프레이밍 (Customer Value Framing)

제품 선택 근거를 "고객이 원한다"로 프레이밍하여 책임을 분산.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| LP MRDIM 선택 이유 | "There are some major CSP customers looking into LP MRDIM for their PCU saving... LP MRDIM shows more customer value. And also we are actually doing some business with by 40 package. So we can leverage LP MRDIM... those are the main reasons why we think is more proper." | "주요 CSP 고객들이 PCU 절감을 위해 LP MRDIM을 검토 중입니다. LP MRDIM이 더 고객 가치가 있습니다. 또한 by 40 패키지 사업이 있어 활용 가능합니다. 이것이 더 적절하다고 생각하는 주요 이유들입니다" |

**패턴 공식**: `There are some major customers looking into X for Y. X shows more customer value. We can leverage X. Those are the main reasons why we think X is more proper.`

**Audrey 교훈**: "우리가 X를 선택한 이유"를 설명할 때, "we think X is better"만 하면 주관적으로 들린다. "Customers are looking into X" + "X shows more customer value" - 고객 관점을 끌어와 객관화. 그리고 "we can leverage X" - 기존 투자를 활용한다는 경제적 근거. 이 3단 구조(고객 수요 + 고객 가치 + 기존 자산 활용)를 외워. 회의에서 의사결정을 설득할 때 써라.

### 전략 5: 갭 브릿징 프레이밍 (Gap Bridging)

제품 갭을 "브릿지 솔루션"으로 긍정적으로 재프레이밍.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| LP MRDIM을 DDR6 갭 필러로 | "Assuming there is a possibility for DDR6 to push out a little bit, then LP MRDIM could be used as an gap bridging, bridging the gap. So we could candidate of making..." | "DDR6이 약간 밀릴 가능성이 있다면, LP MRDIM이 갭 브릿지, 갭을 메우는 용도로 쓰일 수 있습니다. 그래서 후보가 될 수 있습니다" |

**패턴 공식**: `Assuming there is a possibility for X to push out, then Y could be used as a gap bridging. So we could candidate of making.`

**Audrey 교훈**: "gap bridging" / "gap filler" - 제품이 일시적으로 필요할 때 쓰는 핵심 용어. "우리 제품이 임시로 쓸 수 있어"를 "X could be used as a gap bridging"으로 포장. 한국어 "임시 방편"의 긍정적 영어 버전. "push out" = 일정 미루기. roadmap 협상에서 "gap"과 "bridge"는 무조건 외워.

### 전략 6: 세대 한계 인정 + 비용 현실화 (Generation Limit + Cost Reality)

한계를 인정하되, 비용 관점에서 자체 제약을 설명.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 3DS 패키징 비현실성 | "We believe the maximum speed maximum density will be still limited to 256 gigabytes... the mldm Gen 3 gen 2 is already very expensive. Adapting the three million card support or anything 16 link, that's a put on the customers and their vendors." | "최대 밀도는 여전히 256GB에 제한될 것으로 봅니다. MLDIM Gen 3/2는 이미 매우 비쌉니다. 3DS 지원이나 16 link 도입은 고객과 벤더에 부담이 됩니다" |

**패턴 공식**: `We believe X will be still limited to Y. Z is already very expensive. Adapting W is a put on the customers.`

**Audrey 교훈**: "a put on the customers" - "고객에게 부담이 된다"는 관용 표현. "It's expensive"만 하면 약하다. "It's a put on the customers" - 비용이 고객에게 전가된다는 구조적 비판. 이게 SK가 자기 제품 한계를 인정하면서도 "고객을 위해서 안 하는 거다"로 포장하는 화법.

---

## 3. 정중한 도전 화법 (AWS 측 질문자)

AWS 측 John이 SK를 기술적으로 도전하면서도 정중하게 질문하는 패턴. **네가 고객 입장에서 파트너를 평가할 때 직접 써야 할 화법**이다.

### 질문 유형 1: 직접 이유 질문 (Direct Reason Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Why you guys decided not to use X? Do you have any big concern with it?` | "Why you guys decided not to use Rambus do you have any big concern with it?" | "왜 안 써? 큰 우려 있어?" - 직접 도전 |
| `Can you explain why SK is supporting it?` | "Can you explain why SK is supporting it?" | "왜 SK가 이걸 지원하는지 설명해줘" - 근거 요구 |

**Audrey 교훈**: "Why did you decide X?"는 공격적이지만 "Why you guys decided not to use X"는 "you guys"로 조직에 물어 부드럽다. "Do you have any big concern" - "concern"라는 단어가 도전을 우려로 포장. 이게 정중한 도전의 핵심.

### 질문 유형 2: 정렬 확인 (Alignment Verification)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is that aligned with X?` | "Is this one is based on the dmr PRQ schedule... Wasn't that aligned with Intel?" | "Intel과 정렬됐어?" - roadmap 핵심 질문 |
| `So do you think that our SOC validation is aligned with your server roadmap now?` | "do you think that our SSC validates case you are aligned with your your server and relax now?" | "우리 validation이 네 서버 로드맵과 맞아?" - 도전적 정렬 확인 |
| `That doesn't mean Intel will not share the validation result with SK?` | "that Doesn't mean Intel will not share the village of Richard with SK" | "그렇다고 Intel이 SK에 결과 안 공유 안 한다는 건 아니지?" - 우려 해소 |

**Audrey 교훈**: "aligned with X" - roadmap 협상에서 가장 많이 쓰는 질문. "Is this aligned with Intel?" 한마디로 파트너가 거짓말하는지 확인. SK가 "Yes, this is correct"로 답하면, 다음 질문으로 넘어간다. 이게 협상에서 "신뢰 검증" 화법이다.

### 질문 유형 3: 일정 당김 요구 (Pull-in Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `You ask us to pull in the schedule and the Q2 is okay` | "you ask us to pull in the schedule and the queue to is okay" | "Q2까지 당겨달라고 했지, 알겠어" - 당김 요구 확인 |
| `I want to finish all Intel memory validation before Intel hit PRQ` | "I want to finish all Intel memory validation before Intel hit PRQ. This our shift left for DMR servers" | "Intel PRQ 전에 validation 끝내고 싶어" - 자기 일정 노출 + shift left |

**Audrey 교훈**: "pull in the schedule" - roadmap 협상 핵심 동사. "make it faster"가 아니라 "pull in"을 써라. "shift left" - 일정을 앞으로 당긴다는 전문 용어. "We want to shift left our validation" - 이렇게 쓰면 "우리 validation 일정을 앞당기고 싶다"는 전문 발화.

### 질문 유형 4: 가능성/비용 이분 도전 (Feasibility vs Cost Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is there any feasibility or not? You said yes, but in terms of cost, it's not realistic. Is that right?` | "is there any feasibility or not? You said yes, but in terms of cost. It's not realistic Is that right?" | "가능은 한데 비용상 비현실적이지?" - 몰아붙이기 |
| `That's why I keep asking this` | "That's why I keep asking the clarification" | "그래서 계속 묻는 거야" - 반복 질문 정당화 |

**Audrey 교훈**: SK가 "가능합니다"라고 대답하면, 즉시 "but in terms of cost, it's not realistic, is that right?"로 비현실성을 확인. 이게 "네가 가능하다고 했지만 사실 안 되는 거지?"를 정중하게 몰아가는 화법. "That's why I keep asking" - 집요함을 "명확화"로 프레임.

### 질문 유형 5: 정중한 보류/답 없음 (Polite No-Answer)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We don't have an answer today` | "No, thanks. We don't have an answer today" | "오늘 답 없어" - 솔직한 보류 |
| `I was kind of surprised` | "I was kind of surprised. The information that I got from the inters... I know different" | "좀 놀랐어" - 정중한 이의 제기 |

**Audrey 교훈**: "I was kind of surprised" - "좀 놀랐다"는 정중한 이의 제기. "That's wrong"이 아니라 "I was surprised"로 자기 감정을 표현. "We don't have an answer today" - 답이 없을 때 솔직하게 인정. 한국어 "그건 제 선에서 답드리기 어렵네요"의 영어 버전.

### 질문 유형 6: 요구 명시 (Requirement Statement)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We need a solution for high capacity units` | "we need a solution for high capacity units. So mldm can support providers high bandwidth as well as I copy the options" | "고용량 솔루션이 필요해" - 요구 명시 |
| `If you guys just pick up the LP base MLDM, I don't have I copy the option. That's why I keep asking this` | "if you guys just pick up the LP base mldm I don't have I copy the option. That's why I keep asking this" | "LP만 고르면 512GB 옵션 없어. 그래서 계속 묻는 거야" - 요구 + 이유 |

**Audrey 교훈**: "We need a solution for X" - 요구를 명시하는 공식. "We want X"가 아니라 "We need a solution for X" - "솔루션이 필요하다"가 훨씬 전문적. 그리고 "That's why I keep asking" - 반복 질문의 이유를 명시. 협상에서 집요하게 물어야 할 때, 이유를 붙여야 공격적이지 않다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 **Type B 핵심 섹션**. timeline target, volume request, spec pushback, milestone coordination, "aligned with X", "under consideration" 언어.

### 타임라인 타겟 언어 (Timeline Target Language)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 스케줄 기반 선언 | SK | "This is based on the dmr PRQ schedule" | "PRQ 스케줄 기반입니다" - 근거 명시 |
| 완료 시점 | SK | "early validation should be completed by end of Q4" | "Q4 말까지 완료 예정" - target timeline |
| 정렬 선언 | SK | "This is the plan. We have alignment with Intel" | "Intel과 정렬된 계획입니다" - alignment 선언 |
| GA 타겟 | SK | "Our DMA GA is being scheduled Q1 next year" | "DMA GA Q1 내년 예정" - GA target |
| GA 1년 전 validation | SK | "Validation should be completed a year ahead of the GA" | "GA 1년 전 validation 완료" - timeline logic |
| 시프트 레프트 | AWS | "This our shift left for DMR servers" | "DMR 서버 shift left" - 일정 당김 |
| 풀인 요구 | AWS | "you ask us to pull in the schedule and the Q2 is okay" | "Q2까지 당겨달라" - pull-in |
| 푸시아웃 가능성 | SK | "Assuming there is a possibility for DDR6 to push out a little bit" | "DDR6 밀릴 가능성 가정" - push-out |
| 베스트 케이스 | SK | "the best case scenario of D-Dex is volume production starting from 2030" | "D-Dex 베스트 케이스 2030 양산" - best case |
| 갭 필러 | SK | "we need to have the gap, the gatefiller starting from 28 to 32 or 33" | "28~33년 갭 필러 필요" - gap filler |

**Audrey 교훈**:
- "based on the X schedule" - 일정의 근거를 명시. "We plan Q4"가 아니라 "based on the PRQ schedule" - 왜 Q4인지 설명.
- "should be completed by end of X" - 완료 시점. "by"가 중요. "in Q4"가 아니라 "by end of Q4" - 시점 정확.
- "shift left" / "pull in" / "push out" - roadmap 3대 동사. 앞당기기/당김 요구/미루기. 무조건 외워.
- "aligned with X" - 정렬 선언. "matches X"보다 전문적.
- "best case scenario" - 최상 시나리오. "we plan 2030"이 아니라 "best case is 2030" - 불확실성 인정.

### 볼륨/벤더 요구 (Volume/Vendor Request)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 3벤더 요구 | AWS | "We need to have at least three vendors just in case" | "최소 3벤더 필요, 만약을 대비" - 다변화 요구 |
| 벤더 포트비율 질문 | AWS | "Do you have number of position by PMIC vendor like in manufacturing sites, MPS 50% or...?" | "PMIC 벤더별 비중?" - 비율 탐색 |
| 기밀 회피 | SK | "That's a confidential information" | "기밀입니다" - 직접 회피 |
| 부분 답변 | SK | "Major volume is MPS, but we have a certain amount of Vanessa's as well" | "MPS가 주력, Rambus도 일부" - 부분 공개 |
| 세대별 차이 | SK | "It's not half and half. It depends on the generation" | "반반은 아님, 세대마다 다름" - 조건부 답변 |

**Audrey 교훈**:
- "We need to have at least three vendors just in case" - "just in case"가 핵심. "3벤더 필요"가 아니라 "만약을 위해 3벤더 필요" - 이유를 붙여야 설득.
- "That's a confidential information" - 기밀 회피. 그러나 즉시 "Major volume is X, but we have Y as well"로 부분 답변. 완전 거부가 아니라 부분 공개.
- "It depends on the generation" - 조건부 답변. "정확한 수치는 못 주지만, 세대마다 다르다" - 한국어 "때에 따라 다릅니다"의 영어 버전.

### 스펙 푸시백 (Spec Pushback)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 요구 명시 | AWS | "We need a solution for high capacity units" | "고용량 솔루션 필요" - 요구 |
| 옵션 우려 | AWS | "If you guys just pick up the LP base MLDM, I don't have I copy the option" | "LP만 고르면 512GB 옵션 없어" - 우려 |
| 한계 인정 | SK | "We believe the maximum density will be still limited to 256 gigabytes" | "최대 밀도 256GB 제한" - 한계 인정 |
| 비용 현실 | SK | "in terms of cost, it's not realistic" (AWS가 SK 대신 요약) | "비용상 비현실적" - 비용 관점 |
| 고객 부담 | SK | "Adapting the three million card support... that's a put on the customers" | "3DS 도입은 고객 부담" - 책임 전환 |
| 대안 제시 | SK | "If you need 256, then we can utilize the 32 gb products with a 10 day package" | "256 필요하면 32Gb + 10D 패키지" - 대안 |

**Audrey 교훈**:
- "We need a solution for X" - 요구 명시. "We want X"가 아니라 "solution for X" - 솔루션을 요구.
- "I don't have X option. That's why I keep asking" - 우려 + 반복 질문 정당화.
- "in terms of cost, it's not realistic" - 비용 관점 도전. "too expensive"가 아니라 "in terms of cost" - 관점을 명시.
- "that's a put on the customers" - 고객 부담 전가. 이게 SK가 자기 제품 한계를 "고객을 위해"로 포장.

### 마일스톤 조정 (Milestone Coordination)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 제출 | SK | "We already submit the samples to Intel for the 8800" | "8800 샘플 Intel에 제출" - milestone |
| 배치 설명 | SK | "the first batch will be shipped until that this month and next one is the volume validation" | "첫 배치 이번 달, 다음은 volume validation" - 배치 일정 |
| 재제출 조건 | SK | "if there are some issue at the time, we resubmit to some sample for example some RCD change" | "이슈 있으면 재제출, 예: RCD 변경" - 조건부 milestone |
| GA cadence | AWS | "we do have a one month gap between each server instance GA" | "서버 인스턴스 GA 간 1개월 간격" - cadence 설명 |
| 우선순위 | AWS | "we decide the first priority based on our customer demand" | "고객 수요 기반 우선순위" - priority logic |
| 1차/2차/3차 | AWS | "memory for an instance should be the first runner, our instance was second, X is the next one" | "인스턴스 1차, 우리 2차, X 3차" - 순서 명시 |

**Audrey 교훈**:
- "first batch" / "next one" / "final batch" - 배치 구분 언어. "첫 배치/다음/마지막"으로 일정을 단계화.
- "if there are some issue, we resubmit" - 조건부 milestone. "이런 경우 재제출" - 예외 관리.
- "one month gap between each GA" - cadence 설명. "gap" = 간격. "each X" - 반복 패턴.
- "first runner" / "second" / "next one" - 순서 언어. "priority" 대신 "runner" - 경주 비유.

### "Under Consideration" / "Under Investigation" 언어

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 검토 중 | SK | "The third generation feature is still under investigation" | "3세대 기능은 아직 검토 중" - under investigation |
| 의사결정 중 | AWS | "This is a decision making process right now" | "지금 의사결정 중" - decision process |
| 고려 중 | AWS | "we are considering and we are reviewing" | "검토·검토 중" - considering + reviewing |
| 미확정 | AWS | "we haven't decided if we gonna change our G goal or not" | "G 목표 변경 여부 미결정" - undecided |
| 후보 | SK | "LP MRDIM could be used as a gap bridging. So we could candidate of making" | "LP MRDIM 갭 브릿지 후보" - candidate |
| 의향 | SK | "we are willing to have this kind of discussion with you guys" | "논의 의향 있음" - willing to |

**Audrey 교훈**:
- "under investigation" / "under consideration" / "we are reviewing" - "검토 중"의 3가지 표현. "investigation"이 가장 기술적, "consideration"이 가장 비즈니스, "reviewing"이 가장 일반적.
- "we are willing to have this discussion" - "논의 의향이 있다" - 적극적 참여 표시. "we can"이 아니라 "we are willing to" - 의지 표현.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 액션 아이템 수행 | SK | "So let us take action idea (item)" | "액션 아이템으로 잡겠습니다" - commitment |
| 후속 약속 | SK | "I will answer you shortly" | "곧 답드리겠습니다" - follow-up |
| 공유 약속 | SK | "if we decided, I will share with you" | "결정되면 공유하겠습니다" - share commitment |
| 내일 시작 | SK | "tomorrow morning we will start with action item first" | "내일 아침 액션 아이템부터" - next step |
| 노트 확인 | SK | "Juwan took a note" | "Juwan이 노트했습니다" - note taker 명시 |

**Audrey 교훈**:
- "let us take action item" - 한국어 "액션 아이템으로 잡겠습니다"의 영어 버전. "we'll check"보다 강한 약속.
- "if we decided, I will share with you" - 결정 시 공유 약속. "I'll let you know"보다 "share"가 협조적.
- "Juwan took a note" - 노트 테이커 명시. 회의록 책임을 명확히. 회의 종료 시 "X took a note"로 후속 책임 확인.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 validation/roadmap/메모리 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **PRQ** (Product Release Qualification) | 제품 출시 품질 검증 | "based on the dmr PRQ schedule" - 일정의 기준점 |
| **GA** (General Availability) | 일반 출시 | "Our DMA GA is being scheduled Q1 next year" - GA target |
| **shift left** | 일정을 앞으로 당김 | "This our shift left for DMR servers" - 일정 당김 선언 |
| **pull in** | 스케줄을 앞당기라는 요구 | "you ask us to pull in the schedule" - 당김 요구 |
| **push out** | 스케줄을 미룸 | "possibility for DDR6 to push out" - 미루기 가능성 |
| **DMR** (Differential Memory RDIM?) | 차세대 메모리 규격 | "DMR servers" / "DMR 8800" - 차세대 플랫폼 |
| **MRDIM** (Multi-Rank DIMM) | 다중 랭크 DIMM | "MRDIM Gen 3" / "LP MRDIM" - 차세대 선택 |
| **LP MRDIM** | LPDDR5 기반 MRDIM | "LP MRDIM shows more customer value" - SK 주력 방향 |
| **ouRDIM** | (out-of-band RDIM?) | "256 gigabyte that is ouRDIM not our MRD" - 제품 구분 |
| **CXL** (Compute Express Link) | 컴퓨트 익스프레스 링크 | "CXL memory pooling in data center" - 도입 탐색 |
| **CMM** (CXL Memory Module) | CXL 메모리 모듈 | "128 gigabyte cmm is now mp stage" - CXL 제품 |
| **PCU** (Power Consumption Unit?) | 전력 소비 | "LP MRDIM for their PCU saving" - 절감 이유 |
| **DPC** (DIMM Per Channel) | 채널당 DIMM 수 | "one dpc platforms now" - 1DPC 구성 |
| **3DS** (3D Stacked) | 3D 적층 패키지 | "3DS package" - 고용량 패키징 |
| **by 40 package** | 4-high 스택 패키지 | "by 40 package, we can leverage LP MRDIM" - 기존 자산 |
| **Sims** (Simulation/Samples?) | 시뮬레이션/샘플 | "when you guys ship the sims" - 출하 확인 |
| **Tape out** | 설계 완료 | (이 회의 직접 언급 없음, 관련 용어) |
| **bring up** | 초기 구동 검증 | "early bring up next quarter" - 초기 검증 |
| **volume validation** | 양산 검증 | "next one is the volume validation" - 단계 구분 |
| **gate filler** | 갭 메우는 제품 | "we need to have the gap, the gatefiller" - 갭 브릿지 |
| **first runner** | 첫 출시 제품 | "memory for an instance should be the first runner" - 우선순위 |
| **cadence** | 출시 주기 | "those are the general cadence of our GA" - 반복 패턴 |
| **POR** (Plan of Record) | 기준 계획 | "we don't have p o r with the cxl expansion yet" - 미확정 |
| **TCO** (Total Cost of Ownership) | 총소유비용 | "tco level if you get better for performance" - 비용 논리 |
| **KV cache** | LLM 키-값 캐시 | "ai requires big data, having a pool of cxl memory would make sense" - AI 사용례 |
| **MP** (Mass Production) | 양산 | "128 gigabyte cmm is now mp stage" - 양산 단계 |
| **CS** (Customer Sample?) | 고객 샘플 | "CS will be provided in february next year" - 샘플 단계 |
| **SOC validation** | 시스템온칩 검증 | "our SOC validation case is aligned" - 검증 정렬 |
| **PRD** (Product Requirements Doc) | 제품 요구사항 | "PRD planning" - 계획 문서 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 도전 화법 (Challenge Patterns - AWS) ──
- id: m23-001
  expression: "Why you guys decided not to use X? Do you have any big concern with it?"
  category: direct_challenge
  function: reason_probe
  speaker_role: questioner
  difficulty: 4
  context: "Why you guys decided not to use Rambus do you have any big concern with it?"
  note: "you guys"로 조직에 물어 개인 공격 회피. "concern"으로 도전을 우려로 포장.

- id: m23-002
  expression: "Can you explain why SK is supporting it? What is the benefit, what could be benefit for me?"
  category: reason_probe
  function: justification_demand
  speaker_role: questioner
  difficulty: 4
  context: "Can you explain why SK is supporting it? What is the benefit for what could be benefit for me?"
  note: 근거 요구 + "나한테 이득이 뭔데?" 자기 관점 전환. 협상의 핵심 질문.

- id: m23-003
  expression: "Is that aligned with X?"
  category: alignment_check
  function: roadmap_verification
  speaker_role: questioner
  difficulty: 3
  context: "Wasn't that aligned with Intel?"
  note: roadmap 협상 핵심 질문. "matches X"보다 전문적.

- id: m23-004
  expression: "So do you think that our SOC validation is aligned with your server roadmap now?"
  category: alignment_check
  function: roadmap_verification_extended
  speaker_role: questioner
  difficulty: 4
  context: "do you think that our SSC validates case you are aligned with your your server and relax now?"
  note: 도전적 정렬 확인 - "지금 맞아?"로 협상 압박.

- id: m23-005
  expression: "I want to finish all Intel memory validation before Intel hit PRQ"
  category: timeline_demand
  function: shift_left_request
  speaker_role: questioner
  difficulty: 4
  context: "I want to finish all Intel memory validation before Intel hit PRQ. This our shift left for DMR servers"
  note: "shift left" - 일정 당김 선언. 자기 일정 노출 + 당김 요구.

- id: m23-006
  expression: "You ask us to pull in the schedule and the Q2 is okay"
  category: pull_in_request
  function: schedule_acceleration
  speaker_role: questioner
  difficulty: 4
  context: "you ask us to pull in the schedule and the queue to is okay"
  note: "pull in the schedule" - roadmap 핵심 동사. "make faster" 대신 쓸 것.

- id: m23-007
  expression: "Is there any feasibility or not? You said yes, but in terms of cost, it's not realistic. Is that right?"
  category: feasibility_challenge
  function: cost_reality_check
  speaker_role: questioner
  difficulty: 5
  context: "is there any feasibility or not? You said yes, but in terms of cost. It's not realistic Is that right?"
  note: 가능성 확인 + 비용 도전 - "가능은 한데 비현실적이지?"로 몰아붙이기.

- id: m23-008
  expression: "That's why I keep asking this"
  category: justification
  function: repeat_question_legitimacy
  speaker_role: questioner
  difficulty: 3
  context: "That's why I keep asking the clarification"
  note: 반복 질문의 정당화 - 집요함을 "명확화"로 프레임.

- id: m23-009
  expression: "We need a solution for X"
  category: requirement_statement
  function: demand_stating
  speaker_role: questioner
  difficulty: 3
  context: "we need a solution for high capacity units"
  note: "We want X" 대신 "We need a solution for X" - 솔루션 요구.

- id: m23-010
  expression: "If you guys just pick up the LP base MLDM, I don't have I copy the option"
  category: concern_stating
  function: option_loss_concern
  speaker_role: questioner
  difficulty: 5
  context: "if you guys just pick up the LP base mldm I don't have I copy the option. That's why I keep asking this"
  note: 우려 + 반복 질문 이유. "고르면 옵션 없어" - 협상 압박.

- id: m23-011
  expression: "We don't have an answer today"
  category: polite_defer
  function: honest_no_answer
  speaker_role: questioner
  difficulty: 3
  context: "No, thanks. We don't have an answer today"
  note: 솔직한 보류. "We will check and follow up"로 이어야.

- id: m23-012
  expression: "I was kind of surprised"
  category: polite_objection
  function: soft_disagreement
  speaker_role: questioner
  difficulty: 4
  context: "I was kind of surprised. The information that I got from the inters... I know different"
  note: "That's wrong" 대신 "I was surprised" - 자기 감정 표현으로 정중한 이의.

- id: m23-013
  expression: "We don't want to take too much of your lunch time"
  category: polite_close
  function: graceful_close
  speaker_role: questioner
  difficulty: 3
  context: "we don't want to take too much of your lunch time"
  note: 시간 배려 핑계로 회의 종결. "시간 다 됐네요" 정중 버전.

- id: m23-014
  expression: "Why don't we call it a day"
  category: meeting_close
  function: session_end
  speaker_role: questioner
  difficulty: 2
  context: "why don't we call it a today"
  note: "오늘은 여기까지" 관용구. "call it a day" 필수.

# ── 회피·포장 (Hedging & Deflection - SK) ──
- id: m23-015
  expression: "That's a confidential information"
  category: confidential_deflection
  function: direct_refusal
  speaker_role: presenter
  difficulty: 3
  context: "That's a confidential information. So we can talk with..."
  note: 기밀 회피 - "말할 수 없습니다" 정중 버전. 부분 답변과 세트.

- id: m23-016
  expression: "We try to utilize your old supplies. So that means still X's portion is very low, but you're trying to"
  category: partial_answer
  function: confidential_with_partial
  speaker_role: presenter
  difficulty: 5
  context: "We try to utilize your old supplies. So that means still Vanessa's portion is very low, but you're trying to"
  note: 기밀 회피 + 부분 답변. "전부 못 주지만, 이건 줄게" - 핵심 회피.

- id: m23-017
  expression: "We haven't decided if X or not. If we decided, I will share with you"
  category: undecided_declaration
  function: defer_with_promise
  speaker_role: presenter
  difficulty: 4
  context: "we haven't decided if we gonna change our G goal or not. If we decided I will share with you"
  note: 미결정 선언 + 공유 약속. "아직 정해진 없어, 정해지면 알려드릴게".

- id: m23-018
  expression: "That's our goal, but it can be changed later"
  category: goal_with_caveat
  function: soft_commitment
  speaker_role: presenter
  difficulty: 4
  context: "the current people are in GA Q1 is the... Yes, that's our goal. She can be changed later"
  note: 목표는 있되 확정은 아니라는 프레임. "goal but can change" 유용.

- id: m23-019
  expression: "As of today, I don't have that much of detailed data. But we will keep monitoring the progress"
  category: partial_answer
  function: monitoring_promise
  speaker_role: presenter
  difficulty: 5
  context: "As of today, I'm sorry. I don't have that much of detailed data. But we will keep monitoring the progress"
  note: "I don't know" 대신 정중 회피. 모니터링 체계로 신뢰 확보.

- id: m23-020
  expression: "We have a weekly meeting with Intel. We'll keep checking the status"
  category: monitoring_commitment
  function: ongoing_verification
  speaker_role: presenter
  difficulty: 3
  context: "We have we have a Weekly meeting with Intel. We'll keep checking the status"
  note: 미팅 체계로 신뢰. "I'll check"보다 "weekly meeting + keep checking"이 신뢰.

- id: m23-021
  expression: "It depends on the generation"
  category: conditional_answer
  function: generation_specific
  speaker_role: presenter
  difficulty: 3
  context: "It's not half and half. It's not a half and it depends on the on on generation"
  note: 조건부 답변. "정확 수치 못 주지만 세대마다 다름" - 한국어 "때에 따라 다릅니다".

- id: m23-022
  expression: "There are some major CSP customers looking into X for Y"
  category: customer_value_framing
  function: customer_demand_evidence
  speaker_role: presenter
  difficulty: 4
  context: "There are some major CSP customers Looking into LP MRB in for their PCU saving"
  note: 고객 수요를 근거로 제시. "we think" 주관 대신 "customers looking" 객관화.

- id: m23-023
  expression: "X shows more customer value"
  category: value_framing
  function: customer_value_claim
  speaker_role: presenter
  difficulty: 4
  context: "LP MRDIM shows more Customer value"
  note: "X is better" 대신 "X shows more customer value" - 고객 가치로 객관화.

- id: m23-024
  expression: "We can leverage X"
  category: leverage_framing
  function: existing_asset_utilization
  speaker_role: presenter
  difficulty: 3
  context: "we can leverage LP MRDIM we call it LP 5R by 40 package"
  note: 기존 투사 활용 근거. "we can leverage X" - 경제적 정당성.

- id: m23-025
  expression: "Those are the main reasons why we think X is more proper"
  category: reason_summary
  function: conclusion_stating
  speaker_role: presenter
  difficulty: 3
  context: "those are the Main reasons why we think is more Proper"
  note: 이유 나열 후 결론. "those are the main reasons" - 3단 구조 마감.

- id: m23-026
  expression: "Assuming there is a possibility for X to push out, then Y could be used as a gap bridging"
  category: gap_bridging
  function: reframe_as_bridge
  speaker_role: presenter
  difficulty: 5
  context: "Assuming there is a possibility to for DDR6 to Push out a little little bit then LPMRDIM could be used as an as an gap bridging"
  note: "gap bridging" - 제품을 갭 필러로 긍정 재프레이밍. "push out"과 세트.

- id: m23-027
  expression: "We need to have the gap, the gatefiller starting from X to Y"
  category: gap_filler
  function: market_need
  speaker_role: presenter
  difficulty: 4
  context: "we need to have the gap the gatefiller you know starting from 28 to 20 you know 32 or 33"
  note: "gate filler" - 갭 메우는 제품. roadmap 협상 필수 용어.

- id: m23-028
  expression: "We believe the maximum density will be still limited to X"
  category: limit_acknowledgment
  function: cap_admission
  speaker_role: presenter
  difficulty: 3
  context: "We believe the maximum speed maximum density will be still limited to 256 gigabytes"
  note: 한계 인정. "max will be limited to X" - 솔직한 cap 선언.

- id: m23-029
  expression: "That's a put on the customers"
  category: cost_shifting
  function: customer_burden_framing
  speaker_role: presenter
  difficulty: 5
  context: "Adapting the three million card support or anything 16 link that's a put on The customers"
  note: "고객에게 부담" 관용구. 자기 한계를 "고객 위해서"로 포장.

# ── 타임라인/마일스톤 (Timeline & Milestone) ──
- id: m23-030
  expression: "This is based on the X schedule"
  category: schedule_basis
  function: rationale_stating
  speaker_role: presenter
  difficulty: 3
  context: "This is based on the dmr PRQ schedule"
  note: 일정 근거 명시. "We plan Q4" 대신 "based on PRQ schedule" - 왜 Q4인지 설명.

- id: m23-031
  expression: "X should be completed by end of Y"
  category: completion_target
  function: timeline_target
  speaker_role: presenter
  difficulty: 3
  context: "early validation should be completed by end of Q4"
  note: "by end of X" - 완료 시점. "in X" 대신 "by end of X" - 시점 정확.

- id: m23-032
  expression: "This is the plan. We have alignment with X"
  category: alignment_declaration
  function: roadmap_alignment
  speaker_role: presenter
  difficulty: 4
  context: "This is the plan. We have alignment with Intel"
  note: 정렬 선언. "matches X" 대신 "alignment with X" - 전문 용어.

- id: m23-033
  expression: "Our X GA is being scheduled Y"
  category: ga_target
  function: ga_schedule
  speaker_role: presenter
  difficulty: 3
  context: "Our DMA GA is being scheduled Q1 next year"
  note: GA 타겟 선언. "is being scheduled" - 진행형으로 확정 아님 표현.

- id: m23-034
  expression: "Validation should be completed a year ahead of the GA"
  category: timeline_logic
  function: sequence_rationale
  speaker_role: presenter
  difficulty: 4
  context: "Validation should be completed a year ahead of the GA and then you can start the early bring up"
  note: 타임라인 논리. "GA 1년 전 validation" - 왜 지금 하는지 설명.

- id: m23-035
  expression: "The best case scenario of X is volume production starting from Y"
  category: best_case
  function: optimistic_timeline
  speaker_role: presenter
  difficulty: 4
  context: "the best case scenario of D-Dex is in our volume production starting from 2030"
  note: "best case" - 불확실성 인정. "we plan 2030" 대신 "best case is 2030".

- id: m23-036
  expression: "The first batch will be shipped until this month and next one is the volume validation"
  category: batch_schedule
  function: phased_milestone
  speaker_role: presenter
  difficulty: 3
  context: "the first fetch will be shipped Until that this month and next one is the volume validation with that sample"
  note: 배치 구분. "first batch / next / final" - 일정 단계화.

- id: m23-037
  expression: "If there are some issue at the time, we resubmit to some sample"
  category: conditional_milestone
  function: exception_handling
  speaker_role: presenter
  difficulty: 4
  context: "if there are some issue at the time We resummit to some sample for example some RCT change"
  note: 조건부 milestone. "이슈 시 재제출" - 예외 관리.

- id: m23-038
  expression: "We do have a one month gap between each server instance GA"
  category: cadence_stating
  function: release_pattern
  speaker_role: questioner
  difficulty: 4
  context: "we do have a one month gap between each server instance GA"
  note: cadence 설명. "gap between each X" - 반복 패턴 명시.

- id: m23-039
  expression: "We decide the first priority based on our customer demand"
  category: priority_logic
  function: ranking_rationale
  speaker_role: questioner
  difficulty: 3
  context: "we decide the first priority based on our customer demand"
  note: 우선순위 근거. "고객 수요 기반" - 객관적 기준.

- id: m23-040
  expression: "X should be the first runner, Y was second, Z is the next one"
  category: sequence_stating
  function: release_order
  speaker_role: questioner
  difficulty: 3
  context: "memory for an instance should be the first runner Our instance was second since the next one X is the next one"
  note: 순서 언어. "first runner / second / next one" - 경주 비유.

# ── 검토·의향 (Under Consideration) ──
- id: m23-041
  expression: "The third generation feature is still under investigation"
  category: under_investigation
  function: review_status
  speaker_role: presenter
  difficulty: 3
  context: "The third generation feature is still under investigation"
  note: "검토 중" 기술적 표현. "under investigation" 필수.

- id: m23-042
  expression: "This is a decision making process right now"
  category: decision_in_progress
  function: ongoing_decision
  speaker_role: questioner
  difficulty: 3
  context: "This is a making process right now. We really like to have your input"
  note: "의사결정 중" - 진행형으로 협상 여지 표시.

- id: m23-043
  expression: "We are considering and we are reviewing"
  category: considering
  function: review_dual
  speaker_role: questioner
  difficulty: 2
  context: "You are considering and we are reviewing then as of today"
  note: "검토 중" 2중 표현. considering + reviewing 반복 강조.

- id: m23-044
  expression: "We are willing to have this kind of discussion with you guys"
  category: willingness
  function: intent_stating
  speaker_role: presenter
  difficulty: 3
  context: "we are willing to have this kind of discussion with you guys"
  note: 의향 표시. "we can" 대신 "we are willing to" - 의지 표현.

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m23-045
  expression: "We need to have at least three vendors just in case"
  category: vendor_diversification
  function: multi_source_demand
  speaker_role: questioner
  difficulty: 4
  context: "We need to have at least three vendors just in case"
  note: "just in case" - 이유 붙여 설득. 3벤더 다변화 요구.

- id: m23-046
  expression: "Let us take action item"
  category: action_item
  function: commitment_formal
  speaker_role: presenter
  difficulty: 3
  context: "So let us take action idea (item)"
  note: "액션 아이템으로 잡겠습니다" 영어 버전. "we'll check"보다 강한 약속.

- id: m23-047
  expression: "I will answer you shortly"
  category: follow_up
  function: short_term_promise
  speaker_role: presenter
  difficulty: 2
  context: "I will answer you shorter"
  note: "곧 답드리겠습니다" - 단기 후속 약속.

- id: m23-048
  expression: "If we decided, I will share with you"
  category: share_promise
  function: decision_share
  speaker_role: presenter
  difficulty: 3
  context: "if we decided I will share with you"
  note: 결정 시 공유 약속. "I'll let you know" 대신 "share" - 협조적.

- id: m23-049
  expression: "Tomorrow morning we will start with action item first"
  category: next_step
  function: next_session_focus
  speaker_role: presenter
  difficulty: 3
  context: "tomorrow morning we will start with uh action item first"
  note: 다음 회의 시작점 명시. "action item부터" - 책임 확인.

- id: m23-050
  expression: "Juwan took a note"
  category: note_taker
  function: accountability_stating
  speaker_role: presenter
  difficulty: 2
  context: "Action item Juwan took a note"
  note: 노트 테이커 명시. 회의 종료 시 후속 책임 확인.

# ── CXL/인메모리 관련 (CXL Discussion) ──
- id: m23-051
  expression: "We don't have POR with the CXL expansion yet. We are reviewing then"
  category: por_status
  function: not_yet_committed
  speaker_role: questioner
  difficulty: 4
  context: "we don't have p o r with the cxl expansion yet. Whenever we meet the situation of a capacity expansion... Sexly is the one of the candidate we are reviewing"
  note: "POR 없음 + 검토 중" - CXL 도입 미확정. "POR" = Plan of Record.

- id: m23-052
  expression: "The reason we hasn't made this as a POR is we have the better option"
  category: better_option
  function: alternative_preference
  speaker_role: questioner
  difficulty: 5
  context: "The reason we hasn't made this as a p y is We have the better option Better option such as I mean we do have enough and this with ouRDIM"
  note: "더 나은 옵션 있음" - 정중한 거절. "CXL 안 쓰는 이유 = 더 나은 옵션" - 명확한 우선순위.
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-02-10 09 09 09_EN_AWS-extracted.wav` (총 약 60분, 7,697단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입 - PMIC 벤더 (line 1-18) | AWS "Why not Rambus?" + SK "기밀/부분 답변" + "let us take action item" | 직접 도전 + 기밀 회피 + 액션 아이템 | ★★★ |
| 2 | Intel validation 정렬 (line 28-39) | AWS "aligned with Intel?" + SK "based on PRQ schedule" + "shift left" | 정렬 확인 + 타임라인 근거 + shift left | ★★★★ |
| 3 | AMD Venice 256GB (line 66-83) | AWS "ouRDIM vs MRDIM" + SK "G target one quarter later" + cadence 설명 | 스펙 결정 + cadence + 우선순위 | ★★★★ |
| 4 | LP MRDIM 선택 논쟁 (line 111-165) | AWS "왜 SK가 LP 지원?" + SK "고객 가치 + by40 활용 + 갭 브릿지" + 비용 도전 | 고객 가치 프레이밍 + 갭 브릿지 + 비용 현실 도전 | ★★★★★ |
| 5 | CXL 메모리 풀링 (line 199-224) | SK "CXL roadmap" + AWS "POR 없음, 더 나은 옵션" + TCO 논의 | POR 상태 + better option + TCO 논리 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 각 단계에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 협상/회피 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap 협상 + supply alignment** register다. 고객(AWS)이 일정·스펙·벤더를 밀어붙이고, 공급자(SK)가 일정 정렬·기밀 회피·차세대 선택 근거로 방어하는 구조. 두 역할 모두 학습해야:
- **고객 역할 (John/AWS)**: 직접 도전, 정렬 확인, 일정 당김 요구, 스펙 한계 추궁, 요구 명시 - 네가 파트너 평가할 때
- **공급자 역할 (Eugene/SK)**: 기밀 회피, 미결정 선언, 부분 답변, 고객 가치 프레이밍, 갭 브릿징 - 네가 파트너에 답할 때

### Pragmatics (화용론) 핵심
1. **"aligned with X"의 무기화**: AWS가 "Is this aligned with Intel?"로 묻는 것은 단순 질문이 아니다. SK가 "Yes"라고 대답하면, 그 다음 "그럼 왜 우리 일정과 안 맞아?"로 이어지는 협상 도구. roadmap 협상에서 정렬 확인은 **신뢰 검증**이다.
2. **"pull in / push out / shift left" 3대 동사**: roadmap 협상의 핵심 어휘. "빨리 해라/밀린다/앞당긴다"를 이 3개로 표현. 한국어 "일정 당겨주세요"는 "pull in the schedule"로, "밀릴 수도 있어요"는 "push out"으로.
3. **기밀 회피의 기술**: "That's a confidential information"으로 거부한 뒤, 즉시 "we try to utilize X, so Y is low but we're trying to"로 부분 답변. 완전 거부가 아니라 부분 공개. 이게 정중한 회피의 정석.
4. **"gap filler / gap bridging"의 긍정적 재프레이밍**: 제품이 임시 방편일 때, "gap bridging"으로 포장. "임시"가 아니라 "갭을 메우는 가치 있는 솔루션"으로 프레임.
5. **"better option"으로 거절**: AWS가 CXL을 안 쓰는 이유를 "we have better option"으로. "CXL이 별로라서"가 아니라 "더 나은 옵션이 있어서" - 정중한 우선순위 표현.

### 네가 당장 써야 할 Top 5
1. **"Is that aligned with X?"** - roadmap 협상 신뢰 검증
2. **"That's a confidential information. We try to utilize X"** - 기밀 회피 + 부분 답변
3. **"We haven't decided if X or not. If we decided, I will share with you"** - 미결정 선언
4. **"pull in the schedule" / "push out" / "shift left"** - 타임라인 3대 동사
5. **"X shows more customer value" + "we can leverage Y"** - 의사결정 설득

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "왜 안 쓰세요?" | "Why you guys decided not to use X? Any big concern?" | "you guys"로 조직에 물어, "concern"으로 우려 포장 |
| "기밀입니다" | "That's a confidential information. We try to utilize X" | 기밀 선언 후 부분 답변으로 보완 |
| "아직 정해진 없습니다" | "We haven't decided if X or not. If decided, I will share" | 미결정 + 공유 약속 세트 |
| "일정 당겨주세요" | "pull in the schedule" / "shift left" | "make faster" 대신 전문 동사 |
| "고객이 원해서요" | "Customers are looking into X. X shows more customer value" | "우리 생각" 대신 고객 근거 |
| "임시 방편입니다" | "X could be used as a gap bridging" | "임시"를 "갭 브릿지"로 가치화 |
| "비싸서 안 합니다" | "That's a put on the customers" | "비싸다" 대신 고객 부담으로 프레임 |
| "더 나은 옵션이 있어요" | "We have the better option" | 정중한 우선순위 표현 |
| "시간 다 됐네요" | "We don't want to take too much of your lunch time" | 시간 배려 핑계로 종결 |
| "내일 액션 아이템부터" | "Tomorrow morning we will start with action item first" | 다음 회의 시작점 명시 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Type B 집중**: 4절 협상·액션 화법을 가장 깊이 학습 - timeline target, vendor request, spec pushback, milestone coordination
4. **Audrey 금요일 교정**: 2절 회피 화법·3절 도전 화법 중심으로 dump 작성
5. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
6. **역할 바꿔 연습**: AWS 입장(도전)과 SK 입장(회피)을 번갈아 연습 - 둘 다 쓸 일이 있다

---

*Textbook 23 - AWS CXL/Memory Roadmap (2026-02-10). 회의 유형 B (roadmap/supply alignment). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
