---
textbook_id: 28
meeting: Intel (January sync)
date: 2026-01-22
type: D (이슈/품질 디버깅)
partner: Intel (Jenny, Anil, Lutford, Ed, Ivan, Tony)
sk_side: Sundan (SK hynix), plus Don (Intel facilitator)
duration_words: 3116
audio: repo/webex-audio/2026-01-22 09 02 13_EN_Intel-extracted.wav
transcript: repo/webex-audio/2026-01-22 09 02 13_EN_Intel-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, intel, cxl, dmr, flat-memory-mode, miss-rate, link-training, mld, debug, issue-tracking]
---

# Textbook 28 - Intel January sync (2026-01-22)

> **회의 유형**: D (이슈/품질 디버깅) - 정기 sync 미팅에서 20% 성능 저하 디버깇 status 공유, miss rate 진단 tip, link training regression 결과, CXL switch/MLD/GPU 협업 등 다수 이슈를 처리
> **학습 가치**: 이슈 보고 회피 화법, "tip"으로 위험을 돌리는 화법, "I'll try"로 책임 한정, 질문자의 정중한 디버깇 status 확인
> **Audrey 관점**: 이 회의는 "디버깇 동기화"의 전형 - SK가 이슈를 보고하고, Intel이 tip/status/next-step으로 응답. 발표자 없이 다자간 issue review 구조. 네가 SK 입장에서 이슈를 올리고 Intel 답변을 받을 때, 그리고 반대로 네가 책임자일 때 모두 배워야

---

## 1. 발화 아키텍처 - issue review 미팅의 4단계 구조

이 미팅은 단일 발표자가 아니라 **facilitator (Jenny/Don) + 다수 이슈 보고자** 구조. 각 발화자는 고정된 화법 패턴으로 자기 역할을 수행한다.

### 단계 1: Facilitator의 이슈 프레이밍 (Issue Framing by Facilitator)

Jenny/Don은 이슈를 먼저 요약하고 질문을 열어, 보고자가 바로 본론으로 들어가게 한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So again, I saw an email about how they fix the issue, right?` | "So again, I saw an email about how they fix the issue, right?" | 이슈 회상 - "I saw an email"로 공유 맥락 설정 |
| `So in the end, have we finished the measurement and... did I read that correctly?` | "So in the end, have we finished the measurement and I think now they are the Hynex system is running properly... did I read that correctly?" | 확인형 질문 - "did I read that correctly?"로 이슈 상태 검증 |
| `I just wanted to, that was my question for the meeting.` | "I just wanted to, that was my question for the meeting." | 질문 목적 명시 - "my question for the meeting" |

**Audrey 교훈**: 정기 sync 미팅에서 facilitator는 "I saw an email about X, right?"로 시작한다. "right?"가 청중 동의를 끌어내고, "did I read that correctly?"가 자기 이해를 검증. 이게 이슈 review의 여는 화법이다. 단독 질문일 때는 "that was my question for the meeting"으로 목적을 명시하며 마무리.

### 단계 2: 이슈 보고자의 status 보고 (Status Report by Issue Owner)

Sundan (SK)은 상태를 "we are looking for the reason why..."로 보고하고, Lutford (Intel)은 regression 결과를 "we did N loops, no red flag"로 보고한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So we are looking for the reason why there is X` | "So we are looking for the reason why there is just some performance drop" | 원인 탐색 보고 - "looking for the reason why" |
| `So we would like to touch this one in next meeting` | "So we would like to touch this one in next meeting" | 미루기 - "touch this one in next meeting" |
| `We are still debugging it, but.` | "Yes. We are still debugging it, but." | 진행 중 상태 - "still debugging it, but" |
| `we did 10,000 loops of all the X tests, no red flag or no major issues as of today` | "we did 10,000 loops of all the link training tests, no red flag or no major issues as of today" | regression 결과 보고 - "no red flag... as of today" |

**Audrey 교훈**: 이슈 status 보고는 "we are still debugging it, but"으로 시작한다. "but" 뒤에 있는 게 핵심 - 부정을 먼저 인정하고 진행 상황을 연결. regression 보고는 "no red flag or no major issues as of today" - "as of today"가 중요. "오늘 현재 문제 없다"는 한정. 내일 다를 수 있다는 면책이 내장.

### 단계 3: 전문가의 "tip" 제공 (Expert Tip Delivery)

Anil은 SK의 디버깅 방향이 잘못된 경우, 직접 지적 대신 "tip"으로 전환. 이게 이 회의의 화용론적 하이라이트.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `But yeah, I'll give you some tip.` | "But yeah, I'll give you some tip." | tip 선언 - 권위적 지적 대신 "tip"으로 완화 |
| `So depending on how X is behaving, that's why we say something called Y` | "depending on how the database is behaving, and that's why we say something called a miss rate" | 개념 도입 - "that's why we say something called X" |
| `So don't debug too much. So you have to figure out what X is` | "So don't debug too much. So you have to figure out what the miss rate is in general" | 방향 전환 - "don't debug too much" + "you have to figure out X" |
| `So that's my tip. That's all.` | "So that's my tip. That's all." | tip 종료 - "That's all"로 명시적 마침 |

**Audrey 교훈**: "I'll give you some tip"은 강한 지적을 부드럽게 포장. "don't debug too much"는 직접 지적이지만 tip이라는 틀 안에 있어서 도전적이지 않다. "That's all"로 tip을 닫고 발언권을 넘긴다. 이게 전문가가 비전문가의 방향을 수정할 때 쓰는 정중한 화법이다. 한국어로는 "팁 하나 드리자면"의 영어 버전이지만, 권위 차이가 더 분명하다.

### 단계 4: 질문자의 정중한 다음 이슈 전환 (Polite Topic Shift)

Sundan은 새 이슈를 "I'd like to know..." / "we are wondering..."로 정중하게 열고, Intel 측이 "I can follow up with that"으로 응답.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `And I'd like to know the X about that` | "And I'd like to know the man pulling switch about that" | 다음 이슈 개시 - "I'd like to know X about that" |
| `So, we are wondering the X` | "uh, we are wondering the five 12 gigabyte POS is a almost to limited power" | 우려 표현 - "we are wondering" + 문제 진술 |
| `Do you have any information on this one?` | "Do you have any information on this one?" | 직접 질문 - "any information on this one" |
| `So, what exactly is your question?` | "So, what exactly is your question?" | 질문 명확화 요청 - "exactly"로 정밀 요구 |
| `Are you asking whether we will support X with Y?` | "Are you asking whether we will support native flat to a limb with 256 GB?" | 질문 재진술 - "Are you asking whether"로 확인 |

**Audrey 교훈**: 이슈를 넘길 때 "I'd like to know X about that"를 쓴다. "about that"이 앞 맥락을 받아서 자연스럽게 연결. Intel 측은 "what exactly is your question?"으로 질문을 좁힌다 - 이게 회의 시간 절약의 핵심. 모호한 질문을 "Are you asking whether X?"로 재진술하면 답변이 정확해진다. 네가 답할 때도 이 패턴을 써라.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. 이슈/디버깅 미팅에서 약점(책임 불명, 미지원, 정보 부족)을 어떻게 정중하게 포장하는지.

### 전략 1: "as of today"로 면책 (Time-Bounded Disclaimer)

회귀 테스트 결과를 "오늘 현재"로 한정. 내일 다를 수 있다는 면책을 내장.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 10,000 loops regression 결과 | "we did 10,000 loops of all the link training tests, no red flag or no major issues as of today" | "링크 트레이닝 테스트 1만 루프 돌렸고, 오늘 현재 레드 플래그나 주요 이슈 없습니다" |

**패턴 공식**: `we did N loops of all the X tests, no red flag or no major issues as of today`

**Audrey 교훈**: "no issues"만 하면 절대 안 된다. "as of today"를 붙여. 이게 regression 보고의 면책 공식이다. "오늘 현재 문제 없다"는 것은 "내일 문제 생길 수 있다"는 전제가 내장. 회의에서 regression 결과 보고할 때 반드시 "as of today" 또는 "as of now"를 붙여.

### 전략 2: "I'll try"로 책임 한정 (Soft Commitment)

GPU 팀 협업처럼 자기가 결정할 수 없는 건 "I'll try"로 약화.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| GPU 팀 답변 대신 전달 | "I'll try and get you some answers. But yeah, right, right now, my understanding is not having conversations, you know, with our GPU team and CXL at this time." | "답변을 구해보겠습니다. 다만 지금은 GPU 팀과 CXL 관련 대화가 없는 걸로 알고 있습니다" |
| 추가 정보 시도 | "I'll try, um, and see if I can get you more than, you know, the answer I've been given, which was right now." | "제가 받은 답변 이상을 드릴 수 있는지 시도해 보겠습니다" |
| 호환성 답변 시도 | "I'll see about, you know, trying to get you some answers here." | "답변을 구해보겠습니다" |

**패턴 공식**: `I'll try and get you some answers. But right now, my understanding is X.`

**Audrey 교훈**: "I'll do it"는 약속, "I'll try"는 시도. 자기가 통제할 수 없는 다른 팀(GPU 팀) 답변을 대신 전달할 때 "I'll try"를 써. "I'll get you the answer"는 책임이 100%지만 "I'll try and get you the answer"는 책임이 완화. 그리고 "my understanding is X"로 현재 상태를 자기 이해로 한정 - "확실한 건 아니고 제가 아는 한"이라는 면책.

### 전략 3: "I don't recall"로 메모리 한정 (Memory Disclaimer)

이전에 본 자료를 못 찾았을 때 "I don't recall"로 기억의 한계를 인정.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 이전 deck에 있었는지 | "I don't recall this slide being in the last deck, but, um" | "지난 deck에 이 슬라이드가 있었는지 기억나지 않습니다만" |
| 질문 회상 | "I don't recall seeing this slide in the last deck. So you laid out some specific questions. I'm happy to take those and try and get you some answers." | "지난 deck에 본 기억이 없습니다. 구체 질문을 주시면 답변을 구해보겠습니다" |
| 인정 + 사과 | "Yeah, my apologies. I missed that. It's okay. I'll try." | "죄송합니다. 놓쳤습니다. 시도해 보겠습니다" |

**패턴 공식**: `I don't recall X. So I'm happy to take those and try and get you some answers. My apologies, I missed that.`

**Audrey 교훈**: "I don't remember"는 약하고 부정적. "I don't recall"은 더 전문적 - "기억나지 않는다"는 정중한 표현. 그리고 "I don't recall" 다음에는 무조건 "I'm happy to take those and try"로 긍정 후속을 붙여. "모르겠다"로 끝내면 안 되고, "모르겠지만 받아서 해보겠다"로 전환. 그리고 지적당하면 "my apologies, I missed that"로 깨끗하게 인정.

### 전략 4: 타 팀 책임 전환 (Team Boundary Deflection)

GPU 팀이 안 열려 있는 상황을 "GPU team keeps things close to their chest"로 타 팀 성향 탓으로 돌린다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| GPU 팀 비협조 | "the GPU team keeps things very close within their organization" | "GPU 팀은 자기 조직 내에서만 정보를 가둡니다" |
| 비관적 답변 선언 | "I'm almost absolutely certain on is there is no lending of any GPUs" | "GPU 대여는 없다는 건 거의 확실합니다" |

**패턴 공식**: `The X team keeps things very close within their organization. So right now, my understanding is not having conversations with Y.`

**Audrey 교훈**: "keeps things close to their chest"는 영어 관용구 - "자기 가슴에 꼭 끌어안고 있다" = "정보를 안 공유". 타 팀 비협조를 이 관용구로 설명하면, 자기 책임이 아니라 "저쪽 성향"으로 프레이밍. "I'm almost absolutely certain on is there is no X" - "almost absolutely certain"이라는 모순적 표현이 "거의 확실"을 더 강조. 단정을 피하면서 확신 전달.

### 전략 5: "tip"으로 비판 완화 (Tip-as-Criticism)

"don't debug too much"는 강한 비판이지만 "tip"이라는 틀 안에서 부드럽게 전달.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 디버깅 방향 정정 | "But yeah, I'll give you some tip. So depending on the database... If the miss rate is high, then flat memory mode doesn't work. So don't debug too much. So you have to figure out what the miss rate is in general." | "팁 하나 드리겠습니다. 데이터베이스에 따라... miss rate가 높으면 flat memory mode가 안 통합니다. 너무 debug하지 마세요. miss rate가 얼마인지 알아야 합니다" |

**패턴 공식**: `I'll give you some tip. So depending on X... So don't Y too much. So you have to figure out Z.`

**Audrey 교훈**: "don't debug too much"는 단독으로 쓰면 도전적. 하지만 "I'll give you some tip"이라는 틀 안에 있으면 조언이 된다. 네가 상대방의 방향을 정정할 때, "Let me give you a tip"으로 먼저 틀을 열어. 그 다음 "don't X too much" + "you have to figure out Y"로 방향 제시. 한국어로는 "제가 팁 하나 드리자면"의 영어 버전인데, 영어가 더 권위 차이를 허용한다.

### 전략 6: "looking for some additional information"로 진행 상태 보고 (In-Progress Status)

이메일로 답을 받고 있는 상황을 "looking for additional information"로 활동 중 상태로 보고.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| Intel 내부 검토 중 | "We've identified the right folks inside of Intel. We've sent them your information as well as the follow up that you just sent. And, um, they're reviewing that. And, um, So hopefully, um, either an email update or, uh, you, some type of communication when I know more from that." | "Intel 내부 적임자를 찾았습니다. 정보를 보냈고 검토 중입니다. 제가 더 알게 되면 이메일이나 소통으로 알려드리겠습니다" |

**패턴 공식**: `We've identified the right folks inside of X. We've sent them Y. They're reviewing that. So hopefully, either an email update or some type of communication when I know more.`

**Audrey 교훈**: 진행 중일 때 "we've identified the right folks"가 진척의 증거. "they're reviewing that"으로 상태를 받고, "when I know more"로 다음 통신 시점을 한정. "hopefully"로 긍정적 결과를 시사하되 약속하지는 않는다. 이게 진행 보고의 정중한 회피.

---

## 3. 정중한 도전 화법 (SK 측 질문자)

SK 측이 Intel의 status를 확인하고 다음 단계를 밀어붙이는 패턴. **네가 직접 써야 할 화법**.

### 질문 유형 1: 이메일 회상형 이슈 확인 (Email-Recall Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So again, I saw an email about how they fix the issue, right?` | "So again, I saw an email about how they fix the issue, right?" | "이메일 봤다" - 공유 맥락 전제 |
| `Did I read that correctly?` | "did I read that correctly?" | 자기 이해 검증 - 정중한 확인 |
| `I just wanted to, that was my question for the meeting.` | "I just wanted to, that was my question for the meeting." | 질문 목적 한정 - "my question for the meeting" |

**Audrey 교훈**: "I saw an email about X, right?"로 시작하면 상대방은 "네 그 이메일 맞다"고 동의. "did I read that correctly?"는 자기가 잘 이해했는지 검증 - 질문이 아니라 "확인". 이렇게 하면 상대가 "아닙니다"라고 정정할 수 있는 퇴로도 준다. 정중한 이슈 review의 핵심.

### 질문 유형 2: 진행 상태 재촉 (Status Nudge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I'd like to ask to performance test when it's going to be finished or when SK hynix can get the results` | "I'd like to ask to performance test when it's going to be finished or when SK hynix can get the results about that." | 시점 명시 요구 - "when X is going to be finished" |
| `Please check the possibility of collaboration. Just let us know as soon as possible.` | "Please check the possibility of collaboration. Just let us know as soon as possible." | "as soon as possible"로 시점 압박 |
| `Let us know when you update it. Okay.` | "Let us know when you update it. Okay." | 업데이트 시 알림 요청 |

**Audrey 교훈**: "I'd like to ask when X is going to be finished" - "언제 끝나는지"를 직접 물어. 회의에서 시점을 물을 때 "when"으로 시작하면 상대는 날짜로 답해야 한다. "as soon as possible"은 강한 압박이지만 "please check"로 정중하게 포장. 한국어 "빨리 확인해 주세요"의 영어 버전. 회의에서 시점을 못 받으면 다음 회의로 미끄러지니 "when"으로 반드시 짚어.

### 질문 유형 3: 제한 설정 확인 (Constraint Clarification)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Do you have any update or not?` | "do you have any plan to update this table or not?" | "or not"으로 이항 질문 - 회피 차단 |
| `Are you asking whether we will support X with Y?` (Intel 재진술) | "Are you asking whether we will support native flat to a limb with 256 GB?" | (Intel 응답) 질문 재진술 |
| `Yeah. Or just do, do you have any plan to update this table or not?` | "Yeah. Or just do, do you have any plan to update this table or not?" | "any plan" + "or not"으로 압박 |

**Audrey 교훈**: "any plan to X or not?" - "or not"을 붙이면 이항 질문이 된다. 상대는 "yes" 아니면 "no"로 답해야. 회의에서 모호한 답을 받을 때 "or not"으로 좁혀. 단 "or not"은 강하니 "any plan"으로 부드럽게 열어. SK 측이 이걸 잘 쓴다.

### 질문 유형 4: 정중한 우려 표현 (Polite Concern)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So, we are wondering the X is almost to limited power value` | "uh, we are wondering the five 12 gigabyte POS is a almost to limited power value" | "we are wondering" - 정중한 우려 |
| `So. We worry about that and we don't have any environment about high capacity` | "So. We worry about that and we don't have any. Environment about. Uh, High capacity." | "we worry about that" - 직접적 우려 |
| `So we will wait as Intel response. Or if you need some engineer discussion, let me know.` | "So we will wait as Intel response. Or if you need some engineer discussion, let me know." | 대안 제시 - "engineer discussion" 제안 |

**Audrey 교훈**: "we are wondering X"는 "we think X is a problem"보다 정중. "wondering"은 의문 형태라 비난이 아니다. 그 다음 "we worry about that"으로 우려를 명시. 그리고 "if you need some engineer discussion, let me know"로 대안을 제시 - 이게 협조적으로 들린다. 우려만 표현하면 불평이지만, 대안을 제시하면 협력 제안이 된다.

### 질문 유형 5: 범위 확인 (Scope Clarification)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So what happens on the switch is not visible to us, right?` | "So what happens on the switch is not to visible to us, right? We only see what XConn through its fabric manager exposes to our CPU." | "right?"로 확인 + 자기 이해 부연 |
| `Do you use some switch or is that software module or something like that?` | "Do you use some switch or is that software module or something like that?" | "or something like that"로 가능성 열어 |
| `How do you plan to divide the MLD?` | "How do you plan to divide the MLD?" | "how do you plan to" - 계획 질문 |

**Audrey 교훈**: "right?"를 붙이면 자기 이해를 검증하면서 상대 동의를 끌어낸다. "is not visible to us, right?" - "우리한테 안 보이죠?" - 이건 확인이자, "우리가 모르는 게 당연하다"는 면책. 기술 회의에서 모호한 경계를 짚을 때 "X, right?"를 자주 써.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

### 협상 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 다음 회의로 미루기 | SK | "So we would like to touch this one in next meeting." | "touch this one in next meeting" - 정중한 미루기 |
| 이메일로 후속 | SK | "our engineer single sync that is a real bug or hard just to, it's a tip. No, no. So I can, Yeah, but that's correct. We are debugging right now." | 디버깅 중 상태 + 이메일 후속 |
| 다음 분기 제안 | Intel | "Maybe, maybe we can touch base upon maybe after water. What do you suggest Jenny is like a maybe if, if, if they're not interested in currently, do we need to touch base upon in future? Is that a next quarter or one month, two months?" | "touch base" + 시점 옵션 제시 |
| 사내 검토후 답변 | Intel | "So let me wait till I, you know, get a response back from that team and then, um, move forward with that, whatever that next step." | "get a response back" - 대기 표현 |
| 요청 수용 | Intel | "I'm happy to take those and try and get you some answers." | "happy to take" - 정중 수용 |

**Audrey 교훈**:
- "we would like to touch this one in next meeting" - 미루기의 정중한 표현. "touch"로 가볍게 만들어. "discuss"보다 "touch"가 더 비공식적이라 미루기가 자연스럽다.
- "I'm happy to take those and try" - "happy to"로 수용의 감정을 표시. "try"로 책임을 완화. 이게 수용하되 약속하지 않는 화법.
- "touch base"는 후속 회의의 관용구. "touch base upon" - "확인해 보자" - next quarter, 1-2 month 옵션을 주면 상대가 시점을 고르게 되어 협상이 부드러워진다.

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 액션 명시 | Intel | "Yeah, I can, I can follow up with that." | "can follow up" - 후속 약속 |
| 결과 통보 약속 | Intel | "I'll keep you informed." | "keep you informed" - 정보 유지 약속 |
| 이메일 채널 | Intel | "if any question comes up, we will reach out via email" | "reach out via email" - 채널 명시 |
| 다음 스텝 시점 | Intel | "He'll be communicating the multi device performance scaling at that time." | "at that time" - 시점 한정 |
| 최종 퇴로 | Intel | "let me, let me see if I can't, you know..." | "see if I can't" - 시도 표현 |

**Audrey 교훈**:
- "I can follow up with that" - 가장 자주 나오는 action item. "follow up"이 핵심. "I'll check"보다 전문적이고, "I'll do it"보다 가볍다.
- "I'll keep you informed" - 정보를 계속 주겠다는 약속. "keep you"가 지속성을 표시. 한 번 알려주고 마는 게 아니라 계속 업데이트하겠다는 것.
- 회의에서 action item을 받을 때 "I'll check"는 약하고, "I can follow up"이 표준이다. 네가 SK 입장에서 Intel에게 받을 때, "Please follow up via email"로 요구해도 된다.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 CXL/메모리/디버깅 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **miss rate** | 캐시 미적중률 (DB에서 데이터가 흩어진 정도) | "If the miss rate is high, then flat memory mode doesn't work. Typically we want miss rate to be below 10%" - "below 10%"이 임계값 |
| **flat memory mode** | CXL 메모리를 flat하게 통합 운영하는 모드 | "if the miss rate is high, then flat memory mode doesn't work" - miss rate 의존성 |
| **flat2LM** (flat 2-level memory) | native DDR + CXL을 동일한 주소 공간으로 | "the only flat2a configuration that we have for 256 GB devices is the one on plus two" - "one L M requires one terabyte" |
| **auto-numa** | 자동 NUMA 페이지 마이그레이션 | "even simple CXL, TPP or auto-numa is not going to help either because that will be one worse because it will bring the whole 4K page" - "bring the whole 4K page" 비판 |
| **TPP** (Tiered Memory Pooling) | 메모리 tiering 기술 | "even simple CXL, TPP or auto-numa is not going to help" - 3가지 대안 동시 비판 |
| **4K page** | 4KB 단위 메모리 페이지 | "it will bring the whole 4K page. But next time you fetch the data, it doesn't need anything in the 4K page" - 페이지 낭비 설명 |
| **MLD** (Multi-Logical Device) | 하나의 CXL 장치를 다수 head node에 노출 | "MLD multi logic device. So, that will, I believe is a function of the fabric manager on the XConn switch" |
| **fabric manager** | CXL switch의 장치 관리 SW | "a function of the fabric manager on the XConn switch" |
| **XConn** | CXL switch 유일 벤더 | "the only available CXL switch on the market is through XConn right now" |
| **link training** | PCIe/CXL 링크 초기화 절차 | "we did 10,000 loops of all the link training tests, no red flag or no major issues as of today" - regression test |
| **regression test** | 회귀 테스트 | "we have been continually testing the regression test on the DMR system we have" - "regression test on X" |
| **DMR** (Development/Measurement Reference) | Intel 개발/측정 시스템 | "we're getting our DMR systems up and running in the lab" - 시스템 명 |
| **PDK** (Platform Design Kit) | Intel 플랫폼 개발 키트 | "we don't have anyone inside of Intel doing that right now. SK hynix have to check after get a pdk" |
| **link training test loop** | 링크 트레이닝 반복 테스트 | "10,000 loops of all the link training tests" - 회수 명시 |
| **red flag** | 주요 이슈 표시 | "no red flag or no major issues as of today" - 부정형 보고 |
| **power saving mode** | 전력 절약 모드 | "the system was going in power saving mode by throttling the core speeds or something" - 원인 추정 |
| **throttling** | 클럭/속도 강제 저하 | "throttling the core speeds" - 성능 저하 원인 |
| **single device performance** | 단일 장치 성능 | "the single device performances within the expectations" - 기대치 내 |
| **multi device performance scaling** | 다중 장치 성능 확장 | "He'll be communicating the multi device performance scaling at that time" - 지연 사유 |
| **low core count CPU** | 코어 수 적은 CPU | "We can't fully saturate a multiple device configuration due to the availability of low core count CPUs at this stage in the program" - 병목 사유 |
| **RDC** (Resource and Documentation Center) | Intel 자료 사이트 | "Having looked on any materials that maybe might be available on Intel's RDC, our resource and documentation site" - 약어 풀이 |
| **Gaudi** | Intel GPU 제품명 | "Gaudi is a, I mean, that the system is out there launched and everything" - 출시 상태 |
| **POC** (Proof of Concept) | 개념 증명 | "I think this work is more for the POC kind of work. It's not about any productization" - "not about productization" |
| **productization** | 제품화 | "It's not about any, any productization" - POC와 대비 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 55개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# ── Facilitator 화법 (Meeting Orchestration) ──
- id: m28-001
  expression: "So again, I saw an email about how they fix the issue, right?"
  category: issue_recall
  function: shared_context_setup
  speaker_role: facilitator
  difficulty: 4
  context: "So again, I saw an email about how they fix the issue, right?"
  note: "I saw an email about X, right?" - 정기 sync 미팅의 이슈 열기 화법

- id: m28-002
  expression: "did I read that correctly?"
  category: comprehension_check
  function: self_verification
  speaker_role: facilitator
  difficulty: 4
  context: "did I read that correctly?"
  note: 자기 이해 검증 - 정중한 확인 질문

- id: m28-003
  expression: "that was my question for the meeting"
  category: question_purpose
  function: meeting_scope
  speaker_role: facilitator
  difficulty: 3
  context: "I just wanted to, that was my question for the meeting."

- id: m28-004
  expression: "So what exactly is your question?"
  category: question_clarification
  function: precision_request
  speaker_role: facilitator
  difficulty: 4
  context: "So, what exactly is your question?"
  note: "exactly"로 모호 질문을 좁히는 화법 - 회의 시간 절약

- id: m28-005
  expression: "Are you asking whether X with Y?"
  category: question_restatement
  function: precision_confirm
  speaker_role: facilitator
  difficulty: 5
  context: "Are you asking whether we will support native flat to a limb with 256 GB?"
  note: 질문 재진술 - "Are you asking whether"로 정확성 확보

# ── Status 보고 (Status Reporting) ──
- id: m28-006
  expression: "we are looking for the reason why there is X"
  category: status_debugging
  function: cause_search
  speaker_role: issue_owner
  difficulty: 3
  context: "So we are looking for the reason why there is just some performance drop"

- id: m28-007
  expression: "we would like to touch this one in next meeting"
  category: deferral
  function: polite_postpone
  speaker_role: issue_owner
  difficulty: 4
  context: "So we would like to touch this one in next meeting."
  note: "touch"로 미루기 가볍게 - "discuss"보다 비공식적

- id: m28-008
  expression: "We are still debugging it, but."
  category: status_in_progress
  function: ongoing_admission
  speaker_role: issue_owner
  difficulty: 3
  context: "Yes. We are still debugging it, but."

- id: m28-009
  expression: "we did N loops of all the X tests, no red flag or no major issues as of today"
  category: regression_report
  function: time_bound_result
  speaker_role: tester
  difficulty: 5
  context: "we did 10,000 loops of all the link training tests, no red flag or no major issues as of today"
  note: "as of today" 필수 - regression 보고의 면책 공식

- id: m28-010
  expression: "There are some, I would say, minor or small issues"
  category: severity_hedging
  function: magnitude_downgrade
  speaker_role: tester
  difficulty: 4
  context: "There are some, I would say, minor or small issues"
  note: "I would say"로 평가 한정 - 자기 판단 명시

- id: m28-011
  expression: "no major issue, at least on the X side of the things"
  category: scope_bound
  function: domain_qualification
  speaker_role: tester
  difficulty: 4
  context: "no major issue, at least on the link side of the things"
  note: "at least on X side" - 영역 한정 면책

# ── 회피·포장 (Hedging & Deflection) ──
- id: m28-012
  expression: "I'll try and get you some answers. But right now, my understanding is X"
  category: soft_commitment
  function: limited_promise
  speaker_role: intermediate
  difficulty: 5
  context: "I'll try and get you some answers. But yeah, right, right now, my understanding is not having conversations with our GPU team and CXL at this time."
  note: "I'll try"로 책임 완화 + "my understanding is"로 자기 한정

- id: m28-013
  expression: "I don't recall X. So I'm happy to take those and try and get you some answers."
  category: memory_disclaimer
  function: polite_recover
  speaker_role: intermediate
  difficulty: 5
  context: "I don't recall seeing this slide in the last deck. So you laid out some specific questions. I'm happy to take those and try and get you some answers."
  note: "I don't remember" 대신 "I don't recall" - 더 전문적

- id: m28-014
  expression: "my apologies, I missed that"
  category: apology
  function: clean_admission
  speaker_role: intermediate
  difficulty: 3
  context: "Yeah, my apologies. I missed that."

- id: m28-015
  expression: "the X team keeps things very close within their organization"
  category: team_boundary
  function: blame_redirect
  speaker_role: intermediate
  difficulty: 5
  context: "the GPU team keeps things very close within their organization"
  note: 타 팀 비협조를 관용구로 - 자기 책임 회피

- id: m28-016
  expression: "I'm almost absolutely certain on is there is no X"
  category: uncertain_assertion
  function: strong_disclaimer
  speaker_role: intermediate
  difficulty: 5
  context: "One item that you have on there that I'm almost absolutely certain on is there is no lending of any GPUs"
  note: "almost absolutely certain" - 모순적 강조

- id: m28-017
  expression: "I'll give you some tip. So don't X too much. So you have to figure out Y."
  category: tip_delivery
  function: critique_as_advice
  speaker_role: expert
  difficulty: 5
  context: "I'll give you some tip. So don't debug too much. So you have to figure out what the miss rate is in general."
  note: 강한 비판을 "tip" 틀 안에 - 정중한 방향 정정

- id: m28-018
  expression: "So that's my tip. That's all."
  category: tip_close
  function: explicit_close
  speaker_role: expert
  difficulty: 3
  context: "So that's my tip. That's all."

- id: m28-019
  expression: "We've identified the right folks inside of X"
  category: in_progress
  function: progress_evidence
  speaker_role: coordinator
  difficulty: 4
  context: "We've identified the right folks inside of Intel. We've sent them your information as well as the follow up that you just sent."

- id: m28-020
  expression: "So hopefully, either an email update or some type of communication when I know more"
  category: vague_promise
  function: soft_followup
  speaker_role: coordinator
  difficulty: 4
  context: "So hopefully, um, either an email update or, uh, some type of communication when I know more from that."

- id: m28-021
  expression: "let me wait till I get a response back from that team and then move forward with whatever that next step"
  category: waiting_status
  function: pending_report
  speaker_role: coordinator
  difficulty: 4
  context: "let me wait till I, you know, get a response back from that team and then, um, move forward with that, whatever that next step."

# ── 정중한 도전 (Polite Challenge) ──
- id: m28-022
  expression: "Do you have any information on this one?"
  category: direct_inquiry
  function: status_request
  speaker_role: questioner
  difficulty: 3
  context: "Do you have any information on this one?"

- id: m28-023
  expression: "do you have any plan to update this table or not?"
  category: binary_question
  function: forced_clarity
  speaker_role: questioner
  difficulty: 4
  context: "do, do you have any plan to update this table or not?"
  note: "or not"으로 이항 질문 - 회피 차단

- id: m28-024
  expression: "we are wondering the X is almost to limited Y"
  category: polite_concern
  function: concern_stating
  speaker_role: questioner
  difficulty: 4
  context: "uh, we are wondering the five 12 gigabyte POS is a almost to limited power"

- id: m28-025
  expression: "we worry about that and we don't have any environment about X"
  category: direct_concern
  function: resource_lack
  speaker_role: questioner
  difficulty: 3
  context: "We worry about that and we don't have any. Environment about. Uh, High capacity."

- id: m28-026
  expression: "Please check the possibility of X. Just let us know as soon as possible."
  category: nudge
  function: time_pressure
  speaker_role: questioner
  difficulty: 3
  context: "Please check the possibility of collaboration. Just let us know as soon as possible."

- id: m28-027
  expression: "Let us know when you update it."
  category: update_request
  function: notification_ask
  speaker_role: questioner
  difficulty: 2
  context: "Let us know when you update it. Okay."

- id: m28-028
  expression: "I'd like to ask when X is going to be finished or when Y can get the results"
  category: time_inquiry
  function: deadline_request
  speaker_role: questioner
  difficulty: 4
  context: "I'd like to ask to performance test when it's going to be finished or when SK hynix can get the results about that."

- id: m28-029
  expression: "X is not visible to us, right? We only see what Y exposes to our CPU"
  category: scope_check
  function: boundary_confirm
  speaker_role: questioner
  difficulty: 5
  context: "So what happens on the switch is not to visible to us, right? We only see what XConn through its fabric manager exposes to our CPU."

- id: m28-030
  expression: "Do you use some X or is that Y or something like that?"
  category: open_question
  function: possibility_explore
  speaker_role: questioner
  difficulty: 3
  context: "Do you use some switch or is that software module or something like that?"

- id: m28-031
  expression: "How do you plan to divide the X?"
  category: plan_inquiry
  function: approach_question
  speaker_role: questioner
  difficulty: 3
  context: "How do you plan to divide the MLD?"

# ── 협상·액션 (Negotiation) ──
- id: m28-032
  expression: "we would like to touch this one in next meeting"
  category: deferral
  function: polite_postpone
  speaker_role: negotiator
  difficulty: 4
  context: "So we would like to touch this one in next meeting."

- id: m28-033
  expression: "I'm happy to take those and try and get you some answers"
  category: acceptance
  function: polite_accept
  speaker_role: intermediate
  difficulty: 4
  context: "I'm happy to take those and try and get you some answers."

- id: m28-034
  expression: "I can follow up with that"
  category: action_item
  function: followup_promise
  speaker_role: intermediate
  difficulty: 3
  context: "Yeah, I can, I can follow up with that."

- id: m28-035
  expression: "I'll keep you informed"
  category: info_commitment
  function: ongoing_update
  speaker_role: intermediate
  difficulty: 3
  context: "I'll keep you informed."

- id: m28-036
  expression: "if any question comes up, we will reach out via email"
  category: channel
  function: communication_route
  speaker_role: negotiator
  difficulty: 3
  context: "yeah, we'll keep the discourse by email"

- id: m28-037
  expression: "maybe we can touch base upon maybe after X. Is that a next quarter or one month, two months?"
  category: future_option
  function: timeline_options
  speaker_role: intermediate
  difficulty: 5
  context: "maybe we can touch base upon maybe after water. What do you suggest Jenny is like a maybe if, if, if they're not interested in currently, do we need to touch base upon in future? Is that a next quarter or one month, two months?"

- id: m28-038
  expression: "if you need some engineer discussion, let me know"
  category: offer
  function: alternative_offer
  speaker_role: negotiator
  difficulty: 3
  context: "Or if you need some engineer discussion, let me know."

- id: m28-039
  expression: "I'd like to ask you"
  category: request_open
  function: polite_ask
  speaker_role: negotiator
  difficulty: 2
  context: "I'd like to ask you."

# ── 도메인 어휘 활용 (Vocabulary in Context) ──
- id: m28-040
  expression: "if the miss rate is high, then X doesn't work"
  category: technical_rule
  function: threshold_rule
  speaker_role: expert
  difficulty: 5
  context: "If the miss rate is high, then flat memory mode doesn't work."

- id: m28-041
  expression: "Typically we want X to be below Y%"
  category: threshold_stating
  function: metric_target
  speaker_role: expert
  difficulty: 4
  context: "Typically we want miss rate to be below 10%."

- id: m28-042
  expression: "the only available X on the market is through Y right now"
  category: market_constraint
  function: vendor_uniqueness
  speaker_role: expert
  difficulty: 4
  context: "the only available CXL switch on the market is through XConn right now"

- id: m28-043
  expression: "X is a function of Y"
  category: technical_attribution
  function: cause_attribution
  speaker_role: expert
  difficulty: 4
  context: "that will, I believe is a function of the fabric manager on the XConn switch"
  note: "X is a function of Y" - X가 Y에 의해 결정된다는 기술 표현

- id: m28-044
  expression: "we can't fully saturate X due to the availability of Y at this stage in the program"
  category: bottleneck
  function: constraint_reason
  speaker_role: tester
  difficulty: 5
  context: "We can't fully saturate a multiple device configuration due to the availability of low core count CPUs at this stage in the program."

- id: m28-045
  expression: "X works as expected"
  category: positive_status
  function: confirmation
  speaker_role: tester
  difficulty: 3
  context: "the memory mode flows works as expected"

- id: m28-046
  expression: "we don't see any indicators of X with the current available Y"
  category: caveat_status
  function: limited_positive
  speaker_role: tester
  difficulty: 5
  context: "they don't, he doesn't see any indicators of performance issues with the device with the current available platforms"
  note: "with current available Y" - 현재 한정 면책

- id: m28-047
  expression: "this is more for the X kind of work. It's not about any Y"
  category: scope_definition
  function: work_classification
  speaker_role: expert
  difficulty: 4
  context: "I think this work is more for the POC kind of work. It's not about any, any productization."

# ── 발화 채움 (Discourse Markers) ──
- id: m28-048
  expression: "So again, I saw an email about X"
  category: discourse_marker
  function: context_recall
  speaker_role: facilitator
  difficulty: 3
  context: "So again, I saw an email about how they fix the issue, right?"

- id: m28-049
  expression: "It's almost like you were reading my mind"
  category: rapport
  function: alignment_stating
  speaker_role: coordinator
  difficulty: 4
  context: "It's almost like you were reading my mind. Yes, that is absolutely correct."
  note: 유대 형성 화법 - "내 생각 읽으셨네요"

- id: m28-050
  expression: "I wasn't sure if you were wanting to address this"
  category: turn_offer
  function: polite_open
  speaker_role: facilitator
  difficulty: 4
  context: "I wasn't sure if you were wanting to address this."

- id: m28-051
  expression: "I know that there was email thread with X and you folks on that item"
  category: thread_reference
  function: prior_context
  speaker_role: facilitator
  difficulty: 3
  context: "I know that there was email thread with Ed and you folks on that item."

- id: m28-052
  expression: "If nothing else, then we can close out the meeting"
  category: close
  function: meeting_close
  speaker_role: facilitator
  difficulty: 3
  context: "If nothing else, then we can close out the meeting."

- id: m28-053
  expression: "anything from X side?"
  category: turn_check
  function: open_floor
  speaker_role: facilitator
  difficulty: 2
  context: "Anything from Intel side?"

- id: m28-054
  expression: "I mean, I shared the X with Y at the end of the winter break, right?"
  category: status_recall
  function: prior_share
  speaker_role: tester
  difficulty: 3
  context: "I shared the link training tests with SK hynix at the end of the winter break, right?"

- id: m28-055
  expression: "Hopefully those will be addressed as well"
  category: optimistic_close
  function: future_resolution
  speaker_role: tester
  difficulty: 3
  context: "Hopefully those will be addressed as well."
  note: "Hopefully"로 미래 해결 암시 - 약속 아닌 희망
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-01-22 09 02 13_EN_Intel-extracted.wav` (총 ~16분, 3,116단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입 (line 16-49) | Jenny의 이슈 회상 + Sundan status 보고 + "did I read that correctly?" | facilitator 이슈 열기 + status 보고 | ★★★ |
| 2 | Anil의 tip (line 55-81) | "I'll give you some tip" + miss rate 설명 + "don't debug too much" + "That's all" | tip 전달 화법 (이 회의의 하이라이트) | ★★★★ |
| 3 | flat2LM 질문 (line 198-219) | Sundan의 "any plan to update or not?" + Intel "I can follow up" + "I'll keep you informed" | 이항 질문 + soft commitment | ★★★ |
| 4 | GPU 협업 (line 252-309) | "GPU team keeps things close" + "I'll try" + "almost absolutely certain" | 타 팀 책임 전환 + soft commitment | ★★★★ |
| 5 | link training 마무리 (line 327-348) | Lutford regression 보고 + "no red flag as of today" + "close out the meeting" | regression 보고 + 마무리 화법 | ★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 2, 4가 가장 가치 높음 - tip 전달과 soft commitment가 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **issue review + debug coordination** register다. 발표자-청중 구조가 아니라 다자간 이슈 동기화. 각 역할마다 학습해야 할 화법이 다르다:
- **Facilitator (Jenny/Don)**: 이슈 회상, 질문 명확화, 회의 마무리 - 네가 회의 진행할 때
- **Issue owner (Sundan)**: status 보고, 정중한 우려, 시점 압박 - 네가 이슈 올릴 때
- **Expert (Anil)**: tip 전달, threshold 설명, 방향 정정 - 네가 기술 조언할 때
- **Intermediate (Jenny/GPU 팀 대리)**: 책임 한정, 타 팀 비협조 설명, soft commitment - 네가 다른 팀 답변 대신 전달할 때
- **Tester (Lutford/Ivan)**: regression 보고, bottleneck 설명, 제한적 긍정 - 네가 테스트 결과 보고할 때

### Pragmatics (화용론) 핵심
1. **"as of today" 면책**: regression 보고에서 "no issues as of today"는 "내일 다를 수 있다"는 면책이 내장. 이게 없으면 "no issues"는 약속이 되버린다. 회의에서 regression 결과 보고할 때 반드시 시점 한정을 붙여.
2. **"I'll try" vs "I'll do"**: 자기가 통제 못 하는 답변(다른 팀)을 대신 전달할 때 "I'll try"로 책임을 완화. "I'll get you the answer"는 100% 책임이지만 "I'll try and get you the answer"는 시도만 약속.
3. **"I don't recall"의 정중함**: "I don't remember"보다 전문적. 그리고 "I don't recall" 뒤에는 무조건 "I'm happy to take those and try"로 후속을 붙여. 모르는 걸로 끝나지 않게.
4. **"tip"으로 비판 완화**: "don't debug too much"는 단독으면 도전. "I'll give you some tip"이라는 틀 안에 있으면 조언. 상대방 방향을 정정할 때 이 틀을 써.
5. **"or not"으로 회피 차단**: "do you have any plan to X or not?" - "or not"을 붙이면 상대는 yes/no로 답해야. 모호한 답을 받을 때 이항 질문으로 좁혀.

### 네가 당장 써야 할 Top 5
1. **"I'll try and get you some answers. But right now, my understanding is X."** - soft commitment
2. **"I don't recall X. I'm happy to take those and try."** - 메모리 한정 + 정중 후속
3. **"we did N loops of X tests, no red flag or no major issues as of today"** - regression 보고
4. **"do you have any plan to X or not?"** - 이항 질문으로 회피 차단
5. **"I'll give you some tip. So don't X too much. So you have to figure out Y."** - 정중한 방향 정정

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "오늘 현재 문제 없습니다" | "no red flag or no major issues as of today" | "as of today"가 면책 - 내일 다를 수 있다 |
| "확인해 보겠습니다" | "I'll try and get you some answers" | "try"로 시도만 약속 - 100% 책임 아님 |
| "기억 안 납니다" | "I don't recall. I'm happy to take those and try." | "don't recall" + 후속 - 모르는 걸로 끝나지 않게 |
| "저쪽 팀이 안 열어서요" | "the GPU team keeps things very close within their organization" | 관용구로 타 팀 성향 탓 - 자기 책임 회피 |
| "다음 회의에서 다시" | "we would like to touch this one in next meeting" | "touch"로 가볍게 - "discuss"보다 비공식적 |
| "빨리 알려 주세요" | "Please let us know as soon as possible" | "please"로 정중 + "as soon as possible"로 압박 |
| "확인해야 할 게 있어요" | "you have to figure out what the miss rate is" | "you have to figure out X" - 전문가의 방향 제시 |
| "이건 POC입니다" | "this is more for the POC kind of work. It's not about any productization" | "not about Y"로 범위 명시 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 55개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법·3절 도전 화법을 중심으로 dump 작성
4. **비교 학습**: 9절 한국어-영어 비교표로 화법 차이 체득
5. **역할별 연습**: issue owner(너) / facilitator(너) / expert(너) / intermediate(너) 4역할 모두 연습 - 이 회의는 단일 발표자가 아니라 역할별 화법이 다양하므로

---

*Textbook 28 - Intel January sync (2026-01-22). 회의 유형 D (이슈/품질 디버깅). 표현 DB 55개. 5개 발췌 구간. 작성: 2026-09-01.*
