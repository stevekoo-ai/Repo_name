---
essence_id: E-D
type: D
type_name: 이슈/품질 디버깅
source_textbooks: [19, 28, 33]
source_count: 3
total_db_entries_distilled: 45
created: 2026-09-02
audrey: Friday pragmatic-correction channel
---

# Essence E-D - 이슈/품질 디버깅 정수 (Issue/Quality Debugging)

> 3권(type D 3권: MSFT 2026-03-12, Intel 2026-01-22, Intel 2025-08-21)의 액기스.
> 작은 코퍼스(N=3) 기반이므로 S8에 명시한 한계를 반드시 참고할 것.
> em-dash는 사용 금지 - 하이픈(-)만 사용.

---

## S1. 유형의 본질 (What defines this meeting type)

Type D 회의는 "발표자-청중" 구조가 아니다. **진단자(diagnostician) 또는 facilitator**가 회의를 이끌고, 다수의 이슈 owner가 자신의 이슈를 올리고, 전문가가 tip/진단/권고로 응답하는 **다자간 이슈 동기화** 구조다. 단일 pitch가 아니라 여러 이슈가 병렬로 처리된다. 핵심은 "문제를 어떻게 정중하게 진단하고, 책임을 어떻게 hedging하며, 후속을 어떻게 명시하느냐"다.

Steve의 역할은 **양면**이다. SK Hynix 입장에서 Microsoft/Intel에 이슈를 올리고 status를 보고할 때는 **issue owner/defender** 역할이 되고, 반대로 SK가 기술 권고를 하거나 타 팀 답변을 대신 전달할 때는 **diagnostician/intermediate** 역할이 된다. 두 역할 모두 직접 써야 한다. 교재 19(MSFT)에서는 Microsoft가 evaluator/quality reviewer, SK가 defender. 교재 28(Intel)에서는 SK가 issue owner, Intel Anil이 expert/diagnostician, Jenny/Don이 facilitator. 교재 33(Intel)에서는 Ivan(Intel)이 diagnostician, Jerry(SK)가 정중한 요청자/협상자. Steve는 모든 역할을 번갈아 맡는다.

파트너의 typical stance는 "정중하지만 방향을 잡는 권위". Microsoft는 sandwich feedback과 "drive that down"으로 target을 설정하고, Intel은 "tip"과 "I will not recommend that"으로 방향을 정정한다. 감정적 register는 **직접적이되 정중한 (direct-but-deferential)** - 비난은 "you're wrong"이 아니라 "it's not true that X"로, 거부는 "no"가 아니라 "I don't think that would be ideal"로, 비판은 "don't debug too much"를 "I'll give you some tip" 틀 안에 넣어 전달.

다른 유형과의 대비:
- **vs A (기술 deep-dive)**: A는 단일 발표자의 아키텍처 설명 + Q&A. D는 발표자가 없고 다자간 이슈 review. A는 제품 자랑, D는 약점 포장.
- **vs B (Roadmap/Supply)**: B는 양사 로드맵/용량 타겟 negotiation. D는 이미 발생한 이슈의 진단/조정. B는 "we're targeting X in Y", D는 "we are looking for the reason why X".
- **vs C (샘플/일정)**: C는 ES/CS 샘플 수량/시점 조율. D는 샘플이 아니라 그 샘플에서 발견된 문제의 진단. C는 "we'd like to request N units", D는 "we didn't find a connection at this moment".

---

## S2. 화자 아키텍처 정수 (Speaker architecture across this type)

Type D 회의는 5-7개의 구조적 발화 move가 재귀한다. 각 move마다 코퍼스에서 가장 대표적인 표현 1-2개를 제시.

### Move 1: 문제 재확인 (Problem Restatement before Answering)

진단자는 질문을 받으면 즉시 답하지 않고 먼저 문제를 재진술한다. 이해를 점검하고, 잘못된 가정을 일찍 드러내며, 답변 시간을 번다.

- "if I'm understanding right the issue is that X" (33) - 디버그 답변 전 문제 재진술. 필수.
- "am I reading something wrong because X" (33) - 자기 이해 점검, 상대가 정정할 기회 제공.
- "So again, I saw an email about how they fix the issue, right?" (28) - facilitator의 이슈 회상형 열기. "right?"로 공유 맥락 설정.
- "did I read that correctly?" (28) - 자기 이해 검증형 확인.

### Move 2: Hedged 진단 제시 (Hedged Diagnosis)

진단은 "It is X"라는 단정을 피하고 "most likely", "could be", "I don't think", "I would not be surprised"로 hedging한다. 이중 hedging이 type D의 서명 무브.

- "most likely there could be X limitation" (33) - "most likely" + "could be" 이중 hedging. 틀려도 체면이 살고 반박 여지 부여.
- "I would not be surprised to find that X imposes a limitation on Y" (33) - 가능성 시사하는 전문가 표현. "아마 X일 것"의 권위 있는 버전.
- "the conflict that you have is a X violation for Y" (33) - 강한 진단. "violation"으로 규정.
- "we are looking for the reason why there is X" (28) - 원인 탐색 status 보고.

### Move 3: 실험/검증 지시 (Test Instruction)

진단만 하고 끝내지 않고 검증 경로를 제시한다. Type D의 핵심 action move.

- "I will suggest you to do the test collect the [data] and share [data] with me" (33) - 검증 + 데이터 공유 + 후속 가이드. 4단 구조.
- "I would suggest like, try X. See if that works. And then Y" (33) - 단계적 실험.
- "try only one or the other" (33) - 격리 실험.
- "So don't debug too much. So you have to figure out what X is" (28) - "tip" 틀 안에서 방향 전환.

### Move 4: 정중한 정정 (Polite Correction) / 단호한 거부 (Firm Rejection)

상대의 잘못된 가정이나 방향을 정정. 부드러운 거부와 단호한 거부를 구분해 쓴다.

- "So it's not true that X. We have to do that." (33) - 정중한 정정 공식. "You're wrong" 대신 "it's not true that X"로 주어 이동.
- "We have seen that" (33) - 과거 사례를 증거로. 반박 어렵게.
- "you never know sometimes" (33) - 부드러운 이의 제기 오프닝. "No" 대신.
- "I don't think that would be ideal" (33) - 부드러운 거부. "don't think"로 의견 성격 표시.
- "I will not recommend that, especially for X" (33) - 단호한 거부 + "especially for X"로 맥락. 반박 차단.
- "I would not waste my time on X. Try on Y." (33) - 강한 우선순위 신호. "waste my time".

### Move 5: 부재자에게 책임 넘기기 (Deferring to Absent Owner)

결정 권한이 없을 때 개인 의견은 주되 "I'm not the owner"로 권한을 명시하고 부재자에게 미룬다.

- "I don't see an issue on X but I'm not the owner. That will be [name]" (33) - 정중한 회피 공식.
- "let's check with [name] when he gets back from vacation" (33) - 부재자 후속 명시.
- "we need [name] to take the last call" (33) - "take the last call" = 최종 결정권. "make the final decision"보다 회의 체 자연스러움.
- "I'm just speaking from what I have seen the previous work from [name]" (33) - 의견 면책. "제가 본 것만".

### Move 6: Status 보고 (Status Reporting with Disclaimers)

이슈 owner는 진행 상태를 보고할 때 시점 한정, 영역 한정, soft commitment를 붙인다.

- "we did N loops of all the X tests, no red flag or no major issues as of today" (28) - "as of today" 필수. regression 보고의 면책 공식.
- "We are still debugging it, but." (28) - 진행 중 상태. "but" 뒤가 핵심.
- "There are some, I would say, minor or small issues" (28) - "I would say"로 평가 한정.
- "no major issue, at least on the X side of the things" (28) - 영역 한정 면책.
- "we didn't find that there is a specific connection to X at this moment" (19) - past tense non-finding + temporal hedge. 부정도 인정도 아닌 회피의 황금표현.
- "the X team keeps things very close within their organization" (28) - 타 팀 비협조를 관용구로. 자기 책임 회피.

### Move 7: 후속 채널 명시 (Follow-up Channel)

매 이슈 끝에 다음 연락 채널을 명시한다. 디버그 회의는 "회의에서 끝"이 아니다.

- "We will keep the discussion of this with my email" (33) - "keep the discussion with email".
- "I can follow up with that" (28) - 가장 자주 나오는 action item. "I'll check"보다 전문적.
- "I'll keep you informed" (28) - 정보 유지 약속. "keep you"가 지속성.
- "I'll try and get you some answers. But right now, my understanding is X" (28) - soft commitment. 자기가 통제 못 하는 답변을 대신 전달할 때.

---

## S3. 핵심 전략 정수 (Core strategies across this type)

Type D에서 재귀하는 7개 전략. 각 전략마다 사용 시점, 최고 표현, 한국어-영어 pragmatic 대비.

### 전략 1: "at this moment" 시간 한정 회피 (Time-Bounded Disclaimer)

**언제**: 이슈 책임 소재를 직접 묻거나, 당사 디바이스와의 연관을 확정해야 할 때. 부정도 인정도 하지 않고 시간을 번다.

**표현**:
- "we didn't find that there is a specific connection to X at this moment. Definitely we will do further." (19)
- "no red flag or no major issues as of today" (28)

**한-영 대비**: 한국어 "현재로서는 연관성을 못 찾았습니다"는 단일 회피. 영어는 past tense non-finding("we didn't find") + temporal hedge("at this moment") + 협조 표시("Definitely we will do further") 3단. "at this moment"가 "내일 다를 수 있다"는 면책을 내장. 절대 "it's not our issue"라고 말하지 말 것.

### 전략 2: 이중 Hedging 진단 (Double Hedging)

**언제**: 진단을 내릴 때. "It is X" 단정은 틀렸을 때 체면이 깨지고 반박 여지가 없다.

**표현**:
- "most likely there could be X limitation" (33) - "most likely" + "could be" 겹침.
- "I would not be surprised to find that X imposes a limitation on Y" (33)

**한-영 대비**: 한국어 "아마 X일 겁니다"는 단일 완화. 영어는 "most likely" + "could be"를 겹쳐 써서 틀려도 체면이 살고 상대가 반박할 여지를 준다. "I would not be surprised"는 "나는 X일 것 같다"의 전문가 버전 - 한국어 "놀라지 않을 것"에 해당하지만 훨씬 권위 있다.

### 전략 3: 부재자에게 책임 넘기기 (Deferring to Absent Owner)

**언제**: 결정 권한이 없을 때. 개인 의견은 주되 최종 결정은 진짜 owner에게 미룬다.

**표현**:
- "I don't see an issue on X but I'm not the owner. That will be [name]. let's check with [name] when he gets back from vacation." (33)
- "I'm just speaking from what I have seen the previous work from [name]." (33)

**한-영 대비**: 한국어 "제 생각에는 괜찮은데, 결정은 A 담당자가 휴가에서 돌아오면 확인해야 합니다". 영어는 개인 의견("I don't see an issue") + 권한 부인("I'm not the owner") + 부재자 지정("That will be [name]") + 후속("let's check with [name] when he gets back") 4단. "take the last call" = 최종 결정권. "make the final decision"보다 회의 체에서 자연스러움.

### 전략 4: "tip"으로 비판 완화 (Tip-as-Criticism)

**언제**: 상대의 디버깅 방향이 잘못되었을 때. 직접 지적은 도전적, "tip" 틀 안에 넣으면 조언이 된다.

**표현**:
- "I'll give you some tip. So don't X too much. So you have to figure out Y. So that's my tip. That's all." (28)

**한-영 대비**: 한국어 "팁 하나 드리자면". 영어는 "I'll give you some tip"으로 틀을 열고 "don't debug too much"라는 직접 지적을 그 안에 넣고 "That's all"로 명시적 마침. 권위 차이가 허용되지만 정중하게. "don't X too much" + "you have to figure out Y" 조합이 방향 전환의 핵심.

### 전략 5: 정중한 정정 (Polite Correction with "So it's not true that X")

**언제**: 상대의 잘못된 가정을 정정할 때. "You're wrong"은 절대 금지.

**표현**:
- "So it's not true that X. We have to do that. Even if you have seen in the past that Y. We have seen that." (33)
- "you never know sometimes" (33) - 부드러운 이의 제기 오프닝.

**한-영 대비**: 한국어 "아닙니다, 틀렸습니다". 영어는 "So it's not true that X"로 주어를 "you"에서 "사실"로 빼서 비난감을 줄이고, "We have to do that"로 결론을 붙여 정정이 의견이 아니라 사실임을 강조. "We have seen that"으로 과거 사례를 증거 제시하면 반박이 어렵다.

### 전략 6: 단호한 거부 + 맥락 (Firm Rejection with Context)

**언제**: 부드러운 거부로는 안 될 때. "especially for X"로 왜 안 되는지 맥락을 붙여 반박을 차단.

**표현**:
- "I will not recommend that, especially for X" (33) - "especially for performance data publications"이 붙으면 성능 데이터 신뢰성 문제라 반박 어려움.
- "I would not waste my time on X. Try on Y." (33) - 강한 우선순위 신호.
- "I don't think that would be ideal" (33) - 부드러운 거부. "don't think"로 의견 성격.

**한-영 대비**: 한국어 "이건 안 됩니다". 영어는 두 단계 - 부드러운 거부("I don't think that would be ideal")와 단호한 거부("I will not recommend that, especially for X"). "especially for X"로 맥락을 붙이면 반박이 어렵다. "I would not waste my time on X"는 "X는 시간 낭비"라는 강한 우선순위 신호.

### 전략 7: Sandwich 피드백 (Sandwich Feedback for Quality Review)

**언제**: evaluator 입장에서 supplier의 품질 이슈를 리뷰할 때. 긍정 2번 후 비판 1번, 그리고 회복 인정.

**표현**:
- "the good news is X / the good thing is also Y / but Z was a rough year / I mean, we got to really drive that down / X is a target that we want to target / anyways, off to a good start" (19)
- "with a little bit of a caveat in that we slightly reduced X. That's to align with Y. In easy conversation here is that everything that we tested has been best in class." (19)

**한-영 대비**: 한국어 "잘하고 있습니다만, 이 부분은 아쉽습니다". 영어는 긍정 2회("good news is", "good thing is also") 후 "but" 전환, "anyways"로 회복 인정. 부정 소식은 "a little bit of a caveat" + "slightly" 이중 완화 + "to align with" 근거. "best in class"로 reassurance. 비판 전 여유를 확보하는 정중한 권위 화법.

---

## S4. 마스터 표현 DB (Master Expression Database)

3권의 표현 DB(58 + 55 + 52 = 165개)에서 중복 제거·대표성 선별·type-unique 우선하여 40개로 압축. sources 필드는 어느 교재에서 왔는지. **N=3 코퍼스이므로 2+ 교재 출현 표현은 robust, 1교재만은 single-attestation** - note에 명시.

```yaml
# - 진단적 권위 (Diagnostic Authority) -
- id: ex-001
  expression: "if I'm understanding right the issue is that X"
  function: problem restatement before answering
  sources: [33]
  difficulty: 4
  note: 디버그 답변 전 문제 재진술. single-attestation(33)이지만 type D 서명 무브. (28)의 "did I read that correctly?"가 유사 variant.

- id: ex-003
  expression: "So again, I saw an email about how they fix the issue, right?"
  function: facilitator issue recall, shared context setup
  sources: [28]
  difficulty: 4
  note: 정기 sync 미팅의 이슈 열기. single-attestation(28). facilitator 서명 화법.

- id: ex-004
  expression: "did I read that correctly?"
  function: self-verification, polite confirmation
  sources: [28]
  difficulty: 4
  note: 자기 이해 검증. single-attestation(28). (33)의 "am I reading something wrong"와 쌍.

- id: ex-005
  expression: "the conflict that you have is a X violation for Y"
  function: explicit diagnosis, "X violation" framing
  sources: [33]
  difficulty: 5
  note: 강한 진단. single-attestation(33). "violation"으로 규정.

- id: ex-006
  expression: "most likely there could be X limitation"
  function: tentative diagnosis, double hedging
  sources: [33]
  difficulty: 4
  note: "most likely" + "could be" 이중 hedging. single-attestation(33)이지만 type D 핵심 패턴.

- id: ex-007
  expression: "I would not be surprised to find that X imposes a limitation on Y"
  function: hedged prediction, possibility signal
  sources: [33]
  difficulty: 5
  note: "I would not be surprised" - 가능성 시사하는 전문가 표현. single-attestation(33).

- id: ex-008
  expression: "I will suggest you to do the test collect the [data] and share [data] with me"
  function: verify instruction + data share + follow-up guide
  sources: [33]
  difficulty: 5
  note: 검증 + 데이터 공유 + 후속 가이드 3단. Type D 핵심 action item. single-attestation(33).

- id: ex-009
  expression: "I would suggest like, try X. See if that works. And then Y"
  function: stepwise experiment
  sources: [33]
  difficulty: 4
  note: 단계적 실험. single-attestation(33). "try X. See if that works. And then Y".

# - 정중한 정정 / 거부 (Polite Correction / Rejection) -
- id: ex-011
  expression: "So it's not true that X. We have to do that."
  function: polite but firm correction
  sources: [33]
  difficulty: 5
  note: 정중한 정정 공식. "You're wrong" 대신 "it's not true that X". Type D 서명. single-attestation(33).

- id: ex-012
  expression: "We have seen that"
  function: cite past case as evidence
  sources: [33]
  difficulty: 3
  note: 과거 사례 증거. 반박 어려움. single-attestation(33).

- id: ex-014
  expression: "I don't think that would be ideal"
  function: soft rejection, opinion-form rejection
  sources: [33]
  difficulty: 4
  note: 부드러운 거부. "don't think"로 의견 성격. single-attestation(33).

- id: ex-015
  expression: "I will not recommend that, especially for X"
  function: firm rejection with context
  sources: [33]
  difficulty: 5
  note: 단호한 거부 + "especially for X"로 맥락. 반박 차단. Type D 서명. single-attestation(33).

- id: ex-016
  expression: "I would not waste my time on X. Try on Y."
  function: direct priority advice
  sources: [33]
  difficulty: 5
  note: "waste my time" - 강한 우선순위 신호. single-attestation(33).

- id: ex-017
  expression: "I think your best option from what I'm hearing is X"
  function: optimal recommendation, source attribution
  sources: [33]
  difficulty: 4
  note: "from what I'm hearing" - 정보 출처 명시. single-attestation(33).

# - 부재자 회피 (Absent-Owner Deferral) -
- id: ex-018
  expression: "I don't see an issue on X but I'm not the owner. That will be [name]"
  function: defer to absent owner, polite evade
  sources: [33]
  difficulty: 5
  note: 정중한 회피 공식 - 개인 의견 + 권한 부인 + 부재자 지정. Type D 서명. single-attestation(33).

- id: ex-019
  expression: "let's check with [name] when he gets back from vacation"
  function: defer until return
  sources: [33]
  difficulty: 4
  note: 부재자 후속 명시. single-attestation(33).

- id: ex-020
  expression: "we need [name] to take the last call"
  function: final decision owner
  sources: [33]
  difficulty: 4
  note: "take the last call" = 최종 결정권. "make the final decision"보다 회의 체 자연스러움. single-attestation(33).

- id: ex-021
  expression: "I'm just speaking from what I have seen the previous work from [name]"
  function: opinion disclaimer, limit own judgment
  sources: [33]
  difficulty: 5
  note: 의견 면책. "제가 본 것만". 틀려도 책임 없음. single-attestation(33).

# - Status 보고 (Status Reporting with Disclaimers) -
- id: ex-022
  expression: "we did N loops of all the X tests, no red flag or no major issues as of today"
  function: time-bound regression report
  sources: [28]
  difficulty: 5
  note: "as of today" 필수 - regression 보고의 면책 공식. single-attestation(28)이지만 type D 핵심.

- id: ex-023
  expression: "We are still debugging it, but."
  function: in-progress status admission
  sources: [28]
  difficulty: 3
  note: "but" 뒤가 핵심. 진행 중 상태. single-attestation(28).

- id: ex-026
  expression: "we didn't find that there is a specific connection to X at this moment"
  function: no-fault disclaimer, temporal distance
  sources: [19]
  difficulty: 5
  note: past tense non-finding + temporal hedge. 부정도 인정도 아닌 회피의 황금표현. Type D 서명. single-attestation(19).

- id: ex-027
  expression: "Definitely we will do further."
  function: vague investigation promise, cooperation signal
  sources: [19]
  difficulty: 3
  note: "Definitely"로 협조, "further"로 범위 모호. (19)의 ex-026과 쌍. single-attestation(19).

- id: ex-028
  expression: "We will investigate it for finding the root cause of X"
  function: formal root cause commitment
  sources: [19]
  difficulty: 4
  note: "for finding" (not "to find") - 분석적 뉘앙스. single-attestation(19).

- id: ex-029
  expression: "the X team keeps things very close within their organization"
  function: team boundary deflection, blame redirect
  sources: [28]
  difficulty: 5
  note: 타 팀 비협조를 관용구로. 자기 책임 회피. single-attestation(28).

- id: ex-030
  expression: "I'll try and get you some answers. But right now, my understanding is X"
  function: soft commitment, limited promise
  sources: [28]
  difficulty: 5
  note: "I'll try"로 책임 완화 + "my understanding is"로 자기 한정. single-attestation(28).

- id: ex-031
  expression: "I don't recall X. I'm happy to take those and try and get you some answers."
  function: memory disclaimer + polite recover
  sources: [28]
  difficulty: 5
  note: "I don't remember" 대신 "I don't recall" - 더 전문적. 후속 필수. single-attestation(28).

# - Tip / 전문가 화법 (Expert Tip Delivery) -
- id: ex-032
  expression: "I'll give you some tip. So don't X too much. So you have to figure out Y. So that's my tip. That's all."
  function: critique-as-advice, direction correction
  sources: [28]
  difficulty: 5
  note: 강한 비판을 "tip" 틀 안에 - 정중한 방향 정정. Type D 서명. single-attestation(28).

# - Sandwich 피드백 / 품질 리뷰 (Sandwich Feedback) -
- id: ex-034
  expression: "the good news is with X, there is a Y trend going into Z"
  function: sandwich feedback open, positive first
  sources: [19]
  difficulty: 4
  note: 긍정 먼저. single-attestation(19). (19)의 sandwich 시퀀스 시작.

- id: ex-035
  expression: "The good thing is also that you guys were able to lower your X, quarter over quarter for the last Y quarters"
  function: improvement acknowledgment before push
  sources: [19]
  difficulty: 4
  note: "quarter over quarter" - 분기별 추세. 비판 전 개선 인정. single-attestation(19).

- id: ex-036
  expression: "You could see that, you know, X was a really rough year for you guys"
  function: direct but softened critique
  sources: [19]
  difficulty: 4
  note: "rough year" - 직접적 비판, "for you guys"로 familiar. single-attestation(19).

- id: ex-037
  expression: "I mean, we got to really drive that down"
  function: action expectation, reduction demand
  sources: [19]
  difficulty: 3
  note: "drive X down" - 메트릭 감소 액션 동사. single-attestation(19).

- id: ex-038
  expression: "X is a target that we want to target"
  function: numeric target setting
  sources: [19]
  difficulty: 3
  note: "target" 반복 - 숫자 강조. single-attestation(19).

- id: ex-039
  expression: "anyways, for the X, it looks like this year you guys are off to a good start"
  function: recovery acknowledgment, positive close
  sources: [19]
  difficulty: 3
  note: "off to a good start" - 회복 인정. "anyways"가 "그래도" - 비판 접어두기. single-attestation(19).

- id: ex-040
  expression: "with a little bit of a caveat in that we slightly reduced X. That's to align with Y."
  function: double-softened bad news + rationale
  sources: [19]
  difficulty: 5
  note: "a little bit of a caveat" + "slightly" + "to align with" 삼중 완화. Type D 서명. single-attestation(19).

- id: ex-042
  expression: "X is still in planning. It hasn't passed through the full approval loop yet. But this is the current view that we have."
  function: uncommitted roadmap disclaimer
  sources: [19]
  difficulty: 5
  note: 미확정 로드맵 정중 표현 - 상태 + 이유 + 시간 면책 3단. single-attestation(19).

# - 정중한 도전 (Polite Challenge) -
- id: ex-043
  expression: "how about the other vendors' status of the X trend? Is it similar or are they totally different independent?"
  function: competitor probe, system-vs-device deflection
  sources: [19]
  difficulty: 5
  note: system-level vs device-specific 구분. either-or로 명확한 답 강제. Type D 서명. single-attestation(19).

- id: ex-044
  expression: "Based on your X investigation, I haven't seen any Y"
  function: deferential challenge, observation as question
  sources: [19]
  difficulty: 5
  note: "I haven't seen X" - 질문을 관찰 진술로. 비대립적 도전. single-attestation(19).

- id: ex-045
  expression: "do you have any plan to X or not?"
  function: binary question, force clarity
  sources: [28]
  difficulty: 4
  note: "or not"으로 이항 질문 - 회피 차단. single-attestation(28). (33)의 "Is that okay or not?"가 유사 variant.

# - 후속 채널 / Action Item (Follow-up) -
- id: ex-046
  expression: "We will keep the discussion of this with my email"
  function: channel continue, email follow-up
  sources: [33]
  difficulty: 3
  note: "keep the discussion with email" - 후속 채널 명시. single-attestation(33).

- id: ex-047
  expression: "I can follow up with that"
  function: follow-up promise
  sources: [28]
  difficulty: 3
  note: 가장 자주 나오는 action item. "I'll check"보다 전문적. single-attestation(28).

- id: ex-048
  expression: "I'll keep you informed"
  function: ongoing update commitment
  sources: [28]
  difficulty: 3
  note: "keep you" - 지속성. 한 번 알리고 마는 게 아님. single-attestation(28).

- id: ex-049
  expression: "I'm happy to take those and try and get you some answers"
  function: polite accept with soft commitment
  sources: [28]
  difficulty: 4
  note: "happy to"로 수용 감정 + "try"로 책임 완화. single-attestation(28).

# - 발화 채움 / 협상 (Discourse / Negotiation) -
- id: ex-053
  expression: "We would like to have some opportunity X using Y"
  function: polite request as collaboration proposal
  sources: [33]
  difficulty: 5
  note: "give us X" 대신 "have some opportunity X" - 요청을 협력 제안으로. "opportunity"가 핵심. single-attestation(33).

- id: ex-055
  expression: "since I'll be doing X, I don't plan to do Y"
  function: role scope declaration
  sources: [33]
  difficulty: 4
  note: 역할 분담 명시. "Since I'll be doing X, I don't plan to Y". single-attestation(33).

- id: ex-057
  expression: "theoretically should not be a limitation, but X may impose some limitation"
  function: theory-vs-practice hedging
  sources: [33]
  difficulty: 5
  note: "이론상 한계 없지만, X가 한계 부과" - 이론 vs 실제 hedging. single-attestation(33).

```

> **DB 주의**: N=3 코퍼스라 2+ 교재 출현 표현은 거의 없다. 대부분 single-attestation이지만, type D에서 재귀하는 "진단적 권위", "정중한 정정", "부재자 회피", "as of today 면책", "tip 비판", "sandwich 피드백", "at this moment 회피" 패턴은 각 교재에서 독립적으로 등장하므로 패턴 자체는 robust하다. S8 한계 참고.

---

## S5. 영역 어휘 정수 (Domain vocabulary across this type)

Type D에서 재귀하는 도메인 용어. 하위 도메인별 그룹화.

### 결함/품질 지표 (Defect / Quality Metrics)
- **UEA** (Use Error Analysis) - 필드 에러 분석. (19) "the DDR5 UEA trend" - 에러 트렌드.
- **on-correct level** - 디바이스 수준 에러 수정. (19) "dramatic increase of the on correct level" - 에러 지표.
- **ABQ** (Average Bug Quality) - 복합 품질 메트릭. (19) "lower your ABQ quarter over quarter".
- **FA** (Failure Analysis) - 불량 분석. (19) "there were some FAs that really took a long time".
- **FA turnaround time** - 불량 분석 소요 시간. (19) "the FA turnaround time" - 기간 메트릭.
- **best in class** - supplier 중 최상. (19) "everything that we tested has been best in class".
- **red flag** - 주요 이슈 표시. (28) "no red flag or no major issues".
- **regression test** - 회귀 테스트. (28) "continually testing the regression test on the DMR system".

### 테스트/검증 (Test / Verification)
- **link training** - PCIe/CXL 링크 초기화. (28) "10,000 loops of all the link training tests".
- **link level test** - 링크 레벨 테스트. (33) "we don't need to test link level for on your card. We have to do that."
- **pre-qualification test** - 사전 자격 테스트. (33) "the current qualification test requires multiple device".
- **volume validation** - 양산 검증. (33) "in order for us to move on to the volume validation phase".
- **max configuration / full population** - 최대 구성/전체 탑재. (33) "the max configuration" = "full population".
- **EVB / ES** (Evaluation Board / Engineering Sample) - (19) "EVB and ES targeting this year".
- **POC** (Proof of Concept) - 개념 증명. (28) "this is more for the POC kind of work. It's not about any productization."

### 디버깅/진단 (Debugging / Diagnosis)
- **root cause** - 근본 원인. (19) "We will investigate it for finding the root cause of our devices."
- **miss rate** - 캐시 미적중률. (28) "If the miss rate is high, then flat memory mode doesn't work. Typically we want miss rate to be below 10%."
- **page conflict / cache line conflict** - 페이지/캐시라인 충돌. (33) "I can show you how to identify if you are having a page conflicts".
- **throttling** - 클럭/속도 강제 저하. (28) "throttling the core speeds".
- **power saving mode** - 전력 절약 모드. (28) "the system was going in power saving mode".

### CXL/메모리 아키텍처 (CXL / Memory)
- **flat memory mode** - CXL 메모리 flat 통합 운영. (28, 33) "if the miss rate is high, then flat memory mode doesn't work" / "both sockets in flat memory mode".
- **flat2LM** (flat 2-level memory) - native DDR + CXL 동일 주소 공간. (28) "the only flat2LM configuration that we have for 256 GB devices".
- **auto-numa / TPP** - 메모리 tiering 기술. (28) "even simple CXL, TPP or auto-numa is not going to help".
- **MLD** (Multi-Logical Device) - 하나의 CXL 장치를 다수 head node에 노출. (28) "How do you plan to divide the MLD?".
- **fabric manager** - CXL switch 장치 관리 SW. (28) "a function of the fabric manager on the XConn switch".
- **XConn** - 유일 CXL switch 벤더. (28) "the only available CXL switch on the market is through XConn".
- **CXL CMM** (CXL Compute Memory Module) - CXL 메모리 익스팬더. (19) "first gen CXL CMM BDR5".
- **near memory / far memory** - CXL type 2 tiering. (33) "512 gigabytes of near memory in your socket one".
- **CXL 3.0 / 3.1** - CXL 버전. (19, 33) "CXL 3.1 on PCIe6" / "your CXL3.0 early November".
- **montage silicon** - Montage 칩. (33) "since you are using the same PHY and the controller from montage".

### 플랫폼 (Platform)
- **DMR** (Development/Measurement Reference) - Intel 개발/측정 시스템. (28) "we're getting our DMR systems up and running".
- **PDK** (Platform Design Kit) - Intel 플랫폼 개발 키트. (28) "SK hynix have to check after get a pdk".
- **EMR** (Emerald Rapids) / **GNR** (Granite Rapids) - Intel 서버 플랫폼. (33) "I already recommend using the GNR" / "I would not waste my time on EMR".
- **RDC** (Resource and Documentation Center) - Intel 자료 사이트. (28).
- **Gaudi** - Intel GPU 제품. (28) "Gaudi is launched".
- **CDL** (Critical/Compute Design Lot) - 설계 검증 마일스톤. (19) "not actual official CDL form".
- **intercept** - 플랫폼 창을 맞추는 타이밍. (19) "we'll target to intercept that BMR".
- **POL** (Point of Load / Program of Record) - 공식 프로그램 상태. (19) "It's not an official POL yet".

### 타협/협상 (Coordination / Negotiation)
- **touch base** - 후속 회의 관용구. (28) "maybe we can touch base upon maybe after water".
- **approval loop** - 내부 승인 루프. (19) "It hasn't passed through the full approval loop yet".
- **take the last call** - 최종 결정권. (33) "we need Anu to take the last call".

---

## S6. 주간 학습 경로 (Weekly learning path)

5일(Mon-Fri) 계획. 3권이므로 교재 33(Ivan의 진단적 권위, 가장 화용론 가치 높음)과 28(다자간 이슈 review, 가장 다양한 역할)을 중심으로, 19(Microsoft evaluator 화법)을 보조로.

### 월: 교재 33 - 진단적 권위 5단계
- **읽기**: 교재 33의 S1(발화 아키텍처 5단계) + S2(회피 화법 5전략)
- **유의할 패턴**: S2 Move 1-5 (문제 재확인 -> hedged 진단 -> 실험 지시 -> 정중한 정정 -> 부재자 회피)
- **DB drill**: ex-001, ex-006, ex-008, ex-011, ex-018 (5개)
- **shadowing**: 교재 33 발췌 4 (flat memory mode 디버그 - Ivan의 5단계 모두 등장)

### 화: 교재 33 - 정중한 정정 + 단호한 거부 + 협상
- **읽기**: 교재 33의 S3(정중한 도전) + S4(협상·액션)
- **유의할 패턴**: "So it's not true that X. We have to do that." / "I will not recommend that, especially for X" / "We would like to have some opportunity X"
- **DB drill**: ex-011, ex-015, ex-016, ex-053, ex-055 (5개)
- **shadowing**: 교재 33 발췌 1 (링크 레벨 테스트 이견 - 정중한 정정)

### 수: 교재 28 - 다자간 이슈 review + status 보고
- **읽기**: 교재 28의 S1(issue review 4단계) + S2(회피 화법 6전략)
- **유의할 패턴**: "as of today" 면책 / "I'll try" soft commitment / "I don't recall" 정중한 메모리 한정 / "tip" 비판 완화 / "or not" 이항 질문
- **DB drill**: ex-022, ex-030, ex-031, ex-032, ex-045 (5개)
- **shadowing**: 교재 28 발췌 2 (Anil의 tip - 이 회의의 하이라이트)

### 목: 교재 28 + 19 - 중복 패턴 비교 + 마스터 DB drill
- **읽기**: 교재 28의 S3(정중한 도전) + 교재 19의 S2(회피 화법)의 "at this moment" / S3(sandwich 피드백) skimming
- **유의할 패턴**: "at this moment" 회피(19) vs "as of today" 면책(28) - 시간 한정 회피의 두 variant. "sandwich feedback" (19) vs "tip" 비판(28) - evaluator vs expert의 정중한 비판 두 mode.
- **DB drill**: ex-026, ex-027, ex-034, ex-035, ex-039, ex-040, ex-043 (7개)
- **shadowing**: 교재 19 발췌 4 (sandwich feedback) + 발췌 3 (caveat-first bad news)

### 금: Audrey 교정 + 전체 리뷰
- **Audrey dump**: 이 주의 Top 8 표현(ex-006, ex-011, ex-015, ex-018, ex-022, ex-026, ex-032, ex-040)을 가지고 Audrey 금요일 세션에서 register/pragmatics 교정
- **자녹(self-record)**: ex-011("So it's not true that X. We have to do that.")과 ex-015("I will not recommend that, especially for X")의 억양/강세 - "not true"와 "especially"의 강조점 확인
- **비교 학습**: S8의 한계(작은 N, single-attestation 다수)를 상기하며 과잉 일반화 금지
- **통합 리뷰**: S2의 7개 move를 처음부터 끝까지 통째로 한 번 복습 - 진단 사이클의 전체 흐름 체득

---

## S7. Audrey 금요일 교정 노트 (Friday correction notes)

### 교정받아야 할 Top 8 표현

1. **"if I'm understanding right the issue is that X"** (ex-001) - "understanding right"의 연음("/ɹ/" 약화), "the issue is that"의 intonation contour 확인.
2. **"So it's not true that X. We have to do that."** (ex-011) - "not true"의 강조점, "We have to"의 단호함 정도. "You're wrong"과의 register 차이.
3. **"I will not recommend that, especially for X"** (ex-015) - "especially for"의 강조, "will not" vs "won't"의 격식 차이.
4. **"most likely there could be X limitation"** (ex-006) - 이중 hedging의 억양. "most likely"과 "could be" 중 어디에 강조를 둘지.
5. **"I don't see an issue on X but I'm not the owner. That will be [name]"** (ex-018) - "I don't see"의 부드러움, "I'm not the owner"의 단호함, "That will be"의 지정 강도.
6. **"we did N loops of all the X tests, no red flag or no major issues as of today"** (ex-022) - "as of today"의 시점 한정 뉘앙스. 약속이 아닌 한정이라는 것을 억양으로 전달.
7. **"I'll give you some tip. So don't X too much. So you have to figure out Y. So that's my tip. That's all."** (ex-032) - "tip"의 비공식적 뉘앙스, "That's all"로 발언권 넘기는 억양, "you have to"의 강제 정도.
8. **"with a little bit of a caveat in that we slightly reduced X. That's to align with Y."** (ex-040) - "a little bit of a caveat"의 이중 완화 억양, "slightly"의 경감, "to align with"의 근거 제시 강도.

### 한국어-영어 pragmatic 대비 (native check 필요)

| 한국어 | 영어 | Audrey 확인 사항 |
|:---|:---|:---|
| "현재로서는 연관성 못 찾았습니다" | "we didn't find that there is a specific connection to X at this moment" | "at this moment"이 한국어 "현재로서는"과 같은지, 더 강한지. "Definitely we will do further"의 "Definitely"가 과도한 약속으로 들리는지. |
| "아닙니다, 틀렸습니다" | "So it's not true that X. We have to do that." | "it's not true"가 한국어 "사실이 아닙니다"와 register가 같은지, 더 직접적인지. "We have to do that"의 단호함 정도. |
| "아마 X일 겁니다" | "most likely there could be X limitation" | 이중 hedging("most likely" + "could be")가 한국어 "아마" 한 번보다 과도하게 들리는지, 적절한지. |
| "제가 결정 권한 없습니다" | "I don't see an issue on X but I'm not the owner. That will be [name]" | "I don't see an issue"가 개인 의견으로 들리는지, "I'm not the owner"가 정중한지. |
| "이건 안 됩니다" | "I will not recommend that, especially for X" | "will not"이 한국어 "안 됩니다"보다 강한지, "especially for X"의 맥락 붙이기가 자연스러운지. |
| "X에 시간 낭비하지 마세요" | "I would not waste my time on X. Try on Y." | "waste my time"이 도전적으로 들리는지, "I would"가 의견 성격을 유지하는지. |
| "팁 하나 드리자면" | "I'll give you some tip. ... That's all." | "tip"이 권위 차이를 허용하는지, "That's all"이 갑자기 끊는 느낌인지. |
| "잘하고 있습니다만" | "the good news is X / the good thing is also Y / but Z was a rough year" | 긍정 2회 후 "but" 전환이 한국어 "잘하고 있습니다만"과 같은지, 더 정중한지. |

### 자녹(self-record) 피드백 루프

- **정정 화법 3종**: ex-011("it's not true that X"), ex-014("I don't think that would be ideal"), ex-015("I will not recommend that") - 부드러운 거부 -> 단호한 거부의 강도 스펙트럼을 자녹하며 강세 차이 체득.
- **hedging 3종**: ex-006("most likely could be"), ex-007("I would not be surprised"), ex-057("theoretically should not be, but X may") - 진단 hedging의 강도 스펙트럼.
- **"as of today" / "at this moment"**: ex-022, ex-026 - 시간 한정 회피 두 variant를 자녹하고 뉘앙스 차이 비교.

---

## S8. 한계와 신뢰도 (Limitations and confidence)

### 코퍼스 크기 (N=3)

이 액기스는 **단 3권**에 기반한다. 다른 유형(A=9권, B=16권, C=9권)과 비교하면 현저히 작다. 신뢰도는 낮고, 과잉 일반화 위험이 크다. 아래 한계를 반드시 참고할 것.

### 코퍼스가 잡지 못하는 것

1. **오디오 없는 분석**: 3권 모두 오디오 .wav가 있으나 transcript 기반 분석이다. prosody(억양, 강세, 템포, pause)는 잡히지 않는다. "I will not recommend that"의 강도는 강세에 달려 있으나 이 액기스는 텍스트만 기반.
2. **중단/침묵 패턴 없음**: interruption, overlap, silence가 transcript에 드러나지 않는다. 디버그 회의에서 "tip" 전달 후의 침묵, "I will not recommend" 후의 반응 공백 등은 분석 불가.
3. **다자간 역학 미비**: facilitator-issuer-expert-intermediate-tester의 역할 전환이 실시간으로 어떻게 일어나는지, 발언권 쟁탈이 어떻게 일어나는지는 transcript 정적 분석으로 한계.
4. **비원어 표현의 화용론**: "totally different independent" (19, SK 비원어 표현)처럼 문법적으로 어색하지만 화용론적으로 날카로운 표현이 native에게 어떻게 받아들여지는지는 native check(Audrey) 없이 단정 불가.
5. **장기적 변화 없음**: 3권은 2025-08부터 2026-03까지 7개월에 걸친 샘플. Steve의 화법 진화, 파트너와의 관계 변화, 이슈의 누적 효과는 잡히지 않는다.

### Single-attestation vs Robust

- **2+ 교재 출현(robust) 패턴**: 사실상 없다. 3권 각각이 서로 다른 파트너(MSFT/Intel/Intel), 다른 이슈(UEA/miss rate/link training/flat memory mode/EMR BIOS), 다른 역할 구조를 가진다. 표현 단위의 직접 중복은 거의 없다.
- **대신 "패턴" 단위로 robust**: 진단적 권위 5단계(33), issue review 4단계(28), sandwich 피드백(19)은 각 교재에서 독립적으로 등장하는 type D의 구조적 패턴이다. 표현이 다르더라도 "문제 재진술 -> hedged 진단 -> 실험 지시 -> 정중한 정정 -> 후속 채널"의 사이클은 3권 모두에서 재귀한다. 이 패턴 레벨에서는 높은 신뢰도.
- **Single-attestation 표현 주의**: ex-011("So it's not true that X"), ex-015("I will not recommend that, especially for X"), ex-018("I don't see an issue on X but I'm not the owner"), ex-026("we didn't find a specific connection at this moment"), ex-032("I'll give you some tip")는 모두 single-attestation이다. 한 화자(Ivan, Anil, Mike)의 개인 화법일 수 있다. Audrey 교정 없이 과잉 일반화 금지.

### Steve가 과잉 일반화하면 안 되는 것

1. **"Intel 화법 = type D 화법" 착각**: 교재 33의 Ivan 화법은 Intel의 한 엔지니어 개인 화법일 수 있다. 모든 Intel 엔지니어가 "I would not be surprised to find that X"라고 말하는 것은 아니다. 28의 Anil은 "tip"을 쓰지만, 33의 Ivan은 "I will suggest you to do the test"를 쓴다. 동일 파트너 내에서도 개인차가 크다.
2. **"Microsoft = sandwich feedback" 단순화**: 19의 Mike/quality reviewer 화법은 Microsoft의 한 회의에서 나온 것이다. 모든 Microsoft 회의가 sandwich feedback을 쓰는 것은 아니다. 다른 유형(B/C)의 Microsoft 회의는 다른 register를 가질 수 있다.
3. **3권의 비율로 type D 전체 판단**: 3권은 모두 CXL/메모리 컨텍스트이다. type D의 다른 도메인(네트워킹, 스토리지, 소프트웨어 버그)에서는 다른 화법이 재귀할 수 있다. 이 액기스는 CXL/메모리 디버그 한정으로 읽을 것.
4. **"at this moment" / "as of today"만이 회피 패턴**: 이 두 표현은 19와 28에서 나온 것이다. 다른 회의에서는 "at this point", "currently", "as far as we can tell" 등 다른 variant가 쓰일 수 있다. 표현이 아니라 "시간 한정 + 부정 아닌 비부정 + 협조 표시"라는 패턴을 학습할 것.

### 추정 신뢰도 등급
- **패턴 레벨(진단 사이클, 부재자 회피, 시간 한정, sandwich 피드백)**: 중간-높음 (3권 독립 재귀)
- **표현 레벨(개별 표현)**: 낮음-중간 (대부분 single-attestation)
- **도메인 어휘**: 중간 (CXL/메모리 특화, 다른 도메인에는 적용 제한)
- **화용론 강도**: 중간 (Audrey native check 필요한 표현 다수)

---

*Essence E-D - 이슈/품질 디버깅 정수. 3권(19, 28, 33) 기반. 마스터 DB 40 entries. 작성: 2026-09-02.*
