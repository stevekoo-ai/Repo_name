---
textbook_id: 11
meeting: DELL TDF (CXL Product Roadmap, Form Factor, DLC Shear/Compressive Force)
date: 2026-05-27
type: A (기술 Deep-dive)
partner: Dell (Brian, Sam, Robin, Greg, Corey)
sk_side: Steve Koo (CXL Product Planning), Kihoon Lee (DLC), Sam (Server Dell Product Planning), Yongjun
duration_words: 4950
audio: repo/webex-audio/2026-05-27 10 02 42_EN_DELL_TDF-extracted.wav
transcript: repo/webex-audio/2026-05-27 10 02 42_EN_DELL_TDF-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, dell, cxl, form-factor, add-in-card, e3s, dlc, shear-force, compressive-force, technical-deepdive]
---

# Textbook 11 - DELL TDF: CXL Roadmap & DLC Force Discussion (2026-05-27)

> **회의 유형**: A (기술 Deep-dive) - Steve Koo의 CXL product roadmap 발표 + form factor 비교 분석 + DLC shear/compressive force 후속 논의
> **학습 가치**: 발표자의 "비교 우위 프레이밍", 약점을 인정하며 대안 제시, Dell 측의 정중한 기술 도전, 스펙 없을 때의 정직한 회피
> **Audrey 관점**: 이 회의는 "비교 주도 발표 + 기술 defense" 유형 - 네가 Dell에 CXL product를 pitch할 때, 그리고 DLC 이슈 후속을 다룰 때 둘 다 배워야

---

## 1. 발화 아키텍처 - Steve의 발표 설계 (5단계)

Steve Koo는 발표를 5단계 구조로 설계한다. 각 단계마다 **고정된 화법 공식**이 있다. 이게 네가 따라 배워야 할 "비교 주도 발표의 뼈대"다.

### 단계 1: 3-item agenda 명시 (Roadmap Signaling)

Steve는 발표 시작 시 **세 가지 토픽을 번호로 나열**한다. "오늘은 이것들을 다룹니다"의 명시적 패턴.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Today I have prepared three key items` | "Today I have prepared three key items" | "3개 핵심 항목 준비" - 간결한 agenda |
| `First I'll introduce our X. Next I will provide Y. Finally we'll share Z.` | "First I'll introduce our product roadmap. Next I will provide several comparison among different form factors. Finally we'll share our next generation CMM concepts." | First/Next/Finally 3단계 - 발표 지도 |
| `Yeah let's move on to the next page` | "Yeah let's move on to the next page" | 슬라이드 전환 - 간결한 marker |

**Audrey 교훈**: 한국어 발표는 "오늘은 몇 가지 말씀드리겠습니다"로 시작하지만, 영어는 "Today I have prepared **three key items**"로 숫자를 명시해야. 그리고 "First / Next / Finally"로 순서를 tag해야. 청중은 숫자가 들리면 "아, 정리된 발표구나"라고 신뢰한다. "First, Next, Finally"는 초보자용이 아니라 전문가의 기본이다.

### 단계 2: 중심 강조 - "Red Box" 시각화 언어 (Center Framing)

중요 메시지를 슬라이드 중앙의 시각 요소와 연결한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The red box in the center shows our X` | "The red box in the center shows our second generation 256GB CMM" | 시각 요소 + 중앙 - 핵심 강조 |
| `Currently under development to support X over Y` | "Currently under development to support CXL 3.1 over PCIe 5.0" | "Currently under development" - 상태 표시 |
| `The ES will be provided in X and followed by the Y in Z` | "the ES will be provided in December and followed by the CS in February next year" | "X will be provided in Y" - 일정 약속 공식 |

**Audrey 교훈**: 발표에서 "이것이 핵심입니다"를 시각 언어로 전달해. "The red box in the center shows our X" - 이게 슬라이드 리딩 화법이다. 슬라이드를 가리키며 색깔+위치로 강조. 그리고 ES/CS 일정은 "X will be provided in Y, followed by Z in W"로 순차 표시. "provided"는 공식적 납품 표현이다.

### 단계 3: 비교 프레이밍 (Comparison Framing)

이 회의의 핵심 단계. **비교를 통해 자사 우위를 설득**하는 화법.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `From the X perspective, the Y offers twice the capacity of Z` | "From the total capacity perspective, the two terabyte add-in card offers twice the capacity of the 512GB E3.S" | "From X perspective, Y offers..." - 비교 기준 명시 |
| `Even if we consider X, the Y remains the same at Z` | "Even if we consider the one terabyte ES E3.S, the total capacity remains the same at 20 terabytes" | "Even if we consider" - 반론 미리 차단 |
| `It means X is not as competitive as Y` | "It means TCO is not as competitive as the add-in card solution" | "It means" - 결론 도출 공식 |
| `Therefore, X has more advantage than Y, both A and B-wise` | "Therefore, the add-in card form factor has more advantage than E3.S, both capacity and TCO-wise" | "Therefore" + "both A and B-wise" - 이중 근거 |

**Audrey 교훈**: 비교 발표는 "From the X perspective, Y offers..."로 시작해. "In terms of"도 좋지만 "From the X perspective"가 더 전문가 느낌이다. 그리고 "Even if we consider the counter-argument"로 반론을 미리 차단한 뒤 "Therefore"로 결론. "TCO-wise", "capacity-wise" - "-wise" 접미사로 관점을 tag하는 화법을 외워. "From the X perspective" + "Even if we consider Y" + "Therefore X-wise" - 이 3단 비교 공식.

### 단계 4: 약점 인정 + 대안 제시 (Concession-Alternative)

자사 제품의 한계를 인정하되 즉시 대안으로 전환.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Honestly, our early X couldn't fully meet Y demands due to Z` | "honestly our early 96 and 128GB U3.S CMM couldn't fully meet AI market demands due to the capacity and power constraints" | "Honestly" - 정직함 신호 + 과거 제품 한계 인정 |
| `So we are moving to X focused on Y and Z` | "So we are moving to terabyte level products focused on lower power and a reasonable TCO level" | "So we are moving to" - 전환의 방향 표시 |
| `We are currently in the X stage` | "We are currently in the investigation stage" | 현재 상태 - 아직 결론 아님을 정직 표시 |

**Audrey 교훈**: "Honestly"는 정직함의 신호다. 영어 발표에서 약점을 인정할 때 "Honestly"로 시작하면 신뢰가 간다. "Honestly, our early product couldn't fully meet Y" - "솔직히 말해, 우리 초기 제품은 Y를 충족 못 했다." 한국어 발표에서는 약점을 숨기려 하지만, 영어는 "Honestly"로 먼저 인정하면 신뢰가 더 쌓인다. 그리고 "So we are moving to"로 방향 전환. 이게 전문가의 정직한 발표다.

### 단계 5: 피드백 요청 (Feedback Solicitation)

발표 마무리에 feedback을 요청하는 공식.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I'd love to hear your feedback on this` | "I'd love to hear your feedback on this" | "I'd love to" - 부드러운 요청 |
| `I believe your feedback will be a great guide for our direction` | "I believe your feedback will be a great guide for our direction" | feedback을 "guide"로 격상 - 파트너 존중 |
| `Could you please share your comments or insights?` | "Could you please share your comments or insights?" | "comments or insights" - 복수 명사로 폭 넓힘 |

**Audrey 교훈**: "I'd love to hear your feedback"는 "I want to hear"보다 훨씬 부드럽다. "Could you please share your comments or insights?" - 복수 명사("comments", "insights")를 쓰면 feedback의 종류를 넓혀. 그리고 "your feedback will be a great guide for our direction" - feedback을 "guide"로 격상시키면 상대방이 "이 사람이 내 의견을 진지하게 받겠구나"라고 느낀다. 이게 파트너 존중의 화법이다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. Steve와 Sam이 약점·스펙 부재·불확실성을 어떻게 정중하게 포장하는지. DLC discussion에서 특히 빛난다.

### 전략 1: 스펙 부재 인정 + 시간 확보 (Spec Absence + Time Buffer)

스펙이 없을 때, 즉시 "없다"고 인정하되 시간을 요구한다. DLC compressive force에서 결정적 패턴.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| Compressive force 스펙 없음 | "there is no warranty coverage for compressive force with high necks. So, we cannot provide a guarantee for conditions other than those specified in the hours back" | "high necks에 대한 compressive force 보증은 없습니다. 사양서에 명시된 것 외의 조건은 보증할 수 없습니다" |
| SK 내부에도 스펙 없음 | "frankly speaking, it's not easy to provide some any feedback related to the compressive force. That's what our engineer is saying" | "솔직히 말씀드려, compressive force에 대한 feedback을 제공하기 쉽지 않습니다. 엔지니어가 그렇게 말합니다" |

**패턴 공식**: `There is no X for Y. So we cannot provide Z for conditions other than those specified. Frankly speaking, it's not easy to provide any feedback related to Y.`

**Audrey 교훈**: 영어 회의에서 "스펙이 없다"는 "We don't have specs"로 끝내면 안 된다. "There is **no warranty coverage** for X" - 공식적 부정. 그리고 "frankly speaking, it's not easy to provide any feedback" - "frankly speaking"이 정직함을 표시하고, "not easy"가 거부를 부드럽게 만든다. "We cannot"이 단호하지만 "frankly speaking"이 앞에 오면 정중하게 들린다. 이 조합을 외워.

### 전략 2: 시간 지연 - "3 months" buffer (Time Deferral)

DLC shear force에서 샘플 제작에 시간이 걸린다는 정직한 회피.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Shear force 샘플 제작 중 | "samples are currently being manufactured for each component. And it takes orders have been placed and the process is expected to take approximately two to three months" | "각 컴포넌트별로 샘플 제작 중입니다. 주문은 이미 들어갔고, 약 2-3개월 걸릴 예정입니다" |
| 데이터 제공 시점 | "after three months, we can provide real data of shear force" | "3개월 후 shear force 실측 데이터를 제공할 수 있습니다" |
| 특수 팀 구성 필요 | "we have to, we are trying to build a special team that's the old Nairy Arding transport, the checking the shear force. So, building that team takes time" | "shear force 측정을 위한 특수 팀 구성이 필요합니다. 팀 구성에 시간이 걸립니다" |

**패턴 공식**: `Samples are being manufactured. The process is expected to take approximately X months. After X months, we can provide real data. We are trying to build a special team, which takes time.`

**Audrey 교훈**: 시간 지연은 구체적으로 말해. "It takes time"은 약하다. "Approximately two to three months"로 구체적 기간을 주면 신뢰가 생긴다. 그리고 이유까지 주면 더 강하다 - "we are trying to build a special team, which takes time." 한국어 "시간이 좀 걸립니다"의 영어 버전은 "approximately X months, because we have to build a special team"이다. 이유가 동반된 시간 지연은 거부감을 낮춘다.

### 전략 3: 추가 데이터 요구로 후속 미루기 (Data Request Deferral)

상대방이 데이터를 더 달라고 해야 답을 줄 수 있다고 하면서 후속을 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Compressive force 데이터 요청 | "we have to ask for additional testing, but we don't have any specific conditions yet" | "추가 테스트를 요청해야 하지만, 아직 구체적 조건이 없습니다" |
| 추가 detail 필요 | "if you can provide some additional details on the compressive force, then we'll be able to have some additional discussion" | "compressive force에 대한 추가 detail을 주시면, 추가 논의가 가능합니다" |
| 이메일로 specifics 요구 | "perhaps Hinex should send an email with the particulars so that I can make sure we answer the right questions" | "Hinex에서 specifics를 이메일로 주시면, 정확한 질문에 답변할 수 있도록 하겠습니다" |

**패턴 공식**: `We have to ask for additional testing, but we don't have specific conditions yet. If you can provide additional details on X, then we'll be able to have additional discussion. Perhaps you should send an email with the particulars.`

**Audrey 교훈**: 답을 미룰 때 상대방에게서 데이터를 끌어내는 조건을 걸어. "If you can provide X, then we can have additional discussion" - "X를 주시면 추가 논의 가능합니다." 이게 책임을 상대에게 일부 넘기는 회피다. 그리고 "send an email with the particulars" - "particulars"가 "specifics"의 격식적 동의어. "particulars"를 쓰면 더 전문가 느낌이다.

### 전략 4: 의견을 "personal opinion"으로 한정 (Personal Opinion Hedging)

20TB가 적정 size라는 답변을 "personal opinion"으로 한정해 책임을 줄인다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 20TB 적정 size | "the reasonable size is 20 terabytes. But in the application perspective, as much as we have, I mean, in the capacity perspective in pooling system, we'll be helpful for the key value cache and improving the top performance of the AI application. But we should think about its cost level. The intermediate decision, yeah, AC, the 20 terabytes in my personal opinion" | "합리적 size는 20TB입니다. 다만 application 관점에서는 capacity가 많을수록 KV cache에 도움이 됩니다. 단, cost를 고려해야 합니다. 중간 결정으로, 제 개인적 의견으로는 20TB입니다" |

**패턴 공식**: `The reasonable size is X. But we should think about Y. The intermediate decision, X in my personal opinion.`

**Audrey 교훈**: 숫자를 말할 때 "in my personal opinion"을 붙이면 책임이 줄어든다. "20TB가 적정 size입니다"로 끝내면 약속이 되지만, "in my personal opinion"을 붙이면 "공식 입장은 아닙니다"가 된다. 한국어 "개인적 의견으로는"과 같다. 회의에서 불확실한 숫자를 말할 때 무조건 이 hedge를 붙여. 그리고 "the intermediate decision" - "중간 결정" - 최종이 아님을 명시.

### 전략 5: 약점 인정 후 TCO로 재프레이밍 (Concession + TCO Reframe)

E3.S의 thermal/서비스 이점을 인정하되 TCO로 전환.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| E3.S 장점 인정 | "E3, EDSFF, as you mentioned that they also have a good advantage. I mean, a little bit smaller granularity than the 2 terabyte and it might have a good capability for the maintenance perspective" | "E3, EDSFF는 말씀하신 대로 장점이 있습니다. 2TB보다 더 작은 granularity, maintenance 관점에서도 좋은 capability가 있습니다" |
| hot plug 한계 | "there isn't no the software or data migration solution at this moment. So I think that kind of a hot plug feature, it's useful or the valid for the industry" | "현재 hot plug software나 data migration 솔루션이 없습니다. 그런 hot plug feature가 산업에 유효하긴 합니다" |
| TCO로 전환 | "but it's 3.0 or EDSFF, they have the capacity limitations. So it means that there is still, I mean, difficult to lower it to TCO" | "하지만 3.0이나 EDSFF는 capacity 한계가 있습니다. TCO를 낮추기 어렵다는 의미입니다" |

**패턴 공식**: `X, as you mentioned, also have a good advantage. But they have capacity limitations. So it means it's still difficult to lower TCO.`

**Audrey 교훈**: 상대가 지적한 경쟁 form factor의 장점을 먼저 인정해. "as you mentioned, X also have a good advantage" - "말씀하신 대로 X도 장점이 있습니다." 그리고 "But"로 전환. 이게 정중한 반박이다. 한국어는 "하지만"으로 바로 넘어가지만, 영어는 먼저 인정하고 "But"으로 전환. "as you mentioned"를 붙이면 상대를 존중하면서 반박하는 것이 된다.

### 전략 6: "Currently we don't have" + 미래 약속 (Absence + Future Promise)

reference design이 없을 때 정직 인정 + 미래 약속.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Reference design 없음 | "Currently, we don't have. I'm not sure you are aware of that. We made one prototype for this CXL pooled memory reference platform based on this switch list. It's a multi-headed system, but it was FPGA prototype, not really a silicon type. But we are planning on having the reference platform design of the CXL pooling pooled memory system in the future" | "현재는 없습니다. 이미 아실 수 있겠지만, CXL pooled memory reference platform의 프로토타입을 하나 만들었습니다. multi-headed system인데 FPGA 프로토타입이라 실제 silicon은 아닙니다. 하지만 향후 CXL pooling reference platform 설계를 계획하고 있습니다" |

**패턴 공식**: `Currently, we don't have. I'm not sure you are aware of that. We made one prototype... but it was X, not really Y. But we are planning on having Z in the future.`

**Audrey 교훈**: "Currently, we don't have" - 짧고 정직한 부정. 그리고 즉시 "I'm not sure you are aware of that" - "이미 아실 수 있겠지만" - 상대가 모를 리 없는 정보라는 점을 겸손하게 표시. 그리고 프로토타입을 언급하되 "FPGA prototype, not really a silicon type"으로 한계를 명시. 마지막으로 "we are planning on having X in the future"로 미래 약속. 이게 정직한 회피의 4단 공식이다.

---

## 3. 정중한 도전 화법 (Dell 측 질문자)

Dell 측이 기술적으로 도전하면서도 정중하게 질문하는 패턴. **네가 파트너에 대응할 때 직접 써야 할 화법**이다. 이 회의의 질문자는 주로 Brian, Sam, Robin이다.

### 질문 유형 1: 전제 확인형 질문 (Premise Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I guess one of the questions is X` | "I guess one of the questions is the E3 approach, those modules are typically in the front of the chassis" | "I guess one of the questions is" - 겸손한 전제 제시 |
| `Is that a significant factor in your analysis?` | "Is that a significant factor in your analysis?" | "Is that a significant factor" - 분석에 반영됐는지 정중 확인 |

**Audrey 교훈**: "I guess one of the questions is X" - "제 질문 중 하나는 X입니다." "guess"가 겸손함을 표시. 그리고 "Is that a significant factor in your analysis?" - "그것이 분석에 significant factor입니까?" - "significant"를 쓰면 단순 "factor"보다 격상된 질문. "왜 안 하셨습니까"가 아니라 "이게 분석에 반영됐습니까"로 정중하게 도전.

### 질문 유형 2: 대안 제시형 질문 (Alternative Hypothesis Probe)

자사가 지원하는 다른 form factor를 제시하며 분석을 다시 하게 유도.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Dell supports X, but we also support Y for some of our Z` | "Dell supports E3S form factor, but we also support E3Long form factor for some of our storage products" | 자사 스펙 나열 - 우위 암시 |
| `So I guess the question is if this was X versus Y, that changed your analysis?` | "So I guess the question is if this was E3Long versus add-in card, that changed your analysis?" | "if X versus Y, that changed your analysis" - 가정 변경 질문 |

**Audrey 교훈**: 이게 **협상적 질문**이다. "Dell은 E3S도 지원하지만 E3Long도 지원합니다"로 자사 옵션을 나열한 뒤, "E3Long vs add-in card라면 분석이 바뀝니까?"로 물어. 이게 상대의 결론을 흔드는 정중한 도전. "if X versus Y, that changed your analysis?" - 이 패턴을 외워. 상대의 비교 기준을 바꿔서 다시 분석하게 만드는 질문이다.

### 질문 유형 3: 추가 고려사항 제시 (Additional Factor Introduction)

상대가 놓친 요소를 정중하게 제시.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The other consideration is if X, having greater Y may not be an advantage` | "The other consideration is if a memory module fails, having greater capacity may not be an advantage. It might be from a serviceability and RAS standpoint. It might be better to have twice as many modules, E3 modules versus half the number of add-in card hundreds" | "The other consideration is" - 추가 요소 제시 공식 |
| `That was the only point` | "That was the only point" | "한 가지 점만" - 공격 의도 없음을 표시 |

**Audrey 교훈**: "The other consideration is X" - "또 다른 고려사항은 X입니다." 이게 상대가 놓친 요소를 제시하는 정중한 화법. 그리고 "It might be from a serviceability and RAS standpoint" - "It might be"로 불확실성을 표시하며 의견 제시. "It might be better to have X versus Y" - 비교 제시. 마지막에 "That was the only point" - "이것만 말씀드리고 싶었습니다" - 공격 의도가 아님을 명시. 이 마무리가 중요하다. **"That was the only point"는 도전을 부드럽게 마무리하는 화법이다.**

### 질문 유형 4: 가정 명시형 질문 (Assumption Clarification)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I'm assuming that if we were going to design X, it would not be dependent on Y, right?` | "I'm assuming that if we were going to design a dedicated chassis for cooling, it would not be dependent on what our current systems are, right?" | "I'm assuming" - 가정 명시 + "right?" 확인 |
| `I'm trying to understand` | "I'm trying to understand" | "이해하려 합니다" - 겸손한 질문 전제 |

**Audrey 교훈**: "I'm assuming that X" - "제가 가정하는 건 X입니다." 자기 가정을 명시한 뒤 "right?"로 확인. 이게 질문자가 자기 이해를 표시하면서 상대를 확인시키는 화법. 그리고 "I'm trying to understand" - "이해하려 합니다" - 이게 겸손한 질문의 전제. "질문이 있습니다"가 아니라 "이해하려 합니다"로 시작하면, 질문이 도전이 아니라 학습으로 들린다.

### 질문 유형 5: 적용 범위 확인 (Applicability Probe)

DLC shear force testing의 범위를 확인하는 질문.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Will it give you a broad understanding of X for all dims, or will it be like a point answer for one dim?` | "Will it give you a broad understanding of shear force for all dims, R-dims and MR-dims that we may consider? Or will it be like a point answer, you know, a very specific answer for one dim?" | "broad understanding vs point answer" - 이분법 질문 |
| `I would hope it gives us a really broad understanding of applicability` | "I would hope it gives us a really broad understanding of applicability" | "I would hope" - 기대 표시 |
| `Just so we don't have to spend three months to build another test sample for a different dim in the future, right?` | "Just so we don't have to spend three months to build another test sample for a different dim in the future, right?" | "Just so we don't have to" - 비용 회피 이유 제시 |

**Audrey 교훈**: 이분법 질문("broad vs point")이 강력하다. "Will it give you a broad understanding or a point answer?" - 상대가 둘 중 하나를 선택해야. 그리고 "I would hope it gives us a really broad understanding" - "I would hope"로 기대를 표시하면, 상대가 좁은 답을 주기 어렵다. 마지막으로 "Just so we don't have to spend three months again" - 비용 이유를 들면 설득력이 더한다. **"I would hope X"는 정중한 기대 표시이자 암묵적 요구다.**

### 질문 유형 6: 미래 확장 질문 (Future Extension Probe)

DDR6까지 확장 가능한지 묻는 질문.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I imagine we'll have a similar question as we move forward on X as well, right?` | "I imagine we'll have a similar question as we move forward on DDR6 as well, right?" | "I imagine" - 미래 예상 질문 |
| `I think having a general understanding of what X can tolerate and what they cannot is going to be important for these kinds of solutions in the future` | "I think having a general understanding of what share forces various components can tolerate and what they cannot is going to be important for these kinds of solutions in the future" | "general understanding" + "in the future" - 장기 가치 프레이밍 |
| `my thinking was perhaps we would be able to apply some of your knowledge to X so we don't have to do this effort` | "my thinking was perhaps we would be able to apply some of your knowledge to DDR6 so we don't have to do this effort" | "my thinking was perhaps" - 겸손한 제안 |

**Audrey 교훈**: "I imagine we'll have a similar question as we move forward on X" - "X로 넘어갈 때도 비슷한 질문이 있을 것입니다." 미래 질문을 예고하며 현재 노력의 가치를 격상. 그리고 "my thinking was perhaps we would be able to apply X to Y" - "제 생각에는 어쩌면 X를 Y에 적용할 수 있을 것 같습니다." "perhaps"가 겸손함. "we don't have to do this effort" - 중복 노력 회피 이유. 이게 **장기 가치를 프레이밍하는 질문**이다.

### 질문 유형 7: 시간 target 확인 (Timeline Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So with the three months, we're going to target for the TDF in August to be able to follow up and have this conversation again. Is that your expectation from the SKHINICS team?` | "So with the three months, we're going to target for the TDF in August to be able to follow up and have this conversation again. Is that your expectation from the SKHINICS team?" | "we're going to target for X" - 시점 확정 공식 |
| `I guess so. Yeah, in three months` | (SK 답) "I guess so. Yeah, in three months" | "I guess so" - 약한 확인 |

**Audrey 교훈**: 시간을 확정할 때 "we're going to target for X"를 써. "We will"보다 "we're going to target for"이 더 공식적이고 track 가능하다. 그리고 "Is that your expectation from your team?" - 상대의 동의를 명시적으로 요구. 이게 회의에서 쌍방 합의를 만드는 화법. "I guess so"는 약하지만, 이 질문에 대해 SK가 그렇게 답한 건 쌍방 합의가 성립한 것이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

회의 후반, 후속 협상과 action item을 정하는 언어.

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| use case 분리 | Dell (Sam) | "But that's for a different use case entirely, right? The use case that we have for CXL memory today, and it's a small market, is for customers that are trying to get a certain capacity, but they can't get to that capacity without using high capacity DRIMs" | "different use case entirely" - Dell이 시장 분할로 Steve의 비교를 희석 |
| AI pooling 별도 설계 | Dell | "if we're talking about AI pooling, where we want to have very, very high capacity... it's a different trade-off. And again, if we were going to design, we would not use a current platform for that pooling. We would design something optimized for this use case" | "we would not use a current platform, we would design something optimized" - 별도 설계 의지 표시 |
| 시스템 최적화 주장 | Dell | "we're not constrained by how many PCIe lanes or CXL lanes are going to the front of the box, or the rear of the box. We would look for the most optimal module form factor and solution at the chassis level" | "we're not constrained by X, we would look for Y" - 제약 부정 + 최적화 |
| 이메일 후속 제안 | Dell | "If there's additional questions, then perhaps Hinex should send an email with the particulars so that I can make sure we answer the right questions" | "perhaps Hinex should send an email" - 책임을 SK에게 일부 이전 |
| thermal 미해결 질문 언급 | Dell | "I think we might have had some thermal discussion last time that we did not completely close, but I think the most pressing topics are the shear and the compressive force" | "did not completely close" - 미해결 표시 + "most pressing topics" 우선순위 |

**Audrey 교훈**: 
- "But that's for a different use case entirely, right?" - 이게 **시장 분할로 상대의 비교를 희석**하는 화법. Steve가 add-in card vs E3.S 비교를 했는데, Dell이 "그건 다른 use case입니다"로 분리. "entirely"가 강한 분리. 이런 도전을 당했을 때, 당황하지 말고 "I understand your use case differentiation. But..."로 받아.
- "We would not use a current platform, we would design something optimized" - Dell이 자사 설계 의지를 표시. 이게 파트너가 "너희 제품 안 쓰고 우리가 만든다"의 정중한 표현. "We would design"의 조건법이 부드럽게 만든다.
- "we did not completely close" - 미해결을 정중하게 표시. "We didn't finish"보다 "did not completely close"가 더 전문가적.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 meeting 제안 | SK (Steve) | "I expect that if you have more questions and further more, I mean, talk, I mean, we can have the separate meeting for that" | "separate meeting" - 후속 meeting 제안 |
| email 채널 개방 | SK | "feel free to talk and give feedback via email or other media" | "feel free to give feedback via email" - 비동기 채널 |
| August TDF target | Dell | "So with the three months, we're going to target for the TDF in August to be able to follow up and have this conversation again" | "target for the TDF in August" - 시점 확정 |
| August 확인 | SK | "I guess so. Yeah, in three months. Yeah. Okay. August timeframe" | "August timeframe" - 쌍방 합의 표시 |
| 추가 detail 요청 | Dell | "I would like to get your opinion on that. When you say specifics, is that specific component compressive pressures and forces that we expect?" | "I would like to get your opinion" - 의견 요청 공식 |
| Genese meeting 차주 언급 | Dell | "We will just connect next week when we're at the Genese meetings. Corey and I will" | "we will just connect next week when we're at X" - 오프라인 미팅 연결 |
| urgent question 대응 | Dell | "if there are any urgent questions or concerns from your side, feel free to let us know and we'll try to answer as soon as possible" | "feel free to let us know, we'll try to answer as soon as possible" - urgency 대응 공식 |
| 최종 종료 | Dell | "I guess that's about time. That's all the agenda we had listed for today, but any other last minute questions or comments before we end. If not, I will close the call" | "any other last minute questions before we end, if not, I will close the call" - 종료 공식 |

**Audrey 교훈**: 
- 회의 종료 시 "any other last minute questions or comments before we end" - "끝내기 전에 마지막 질문이나 comment 있습니까." 이게 **정중한 종료 공식**이다. "I'll close the call"이 단호한 마무리.
- "August timeframe" - Dell이 "in three months"를 "August timeframe"으로 명시. 시간을 구체적으로 못 박으면 합의가 확정된다.
- "we'll try to answer as soon as possible" - urgent 대응의 공식. "We'll answer soon"보다 "We'll try to answer as soon as possible"이 더 공식적이다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/form factor/DLC 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **CMM** (CXL Memory Module) | CXL 메모리 모듈 | "our second generation 256GB CMM" - "second generation" 세대 표시 |
| **ES / CS** (Engineering Sample / Customer Sample) | 엔지니어링 샘플 / 고객 샘플 | "the ES will be provided in December and followed by the CS in February next year" - 샘플 단계 일정 |
| **form factor** | 물리적 규격 | "several comparison among different form factors" - 비교 대상 |
| **add-in card (AIC)** | PCIe 카드 형태 CXL 모듈 | "the add-in card form factor has more advantage than E3.S" - Steve의 우위 주장 |
| **E3.S / E3.L (EDSFF)** | Enterprise 3 Short/Long form factor | "E3S requires double the controller count" - 단점 지적 |
| **FHHR** (Full Height Half Length) | AIC의 세부 규격 | "add-in card FHHR form factor" - 상세 규격 명시 |
| **TCO** (Total Cost of Ownership) | 총소유비용 | "TCO is not as competitive as the add-in card solution" - 비교 기준 |
| **near memory computing** | 가까운 메모리 연산 | "we have integrated the CMM-AX as a near memory computing as a POC" - POC 표시 |
| **CXL pooling** | CXL 메모리 풀링 | "focusing on the pooling system chassis" - 용도 전환 |
| **multi-headed system** | 다중 호스트 연결 시스템 | "It's a multi-headed system, but it was FPGA prototype" - FPGA 한계 명시 |
| **shear force** | 전단력 (DLC 부착 시) | "we can provide real data of shear force" - 3개월 후 데이터 약속 |
| **compressive force** | 압축력 (DLC 부착 시) | "there is no warranty coverage for compressive force with high necks" - 스펙 부재 |
| **DLC** (Direct Liquid Cooling) | 직접 액체 냉각 | "if you can adopt DLC, then how much power consumption your system can tolerate" - power 질문 |
| **PMIC** (Power Management IC) | 전력 관리 칩 | "the biggest trick seems to be if we can capture the PMIC or not" - DLC 핵심 과제 |
| **RDIM / MRDIM** | Registered DIMM / Multi-Rank DIMM | "we'll be able to use all the parts of R-dims. But in the case of MR-dims, there are some additional differences" - 범위 한정 |
| **SDDC / DDDC** | Single/Double Device Data Correction (ECC) | "RAS capability are covering both SDDC and DDDC using an 8 plus 2 configuration" - RAS 스펙 |
| **hot plug** | 전원 인가 중 장치 교체 | "the half plug feature, it's useful or the valid for the industry" - 기술 유효성 |
| **wire bonding** | 와이어 본딩 (패키징) | "It doesn't use TSP process, instead it goes through the wire bonding connections" - LPDDR 이점 |
| **3DS TSV** | 3D Stacked Through-Silicon Via | "the only way is to stack the die through the expensive 3DS TSV process" - 비용 단점 |
| **LPDDR6** | Low Power DDR6 | "the add-in card goes up to 75W. This is a sufficient power budget for LPDDR to achieve over 1TB" - LPDDR 우위 |
| **PCIe 5.0** | PCIe 5세대 | "support CXL 3.1 over PCIe 5.0" - 인터페이스 스펙 |
| **KV cache** | Key-Value 캐시 (LLM) | "the key value cache and improving the top performance of the AI application" - AI 활용 |
| **reference platform** | 참조 설계 | "we are planning on having the reference platform design of the CXL pooling system in the future" - 미래 약속 |
| **TDF** (Technical Design Forum) | Dell 기술 디자인 포럼 | "we're going to target for the TDF in August to be able to follow up" - 후속 시점 |
| **RAS** (Reliability/Availability/Serviceability) | 신뢰성/가용성/서비스용이성 | "from a serviceability and RAS standpoint, it might be better to have twice as many modules" - RAS 관점 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 50개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m11-001
  expression: "Today I have prepared three key items"
  category: presentation_opening
  function: agenda_signaling
  speaker_role: presenter
  difficulty: 3
  context: "Today I have prepared three key items. First I'll introduce our product roadmap. Next I will provide several comparison among different form factors. Finally we'll share our next generation CMM concepts"
  note: 3-item agenda 명시 - "three key items"로 숫자 표시

- id: m11-002
  expression: "First I'll introduce X. Next I will provide Y. Finally we'll share Z."
  category: presentation_structure
  function: sequence_signaling
  speaker_role: presenter
  difficulty: 3
  context: "First I'll introduce our product roadmap. Next I will provide several comparison among different form factors. Finally we'll share our next generation CMM concepts"
  note: First/Next/Finally - 발표 3단 지도

- id: m11-003
  expression: "Yeah let's move on to the next page"
  category: slide_transition
  function: forward_move
  speaker_role: presenter
  difficulty: 2
  context: "Yeah let's move on to the next page"

- id: m11-004
  expression: "The red box in the center shows our X"
  category: visual_leading
  function: focus_directing
  speaker_role: presenter
  difficulty: 4
  context: "The red box in the center shows our second generation 256GB CMM"
  note: 시각 요소 + 위치로 핵심 강조

- id: m11-005
  expression: "Currently under development to support X over Y"
  category: status_stating
  function: dev_state
  speaker_role: presenter
  difficulty: 3
  context: "Currently under development to support CXL 3.1 over PCIe 5.0"

- id: m11-006
  expression: "The ES will be provided in X and followed by the Y in Z"
  category: milestone
  function: sample_schedule
  speaker_role: presenter
  difficulty: 3
  context: "the ES will be provided in December and followed by the CS in February next year"
  note: ES/CS 샘플 단계 일정 공식

- id: m11-007
  expression: "From the X perspective, the Y offers twice the capacity of Z"
  category: comparison_framing
  function: advantage_stating
  speaker_role: presenter
  difficulty: 4
  context: "From the total capacity perspective, the two terabyte add-in card offers twice the capacity of the 512GB E3.S"
  note: "From the X perspective" - 비교 기준 명시

- id: m11-008
  expression: "Even if we consider X, the Y remains the same at Z"
  category: counterargument_block
  function: preemptive_defense
  speaker_role: presenter
  difficulty: 5
  context: "Even if we consider the one terabyte ES E3.S, the total capacity remains the same at 20 terabytes"
  note: "Even if we consider" - 반론 미리 차단

- id: m11-009
  expression: "It means X is not as competitive as Y"
  category: conclusion_draw
  function: consequence_stating
  speaker_role: presenter
  difficulty: 3
  context: "It means TCO is not as competitive as the add-in card solution"

- id: m11-010
  expression: "Therefore, X has more advantage than Y, both A and B-wise"
  category: dual_advantage
  function: comparison_conclusion
  speaker_role: presenter
  difficulty: 5
  context: "Therefore, the add-in card form factor has more advantage than E3.S, both capacity and TCO-wise"
  note: "both A and B-wise" - 이중 근거

- id: m11-011
  expression: "Do you have any questions on this page?"
  category: question_invitation
  function: slide_pause
  speaker_role: presenter
  difficulty: 2
  context: "Yeah, do you have any questions on this page?"

- id: m11-012
  expression: "If you don't have."
  category: silence_handling
  function: awkwardness_recovery
  speaker_role: presenter
  difficulty: 3
  context: "Okay. If you don't have."
  note: 침묵 처리 - 짧게 넘어가는 화법

- id: m11-013
  expression: "Honestly, our early X couldn't fully meet Y demands due to Z"
  category: weakness_admission
  function: honest_concession
  speaker_role: presenter
  difficulty: 5
  context: "honestly our early 96 and 128GB U3.S CMM couldn't fully meet AI market demands due to the capacity and power constraints"
  note: "Honestly" - 정직함 신호. 약점 인정의 전문가 화법

- id: m11-014
  expression: "So we are moving to X focused on Y and Z"
  category: direction_shift
  function: pivot_announcement
  speaker_role: presenter
  difficulty: 4
  context: "So we are moving to terabyte level products focused on lower power and a reasonable TCO level"

- id: m11-015
  expression: "We are currently in the investigation stage"
  category: state_hedging
  function: incomplete_status
  speaker_role: presenter
  difficulty: 3
  context: "We are currently in the investigation stage"
  note: "investigation stage" - 아직 결론 아님 정직 표시

- id: m11-016
  expression: "I'd love to hear your feedback on this"
  category: feedback_solicitation
  function: soft_request
  speaker_role: presenter
  difficulty: 3
  context: "And I'd love to hear your feedback on this"

- id: m11-017
  expression: "I believe your feedback will be a great guide for our direction"
  category: feedback_elevating
  function: partner_respect
  speaker_role: presenter
  difficulty: 5
  context: "I believe your feedback will be a great guide for our direction"
  note: feedback을 "guide"로 격상 - 파트너 존중

- id: m11-018
  expression: "Could you please share your comments or insights?"
  category: feedback_request
  function: plural_noun_request
  speaker_role: presenter
  difficulty: 3
  context: "Could you please share your comments or insights?"
  note: "comments or insights" - 복수 명사로 feedback 폭 넓힘

# ── 회피·포장 (Hedging & Deflection) ──
- id: m11-019
  expression: "there is no warranty coverage for X with Y"
  category: spec_absence
  function: formal_negation
  speaker_role: presenter
  difficulty: 4
  context: "there is no warranty coverage for compressive force with high necks"
  note: 스펙 부재의 공식적 부정

- id: m11-020
  expression: "we cannot provide a guarantee for conditions other than those specified in X"
  category: scope_limiting
  function: specification_boundary
  speaker_role: presenter
  difficulty: 5
  context: "we cannot provide a guarantee for conditions other than those specified in the hours back"
  note: "conditions other than those specified" - 보증 범위 한정

- id: m11-021
  expression: "Frankly speaking, it's not easy to provide some any feedback related to X"
  category: honest_evasion
  function: polite_refusal
  speaker_role: presenter
  difficulty: 5
  context: "frankly speaking, it's not easy to provide some any feedback related to the compressive force"
  note: "Frankly speaking" + "not easy" - 정직한 거부 공식

- id: m11-022
  expression: "samples are currently being manufactured for each component"
  category: progress_stating
  function: ongoing_work
  speaker_role: presenter
  difficulty: 3
  context: "samples are currently being manufactured for each component"

- id: m11-023
  expression: "the process is expected to take approximately X months"
  category: time_estimate
  function: duration_specific
  speaker_role: presenter
  difficulty: 4
  context: "the process is expected to take approximately two to three months"
  note: "approximately X months" - 구체적 기간이 신뢰 생성

- id: m11-024
  expression: "after X months, we can provide real data of Y"
  category: future_promise
  function: data_commitment
  speaker_role: presenter
  difficulty: 3
  context: "after three months, we can provide real data of shear force"

- id: m11-025
  expression: "we are trying to build a special team, which takes time"
  category: reason_for_delay
  function: structural_bottleneck
  speaker_role: presenter
  difficulty: 4
  context: "we have to, we are trying to build a special team that's the old Nairy Arding transport, the checking the shear force. So, building that team takes time"
  note: 이유 동반 시간 지연 - 거부감 낮춤

- id: m11-026
  expression: "we have to ask for additional testing, but we don't have any specific conditions yet"
  category: data_gap_admission
  function: requirement_gap
  speaker_role: presenter
  difficulty: 4
  context: "we have to ask for additional testing, but we don't have any specific conditions yet"

- id: m11-027
  expression: "if you can provide some additional details on X, then we'll be able to have some additional discussion"
  category: conditional_promise
  function: data_for_discussion
  speaker_role: presenter
  difficulty: 5
  context: "if you can provide some additional details on the compressive force, then we'll be able to have some additional discussion"
  note: 데이터 요구 + 논의 조건부 - 책임 일부 이전

- id: m11-028
  expression: "perhaps Hinex should send an email with the particulars so that I can make sure we answer the right questions"
  category: action_redirect
  function: responsibility_share
  speaker_role: questioner
  difficulty: 5
  context: "perhaps Hinex should send an email with the particulars so that I can make sure we answer the right questions"
  note: "particulars" - specifics의 격식적 동의어

- id: m11-029
  expression: "Currently, we don't have. I'm not sure you are aware of that."
  category: absence_admission
  function: honest_negation
  speaker_role: presenter
  difficulty: 4
  context: "Currently, we don't have. I'm not sure you are aware of that."

- id: m11-030
  expression: "We made one prototype... but it was X, not really Y."
  category: prototype_disclaimer
  function: scope_limit
  speaker_role: presenter
  difficulty: 4
  context: "We made one prototype for this CXL pooled memory reference platform based on this switch list. It's a multi-headed system, but it was FPGA prototype, not really a silicon type"

- id: m11-031
  expression: "we are planning on having X in the future"
  category: future_promise
  function: roadmap_promise
  speaker_role: presenter
  difficulty: 3
  context: "we are planning on having the reference platform design of the CXL pooling pooled memory system in the future"

- id: m11-032
  expression: "in my personal opinion"
  category: opinion_hedging
  function: responsibility_limiting
  speaker_role: presenter
  difficulty: 3
  context: "The intermediate decision, yeah, AC, the 20 terabytes in my personal opinion"
  note: 숫자에 붙이면 공식 입장 아님을 표시

- id: m11-033
  expression: "as you mentioned, X also have a good advantage"
  category: concession
  function: polite_acknowledgment
  speaker_role: presenter
  difficulty: 4
  context: "E3, EDSFF, as you mentioned that they also have a good advantage"
  note: 상대 지적 먼저 인정 - 정중한 반박 전제

- id: m11-034
  expression: "but they have capacity limitations. So it means it's still difficult to lower TCO"
  category: reframe_to_tco
  function: pivot_to_strength
  speaker_role: presenter
  difficulty: 4
  context: "but it's 3.0 or EDSFF, they have the capacity limitations. So it means that there is still difficult to lower it to TCO"

- id: m11-035
  expression: "I will get back to you after completion of our internal analysis of X"
  category: follow_up_promise
  function: pending_promise
  speaker_role: presenter
  difficulty: 4
  context: "I will get back to you after completion of our internal analysis of the E3.L. and its accommodation"

# ── 정중한 도전 (Polite Challenge) ──
- id: m11-036
  expression: "I guess one of the questions is X"
  category: polite_probe
  function: humble_premise
  speaker_role: questioner
  difficulty: 4
  context: "I guess one of the questions is the E3 approach, those modules are typically in the front of the chassis"
  note: "I guess" - 겸손한 전제

- id: m11-037
  expression: "Is that a significant factor in your analysis?"
  category: factor_probe
  function: significance_check
  speaker_role: questioner
  difficulty: 4
  context: "Is that a significant factor in your analysis?"

- id: m11-038
  expression: "Dell supports X, but we also support Y for some of our Z"
  category: alternative_introduction
  function: option_listing
  speaker_role: questioner
  difficulty: 4
  context: "Dell supports E3S form factor, but we also support E3Long form factor for some of our storage products"

- id: m11-039
  expression: "if this was X versus Y, that changed your analysis?"
  category: hypothetical_probe
  function: comparison_reset
  speaker_role: questioner
  difficulty: 5
  context: "if this was E3Long versus add-in card, that changed your analysis?"
  note: 비교 기준 변경 질문 - 정중한 도전

- id: m11-040
  expression: "The other consideration is if X, having greater Y may not be an advantage"
  category: additional_factor
  function: counterpoint_introduction
  speaker_role: questioner
  difficulty: 5
  context: "The other consideration is if a memory module fails, having greater capacity may not be an advantage. It might be from a serviceability and RAS standpoint"

- id: m11-041
  expression: "That was the only point"
  category: challenge_softener
  function: attack_intent_denial
  speaker_role: questioner
  difficulty: 3
  context: "That was the only point"
  note: 도전 부드럽게 마무리 - 공격 의도 아님 명시

- id: m11-042
  expression: "I'm assuming that if we were going to design X, it would not be dependent on Y, right?"
  category: assumption_check
  function: hypothetical_confirm
  speaker_role: questioner
  difficulty: 4
  context: "I'm assuming that if we were going to design a dedicated chassis for cooling, it would not be dependent on what our current systems are, right?"

- id: m11-043
  expression: "I'm trying to understand"
  category: humble_preface
  function: learning_signal
  speaker_role: questioner
  difficulty: 3
  context: "I'm trying to understand"
  note: "질문 있습니다" 대신 "이해하려 합니다" - 학습으로 들림

- id: m11-044
  expression: "Will it give you a broad understanding of X for all Y, or will it be like a point answer for one Y?"
  category: dichotomy_probe
  function: scope_check
  speaker_role: questioner
  difficulty: 5
  context: "Will it give you a broad understanding of shear force for all dims, R-dims and MR-dims that we may consider? Or will it be like a point answer, you know, a very specific answer for one dim?"

- id: m11-045
  expression: "I would hope it gives us a really broad understanding of applicability"
  category: expectation_stating
  function: implicit_demand
  speaker_role: questioner
  difficulty: 4
  context: "I would hope it gives us a really broad understanding of applicability"
  note: "I would hope X" - 정중한 기대 + 암묵적 요구

- id: m11-046
  expression: "Just so we don't have to spend three months to build another test sample for a different X in the future, right?"
  category: cost_avoidance_reason
  function: efficiency_argument
  speaker_role: questioner
  difficulty: 4
  context: "Just so we don't have to spend three months to build another test sample for a different dim in the future, right?"

- id: m11-047
  expression: "I imagine we'll have a similar question as we move forward on X as well, right?"
  category: future_question_preview
  function: long_term_framing
  speaker_role: questioner
  difficulty: 4
  context: "I imagine we'll have a similar question as we move forward on DDR6 as well, right?"

- id: m11-048
  expression: "my thinking was perhaps we would be able to apply some of your knowledge to X so we don't have to do this effort"
  category: knowledge_transfer_request
  function: leverage_request
  speaker_role: questioner
  difficulty: 5
  context: "my thinking was perhaps we would be able to apply some of your knowledge to DDR6 so we don't have to do this effort"

# ── 협상·액션 (Negotiation) ──
- id: m11-049
  expression: "But that's for a different use case entirely, right?"
  category: market_split
  function: comparison_dilution
  speaker_role: questioner
  difficulty: 5
  context: "But that's for a different use case entirely, right?"
  note: "entirely" - 시장 분할로 상대 비교 희석

- id: m11-050
  expression: "if we were going to design, we would not use a current platform for that pooling. We would design something optimized for this use case"
  category: design_intent
  function: alternative_design
  speaker_role: questioner
  difficulty: 5
  context: "if we were going to design, we would not use a current platform for that pooling. We would design something optimized for this use case"
  note: "we would not use X, we would design Y" - 별도 설계 의지

- id: m11-051
  expression: "we're not constrained by X, we would look for Y"
  category: constraint_negation
  function: optimization_claim
  speaker_role: questioner
  difficulty: 4
  context: "we're not constrained by how many PCIe lanes or CXL lanes are going to the front of the box. We would look for the most optimal module form factor and solution at the chassis level"

- id: m11-052
  expression: "we're going to target for the TDF in August to be able to follow up and have this conversation again. Is that your expectation from your team?"
  category: timeline_lock
  function: bilateral_agreement
  speaker_role: questioner
  difficulty: 5
  context: "we're going to target for the TDF in August to be able to follow up and have this conversation again. Is that your expectation from the SKHINICS team?"
  note: "we're going to target for X" + "Is that your expectation?" - 쌍방 합의 확정

- id: m11-053
  expression: "August timeframe"
  category: time_anchor
  function: agreement_confirmation
  speaker_role: presenter
  difficulty: 2
  context: "Yeah. Okay. August timeframe."

- id: m11-054
  expression: "any other last minute questions or comments before we end. If not, I will close the call"
  category: meeting_close
  function: formal_termination
  speaker_role: questioner
  difficulty: 3
  context: "any other last minute questions or comments before we end. If not, I will close the call"
  note: 정중한 종료 공식

- id: m11-055
  expression: "if there are any urgent questions or concerns from your side, feel free to let us know and we'll try to answer as soon as possible"
  category: urgency_response
  function: open_channel
  speaker_role: questioner
  difficulty: 3
  context: "if there are any urgent questions or concerns from your side, feel free to let us know and we'll try to answer as soon as possible"

- id: m11-056
  expression: "we did not completely close"
  category: unfinished_acknowledgment
  function: open_item_flag
  speaker_role: questioner
  difficulty: 4
  context: "I think we might have had some thermal discussion last time that we did not completely close, but I think the most pressing topics are the shear and the compressive force"
  note: "did not completely close" - 미해결 정중 표시

- id: m11-057
  expression: "we can have the separate meeting for that"
  category: follow_up_proposal
  function: deferred_discussion
  speaker_role: presenter
  difficulty: 3
  context: "we can have the separate meeting for that"

- id: m11-058
  expression: "feel free to talk and give feedback via email or other media"
  category: async_channel
  function: open_contact
  speaker_role: presenter
  difficulty: 2
  context: "feel free to talk and give feedback via email or other media"

- id: m11-059
  expression: "the most pressing topics are X and Y"
  category: priority_stating
  function: focus_directing
  speaker_role: questioner
  difficulty: 3
  context: "the most pressing topics are the shear and the compressive force"
  note: "most pressing topics" - 우선순위 명시

- id: m11-060
  expression: "the biggest trick seems to be if we can capture the PMIC or not"
  category: technical_core
  function: bottleneck_identification
  speaker_role: questioner
  difficulty: 4
  context: "the biggest trick seems to be if we can capture the PMIC or not, our easiest solutions, we do not directly contact PMIC"
  note: "biggest trick" - 기술 핵심 과제 표현
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-05-27 10 02 42_EN_DELL_TDF-extracted.wav` (총 ~45분, 4,950단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 18-33) | Steve의 3-item agenda + roadmap 중앙 강조 | 발표开场 + 시각 강조 화법 | ★★☆ |
| 2 | 비교 프레이밍 (line 51-56) | "From the X perspective" + "Even if we consider" + "Therefore" 3단 비교 | 비교 우위 프레이밍 공식 | ★★★★ |
| 3 | Dell 도전 (line 76-95) | "E3Long vs add-in card, that changed your analysis?" + "The other consideration is" | 정중 도전 + 추가 요소 제시 | ★★★★ |
| 4 | DLC 스펙 부재 (line 220-256) | "no warranty coverage" + "Frankly speaking" + "3 months" | 정직 회피 + 시간 확보 | ★★★★ |
| 5 | 시간 확정 마무리 (line 332-340) | "target for the TDF in August" + "Is that your expectation?" | 시간 target + 쌍방 합의 | ★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 2, 3, 4가 가장 가치 높음 - 비교 프레이밍, 정중 도전, 정직 회피가 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **비교 주도 발표 + 기술 defense + DLC 이슈 논의**의 3층 register다.
- **발표자 역할 (Steve)**: 비교 프레이밍, 약점 인정, feedback 요청 - 네가 Dell에 CXL product를 pitch할 때
- **DLC 대응자 역할 (Kihoon, Sam)**: 스펙 부재 인정, 시간 확보, 이유 명시 - 네가 스펙 없는 이슈를 다룰 때
- **질문자 역할 (Dell)**: 정중 도전, 대안 제시, 시간 확정 - 네가 파트너 제품을 평가할 때

### Pragmatics (화용론) 핵심
1. **비교의 3단 공식**: "From the X perspective" + "Even if we consider Y" + "Therefore Z-wise." 영어 발표에서 비교 우위를 주장할 때, 이 3단을 외워. 한국어는 "그리고요"로 연결하지만, 영어는 "From / Even if / Therefore"로 논리 단계를 명시해야.
2. **"Honestly"의 정직함 신호**: 영어 회의에서 약점을 인정할 때 "Honestly"로 시작하면 신뢰가 간다. "Honestly, our early product couldn't fully meet Y" - 이게 정직함의 화법이다. 한국 발표문화는 약점을 숨기지만, 영어는 "Honestly"로 먼저 인정하면 더 강해진다.
3. **"Frankly speaking, it's not easy"**: 스펙이 없을 때 "We don't know"는 약하다. "Frankly speaking, it's not easy to provide any feedback related to X" - "frankly speaking"이 정직함을, "not easy"가 거부를 부드럽게 만든다. 이 조합이 정중한 거부의 공식이다.
4. **"Is that your expectation?"**: 시간을 확정할 때 상대의 동의를 명시적으로 요구. "We're going to target for August. Is that your expectation?" - 쌍방 합의를 만드는 화법. 회의록에 합의로 남길 수 있다.
5. **"That was the only point"**: 도전 후 부드럽게 마무리. 이게 공격 의도가 아님을 표시하는 화법이다. 한국어 "이것만 말씀드리고 싶었습니다"의 영어 버전.

### 네가 당장 써야 할 Top 5
1. **"From the X perspective, Y offers twice the Z"** - 비교 우위 프레이밍
2. **"Honestly, our early X couldn't fully meet Y"** - 정직한 약점 인정
3. **"Frankly speaking, it's not easy to provide any feedback related to X"** - 정중한 거부
4. **"if you can provide additional details on X, then we'll be able to have additional discussion"** - 조건부 후속
5. **"we're going to target for X in Y. Is that your expectation?"** - 쌍방 합의 확정

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "A가 B보다 낫습니다" | "From the X perspective, A offers twice the capacity of B. Even if we consider C, A remains the same. Therefore A has more advantage both D and E-wise" | 영어는 3단 논리 + 이중 근거 |
| "솔직히, 우리 초기 제품은 부족했습니다" | "Honestly, our early product couldn't fully meet AI market demands" | "Honestly" - 정직함 신호 |
| "스펙이 없습니다" | "There is no warranty coverage for X. Frankly speaking, it's not easy to provide any feedback" | "no warranty" + "Frankly speaking" - 공식적 부정 + 정직함 |
| "시간이 좀 걸립니다" | "the process is expected to take approximately two to three months, because we are trying to build a special team" | 구체적 기간 + 이유 |
| "8월에 합시다" | "we're going to target for the TDF in August. Is that your expectation from your team?" | "target for X" + "Is that your expectation?" - 쌍방 합의 |
| "다른 use case 아닙니까?" | "But that's for a different use case entirely, right?" | "entirely" - 강한 분리 |
| "이것만 말씀드리고 싶습니다" | "That was the only point" | 도전 부드럽게 마무리 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 60개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **DLC 이슈 적용**: 2절의 스펙 부재 회피 패턴은 DLC 후속 회의에서 직접 활용

---

*Textbook 11 - DELL TDF: CXL Roadmap & DLC Force Discussion (2026-05-27). 회의 유형 A (기술 Deep-dive). 표현 DB 60개. 5개 발췌 구간. 작성: 2026-09-01.*
