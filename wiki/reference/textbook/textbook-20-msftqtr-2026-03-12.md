---
textbook_id: 20
meeting: MSFTQTR (Microsoft Quarterly Business Review)
date: 2026-03-12
type: B (로드맵/공급 alignment)
partner: Microsoft (Victor, Sam Di, multiple MSFT voices)
sk_side: SK Hynix (Young-Goo Koh / Next Generation Memory & 3D Planning, Custom HBM team, CXL CMM team, Quality team)
duration_words: 3164
audio: repo/webex-audio/2026-03-12 08 35 58_EN_MSFTQTR-extracted.wav
transcript: repo/webex-audio/2026-03-12 08 35 58_EN_MSFTQTR-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, microsoft, msft, qbr, hbm, custom-hbm, 3ds, cxl, cmm, dram-roadmap, supply-alignment, type-b]
---

# Textbook 20 - Microsoft QBR (2026-03-12)

> **회의 유형**: B (로드맵/공급 alignment) - 분기별 비즈니스 리뷰. 타임라인 타깃, 볼륨/샘플 요청, 스펙 조율, 마일스톤 정렬.
> **학습 가치**: HBM 커스텀 개발 협상, HBM5 bump metrics 스펙 클로저, CXL CMM 로드맵, DRAM 기술 전환(6F² → 4F² vertical gate → 3D DRAM), 데이터센터 품질 리뷰. Type B의 핵심 - "we're targeting X in Y", "can you support X by Y", spec pushback, milestone coordination.
> **Audrey 관점**: 이 회의는 QBR 레지스터다. 파트너(MSFT)가 타임라인·볼륨·스펙을 물고, SKH가 "targeting", "by end of Q2", "we don't plan to change"로 방어/협상. Type B 협상 언어의 밀도 높은 샘플.

---

## 1. 발화 아키텍처 - SKH 발표자의 설계 구조 (4단계)

MSFTQTR은 한 명의 장편 발표자가 아니라 여러 SKH 발표자가 차례로 micro-presentation을 하는 구조. 각 발표자는 **QBR 포맷**을 따른다: 현재 상태 → 타임라인 타깃 → 오픈 이슈 → 합의 요청. 이게 Type B 회의의 발표 설계 뼈대다.

### 단계 1: 현재 상태와 타임라인 타깃 동시 제시 (Status + Target Timeline)

Type B 발표자는 "현재 우리가 뭘 하고 있는가"와 "언제까지 뭘 할 것인가"를 한 문장에 묶는다. 이게 Type A(기술 deep-dive)와의 결정적 차이.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we are targeting X (product) by Y (time)` | "we are targeting our second generation CXL CMM DDR5 3.S2T... targeting this year" | 타임라인 타깃 - Type B 핵심 동사 |
| `we plan to extend X to Y by Z` | "we plan to extend 6F square one further generation to sub 10 nanometer 0A by 2028" | "plan to extend X to Y by Z" - 로드맵 약속 공식 |
| `we are preparing X, but the schedule is not fixed yet` | "we are also preparing vertical gate V4 and V5, but the schedule is not fixed yet" | "not fixed yet" - 확정 회피하며 로드맵 공개 |
| `we are planning to build X as a prototype by Y` | "we are planning to build 3D DRAM 3D 0 as a prototype by 2030" | "as a prototype" - 양산이 아닌 프로토타입 명시 |

**Audrey 교훈**: Type B 회의에서 "will do X"는 위험하다. "we are targeting X by Y"가 안전하다 - "targeting"은 목표임을 명시하되 확약은 회피. "will"은 약속이지만 "targeting"은 목표다. 한국어 "목표로 하고 있습니다"의 영어 버전. 네가 로드맵을 발표할 때 무조건 "we are targeting"을 써라.

### 단계 2: 오픈 이슈와 의존성 명시 (Open Items + Dependency)

Type B 발표자는 "닫아야 할 이슈"를 명시하고, 의존관계를 드러낸다. 이게 QBR의 협상 자리다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `the key items that we need to close by end of Q2` | "the key items that we need to close by end of Q2" | "close by end of Q2" - 마감 일정 명시 |
| `X is the most critical. We are trying to drive a consensus by end of this month` | "the bump map is the most critical. And we are trying to drive a consensus in within the task group by end of this month" | "drive a consensus by Y" - 합의 주도 표현 |
| `some other items are dependent to the X discussion` | "some other items that are marked as triangle in this table are dependent to the bump map discussion" | "dependent to X" - 의존관계 공식 |
| `we want to close X first and then Y` | "we want to close the bump map discussion first and probably have like key other items" | 순서 명시 - 협상 우선순위 |

**Audrey 교훈**: "We need to close X by Y" - QBR에서 가장 많이 쓰는 표현. 단순히 "we need X"가 아니라 "close"가 합의 완료의 뉘앙스. "Close the discussion", "close the spec", "close the item" - 다 "합의 완료"다. 그리고 "dependent to X"로 의존관계를 명시하면, 상대가 "그럼 X부터 하자"라고 우선순위에 동의하게 된다.

### 단계 3: 포지션 명시와 정당화 (Position + Justification)

Type B 발표자는 SKH의 입장을 명시하고, 왜 그 입장인지 기술적 근거를 댄다. 이게 스펙 pushback의 기본형이다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `from our perspective, X is the optimal way` | "from our perspective, the 23 micrometer is the optimal way with a 55 by 70 micrometer bump pitch" | "from our perspective, X is optimal" - 입장 명시 공식 |
| `we believe that the X risk is relatively small, comparing to Y` | "we believe that the thermal risk is kind of relatively small, comparing to all the study that we have done" | "relatively small, comparing to Y" - 위험 최소화 정당화 |
| `we don't plan to make any change` | "we don't plan to make any change" | 직접적 비변경 선언 |
| `Hynix is not planning any making any big changes on the X` | "Hynix is not planning any making any big changes on the A-word or D-word signal layout" | "not planning" - 현재 진행형으로 의도 부정 |

**Audrey 교훈**: "We don't plan to make any change"는 강한 발화다. QBR에서 이 정도 직접 표현은 허용된다. 하지만 바로 뒤에 "we want to make a fast consensus"를 붙여서 "안 바꿀 건데, 합의는 빨리 하자"로 협상 여지를 만든다. 한국어 "변경 계획 없습니다" 다음 "빠른 합의를 원합니다"로 이어지는 패턴의 영어 버전.

### 단계 4: 협상 마감과 다음 액션 연결 (Close + Next Action)

발표 마지막에 "우리가 뭘 닫아야 하는가"를 다시 한번 짚고, 다음 액션을 제안한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we need to expedite the X in order to meet our schedule` | "we need to expedite the spec closure in order to meet our schedule" | "expedite X to meet Y" - 일정 압박 공식 |
| `to meet that schedule, we need to have X back by Y` | "to meet that schedule, we need to have some sort of like initial design targets back by second quarter of this year" | "to meet X, we need Y by Z" - 조건부 일정 |
| `maybe we can schedule a separate session to have some exploratory discussion` | "maybe we can like a schedule a separate session to have some exploratory discussion" | "separate session" - 회의 미루기 공식 |

**Audrey 교훈**: "expedite"는 QBR 핵심 동사. "hurry up"이 아니라 "expedite the closure" - 전문가의 "빨리 하자". 그리고 "schedule a separate session"은 이 회의에서 답을 못 줄 때 미루는 정중 화법. "나중에 다시 얘기하자"가 아니라 "별도 세션을 잡자" - 더 전문적이고 진지하다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

Type B 회의의 회피는 "언제"를 중심이다. 일정 확약을 피하면서도 협조적으로 보이는 화법.

### 전략 1: "It depends" + 조건부 타임라인 (Conditional Timeline)

가장 중요한 Type B 회피. 직접적 일정 질문에 "case-by-case"로 시작, 대략값으로 마무리.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| HBM 커스텀 개발 소요 시간 질문 | "for the custom HBM, as a name implies, it depends based on the project by project. So it's very hard to tell you what's the generic timeline because whenever we close on the agreement and then SOW, then we need to look at also our internal resource allocation status. And depending that situation, that overall project milestone will vary. Typically, you know, from the discussion kickoff to the project launch is about two years." | "커스텀 HBM은 이름 그대로 프로젝트마다 다릅니다. 제네릭 타임라인 말씀드리기 어렵습니다. 계약과 SOW 클로즈 후 내부 자원 할당 상황을 봐야 해서, 프로젝트 마일스톤이 달라집니다. 일반적으로 킥오프부터 런치까지 약 2년입니다." |

**패턴 공식**: `It depends based on the project by project. It's very hard to tell you the generic timeline because [conditions]. Typically, [ballpark].`

**Audrey 교훈**: "It depends"는 약한 회피로 들릴 수 있다. 그래서 "as a name implies, it depends"로 시작하면 - "커스텀이라는 이름 자체가 case-by-case를 의미" - 회피가 아니라 제품 본성 설명으로 프레이밍. 그리고 마지막에 "typically, about two years"로 대략값을 줘서 협조적 태도를 유지. 이 구조를 외워라: 회피 + 이유 + 대략값.

### 전략 2: "Not fixed yet" + "exploration mode" (Roadmap Vagueness)

로드맵 확정을 피하면서 "작업 중"임은 강조.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 4F² V4/V5 일정 질문 | "we are also preparing vertical gate V4 and V5, but the schedule is not fixed yet. So that's why we used dashed line here. We are doing technical exploration now on these technologies." | "V4/V5 준비 중이나 일정 미확정. 그래서 점선으로 표시. 기술 탐색 중입니다." |
| 3D-stacked HBM 로드맵 | "we are currently in the exploration mode on the 3D like logic HBM stack. So we are aware of that and we are also having some internal discussions and having some past finding discussion with a few partners and customers." | "3D logic HBM은 탐색 모드. 인지는 하고 있고, 내부 논의 중이며 일부 파트너/고객과 논의 중입니다." |

**패턴 공식**: `We are currently in the exploration mode on X. We are having some internal discussions and discussion with a few partners.`

**Audrey 교훈**: "exploration mode"는 "research"보다 진지하고 "committed"보다 자유롭다. 로드맵 발표에서 가장 안전한 단어. 그리고 "dashed line"을 언급하며 시각적으로 "미확정"을 강화하는 것 - 발표 자료와 언어가 일치하는 전문가 화법. "we are aware of that"는 경쟁사 제품 질문에 대한 정중한 인정.

### 전략 3: 조건부 의존적 전환 (Market-Dependent Transition)

기술 전환 시점을 "시장 상황"에 돌려서 확약 회피.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 4F² V1 양산 시점 | "transition from 0A to vertical gate V1 will be dependent on the market situation at that time frame. So it does not necessarily mean that we will start mass production from 2028 on V1." | "0A에서 V1 전환은 그 시점 시장 상황에 의존. 따라서 2028년 V1 양산을 반드시 시작한다는 의미는 아닙니다." |
| 3D DRAM 전환 | "transition from vertical gate to 3D DRAM also can be dependent on the market situation at that time." | "vertical gate에서 3D DRAM 전환도 그 시점 시장 상황에 의존 가능." |

**패턴 공식**: `Transition from X to Y will be dependent on the market situation. It does not necessarily mean that we will Z.`

**Audrey 교훈**: "dependent on the market situation" - 이 표현은 로드맵 발표에서 가장 많이 쓰는 확약 회피. 기술 준비는 되어 있지만 시장이 받아들여야 양산 - 기술 부식체가 아니라 비즈니스 판단체로 프레이밍. "does not necessarily mean"로 확정 해석을 차단. 이게 로드맵 발표자의 안전망이다.

### 전략 4: 이슈 인정 + 진행 중 표시 (Issue Acknowledgment + Ongoing Action)

데이터센터 품질 이슈에서, 문제를 인정하면서도 "대응 중"임을 강조.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR5 uncorrectable error 증가 | "we do for both Gen 9 and Gen 10 platform we are meeting targets. I do see that Gen 10 slightly increased quarter to quarter and some of this is probably we are having an ongoing conversation" | "Gen 9/10 타깃 충족. 단 Gen 10은 QoQ 약간 증가, 이건 진행 중인 대화입니다." |
| storage telemetry 부족 | "we are actively working on getting the real logs or the memory register logs too. Once that is probably going to take some time. It's not immediate." | "실제 로그 획득 적극 작업 중. 시간 걸립니다. 즉시는 아닙니다." |

**패턴 공식**: `We are actively working on X. It's going to take some time. It's not immediate.`

**Audrey 교훈**: "actively working on"을 쓰면 "작업 안 함"이 아니라 "진행 중"으로 들린다. 그리고 "not immediate"로 기대를 낮추되 "no"라고는 안 한다. QBR에서 품질 이슈 대응을 보고할 때 이 패턴을 써라.

### 전략 5: 비용 우려를 기술 가치로 재프레이밍 (Cost Concern Reframe)

MSFT가 PIM 비용 문제 제기하자, 별도 logic die 대안을 제안.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| PIM 비용 우려 | MSFT: "PIM may incur some prohibitive cost overhead in die overhead." → SKH 측 후속: "if we have to manipulate some of the data, if it's close enough to our own processing unit, it may be easier to move the data there and manipulate it. Whether it could be a last level cache, could be in the controller, could be in so many places." | "데이터 조작 필요 시, 자체 처리 유닛 가까이 있으면 데이터 이동이 쉽습니다. last level cache, controller 등 여러 곳 가능." |

**Audrey 교훈**: 상대의 비용 우려를 직접 반박하지 말고, "대안 위치"를 나열하며 "여러 옵션이 있다"로 돌려라. "Whether it could be X, could be Y, could be Z" - 이 나열 패턴이 비용 문제를 우회하는 부드러운 화법.

---

## 3. 정중한 도전 화법 (MSFT 측 질문자)

Type B 회의의 질문은 "기술 도전"보다 "조건 탐색"이다. 타임라인, 볼륨, 스펙 변경 가능성을 정중하게 파고든다.

### 질문 유형 1: 타임라인 가이던스 요청 (Timeline Guidance Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `What's the general time frame for X?` | "What's the general time frame for custom HBM development?" | "general time frame" - 구체가 아닌 대략 요청 |
| `What I need by that is, assuming Y, how long is Z? What would be your guidance on that?` | "What I need by that is assuming we start engaging with SK. How long is that typical design? What would be your guidance on that?" | "assuming Y" 전제 + "guidance" 요청 |
| `What would be your guidance on that?` | (위와 동일) | "guidance" - 가이던스 요청 공식 |

**Audrey 교훈**: "How long does it take?"는 너무 직접. "What would be your guidance on that?" - 상대에게 "가이던스"를 요청하는 정중 화법. 상대가 전문가로서 조언하는 자리를 준다. 네가 일정 물을 때 무조건 이 표현 써라.

### 질문 유형 2: 로드맵 존재 탐색 (Roadmap Existence Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I was wondering if you guys have thought of anything like that` | "I was wondering if you guys have thought of anything like that." | "I was wondering if" - 가장 정중한 탐색 |
| `You have anything on your roadmap like that or is that something you consider?` | "You have anything on your roadmap like that or. Is that something you consider?" | "on your roadmap" + "something you consider" - 두 단계 탐색 |
| `Are you aware of that and do you have a response to that?` | "I'm just wondering, are you aware of that and do you have a response to that?" | "aware + response" - 인지 + 대응 이중 질문 |

**Audrey 교훈**: "I was wondering if"는 부드러운 질문 도입. 직접 "Do you have X?"보다 "I was wondering if you have X"가 훨씬 정중. "consider"는 "do"보다 약한 동사 - "실행 중"이 아니라 "고려 중"을 물을 때. 경쟁사 동향을 물을 때 "are you aware + do you have a response" 조합이 아주 강력하다.

### 질문 유형 3: 스펙 변경 의도 탐색 (Spec Change Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `What are your thoughts on X?` | "What are your thoughts on interrupting P and then processing near memory with some separate logic die?" | "thoughts on X" - 의견 요청 |
| `I was curious what SK's position is on that` | "I was curious what SK's position is on that." | "position" - 입장 요청 |
| `It seemed to be some opposition at the committee meeting` | "It seemed to be some opposition at the committee meeting. You're trying to understand that a little bit more because we thought CA parity." | "seemed to be" - 추측으로 입장 탐색 |

**Audrey 교훈**: "What do you think?"는 캐주얼. "What are your thoughts on X?"가 비즈니스. 그리고 "I was curious what SK's position is" - "curious"로 정중함, "position"으로 입장 요청. 회의에서 상대 입장을 물을 때 "position"을 써라. "opinion"보다 격식 있다.

### 질문 유형 4: 비용/비즈니스 모델 도전 (Cost/Business Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `This is an expensive die. And it's trying to target a market that's very cost sensitive` | "this is an expensive die. And it's trying to target a market that's very cost sensitive. So the business model doesn't line up." | 비용 문제 + 시장 부적합 |
| `I mean, this is being designed for edge devices that are the most cost sensitive and we're adding significant overhead` | "I mean, this is being designed for edge devices that are the most cost sensitive and we're adding significant overhead to an LP6 die to enable it." | "designed for X" + "adding overhead" - 설계 의도 vs 현실 괴리 |

**Audrey 교훈**: 비즈니스 도전에서 "the business model doesn't line up"이 핵심 문장. "doesn't make sense"보다 격식 있고, "business model"이라는 프레임으로 기술 비판을 비즈니스 비판으로 승격. 네가 파트너 기술을 도전할 때 기술만 공격하면 감정싸움 되지만, "business model"을 들면 전문적 비즈니스 토론이 된다.

### 질문 유형 5: ROI 추정 요청 (ROI Trade-off Probe)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `set up some time later to try and understand from you which parameters, refresh, P rack etc. can we maybe change in D6 to help the ROI` | "should not now, but maybe set up some time later to try and understand from you which parameters refresh P rack etc. Can we maybe change in D six to help the ROI" | "set up some time later" + "help the ROI" - 후속 제안 + 가치 명시 |
| `it feels like making an offline load in D6 with all this extra cost needed because maybe it just needs to start a year later. Maybe that's a good trade off.` | "it feels like making an off-line load in D six with all this extra cost needed because maybe it just needs to start a year later. Maybe that's a good trade off." | "feels like" + "good trade off" - 의견을 부드럽게 제안 |

**Audrey 교훈**: "it feels like"는 "I think"보다 부드럽고 "maybe that's a good trade off"는 "you should do X"보다 훨씬 정중한 제안. 의견을 제안으로 포장. 그리고 "set up some time later"로 이 회의에서 답 안 듣고 별도 논의를 요청. Type B 회의에서 복잡한 질문은 "나중에 따로"로 미루는 것이 정상.

### 질문 유형 6: 품질 데이터 의미 해석 (Quality Data Interpretation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we want to understand more if these are two 3D issues or something that are on the software level or the system stack` | "we want to understand more if these are two 3D issues or something that are on the software level or the system stack that's causing these uncorrectable error events" | "want to understand more" + 대안 나열 |
| `I also want to see understand these multi bit error trends and how they're going to age over time` | "I also want to see understand these multi bit error trends and how they're going to age over time" | "age over time" - 시간 경과별 노화 |
| `is there anything that we can do more proactively` | "if there's any concerns or anything that we can do more proactively" | "more proactively" - 적극 대응 요청 |

**Audrey 교훈**: "we want to understand more"는 "we don't understand"와 다르다. 전자는 더 깊이 파고들 의향, 후자는 이해 못 함. 그리고 "age over time"은 "노화"의 정확한 비즈니스 영어 - "degrade"보다 구체적. "more proactively"는 "do more"보다 훨씬 진지한 대응 요청.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

Type B 회의의 핵심. 타임라인, 볼륨, 샘플, 마일스톤 언어.

### 협상 화법 - 타임라인

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 마감 일정 명시 | SKH | "we need to expedite the spec closure in order to meet our schedule that HomeJet presented, end of 28 or early 29" | "meet our schedule that X presented" - 외부 일정 인용 |
| 조건부 마감 | SKH | "to meet that schedule, we need to have like some sort of like initial design targets back by second quarter of this year" | "to meet X, we need Y by Z" |
| 합의 주도 | SKH | "we want to make a fast consensus in the task group to make this move forward" | "fast consensus to move forward" |
| 일정 미루기 | MSFT | "should not now, but maybe set up some time later" | "set up some time later" - 정중 미루기 |
| 별도 세션 제안 | SKH | "maybe we can like a schedule a separate session to have some exploratory discussion" | "separate session" - 회의 미루기 |
| 사이클 활용 제안 | SKH | "we're having a cycle HBM deep dive. I don't know that may be a good time to bring in that material as well" | "may be a good time to bring in X" |

### 협상 화법 - 볼륨/샘플

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 샘플 수요 요청 | MSFT | "please let us know the sample demand since currently we're under the memory shortage" | "under the memory shortage" - 배경 설명 + 요청 |
| 우선 할당 제안 | MSFT | "if you have the initial sample demand, then let me create the teams for me to allocate Microsoft first" | "allocate Microsoft first" - 우선 순위 제안 |
| 의향 표시 | MSFT | "we'd be interested to discuss with you, or our density compute functions that might be put underneath one of your stacks" | "interested to discuss" - 의향 표시 |
| 스케줄 제안 | MSFT | "we'd be interested in having a discussion" → "Sure" → "schedule a separate session" | "interested" → "Sure" → 구체 제안 흐름 |

### 협상 화법 - 스펙

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 입장 명시 | SKH | "from our perspective, the 23 micrometer is the optimal way" | "from our perspective, X is optimal" |
| 비변경 선언 | SKH | "we don't plan to make any change" | 직접 거절 |
| 위험 최소화 | SKH | "we believe that the thermal risk is kind of relatively small, comparing to all the study that we have done for the past year" | "relatively small, comparing to Y" |
| 타협 가능성 시사 | SKH | "we want to make a fast consensus in the task group to make this move forward" | "fast consensus" - 속도로 타협 |

### Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 약속 | MSFT | "once we make the decision, [we'll share those]" | "once X, Y" - 조건부 후속 |
| 후속 약속 | MSFT | "once you finalize the memory pure, then please let us know the sample demand" | "once X, please let us know Y" |
| 자료 공유 후속 | SKH | "we will start sharing it with you but right now we are limited to the system event logs for storage" | "we will start sharing X but right now limited to Y" |
| 비확정 후속 | SKH | "I don't have an exact time that we will be enabling that. So once we have the data we will start sharing it with you" | "don't have exact time" + "once X, Y" |
| 별도 회의 약속 | SKH/MSFT | "maybe we can schedule a separate session" + "Sure" | "Sure" - 가벼운 약속 수락 |

**Audrey 교훈**:
- "once X, Y"는 QBR에서 가장 많이 쓰는 action item 패턴. "we'll do Y once X happens" - 조건부 약속.
- "allocate Microsoft first"는 강한 제안. "first"로 우선순위를 직접 요청. 샘플 볼륨 협상에서 쓸 수 있는 정중하지만 명확한 표현.
- "under the memory shortage"로 상황을 먼저 설명하고 요청 - 한국어 "지금 메모리 부족 상황이라"의 영어 버전. 배경 설명 → 요청의 구조를 외워라.
- "I don't have an exact time"은 "I don't know when"보다 훨씬 전문적. 시간 모를 때 이 표현 써라.

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 HBM/CXL/DRAM/품질 전문 용어. 각 용어의 정확한 쓰임새와 발화 맥락.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **custom HBM** | 고객 맞춤형 HBM (3D-stacked logic 아래 ASIC) | "for the custom HBM, as a name implies, it depends based on the project by project" - "as a name implies"로 본성 설명 |
| **SOW** (Statement of Work) | 작업 범위 정의서 | "whenever we close on the agreement and then SOW" - "close on X and Y" |
| **3D-stacked / 3D-like logic HBM** | 로직 칩 위에 HBM 적층 | "we are currently in the exploration mode on the 3D like logic HBM stack" |
| **bump metrics / bump map** | 범프 배치도 (스펙 합의 대상) | "the key opens from the HBM5 bump metrics perspective" / "the bump map is the most critical" |
| **bump pitch / bump diameter** | 범프 간격 / 범프 직경 | "23 micrometer is the optimal way with a 55 by 70 micrometer bump pitch" - 단위 표기 |
| **TSP center power / VHH power rail** | TSP 중앙 전원 레일 | "discussion to add some TSP center power, more like adding one VHH power rail in a center place" |
| **VDDQ / VPP / VSS** | DRAM 전원 레일 종류 | "what is the ideal ratio between VDDQ, VPP and VSS" |
| **task group** | JEDEC 내 스펙 합의 소위 | "drive a consensus in the task group by end of this month" |
| **ballot** | JEDEC 투표 절차 | "be prepared and ballot in the proper timeline" |
| **CA parity** | Command/Address parity (JEDEC 제안) | "Sam Di made a proposal in the CA and SANA CA parity block" - 인명 + 제안 연결 |
| **PIM** (Processing In Memory) | 메모리 내 처리 | "PIM including all those features that you need may incur some prohibitive cost overhead in die overhead" |
| **logic die** | 별도 로직 칩 | "processing near memory with some separate logic die" |
| **last level cache** | 최후 계층 캐시 | "Whether it could be a last level cache, could be in the controller" - 대안 나열 |
| **CXL CMM DDR5** | SKH CXL 메모리 모듈 | "we already have our first gen CXL CMM DDR5" |
| **CXL 3.1 2T** | CXL 3.1 2-tier | "we are targeting our second generation CXL CMM DDR5 3.S2T" |
| **EVP / ES** | Engineering Validation Prototype / Engineering Sample | "we have our EVP and our ES targeting this year. And of this year, it will be next year, February" - 마일스톤 |
| **DMR** | (문맥상) Design Maturity Review | "we'll target to intercept the DMR" |
| **mezzanine** | 중간층 PCB | "Two, like a mezzanine" - 적층 방식 설명 |
| **foldable twin PCB** | 접이식 트윈 PCB | "targeting having a foldable twin PCB and increasing the density up to 525 gigabytes" |
| **6F square / 4F square** | DRAM 셀 구조 (6F² / 4F²) | "we plan to extend 6F square one further generation to sub 10 nanometer 0A by 2028" |
| **vertical gate (VG)** | 수직 게이트 (4F² 전환) | "first platform vertical gate will be ready by 2028" - "ready by Y" |
| **3D DRAM** | 3D 적층 DRAM | "we are planning to build 3D DRAM 3D 0 as a prototype by 2030" |
| **hybrid copper bonding (HCB)** | 하이브리드 구리 접합 | "you have to do hybrid copper bonding. And so there that's where the expenses. That's where the challenge." |
| **mass production** | 양산 | "it does not necessarily mean that we will start mass production from 2028 on V1" |
| **uncorrectable error** | 정정 불가 에러 | "uncorrectable errors and multi-bit errors and how they're performing across the DDR4 and DDR5" |
| **multi-bit error** | 다중 비트 에러 | "anything other than single bits" - 정의 풀이 |
| **Gen 7 / Gen 9 / Gen 10** | MSFT 서버 세대 | "for Gen 5 we do see slight uptake... for both Gen 9 and Gen 10 platform we are meeting targets" |
| **excursion** | 품질 이탈 이벤트 | "help us capture some of these quality issues or excursions more reliably" |
| **telemetry** | 원격 측정/진단 데이터 | "do you think that we can enable the telemetry data on the Qovo 200 right away" |
| **system event logs** | 시스템 이벤트 로그 | "we only get this system event logs as of today" |
| **Qovo 200** | (문맥상) 서버 플랫폼 | "enable the telemetry data on the Qovo 200 right away once the system is deployed" |
| **13 weeks / 4 weeks rolling** | 평균 기간 (target 계산) | "previously taking average over 13 weeks but we will be looking into more of spikes in the three months" |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 50개. IDs use prefix `m20`.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: m20-001
  expression: "we are targeting X by Y"
  category: timeline_target
  function: roadmap_commitment
  speaker_role: presenter
  difficulty: 4
  context: "we are targeting our second generation CXL CMM DDR5 3.S2T... targeting this year"
  note: Type B 핵심 동사. "will" 대신 "targeting" - 약속 아닌 목표.

- id: m20-002
  expression: "we plan to extend X to Y by Z"
  category: roadmap_promise
  function: generation_extension
  speaker_role: presenter
  difficulty: 4
  context: "we plan to extend 6F square one further generation to sub 10 nanometer 0A by 2028"

- id: m20-003
  expression: "we are preparing X, but the schedule is not fixed yet"
  category: roadmap_vague
  function: hedged_commitment
  speaker_role: presenter
  difficulty: 4
  context: "we are also preparing vertical gate V4 and V5, but the schedule is not fixed yet"
  note: "not fixed yet" - 확정 회피하며 로드맵 공개. 안전한 로드맵 발표 패턴.

- id: m20-004
  expression: "we are planning to build X as a prototype by Y"
  category: milestone_prototype
  function: prototype_target
  speaker_role: presenter
  difficulty: 3
  context: "we are planning to build 3D DRAM 3D 0 as a prototype by 2030"
  note: "as a prototype" - 양산 아님 명시. 기대 관리.

- id: m20-005
  expression: "the key items that we need to close by end of Q2"
  category: deadline_spec
  function: closure_target
  speaker_role: presenter
  difficulty: 4
  context: "the key items that we need to close by end of Q2"
  note: "close by Y" - QBR 핵심. "complete" 아닌 "close" - 합의 완료 뉘앙스.

- id: m20-006
  expression: "X is the most critical. We are trying to drive a consensus by end of this month"
  category: consensus_drive
  function: priority_assert
  speaker_role: presenter
  difficulty: 4
  context: "the bump map is the most critical. And we are trying to drive a consensus within the task group by end of this month"
  note: "drive a consensus by Y" - 합의 주도. QBR 협상 공식.

- id: m20-007
  expression: "some other items are dependent to the X discussion"
  category: dependency
  function: dependency_link
  speaker_role: presenter
  difficulty: 3
  context: "some other items that are marked as triangle in this table are dependent to the bump map discussion"
  note: "dependent to X" - 의존관계 명시. 우선순위 설득.

- id: m20-008
  expression: "from our perspective, X is the optimal way"
  category: position_state
  function: stance_declare
  speaker_role: presenter
  difficulty: 4
  context: "from our perspective, the 23 micrometer is the optimal way with a 55 by 70 micrometer bump pitch"
  note: "from our perspective" - 견해 명시. 직접 주장 회피.

- id: m20-009
  expression: "we believe that the X risk is relatively small, comparing to Y"
  category: risk_minimize
  function: concern_deflect
  speaker_role: presenter
  difficulty: 5
  context: "we believe that the thermal risk is kind of relatively small, comparing to all the study that we have done for the past year"
  note: "relatively small, comparing to Y" - 위험 최소화 정당화. 비교로 회피.

- id: m20-010
  expression: "we don't plan to make any change"
  category: position_direct
  function: no_change_declare
  speaker_role: presenter
  difficulty: 3
  context: "we don't plan to make any change"
  note: 강한 비변경 선언. QBR에 허용되는 직접 표현.

- id: m20-011
  expression: "Hynix is not planning any making any big changes on the X"
  category: position_state
  function: no_change_soft
  speaker_role: presenter
  difficulty: 3
  context: "Hynix is not planning any making any big changes on the A-word or D-word signal layout"
  note: "big changes" - 작은 변경은 여지 남김.

- id: m20-012
  expression: "we want to make a fast consensus in the task group to make this move forward"
  category: pace_push
  function: speed_demand
  speaker_role: presenter
  difficulty: 4
  context: "we want to make a fast consensus in the task group to make this move forward"

- id: m20-013
  expression: "we need to expedite the X in order to meet our schedule"
  category: schedule_pressure
  function: urgency_create
  speaker_role: presenter
  difficulty: 4
  context: "we need to expedite the spec closure in order to meet our schedule that HomeJet presented, end of 28 or early 29"
  note: "expedite X to meet Y" - 일정 압박 공식. "hurry" 아닌 "expedite".

- id: m20-014
  expression: "to meet that schedule, we need to have X back by Y"
  category: conditional_schedule
  function: requirement_link
  speaker_role: presenter
  difficulty: 4
  context: "to meet that schedule, we need to have like some sort of like initial design targets back by second quarter of this year"

# ── 회피·포장 (Hedging & Deflection) ──
- id: m20-015
  expression: "as a name implies, it depends based on the project by project"
  category: case_by_case
  function: generic_evasion
  speaker_role: presenter
  difficulty: 4
  context: "for the custom HBM, as a name implies, it depends based on the project by project"
  note: 회피를 제품 본성으로 프레이밍. "it depends"의 가장 세련된 도입.

- id: m20-016
  expression: "it's very hard to tell you the generic timeline because [conditions]"
  category: timeline_evasion
  function: timeline_vague
  speaker_role: presenter
  difficulty: 4
  context: "it's very hard to tell you what's the generic timeline because whenever we close on the agreement and then SOW, then we need to look at also our internal resource allocation status"

- id: m20-017
  expression: "depending that situation, X will vary. Typically, [ballpark]."
  category: ballpark_after_vague
  function: vague_then_specific
  speaker_role: presenter
  difficulty: 5
  context: "depending that situation, that overall project milestone will vary. Typically, you know, from the discussion kickoff to the project launch is about two years."
  note: 회피 + 대략값 - 협조적 회피 공식. 무조건 외울 것.

- id: m20-018
  expression: "we are currently in the exploration mode on X"
  category: roadmap_vague
  function: soft_commit
  speaker_role: presenter
  difficulty: 4
  context: "we are currently in the exploration mode on the 3D like logic HBM stack"
  note: "exploration mode" - "research"보다 진지, "committed"보다 자유. 로드맵 안전어.

- id: m20-019
  expression: "we are having some internal discussions and discussion with a few partners"
  category: ongoing_dialog
  function: activity_signal
  speaker_role: presenter
  difficulty: 3
  context: "we are also having some internal discussions and having some past finding discussion with a few partners and customers"
  note: 진행 중임을 표시하되 구체 언급 회피.

- id: m20-020
  expression: "transition from X to Y will be dependent on the market situation"
  category: market_dependent
  function: transition_hedge
  speaker_role: presenter
  difficulty: 5
  context: "transition from 0A to vertical gate V1 will be dependent on the market situation at that time frame"
  note: 기술 전환 시점을 "시장 상황"에 돌려 확약 회피. 로드맵 발표자 안전망.

- id: m20-021
  expression: "it does not necessarily mean that we will X"
  category: interpretation_block
  function: expectation_correct
  speaker_role: presenter
  difficulty: 4
  context: "it does not necessarily mean that we will start mass production from 2028 on V1"
  note: 확정 해석 차단. "necessarily"가 부드럽게 만듦.

- id: m20-022
  expression: "we are actively working on X. It's going to take some time. It's not immediate."
  category: ongoing_evasion
  function: progress_acknowledge
  speaker_role: presenter
  difficulty: 4
  context: "we are actively working on getting the real logs or the memory register logs too. Once that is probably going to take some time. It's not immediate."
  note: "actively working" + "not immediate" - 진행 + 기대 낮추기.

- id: m20-023
  expression: "I don't have an exact time that we will be enabling that"
  category: time_unknown
  function: time_evasion
  speaker_role: presenter
  difficulty: 4
  context: "I don't have an exact time that we will be enabling that"
  note: "I don't know when" 대신 "I don't have an exact time" - 전문적.

- id: m20-024
  expression: "whether it could be X, could be Y, could be Z"
  category: alternative_enumerate
  function: options_scatter
  speaker_role: presenter
  difficulty: 4
  context: "Whether it could be a last level cache, could be in the controller, could be in so many places"
  note: 비용 우려를 대안 나열로 우회. 부드러운 회피.

# ── 정중한 도전 (Polite Challenge) ──
- id: m20-025
  expression: "What's the general time frame for X?"
  category: timeline_probe
  function: timeline_ask
  speaker_role: questioner
  difficulty: 3
  context: "What's the general time frame for custom HBM development?"

- id: m20-026
  expression: "What I need by that is, assuming Y, how long is Z? What would be your guidance on that?"
  category: guidance_request
  function: refined_timeline_ask
  speaker_role: questioner
  difficulty: 5
  context: "What I need by that is assuming we start engaging with SK. How long is that typical design? What would be your guidance on that?"
  note: "guidance" - 가이던스 요청. 무조건 외울 것.

- id: m20-027
  expression: "I was wondering if you guys have thought of anything like that"
  category: roadmap_probe
  function: soft_existence_ask
  speaker_role: questioner
  difficulty: 4
  context: "I was wondering if you guys have thought of anything like that"
  note: "I was wondering if" - 가장 정중한 탐색.

- id: m20-028
  expression: "You have anything on your roadmap like that or is that something you consider?"
  category: roadmap_two_step
  function: existence_consideration_ask
  speaker_role: questioner
  difficulty: 3
  context: "You have anything on your roadmap like that or. Is that something you consider?"

- id: m20-029
  expression: "are you aware of that and do you have a response to that?"
  category: awareness_response
  function: competitor_challenge
  speaker_role: questioner
  difficulty: 4
  context: "I'm just wondering, are you aware of that and do you have a response to that?"
  note: 경쟁 동향 - 인지 + 대응 이중 질문.

- id: m20-030
  expression: "What are your thoughts on X?"
  category: opinion_request
  function: thought_ask
  speaker_role: questioner
  difficulty: 3
  context: "What are your thoughts on interrupting P and then processing near memory with some separate logic die?"

- id: m20-031
  expression: "I was curious what SK's position is on that"
  category: position_request
  function: stance_ask
  speaker_role: questioner
  difficulty: 4
  context: "I was curious what SK's position is on that"
  note: "position" - "opinion"보다 격식 있는 입장 요청.

- id: m20-032
  expression: "it seemed to be some opposition at the committee meeting"
  category: observation_probe
  function: inference_state
  speaker_role: questioner
  difficulty: 4
  context: "It seemed to be some opposition at the committee meeting. You're trying to understand that a little bit more"
  note: "seemed to be" - 추측으로 입장 탐색. 단정 피함.

- id: m20-033
  expression: "this is an expensive die. And it's trying to target a market that's very cost sensitive. So the business model doesn't line up."
  category: business_challenge
  function: business_model_critique
  speaker_role: questioner
  difficulty: 5
  context: "this is an expensive die. And it's trying to target a market that's very cost sensitive. So the business model doesn't line up."
  note: 기술 비판을 비즈니스 모델 비판으로 승격. 전문적 도전.

- id: m20-034
  expression: "we're adding significant overhead to X to enable it"
  category: overhead_critique
  function: cost_critique
  speaker_role: questioner
  difficulty: 4
  context: "we're adding significant overhead to an LP6 die to enable it"

- id: m20-035
  expression: "we want to understand more if these are X issues or something that are on the Y level"
  category: cause_probe
  function: root_cause_explore
  speaker_role: questioner
  difficulty: 4
  context: "we want to understand more if these are two 3D issues or something that are on the software level or the system stack that's causing these uncorrectable error events"

- id: m20-036
  expression: "how they're going to age over time"
  category: aging_probe
  function: time_trend_ask
  speaker_role: questioner
  difficulty: 4
  context: "I also want to see understand these multi bit error trends and how they're going to age over time"
  note: "age over time" - "degrade"보다 구체적 비즈니스 영어.

- id: m20-037
  expression: "is there anything that we can do more proactively"
  category: proactive_ask
  function: action_request
  speaker_role: questioner
  difficulty: 4
  context: "if there's any concerns or anything that we can do more proactively"
  note: "more proactively" - "do more"보다 진지한 대응 요청.

- id: m20-038
  expression: "it feels like X. Maybe that's a good trade off."
  category: soft_suggestion
  function: opinion_as_tradeoff
  speaker_role: questioner
  difficulty: 5
  context: "it feels like making an off-line load in D6 with all this extra cost needed because maybe it just needs to start a year later. Maybe that's a good trade off."
  note: 의견을 제안으로 포장. "feels like" + "good trade off".

- id: m20-039
  expression: "should not now, but maybe set up some time later to try and understand from you"
  category: defer_request
  function: later_session_ask
  speaker_role: questioner
  difficulty: 4
  context: "should not now, but maybe set up some time later to try and understand from you which parameters refresh P rack etc."
  note: 복잡한 질문 - "나중에 따로"로 미루기. Type B 정상 패턴.

# ── 협상·액션 (Negotiation & Action Items) ──
- id: m20-040
  expression: "please let us know the sample demand since currently we're under the memory shortage"
  category: volume_request
  function: background_then_ask
  speaker_role: negotiator
  difficulty: 4
  context: "once you finalize the memory pure, then please let us know the sample demand since currently we're under the memory shortage"
  note: 배경 설명 → 요청. "under the memory shortage" - 상황 먼저.

- id: m20-041
  expression: "let me create the teams for me to allocate Microsoft first"
  category: priority_request
  function: first_allocation
  speaker_role: negotiator
  difficulty: 4
  context: "if you have the initial sample demand, then let me create the teams for me to allocate Microsoft first"
  note: "allocate X first" - 우선 순위 직접 요청.

- id: m20-042
  expression: "we'd be interested to discuss with you, or our X functions that might be put underneath Y"
  category: interest_express
  function: intent_signal
  speaker_role: negotiator
  difficulty: 4
  context: "we'd be interested to discuss with you, or our density compute functions that might be put underneath one of your stacks"

- id: m20-043
  expression: "maybe we can schedule a separate session to have some exploratory discussion"
  category: meeting_defer
  function: separate_session
  speaker_role: presenter
  difficulty: 4
  context: "maybe we can like a schedule a separate session to have some exploratory discussion"
  note: "separate session" - 회의 미루기 공식.

- id: m20-044
  expression: "may be a good time to bring in that material as well"
  category: timing_suggest
  function: venue_propose
  speaker_role: presenter
  difficulty: 4
  context: "we're having a cycle HBM deep dive. I don't know that may be a good time to bring in that material as well"

- id: m20-045
  expression: "once X, please let us know Y"
  category: conditional_followup
  function: action_request
  speaker_role: negotiator
  difficulty: 3
  context: "once you finalize the memory pure, then please let us know the sample demand"

- id: m20-046
  expression: "once we have the data we will start sharing it with you but right now we are limited to X"
  category: status_share
  function: current_limit
  speaker_role: presenter
  difficulty: 4
  context: "once we have the data we will start sharing it with you but right now we are limited to the system event logs for storage"

- id: m20-047
  expression: "we will be updating the target calculations moving forward"
  category: process_change
  function: methodology_update
  speaker_role: presenter
  difficulty: 4
  context: "we will be updating the target calculations moving forward from the next quarter"
  note: "moving forward" - 앞으로의 변경 명시.

- id: m20-048
  expression: "we want to track X performance also against our set target and expectations"
  category: tracking_expand
  function: scope_extend
  speaker_role: presenter
  difficulty: 3
  context: "we want to track the storage performance also against our set target and expectations"

# ── 발화 채움 표현 (Discourse Markers in Use) ──
- id: m20-049
  expression: "long story short, X"
  category: discourse_marker
  function: summary_lead
  speaker_role: presenter
  difficulty: 3
  context: "So long story short, we don't plan to make any change"
  note: "long story short" - 결론 도출. 한국어 "긴 말 짧게"의 영어 버전.

- id: m20-050
  expression: "that's where the expenses. That's where the challenge."
  category: emphasis_repeat
  function: key_point_punch
  speaker_role: questioner
  difficulty: 4
  context: "you have to do hybrid copper bonding. And so there that's where the expenses. That's where the challenge."
  note: "That's where X. That's where Y." - 반복으로 핵심 강조. 짧은 펀치라인.
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2026-03-12 08 35 58_EN_MSFTQTR-extracted.wav` (총 약 30분, 3,164단어)
추천 발췌 5구간 (월~금 순회용). 각 구간 1-2분 내외.

| # | 시간대(추정) | line 범위 | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:--|:---|:---|:--:|
| 1 | 도입 - HBM 커스텀 타임라인 | line 6-21 | MSFT "general time frame" 질문 → SKH "as a name implies, it depends" 회피 + "typically about two years" | Type B 회피+대략값 공식 | ★★★★ |
| 2 | 3D-stacked HBM 로드맵 탐색 | line 22-47 | MSFT "I was wondering if you have anything on your roadmap" → SKH "exploration mode" + "separate session" 미루기 | 정중 탐색 + 회피 + 별도 세션 | ★★★★ |
| 3 | HBM5 bump metrics 스펙 클로저 | line 68-88 | SKH "we don't plan to make any change" + "drive consensus by end of this month" + "key items to close by end of Q2" | 스펙 pushback + 마감 일정 언어 | ★★★ |
| 4 | CXL CMM 로드맵 발표 | line 107-129 | SKH "we are targeting our second generation" + "EVP and ES targeting this year" + double PCB 밀도 확장 | 타임라인 타깃 + 마일스톤 | ★★★ |
| 5 | DRAM 로드맵 6F² → 4F² → 3D DRAM | line 138-195 | SKH "we plan to extend X to Y by Z" + "market dependent transition" + MSFT "set up some time later" + "good trade off" | 로드맵 확약 회피 + ROI 협상 | ★★★★★ |

**사용법**:
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 1, 5가 가장 가치 높음 - 회피/협상 화법이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **QBR (Quarterly Business Review)** 레지스터다. 정기 비즈니스 리뷰 - 분기별로 진행, 로드맵·공급·품질을 점검. Type A(기술 deep-dive)와의 차이:
- **Type A**: 한 발표자가 길게 발표, 청중이 기술 도전 → 설명 설계 + defense
- **Type B**: 여러 발표자가 차례로 micro-presentation, 상대가 타임라인/볼륨/스펙 질문 → 협상 + 마일스톤

QBR의 언어는 "targeting", "by end of Q2", "close", "consensus", "expedite", "dependent on" - 모두 **일정과 합의** 중심.

### Pragmatics (화용론) 핵심
1. **"targeting"이 "will"을 대신**: Type B에서는 "we will do X by Y"가 위험. "we are targeting X by Y"가 안전 - 목표임을 명시하되 약속은 회피. QBR에서 가장 많이 쓰는 동사.
2. **"close"가 "complete"을 대신**: 스펙 합의는 "complete"가 아니라 "close". "close the discussion", "close the spec", "close the item" - 모두 합의 완료의 뉘앙스. "complete"는 작업 완료, "close"는 합의 완료.
3. **"exploration mode"가 "research"를 대신**: 로드맵에서 "research"는 너무 가볍고 "committed"는 너무 강함. "exploration mode"가 안전. "we are in the exploration mode on X" - 로드맵 발표자의 안전망.
4. **"as a name implies, it depends"**: 회피를 제품 본성으로 프레이밍. "it depends"를 그냥 쓰면 약해 보이지만, "as a name implies"로 시작하면 - "이 제품이 원래 그런 것" - 회피가 아니라 설명이 됨.
5. **"dependent on the market situation"**: 기술 전환 시점 확약 회피의 핵심. "우리가 정하는 게 아니라 시장이 정한다" - 기술 부식체가 아니라 비즈니스 판단체로 프레이밍.

### 네가 당장 써야 할 Top 5
1. **"we are targeting X by Y"** - 타임라인 타깃. "will" 대신 무조건 이것.
2. **"as a name implies, it depends... typically, [ballpark]"** - 회피 + 대략값.
3. **"What would be your guidance on that?"** - 일정 물을 때.
4. **"from our perspective, X is the optimal way"** - 스펙 입장 명시.
5. **"maybe we can schedule a separate session"** - 회의 미루기.

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "목표로 하고 있습니다" | "we are targeting X by Y" | "will"은 약속, "targeting"은 목표 |
| "검토 중입니다" | "we are in the exploration mode on X" | "research"보다 진지 |
| "시장 상황을 보겠습니다" | "transition will be dependent on the market situation" | 비즈니스 판단으로 프레이밍 |
| "확정된 건 없습니다" | "the schedule is not fixed yet" | "yet"로 여지 남김 |
| "합의를 끝내야 합니다" | "we need to close the X by end of Q2" | "close" - 합의 완료 |
| "빨리 합시다" | "we need to expedite the closure" | "hurry" 아닌 "expedite" |
| "나중에 다시 얘기하자" | "maybe we can schedule a separate session" | "나중에" 대신 "별도 세션" |
| "가이던스를 주십시오" | "What would be your guidance on that?" | "How long" 대신 "guidance" |
| "그건 비용이 문제입니다" | "the business model doesn't line up" | 비용 비판 → 비즈니스 모델 비판 |
| "좀 더 적극적으로 해주세요" | "anything that we can do more proactively" | "do more"보다 진지 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 50개 표현 중, 8절 Top 5부터 우선 숙지
3. **Type B 특화 학습**: 이 교재는 Type B(로드맵/공급 alignment) 특화. 타임라인, 볼륨, 스펙 협상 언어에 집중
4. **비교 학습**: 8절 한국어-영어 비교표로 QBR 화법 차이 체득
5. **QBR 시나리오 대비**: 다음 분기 QBR 전, 발췌 1(회피)과 발췌 5(ROI 협상)를 집중 shadowing
6. **Audrey 금요일 교정**: 6절의 회피·협상 표현을 중심으로 dump 작성

---

*Textbook 20 - MSFTQTR (2026-03-12). 회의 유형 B (로드맵/공급 alignment). 표현 DB 50개. 5개 발췌 구간. 작성: 2026-09-01.*
