---
textbook_id: 15
meeting: Qualcomm Morning1 (DRAM/NAND market + Qualcomm SoC roadmap)
date: 2026-04-27
type: B (roadmap/supply alignment)
partner: Qualcomm (SoC roadmap presenter)
sk_side: SK hynix Market Intelligence, NAND Marketing (Kasey Kim), DRAM/mobile DRAM analyst, SoC packaging engineers
duration_words: 4277
audio: repo/webex-audio/2026-04-27 10 01 41_EN_Qualcomm_Morning1-extracted.wav
transcript: repo/webex-audio/2026-04-27 10 01 41_EN_Qualcomm_Morning1-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, qualcomm, soc-roadmap, lpddr6, lpddr5x, cob, sip, packaging, dram-market, nand-market, supply-alignment, type-b]
---

# Textbook 15 - Qualcomm Morning1 (2026-04-27)

> **회의 유형**: B (로드맵/공급 정합) - SK가 시장 전망을 공유하고 Qualcomm이 SoC 로드맵(8975/8875)과 패키징(COB/SIP) 방향을 발표. Z-height, LPDDR6 전환, 비즈니스 모델 등 공급 정합 협의.
> **학습 가치**: 로드맵 발표자의 "부드럽게 미루기 + 협력 제안", 시장 분석가의 "전망+근거" 프레이밍, 질문자의 "정중 도전 + 확인" 패턴
> **Audrey 관점**: Type B 회의의 핵심은 "we're targeting X in Y", "we would like X but Y is limited", "aligned with X", "under consideration" 같은 타협 언어. 이 회의엔 그게 다 있다. 네가 파트너와 로드맵을 맞출 때 직접 써라.

---

## 1. 발화 아키텍처 - Qualcomm 발표자의 로드맵 설계 (5단계)

Qualcomm 발표자는 SoC 로드맵을 5단계로 설계한다. 각 단계마다 고정된 화법 공식이 있다.

### 단계 1: 변화 프레이밍 (Change Framing)

"이전과 같다"로 시작하지 않고, "변화가 있다"로 듣는 이의 주의를 끌어모은다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `as you guys are familiar with the X, I think there are a few changes` | "So as you guys are familiar with the roadmap, I think there are a few changes" | 친숙함 전제 + 변화 신호 - "familiar with"로 과거 합의 회상 |
| `Now we have like N tiers in the X flagship` | "Now we have like three tiers in the 800 flagship" | "Now we have like N tiers" - 구조 변화 선언 |
| `Primarily because of the dynamics in X, right?` | "Primarily because of the dynamics in that idea market, right?" | "right?"로 청중 동의 끌어내기 + 이유 |

**Audrey 교훈**: 로드맵 발표는 "What's new"로 시작한다. "As you guys are familiar with X, I think there are a few changes" - 이 한 문장이 "나는 너희가 이미 아는 것을 알고 있고, 그 위에 덧붙일 게 있다"를 동시에 전달한다. 한국어 "아시다시피 몇 가지 변경이 있습니다"의 영어 버전이지만, "I think there are a few changes"의 "I think"가 자신감을 줄여 겸손하게 들리게 만든다.

### 단계 2: 부드러운 수정 (Soft Correction)

단어 선택이 너무 강한 것을 스스로 교정한다. 이게 발표자의 "말 다루기" 기술이다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I won't say X, but we need to be more Y` | "we need to be more, I won't say aggressive, but we need to be more competitive in certain segments" | 자기 교정 - "aggressive"가 너무 강해서 "competitive"로 후퇴 |
| `we are hoping that that's just a transitionary time for X` | "Though we are seeing not much demand on the LP6, but we're hoping that that's just a transitionary time for 26" | "transitionary time"로 부정적 현상을 일시적으로 프레이밍 |

**Audrey 교훈**: "I won't say X, but Y"는 발표자가 자기 언어를 실시간으로 다듬는 화법이다. "aggressive"라는 단어가 파트너에게 위협적으로 들릴 것을 알고, 즉시 "competitive"로 회수한다. 네가 발표 중 "너무 강한 단어"를 입에 올렸을 때, "I won't say X, but Y"로 교정해라. 이게 영어 발표의 자기 통제 기술이다.

### 단계 3: 스펙 나열 (Spec Enumeration)

칩스pec을 "SoC + memory + storage"의 3단 구조로 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are working on X. That is slated for Y at Z` | "we are working on 8,975. That is slated for LPDDR 5 and 6 combo at 5.3" | "slated for" - 확정 일정 표시 |
| `going forward X, we are hoping that we can actually do Y` | "And then going forward 8,875, we are hoping that we can actually do LP6" | "going forward" - 다음 제품으로 전환 |
| `The X doesn't change on either one of them` | "The UFS doesn't change on either one of them" | "doesn't change" - 변하지 않는 스펙 강조 |
| `that remains to be X` | "that remains to be UFS 5.0 Gear 6.2 lanes" | "remains to be" - 스펙 유지 표현 |

**Audrey 교훈**: "slated for"는 "예정되다"의 전문 표현이다. "scheduled"보다 비즈니스 회의에서 자연스럽다. "8975 is slated for LPDDR5X and LPDDR6 combo at 5.3" - 제품명 + 메모리 spec + data rate을 한 문장에. 이게 로드맵 발표의 단위 문장이다.

### 단계 4: 협력 제안 (Collaboration Push)

단순 발표가 아니라 "같이 밀어붙이자"는 제안을 넣는다. 이게 Type B 회의의 핵심.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we do want to push X as much as we could` | "we do want to push LP6 as much as we could because we've all worked so hard on it" | "do want to push" - 강조 + 협력 촉구 |
| `we should push them to see if there is a possibility of X` | "we should push them to see if there is a possibility of launching with LP6, even for the few designs" | "we should push them" - 공동 행동 제안 |
| `I think it's just the fact that we need to have it out there to show X` | "I think it's just the fact that we need to have it out there to show the differences and the gaps that we cover with LP6" | "need to have it out there" - 존재감 확보 논리 |

**Audrey 교훈**: "we should push them" - 주어가 "we"다. Qualcomm 발표자가 SK를 동참시키는 화법. "You should push"가 아니라 "we should push"로 공동 행동을 제안한다. 네가 파트너에게 "같이 고객을 밀어붙이자"고 할 때, "we should push them to see if there is a possibility of X"를 써라. "we"가 협력의 핵심 단어다.

### 단계 5: 이슈 언급 + 후속 논의 유도 (Issue Flag + Follow-up)

문제를 짧게 언급하고 "나중에 자세히"로 미룬다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `There are some, maybe we can have that discussion later on` | "There are some, maybe we can have that discussion later on" | "maybe we can have that discussion later" - 후속 유도 |
| `We need to work with you guys to figure out the X` | "We need to work with you guys to figure out the Z heights for LP5X and LP6" | "work with you guys to figure out" - 협력 필요성 표시 |
| `So maybe we can have that discussion there` | "So maybe we can have that discussion there" | "that discussion there" - 후속 지점 지정 |
| `I don't know if you guys have any questions on the X` | "I don't know if you guys have any questions on the packaging for 8,975" | "I don't know if" - 겸손한 질문 유도 |

**Audrey 교훈**: "maybe we can have that discussion later"는 회의에서 민감한 이슈를 뒤로 미루는 정중한 화법이다. "지금은 말하기 어렵다"가 아니라 "나중에 자세히 논의하자"로 포장. 네가 회의에서 복잡한 문제에 부닥치면, "maybe we can have that discussion later on"으로 시간을 벌어라.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 진짜 학습 가치. Qualcomm 발표자와 SK 담당자가 각자의 약점을 어떻게 정중하게 포장하는지.

### 전략 1: 정보 공유 한계 인정 + 후속 약속 (Information Boundary + Follow-up)

정확한 수치나 내부 정보를 공유할 수 없을 때, "내부에서 확인하고 다시 연락하겠다"로 포장한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 가격 정보 공유 한계 | "Okay I understand what your question is. We'll check internally and just get back to you on in terms of you know how much detail we can share or what degree we can kind of address your question." | "네, 질문은 이해했습니다. 내부에서 확인하고 어느 정도까지 공유할 수 있는지, 질문에 어디까지 답할 수 있는지 다시 연락드리겠습니다." |
| LPDDR6 가이던스 요청 | "We'll see. I'm not sure what scope or what level of information we can provide, but we'll definitely just discuss internally our marketing team." | "봐야겠네요. 어느 범위까지 정보 제공 가능한지 확신 없지만, 마케팅 팀과 내부 논의는 확실히 하겠습니다." |

**패턴 공식**: `I understand what your question is. We'll check internally and get back to you on how much detail we can share.`

**Audrey 교훈**: "I don't know"는 절대 쓰지 마라. 대신 "I'm not sure what scope or what level of information we can provide" - "어느 범위까지 제공 가능한지 확신 없다"로, "모른다"가 아니라 "공유 결정 권한이 내게 없다"를 정중하게 표현. 그리고 "we'll definitely discuss internally"의 "definitely"가 미루는 것을 부드럽게 만든다. 한국어 "내부 확인 후 회신 드리겠습니다"의 영어 버전이다.

### 전략 2: "희망"으로 현실 포장 (Hope Hedging)

부정적 현상을 "transitionary"나 "hoping"으로 완화한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| LP6 수요 부족 | "Though we are seeing not much demand on the LP6, but we're hoping that that's just a transitionary time for 26. And hopefully when there is, you know, 27 comes around, there'll be more designs in LP6." | "LP6 수요는 별로 없지만, 26년엔 일시적 과도기일 거라 희망합니다. 27년이 오면 LP6 디자인이 더 늘어나길 바랍니다." |
| 기대감으로 밀어붙이기 | "Though we do want to push LP6 as much as we could because we've all worked so hard on it." | "우리 모두 너무 열심히 일했기 때문에, LP6을 최대한 밀어붙이고 싶습니다." |

**패턴 공식**: `We are seeing not much X, but we're hoping that's just a transitionary time for Y. Hopefully when Z comes around, there'll be more X.`

**Audrey 교훈**: "not much demand"라는 부정적 사실을 인정하되, 즉시 "transitionary time"으로 일시적 현상으로 프레이밍. 그리고 "hopefully when 27 comes around"로 미래 시제로 전환. "지금은 안 좋지만 다음엔 좋을 거다"의 영어 패턴이다. 한국어 "일시적이고, 다음엔 개선될 것으로 보입니다"와 구조가 같다. "hoping that + that's just a transitionary time"을 외워라.

### 전략 3: 책임 회피 + 대안 제시 (Deflection + Alternative)

자기 전문 영역이 아닌 질문은 거절하되, 다른 방법이 있다고 포인팅한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Z-height 기술 질문 | "So I won't comment on that because I don't want to, you know, because it's not my feed, but there are other ways that companies are looking at to make that happen. So it doesn't have to be the DRAM high. There could be other ways of packaging technology or how we package the dies could be different." | "제 전문 분야가 아니라서 코멘트는 삼가겠습니다. 하지만 다른 방법들이 있습니다. DRAM 높이가 아니라 패키징 기술이나 다이 적재 방식으로 해결할 수 있습니다." |

**패턴 공식**: `I won't comment on that because it's not my feed, but there are other ways that X. It doesn't have to be Y. There could be other ways of Z.`

**Audrey 교훈**: "It's not my feed"는 "제 전문 분야가 아닙니다"의 자연스러운 영어 표현이다. "feed"는 분야/영역을 뜻하는 비즈니스 슬랭. "I won't comment"으로 거부한 후 "but there are other ways"로 즉시 대안 제시. 부정만 하고 끝내지 않는 패턴은 Type B 회의에서 특히 중요하다. "안 됩니다"가 아니라 "제 영역이 아니지만 다른 방법이 있습니다"로 포장.

### 전략 4: 비결정 상태 인정 (Non-decision Acknowledgment)

결정되지 않은 사안을 "haven't closed"로 솔직하게 인정하되, 영향은 적다고 포장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 비즈니스 모델 미확정 | "We haven't closed that, but at the end of the day, it doesn't matter. We're not really driving to see if we can procure the memory, even though it'll be a better option. But if our customer wants to procure the memory, then it's fine as well." | "확정 안 했습니다. 하지만 결국 중요한 건 아닙니다. 우리가 메모리를 직접 구매하는 게 더 낫겠지만, 고객이 구매 원하면 그것도 괜찮습니다." |

**패턴 공식**: `We haven't closed that, but at the end of the day, it doesn't matter. We're not really driving to X, even though Y. But if Z, then it's fine as well.`

**Audrey 교훈**: "We haven't closed that"는 "결정 안 했습니다"의 솔직한 인정. 그리고 즉시 "at the end of the day, it doesn't matter"로 중요성을 축소. 결정 미루기를 부드럽게 만드는 화법이다. "We're not really driving to X" - "우리가 주도하지 않겠다"로 자신의 의도를 낮추고, "if customer wants, it's fine"으로 선택권을 상대에게 넘긴다. "검토 중"이라는 한국어 회피를 영어로 할 때, "we haven't closed that, but it doesn't matter"가 훨씬 자연스럽다.

### 전략 5: 정보 부재의 외부 탓 (External Blame for Info Gap)

정보가 없는 것을 자기 탓이 아니라 시장 상황 탓으로 돌린다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 고객 로드맵 정보 부재 | "we haven't actually seen the technical background or technical details of what our customers are planning but we're just seeing in the first hand the price hikes or the sensitivity to the prices in the DUM." | "고객이 계획하는 기술적 배경이나 상세는 아직 못 봤습니다. 다만 1차적으로 DUM에서 가격 인상이나 가격 민감도를 보고 있습니다." |
| 시장 상황 탓 | "I think they're preparing something in the background but the market conditions are not good enough that they are able to share that information." | "고객들이 뒤에서 뭔가 준비는 하고 있는 것 같습니다. 하지만 시장 상황이 그 정보를 공유할 만큼 좋지 않습니다." |
| 쇼크 탓 | "26 is too much of a shock in the first year of all this so maybe it'll stabilize a little bit in people's customers' minds for the next year" | "26년은 1년차라 너무 큰 충격입니다. 내년에는 고객 마인드에서 약간 안정화되리라 봅니다." |

**패턴 공식**: `We haven't actually seen X, but we're just seeing Y in the first hand. I think they're preparing something, but the market conditions are not good enough that they are able to share.`

**Audrey 교훈**: "they are not able to share" - 주어를 "we don't have"가 아니라 "they are not able to"로. 정보가 없는 게 내 능력 부족이 아니라 상대가 공유 못 하는 상황 탓. 이게 부정을 외부로 돌리는 화법이다. "시장 상황이 안 좋아서 고객이 정보 못 준다"는 한국어 발화를 영어로 할 때, "the market conditions are not good enough that they are able to share"를 써라.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 로드맵과 시장 전망을 정중하게 도전하는 패턴. 네가 직접 써야 할 화법이다.

### 질문 유형 1: 호기심 프레이밍 (Curiosity Framing)

질문을 "궁금해서"로 포장해 공격감을 없앤다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I'm just curious like how much X are you expecting in Y?` | "I'm just curious like how much pushout are you expecting in LPDDR6 or flagship?" | "just curious like" - 호기심으로 포장, "how much"로 수치 질문 |
| `I was just saying that we understand you're not ready for today` | "I was just saying that we understand you're not ready for today" | "just saying" + "we understand" - 양해 구하면서 압박 |

**Audrey 교훈**: "I'm just curious like"는 공격적 질문을 부드럽게 만드는 전형적 화법이다. "how much pushout are you expecting"이라는 직접 질문을 "just curious"로 포장. "just"가 핵심 단어 - "단지 궁금해서"의 뉘앙스. 한국어 "그냥 궁금해서요"의 영어 버전이 "I'm just curious like"다.

### 질문 유형 2: 도움 요청 프레이밍 (Help-seeking Framing)

질문을 "도움이 필요하다"로 포장해 발표자를 전문가 위치에 올린다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `this is an area where we need your help your insight on` | "Just aside from the data what we're seeing and this is where this is an area where we need your help your insight on at least in the mobile segments right" | "we need your help your insight" - 전문가 대우 + 질문 |
| `if you could take that and give us some guidance going forward, that would help` | "But if you could take that and give us some guidance going forward, that would help." | "if you could... that would help" - 정중한 요청 공식 |

**Audrey 교훈**: "this is an area where we need your help your insight" - 질문을 도움 요청으로 포장. 발표자가 "내게 가르쳐 달라"는 자세를 보이면 방어적으로 답할 이유가 없다. "we need your help" + "your insight" 두 번 전문가 대우. 그리고 "if you could take that and give us some guidance going forward, that would help" - "guidance"가 핵심 단어. "가이던스를 달라"는 비즈니스 영어의 정중한 요청이다. "if you could X, that would help" 구조를 외워라.

### 질문 유형 3: 이유 질문 (Reason Inquiry)

설계 의도를 탐색하는 정중한 "Is there a reason" 패턴.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Is there a reason why X is also being sensitive to Y?` | "Is there a reason why Allcome is also being sensitive to the SoCAM prices?" | "Is there a reason why" - 정중한 이유 탐색 |
| `Is that X exclusively for Y or that applied to Z?` | "Is that Z height requirement exclusively for side by side SIP or that applied to CUB?" | "exclusively"로 범위 명확화 |
| `Are you primarily worried about X versus Y?` | "Are you primarily worried about LP5 versus LP6 SoCAM price differences?" | "primarily worried" - 핵심 우려 확인 |

**Audrey 교훈**: "Why are you X?"는 공격적으로 들린다. "Is there a reason why X?"는 정중하다. 주어가 "you"에서 "reason"으로 옮겨가서 비난감을 줄인다. "Allcome is being sensitive to SoCAM prices"라는 비판적 관찰을 "Is there a reason why Allcome is also being sensitive to X?"로 포장하면, 비난이 아니라 이해 시도가 된다. 이 패턴은 모든 비즈니스 회의에서 쓸 수 있다.

### 질문 유형 4: 확인식 되물음 (Confirm-as-Question)

상대의 말을 되물어 이해를 확인하고, 동시에 다른 가능성을 시사한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I think you should apply the X on Y, but you're saying there's no X on Y?` | "I think you should apply the heat slug on the top of the S-O-C package, but you're saying there's no heat slug on the top of the S-O-C?" | 자기 의견 + 되물음 - 의견 제시하면서 확인 |
| `So it's going to be the X?` | "So it's going to be the customer's thoughts?" | 짧은 되물음 - 비즈니스 모델 확인 |
| `Are you also kind of considering the fact that that's going to act as a cost adder for customers and baby?` | "Are you also kind of considering the fact that that's going to act as a cost adder for customers and baby?" | "kind of considering" - 부드러운 우려 제기 |

**Audrey 교훈**: "I think you should X, but you're saying Y?" - 자기 의견을 먼저 내고, 상대의 말과 다르면 되물음. 공격이 아니라 "내가 이해한 게 맞나요?"를 시도. 그리고 "Are you also kind of considering the fact that X?" - "kind of"가 부드러움을 만들고, "considering the fact that"가 우려를 사실 기반으로 표현. "cost adder"라는 비용 전문 용어가 우려의 구체성을 높인다. 네가 파트너 제안의 비용 우려를 제기할 때, "Are you also kind of considering the fact that X will act as a cost adder for Y?"를 써라.

### 질문 유형 5: 비교·대조 질문 (Comparison Probe)

상대 발표 내용과 다른 경우를 제시해 논리 일관성을 테스트한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Contrary to X, right? So X showed opposite trends where Y` | "Contrary to LPDDR, right? So LPDDR showed opposite trends where your customers are asking for decreased capacity." | "Contrary to" - 자료 내 모순 지적 |
| `You don't see there'll be any uptake on X at all?` | "You don't see there'll be any uptake on AI use cases at all." | "any uptake at all" - 가능성 배제 확인 |
| `Are you seeing such demands?` | "Are you seeing such demands?" | 짧은 확인 질문 |

**Audrey 교훈**: "Contrary to LPDDR, right?" - 자료의 다른 부분과 비교해 "이건 다른 거 아닌가요?"를 제기. "right?"로 동의를 유도하면서. "any uptake at all" - "at all"이 "전혀 없다"는 강한 의미를 부드럽게 전달. "전혀 없다고 보십니까?"의 영어 버전. 발표 자료에서 모순을 발견하면 "Contrary to X, right?"로 질문을 시작해라.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 핵심 섹션. Type B 회의에서는 타임라인·볼륨·스펙·비즈니스 모델을 맞추는 언어가 중요하다.

### 타겟·타임라인 언어

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 확정 일정 | Qualcomm | "we are working on 8,975. That is slated for LPDDR 5 and 6 combo at 5.3" | "slated for X" - 확정 |
| 희망 일정 | Qualcomm | "going forward 8,875, we are hoping that we can actually do LP6" | "hoping that we can actually do" - 희망 표시 |
| 전환 시점 | Qualcomm | "So we're thinking that for one transition in 26, we did the offset pop" | "for one transition in 26" - 시점 명시 |
| 미래 탐색 | Qualcomm | "So we're looking at that" | "looking at" - 검토 중 |
| 기대 시점 | Qualcomm | "And hopefully when there is, you know, 27 comes around, there'll be more designs in LP6" | "when 27 comes around" - 미래 전환 |

**Audrey 교훈**: Type B 회의에서는 "확정"과 "희망"을 구분하는 단어가 중요하다. "slated for" = 확정, "hoping that" = 희망, "looking at" = 검토 중. 네가 파트너에게 일정을 말할 때, 확정은 "slated for", 희망은 "we're hoping we can actually do X", 검토는 "we're looking at that"으로 구분해라. 세 가지가 섞이면 신뢰성이 떨어진다.

### 볼륨·공급 요청 언어

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 공동 밀어붙임 | Qualcomm | "we do want to push LP6 as much as we could" | "push X as much as we could" - 최대 밀어붙임 |
| 고객 공동 압박 | Qualcomm | "We should push them to see if there is a possibility of launching with LP6, even for the few designs" | "we should push them to see if there is a possibility" - 공동 행동 |
| 협력 필요성 | Qualcomm | "We need to work with you guys to figure out the Z heights for LP5X and LP6" | "need to work with you guys to figure out X" - 협력 요청 |
| 고객 선택권 | Qualcomm | "So it's going to be the customer's thoughts? - They can decide as to which one." | "customer's thoughts" + "they can decide" - 고객 결정권 |

**Audrey 교훈**: "we should push them" - "we"가 협력의 핵심. "you should push"가 아니라 "we should push"로 같이 하자고 제안. "even for the few designs" - "몇 디자인이라도"로 소극적 시작을 승인. 네가 파트너와 공동으로 고객을 설득할 때, "we should push them to see if there is a possibility of X, even for a few Y"를 써라.

### 스펙 푸시백·대안 언어

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 대안 제시 | Qualcomm | "There could be other ways of packaging technology or how we package the dies could be different." | "There could be other ways of X" - 대안 가능성 |
| 범위 한정 | SK | "Is that Z height requirement exclusively for side by side SIP or that applied to CUB?" | "exclusively for X or applied to Y" - 범위 명확화 |
| 단일 옵션 제안 | Qualcomm | "We would like to offer both CUB and side by side SIP with LP5X." | "would like to offer both X and Y" - 다중 옵션 제공 |
| 단일 패키지 고집 | Qualcomm | "So we would like to do the same SKU for both options." | "would like to do the same X for both options" - 단순화 요구 |
| 비교 거절 | Qualcomm | "We won't have to do a SKU on top of that." | "won't have to do X on top of that" - 추가 부담 거부 |

**Audrey 교훈**: "We would like to offer both X and Y" - 정중한 제안. "We would like to"가 "We want to"보다 정중하고, "offer both"가 "provide both"보다 제안 느낌이 강하다. 그리고 "We won't have to do X on top of that" - "그 위에 또 X할 필요 없다"로 추가 작업 거부. "on top of that"이 핵심 - "그것까지 해야 한다면 부담"을 암시. 네가 파트너 요청을 거절할 때, "We won't have to do X on top of that"로 정중하게 거부해라.

### 마일스톤·비즈니스 모델 조율

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 미결정 인정 | Qualcomm | "We haven't closed that, but at the end of the day, it doesn't matter." | "haven't closed" + "doesn't matter" - 결정 미루기 |
| 주도 의사 없음 | Qualcomm | "We're not really driving to see if we can procure the memory" | "not really driving to X" - 주도 의사 부재 |
| 고객 선택권 | Qualcomm | "But if our customer wants to procure the memory, then it's fine as well." | "if customer wants X, it's fine as well" - 유연성 |
| 기술 논의 예약 | Qualcomm | "We'll discuss the technical details in the later slides. We have several questions regarding that." | "later slides" + "several questions regarding" - 후속 예약 |
| 후속 약속 | SK | "We'll check internally and just get back to you on in terms of you know how much detail we can share" | "check internally and get back to you" - 후속 약속 |
| 가이던스 요청 | SK | "if you could take that and give us some guidance going forward, that would help" | "if you could X, that would help" - 정중 요청 |

**Audrey 교훈**: "We haven't closed that, but at the end of the day, it doesn't matter" - 결정 미루기를 "중요하지 않다"로 포장. "at the end of the day"가 비즈니스 회의에서 자주 쓰이는 "결국" 표현. "We're not really driving to X" - "주도하지 않겠다"로 자기 의도를 낮추고, "if customer wants X, it's fine as well" - "고객이 원하면 그것도 괜찮다"로 유연성 표시. 네가 결정을 미뤄야 할 때, 이 3단 패턴을 외워라.

### 후속 액션

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 내부 확인 약속 | SK | "We'll check internally and just get back to you on in terms of you know how much detail we can share" | "check internally and get back to you on X" - 후속 약속 |
| 내부 논의 약속 | SK | "we'll definitely just discuss internally our marketing team" | "definitely discuss internally" - 강한 약속 |
| 후속 논의 예약 | Qualcomm | "We'll discuss the technical details in the later slides. We have several questions regarding that. For ideas, maybe." | "later slides" + "several questions regarding" - 후속 예약 |
| 양해 구하기 | SK | "I was just saying that we understand you're not ready for today." | "we understand you're not ready" - 양해 표시 |
| 감사 표시 | SK | "I appreciate that." | "I appreciate that" - 감사 표시 |

**Audrey 교훈**: 회의에서 "I'll check"는 약하다. "We'll check internally and get back to you on X" - "내부 확인 후 회신"의 공식적 표현. "definitely discuss internally" - "definitely"가 약속을 강하게 만든다. 그리고 "We have several questions regarding that" - "몇 가지 질문이 더 있다"로 후속 논의를 예약. 네가 회의에서 후속 액션을 약속할 때, "check internally + get back to you + definitely discuss" 3단 패턴을 써라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 DRAM/NAND/SoC/패키징 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **LPDDR5X / LPDDR6** | 모바일용 LPDDR 5세대 고속 / 6세대 | "we are working on 8,975. That is slated for LPDDR 5 and 6 combo at 5.3" - "slated for X at Y" |
| **8975 / 8875** | Qualcomm SoC 모델명 (연도+세대) | "we are working on 8,975" / "going forward 8,875" - 연도별 로드맵 |
| **COB (Chip on Board)** | 칩을 메인보드에 직접 실장하는 패키징 | "going forward in 27 is COV, which is chip on board" - "chip on board"로 풀이 |
| **SIP (System in Package)** | 여러 칩을 단일 패키지로 통합 | "the side by side SIP" - "side by side"로 위치 설명 |
| **PoP (Package on Package)** | 두 패키지를 위아래로 적층 | "offset pop as we communicated last time" - "offset" 변형 |
| **offset PoP** | SoC와 메모리 패키지를 어긋나게 적층해 열 방출 개선 | "we did the offset pop, which actually gives us enough gains on the thermals" - "gains on the thermals" |
| **Z-height** | 패키지 수직 높이 | "we need to revisit and see if there's a path for us to drop the Z height" - "drop the Z height" |
| **heat slug** | 방열 금속 부품 | "What about heat slug? - No, no, no, no heat slug." - 부정 강조 |
| **UFS 5.0 Gear 6.2 lanes** | Universal Flash Storage 5.0, Gear 6, 2레인 | "that remains to be UFS 5.0 Gear 6.2 lanes" - "remains to be" 스펙 유지 |
| **4-channel DRAM** | 4채널 구성 DRAM | "what we're describing as POP in 2027 time frame will be just 4-channel DRAM" |
| **combo (LPDDR5X + LPDDR6)** | 두 spec 동시 지원 | "LPDDR 5 and 6 combo at 5.3" - "combo at X" data rate |
| **bit growth** | bit 생산량 증가율 | "NAND bit growth is similar to 20%" - 비율 표시 |
| **wafer capacity** | 웨이퍼 생산 능력 | "the vapor capacity to be limited" - "capacity" 단독 사용 |
| **bit penalty** | 신규 제품에서 기존 대비 생산성 손실 | "productivity of HCBM4 is projected to be only about 80% of HCBM3E productivity" - 수치화 |
| **bit output growth** | bit 생산량 증가 | "bit output growth will primarily rely on the tech transition" - "rely on X" |
| **BoM cost (bomb cost)** | Bill of Materials - 재료 비용 | "Medium-low model facing a severe bomb cost pressure" - "BoM cost"의 음성 인식 오류 |
| **HBM3E / HBM4** | High Bandwidth Memory 3세대 강화 / 4세대 | "productivity of HCBM4 is projected to be only about 80% of HCBM3E productivity" |
| **FAB** | 반도체 팹 (Wuxi/Korea) | "Our Korea FAP is dedicated to handle HBM and sovereign demand our Uchi FAP is fully okay allocate to serve mobile customer" - "Uchi" = Wuxi |
| **sovereign demand** | 자국 우선 / 전략 수요 | "Korea FAP is dedicated to handle HBM and sovereign demand" - 우선순위 |
| **UFS 4.X / 5.X** | Universal Flash Storage 버전 | "we expect UFS 4.X portion to be increasing" - "portion" 표현 |
| **eMMC** | embedded MultiMediaCard (구형 스토리지) | "the market share is shrinking, limited to lower end segments" |
| **MCP (Multi-Chip Package)** | 멀티 칩 패키지 (NAND+컨트롤러) | "mainly used for Samsung and Lenovo, and we believe it to be phased out by two or three years" |
| **YMTC** | Yangtze Memory Technologies (중국 NAND) | "driven by Chinese supplier YMTC's expansion and supply flexibility" |
| **SKU** | Stock Keeping Unit - 제품 코드 | "basic SKUs for LP5 and LP6" - "basic SKUs" |
| **pinout** | 패키지 핀 배치 | "that's the pinout challenge" - 기술적 한계 |
| **cost adder** | 비용 증가 요인 | "that's going to act as a cost adder for customers and baby" - "act as a cost adder" |
| **transitionary time** | 과도기 | "we're hoping that that's just a transitionary time for 26" - 일시적 현상 |
| **killer application** | 도입을 촉진할 핵심 앱 | "unless the killer application emerge that truly demonstrate the power of the on-device AI" |
| **on-device AI** | 기기 내 AI | "OEM or has them to switch to LPDR6 instead of rushing into the LPDR6" |
| **scale of economy** | 규모의 경제 | "customers' expectation is they want to leverage the scale of economy" |
| **killer application emerge** | 핵심 앱 등장 | "unless the killer application emerge" - 도입 조건 |
| **SoCAM** | Snapdragon X / AI PC 관련 SoC (추정) | "the SoCAM market, people are at least at this time, they think they're willing to take the price premium" - "price premium" |
| **4 ball LPDDR5** | 4-ball LPDDR5 (패키지 변형) | "expansion of SOC supporting to 45 ball LPDDR5" - "45 ball" 핀 수 |
| **POP vs discrete** | 패키지 적층 vs 개별 실장 | "we are also seeing transition to discrete for the flagship" - "transition to discrete" |
| **DDR5** | 서버용 DRAM 5세대 | "ddr5 prices higher because of the demand" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 50개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m15-001
  expression: "as you guys are familiar with the X, I think there are a few changes"
  category: change_framing
  function: familiar_reference
  speaker_role: presenter
  difficulty: 4
  context: "So as you guys are familiar with the roadmap, I think there are a few changes"
  note: 로드맵 발표 시작 공식 - 친숙함 전제 + 변화 신호

- id: m15-002
  expression: "Now we have like N tiers in the X"
  category: structure_change
  function: reorganization_stating
  speaker_role: presenter
  difficulty: 3
  context: "Now we have like three tiers in the 800 flagship"
  note: "Now we have like N tiers" - 구조 변화 선언

- id: m15-003
  expression: "Primarily because of the dynamics in X, right?"
  category: reason_with_tag
  function: reason_plus_agreement
  speaker_role: presenter
  difficulty: 4
  context: "Primarily because of the dynamics in that idea market, right?"
  note: "right?"로 청중 동의 끌어내기

- id: m15-004
  expression: "I won't say X, but we need to be more Y"
  category: soft_correction
  function: self_correction
  speaker_role: presenter
  difficulty: 5
  context: "we need to be more, I won't say aggressive, but we need to be more competitive"
  note: 자기 교정 - 너무 강한 단어를 즉시 회수

- id: m15-005
  expression: "we are working on X. That is slated for Y"
  category: spec_declaration
  function: confirmed_schedule
  speaker_role: presenter
  difficulty: 4
  context: "we are working on 8,975. That is slated for LPDDR 5 and 6 combo at 5.3"
  note: "slated for" - 확정 일정 표시

- id: m15-006
  expression: "going forward X, we are hoping that we can actually do Y"
  category: future_hope
  function: future_target
  speaker_role: presenter
  difficulty: 4
  context: "And then going forward 8,875, we are hoping that we can actually do LP6"
  note: "going forward" 다음 제품 전환

- id: m15-007
  expression: "The X doesn't change on either one of them"
  category: spec_persistence
  function: unchanged_emphasis
  speaker_role: presenter
  difficulty: 3
  context: "The UFS doesn't change on either one of them"
  note: "doesn't change" - 변하지 않는 스펙 강조

- id: m15-008
  expression: "that remains to be X"
  category: spec_persistence
  function: unchanged_spec
  speaker_role: presenter
  difficulty: 3
  context: "that remains to be UFS 5.0 Gear 6.2 lanes"
  note: "remains to be" - 스펙 유지

- id: m15-009
  expression: "I don't know if you guys have any questions on the X"
  category: question_invitation
  function: humble_check
  speaker_role: presenter
  difficulty: 3
  context: "I don't know if you guys have any questions on the packaging for 8,975"
  note: "I don't know if" - 겸손한 질문 유도

- id: m15-010
  expression: "There are some, maybe we can have that discussion later on"
  category: deferral
  function: follow_up_redirect
  speaker_role: presenter
  difficulty: 4
  context: "There are some, maybe we can have that discussion later on"
  note: 후속 논의로 미루는 정중한 화법

- id: m15-011
  expression: "We need to work with you guys to figure out the X"
  category: collaboration_request
  function: cooperation_ask
  speaker_role: presenter
  difficulty: 4
  context: "We need to work with you guys to figure out the Z heights for LP5X and LP6"
  note: "work with you guys to figure out" - 협력 필요성 표시

# ── 협력 제안 (Collaboration Push) ──
- id: m15-012
  expression: "we do want to push X as much as we could"
  category: push_strategy
  function: emphatic_push
  speaker_role: presenter
  difficulty: 4
  context: "we do want to push LP6 as much as we could because we've all worked so hard on it"
  note: "do want to push" - 강조 + 협력 촉구

- id: m15-013
  expression: "We should push them to see if there is a possibility of X"
  category: joint_action
  function: co_push_request
  speaker_role: presenter
  difficulty: 5
  context: "We should push them to see if there is a possibility of launching with LP6, even for the few designs"
  note: "we should push" - "we"가 협력의 핵심

- id: m15-014
  expression: "I think it's just the fact that we need to have it out there to show X"
  category: existence_argument
  function: presence_justification
  speaker_role: presenter
  difficulty: 4
  context: "I think it's just the fact that we need to have it out there to show the differences and the gaps"
  note: "have it out there" - 존재감 확보 논리

# ── 회피·포장 (Hedging & Deflection) ──
- id: m15-015
  expression: "I understand what your question is. We'll check internally and just get back to you on X"
  category: information_boundary
  function: polite_deflection
  speaker_role: negotiator
  difficulty: 5
  context: "Okay I understand what your question is. We'll check internally and just get back to you on in terms of you know how much detail we can share"
  note: "I don't know" 대신 - 정중한 회피 + 후속 약속

- id: m15-016
  expression: "I'm not sure what scope or what level of information we can provide"
  category: authority_boundary
  function: scope_disclaimer
  speaker_role: negotiator
  difficulty: 5
  context: "I'm not sure what scope or what level of information we can provide, but we'll definitely just discuss internally our marketing team"
  note: "권한 없음"을 정중하게 표현

- id: m15-017
  expression: "we'll definitely just discuss internally our marketing team"
  category: internal_commitment
  function: definite_followup
  speaker_role: negotiator
  difficulty: 4
  context: "we'll definitely just discuss internally our marketing team"
  note: "definitely"로 후속 약속 강화

- id: m15-018
  expression: "we're hoping that that's just a transitionary time for X"
  category: hope_hedging
  function: temporary_framing
  speaker_role: presenter
  difficulty: 5
  context: "we're hoping that that's just a transitionary time for 26"
  note: 부정적 현상을 일시적으로 프레이밍

- id: m15-019
  expression: "hopefully when there is X comes around, there'll be more Y"
  category: future_hope
  function: future_shift
  speaker_role: presenter
  difficulty: 4
  context: "hopefully when there is, you know, 27 comes around, there'll be more designs in LP6"
  note: "when X comes around" - 미래 시점 전환

- id: m15-020
  expression: "I won't comment on that because it's not my feed"
  category: domain_boundary
  function: polite_decline
  speaker_role: presenter
  difficulty: 5
  context: "So I won't comment on that because I don't want to, you know, because it's not my feed"
  note: "it's not my feed" - 전문 분야 아님을 이유로 거절

- id: m15-021
  expression: "there are other ways that X is looking at to make that happen"
  category: alternative_pointer
  function: vague_alternative
  speaker_role: presenter
  difficulty: 4
  context: "there are other ways that companies are looking at to make that happen"
  note: 거절 후 즉시 대안 제시

- id: m15-022
  expression: "it doesn't have to be the X. There could be other ways of Y"
  category: alternative_expansion
  function: possibility_expansion
  speaker_role: presenter
  difficulty: 4
  context: "it doesn't have to be the DRAM high. There could be other ways of packaging technology or how we package the dies could be different"
  note: "다른 방법이 있다"로 가능성 확장

- id: m15-023
  expression: "We haven't closed that, but at the end of the day, it doesn't matter"
  category: non_decision
  function: importance_downplay
  speaker_role: presenter
  difficulty: 5
  context: "We haven't closed that, but at the end of the day, it doesn't matter"
  note: 결정 미루기를 "중요하지 않다"로 포장

- id: m15-024
  expression: "We're not really driving to see if we can X, even though Y"
  category: non_leadership
  function: intent_downplay
  speaker_role: presenter
  difficulty: 5
  context: "We're not really driving to see if we can procure the memory, even though it'll be a better option"
  note: 자기 의도를 낮추는 화법

- id: m15-025
  expression: "if our customer wants to X, then it's fine as well"
  category: customer_choice
  function: flexibility_show
  speaker_role: presenter
  difficulty: 4
  context: "if our customer wants to procure the memory, then it's fine as well"
  note: 선택권을 상대에게 넘기는 화법

- id: m15-026
  expression: "we haven't actually seen X but we're just seeing Y in the first hand"
  category: info_gap_acknowledgment
  function: limited_info_stating
  speaker_role: negotiator
  difficulty: 4
  context: "we haven't actually seen the technical background or technical details of what our customers are planning but we're just seeing in the first hand the price hikes"
  note: 정보 부재 인정 + 1차 관찰 강조

- id: m15-027
  expression: "the market conditions are not good enough that they are able to share that information"
  category: external_blame
  function: info_gap_attribution
  speaker_role: negotiator
  difficulty: 5
  context: "the market conditions are not good enough that they are able to share that information"
  note: 정보 부재를 시장 상황 탓으로 돌림

- id: m15-028
  expression: "X is too much of a shock in the first year of all this"
  category: shock_attribution
  function: situation_blame
  speaker_role: negotiator
  difficulty: 4
  context: "26 is too much of a shock in the first year of all this"
  note: 외부 충격으로 상황 설명

# ── 정중한 도전 (Polite Challenge) ──
- id: m15-029
  expression: "I'm just curious like how much X are you expecting in Y?"
  category: curiosity_framing
  function: soft_probe
  speaker_role: questioner
  difficulty: 4
  context: "I'm just curious like how much pushout are you expecting in LPDDR6 or flagship?"
  note: "just curious like" - 공격성 제거

- id: m15-030
  expression: "this is an area where we need your help your insight on"
  category: help_seeking
  function: expert_positioning
  speaker_role: questioner
  difficulty: 5
  context: "this is an area where we need your help your insight on at least in the mobile segments right"
  note: 질문을 도움 요청으로 포장

- id: m15-031
  expression: "if you could take that and give us some guidance going forward, that would help"
  category: guidance_request
  function: polite_request
  speaker_role: questioner
  difficulty: 5
  context: "if you could take that and give us some guidance going forward, that would help"
  note: "if you could X, that would help" - 정중한 요청 공식

- id: m15-032
  expression: "Is there a reason why X is also being sensitive to Y?"
  category: reason_inquiry
  function: polite_reason_probe
  speaker_role: questioner
  difficulty: 4
  context: "Is there a reason why Allcome is also being sensitive to the SoCAM prices?"
  note: "Why X" 대신 "Is there a reason why X"

- id: m15-033
  expression: "Are you primarily worried about X versus Y?"
  category: concern_clarification
  function: priority_check
  speaker_role: questioner
  difficulty: 4
  context: "Are you primarily worried about LP5 versus LP6 SoCAM price differences?"
  note: "primarily worried" - 핵심 우려 확인

- id: m15-034
  expression: "Is that X exclusively for Y or that applied to Z?"
  category: scope_clarification
  function: range_check
  speaker_role: questioner
  difficulty: 4
  context: "Is that Z height requirement exclusively for side by side SIP or that applied to CUB?"
  note: "exclusively for X or applied to Y" - 범위 명확화

- id: m15-035
  expression: "I think you should apply the X on Y, but you're saying there's no X on Y?"
  category: confirm_as_question
  function: opinion_plus_check
  speaker_role: questioner
  difficulty: 5
  context: "I think you should apply the heat slug on the top of the S-O-C package, but you're saying there's no heat slug on the top of the S-O-C?"
  note: 자기 의견 + 되물음 - 공격 아닌 확인

- id: m15-036
  expression: "Are you also kind of considering the fact that that's going to act as a cost adder for customers?"
  category: soft_concern
  function: gentle_warning
  speaker_role: questioner
  difficulty: 5
  context: "Are you also kind of considering the fact that that's going to act as a cost adder for customers and baby?"
  note: "kind of considering" + "cost adder" - 부드러운 우려 제기

- id: m15-037
  expression: "Contrary to X, right? So X showed opposite trends where Y"
  category: consistency_probe
  function: internal_contradiction
  speaker_role: questioner
  difficulty: 5
  context: "Contrary to LPDDR, right? So LPDDR showed opposite trends where your customers are asking for decreased capacity"
  note: 자료 내 모순 지적

- id: m15-038
  expression: "You don't see there'll be any uptake on X at all?"
  category: possibility_check
  function: extreme_negation_check
  speaker_role: questioner
  difficulty: 4
  context: "You don't see there'll be any uptake on AI use cases at all"
  note: "any X at all" - 가능성 배제 확인

- id: m15-039
  expression: "I was just saying that we understand you're not ready for today"
  category: consideration_statement
  function: understanding_show
  speaker_role: questioner
  difficulty: 4
  context: "I was just saying that we understand you're not ready for today"
  note: 양해 구하면서 압박 - "we understand"이 핵심

# ── 협상·액션 (Negotiation & Action) ──
- id: m15-040
  expression: "We would like to offer both X and Y"
  category: multi_option_offer
  function: option_proposal
  speaker_role: presenter
  difficulty: 4
  context: "We would like to offer both CUB and side by side SIP with LP5X"
  note: "would like to offer both" - 정중한 다중 옵션 제안

- id: m15-041
  expression: "We would like to do the same X for both options"
  category: simplification_request
  function: single_version_push
  speaker_role: presenter
  difficulty: 4
  context: "So we would like to do the same SKU for both options"
  note: 단순화 요구 - "same X for both options"

- id: m15-042
  expression: "We won't have to do a X on top of that"
  category: scope_refusal
  function: additional_burden_reject
  speaker_role: presenter
  difficulty: 4
  context: "So we won't have to do a SKU on top of that"
  note: "on top of that" - 추가 부담 거부

- id: m15-043
  expression: "it's going to be the customer's thoughts? - They can decide as to which one"
  category: customer_decision
  function: decision_delegation
  speaker_role: presenter
  difficulty: 3
  context: "So it's going to be the customer's thoughts? - Exactly. They can decide as to which one"
  note: 고객 결정권 표시

- id: m15-044
  expression: "We'll discuss the technical details in the later slides. We have several questions regarding that"
  category: followup_reservation
  function: future_topic_block
  speaker_role: presenter
  difficulty: 4
  context: "We'll discuss the technical details in the later slides. We have several questions regarding that. For ideas, maybe."
  note: "later slides" + "several questions regarding" - 후속 예약

- id: m15-045
  expression: "I appreciate that"
  category: thanks
  function: graceful_acceptance
  speaker_role: negotiator
  difficulty: 2
  context: "I appreciate that."
  note: 정중한 감사 표현

- id: m15-046
  expression: "Maybe next year some OEM all they adopt X but I think it depends on the market situation"
  category: conditional_forecast
  function: market_dependent_prediction
  speaker_role: analyst
  difficulty: 4
  context: "Maybe next year some OEM all they adopt LPDDR6 but I think it depends on the market situation"
  note: "depends on the market situation" - 조건부 예측

# ── 시장 분석가 화법 (Market Analyst Language) ──
- id: m15-047
  expression: "We forecast that X to increase by Y% through Z, driven by W"
  category: forecast_statement
  function: data_driven_prediction
  speaker_role: analyst
  difficulty: 4
  context: "We forecast that global demand to increase by 20% cater through 2030, driven by the strong demand in ESSD"
  note: "forecast X to increase by Y% through Z, driven by W" - 시장 분석가 공식

- id: m15-048
  expression: "Looking at the left-hand side, you can see that X"
  category: visual_reference
  function: chart_pointer
  speaker_role: analyst
  difficulty: 3
  context: "Looking at the left-hand side, you can see that the demand figure of ESSD is almost 40%"
  note: "Looking at the X, you can see that Y" - 차트 설명 공식

- id: m15-049
  expression: "We believe that X will remain constrained because of Y"
  category: belief_constraint
  function: position_stating
  speaker_role: analyst
  difficulty: 4
  context: "We believe that the consumer segment will remain constrained because of the bonkers pressure, inflation"
  note: "We believe X will remain Y because of Z" - 의견+근거 구조

- id: m15-050
  expression: "This is mainly because X. When you transfer to Y, there is more Z needed"
  category: causal_explanation
  function: reason_elaboration
  speaker_role: analyst
  difficulty: 4
  context: "This is mainly because of the technology migration. When you transfer to the next technology, there is more space needed to produce the same vapor"
  note: "This is mainly because X. When you Y, there is more Z needed" - 인과 설명

- id: m15-051
  expression: "Contrary to X, right? So X showed opposite trends where Y"
  category: comparison_observation
  function: contrast_stating
  speaker_role: questioner
  difficulty: 4
  context: "Contrary to LPDDR, right? So LPDDR showed opposite trends where your customers are asking for decreased capacity"
  note: 자료 내 비교 지적 - "Contrary to X, right?"

- id: m15-052
  expression: "Until 2030, the shortage will be continued"
  category: timeline_forecast
  function: long_term_prediction
  speaker_role: analyst
  difficulty: 3
  context: "Until 2030, the shortage will be continued?"
  note: 시점 명시 예측

- id: m15-053
  expression: "you're not keeping up with the capacity"
  category: direct_assessment
  function: blunt_observation
  speaker_role: questioner
  difficulty: 3
  context: "You are not keeping up with the capacity."
  note: 직접적 평가 - 분석가의 솔직 관찰

# ── 발화 채움 (Discourse Markers) ──
- id: m15-054
  expression: "by the way, that's a typo, not a typo, but it's missing X"
  category: self_correction
  function: slide_correction
  speaker_role: presenter
  difficulty: 3
  context: "By the way, that's a typo, not a typo, but it's missing LP5X"
  note: 발표 중 자료 오류 자가 교정

- id: m15-055
  expression: "Let me move to your audience. Please forward"
  category: turn_handoff
  function: speaker_switch
  speaker_role: host
  difficulty: 2
  context: "So let me move to your audience. Please forward."
  note: 발표자 전환 공식
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-04-27 10 01 41_EN_Qualcomm_Morning1-extracted.wav` (총 4,277단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 1-15) | DRAM 시장 전망 - "expected to persist until 2020 A" + "bit output growth will primarily rely on" | 시장 분석가의 전망 화법 | ★★☆ |
| 2 | LPDDR6 푸시아웃 (line 37-49) | "I'm just curious like how much pushout are you expecting" + "Maybe next year... depends on the market" | 호기심 프레이밍 + 조건부 예측 | ★★★ |
| 3 | Qualcomm 로드맵 시작 (line 169-190) | "as you guys are familiar with the roadmap, I think there are a few changes" + "Now we have like three tiers" + "I won't say aggressive, but competitive" | 변화 프레이밍 + 자기 교정 | ★★★★ |
| 4 | LP6 밀어붙임 (line 178-185) | "we do want to push LP6 as much as we could" + "We should push them to see if there is a possibility" | 협력 제안 화법 - Type B 핵심 | ★★★★ |
| 5 | Z-height + 비즈니스 모델 (line 190-260) | "We need to work with you guys to figure out the Z heights" + "We haven't closed that, but it doesn't matter" + "We'll check internally and get back to you" | 협상 + 회피 + 후속 약속 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 4, 5가 가장 가치 높음 - 협상/회피 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **roadmap alignment + market intelligence** register다. 두 가지 역할이 혼재:
- **시장 분석가 역할 (SK)**: 전망+근거 프레이밍, "We forecast X to increase by Y% driven by Z" 공식
- **로드맵 발표자 역할 (Qualcomm)**: 변화 프레이밍 + 부드러운 미루기 + 협력 제안
- **질문자 역할 (SK)**: 호기심 프레이밍, 도움 요청, 정중 도전

Type B 회의의 핵심은 "정보를 공유하면서 로드맵을 맞추는 것" - 그래서 "우리가 같이 밀어붙이자"는 협력 언어와 "내부 확인 후 회신"이라는 회피 언어가 공존한다.

### Pragmatics (화용론) 핵심
1. **"We"로 협력 제안**: "We should push them" - "You should"가 아니라 "We should"로 공동 행동 제안. Type B 회의에서 "we"가 협력의 핵심 단어.
2. **"transitionary time"으로 부정 포장**: "not much demand"를 "transitionary time"으로 일시화. 부정적 현상을 시간적 한시성으로 포장하는 화법.
3. **"it's not my feed"로 거절**: "I won't comment" + "it's not my feed" - 전문 분야 아님을 이유로 정중 거절. "모른다"가 아니라 "내 영역이 아니다"로 포장.
4. **"check internally + get back to you"**: 정보 공유 한계를 "내부 확인 후 회신"으로 포장. "I don't know"의 정중한 대체.
5. **"haven't closed that" + "doesn't matter"**: 결정 미루기를 "중요하지 않다"로 축소. "at the end of the day"가 자주 쓰이는 비즈니스 표현.

### 네가 당장 써야 할 Top 5
1. **"we do want to push X as much as we could"** - 협력 제안 강조
2. **"We should push them to see if there is a possibility of X"** - 공동 행동 제안
3. **"we'll check internally and get back to you on X"** - 정중한 회피 + 후속
4. **"we're hoping that that's just a transitionary time for X"** - 부정 현상 일시화
5. **"I'm just curious like how much X are you expecting?"** - 호기심 프레이밍 질문

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "내부 확인 후 회신 드리겠습니다" | "We'll check internally and get back to you on X" | "check internally" + "get back to you" 두 단어로 정중 |
| "검토 중입니다" | "We haven't closed that, but it the end of the day, it doesn't matter" | "haven't closed" + "doesn't matter"로 결정 미루기 부드럽게 |
| "일시적 현상입니다" | "we're hoping that that's just a transitionary time" | "transitionary time"이 일시화 핵심 |
| "왜 그렇게 하셨습니까?" | "Is there a reason why X?" | "Why" 대신 "Is there a reason" |
| "우리가 같이 밀어붙입시다" | "We should push them to see if there is a possibility of X" | "we should push" - "we"가 협력 핵심 |
| "제 전문 분야가 아닙니다" | "I won't comment on that because it's not my feed" | "feed"로 전문 영역 표현 |
| "그냥 궁금해서요" | "I'm just curious like" | "just curious"가 호기심 포장 |
| "도움이 필요합니다" | "this is an area where we need your help your insight on" | "your help your insight" 두 번 전문가 대우 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 50개 표현 중, 8절 Top 5부터 우선 숙지
3. **Type B 강점 학습**: 4절 협상·액션 화법을 중심으로 - "we should push", "check internally", "haven't closed" 3개 패턴 무조건 숙지
4. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 정중 도전 화법을 중심으로 dump 작성
5. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
6. **역할별 학습**:
   - 시장 분석가 발표할 때: 1절의 시장 분석가 화법 (m15-047~052)
   - 파트너와 로드맵 맞출 때: 4절 전체 (협상·액션 화법)
   - 파트너에게 도전할 때: 3절 (정중 도전)
   - 부정적 정보를 전달할 때: 2절 (회피·포장)

---

*Textbook 15 - Qualcomm Morning1 (2026-04-27). 회의 유형 B (로드맵/공급 정합). 표현 DB 50개. 5개 발췌 구간. 작성: 2026-09-01.*
