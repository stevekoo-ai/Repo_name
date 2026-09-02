---
textbook_id: 33
meeting: Intel (CXL 3.0 sample test coordination + debug)
date: 2025-08-21
type: D (이슈/디버그) - 재분류 (초기 A → D)
partner: Intel (Ivan, Anu, Ed, Shiyani/Sandhya, Santosh)
sk_side: SK Hynix (Jerry, Sam, Tony, Sandhya/Santosh)
duration_words: 5439
audio: repo/webex-audio/2025-08-21 08 19 45_EN_Intel-extracted.wav
transcript: repo/webex-audio/2025-08-21 08 19 45_EN_Intel-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, intel, cxl, cxl3, emr, gnr, flat-memory-mode, sample-coordination, debug, bios-limitation, white-paper]
---

# Textbook 33 - Intel CXL 3.0 Sample Coordination + Debug (2025-08-21)

> **회의 유형**: D (이슈/디버그) - 초기 할당 A(기술 deep-dive)에서 재분류. 이 회의는 단일 발표자의 제품 deep-dive가 아니다. 샘플 테스트 조율, 링크 레벨 테스트 이견, white paper 저자권 협상, flat memory mode 위반 디버그, EMR BIOS 용량 한계 진단이 혼재된 coordination + debug 회의.
> **학습 가치**: Intel 엔지니어(Ivan)의 "진단적 권위" 화법 - 부드럽지만 단호한 기술 권고, 정중한 정정, hedged 진단. SK 측(Jerry)의 정중한 요청/협상. 이 두 역할 모두 Steve가 SK Hynix 입장에서 Intel과 일할 때 직접 써야 할 화법.
> **Audrey 관점**: Type D 회의의 핵심은 "문제 진단 언어"와 "정중한 정정"이다. Ivan은 "I don't think that would be ideal"로 거부하고, "I will not recommend that"로 단호하게 막으며, "most likely there could be"로 진단을 hedging한다. 이게 네가 배워야 할 디버그 회의 화법이다.

---

## 1. 발화 아키텍처 - Ivan의 "진단적 권위" 설계 (5단계)

Type D 회의는 발표자가 없다. 대신 **진단자(diagnostician)**가 회의를 이끈다. 이 회의에서 Ivan(Intel)이 그 역할이다. 그의 발화는 5단계 구조를 따른다.

### 단계 1: 문제 재확인 (Problem Restatement)

질문을 받은 후, Ivan은 먼저 자신이 이해한 문제를 재진술하며 시간을 번다. "Am I reading something wrong?"로 자신의 이해를 점검.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `if I'm understanding right the issue is that X` | "and if I'm understanding right the issue is that you are populating CXL in socket zero and socket one you don't have CXL" | 문제 재진술 - 답변 전 이해 확인 |
| `am I reading something wrong because X` | "am I reading something wrong because you can only have up to eight channels right while you are saying that you have eight channels on numeral zero" | 자기 이해 점검 - 정정 유도 |
| `so you mean X, right?` | "so then you mean numeral one is CPU one you mean different socket" | 확인식 요약 - 상대 수정 유도 |

**Audrey 교훈**: 디버그 회의에서 질문을 받으면 즉시 답하지 마라. 먼저 "if I'm understanding right the issue is that X"로 문제를 재진술해라. 이게 (a) 내 이해가 맞는지 확인하고, (b) 잘못된 가정을 일찍 드러내며, (c) 답변 시간을 번다. 한국어 "그니까 말씀하신 게 X라는 거죠?"의 전문가 영어 버전이다.

### 단계 2: 진단 제시 (Diagnosis Delivery)

재확인 후, Ivan은 "I believe", "I don't think", "most likely"로 hedged 진단을 내린다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the conflict that you have is a X violation for Y` | "Yeah, well, the conflict that you have is a vital violation for flat memory mode" | 진단 명시 - "X violation"으로 규정 |
| `I mean like you can't` | "I mean like you can't" | 부정 - "I mean like"로 부드럽게 |
| `most likely there could be X limitation` | "Most likely there could be bias limitation that" | hedged 진단 - "most likely" + "could be" 이중 완화 |
| `I would not be surprised to find that X imposes a limitation on Y` | "I would not be surprised to find that bios imposes a limitation on CXO expansion" | 예측 hedging - "I would not be surprised"로 가능성 시사 |

**Audrey 교훈**: 진단할 때 "It is X"라는 단정은 피해라. "most likely there could be X" - "most likely"와 "could be"를 겹쳐 써라. 틀렸을 때 체면이 살고, 상대가 반박할 여지를 준다. 그리고 "I would not be surprised to find that X" - 이 표현은 "나는 X일 것 같다"인데, 훨씬 전문가 느낌이다. 한국어 "아마 X일 겁니다"보다 훨씬 권위 있다.

### 단계 3: 실험 지시 (Test Instruction)

진단 후, Ivan은 "I will suggest you to do the test"로 검증 방법을 지시한다. 이게 Type D의 핵심 - 진단만 하고 끝내지 않고, 검증 경로를 제시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I will suggest you to do the test collect the [data] and share [data] with me` | "I will suggest you to do the test collect the human and just share human with me and I can show you how to identify if you are having a page conflicts" | 검증 지시 + 데이터 공유 요청 + 후속 가이드 |
| `I would suggest like, try X. See if that works. And then Y` | "what I would suggest like, try, like, you know that your earlier device 256 works, right? We know that. So try 512. See if that works. And then seven, you know, 68, whatever that is. And then, uh, yeah. So go by that." | 단계적 실험 - "try X. See if that works. And then Y" |
| `try only one or the other` | "I would say try only one or the other" | 격리 실험 지시 |
| `go by step by step and see what the actual the issue is` | "go by step by step and see what the actual the issue is" | 방법론 제시 |

**Audrey 교훈**: 디버그 회의에서 "문제는 X입니다"만 말하면 협력자가 아니다. "I will suggest you to do the test, collect the data, and share it with me" - 검증 + 데이터 공유 + 후속을 한 문장에 담아야 한다. 이게 Intel 엔지니어의 "진단적 권위"다. 한국어 "테스트 한 번 해보시죠"의 전문가 영어 버전이다.

### 단계 4: 권고/거부 (Recommendation & Rejection)

Ivan은 "I don't think that would be ideal"로 부드러운 거부, "I will not recommend that"로 단호한 거부를 구분해 쓴다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I don't think that would be ideal` | "Yes, I don't think that would be ideal" | 부드러운 거부 - "don't think"로 의견 성격 표시 |
| `I will not recommend that, especially for X` | "No, I will not recommend that, especially for performance data publications" | 단호한 거부 + 맥락 명시 - "especially for X"로 왜 안 되는지 |
| `I think your best option from what I'm hearing is X` | "I think your best option from what I'm hearing is go with the two socket system both sockets in flat memory mode" | 최적안 제시 - "from what I'm hearing"로 정보 출처 명시 |
| `I would not waste my time on X. Try on Y.` | "So I would, I would not waste my time on EMR. Try on GNR." | 직접적 조언 - "waste my time"으로 우선순위 강제 |

**Audrey 교훈**: "안 됩니다"의 두 단계가 있다. 부드러운 거부는 "I don't think that would be ideal" - 의견 형태라 상대가 반박할 수 있다. 단호한 거부는 "I will not recommend that, especially for X" - 권고 형태이고 맥락을 붙인다. "especially for performance data publications" - 왜 안 되는지 맥락을 붙이면 반박이 어렵다. 그리고 "I would not waste my time on X" - 이 표현은 "X는 시간 낭비"라는 강한 우선순위 신호다. 네가 Intel 입장에서 SK의 잘못된 방향을 잡을 때 써라.

### 단계 5: 후속 채널 명시 (Follow-up Channel)

매 디버그 끝에 Ivan은 다음 연락 채널을 명시한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I will send our configuration and options to you. Please check your recommendation.` | "Okay, I will send our configuration and options to you. Please check your recommendation." | SK 측 후속 - 구성 전송 + 권고 요청 |
| `yeah, sure.` | (Ivan 수락) "Yeah, sure." | 간결한 수락 |
| `We will keep the discussion of this with my email.` | "Okay, we will keep the discussion of this with my email." | 채널 명시 - "keep the discussion with email" |
| `can I mean you about this issue?` | "Okay, I will check it is okay in the two separate and can I mean you about this issue?" | 후속 의사 표시 |

**Audrey 교훈**: 디버그 회의는 "회의에서 끝"이 아니다. "We will keep the discussion of this with my email" - 이메일로 계속하겠다는 후속 채널 명시가 필수다. "keep the discussion with email"이라는 표현을 외워. 한국어 "이메일로 계속하죠"의 자연스러운 영어 버전이다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

Type D 회의의 **진짜 학습 가치**. Intel 측이 약점/불확실성을 어떻게 포장하는지.

### 전략 1: 부재자에게 책임 넘기기 (Absent-Owner Deferral)

white paper 저자권 질문에서, Ivan은 자신은 "주인이 아니다"라고 하며 휴가 중인 Anu에게 최종 결정을 미룬다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| white paper 저자권 | "I don't see an issue on having your name there if you are collecting the data **but I'm not the owner. That will be a new** but yeah. You guys are collecting data is fair for your name to be there. But yeah, like you said, **let's check with a new when he gets back from occasion.**" | "데이터 수집 중이면 이름 넣는 건 문제없습니다만, **제가 owner가 아닙니다. Anu가 owner입니다.** 데이터 수집 중이시니 이름 들어가는 건 공정합니다. **Anu 휴가에서 돌아오면 확인합시다.**" |

**패턴 공식**: `I don't see an issue on X but I'm not the owner. That will be [name]. Let's check with [name] when he gets back from vacation.`

**Audrey 교훈**: 네가 결정 권한이 없을 때, 개인 의견은 주되 "I'm not the owner"로 권한을 명시해라. "I don't see an issue but I'm not the owner" - 이게 정중한 회피의 공식이다. 개인 의견으로 호의를 보이되, 결정은 진짜 owner에게 미룬다. 한국어 "제 생각에는 괜찮은데, 결정은 A 담당자가 휴가에서 돌아오면 확인해야 합니다"의 영어 버전이다. "let's check with [name] when he gets back" - 이 후속을 반드시 붙여라.

### 전략 2: "내 의견일 뿐" 면책 (Opinion Disclaimer)

Ivan은 자신의 판단이 "과거 경험 기반 개인 의견"임을 반복해 명시한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 최종 결정 권한 | "I'm just speaking from what I have seen the previous work from a new but." | "제가 말씀드리는 건 Anu의 과거 작업에서 본 것에 불과합니다" |
| 의견 성격 표시 | "I don't see an issue on having your name there if you are collecting the data but I'm not the owner" | "데이터 수집 중이면 이름 들어가는 건 문제없어 보입니다만, 제가 owner가 아닙니다" |

**패턴 공식**: `I'm just speaking from what I have seen the previous work from [name].`

**Audrey 교훈**: "I'm just speaking from what I have seen" - "제가 본 것만 말씀드리면" - 이 표현은 의견의 한계를 명시한다. 틀려도 책임이 없다. 전문가의 겸손 + 면책 화법이다. 한국어 "제가 아는 선에서는"의 영어 버전이다. 회의에서 의견을 낼 때, 특히 결정 권한이 없을 때 이 표현을 앞에 붙여라.

### 전략 3: 정중한 정정 (Polite Correction)

Intel 측이 SK의 잘못된 가정("montage 테스트 했으니 링크 테스트 안 해도 된다")을 정중하지만 단호하게 정정한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 링크 테스트 불필요 가정 정정 | "So there is some link level difference there **so it's not true that we tested montage and we don't need to test link level for on your card. We have to do that.**" | "링크 레벨 차이가 있습니다. **그러니까 montage 테스트했다고 카드 링크 테스트 안 해도 된다는 건 사실이 아닙니다. 우리가 해야 합니다.**" |
| 과거 사례 증거 | "**Even if you have seen in the past that montage chem card doesn't have any link level issue in CXL2 but your card had issues at the link level in CXL2. We have seen that.**" | "**과거에 montage chem card는 CXL2에서 링크 이슈가 없었는데, 당신 카드는 CXL2 링크 레벨에서 이슈가 있었습니다. 우리가 봤습니다.**" |
| 부드러운 이의 제기 | "We'll see I mean **you never know sometimes** I mean in the CXL2.0 phase also." | "글쎄요, **때로는 모르는 일입니다**, CXL 2.0 단계에서도 그랬으니까요" |

**패턴 공식**: `So it's not true that X. We have to do that. Even if you have seen in the past that Y. We have seen that.`

**Audrey 교훈**: 상대의 잘못된 가정을 정정할 때 "You're wrong"은 절대 쓰지 마라. "So it's not true that X. We have to do that." - "X라는 건 사실이 아닙니다. 우리가 해야 합니다." - 이게 정중한 정정의 공식이다. 그리고 "We have seen that" - "우리가 봤습니다" - 과거 사례를 증거로 제시하면 반박이 어렵다. "you never know sometimes" - "때로는 모르는 일입니다" - 이건 부드러운 이의 제기 오프닝이다. "No" 대신 써라.

### 전략 4: 이해 못함 인정 + 재확인 요청 (Comprehension Buy-time)

SK 측의 복잡한 질문을 이해하지 못했을 때, "I don't know if I got it yet"로 시간을 번다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Jerry의 질문 이해 못함 | "I don't know if I got it yet." | "아직 제가 파악을 못했습니다" |
| 제3자에게 재확인 요청 | "Do you have any visibility when Jerry is referring to?" | "Jerry가 말씀하시는 게 무엇인지 보이십니까?" (제3자에게) |
| 의미 재확인 질문 | "Jerry are you asking if the pre-qual test it's okay to run the pre-qual test and qualify with only one device?" | "Jerry, pre-qual 테스트를 단일 디바이스로만 돌려도 되느냐고 물으시는 건가요?" |

**패턴 공식**: `I don't know if I got it yet. Do you have any visibility when [name] is referring to? [name] are you asking if X?`

**Audrey 교훈**: 영어 회의에서 못 알아들었을 때 "I don't understand"는 약하다. "I don't know if I got it yet" - "아직 파앬을 못했습니다" - "yet"이 핵심이다. "지금은 모르지만 곧 알겠다"는 뉘앙스. 그리고 제3자에게 "Do you have any visibility when X is referring to?" - "X가 말하는 게 보이십니까?" - 이렇게 제3자에게 도움을 요청하면, 자존심 상하지 않게 의미를 재확인할 수 있다. 회의에서 못 알아들었을 때 이 패턴을 써라.

### 전략 5: "우리도 본 적 있다" 증거 회피 (Evidence-Based Deflection)

경쟁/우선순위 질문을 "과거 사례"로 포장해 회피한다. 그리고 "I already recommend"로 이미 권고한 사실을 강조한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| EMR vs GNR 플랫폼 선택 | "I think that the, I already recommend using the GNR." | "저는 이미 GNR 사용을 권고했습니다" |
| 인벤토리 문제 회피 | "Yeah, it's a team for, I think that it's a problem of the inventory of your platform." | "네, 팀 차원에서, 플랫폼 인벤토리 문제라고 생각합니다" |
| EMR 포기 권고 | "So I would, I would not waste my time on EMR. Try on GNR." | "EMR에 시간 낭비하지 마세요. GNR에서 해보세요" |

**패턴 공식**: `I already recommend X. It's a problem of Y. I would not waste my time on Z. Try on X.`

**Audrey 교훈**: "I already recommend X" - "이미 X를 권고했습니다" - 이 표현은 "내가 이미 말했으니, 다시 설명 안 해도 된다"는 권위 신호다. 그리고 "I would not waste my time on X" - "X에 시간 낭비 안 하겠다" - 이 표현은 상대의 방향이 틀렸음을 강하게 시사한다. 직접적이면서도 "I would"로 의견 성격을 유지한다. 디버그 회의에서 잘못된 방향을 잡을 때 이 패턴을 써라.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 Intel에 기술적으로 요청/도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다.

### 질문 유형 1: 정중한 기회 요청 (Opportunity Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We would like to have some opportunity [X] using [Y]` | "We would like to have some opportunity covalidation using the multi-prower evaluation board on the your Johnson city in your lab" | "기회를 얻고 싶다" - 정중한 요청 |
| `That's the main reason we wanted to have some opportunity` | "So that's the main reason we wanted to have some opportunity. Yeah in your lab." | "그게 주된 이유입니다" - 요청 이유 명시 |
| `We definitely will send the couple of samples to you` | "We definitely will send the couple of samples to you and couple of samples to the ad for the link and the memory media test perspective" | "definitely"로 확약 - 샘플 송부 의지 |

**Audrey 교훈**: "We want X"가 아니라 "We would like to have some opportunity X" - "X할 기회를 얻고 싶습니다" - 이게 정중한 요청 공식이다. "opportunity"가 핵심 단어다. "give us X"가 아니라 "have some opportunity"로 포장하면, 요청이 협력 제안이 된다. 그리고 "We definitely will send" - "definitely"로 샘플 송부를 확약하면, Intel도 거절하기 어렵다. 이 요청 + 확약 조합을 외워.

### 질문 유형 2: 동의 유도형 질문 (Agreement-Seeking)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So I think that the most of X will be done by using Y. Do you agree with that?` | "So I think that the most of the pre-qualification test item will be done by using the single device population on the platform. Do you agree with that?" | 의견 제시 + "Do you agree"로 동의 유도 |
| `Is that okay?` | "as can the problem only one the one CPU system with the one five foot 12 gigabytes are dim and five to seven gigabytes is it okay or not" | 짧은 동의 확인 |
| `Is that okay or not?` | "is it okay or not" | 이진 질문 - 명확한 답 요구 |

**Audrey 교훈**: 의견을 말한 후 "Do you agree with that?"로 동의를 유도해라. 한국어 "맞지요?"의 전문가 영어 버전이다. "Is that okay or not?" - "okay or not"으로 이진을 만들면, 상대가 애매하게 넘길 수 없다. 회의에서 명확한 답이 필요할 때 써라.

### 질문 유형 3: 타임라인/가용성 확인 (Timeline Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So let me ask you when is your sample will be available?` | "So let me ask you when is your sample will be available?" | 직접적 타임라인 질문 |
| `Could you please check the timeline of the [X]?` | "Could you please check the timeline of the backplane. I mean, is it available at the same time." | "Could you please check" - 정중한 확인 요청 |
| `Did you get any request about the [X] from the [team]?` | "Did you get any request about the sample from the Auto-Inter-RND team?" | 정보 확인 - "Did you get any request" |

### 질문 유형 4: 제안 + 의향 탐색 (Proposal + Intent Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I believe that we can send the, I mean, at least [N] [samples] to you guys. So what do you think about it?` | "I believe that we can send the, I mean, at least eight CMM samples to you guys. So what do you think about it?" | 제안 + "what do you think"로 의향 탐색 |
| `That should be fine` | (Intel 수락) "That should be fine." | 부드러운 수락 |
| `If you're sending us two cards to me and two to [team] we can plug in both of them` | "If you're sending us two cards to me and two to it we can plug in both of them" | 조건부 수용 - "If you're sending X, we can Y" |

**Audrey 교훈**: 숫자를 제안할 때 "I believe that we can send at least N" - "최소 N개 보낼 수 있다고 믿습니다" - "I believe"로 의견 형태, "at least"로 여지. 그리고 "So what do you think about it?"로 의향을 탐색해라. 상대가 반박하면 "at least"가 깎을 여지를 준다. 협상의 시작 화법이다.

### 질문 유형 5: 정중한 이의/재확인 (Polite Pushback / Reconfirm)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `We couldn't conclude this one` | "Just do what's the EMR max orders size, max capacity size. So we couldn't conclude this one" | "결론 못 냈습니다" - 정중한 재개 요청 |
| `we couldn't finish yet` | "Just one question. We couldn't finish yet." | "아직 못 끝냈습니다" - 의제 재개 |
| `Would you go to [slide/page]?` | "Would you go to first to, no, previous one." | 발표자 페이지 이동 요청 - 정중 |

**Audrey 교훈**: "We couldn't conclude this one" - "이건 결론을 못 냈습니다" - 미해결 의제를 재개할 때 써라. "We couldn't finish yet" - "아직 못 끝냈습니다" - 이게 정중한 재개 요청이다. 한국어 "이건 아직 안 끝났습니다"의 전문가 영어 버전이다.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

샘플 수량 협상, white paper 저자권, 후속 채널을 정하는 언어.

### 샘플 수량 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 제안 | SK | "I believe that we can send the, I mean, at least eight CMM samples to you guys. So what do you think about it?" | "at least N"으로 제안 + "what do you think" |
| 수락 | Intel | "That should be fine." | 부드러운 수락 |
| 수량 분배 | SK | "Total 10. So eight for it and two for you." | 총량 + 분배 명시 |
| 확인 | SK | "Is that okay?" / Intel: "That's ideal." | "ideal" - 최적이라는 강한 수락 |
| 사유 | SK | "Because any max configuration, most likely, I mean, it may be either the Intel volume validation team will do. It may want to do that also." | "most likely" + "either X or Y"로 사유 설명 |
| 역할 분담 | Intel | "Since I'll be doing the link testing, I don't plan to do the max configuration. So I see. It would be fine for me." | "Since I'll be doing X, I don't plan to Y" |

**Audrey 교훈**: 샘플 수량 협상은 (a) "I believe we can send at least N"으로 제안하고, (b) "So what do you think about it?"로 의향을 묻고, (c) "Total N. So N1 for team1 and N2 for team2."로 분배를 명시하고, (d) "Is that okay?"로 최종 확인한다. Intel이 "That should be fine"이나 "That's ideal"로 수락하면 끝. "ideal"은 "fine"보다 강한 수락이다 - "딱 좋다"의 뉘앙스.

### White paper 저자권 협상

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 질문 | SK | "after the collaboration is complete ... is a possibility to do add some data provided by as kind of system on this team" | "possibility to add" - 정중한 요청 |
| 권한 명시 | Intel(Ivan) | "I don't see an issue on having your name there if you are collecting the data but I'm not the owner. That will be a new" | 개인 의견 + 권한 부인 |
| 후속 | Intel(Ivan) | "let's check with a new when he gets back from occasion" | 부재자에게 미루기 |
| 사유 | Intel | "I need to have all this white paper before collaborating with other hardware vendors. Yeah, I mean, all the name of the participants are there." | "all the name of the participants are there" - 관행 근거 |
| 최종 | Intel | "we need a new to take the last call. I'm just speaking from what I have seen the previous work from a new" | "take the last call" - 최종 결정권 명시 |

**Audrey 교훈**: "take the last call" - "최종 결정하다" - 이 표현을 외워. "make the final decision"보다 회의 체에서 자연스럽다. 그리고 "I'm just speaking from what I have seen" - 의견 면책. 이 두 가지를 조합하면, "제 의견은 이렇습니다만 최종은 A 담당자가 결정합니다"가 된다.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 액션 | Intel(Ivan) | "I will suggest you to do the test collect the human and just share human with me and I will tell you if flat to a living socket one is degrading your performance" | 검증 + 데이터 공유 + 분석 약속 |
| 이메일 후속 | SK | "Okay, I will send our configuration and options to you. Please check your recommendation." | 구성 전송 + 권고 요청 |
| 채널 명시 | SK | "We will keep the discussion of this with my email." | "keep the discussion with email" |
| 후속 의사 | SK | "Okay, I will check it is okay in the two separate and can I mean you about this issue?" | 후속 의사 표시 |
| 팀 후속 | Intel | "let me follow up with the team again on this one. And if I can't get a response." | "follow up with the team" - 팀 확인 약속 |
| 권고 요청 | SK | "Please check your recommendation." | "check your recommendation" - 권고 검토 요청 |

**Audrey 교훈**: 디버그 회의의 action item은 "I will suggest you to do X, collect Y, and share Y with me, and I will tell you Z" - 이 4단 구조다. (a) 검증 지시, (b) 데이터 수집, (c) 데이터 공유, (d) 분석 약속. 이게 Intel 엔지니어의 action item 공식이다. 한국어 "테스트 하시고 결과 주시면, 분석해 드릴게요"의 영어 버전이다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/플랫폼/메모리 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **CXL 3.0** | CXL 버전 3.0 | "your CXL3.0 early November it's based on montage silicon?" - 버전 + 실리콘 출처 질문 |
| **montage silicon** | Montage(중국 팹리) 칩 | "since you are using the same PHY and the controller from montage so a lot of testing will be already done" - PHY/컨트롤러 공유 가정 |
| **PHY** | 물리 계층 | "the same PHY and the controller from montage" - PHY + controller 세트 |
| **chem card** | 특정 form factor 카드 | "montage device is a chem card right the form factor. Yours is a EDS fact right?" - form factor 비교 |
| **EDSFF** | Enterprise & Datacenter Storage Form Factor | "Yours is a EDS fact right?" - SK 카드 form factor |
| **link level test** | 링크 레벨 테스트 | "it's not true that we tested montage and we don't need to test link level for on your card. We have to do that." - 링크 테스트 필수 주장 |
| **pre-qualification test** | 사전 자격 테스트 | "the current qualification test I am required the using multiple device and multiple platform testing" - 자격 테스트 요건 |
| **volume validation** | 양산 검증 | "in order for us to move on to the volume validation phase we will have to make sure that you know it's compatible in all the memory modes" - 단계 전환 |
| **max configuration** | 최대 구성 | "you are basically referring to the max configuration right?" - 최대 구성 확인 |
| **full population** | 전체 디바이스 탑재 | "the full population. Yes. Configuration." - 최대 구성 = full population |
| **Johnson city reference platform** | Intel Johnson City 참조 플랫폼 | "getting the official Johnson city reference platform. Yeah in Q1 26 time frame" - 참조 플랫폼 타임라인 |
| **multi-power evaluation board** | 다중 전원 평가 보드 | "covalidation using the multi-prower evaluation board on the your Johnson city in your lab" - 평가 보드 |
| **flat memory mode** | 플랫 메모리 모드 (CXL 2.0 type 3) | "we cannot keep the plan mode anymore" / "both sockets in flat memory mode" - 모드 설정 |
| **page conflict** | 페이지 충돌 (메모리) | "I can show you how to identify if you are having a page conflicts between DDR and CXL" - 진단 항목 |
| **cache line conflict** | 캐시 라인 충돌 | "if your clients are having a page conflicts or cash line conflict will happen" - 성능 저하 원인 |
| **near memory** | CXL type 2 near memory (DDR) | "you will have 512 gigabytes of near memory in your socket one" - near memory 용량 |
| **far memory** | CXL type 2 far memory (CXL 디바이스) | "far memory" - 맥락상 DDR/CXL tiering |
| **EMR** (Emerald Rapids) | Intel EMR 서버 플랫폼 | "is there a particular reason you guys wanted to do this POC on EMR and not GNR?" - 플랫폼 선택 질문 |
| **GNR** (Granite Rapids) | Intel GNR 서버 플랫폼 | "I already recommend using the GNR" - GNR 권고 |
| **GNR AP** | Granite Rapids AP | "an emera rapids on or even a GNR AP or any other Intel system" - 플랫폼 비교 |
| **Clearwater Forest** | Intel 차세대 플랫폼 | "It even also works for Clearwater Forest." - 호환 플랫폼 |
| **emome / emome-tune** | Intel 메모리 튜닝 도구 | "the getting update, automated update on emome-tune, currently the way it is set up, it's not possible." - 자동 업데이트 불가 |
| **B-tune** | Intel 성능 프로파일링 툴체인 | "you can probably get B-tune" - emome 획득 경로 |
| **BIOS** | BIOS 펌웨어 | "most likely there could be bias limitation that" - BIOS 용량 한계 의심 |
| **bar / BAR** | Base Address Register | "which configuration in the bar, you FI as long" - BIOS/BAR 설정 |
| **CMM** | CXL Memory Module | "we can send the, I mean, at least eight CMM samples to you guys" - CXL 메모리 모듈 샘플 |
| **DDR** | DDR 메모리 | "the hybrid type of the six memory motor, uh, which has a combination of the DDR and the NAND device" - DDR + NAND 하이브리드 |
| **NAND** | NAND 플래시 | "combination of the DDR and the NAND device" - 하이브리드 구성 |
| **white paper** | 백서 | "who owns this white paper on my perspective" - 백서 owner |
| **POC** | Proof of Concept | "the entire CXO concept was a POC on EMR" - POC 플랫폼 |
| **MPI** | Memory Product Introduction | "9.2 MPI introduction" - 제품 양산 도입 |
| **R-dim / RDIM** | Registered DIMM | "one five foot 12 gigabytes are dim and five to seven gigabytes" - RDIM 용량 |
| **1C nm / 1B nm / 1D nm** | 1xC nm / 1xB nm / 1xD nm 공정 | "one C nanometer, 16 gigabit and one B nanometer, 24 gigabit" - 공정 노드 |
| **gigabit (Gb)** | 기가비트 (DRAM 밀도) | "16 gigabit and one B nanometer, 24 gigabit and 32 gigabit" - DRAM 밀도 |
| **sustain / go into** | (전환 동사) | "going to the sustain from 6.2 to 8.0 gigabit. And we go into 9.2 MPI." - 제품 세대 전환 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨. 접두사 `m33`.

```yaml
# ── 진단적 권위 (Diagnostic Authority) ──
- id: m33-001
  expression: "if I'm understanding right the issue is that X"
  category: problem_restatement
  function: understanding_check
  speaker_role: diagnostician
  difficulty: 4
  context: "if I'm understanding right the issue is that you are populating CXL in socket zero and socket one you don't have CXL"
  note: 디버그 회의의 첫 단계 - 답변 전 문제 재진술. 필수.

- id: m33-002
  expression: "am I reading something wrong because X"
  category: self_check
  function: self_correction_invite
  speaker_role: diagnostician
  difficulty: 4
  context: "am I reading something wrong because you can only have up to eight channels right while you are saying that you have eight channels on numeral zero"
  note: 자기 이해 점검 - 상대가 정정할 기회 줌

- id: m33-003
  expression: "so you mean X, right?"
  category: confirm_summary
  function: restate_verify
  speaker_role: diagnostician
  difficulty: 3
  context: "so then you mean numeral one is CPU one you mean different socket"

- id: m33-004
  expression: "the conflict that you have is a X violation for Y"
  category: diagnosis_state
  function: diagnosis_delivery
  speaker_role: diagnostician
  difficulty: 5
  context: "Yeah, well, the conflict that you have is a vital violation for flat memory mode"
  note: 진단 명시 - "X violation for Y"로 규정. 강한 진단.

- id: m33-005
  expression: "most likely there could be X limitation"
  category: hedged_diagnosis
  function: tentative_diagnosis
  speaker_role: diagnostician
  difficulty: 4
  context: "Most likely there could be bias limitation that"
  note: "most likely" + "could be" 이중 hedging. 틀려도 체면 살음.

- id: m33-006
  expression: "I would not be surprised to find that X imposes a limitation on Y"
  category: hedged_prediction
  function: possibility_signal
  speaker_role: diagnostician
  difficulty: 5
  context: "I would not be surprised to find that bios imposes a limitation on CXO expansion"
  note: "I would not be surprised" - 가능성 시사하는 전문가 표현

- id: m33-007
  expression: "I will suggest you to do the test collect the [data] and share [data] with me"
  category: test_instruction
  function: verify_instruct
  speaker_role: diagnostician
  difficulty: 5
  context: "I will suggest you to do the test collect the human and just share human with me and I can show you how to identify if you are having a page conflicts"
  note: 검증 + 데이터 공유 + 후속 가이드. Type D 핵심 action item.

- id: m33-008
  expression: "I would suggest like, try X. See if that works. And then Y"
  category: stepwise_test
  function: incremental_experiment
  speaker_role: diagnostician
  difficulty: 4
  context: "try, like, you know that your earlier device 256 works, right? We know that. So try 512. See if that works. And then seven, you know, 68, whatever that is"
  note: 단계적 실험 - "try X. See if that works. And then Y"

- id: m33-009
  expression: "try only one or the other"
  category: isolation_test
  function: isolation_instruct
  speaker_role: diagnostician
  difficulty: 3
  context: "I would say try only one or the other"

- id: m33-010
  expression: "go by step by step and see what the actual the issue is"
  category: methodology
  function: diagnostic_method
  speaker_role: diagnostician
  difficulty: 3
  context: "go by step by step and see what the actual the issue is"

- id: m33-011
  expression: "I don't think that would be ideal"
  category: soft_rejection
  function: opinion_reject
  speaker_role: diagnostician
  difficulty: 4
  context: "Yes, I don't think that would be ideal"
  note: 부드러운 거부 - "don't think"로 의견 성격 표시

- id: m33-012
  expression: "I will not recommend that, especially for X"
  category: firm_rejection
  function: firm_advise_against
  speaker_role: diagnostician
  difficulty: 5
  context: "No, I will not recommend that, especially for performance data publications"
  note: 단호한 거부 + "especially for X"로 맥락. 반박 어렵게.

- id: m33-013
  expression: "I think your best option from what I'm hearing is X"
  category: best_option
  function: optimal_recommendation
  speaker_role: diagnostician
  difficulty: 4
  context: "I think your best option from what I'm hearing is go with the two socket system both sockets in flat memory mode"
  note: "from what I'm hearing" - 정보 출처 명시

- id: m33-014
  expression: "I would not waste my time on X. Try on Y."
  category: priority_advice
  function: direct_priority
  speaker_role: diagnostician
  difficulty: 5
  context: "So I would, I would not waste my time on EMR. Try on GNR."
  note: "waste my time" - 강한 우선순위 신호. 직접적 조언.

- id: m33-015
  expression: "I believe you should be okay because X"
  category: reassurance
  function: reassure_with_reason
  speaker_role: diagnostician
  difficulty: 4
  context: "I believe you should be okay because the clients on me here. As far as I know and remember do not use a large memory footprint"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m33-016
  expression: "I don't see an issue on X but I'm not the owner. That will be [name]"
  category: absent_owner_deferral
  function: defer_to_absent_owner
  speaker_role: participant
  difficulty: 5
  context: "I don't see an issue on having your name there if you are collecting the data but I'm not the owner. That will be a new"
  note: 정중한 회피 공식 - 개인 의견 + 권한 부인 + 부재자 지정

- id: m33-017
  expression: "let's check with [name] when he gets back from vacation"
  category: follow_up_defer
  function: defer_until_return
  speaker_role: participant
  difficulty: 4
  context: "let's check with a new when he gets back from occasion"

- id: m33-018
  expression: "we need [name] to take the last call"
  category: final_authority
  function: final_decision_owner
  speaker_role: participant
  difficulty: 4
  context: "we need a new to take the last call"
  note: "take the last call" - 최종 결정권. "make the final decision"보다 회의 체 자연스러움.

- id: m33-019
  expression: "I'm just speaking from what I have seen the previous work from [name]"
  category: opinion_disclaimer
  function: opinion_hedge
  speaker_role: participant
  difficulty: 5
  context: "I'm just speaking from what I have seen the previous work from a new but"
  note: 의견 면책 - "제가 본 것만 말씀드리면". 틀려도 책임 없음.

- id: m33-020
  expression: "So it's not true that X. We have to do that."
  category: polite_correction
  function: firm_correction
  speaker_role: partner_side
  difficulty: 5
  context: "so it's not true that we tested montage and we don't need to test link level for on your card. We have to do that."
  note: 정중한 정정 공식 - "You're wrong" 대신 "it's not true that X"

- id: m33-021
  expression: "We have seen that"
  category: evidence_statement
  function: evidence_cite
  speaker_role: partner_side
  difficulty: 3
  context: "Even if you have seen in the past that montage chem card doesn't have any link level issue in CXL2 but your card had issues at the link level in CXL2. We have seen that."
  note: 과거 사례 증거 - 반박 어려움

- id: m33-022
  expression: "you never know sometimes"
  category: soft_objection
  function: soft_pushback_open
  speaker_role: partner_side
  difficulty: 4
  context: "We'll see I mean you never know sometimes I mean in the CXL2.0 phase also"
  note: 부드러운 이의 제기 오프닝 - "No" 대신

- id: m33-023
  expression: "I don't know if I got it yet"
  category: comprehension_buy_time
  function: admit_incomplete_understanding
  speaker_role: participant
  difficulty: 4
  context: "I don't know if I got it yet"
  note: "I don't understand" 대신 - "yet"이 핵심. 시간 벌기.

- id: m33-024
  expression: "Do you have any visibility when [name] is referring to?"
  category: third_party_check
  function: redirect_for_clarify
  speaker_role: participant
  difficulty: 5
  context: "Do you have any visibility when Jerry is referring to?"
  note: 제3자에게 의미 재확인 요청 - 자존심 상하지 않게

- id: m33-025
  expression: "[name] are you asking if X?"
  category: meaning_restate
  function: paraphrase_check
  speaker_role: participant
  difficulty: 4
  context: "Jerry are you asking if the pre-qual test it's okay to run the pre-qual test and qualify with only one device?"

- id: m33-026
  expression: "I already recommend using X"
  category: prior_recommendation
  function: authority_signal
  speaker_role: diagnostician
  difficulty: 3
  context: "I think that the, I already recommend using the GNR"
  note: "이미 권고했습니다" - 재설명 안 해도 된다는 권위 신호

- id: m33-027
  expression: "it's a problem of X"
  category: issue_attribute
  function: cause_attribute
  speaker_role: participant
  difficulty: 3
  context: "I think that it's a problem of the inventory of your platform"

# ── 정중한 도전 (Polite Challenge / Request) ──
- id: m33-028
  expression: "We would like to have some opportunity [X] using [Y]"
  category: opportunity_request
  function: polite_request
  speaker_role: questioner
  difficulty: 5
  context: "We would like to have some opportunity covalidation using the multi-prower evaluation board on the your Johnson city in your lab"
  note: "give us X" 대신 "have some opportunity X" - 정중한 요청 공식

- id: m33-029
  expression: "That's the main reason we wanted to have some opportunity"
  category: reason_state
  function: request_justify
  speaker_role: questioner
  difficulty: 3
  context: "So that's the main reason we wanted to have some opportunity. Yeah in your lab"

- id: m33-030
  expression: "We definitely will send the couple of samples to you"
  category: commitment_strong
  function: sample_commit
  speaker_role: questioner
  difficulty: 3
  context: "We definitely will send the couple of samples to you and couple of samples to the ad"
  note: "definitely"로 샘플 송부 확약 - 거절 어렵게

- id: m33-031
  expression: "So I think that the most of X will be done by using Y. Do you agree with that?"
  category: agreement_seek
  function: opinion_then_seek_agree
  speaker_role: questioner
  difficulty: 4
  context: "So I think that the most of the pre-qualification test item will be done by using the single device population on the platform. Do you agree with that?"

- id: m33-032
  expression: "Is that okay or not?"
  category: binary_check
  function: force_clear_answer
  speaker_role: questioner
  difficulty: 2
  context: "is it okay or not"
  note: "okay or not" 이진 - 애매한 답 차단

- id: m33-033
  expression: "So let me ask you when is your X will be available?"
  category: timeline_probe
  function: direct_timeline
  speaker_role: questioner
  difficulty: 3
  context: "So let me ask you when is your sample will be available?"

- id: m33-034
  expression: "Could you please check the timeline of the [X]?"
  category: timeline_check_polite
  function: polite_timeline
  speaker_role: questioner
  difficulty: 3
  context: "Could you please check the timeline of the backplane. I mean, is it available at the same time"

- id: m33-035
  expression: "Did you get any request about the [X] from the [team]?"
  category: info_probe
  function: info_check
  speaker_role: questioner
  difficulty: 3
  context: "Did you get any request about the sample from the Auto-Inter-RND team?"

- id: m33-036
  expression: "I believe that we can send the, I mean, at least [N] [samples] to you guys. So what do you think about it?"
  category: proposal_seek
  function: propose_number
  speaker_role: negotiator
  difficulty: 5
  context: "I believe that we can send the, I mean, at least eight CMM samples to you guys. So what do you think about it?"
  note: "I believe" + "at least" + "what do you think" - 협상 3단계

- id: m33-037
  expression: "That should be fine"
  category: soft_accept
  function: gentle_accept
  speaker_role: negotiator
  difficulty: 2
  context: "That should be fine"

- id: m33-038
  expression: "That's ideal"
  category: strong_accept
  function: ideal_accept
  speaker_role: negotiator
  difficulty: 2
  context: "That's ideal"
  note: "fine"보다 강한 수락 - "딱 좋다"

- id: m33-039
  expression: "Total [N]. So [N1] for [team1] and [N2] for [team2]."
  category: allocation_state
  function: split_state
  speaker_role: negotiator
  difficulty: 3
  context: "Total 10. So eight for it and two for you"

- id: m33-040
  expression: "Since I'll be doing the [X], I don't plan to do the [Y]"
  category: role_scope
  function: role_declare
  speaker_role: participant
  difficulty: 4
  context: "Since I'll be doing the link testing, I don't plan to do the max configuration"

- id: m33-041
  expression: "We couldn't conclude this one"
  category: reopen_topic
  function: polite_reopen
  speaker_role: questioner
  difficulty: 4
  context: "Just do what's the EMR max orders size, max capacity size. So we couldn't conclude this one"
  note: 미해결 의제 재개 - "결론 못 냈습니다"

- id: m33-042
  expression: "We couldn't finish yet"
  category: reopen_topic
  function: reopen_short
  speaker_role: questioner
  difficulty: 2
  context: "Just one question. We couldn't finish yet."

- id: m33-043
  expression: "Would you go to [slide/page]?"
  category: presenter_request
  function: polite_navigate
  speaker_role: questioner
  difficulty: 2
  context: "Would you go to first to, no, previous one"

# ── 협상·액션 (Negotiation & Action) ──
- id: m33-044
  expression: "I will send our configuration and options to you. Please check your recommendation."
  category: follow_up_action
  function: send_and_request
  speaker_role: questioner
  difficulty: 4
  context: "Okay, I will send our configuration and options to you. Please check your recommendation"

- id: m33-045
  expression: "We will keep the discussion of this with my email"
  category: channel_state
  function: channel_continue
  speaker_role: questioner
  difficulty: 3
  context: "Okay, we will keep the discussion of this with my email"
  note: "이메일로 계속하죠" - 후속 채널 명시

- id: m33-046
  expression: "let me follow up with the team again on this one"
  category: team_follow_up
  function: team_check
  speaker_role: participant
  difficulty: 3
  context: "let me follow up with the team again on this one. And if I can't get a response"

- id: m33-047
  expression: "as long as you are on the [platform], use this version that you have"
  category: version_guidance
  function: version_lock
  speaker_role: diagnostician
  difficulty: 3
  context: "as long as you are on the GNR, use this version that you have"

- id: m33-048
  expression: "when you move to future generations or future platforms, you most likely will need a new [tool]"
  category: future_version
  function: future_need_predict
  speaker_role: diagnostician
  difficulty: 4
  context: "When you move to future generations or future platforms, you most likely will need a new emome, but you can get that from any moment you need it"

- id: m33-049
  expression: "theoretically should not be a limitation, but [X] may impose some limitation"
  category: theory_vs_practice
  function: theory_practice_gap
  speaker_role: diagnostician
  difficulty: 5
  context: "theoretically should not be a limitation, but bias may impose some limitation"
  note: "이론상 한계 없지만, X가 한계 부과할 수 있다" - 이론 vs 실제 hedging

- id: m33-050
  expression: "do you have anything else or are we done?"
  category: meeting_close
  function: close_check
  speaker_role: participant
  difficulty: 2
  context: "Sandong, do you have anything else or are we done?"

- id: m33-051
  expression: "Just one question"
  category: question_opening
  function: turn_taking
  speaker_role: questioner
  difficulty: 1
  context: "Just one question. We couldn't finish yet"

- id: m33-052
  expression: "I will present a [X] roadmap"
  category: roadmap_intro
  function: presentation_open
  speaker_role: presenter
  difficulty: 2
  context: "I will present a sub-ADIRAM roadmap"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2025-08-21 08 19 45_EN_Intel-extracted.wav` (총 ~50분, 5,439단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 16-39) | 링크 레벨 테스트 이견 - Intel이 "montage 테스트했으니 안 해도 된다"는 SK 가정을 정중히 정정 | 정중한 정정 화법("it's not true that X. We have to do that.") | ★★★★ |
| 2 | 샘플 요청 (line 46-65) | Jerry의 정중한 covalidation 요청 + "definitely will send" 확약 | 정중한 기회 요청 화법("We would like to have some opportunity X") | ★★★ |
| 3 | white paper 협상 (line 115-160) | 저자권 협상 - Ivan의 "I'm not the owner" 회피 + Anu에게 미루기 | 부재자 회피 화법("let's check with X when he gets back") | ★★★★ |
| 4 | flat memory mode 디버그 (line 194-286) | Ivan의 진단적 권위 - "violation" 규정, "I will not recommend", "best option" 권고 | 진단 + 권고 + 거부 화법 종합 | ★★★★ |
| 5 | EMR BIOS 한계 진단 (line 421-481) | EMR 용량 한계 진단 - "most likely could be", "I would not be surprised", "try X. See if that works" | hedged 진단 + 단계적 실험 지시 | ★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 각 단계에 발췌를 넣어 사용
- 발췌 1, 4, 5가 가장 가치 높음 - 정중한 정정/진단/디버그 화법이 밀집
- 발췌 4는 Ivan의 "진단적 권위" 5단계가 모두 등장 - 필수

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **coordination + debug** register다. 발표자가 없고, 진단자(Ivan)가 회의를 이끈다. 두 역할 모두 학습해야:
- **진단자 역할 (Ivan, Intel)**: 문제 재진술, hedged 진단, 실험 지시, 단호한 권고/거부, 후속 채널 - 네가 Intel처럼 기술 권고할 때
- **요청자 역할 (Jerry/SK)**: 정중한 기회 요청, 동의 유도, 샘플 분배 협상, 미해결 의제 재개 - 네가 Intel에 요청할 때

### Pragmatics (화용론) 핵심
1. **"it's not true that X" 정정**: 상대의 잘못된 가정을 정정할 때 "You're wrong" 대신 "it's not true that X"를 써라. "X라는 건 사실이 아닙니다" - 주어를 "you"에서 "사실"로 빼서 비난감을 줄인다. 그리고 "We have to do that"로 결론을 붙여, 정정이 의견이 아니라 사실임을 강조한다.
2. **"most likely could be" 이중 hedging**: 진단할 때 "most likely"와 "could be"를 겹쳐 써라. "most likely there could be X limitation" - 틀렸을 때 체면이 살고, 상대가 반박할 여지를 준다. "It is X"라는 단정은 절대 쓰지 마라.
3. **"I'm not the owner" 회피**: 결정 권한이 없을 때, 개인 의견은 주되 "I'm not the owner. That will be [name]."로 권한을 명시해라. "let's check with [name] when he gets back"으로 후속을 붙이면, 정중한 회피가 완성된다.
4. **"I will not recommend that, especially for X"**: 단호한 거부는 "especially for X"로 맥락을 붙여라. 왜 안 되는지 맥락을 붙이면 반박이 어렵다. "performance data publications"이라는 맥락이 붙으면, 성능 데이터 신뢰성 문제라서 더 반박하기 어렵다.
5. **"We would like to have some opportunity X"**: "give us X"가 아니라 "have some opportunity X"로 포장하면, 요청이 협력 제안이 된다. "opportunity"가 핵심 단어다. 네가 Intel에 뭘 요청할 때 이 표현을 써라.

### 네가 당장 써야 할 Top 5
1. **"if I'm understanding right the issue is that X"** - 디버그 답변 전 문제 재진술. 필수.
2. **"So it's not true that X. We have to do that."** - 정중한 정정 공식.
3. **"I will not recommend that, especially for X"** - 단호한 거부 + 맥락.
4. **"I don't see an issue on X but I'm not the owner. That will be [name]"** - 부재자에게 책임 넘기기.
5. **"We would like to have some opportunity X using Y"** - 정중한 요청/협력 제안.

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "그니까 말씀하신 게 X라는 거죠?" | "if I'm understanding right the issue is that X" | "am I reading something wrong"으로 자기 점검 옵션 |
| "아닙니다, 틀렸습니다" | "So it's not true that X. We have to do that." | "you're wrong" 대신 "it's not true"로 주어 이동 |
| "아마 X일 겁니다" | "most likely there could be X limitation" | "most likely" + "could be" 이중 hedging |
| "제가 결정 권한 없습니다" | "I don't see an issue on X but I'm not the owner. That will be [name]" | 개인 의견 주고 권한 명시, 부재자 지정 |
| "이건 안 됩니다" | "I will not recommend that, especially for X" | "especially for X"로 맥락 붙여 반박 차단 |
| "X에 시간 낭비하지 마세요" | "I would not waste my time on X. Try on Y." | "I would"로 의견 성격 유지 |
| "저희가 X하고 싶습니다" | "We would like to have some opportunity X" | "give us" 대신 "have some opportunity" |
| "확인해 보겠습니다" | "let me follow up with the team again on this one" | "check" 대신 "follow up with the team" |
| "이메일로 계속하죠" | "We will keep the discussion of this with my email" | "keep the discussion with email" |
| "결국 A가 결정합니다" | "we need [name] to take the last call" | "take the last call" - 회의 체 자연스러운 표현 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법("I'm not the owner" 회피) + 3절 정중한 정정 화법("it's not true that X")을 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **역할 연습**: Ivan(진단자) 역할과 Jerry(요청자) 역할을 번갈아 연습 - 두 입장 모두 경험해야 SK-Intel 회의 대응 가능

---

*Textbook 33 - Intel CXL 3.0 Sample Coordination + Debug (2025-08-21). 회의 유형 D (이슈/디버그) - 초기 A에서 재분류. 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01.*
