---
essence_id: E-A
type: A
type_name: "기술 Deep-dive (Technical Deep-dive)"
source_textbooks: [01, 07, 09, 11, 25, 26, 32, 34, 36]
source_count: 9
total_source_db_entries: 494
master_db_entries: 50
created: 2026-09-02
audrey_channel: "Friday pragmatic-correction (dump channel)"
status: active
---

# Essence E-A: 기술 Deep-dive (Technical Deep-dive)

> 단일 회의 교재가 아니다. 9개 Type-A 교재(01 Marvell PFMA, 07 MSFT CXlpooling,
> 09 Penguin, 11 Dell TDF, 25 IBM, 26 Montage Switchless, 32 Intel,
> 34 AMD CXL Sync, 36 Google)의 표현 DB 494개 엔트리를 증류한 마스터 참조서.
> 발표자 아키텍처(편향된 제품/아키텍처 피치 + Q&A 방어)와 회피/전환 전략,
> 정중한 도전 패턴에 집중.

---

## 1. 유형의 본질 (Essence of Type A)

Type-A 회의는 **한쪽이 피치하고 상대가 기술적으로 검증·도전하는 비대칭 구조**다.
양측 모두 기술 전문가이지만, 발표자는 "설득의 시간"을 가지고 질문자는
"검증의 시간"을 가진다. 발표자는 고정된 아키텍처(보통 5-6단계)로 제품의
문제 프레이밍 → 솔루션 공개 → 스펙 심화 → 질문 초대 → 다음 단계 제안
사이클을 회전시킨다. 질문자는 발표자의 아키텍처 안으로 들어가
이해 확인 → 제약 탐색 → 가설 제안 → 다음 단계 요구 패턴으로 검증한다.

이 유형의 진짜 학습 가치는 **회피·포장 화법**과 **정중한 도전 화법**에 있다.
발표자는 제약·경쟁·책임·일정 불확실성을 정중하게 포장하고, 질문자는
도전을 "확인"으로 위장하며 메커니즘과 의사결정 정보를 캐낸다.

Type B(협상/의사결정)와의 차이: Type-A는 기술 타당성이 의사결정의
전제이므로, 설득과 검증이 회의의 본질이다. 가격·공급 합의는 부수적이다.
Type C(정보 수집/인텔리전스)와의 차이: Type-A는 한쪽이 명확히
솔루션을 들고 나온다. 양측이 모두 "탐색 중"인 C와 다르다.
Type D(브리핑/상태 보고)와의 차이: Type-A는 Q&A 방어가 핵심이다.
단방향 보고인 D와 달리 양방향 검증이 설계되어 있다.

---

## 2. 화자 아키텍처 정수 (Speaker Architecture)

9개 교재에서 반복되는 발표자 구조. 파트너 유형에 따라 변형이 있지만
뼈대는 동일하다.

### Move 1: 문제 프레이밍 (Problem Framing)
발표자는 기능 소개 전 제약이나 업계 공통 문제를 먼저 설정한다.
- "we feel that X is now the hardest problem in Y" (01)
- "However, there are very significant X concerns with Y" (36)

### Move 2: 솔루션 공개 (Solution Reveal)
제약을 솔루션으로 전환하는 공식. "solve" 대신 세련된 동사 사용.
- "So for that, X has what we call the Y" (01)
- "And the way we get around that restriction on this device is X" (36)

### Move 3: 차별성 명시 (Differentiation)
자사 가치를 대비 구조로 강조. 범용 vs 독점, 용량 vs 신뢰성 등.
- "X will be available to anyone. But the Y exclusive feature here is Z" (36)
- "From the X perspective, Y offers twice the capacity of Z" (11)

### Move 4: 스펙 심화 (Spec Deep-dive)
기능-이유-제약-솔루션 4단 설명. "compelling because"로 가치 연결.
- "And this is compelling because it can give us X" (36)
- "this is one of the things that we do that is gonna give us significantly higher X" (36)

### Move 5: 질문 초대 + 범위 좁히기 (Question Invitation + Scope Narrowing)
질문을 받으면 즉시 용어 범위를 좁힌다. "What do you mean?"은 금지.
- "When you say X, I'm not sure that I know, are you talking about A, B, or C?" (36)
- "Just to make sure I understand correctly" (01)

### Move 6: 다음 단계 제안 (Next-Step Proposal)
회의 마무리에 "누가, 뭘, 언제"를 명시. 정중한 과제 부여 공식.
- "I think we should set up a three way discussion with X" (36)
- "I think the best way would be for X to come back and let us know Y" (36)

### Move 7: 책임 소재 명시 (Responsibility Redirect)
모르는 것은 솔직히 인정하되 "I don't know"는 쓰지 않는다.
- "That's something you should get from Marvell" (36)
- "I think it's probably something that you want to talk to X about" (36)

---

## 3. 핵심 전략 정수 (Core Strategies)

### 전략 1: 제약을 솔루션으로 재프레이밍 (Constraint-as-Solution)
"we lost X"는 절대 금지. "We are taking advantage of that to do Y"로
손실을 활용으로 전환. 발표자의 가장 강력한 무기.
- "X could have been Y. But instead we are taking advantage of that to do Z" (36)
- "Even if we consider X, the Y remains the same" (11)

### 전략 2: 정중한 불가능 (Polite Impossibility)
"That's useless"는 공격적. "I can't imagine"로 자기 인지 한계로 포장.
- "X is possible, but I can't imagine a scenario where that would be useful" (36)
- "I don't see any reason why that would not continue" (25)

### 전략 3: 내부 논의 단계 표시 (Internal Discussion Phase)
확정 못 함을 솔직히 밝히되, 단계를 명시해 가능성을 열어둔다.
- "it is still an internal discussion phase, so I cannot show the details" (25)
- "still in planning" (26)
- "between Jenny and myself, we don't really have anything official" (32)

### 전략 4: POR 헤지 (POR Hedge)
Plan of Record 미확정을 연속적 헤지 래더로 표현.
- "we don't have our POR aligned" → "we don't have a POR yet. We don't have a commit yet" (32)
- "we're hoping to make our POR decision for X around end of Y" (32)

### 전략 5: 브레인스톰 마커 (Brainstorm Markers)
생각 중임을 명시해 거절 가능성을 열어둔다.
- "I'm thinking aloud here, so I am going to say garbage here for a minute" (34)
- "Just for the conversation purposes, let's say X is Y" (34)

### 전략 6: 정밀도 부인 (Precision Disclaimer)
정확한 수치/체계를 못 주는 상황에서 대략적 범위로 답.
- "I can get you the breakdown, but X is about Y" (01)
- "I'm not confident in any of the answers I'm giving here" (25)
- "I don't know how much I can share honestly, but at the highest level" (07)

### 전략 7: 동의 후 도전 (Agree-then-Challenge)
먼저 동의나 추적을 표시하고 "but"로 도전으로 전환.
- "I also have a similar opinion. But X told me Y" (26)
- "Thank you for your presentation today, but I'd like to ask X" (36)
- "That's going to be wrong from the X perspective also. That's all I'm trying to say" (34)

### 전략 8: 공격 무장 해제 (Attack Disarm)
어려운 질문을 부드럽게 받아치며 상대의 공격 의도를 무력화.
- "So sorry, I followed you till the last point. Why do you think X?" (34)
- "So sorry, I followed you till the last point" - 추적 했음을 먼저 인정

---

## 4. 마스터 표현 DB (Master Expression Database)

9개 교재 494개 엔트리에서 증류한 50개. 우선순위: 낮은 빈도 + 높은 구조적 가치.
2개 이상 교재에서 반복되는 패턴, Type-A 고유 시그니처 무브 포함.

```yaml
# ── 발표 설계 (Presentation Architecture) ──
- id: ex-001
  expression: "Anyway, let me push on to the next feature."
  function: speaker_control
  sources: [36]
  difficulty: 3
  note: "move on" 보다 능동적인 "push on" - 발표자 주도권 유지

- id: ex-002
  expression: "And then I just have one more feature and that is X"
  function: final_preview
  sources: [36]
  difficulty: 3
  note: "one more"로 마지막임 예고 - 청중 집중 유도

- id: ex-003
  expression: "And this is compelling because it can give us X"
  function: benefit_stating
  sources: [36, 11]
  difficulty: 4
  note: 기능-가치 연결 공식. "이 기능은 X because Y" 한 문장 구조

- id: ex-004
  expression: "we feel that X is now the hardest problem in Y"
  function: problem_escalation
  sources: [01]
  difficulty: 5
  note: 업계 공통 문제를 무겁게 프레이밍 - 솔루션 등장 정당화

- id: ex-005
  expression: "So for that, X has what we call the Y"
  function: solution_reveal
  sources: [01]
  difficulty: 4
  note: "we call" - 자사 명명으로 솔루션 주권 표시

- id: ex-006
  expression: "And the way we get around that restriction on this device is X"
  function: constraint_solution
  sources: [36]
  difficulty: 5
  note: "get around that restriction" - "solve" 보다 세련된 제약 해결 공식

- id: ex-007
  expression: "X will be available to anyone. But the Y exclusive feature here is Z"
  function: commodity_vs_exclusive
  sources: [36, 34]
  difficulty: 5
  note: "anyone vs exclusive" 대비 - 차별성 명시. AMD/SK 회의에서도 변형 사용

- id: ex-008
  expression: "this is one of the things that we do that is gonna give us significantly higher X"
  function: value_emphasis
  sources: [36]
  difficulty: 4
  note: "one of the things we do" - 자사 가치 함축

- id: ex-009
  expression: "From the X perspective, Y offers twice the capacity of Z"
  function: comparison_framing
  sources: [11]
  difficulty: 4
  note: "From X perspective"로 비교의 한계를 전제하며 우위 강조

- id: ex-010
  expression: "Even if we consider X, the Y remains the same"
  function: concession_framing
  sources: [11]
  note: 양보 전제 후 결론 유지 - 반론 방어

# ── 회피·포장 (Hedging & Deflection) ──
- id: ex-011
  expression: "X could have been Y. But instead we are taking advantage of that to do Z."
  function: constraint_reframe
  sources: [36]
  difficulty: 5
  note: 가장 강력한 재프레이밍. "잃은 게 아니라 활용한 것이다"

- id: ex-012
  expression: "We're not going to want terribly X, right? even with Y."
  function: floor_setting
  sources: [36]
  difficulty: 5
  note: "terribly" 부정문에서 "터무니없이" - 품질 하한선 설정

- id: ex-013
  expression: "So it's gonna be a space where we're going to expect X"
  function: floor_expression
  sources: [36]
  difficulty: 4
  note: "거절"을 "space"로 포장 - 가능성 열고 조건 단다

- id: ex-014
  expression: "X is possible, but I can't imagine a scenario where that would be useful."
  function: soft_negation
  sources: [36]
  difficulty: 5
  note: "useless" 대신 "can't imagine useful scenario" - 자기 인지 한계로 포장

- id: ex-015
  expression: "you could even imagine a scenario where X"
  function: scenario_invite
  sources: [36, 09]
  difficulty: 4
  note: 청중을 가설 시나리오로 초대 - 설득적 부드러움

- id: ex-016
  expression: "we could imagine still using X in some configuration on this card"
  function: possibility_open
  sources: [36]
  difficulty: 4
  note: "we could do X" 보다 "we could imagine using X" 가 부드러움

- id: ex-017
  expression: "the variable capacity is, is absolutely a drawback of using X"
  function: honest_limit
  sources: [36]
  difficulty: 4
  note: "absolutely a drawback" - 솔직한 한계 인정이 신뢰를 만듦

- id: ex-018
  expression: "It is a necessary evil that the host has to be able to deal with X"
  function: necessary_evil_framing
  sources: [36]
  difficulty: 5
  note: "necessary evil" 관용구 - 불가피한 제약 인정

- id: ex-019
  expression: "I keep saying X because it's very important that Y"
  function: importance_flag
  sources: [36]
  difficulty: 4
  note: 반복의 정당화 - 강조 표현

- id: ex-020
  expression: "That is the beauty of it."
  function: feature_celebration
  sources: [36]
  difficulty: 3
  note: "beauty of it" - 장점 강조 관용구

- id: ex-021
  expression: "it is still an internal discussion phase, so I cannot show the details"
  function: internal_phase
  sources: [25, 26]
  difficulty: 4
  note: "still in planning" 과 변형. 25/26 모두 비원어민 발화자가 사용

- id: ex-022
  expression: "between X and myself, we don't really have anything official"
  function: informal_status
  sources: [32]
  difficulty: 4
  note: "between X and myself" - 비공식 상태를 인물 쌍으로 표현

- id: ex-023
  expression: "we don't have a POR yet. We don't have a commit yet."
  function: por_hedge
  sources: [32]
  difficulty: 5
  note: Intel 시그니처. POR + commit 이중 부인

- id: ex-024
  expression: "we're hoping to make our POR decision for X around end of Y"
  function: schedule_tentative
  sources: [32]
  difficulty: 4
  note: "hoping" + "around" - 이중 헤지로 일정 유연성 확보

- id: ex-025
  expression: "the trend today is that our future product will probably have, we hope, X"
  function: trend_hedge
  sources: [32]
  difficulty: 5
  note: "probably" + "we hope" 이중 헤지 - 미래 제품 스펙 회피

- id: ex-026
  expression: "I'm thinking aloud here, so I am going to say garbage here for a minute"
  function: brainstorm_marker
  sources: [34]
  difficulty: 5
  note: AMD 시그니처. "garbage"로 거절 가능성 사전 차단

- id: ex-027
  expression: "Just for the conversation purposes, let's say X is Y"
  function: hypothetical_setup
  sources: [34]
  difficulty: 4
  note: 가설 전제 - 실제 약속과 구분

- id: ex-028
  expression: "I can get you the breakdown, but X is about Y"
  function: precision_disclaimer
  sources: [01, 07]
  difficulty: 4
  note: 정확한 수치 못 줄 때 대략 범위로 답

- id: ex-029
  expression: "I don't know how much I can share honestly, but at the highest level"
  function: hierarchical_disclosure
  sources: [07]
  difficulty: 5
  note: 공개 한계를 먼저 밝히고 high-level 만 제공

- id: ex-030
  expression: "I'm not confident in any of the answers I'm giving here"
  function: meta_hedge
  sources: [25]
  difficulty: 5
  note: 자신의 모든 답을 meta 수준에서 부인. IBM 시그니처

- id: ex-031
  expression: "I'm not sure we can compare the Apple to Apple, but we will calculate"
  function: comparison_caveat
  sources: [25]
  difficulty: 4
  note: 비교 불가능함을 전제하되 계산은 시도하겠다는 타협

- id: ex-032
  expression: "if I had to say right now, I would say X"
  function: tentative_answer
  sources: [36]
  difficulty: 4
  note: 임시 답변 표시 - 확정 없이 답을 줄 때

- id: ex-033
  expression: "you're moving the problem, you're not solving the problem"
  function: problem_displacement
  sources: [34]
  difficulty: 5
  note: 상대 솔루션이 문제를 옮길 뿐이라는 도전. AMD 시그니처

# ── 정중한 도전 (Polite Challenge) ──
- id: ex-034
  expression: "Just to make sure I understand correctly"
  function: comprehension_check
  sources: [01, 25, 34]
  difficulty: 4
  note: 3개 교재 반복. 질문 전 확인 전제. 가장 유용한 정중 질문 화법

- id: ex-035
  expression: "If I understand you correctly."
  function: polite_preface
  sources: [36, 25]
  difficulty: 4
  note: ex-034 의 축약형. 한 줄로 질문을 "확인"으로 위장

- id: ex-036
  expression: "When you say X, I'm not sure that I know, are you talking about A, B, or C?"
  function: scope_narrowing
  sources: [36]
  difficulty: 5
  note: "What do you mean?" 대신 정중한 범위 좁히기

- id: ex-037
  expression: "are we talking about X, are we talking about Y, are we talking about Z?"
  function: checklist_repeat
  sources: [36]
  difficulty: 4
  note: 3-4회 반복으로 질문자가 자체 정리하도록 유도

- id: ex-038
  expression: "have you looked at the trade-offs between X versus Y in terms of Z?"
  function: trade_off_probe
  sources: [07, 36]
  difficulty: 5
  note: 2개 교재. 트레이드오프 탐색 - 결정 정보 캐내기

- id: ex-039
  expression: "the reason I'm asking is"
  function: reason_prefacing
  sources: [07]
  difficulty: 4
  note: 질문 의도를 먼저 밝혀 도전을 완화

- id: ex-040
  expression: "So sorry, I followed you till the last point. Why do you think X?"
  function: attack_disarm
  sources: [34]
  difficulty: 5
  note: 추적 했음을 먼저 인정하고 도전. AMD 시그니처

- id: ex-041
  expression: "Are you guaranteed that X, or does that have Y?"
  function: binary_challenge
  sources: [09, 36]
  difficulty: 4
  note: "A or B" 선택지 질문으로 답 범위 좁히기

- id: ex-042
  expression: "I also have a similar opinion. But X told me Y"
  function: agree_then_challenge
  sources: [26]
  difficulty: 5
  note: 한국식 정중 도전. 동의 후 제3자 권위로 도전

- id: ex-043
  expression: "That's going to be wrong from the X perspective also. That's all I'm trying to say."
  function: perspective_challenge
  sources: [34]
  difficulty: 5
  note: 공격이 아닌 "관점" 표현으로 포장. "all I'm trying to say" 로 의도 축소

- id: ex-044
  expression: "Thank you for your presentation today, but I'd like to ask X"
  function: thank_then_challenge
  sources: [36, 11]
  difficulty: 4
  note: 감사 후 "but" 로 도전 전환

- id: ex-045
  expression: "if there is a way where X could be Y, that would be a lot more Z"
  function: possibility_proposal
  sources: [07, 09, 25]
  difficulty: 5
  note: 3개 교재. 제안을 "if there is a way" 로 부드럽게

- id: ex-046
  expression: "it's not a stretch to think that we could X"
  function: feasibility_claim
  sources: [09]
  difficulty: 4
  note: "not a stretch" - 가능성을 겸손하게 주장

- id: ex-047
  expression: "perhaps you might be able to X with Y anyways, right?"
  function: workaround_suggest
  sources: [34]
  difficulty: 4
  note: "perhaps" + "might" + "anyways" + "right?" 4중 헤지 제안

# ── 협상·액션 (Negotiation & Action) ──
- id: ex-048
  expression: "we can definitely discuss it for next generation"
  function: next_gen_deferral
  sources: [01]
  difficulty: 4
  note: 거절을 "차세대 논의" 로 연착. Type-A 시그니처

- id: ex-049
  expression: "I think the best way would be for X to come back and let us know Y"
  function: polite_directive
  sources: [36]
  difficulty: 5
  note: "you should" 대신 "the best way would be" - 정중한 지시

- id: ex-050
  expression: "I think X should go off and think about Y and come back and let us know"
  function: action_item_assignment
  sources: [36]
  difficulty: 5
  note: "go off and think about" - 정중한 과제 부여 공식
```

---

## 5. 영역 어휘 정수 (Domain Vocabulary)

CXL/AI 메모리/반도체 협상 맥락에서 9개 교재에 반복 출현하는 용어.

### CXL 프로토콜 & 아키텍처
- **CXL 2.0/3.1/4.0**: 버전별 기능 차이. 3.1부터 switchless/multi-head 강화
- **switchless**: 스위치 없이 직접 연결하는 CXL 토폴로지 (26, 34)
- **multi-head**: 단일 메모리를 다수 호스트가 공유 (34)
- **CXL pool**: CXL 로 공유되는 메모리 풀 (07, 36)
- **free list**: 풀의 가용 용량 목록 (36)
- **RDMA**: 원격 직접 메모리 접근 (07, 34)
- **KV cache**: 키-값 캐시 패턴 (07)

### 메모리/디바이스
- **DDR5 / DDR4**: 차세대/구세대 DRAM 표준. DDR5 가 ECC 비트 더 많음 (36)
- **EDSFF**: 서버 폼팩터 (01, 11)
- **graded DRAM**: 등급별 분류 DRAM. 품질 차등 (36)
- **DIMM**: 듀얼 인라인 메모리 모듈 (36)
- **double chip kill**: 칩 2개 연속 불량 허용 ECC (36)
- **chunk size**: ECC 단위 데이터 크기 (36)
- **PFMA**: Marvell 프로그래머블 메모리 아키텍처 (01)
- **photonic interposer**: 광 인터포저 (01)
- **radix**: 스위치 패브릭 토폴로지 (01)

### 압축/보안
- **on the fly dictionary**: 런타임 실시간 생성 압축 사전 (36)
- **numeric compression**: 수치 데이터 최적화 압축 (36)
- **entropy encoding**: Huffman 등 엔트로피 기반 인코딩 (36)
- **LZ4**: 무손실 압축 알고리즘 (36)
- **PII**: 개인 식별 정보 (36)
- **SNU filter**: 정렬 뉴럴 유닛 필터 (01)

### 비즈니스/공급망
- **POR (Plan of Record)**: 확정 제품 계획. Intel 시그니처 (32)
- **dual source / single source**: 이중/단일 공급처 (36)
- **JDM (Joint Design Manufacturer)**: 공동 설계 제조사 (36)
- **TCO**: 총 소유 비용 (01, 11)
- **ES/CS/MP**: 엔지니어링 샘플/고객 샘플/양산 (11, 26)
- **DPM (Defects Per Million)**: 백만당 결함 수 (36)
- **fall out**: 불량 발생 (36)
- **three way discussion**: 3자 회의 (36)
- **FAU**: 팹릭 어셈블리 유닛 (01)
- **BI**: 버스트 인터리빙 (01)
- **TDF**: 기술 결의 파일 (Dell 시그니처, 11)

---

## 6. 주간 학습 경로 (Weekly Learning Path)

5일 Mon-Fri 회전. 각 날짜별 1개 교재 집중 + 발췌 shadowing + 표현 DB 10개.

### 월요일: Marvell PFMA (textbook 01)
- 발표자 아키텍처의 정석. 6단계 구조 학습.
- 발췌: Ravi 의 "we feel that X is the hardest problem in Y" 문제 프레이밍
- 표현 DB: ex-004, ex-005, ex-028, ex-034, ex-048 외 5개 (01 출처)

### 화요일: MSFT CXL Pooling (textbook 07)
- 질문자 아키텍처. SK 의 4단계 발표 + MS 의 3단계 질문.
- 발췌: "have you looked at the trade-offs between X versus Y in terms of Z?"
- 표현 DB: ex-029, ex-038, ex-039, ex-045 외 5개 (07 출처)

### 수요일: Penguin (textbook 09)
- 재해석·비교·추론 화법. Andy 의 5단계.
- 발췌: "in a weird way, this would be conceptually similar to X, except that Y"
- 표현 DB: ex-015, ex-041, ex-046 외 7개 (09 출처)

### 목요일: Dell TDF (textbook 11) + Montage Switchless (textbook 26)
- 비원어민 발표자의 정중 도전. 한국식 "agree-then-challenge" 학습.
- 발췌: "Frankly speaking, it's not easy to provide any feedback" + "I also have a similar opinion. But X told me Y"
- 표현 DB: ex-010, ex-042 외 8개 (11, 26 출처)

### 금요일: Intel (textbook 32) + AMD (textbook 34) + Google (textbook 36)
- 헤지 래더(32) + 브레인스톤 마커(34) + 재프레이밍(36) 종합 복습.
- 발췌: "we don't have our POR yet" → "I'm thinking aloud, garbage for a minute" → "X could have been Y. But instead we are taking advantage of that to do Z"
- 표현 DB: ex-011, ex-023, ex-026, ex-033, ex-040, ex-049 외 4개

---

## 7. Audrey 금요일 교정 노트 (Friday Correction Notes)

금요일 dump 채널에서 집중 교정할 Top 8 표현. 한국어 화법 간섭이 가장 큰 항목.

### 1. "Just to make sure I understand correctly"
한국어 간섭: "확인하려고 합니다" 직역 회피. Audrey 교정: 반드시 문장 맨 앞에, 그리고 질문 전 한 줄로.

### 2. "X could have been Y. But instead we are taking advantage of that to do Z."
한국어 간섭: "손해봤습니다" 솔직 인정. Audrey 교정: 제약은 "taking advantage of" 로 재프레이밍.

### 3. "I can't imagine a scenario where that would be useful."
한국어 간섭: "쓸모없습니다" 직설. Audrey 교정: 자기 인지 한계로 포장.

### 4. "When you say X, I'm not sure I know, are you talking about A, B, or C?"
한국어 간섭: "무슨 말인지 모르겠습니다". Audrey 교정: "What do you mean?" 금지. 범위 좁히기.

### 5. "That's something you should get from X."
한국어 간섭: "모르겠습니다". Audrey 교정: "I don't know" 금지. 책임 주체 명시.

### 6. "I think the best way would be for X to come back and let us know Y."
한국어 간섭: "X 가 Y 해야 합니다" 직역. Audrey 교정: "you should" 금지. "the best way would be".

### 7. "it is still an internal discussion phase, so I cannot show the details"
한국어 간섭: "내부 논의 중입니다" 직역. Audrey 교정: "phase" 로 단계 명시, "cannot show" 로 한계 명시.

### 8. "you're moving the problem, you're not solving the problem"
한국어 간섭: "문제를 해결하는 게 아니라 옮기는 겁니다". Audrey 교정: "moving the problem" - 문제 이동 비유.

---

## 8. 한계와 신뢰도 (Limitations & Reliability)

### 신뢰도 높음 (3+ 교재 반복 검증)
- "Just to make sure I understand correctly" (01, 25, 34)
- "if there is a way where X could be Y" (07, 09, 25)
- "trade-off between X and Y" (07, 36)
- "Thank you for X, but I'd like to ask Y" (11, 36)
- "still in planning" / "internal discussion phase" (25, 26)
- "anyone vs exclusive" 대비 구조 (34, 36)

### 신뢰도 중간 (2 교재 또는 강한 맥락 유사)
- "if I had to say right now" (36, 32 유사)
- "Are you guaranteed that X, or does that have Y?" (09, 36)
- 비원어민 발화자의 "I also have a similar opinion. But" (26, 25 유사)

### 신뢰도 낮음 (단일 교재 시그니처 - 맥락 의존)
- AMD 시그니처 "thinking aloud / garbage mode" (34) - AMD 문화 특수. 범용 적용 시 주의.
- Intel 시그니처 "POR" 헤지 래더 (32) - Intel 의 결의 문화 특수. 타사엔 어색.
- Marvell "hardest problem in Y" 프레이밍 (01) - Ravi 개인 스타일. 과용 금지.
- Dell "TDF in August. Is that your expectation?" (11) - Dell 의 특수 일정 용어.

### 코퍼스 한계
1. 9개 교재 모두 SK Hynix 시점이다. 파트너사 발표자 화법은 간접 관찰.
   발표자 화법을 실제로 쓰려면 추가 역할귬 연습 필요.
2. 비원어민 발화자 자료(25 IBM Patrick, 26 Montage, 09 Penguin Andy,
   34 AMD SK 측)는 한국어 간섭이 일부 포함. 원어민 화법과 분리 학습 권장.
3. 494개 소스 엔트리에서 50개로 압축. 빈도 우선이 아닌 구조적 가치 우선.
   발화 빈도가 높은 단순 표현("I see", "Okay, I see")은 의도적으로 제외.
4. 모든 회의가 CXL/AI 메모리 도메인. 타 도메인(네트워킹, 스토리지, 소프트웨어)
   적용 시 도메인 어휘는 교체 필요.
5. 작성 시점 2026-09-02. 언어 사용 패턴은 2025-06 ~ 2026-08 회의 기반.
   시대 변화에 따른 화법 진화 가능.

---

*Essence E-A. 9개 Type-A 교재 494 엔트리에서 50개로 증류. 작성 2026-09-02.
Audrey 금요일 교정 채널과 함께 사용. em-dash 미사용. forward-slash 경로.*
