---
essence_id: E-B
type: B
type_name: Roadmap/Supply 정합 (Roadmap & Supply Alignment)
source_textbooks: [02, 03, 04, 06, 15, 16, 17, 18, 20, 21, 22, 23, 24, 31, 35, 37]
source_count: 16
total_db_entries_distilled: 60
created: 2026-09-02
audrey: Friday pragmatic-correction channel
---

# Essence Volume E-B: Roadmap / Supply 정합 (16권 정수)

> 16권의 Type B 회의 교재에서 공통으로 재등장하는 패턴을 압축한 마스터 참고서.
> Steve가 임의의 partner roadmap / supply 회의에 들어가기 전 1차로 봐야 할 단일 출처.
> em-dash 금지 - hyphen only.

---

## S1. 유형의 본질 (What defines this meeting type)

Type B 회의는 "기술 발표"가 아니라 **"양사 로드맵·일정·용량·스펙 타겟을 맞추는 정합(alignment) 회의"**다. 한쪽이 발표하고 한쪽이 듣는 구조가 아니다. 양쪽이 각자의 로드맵을 깔고, 마찰점(items that seem odd, not aligned, biggest challenge)을 찾아, 타협점(workable, feasible, in flux)을 조율하는 구조다. 발화의 단위는 "설명"이 아니라 "negotiation turn" - opening position, counter, constraint reveal, compromise probe, action item의 5-move 사이클이 반복된다.

Steve의 역할은 대개 **responder + negotiator**다. Steve는 SK 로드맵을 발표하거나(ref: 02, 04, 15, 17, 20, 22, 23, 35), 파트너 로드맵에 도전하거나(ref: 06, 16), 공급 제약을 방어하거나(ref: 23, 24, 37) 한다. 파트너(NVIDIA, Qualcomm, AMD, AWS, HPE, MSFT, Marvell, Lenovo, Scaleflux)의 typical stance는 "당겨라(pull in), 더 내놔라(volume), 이 스펙 가능한가(spec probe), 왜 안 되는가(reason challenge)"다. 감정·실용 register는 Type A보다 **덜 기술적이고 더 비즈니스적**이다 - "time to market", "fair share", "incumbent", "POR", "under consideration" 같은 비즈니스 어휘가 핵심. 감정 표현("my blood is boiling", "I beg you")은 AMD Joe 극단 케이스에서만 허용되며, 일반적으로는 concern / confusion / worry / surprise로 포장된다.

Type A(기술 deep-dive)는 발표자가 설명하고 질문자가 기술 검증하는 단방향 구조지만, Type B는 양쪽이 동시에 로드맵을 깔고 조율하는 양방향 구조. Type C(샘플/일정 조율)는 단기 sample 수량·시점에 집중하지만, Type B는 **다년 로드맵·전략적 정렬**까지 다룬다 (B ⊃ C의 상위 집합). Type D(이슈/품질 디버깅)는 과거 결함을 원인 분석하지만, Type B는 미래 일정을 맞추는 forward-looking 협상이다.

---

## S2. 화자 아키텍처 정수 (Speaker architecture across this type)

16권 전체에서 재등장하는 negotiation turn 구조는 **5-7 move 사이클**이다. 각 move마다 고정 화법 공식이 있다.

### Move 1: 맥락으로 열기 (Context Opening)

Type B 회의는 "우리 제품"이나 "우리 요구"로 시작하지 않는다. **"고객 수요"** 또는 **"시장 상황"**으로 시작한다. 이게 정합 회의의 첫 뼈대.

- `Multiple customers started to show a strong interest in X as well as Y` (03, 06) - 고객 수요로 열기
- `Starting in Q4 last year, we have seen a dramatic acceleration in X` (24) - 시장 상황으로 열기
- `as you guys are familiar with the X, I think there are a few changes` (15, 17) - 과거 합의 회상 + 변경 신호
- `the all the contents is all the same except X` (22) - 분기 로드맵의 "변경점 단일화"

### Move 2: 타겟·타임라인 명시 (Target Timeline)

제안마다 구체 분기·시점을 명시. "내년쯤"이 아니라 "2027 Q1-Q2"로.

- `we are targeting X by Y timeframe` (04, 20, 22) - "targeting" + "timeframe"이 Type B 기본 동사
- `we plan to have X, so the timeline would be Y` (04) - 타임라인 명시 공식
- `It is slated for X at Y` (15) - "slated for" = 확정 일정
- `CSA in Q3, ES in December, CS in February` (18) - 샘플 단계와 시점 짝지어 말하기

### Move 3: 제약 공개 (Constraint Reveal)

타겟을 말하되, 즉시 한계를 인정하거나 조건을 건다. 이게 정합 회의의 핵심 hedging.

- `this is frankly the best we can do at the moment with the current X` (04) - "frankly"로 정직한 한계 인정
- `we'd love to, but to be honest, we don't have the resources to X` (04, 06) - "we'd love to, but" 거절-협업 전환
- `It depends based on the project by project. Typically, [ballpark]` (20) - "It depends" 회피 + 대략값
- `pulling in these schedules is structurally very difficult` (24) - "structurally difficult"로 구조적 한계 프레이밍
- `That is the biggest challenge the whole industry is facing` (03) - 산업 전체 문제로 책임 분산

### Move 4: 도전/정렬 확인 (Alignment Probe)

양쪽이 스펙·일정이 맞는지 확인. Type B의 **시그니처 move**.

- `are we well aligned?` (06) - THE alignment check. "agreed" 대신 "aligned"
- `I think generally we're well aligned` (06) - "generally"가 여지를 남기는 핵심 수식어
- `there are a couple of things that's not aligned with our roadmap` (06) - 부정 정렬 선언
- `Is that aligned with Intel?` (23) - 외부 기준과 정렬 확인
- `we'd like to check your test-bake schedule` (06) - schedule coordination
- `do you have kind of a minimum size for this opportunity to be viable?` (03) - viability probe

### Move 5: 타협 탐색 (Compromise Probe)

"if X, is that workable?"로 타협 가능성을 탐색한다. yes/no가 아니라 조건부.

- `if 128 is towards the beginning of the fourth quarter, is that workable?` (18) - "if X, is that workable?"가 Type B 핵심 타협 화법
- `if a pull-in is absolutely not possible, then please increase your volume support` (24) - if-then 이중 요구
- `if you can share X to us, we could further evaluate` (04) - 조건부 협업
- `we'd like X but Y is limited` (06) - "we'd like but" 양보 표현
- `Maybe it will be few hundred thousand at the most` (17) - 상한선 제시로 투자 우려 완화

### Move 6: 액션 아이템 / 후속 (Action Item)

Type B의 action item은 "I will send X by Y"보다 **deferred decision**이 많다.

- `let's settle on that maybe in a few months` (17) - roadmap 회의의 norm: deferred decision
- `we'll take an action to follow up` (03) - "take an action" 책임 명시
- `let us take action item` (24) - "action item" 공식 표현
- `we can sync up again in about a week` (02, 03) - "sync up" 후속 일정
- `maybe we can schedule a separate session to have some exploratory discussion` (20) - 별도 세션 미루기
- `once X, please let us know Y` (20) - "once X, Y" 조건부 후속

### Move 7: 마무리 선언 (Close Declaration)

- `I think that we have covered today's agenda` (03) - 선언적 마무리
- `why don't we call it a today` (23) - 정중한 종결
- `we don't want to take too much of your lunch time` (23) - 시간 배려 프레임
- `Without Hynix, we cannot survive` (24) - 의존성 인정 마무리

---

## S3. 핵심 전략 정수 (Core strategies across this type)

16권에서 재등장하는 7개 전략. 각 전략마다 name, when to use, BEST 1-2 expressions, Korean-vs-English pragmatic contrast note.

### 전략 1: Anchor-and-Concede (앵커-양보)

**When**: 상대에게 요구를 전달하되, 즉시 양보 여지를 열어둘 때. 16권에서 가장 자주 쓰이는 정합 전략.

**Best expressions**:
- `we'd love to, but to be honest, we don't have the resources to X` (04, 06) - 거절을 "하고 싶다"로 시작해 협업 제안으로 전환
- `we'd like X but Y is limited` (06) - "we'd like but"로 양보 표현
- `Maybe it will be few hundred thousand at the most` (17) - 상한선 제시

**Korean vs English**: 한국어 "하고 싶지만 어렵습니다"는 거절로 들린다. 영어 "we'd love to, but"는 거절의 **부드러운 시작**이며, "but" 뒤에 partner 칭찬("NVIDIA is the best player")을 붙이면 거절이 협업 제안으로 바뀐다. "we'd love to"를 생략하면 거절이 공격으로 들리므로 무조건 붙여라.

### 전략 2: Timeline Leverage (타임라인 레버리지)

**When**: 결정 시급성을 만들 때. 상대에게 "지금 결정 안 하으면 나중에 못 한다"를 정중하게 전달.

**Best expressions**:
- `before we finalize everything and it goes behind the curtain, we can have a review with SK hynix` (02) - "behind the curtain" 비유로 시간 압박
- `can you give me an answer before I leave Korea? 48 hours` (37) - personal stake를 deadline으로
- `anything later than that jeopardize the program in general` (16) - "jeopardize"로 위험 명시
- `we need some sort of decision by October of this year` (06) - 명시적 deadline
- `if everything is happening at the right time, we still have some issues about X` (18) - 최선의 경우에도 리스크

**Korean vs English**: 한국어 "빨리 결정해 주세요"는 압박으로 들린다. 영어는 "jeopardize the program" (위험), "before I leave Korea" (개인적 이벤트), "behind the curtain" (비유)로 우회. "hurry up" 절대 쓰지 말 것 - "expedite"나 "we need a decision by X"를 써라.

### 전략 3: Spec Pushback (스펙 푸시백)

**When**: 상대의 스펙 요구가不合理할 때, "no" 없이 거부.

**Best expressions**:
- `that is not really the purpose of why X was first shown` (04) - "no" 없는 거부, 원래 목적 상기
- `you can do up to X. But the challenge is Y` (03) - 능력 인정 + 한계 명시
- `in order for it to work, there has to be no delta` (16) - "no delta" 정밀 스펙 요구 (고객 입장)
- `we don't think it's feasible with the current architecture` (04) - "we don't think"로 정중한 비실용 선언
- `the main reason for why X was adopted in the first place was to Y, right?` (04) - "in the first place"로 원래 목적 도발

**Korean vs English**: 한국어 "그건 안 됩니다"는 단호하지만 공격적으로 들린다. 영어는 "not really the purpose", "we don't think it's feasible", "the challenge is"로 우회. "no"를 안 쓰면서 거부하는 화법. 핵심은 "안 한다"가 아니라 "목적에 맞지 않는다", "현재 아키텍처로는 어렵다"로 프레이밍.

### 전략 4: EOL/Negotiation Deferral (EOL 협상)

**When**: 제품 종료, 다음 세대 전환, 드롭 결정을 미룰 때.

**Best expressions**:
- `That's under consideration. We're effectively holding off the development because of X. We need some sort of decision by Y` (06) - "under consideration + holding off + decision by Y" 3단 공식
- `It's technically possible but not our POR. We're still exploring` (06) - POR로 비확정 명시
- `we haven't decided if X or not. If we decided, I will share with you` (23) - 결정 미루기 + 후속 약속
- `we are still under investigation for this kind of X` (04) - "under investigation"
- `We haven't closed that, but at the end of the day, it doesn't matter` (15) - "haven't closed" + 축소
- `Not at this time. ... we can look together` (17) - 2단 거절→협업 전환

**Korean vs English**: 한국어 "검토 중입니다"는 open-ended로 들려 US 귀에는 "안 할 것"으로 해석된다. 영어는 반드시 **deadline 또는 조건**을 붙여야 한다: "under consideration + decision by Y", "not a POR yet, still exploring", "haven't decided, but if X then I will share". 검토 중임을 밝히되 다음 단계를 명시하지 않으면 신뢰를 잃는다.

### 전략 5: Conditional Collaboration (조건부 협업)

**When**: 거절한 뒤 관계를 유지하거나, 자원 교환을 제안할 때.

**Best expressions**:
- `if you can share X to us, we could further evaluate` (04) - "could"로 더 정중
- `if you have X, it would be good for us to exchange Z` (31) - "exchange"로 reciprocity
- `we don't need to be in it for making money, but we need to just make sure that technology moves forward` (17) - 비금전적 프레이밍
- `we'd like to leave you with the feasibility together in Y` (16) - "leave you with the feasibility" 부드러운 푸시

**Korean vs English**: 한국어 "자료 주시면 검토하겠습니다"는 단방향. 영어 "if you can share X, we could further evaluate"는 양방향 - "exchange", "together"를 쓰면 reciprocity가 성립. "please send us"가 아니라 "if you have, it would be good for us to exchange"를 써라.

### 전략 6: Honest Limitation Admission (정직한 한계 인정)

**When**: 자원 부족, 실적 부진, 모름을 인정해 신뢰를 만들 때. Type B 회의에서 "모른다"를 정중하게 말하는 핵심 전략.

**Best expressions**:
- `my track record with SK hynix is not very good. In the last four years, I have not won a single project` (02) - 구체적 숫자로 실패 인정
- `If we have it, we will support it, but we don't know anybody` (03) - 솔직한 한계 + 의지
- `let us do a little bit of more homework` (03) - "homework"로 "좀 더 알아보겠다"
- `I don't have it on top of my head. I'll have to double check X` (31) - "I don't know" 대신 idiom
- `We don't have answer of every question. That's why we are looking for partner` (21) - 모름 + 파트너십 요청
- `this is frankly the best we can do at the moment with the current X` (04) - "frankly" 정직함 강조

**Korean vs English**: 한국어 "모르겠습니다"는 약해 보인다. 영어 "I don't know"는 초보자. "I don't have it on top of my head"는 "정보는 존재하지만 지금 머릿속에 없다"로 프로다운 회피. "frankly the best we can do"는 한계 인정을 정직함의 표현으로 승격. 자기 실패를 "I have not won a single project in four years"로 구체적 숫자로 인정하면 신뢰의 역설이 발생 - 약해지면서 오히려 강해진다.

### 전략 7: Decision Forcing / Binary Choice (의사결정 유도)

**When**: 모호한 상대에게 양자택일을 제시해 결정을 이끌어낼 때.

**Best expressions**:
- `So what kind of thing are they interested in more, so X or Y?` (03) - "so X or Y" 양자택일
- `Have to make the decision. Go for both or?` (03) - 주어 생략으로 무게감
- `which one is correct?` (03) - "맞는 건가요?" 확인
- `do you guys see a customer, a mutual customer that is going to ask for it?` (16) - 시장 수요로 도전
- `I want my fair share. And my fair share should be based on X` (37) - allocation formula

**Korean vs English**: 한국어 "어떻게 생각하세요?"로 끝내면 안 된다. 영어는 "X or Y?"로 양자택일을 제시, "which one is correct?"로 확인. "fair share"를 요구할 때는 숫자가 아니라 **formula**를 정의: "fair share based on X". formula에 동의하면 숫자는 자동 도출.

---

## S4. 마스터 표현 DB (Master Expression Database)

16권의 개별 expression DB에서 중복 제거·정제하여 60개를 선별. **3+ 교재에서 재등장하는 robust 패턴**을 우선. 각 엔트리: id, expression, function, sources, difficulty(1-5), note.

```yaml
# ── Move 1: Context Opening (회의 여는 화법) ──
- id: ex-001
  expression: "Multiple customers started to show a strong interest in X as well as Y"
  function: customer_demand_framing
  sources: [03, 06, 24]
  difficulty: 4
  note: 회의를 "우리 제안"이 아니라 "고객 수요"로 여는 화법. Type B의 첫 패턴

- id: ex-002
  expression: "as you guys are familiar with the X, I think there are a few changes"
  function: familiarity_precede_change
  sources: [15, 17, 22]
  difficulty: 3
  note: 로드맵 발표의 "변경점 프레이밍". "familiar with"로 과거 합의 회상 + "few changes"로 변경 신호

- id: ex-003
  expression: "the all the contents is all the same except X"
  function: delta_only_opening
  sources: [22, 20]
  difficulty: 3
  note: 분기 로드맵에서 "지난번과 같은데 X만 다릅니다" - 변경점에 주의 집중

- id: ex-004
  expression: "Starting in Q4 last year, we have seen a dramatic acceleration in X"
  function: market_framing
  sources: [24, 23]
  difficulty: 4
  note: 시장 상황을 "dramatic acceleration"으로 극적 프레이밍. 공급 제약 정당화의 서론

# ── Move 2: Target Timeline (타겟·타임라인 명시) ──
- id: ex-005
  expression: "we are targeting X by Y timeframe"
  function: timeline_target
  sources: [04, 06, 20, 22]
  difficulty: 3
  note: Type B 기본 동사. "will"이 아니라 "targeting"으로 목표 명시하되 확약 회피. "timeframe"이 완충제

- id: ex-006
  expression: "we plan to have X, so the timeline would be Y"
  function: schedule_declaration
  sources: [04, 18, 22]
  difficulty: 4
  note: 타임라인 명시 공식. "we plan to" + "the timeline would be"

- id: ex-007
  expression: "It is slated for X at Y"
  function: firm_timeline
  sources: [15, 17]
  difficulty: 3
  note: "slated for" = 확정 일정. "scheduled"보다 비즈니스 회의에서 자연스러움

- id: ex-008
  expression: "we expect the sample will be ready in end of X timeframe"
  function: sample_readiness
  sources: [22, 20, 18]
  difficulty: 3
  note: "timeframe"을 붙이는 게 핵심 - "end of February"는 너무 확정적, "end of February timeframe"이 여유

- id: ex-009
  expression: "we haven't had any specific schedule yet, but if you have any interest to evaluate, we can have more discussion"
  function: interest_probing_deferral
  sources: [04, 16, 18]
  difficulty: 5
  note: 관심 탐색형 미루기 - 핵심 화법. 부담을 고객에게 넘기면서 거부감 없이

- id: ex-010
  expression: "It might be Q4, maybe end of this year"
  function: tentative_schedule
  sources: [03, 04]
  difficulty: 3
  note: "might + maybe" 이중 불확실성 표시

# ── Move 3: Constraint Reveal (제약 공개) ──
- id: ex-011
  expression: "we'd love to, but to be honest, we don't have the resources to X"
  function: honest_refusal
  sources: [04, 06, 18]
  difficulty: 5
  note: 정직한 거절의 황금 공식. "we'd love to" + "to be honest" + (선택) partner 칭찬

- id: ex-012
  expression: "this is frankly the best we can do at the moment with the current X"
  function: honest_ceiling
  sources: [04, 31]
  difficulty: 5
  note: "frankly"로 정직함 강조. 한계 인정의 공식. 다음 세대 제안의 도입부로 쓰임

- id: ex-013
  expression: "we don't think it's feasible with the current architecture"
  function: infeasibility_declaration
  sources: [04, 31]
  difficulty: 4
  note: "we don't think"로 정중한 비실용 선언. "we can't"보다 부드러움

- id: ex-014
  expression: "It depends based on the project by project. Typically, [ballpark]"
  function: case_by_case_evasion
  sources: [20, 31]
  difficulty: 4
  note: "It depends" 회피 + 대략값. 회피를 제품 본성 설명으로 프레이밍

- id: ex-015
  expression: "pulling in these schedules is structurally very difficult"
  function: structural_constraint
  sources: [24, 23]
  difficulty: 5
  note: "structurally very difficult" - "우리가 안 해서"가 아니라 "구조적 한계"로 프레이밍. "cannot give the commitment"와 짝

- id: ex-016
  expression: "That is the biggest challenge the whole industry is facing"
  function: industry_wide_blame
  sources: [03, 24]
  difficulty: 5
  note: "whole industry is facing"로 책임 분산. "we can't" 대신 "산업 전체 문제"로 프레이밍

- id: ex-017
  expression: "We were supposed to X, but as the best case, Y"
  function: timeline_slip_acknowledgment
  sources: [03, 22]
  difficulty: 4
  note: "as the best case"로 원래 계획이 낙관적이었음을 함의. 일정 밀림 인정 공식

# ── Move 4: Alignment Probe (정렬 확인) ──
- id: ex-018
  expression: "are we well aligned?"
  function: alignment_check
  sources: [06, 22, 23, 37]
  difficulty: 4
  note: THE Type B alignment check. "agreed" 대신 "aligned" - binary가 아니라 spectrum

- id: ex-019
  expression: "I think generally we're well aligned"
  function: affirm_with_hedge
  sources: [06, 17, 23]
  difficulty: 4
  note: "generally"가 핵심 - 여지를 남겨두는 수식어. 100% 확신 아닐 때 무조건 붙여

- id: ex-020
  expression: "there are a couple of things that's not aligned with our roadmap"
  function: negative_alignment
  sources: [06, 04, 18]
  difficulty: 4
  note: "not aligned"가 Type B의 "we disagree" 표현. "you're wrong"이 아니라 "plans don't match"

- id: ex-021
  expression: "Is that aligned with X?"
  function: external_alignment_check
  sources: [23, 22]
  difficulty: 3
  note: 외부 기준(Intel, AMD roadmap)과 정렬 확인. 거짓말 탐지 화법

- id: ex-022
  expression: "do you have kind of a minimum size for this opportunity to be viable?"
  function: viability_probe
  sources: [03, 18]
  difficulty: 5
  note: "viable" - 비즈니스 타당성 핵심 단어. 파트너의 진지함 테스트

- id: ex-023
  expression: "we'd like to check your test-bake schedule"
  function: schedule_coordination
  sources: [06, 22]
  difficulty: 3
  note: schedule coordination의 정중 화법. "we'd like to check"가 협조적 뉘앙스

# ── Move 5: Compromise Probe (타협 탐색) ──
- id: ex-024
  expression: "if 128 is towards the beginning of the fourth quarter, is that workable?"
  function: conditional_compromise
  sources: [18, 17, 24]
  difficulty: 5
  note: "if X, is that workable?"가 Type B 핵심 타협 화법. yes/no가 아니라 타협을 유도

- id: ex-025
  expression: "if a pull-in is absolutely not possible, then please increase your volume support"
  function: if_then_demand
  sources: [24, 23]
  difficulty: 5
  note: "absolutely not possible"로 상대 한계 인정 + "then please" 대안 제시. 이중 요구

- id: ex-026
  expression: "if you can share X to us, we could further evaluate"
  function: conditional_collaboration
  sources: [04, 31, 18]
  difficulty: 4
  note: "could"가 "can"보다 더 정중. 책임을 상대에게 넘기면서도 적극적으로 들림

- id: ex-027
  expression: "we'd like X but Y is limited"
  function: spec_pushback_with_constraint
  sources: [06, 04]
  difficulty: 4
  note: "we'd like but"로 양보 표현. "we can't"가 아니라 "제약이 있다"로 프레이밍

- id: ex-028
  expression: "Maybe it will be few hundred thousand at the most"
  function: upper_bound_scope
  sources: [17, 18]
  difficulty: 4
  note: "at the most"로 상한선 제시. 투자 우려 사전 완화. partner의 두려움은 숫자가 아니라 미지의 ceiling

- id: ex-029
  expression: "That's a bigger ask. Maybe it's the next gen"
  function: acknowledge_and_defer
  sources: [06, 04]
  difficulty: 4
  note: "bigger ask"로 요구 크기 인정, "next gen"으로 다음 사이클로 미루기

# ── Move 6: Action Item / Follow-up ──
- id: ex-030
  expression: "let's settle on that maybe in a few months"
  function: deferred_decision
  sources: [17, 20]
  difficulty: 4
  note: roadmap 회의의 norm - hard action item 대신 deferred decision. "강제 action item 피하라"

- id: ex-031
  expression: "we'll take an action to follow up"
  function: formal_commitment
  sources: [03, 24]
  difficulty: 4
  note: "take an action" 책임 명시 공식. "I'll check"보다 강함, "I'll think about it"보다 진지함

- id: ex-032
  expression: "let us take action item"
  function: action_item_acceptance
  sources: [24, 22]
  difficulty: 3
  note: 답변 못할 때 "action item"으로 후속 약속. "I don't know" 절대 쓰지 말 것

- id: ex-033
  expression: "we can sync up again in about a week"
  function: follow_up_schedule
  sources: [02, 03, 18]
  difficulty: 3
  note: "sync up" 비즈니스 영어 필수 표현. "meet again"보다 가볍고 전문적

- id: ex-034
  expression: "maybe we can schedule a separate session to have some exploratory discussion"
  function: defer_to_separate_session
  sources: [20, 17, 21]
  difficulty: 4
  note: 별도 세션 미루기. "나중에 다시"가 아니라 "별도 세션"으로 더 전문적

- id: ex-035
  expression: "once X, please let us know Y"
  function: conditional_follow_up
  sources: [20, 23, 24]
  difficulty: 3
  note: "once X, Y" 조건부 후속. QBR에서 가장 많이 쓰는 action item 패턴

- id: ex-036
  expression: "during our discussion, if any question comes up, we will reach out via email"
  function: contact_channel
  sources: [04, 22]
  difficulty: 3
  note: 후속 채널 명시 공식. 회의 끝에 무조건 써라

# ── Move 7: Close (마무리) ──
- id: ex-037
  expression: "I think that we have covered today's agenda"
  function: agenda_completion
  sources: [03, 22]
  difficulty: 3
  note: 선언적 마무리. "Any questions?"가 아니라 "covered today's agenda"로 끝내야

- id: ex-038
  expression: "why don't we call it a today"
  function: polite_close
  sources: [23, 24]
  difficulty: 2
  note: "오늘은 여기까지" 관용구. "we don't want to take too much of your lunch time"과 짝

# ── Polite Challenge / Reason Probe (정중한 도전) ──
- id: ex-039
  expression: "I wanted to understand the background. Why the sudden jump to X"
  function: reason_probe
  sources: [06, 16]
  difficulty: 5
  note: "Why did you ask" 대신 "I wanted to understand the background". "sudden jump"로 우려 이름짓기

- id: ex-040
  expression: "Can you clarify - do you mean X or Y?"
  function: clarification_probe
  sources: [06, 16, 31]
  difficulty: 3
  note: 모호한 요구를 명확화. "do you mean X or Y?"로 forced commitment

- id: ex-041
  expression: "Is there a reason why X is also being sensitive to Y?"
  function: polite_reason_inquiry
  sources: [15, 16]
  difficulty: 4
  note: "Why are you X?" 대신 "Is there a reason why X". 주어를 "you"에서 "reason"으로 옮겨 비난감 감소

- id: ex-042
  expression: "I'm a little bit confused from the X perspective"
  function: confusion_as_challenge
  sources: [37, 22]
  difficulty: 4
  note: "I disagree" 대신 "I'm confused" - "I think you are wrong"을 정중하게 표현

- id: ex-043
  expression: "Maybe that was my misunderstanding, but that's how it came out"
  function: graceful_misunderstanding_ownership
  sources: [17, 22]
  difficulty: 5
  note: 상대가 모순 지적할 때 "no I never said that" 대신 "Maybe my misunderstanding". "how it came out"로 책임 분산

- id: ex-044
  expression: "I do understand X. That is true, but Y"
  function: acknowledge_then_challenge
  sources: [04, 22]
  difficulty: 5
  note: 반대 전 상대 인정. "do understand" + "That is true"로 두 번 인정하고 "but"로 전환

- id: ex-045
  expression: "all of their math is correct, but trying to determine if the base assumption is valid"
  function: math_yes_assumption_no
  sources: [22, 31]
  difficulty: 5
  note: 가장 고급 도전. "틀렸다"가 아니라 "수식은 맞는데 가정을 확인 중". 상대 작업 인정하면서 근본 도전

# ── Spec Pushback (스펙 푸시백) ──
- id: ex-046
  expression: "that is not really the purpose of why X was first shown"
  function: purpose_refutation
  sources: [04, 31]
  difficulty: 5
  note: "no" 없는 거부. "not really the purpose"로 원래 목적 상기시켜 정중하게 거부

- id: ex-047
  expression: "you can do up to X. But the challenge is Y"
  function: capability_vs_constraint
  sources: [03, 04]
  difficulty: 4
  note: 스펙 푸시백 공식 - 능력 인정 + 한계 명시

- id: ex-048
  expression: "we want to keep X as is, but we just want to release Y"
  function: keep_and_request
  sources: [04, 18]
  difficulty: 4
  note: 스펙 협상 - "keep X, ask for Y". 한 쪽 고정하고 다른 쪽 요구

# ── EOL / Decision Deferral (EOL/결정 미루기) ──
- id: ex-049
  expression: "That's under consideration. We're effectively holding off the development because of X. We need some sort of decision by Y"
  function: eol_negotiation
  sources: [06, 24, 04]
  difficulty: 5
  note: EOL 협상 3단 공식 - under consideration + holding off + decision deadline. 한국어 "검토 중"에 deadline 붙이는 게 필수

- id: ex-050
  expression: "It's technically possible but not our POR. We're still exploring"
  function: por_boundary
  sources: [06, 20]
  difficulty: 5
  note: POR(Plan of Record)로 비확정 명시. "do not plan around this" 경고. "still exploring"로 완화

- id: ex-051
  expression: "we haven't decided if X or not. If we decided, I will share with you"
  function: undecided_with_followup
  sources: [23, 18, 16]
  difficulty: 4
  note: 결정 미루기 + 후속 약속. "haven't decided"만 쓰면 약하고, "if X, I will share" 붙여야 전문가

- id: ex-052
  expression: "We haven't closed that, but at the end of the day, it doesn't matter"
  function: minimize_undecided
  sources: [15, 18]
  difficulty: 4
  note: "haven't closed" 솔직 인정 + "doesn't matter"로 중요성 축소. 결정 미루기를 부드럽게

# ── Honest Limitation (정직한 한계) ──
- id: ex-053
  expression: "my track record with X is not very good. In the last Y years, I have not won a single project"
  function: honest_failure_admission
  sources: [02, 22]
  difficulty: 5
  note: 구체적 숫자로 실패 인정. "How can I be helpful?"로 협력 의지 전환. 신뢰의 역설

- id: ex-054
  expression: "If we have it, we will support it, but we don't know anybody"
  function: honest_no_with_willingness
  sources: [03, 18]
  difficulty: 5
  note: "I don't know" 대신 "If we have it, we will support it". 솔직한 한계 + 의지 표시 2단

- id: ex-055
  expression: "I don't have it on top of my head. I'll have to double check X"
  function: professional_memory_lapse
  sources: [31, 22]
  difficulty: 4
  note: "I don't know"는 초보자. "on top of my head"는 "정보는 존재하지만 지금 없다"는 프로 회피

- id: ex-056
  expression: "We don't have answer of every question. That's why we are looking for partner"
  function: ignorance_to_partnership
  sources: [21, 17]
  difficulty: 5
  note: 모름 인정 + 파트너십 요청 전환. 정직함을 협력의 시작으로 포장

# ── Industry Framing / Blame Diffusion ──
- id: ex-057
  expression: "we tend to give favor to the incumbent. The incumbent is the people that already moved on with X"
  function: incumbent_favor_deflection
  sources: [18, 37]
  difficulty: 5
  note: 우선순위 거절을 "incumbent 우선"으로 포장. "tend to"로 부드럽게, "incumbent"로 시장 구조 탓

- id: ex-058
  expression: "we're just following the market. If the market changes, ..."
  function: market_following_deflection
  sources: [18, 20]
  difficulty: 4
  note: "We choose to"가 아니라 "we're following the market"로 주체성 제거. "if the market changes"로 조건부 가능성 열어둠

# ── Decision Forcing / Binary Choice ──
- id: ex-059
  expression: "So what kind of thing are they interested in more, so X or Y?"
  function: binary_choice_probe
  sources: [03, 16, 22]
  difficulty: 4
  note: 양자택일 질문 - 결정 유도. "어떻게 생각하세요?"로 끝내지 말고 "X or Y?"로

- id: ex-060
  expression: "I want my fair share. And my fair share should be based on X"
  function: allocation_formula
  sources: [37, 23]
  difficulty: 5
  note: allocation 협상. 숫자가 아니라 formula를 정의 - formula에 동의하면 숫자는 자동 도출. "fair share"가 핵심
```

---

## S5. 영역 어휘 정수 (Domain vocabulary across this type)

16권에서 재등장하는 도메인 용어. 4개 sub-domain으로 분류.

### Sub-domain A: Roadmap / Generations (로드맵·세대)

| Term | Gloss | Recurs in |
|:---|:---|:---|
| **POR** (Plan of Record) | 확정된 계획, 공식 로드맵 항목. "not a POR yet" = "do not plan around this" | 06, 20, 22 |
| **ES** (Engineering Sample) | 초기 프로토타입 실리콘 | 04, 06, 18, 22 |
| **CS** (Customer Sample) | 고객 검증용 샘플. ES 다음 단계 | 04, 06, 18, 22 |
| **NPI** (New Product Introduction) | 공식 제품 출시 프로세스 | 06, 22 |
| **POC** (Proof of Concept) | 개념 증명 (Pull-in Of Commitment와 혼용 주의) | 02, 06, 18 |
| **tape out** | 칩 설계 완료·제조 의뢰 | 02, 04, 22 |
| **bring up** | 초기 하드웨어 전원 인가·검증 | 06, 22, 31 |
| **locked and loaded** | 완전 준비됨·확정됨 (군사 용어 유래) | 02, 22 |
| **kicked off** | 프로젝트 시작됨 | 02, 06 |
| **exploration mode** | 로드맵 발표에서 가장 안전한 단어 - "research"보다 진지하고 "committed"보다 자유로움 | 20, 21 |
| **in flux** | 유동적. "we don't know" 대신 "in flux" | 21, 20 |
| **under consideration** | 검토 중. 한국어 "검토 중"의 정확한 영어 버전 | 06, 22, 23 |
| **gap filler** / **gap bridging** | 제품 갭을 메우는 임시 솔루션 | 23, 18 |
| **shift left** | 일정을 앞당기기. "pull in"의 전문 용어 | 23, 24 |
| **pull in** / **push out** | 일정 당기기 / 미루기 (Type B 3대 동사) | 23, 24, 06 |

### Sub-domain B: Supply / Volume (공급·볼륨)

| Term | Gloss | Recurs in |
|:---|:---|:---|
| **incumbent** | 기존 고객. "we tend to give favor to the incumbent"로 우선순위 거절 포장 | 18, 37 |
| **fair share** | 공정 할당량. formula로 정의 ("based on X") | 37, 23 |
| **allocation** | 할당. volume allocation, supply allocation | 37, 23, 18 |
| **capacity** | 생산 능력. "under capacity constraint" | 23, 24, 18 |
| **volume** | 물량. "we will build a limited quantity" | 18, 23, 24 |
| **NRE** (Non-Recurring Engineering) | 일회성 개발 비용. "will require NRE" | 02, 04 |
| **MOU** (Memorandum of Understanding) | 양해 각서. 형식적 약정 요구 | 02 |
| **RFQ** (Request for Quote) | 견적 요청서. "if we know your RFQ, we can be helpful" | 02 |
| **supply constrained** | 공급 제약 상태. "market conditions are supply constrained" | 18, 24 |
| **structural difficulty** | 구조적 어려움. "structurally very difficult" | 24, 23 |

### Sub-domain C: Timeline / Milestones (타임라인·마일스톤)

| Term | Gloss | Recurs in |
|:---|:---|:---|
| **timeframe** | 시점. "end of February timeframe" - timeframe이 완충제 | 04, 20, 22 |
| **best case scenario** | 최상 시나리오. "best case is 2030" - 불확실성 인정 | 23, 22 |
| **as the best case** | 원래 계획이 낙관적이었음을 함의 | 03, 04 |
| **PRQ** (Production Readiness Qualification) | 양산 준비 검증. Intel 용어 | 23 |
| **GA** (General Availability) | 일반 출시. "GA Q1 next year" | 23, 22 |
| **milestone** | 마일스톤. project milestone, development milestone | 18, 22, 06 |
| **cadence** | 주기. "your cadences year over year" | 16, 18 |
| **jeopardize** | 위태롭게 하다. "anything later jeopardize the program" | 16, 22 |
| **expedite** | 촉진하다. "expedite the spec closure" - "hurry up"의 전문가 버전 | 20, 22 |

### Sub-domain D: Negotiation / Strategic (협상·전략)

| Term | Gloss | Recurs in |
|:---|:---|:---|
| **aligned** | 정렬된. "are we well aligned?" - "agreed" 대신 쓰이는 spectrum 용어 | 06, 22, 23, 37 |
| **aligned with X** | X와 정렬된. "aligned with Intel" | 23, 22 |
| **viable** | 타당성 있는. "minimum size to be viable" | 03, 18 |
| **workable** | 실현 가능한. "is that workable?" - 타협 탐색 핵심 단어 | 18, 17 |
| **feasible** | 실현 가능한. "we don't think it's feasible" | 04, 31 |
| **fundamental constraint** | 근본 제약. "I think that's the fundamental constraint" | 04, 06 |
| **bigger ask** | 더 큰 요구. "That's a bigger ask" - 요구 크기 인정 | 06, 04 |
| **behind the curtain** | 커튼 뒤로. "before it goes behind the curtain" - 시간 압박 비유 | 02 |
| **cherry-pick** | 골라서 선택. "cherry picking of parts" | 06 |
| **baked in stone** | 확정된. "don't assume anything's baked in stone" | 24 |
| **judgment call** | 판단. "make a judgment call early on" | 02, 17 |
| **due diligence** | 실사. "give the team enough time to do due diligence" | 22 |
| **sync up** | 다시 만나 정보 맞추자. "meet again"보다 가볍고 전문적 | 02, 03, 18 |
| **leading partner** | 리딩 파트너. "positioning you as a leading partner" | 03, 02 |
| **total package** | 통합 패키지. "sell a total package" | 03 |

### Sub-domain E: Memory / Tech (메모리·기술)

| Term | Gloss | Recurs in |
|:---|:---|:---|
| **HBM** (High Bandwidth Memory) | 고대역폭 메모리. HBM4, HBM4e, HBM5 | 04, 06, 21, 22 |
| **SOCAM** (SoC AM) | System-on-Chip Advanced Memory (Qualcomm custom) | 04, 15, 17, 18 |
| **LPDDR5X / LPDDR6 / LPDDR7** | 모바일 DRAM 세대 | 15, 16, 17, 18 |
| **MRDIM** (Multi-Rank DIMM) | JEDEC 버퍼 메모리 모듈 표준 | 22, 37, 23 |
| **tall MRDIM** | 16Gbit 베이스 MRDIM (비용 효율적 128GB) | 37 |
| **RDIM** (Registered DIMM) | 표준 버퍼 DIM | 22, 37 |
| **CXL** (Compute Express Link) | CXL pooling, CXL CMM | 02, 06, 20, 21 |
| **fmax** | 최대 동작 주파수. "targeting X for fmax" | 06 |
| **guard band** | 안전 여유. 5-10% 전형 | 06, 04 |
| **rank** | 독립 접근 뱅크 수 | 06, 22 |
| **HBF** (High Bandwidth Flash) | HBM과 유사하지만 NAND 기반 | 21 |
| **PIM** (Processing In Memory) | 메모리 내 처리 | 16, 20 |
| **redriver / retimer** | 신호 재구동 칩 | 04 |
| **buffer die** | 모듈 상의 이산 버퍼 | 04, 06 |

---

## S6. 주간 학습 경로 (Weekly learning path)

5일 계획. 16권 중 가장 학습 가치가 높은 교재를 우선 배치.

### Day 1 (Mon): Speaker Architecture - "Alignment Dance"

- 읽기: **textbook-06** (NVIDIA morning, Type B 정수) Section 1 + 4
- 읽기: **textbook-03** (Marvell) Section 1 (5단계 회의 설계)
- 주목 S2 patterns: Move 1 (Context Opening), Move 2 (Target Timeline), Move 4 (Alignment Probe)
- DB drilling: ex-001, ex-005, ex-018, ex-019, ex-020 (alignment 관련 5개)
- self-recording: "are we well aligned?" / "I think generally we're well aligned" 5회

### Day 2 (Tue): Hedging & Deflection - 정직한 한계

- 읽기: **textbook-04** (NVIDIA 2H) Section 2 (Hedging 6 전략)
- 읽기: **textbook-37** (AMD Joe) Section 2 (SK deflection 5 전략)
- 주목 S3 strategies: 전략 6 (Honest Limitation), 전략 4 (EOL Deferral)
- DB drilling: ex-011, ex-012, ex-049, ex-050, ex-053, ex-054, ex-055 (한계 관련 7개)
- contrastive noticing: 한국어 "검토 중입니다" vs 영어 "under consideration + deadline by Y" - deadline이 없으면 신뢰 잃음

### Day 3 (Wed): Spec Pushback & Compromise Probe

- 읽기: **textbook-18** (Qualcomm 2H) Section 3 (조건부 타협 탐색)
- 읽기: **textbook-31** (AMD) Section 3-4 (polite challenge + negotiation)
- 주목 S3 strategies: 전략 3 (Spec Pushback), 전략 1 (Anchor-and-Concede)
- DB drilling: ex-024, ex-025, ex-026, ex-029, ex-046, ex-047, ex-048 (스펙·타협 7개)
- retrieval practice: "if X, is that workable?" / "you can do up to X. But the challenge is Y" 5회

### Day 4 (Thu): EOL Negotiation & Decision Forcing

- 읽기: **textbook-02** (Scaleflux) Section 1-2 (Exclusivity, behind the curtain)
- 읽기: **textbook-17** (Qualcomm 1H) Section 2 (Partial-Agreement Summary)
- 읽기: **textbook-22** (HPE QTR) Section 1.5 (Eric의 math-correct/assumption-invalid 도전)
- 주목 S3 strategies: 전략 2 (Timeline Leverage), 전략 7 (Decision Forcing)
- DB drilling: ex-039, ex-045, ex-059, ex-060, ex-030, ex-034, ex-007 (도전·EOL 7개)
- self-recording: "behind the curtain" / "jeopardize the program" / "X or Y?" 5회

### Day 5 (Fri): Audrey 교정 - Pragmatic Drill

- 복습: DB 60개 중 어려웠던 15개 재 drill
- Audrey session: S7의 Top 5 표현 native check
- role-play: Type B 회의 5-move 사이클 (opening → timeline → constraint → alignment → action item) 통연습
- self-record: "we'd love to, but to be honest..." / "if X, is that workable?" / "are we well aligned?" 3세트

---

## S7. Audrey 금요일 교정 노트 (Friday correction notes)

Steve가 매주 금요일 Audrey에게 가져가야 할 Type B 교정 항목.

### Top 5 must-correct expressions (register/pragmatics)

1. **"are we well aligned?"** - 한국인은 "do you agree?"로 직접 묻는 경향. "aligned"가 Type B 시그니처. Audrey에게 "agreed vs aligned" 뉘앙스 차이 drill. 복수형 "are we"인지 "is this"인지 register 확인.

2. **"we'd love to, but to be honest, we don't have the resources to X"** - 한국어 "하고 싶지만 어렵습니다"는 거절로만 들림. "we'd love to"의 발음 강세, "to be honest"의 삽입 위치, "but" 뒤 pause 길이. Audrey에게 native 버전으로 교정.

3. **"if X, is that workable?"** - 한국인은 "Is X possible?"로 직접 질문. "if X, is that workable?"의 조건부 구조와 "workable"의 비즈니스 register. 타협을 유도하는 화용론적 뉘앙스 교정.

4. **"That's under consideration. We're effectively holding off the development because of X. We need some sort of decision by Y"** - 한국어 "검토 중입니다"는 open-ended. 3단 공식의 강세 위치, "effectively holding off"의 강도, "some sort of decision"의 vagueness 의도. Audrey에게 deadline 붙이는 화법 교정.

5. **"maybe we can schedule a separate session to have some exploratory discussion"** - 한국어 "나중에 다시 얘기하죠"는 회피. "separate session" + "exploratory discussion"의 진지함 표현. "maybe"로 부드럽게, "exploratory"로 비확정 명시.

### Top Korean-vs-English contrasts to check

- "검토 중입니다" → "under consideration" (단독 사용 금지 - deadline 또는 조건 필수)
- "시간이 좀 부족해서요" → "pulling in these schedules is structurally very difficult" (개인 핑계 대신 구조적 한계로 프레이밍)
- "그건 좀 어려울 것 같습니다" → "we don't think it's feasible with the current architecture" (주관 평가 대신 구체적 이유)
- "다음에 다시 논의하죠" → "let's settle on that maybe in a few months" (구체 시점 없으면 신뢰 하락)
- "고객이 원해서요" → "Multiple customers started to show a strong interest in X" (능동 구조로 수요 묘사)
- "다 알아요" → "as you guys are familiar with the X, I think there are a few changes" (친숙함 전제 + 변경 신호)
- "시간 다 됐네요" → "we don't want to take too much of your lunch time" (상대 시간 배려 프레임)

### Self-record (auditory feedback loop)

Steve가 매주 녹음해서 들어야 할 5문장:
1. "We are targeting X by Y timeframe." - "targeting"과 "timeframe"의 강세
2. "Are we well aligned?" - "well"의 억양 (올림/내림)
3. "we'd love to, but to be honest, we don't have the resources" - "but" 뒤 pause
4. "if 128 is towards the beginning of Q4, is that workable?" - "workable"의 억양
5. "let's settle on that maybe in a few months" - "maybe"와 "a few months"의 리듬

---

## S8. 한계와 신뢰도 (Limitations and confidence)

### Source coverage

- **N = 16 textbooks** (Type B, 2025-05-12 ~ 2026-08-19)
- 총 단어 수 ~110,000 (16권 평균 7,000단어)
- 총 expression DB entry: ~840 (16권 평균 53)
- 본 essence의 master DB: 60개 (840에서 중복 제거·정제하여 선별)

### Robust (3+ textbooks) vs Single-attestation

**Robust (3+ sources)** - 높은 신뢰도:
- "are we well aligned?" (06, 22, 23, 37) - 4+ 권
- "we are targeting X by Y timeframe" (04, 06, 20, 22) - 4 권
- "we'd love to, but to be honest" (04, 06, 18) - 3 권
- "if you can share X, we could further evaluate" (04, 31, 18) - 3 권
- "under consideration + deadline by Y" (06, 24, 04) - 3 권
- "It depends + ballpark" (20, 31) - 2 권
- "behind the curtain" (02) - 1 권 (signature move)
- " structurally very difficult" (24, 23) - 2 권

**Single-attestation (1 textbook)** - 낮은 신뢰도, signature move:
- "behind the curtain" (02 only) - Scaleflux 특유 비유
- "My blood is boiling" (37 only) - AMD Joe 극단 케이스
- "Without Hynix, we cannot survive" (24 only) - AWS Ashik 극단
- "all of their math is correct, but base assumption invalid" (22 only) - HPE Eric 고급 도전
- "I want my fair share based on X" (37 only) - AMD Joe allocation formula
- "Chicken and chicken" (21 only) - Qualcomm 비유 변형

### Corpus does NOT capture

1. **Audio missing** → prosody, pause, interruption, silence 없음. 특히 "are we well aligned?"의 억양(올림/내림)이 화용론적 의미를 결정하지만, 전사본만으로는 파악 불가.
2. **No interruption patterns** - 실제 회의에서는 발화가 겹치고 끊기지만 전사본은 정렬됨. "let me finish" / "hold on" / "can I just..." 같은 차단 패턴 미포착.
3. **No silence** - 한국인이 "검토 중입니다" 후 침묵하는 시간이 신뢰에 미치는 영향 미포착.
4. **No body language** - "behind the curtain" 비유의 손동작, "fair share" 요구의 시선 등.
5. **Recency skew** - 2025-05 ~ 2026-08 회의. 2024년 이전 Type B 회의 패턴은 다를 수 있음.

### What Steve should NOT over-generalize

1. **AMD Joe의 공격적 화법** (37권) - "my blood is boiling", "I beg you", "we will remove resources" - US executive의 극단 케이스이며, 일반 Type B 회의에서 이런 화법 쓰면 관계 손상. 학습은 하되 **따라 쓰지 말 것**.

2. **Qualcomm의 "we don't need to be in it for making money"** (17권) - 파트너가 비금전적 프레이밍을 쓸 때 SK가 어떻게 받아야 할지는 맥락 의존적. 매번 "technology moves forward"로 응대하면 비즈니스 리버리지 잃음.

3. **"aligned with X"의 남용** - "are we well aligned?"는 강력하지만, 매 턴마다 쓰면 비즈니스 용어 오염. 핵심 결정 지점에서만 쓰고, 일반 확인은 "is this correct?" / "right?"로.

4. **POR는 특정 회사 용어** - NVIDIA, HPE 회의에서 자주 쓰이지만, Qualcomm이나 Scaleflux 회의에서는 "POR" 대신 "slated for" / "targeting"으로. 모든 partner에게 POR를 쓰면 어색.

5. **"we'd love to, but"의 반복** - 한 회의에서 2번 이상 쓰면 회피 패턴으로 인식. 1회당 1번만. 두 번째 거절은 "we cannot commit at this time" 또는 "that's a bigger ask"로 우회.

### Confidence rating

- S2 (Speaker architecture): HIGH - 16권 전체에서 7-move 사이클 일관
- S3 (Strategies): HIGH - 7 전략 모두 3+ 권에서 재등장
- S4 (Master DB): MEDIUM-HIGH - 60개 중 ~45개는 3+ 권 robust, ~15개는 1-2 권 signature. robust 비율 75%
- S5 (Domain vocabulary): HIGH - 50개 용어 모두 2+ 권에서 재등장
- S6-S7: MEDIUM - 학습 경로는 16권 기반으로 설계했으나, Audrey 실제 교정은 Steve의 산출물에 의존

---

> End of Essence Volume E-B. 16권 정수.
> Master DB 60개는 840개 원 expression에서 중복 제거·정제하여 선별.
> Steve는 이 essence를 Type B 회의 1-2시간 전에 1차로 읽고, 해당 partner별 특성은 원 교재로 돌아가 확인.
