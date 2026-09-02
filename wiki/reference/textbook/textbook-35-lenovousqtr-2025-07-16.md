---
textbook_id: 35
meeting: Lenovo US QTR
date: 2025-07-16
type: B (roadmap/supply alignment) - confirmed after reading
partner: Lenovo ISG (Nicky Dillinger - procurement, Eddie - platform memory architect, Greg - procurement, Samantha - architect)
sk_side: DK Park, Chung Ha (marketing), Theo Kim (sub amp team), Eugene (DLM product planning lead), Jerry (DLM solution product planning), Steven Scott (Lenovo account manager), Jason (China DFAE), Maggie
duration_words: 2907 (transcript truncated mid-roadmap)
audio: repo/webex-audio/2025-07-16 08 21 54_EN_LenovoUSQTR-extracted.wav
transcript: repo/webex-audio/2025-07-16 08 21 54_EN_LenovoUSQTR-extracted-rag-corrected.txt
created: 2026-09-01
tags: [textbook, english, lenovo, quarterly-review, roadmap, ddr4-eol, ddr5, supply-alignment, bmc, venice, agisa]
---

# Textbook 35 - Lenovo US QTR (2025-07-16)

> **회의 유형**: B (roadmap/supply alignment) - 분기 리뷰 + 로드맵 정합 + DDR4 EOL 협상
> **학습 가치**: 공급자(SK Hynix) vs 고객(Lenovo) 협상 구조, EOL pushback 화법, 타임라인 조정 언어, 스펙 pushback
> **Audrey 관점**: 이 회의는 "분기 로드맵 발표 + 고객 공급 pushback"의 전형. 네가 SK Hynix 입장(공급자, 발표자)이든, 파트너 입장(고객, 요구자)이든 둘 다 배워야. 특히 Nicky의 DDR4 EOL pushback은 협상 영어의 교과서.

> **주의**: 이 전사본은 로드맵 발표 도중(24GB Arlim roadmap 시작 부분)에서 잘려 있음. 분석은 전사본에 있는 부분만 기반.

---

## 1. 발화 아키텍처 - 발표자의 설명 설계 (4단계)

이 회의는 두 명의 SK Hynix 발표자가 단계적 발표를 진행한다. Chung Ha(마케팅, market outlook)와 Theo Kim(sub amp team, roadmap). 각각 **고정된 화법 공식**을 사용.

### 단계 1: 맥락 설정 (Market Context Framing) - Chung Ha

Chung Ha는 데이터부터 시작한다. "우리가 왜 이 이야기를 하는가"가 아니라 "시장이 이렇다"로 시작.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `X is expected to grow by Y% in this year and Z% in the next year` | "DLM demand is expected to grow by 16% in this year and 15% in the next year" | 성장률 프레이밍 - 구체 수치로 권위 |
| `The leading application for this growth are X and Y` | "The leading application for this growth are HBM and server" | 성장 동기 귀인 |
| `X's growth rate is Y% this year and Z% next year` | "HBM's growth rate is 83% this year and 26% in next year" | 제품별 성장률 분리 명시 |

**Audrey 교훈**: 분기 리뷰 발표는 "결론"으로 시작하지 않는다. **"데이터"**로 시작한다. "X is expected to grow by Y%" - 이 공식을 외워. 회의에서 시장 전망을 말할 때, "I think the market will grow"가 아니라 "X is expected to grow by Y%"로 수치를 명시해야 발표자 권위가 선다.

### 단계 2: 공급 제약 프레이밍 (Supply Constraint Framing)

수요 설명 후, 공급 제약을 연결한다. "성장은 있는데 공급이 안 따라" 구조.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The X is projected to constrain through Y` | "The vapor capacity for conventional DLM is projected to constrain through the next year" | 공급 제약 선언 |
| `So, it will make X in Y` | "So, it will make supply shortage in the second half of this year" | 귀결 - 부족 예고 |
| `But X's Y is quite lower than Z because of...` | "But HBM4's big ratio is quite lower than DL5 because of net-dive penalty and use penalty" | 비교 부연 - 제약의 이유 |

**Audrey 교훈**: "X is projected to constrain through Y" - "내년까지 제약될 것으로 예상된다" - 공급 제약을 선언하는 공식. "will be tight"가 아니라 "is projected to constrain"이 전문가 표현이다. 이게 SK Hynix가 "공급이 부족할 수 있다"는 것을 권위 있게 말하는 화법이다.

### 단계 3: 패러다임 전환 선언 (Paradigm Shift Declaration)

"supply paradigm is shifted"로 시장 구조 변화를 선언한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So, X is shifted` | "So, supply paradigm is shifted" | 패러다임 전환 선언 - 강한 명제 |
| `X makes Y limited` | "Capex increase for HBM infrastructure makes the DLM supply limited" | 인과 - 자본 집중이 공급 제약 |
| `X with Y will turn into Z` | "DLM cycle with oversupply in the past year will turn into the milder and shorter DLM cycle with limited big growth in the future" | 과거 vs 미래 대비 - "will turn into" |

**Audrey 교훈**: "paradigm is shifted"는 강한 선언이다. "the situation changed"가 아니라 "paradigm is shifted" - 사업 구조 자체가 바뀌었다는 프레이밍. 이게 SK Hynix가 "공급 여유는 끝났다"는 것을 선언하는 화법. 회의에서 큰 변화를 설명할 때 써라.

### 단계 4: 질문 유도 (Question Invitation)

발표자는 매 섹션 끝에 같은 패턴으로 질문을 유도한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So, do you have questions or let me move to X?` | "So, do you have questions or let me move the supermarket outlook?" | 질문 유도 + 다음 주제 암시 |
| `Do you have any question or comments?` | "Do you have any question or comments?" | 표준 질문 유도 |
| `If not we can move to X` | "If not we can move to roadmap slide" | 침묵 처리 - 자연스러운 전환 |

**Audrey 교훈**: "do you have questions or let me move to X?" - 질문을 유도하면서 동시에 다음 주제를 암시하는 이중 기능 화법. 단순 "Any questions?"보다 능숙한 발표자 화법이다. 질문 없으면 자연스럽게 "let me move to X"로 넘어간다. 이 "or" 연결을 외워.

### 단계 5: 로드맵 발표 패턴 (Roadmap Presentation) - Theo Kim

Theo Kim은 로드맵을 타임라인 기반으로 나열한다.

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `The X product is EOL in Y` | "the 1A 4800 product is EOL in July 25" | EOL 선언 - 명시적 종료 |
| `X is scheduled for CS in Y and mass production in Z` | "The 7200 product is 1B scheduled for CS in June and mass production in January 26" | 이중 마일스톤 - CS + MP |
| `X is scheduled in Y` | "9200 CS is scheduled in November 26" | 단일 마일스톤 |

**Audrey 교훈**: 로드맵 발표는 "scheduled for CS in X and mass production in Y" - CS(Customer Sample)와 MP(Mass Production) 두 마일스톤을 명시하는 게 SK Hynix 표준 패턴. 회의에서 일정을 말할 때 "we will release in Q3"가 아니라 "scheduled for CS in September and mass production in April 26"으로 두 단계로 명시해야 - 정밀한 일정 관리 인상을 준다.

---

## 2. 회피·포장 화법 (Hedging & Deflection)

이 회의의 **진짜 학습 가치**. SK Hynix가 Lenovo의 강한 pushback을 어떻게 정중하게 회피하는지. 그리고 이게 네가 회의에서 직접 써야 할 화법이다.

### 전략 1: 부정 → "But" → 검토 약속 (Negation-But-Review)

가장 중요한 패턴. "계획 없다"고 인정하되, 즉시 "검토 중"으로 전환.

| 약점 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR4 연장 불가 | "Unfortunately currently we don't have plan to extend DDR4 including components and module. **But we also reviewing how to deal our customer demand. So, after reviewing it then we can share it.**" | "유감스럽게도 현재 DDR4 연장 계획이 없습니다. **하지만 고객 수요 대응 방안을 검토 중입니다. 검토 후 공유하겠습니다.**" |

**패턴 공식**: `Unfortunately currently we don't have plan to X. But we also reviewing Y. So, after reviewing it then we can share it.`

**Audrey 교훈**: 영어 회의에서 "없습니다"는 절대 단독으로 끝내지 마라. "we don't have plan to X. But we also reviewing Y." - 부정 뒤에 무조건 "But + 검토"를 붙여. "Unfortunately"를 부정 앞에 써서 유감을 표시하고, "But we also reviewing"로 즉시 대안을 제시. 한국어 "안 됩니다, 그런데 검토해 보겠습니다"의 영어 버전이 이것이다. "검토 후 공유하겠습니다"는 "after reviewing it then we can share it" - "can share"가 미래 약속의 부드러운 표현.

### 전략 2: 차트 오류 인정 + 수정 약속 (Chart Error Admission)

Lenovo가 차트의 불일치를 지적하자, "업데이트해야 함"으로 인정한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| 2026년 DDR4 볼륨 표시 문제 | "So, it should be updated. So, measuring the cut in the middle of 2026 and DDR4 for DDR4." | "그건 업데이트되어야 합니다. 2026년 중반 DDR4 컷 측정에 관한 것이니까요." |

**패턴 공식**: `So, it should be updated. So, [clarification].`

**Audrey 교훈**: 차트나 데이터 오류를 지적당했을 때, 변명하지 마라. "It should be updated" - "업데이트되어야 한다" - 깔끔하게 인정하는 화법. 한국어로는 "제가 확인해 보겠습니다"로 시간을 끌지만, 영어는 "it should be updated"로 즉시 인정하고 넘어간다.

### 전략 3: 제3사 책임 분리 (Third-Party Boundary)

BMC 컴포넌트 책임이 SK Hynix 밖에 있음을 명시한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| BMC 책임 소재 | "Again, ouRDIM, our Andes team doesn't own the components. There's anotheRDIM that is owning those." | "당사 Andes 팀은 컴포넌트를 담당하지 않습니다. 해당 컴포넌트를 담당하는 별도 팀이 있습니다." |

**패턴 공식**: `Our X team doesn't own Y. There's another team that is owning those.`

**Audrey 교훈**: 책임이 다른 팀에 있을 때, "I don't know"가 아니라 "our team doesn't own X. There's another team that is owning those" - 소유권 경계를 명시. 이게 "모르겠다"가 아니라 "내 담당이 아니다"를 정중하게 말하는 화법이다. 한국어 "담당 부서가 다릅니다"의 영어 버전.

### 전략 4: 모른다고 솔직히 인정 (Honest Ignorance)

담당 외 질문에는 솔직히 "I don't know"를 인정한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| DDR5 컴포넌트 구매 여부 | "I don't know. I don't know. Because I don't, again, I don't own the procurement for them." | "모릅니다. 모릅니다. 제가 그 부분 조달을 담당하지 않기 때문입니다." |

**패턴 공식**: `I don't know. Because I don't own X for them.`

**Audrey 교훈**: "I don't know"가 항상 나쁜 것은 아니다. 단, 이유를 붙여라. "I don't know. Because I don't own X" - "모른다. 왜냐하면 내 담당이 아니기 때문이다." 이유가 있으면 "I don't know"도 전문적으로 들린다. 단답 "I don't know"는 약하지만, "I don't know because I don't own X"는 책임의 경계를 명시하는 정중한 답이다.

### 전략 5: 타임라인 우위 주장 (Timeline Advantage)

Lenovo보다 먼저 BIOS를 받아 테스트할 수 있다는 우위를 강조한다.

| 상황 | 원문 화법 | 번역 |
|:---|:---|:---|
| AMD BIOS 수급 시점 | "We are going to receive a head of a Lenovo. We are at least a couple of weeks ahead of Lenovo." | "Lenovo보다 먼저 받을 예정입니다. 당사가 최소 몇 주 앞서 있습니다." |

**패턴 공식**: `We are going to receive a head of X. We are at least a couple of weeks ahead of X.`

**Audrey 교훈**: "we are at least a couple of weeks ahead of X" - 타임라인 우위를 주장하는 화법. "우리가 더 빠르다"가 아니라 "we are ahead of X by Y weeks" - 구체적 시차로 우위를 표시. 회의에서 경쟁사나 파트너 대비 우위를 말할 때, "ahead of X by Y"로 구체화해야 신뢰가 간다.

---

## 3. 정중한 도전 화법 (Lenovo 측 질문자)

Lenovo의 Nicky가 SK Hynix 발표에 도전하면서도 정중하게 질문하는 패턴. **네가 직접 써야 할 화법**이다. 이 회의에서 Nicky는 교과서적 pushback을 보여준다.

### 질문 유형 1: EOL 연장 요청 (EOL Extension Request)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we hope you guys have some good news for us on last quantities on continuing support especially for X` | "we hope you guys have some good news for us on last quantities on continuing support especially for the component side of things" | "좋은 소식이 있길 바란다" - 정중한 요청 + "especially"로 우선순위 명시 |

**Audrey 교훈**: "we hope you have some good news for us on X" - "좋은 소식이 있길 바란다" - 정중한 요청의 화법. "We want X"가 아니라 "We hope you have good news on X" - 요구를 희망으로 포장. "especially for Y"로 우선순위를 명시. 이게 파트너에게 EOL 연장을 요구할 때 쓰는 정중한 화법이다.

### 질문 유형 2: 데이터 불일치 지적 (Data Inconsistency Challenge)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `Can I ask why that chart shows X if Y?` + `Is that for other customers?` | "Can I ask why that chart shows into 2026 if Lenovo is not going to be extended? Is that for other customers?" | "왜 차트에 X가 있는가?" + "다른 고객용인가?" - 직접 도전 + 대안 해석 제시 |

**Audrey 교훈**: "Can I ask why X if Y?" - "Y인데 왜 X인가요?" - 차트의 불일치를 직접 질문하는 화법. "if Y"로 전제를 명시한 후 "why X"로 도전. 이게 "I don't understand the chart"가 아니라 "your chart is inconsistent with what you said"를 정중하게 표현하는 화법이다. "Is that for other customers?"로 대답을 유도하는 것도 중요 - 답을 알려주지 말고 질문으로 끝내면 발표자가 직접 설명하게 된다.

### 질문 유형 3: 비즈니스 임팩트 명시 (Business Impact Stating)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `we can't ship X without Y` + `So, no Z if we can't get Y` | "we can't ship servers without the components. So, no DDR5 sales if we can't get DDR4 components." | "Y 없으면 X 못 판다" - 직접적 비즈니스 임팩트 명시 |
| `If we don't take it from you guys now, we're going to need X to try to accelerate Y` | "if we don't take it from you guys now, we're going to need support and responsiveness and everything on the component side for DDR5 to try to accelerate the plans of changing those BMCs" | "지금 안 주면, 우리가 가속화해야 한다" - 조건부 요구 |

**Audrey 교훈**: "we can't ship X without Y" - 이게 회의에서 **가장 강력한** pushback 화법이다. "It would be difficult"가 아니라 "we can't ship" - 부정의 강도를 최대로. 그리고 "So, no Z if we can't get Y"로 비즈니스 임팩트를 명시. 한국어 "그러면 서버 출하를 못 합니다"의 영어 버전이 이것이다. Nicky는 "we can't ship servers without the components"로 직접적으로 비즈니스 차질을 선언한다. 이게 협상에서 레버리지를 만드는 화법이다.

### 질문 유형 4: 업계 전체 이슈로 확장 (Industry-Wide Framing)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `I would say this is X wide` | "I would say this is industry wide" | "업계 전체 문제" - 이슈 격상 |
| `And like I said, this is something that's not unique to X` | "And like I said, this is something that's not unique to Lenovo" | "Lenovo만의 문제가 아니다" - 동병상련의 논리 |
| `we have some large cloud customers. I think you guys know who that is` | "we have some large cloud customers. I think you guys know who that is that we build for" | "대형 클라우드 고객도 같은 문제" - 암시적 동맹 |

**Audrey 교훈**: "this is something that's not unique to X" - "X만의 문제가 아니다" - 개별 회사 이슈를 업계 전체 이슈로 격상하는 화법. "우리만의 문제가 아니라 다 같은 문제다"라고 하면, 공급자가 "Lenovo 특별 케어"가 아니라 "업계 대응"으로 받아들이게 된다. "I think you guys know who that is" - 클라우드 고객 이름을 직접 말하지 않고 암시하는 것도 화법이다. 구체 이름을 안 대면서 "너도 알 만한 대형 고객"이라는 압박을 준다.

### 질문 유형 5: 제3자 책임 명시 (Third-Party Constraint)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `since we're reliant on a third party outside of you and us, it's problematic because we can't control it` | "since we're reliant on a third party outside of you and us, it's problematic because we can't control it" | "제3자에 의존해서 통제 불가" - 책임 한계 명시 |
| `now that this has been designed in, it's very difficult for us OEMs to make that change` | "now that this has been designed in, it's very difficult for us OEMs to make that change" | "이미 설계되어 변경 곤란" - 기술적 제약 명시 |

**Audrey 교훈**: "since we're reliant on a third party, it's problematic because we can't control it" - 제3자 의존성을 명시하면서 "we can't control"로 통제 불가를 선언. 이게 "우리 탓이 아니다"를 정중하게 말하는 화법이다. "now that this has been designed in" - "이미 설계에 들어갔다" - 이미 결정된 사실을 명시해서 변경 비용을 강조. 회의에서 책임 회피가 아니라 구조적 제약을 설명할 때 써라.

### 질문 유형 6: 확인식 짧은 질문 (Quick Confirmation)

| 화법 공식 | 원문 | 기능 |
|:---|:---|:---|
| `So, this is both X and Y?` | "Okay, so this is both server and client?" | 짧은 확인 - 발표 흐름 유지 |
| `So the current situation requiring X, applies to Y in common?` | "So the current situation requiring BMC, requiring DDR4, applies to Intel and AMD system in common?" | "공통 적용인가?" - 범위 확인 |
| `Would that be a correct understanding?` | "Would that be a correct understanding?" | "제 이해가 맞습니까?" - 정중한 확인 마무리 |

**Audrey 교훈**: "Would that be a correct understanding?" - 이게 회의에서 **가장 유용한** 확인 화법 중 하나. 긴 발언 후 "이게 맞습니까?"로 확인하면, 발표자가 직접 확인/정정하게 된다. "Is that right?"보다 정중하고 "Do you agree?"보다 구체적. 자기 이해를 명시하고 상대 확인을 요구하는 이중 기능. 이걸 외워.

---

## 4. 협상·액션 화법 (Negotiation & Action Items)

이 회의의 **핵심 학습 가치**. Section 4가 Type B 회의에서 가장 중요. DDR4 EOL 협상과 타임라인 조정 언어를 중심으로.

### 4.1 EOL 협상 화법 (EOL Negotiation)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| EOL 연장 희망 | Nicky | "we hope you guys have some good news for us on last quantities on continuing support especially for the component side of things" | 정중한 EOL 연장 요청 |
| 비즈니스 임팩트 명시 | Nicky | "we can't ship servers without the components. So, no DDR5 sales if we can't get DDR4 components" | 강한 레버리지 - DDR5 매출 연결 |
| 업계 공통 문제 격상 | Nicky | "I would say this is industry wide. ... this is something that's not unique to Lenovo" | 개별 문제를 업계 이슈로 |
| 대형 고객 암시 | Nicky | "we have some large cloud customers. I think you guys know who that is" | 압박 - 클라우드 고객 동맹 암시 |
| 제3자 통제 불가 | Nicky | "since we're reliant on a third party outside of you and us, it's problematic because we can't control it" | 구조적 제약 명시 |
| 이미 설계된 제약 | Nicky | "now that this has been designed in, it's very difficult for us OEMs to make that change" | 기술적 변경 비용 강조 |
| 가속화 요구 | Nicky | "if we don't take it from you guys now, we're going to need support and responsiveness and everything on the component side for DDR5 to try to accelerate the plans" | 조건부 요구 - "if not now, then accelerate" |
| 정중한 거절 | SK Hynix | "Unfortunately currently we don't have plan to extend DDR4" | 부정 - "Unfortunately"로 유감 표시 |
| 검토 약속 | SK Hynix | "But we also reviewing how to deal our customer demand. So, after reviewing it then we can share it" | 부정 뒤 대안 - "검토 후 공유" |
| 차트 인정 | SK Hynix | "So, it should be updated" | 데이터 오류 인정 |

**Audrey 교훈**: EOL 협상의 핵심 구조:
1. **고객**: "we hope you have good news" (정중 요청) → "we can't ship without Y" (비즈니스 임팩트) → "this is industry wide" (격상) → "if not now, accelerate" (조건부 요구)
2. **공급자**: "Unfortunately we don't have plan" (부정) → "But we also reviewing" (대안) → "after reviewing we can share" (후속 약속)

이 4단 구조를 외워. 네가 EOL을 통보받거나 통보할 때, 이 패턴을 써.

### 4.2 타임라인 조정 화법 (Timeline Coordination)

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 마일스톤 명시 | Theo | "The 7200 product is 1B scheduled for CS in June and mass production in January 26" | 이중 마일스톤 - CS + MP |
| CS 시점 질문 | Jason | "I got a question for the 8000 sample support with the 1C nanometer product" | 기술적 타임라인 질문 |
| 테스트 시스템 수급 | Jason | "How does the CS by has a 8000 CS. So that's how it's doing the application testing in Venice system" | 테스트 환경 조정 질문 |
| 현재 상태 | Theo | "The currently we are receiving the Venice CR system from AMD and also Lenovo Taiwan. So we can start to testing within couple of weeks" | 진행 상황 + 기대 시점 |
| BIOS 수급 우위 | Jason | "We are going to utilize AMD BIOS as a release. So we are going to receive a head of a Lenovo. We are at least a couple of weeks ahead of Lenovo" | 타임라인 우위 주장 |
| 확인 요청 | Jason | "So once the CS release from Hynix at the time of September, can you think that that is completed application testing in AMD CLB?" | 타임라인 일치 확인 |
| 검증 요구 | Nicky | "we want to verify that it is tested and approved with the necessary testing like a MIM is completed in the application system" | 검증 조건 명시 |

**Audrey 교훈**: 타임라인 조정 화법의 핵심:
1. **CS + MP 이중 명시**: "scheduled for CS in X and mass production in Y" - 단일 일정이 아니라 두 마일스톤으로 명시
2. **진행 상황 + 시점**: "currently we are receiving X. So we can start testing within Y" - 현재 상태와 기대 시점을 연결
3. **우위 주장**: "we are at least a couple of weeks ahead of X" - 구체적 시차로 우위
4. **검증 요구**: "we want to verify that it is tested and approved with the necessary testing" - 단순 "테스트 완료"가 아니라 "검증, 승인, 필수 테스트"로 조건 명시

### 4.3 Action Item 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 후속 약속 | SK Hynix | "after reviewing it then we can share it" | "검토 후 공유" - 부드러운 후속 |
| 확인 요청 | Jason | "please let us know that we want to verify that it is tested and approved" | "알려달라" + "검증 원한다" - 이중 요청 |
| 별도 일정 제안 | DK Park | "I sent a separate one due to the limited time. I'd like to explain that one later on in another day. I can explain it to Greg later on" | 별도 회의 제안 - 시간 부족 시 |

**Audrey 교훈**: 
- "after reviewing it then we can share it" - "검토 후 공유하겠다" - 명시적 약속이 아니라 조건부 후속. "we will share"가 아니라 "we can share" - 가능성을 표시. 이게 "반드시 공유하겠다"가 아니라 "검토가 끝나면 공유할 수 있다"는 부드러운 표현이다.
- "I'd like to explain that one later on in another day. I can explain it to Greg later on" - 시간 부족으로 미룰 때 "later on in another day"로 별도 일정을 제안. "다음에 따로"라고 하지 말고 "another day" + "I can explain it to X"로 담당자를 명시.

### 4.4 스펙 Pushback 화법

| 화법 | 발화자 | 원문 | 기능 |
|:---|:---:|:---|:---|
| 설계 이슈 명시 | Jason | "One of the design point is the command address signal is not meeting the AMD MBTG" | 스펙 미충족 명시 - "is not meeting" |
| 지연 언급 | Jason | "I was told that there is some delay with the CIB. The amount of availability" | 지연 사실 - "there is some delay" |
| 이유 설명 | Jason | "The reason why I am asking is the AMD Venus Agisa release note" | 질문 이유 명시 - "The reason why I am asking is..." |
| 출시 노트 인용 | Jason | "At the time of the 1x by 4, 8000 is supported in July and August. And 2x by 4 is following the August" | 공식 문서 인용 - 시점 명시 |
| 호기심 표현 | Jason | "So my curiosity is that even the Agisa is releasing in September. How does the SK Hynix can test 8000 testing with 16GB and 32GB to FIA?" | "curiosity"로 정중 도전 |

**Audrey 교훈**: 스펙 pushback 화법의 핵심:
1. **"is not meeting"**: "doesn't meet"이 아니라 "is not meeting" - 진행형으로 현재 미충족 상태를 강조
2. **"The reason why I am asking is..."**: 질문 전 이유를 명시하면, 단순 호기심이 아니라 근거 있는 도전이 됨
3. **"my curiosity is that..."**: "I want to know"가 아니라 "my curiosity is" - 질문을 지적 호기심으로 포장. 정중한 도전 화법
4. **공식 문서 인용**: "At the time of X, Y is supported in Z" - 파트너 공식 노트를 인용하면 도전의 근거가 된다

---

## 5. 도메인 어휘 (Domain Vocabulary)

이 회의에서 쓰인 DLM/서버/BMC/EOL 관련 전문 용어. 각 용어의 **정확한 쓰임새**와 발화 맥락을 함께.

| 용어 | 뜻 | 이 회의에서의 쓰임새 |
|:---|:---|:---|
| **DLM** (Dynamic Linear Memory?) | SK Hynix 메모리 사업 총칭 | "DLM demand is expected to grow by 16% in this year" - DLM 전체 수요 |
| **HBM** (High Bandwidth Memory) | 고대역폭 메모리 | "HBM's growth rate is 83% this year and 26% in next year" - HBM 성장률 |
| **CSP** (Cloud Service Provider) | 클라우드 서비스 제공자 | "increased server demand of US and China CSP" - CSP 수요 동기 |
| **capex** (Capital Expenditure) | 자본 지출 | "Industry DLM capex is increased to $43 billion in this year" - 자본 지출 규모 |
| **vapor capacity** | 웨이퍼 생산 능력 (전사 오류 가능) | "The vapor capacity for conventional DLM is projected to constrain through the next year" - 생산 능력 제약 |
| **big ratio** (비트 비율?) | 비트 밀도 비율 | "HBM4's big ratio is quite lower than DL5 because of net-dive penalty and use penalty" - 비트 성장률 |
| **EOL** (End of Life) | 제품 생산 종료 | "The one life 4800 product is EOL and the end of the 25" - EOL 선언 |
| **BMC** (Baseboard Management Controller) | 메인보드 관리 칩 | "the BMC on every motherboard, previously, suppliers that do the BMCs, they did not have DDR5 components qualified" - BMC DDR4 의존 |
| ** motherboard** | 메인보드 | "the only way for us to move to DDR5 ... would be for us to re-spin every motherboard" - 메인보드 재설계 필요 |
| **re-spin** | (메인보드) 재설계 | "re-spin every motherboard that we have already launched" - 이미 출시된 보드 재설계 |
| **quibs** | (작은 SMD 컴포넌트, 전사 오류 가능) | "I think it's one component or two components per motherboard. So, little quibs, right?" - 소형 컴포넌트 |
| **CS** (Customer Sample) | 고객 샘플 (개발 단계) | "scheduled for CS in June and mass production in January 26" - CS + MP 이중 마일스톤 |
| **MP** (Mass Production) | 양산 | "mass production in January 26" - 양산 시점 |
| **1A / 1B / 1C** | 공정 노드 세대 | "The 7200 product is 1B scheduled for CS" / "The 800 product is 1C nanometer" - 공정 노드 명시 |
| **Venice** | AMD 서버 플랫폼 코드명 | "the application testing in Venice system" / "B5 systems are finishing up the August stream" - AMD 플랫폼 |
| **Agisa** | AMD BIOS 릴리즈 명 | "the AMD Venus Agisa release note" / "Agisa 0062" / "Agisa 0070" - BIOS 버전 |
| **CR** (Customer Reference) | 고객 참조 보드 | "we are receiving the Venice CR system from AMD" - CR 보드 수급 |
| **CRB** (Customer Reference Board) | 고객 참조 보드 | "you can take a look at the SGA high mix source can access to the CRB schematics" - CRB 스키메틱 |
| **AVL** (Approved Vendor List) | 승인된 벤더 목록 | "we can give it to AMD to put that one into their AVL" - AMD 승인 목록 |
| **CLB** | (AMD 테스트 환경) | "completed application testing in AMD CLB?" - AMD 테스트 완료 확인 |
| **MBTG** | AMD 사양/요구사항 | "the command address signal is not meeting the AMD MBTG" - 스펙 미충족 |
| **MIM** | (테스트 항목, 전사 오류 가능) | "like a MIM is completed in the application system" - 필수 테스트 |
| **AST2600 / AST2800** | ASPEED BMC 칩 | "our DCS-C using AST2600" / "next generation of AST kind of 2800" - BMC 칩 세대 |
| **DCS-C** | Lenovo 서버 제품군 | "our DCS-C using AST2600 and that chip is using a 16 gigabit DDR4 by 16 device" - 서버-BMC 매핑 |
| **August stream / purchase stream / Turin** | 서버 플랫폼 세대 | "B5 systems are finishing up the August stream" / "OEM customers as well as cloud service provider using purchase stream and Turin" - 플랫폼 세대 |
| **end of marketing** | 출하 종료 (EOL 전 단계) | "some of the platforms that are, we are end of marketing here and soon" - 출하 종료 단계 |
| **longevity support** | 장기 지원 | "We'll need some longevity support on that" - 장기 지원 요청 |
| **deep-seek** | AI 모델 (DeepSeek) | "China major CSP prospects are increased to 54% after deep-seek introduction" - AI 모델 영향 |
| **tariff effect** | 관세 효과 | "there is also pouring demand from US tariffs" / "we still looking into the tariff effect on the economy" - 관세 영향 |
| **big growth** | 비트 성장 | "difficulty to big growth by capex increase" / "limited big growth in the future" - 비트 성장 둔화 |
| **DMY trend** | (시장 트렌드, 전사 오류 가능) | "this is a DMY trend. It's just showing the trend" - 시장 트렌드 차트 |

---

## 6. 표현 DB (Expression Database)

이 회의에서 학습 가치가 있는 표현 52개. 각 엔트리는 카테고리·기능·난이도·화자 역할로 tagging됨.

```yaml
# -- 발표 설계 (Presentation Architecture) --
- id: m35-001
  expression: "X is expected to grow by Y% in this year and Z% in the next year"
  category: presentation_framing
  function: growth_rate_stating
  speaker_role: presenter
  difficulty: 3
  context: "DLM demand is expected to grow by 16% in this year and 15% in the next year"
  note: 분기 리뷰 발표 시작 화법 - 구체 수치로 권위

- id: m35-002
  expression: "The leading application for this growth are X and Y"
  category: presentation_framing
  function: growth_attribution
  speaker_role: presenter
  difficulty: 3
  context: "The leading application for this growth are HBM and server"

- id: m35-003
  expression: "X is projected to constrain through Y"
  category: supply_constraint
  function: constraint_forecast
  speaker_role: presenter
  difficulty: 4
  context: "The vapor capacity for conventional DLM is projected to constrain through the next year"
  note: 공급 제약 선언 공식 - "will be tight"보다 전문적

- id: m35-004
  expression: "So, it will make X in Y"
  category: consequence_stating
  function: outcome_prediction
  speaker_role: presenter
  difficulty: 3
  context: "So, it will make supply shortage in the second half of this year"

- id: m35-005
  expression: "So, X is shifted"
  category: paradigm_declaration
  function: structural_change
  speaker_role: presenter
  difficulty: 5
  context: "So, supply paradigm is shifted"
  note: 강한 선언 - 패러다임 전환

- id: m35-006
  expression: "X with Y will turn into Z"
  category: contrast_future
  function: before_after_transition
  speaker_role: presenter
  difficulty: 4
  context: "DLM cycle with oversupply in the past year will turn into the milder and shorter DLM cycle with limited big growth in the future"

- id: m35-007
  expression: "So, do you have questions or let me move to X?"
  category: question_invitation
  function: transition_invitation
  speaker_role: presenter
  difficulty: 3
  context: "So, do you have questions or let me move the supermarket outlook?"
  note: 질문 유도 + 다음 주제 암시 이중 기능

- id: m35-008
  expression: "If not we can move to X"
  category: silence_handling
  function: natural_transition
  speaker_role: presenter
  difficulty: 2
  context: "If not we can move to roadmap slide"

- id: m35-009
  expression: "X is scheduled for CS in Y and mass production in Z"
  category: roadmap_milestone
  function: dual_milestone
  speaker_role: presenter
  difficulty: 4
  context: "The 7200 product is 1B scheduled for CS in June and mass production in January 26"
  note: CS + MP 이중 마일스톤 - SK Hynix 표준 로드맵 화법

- id: m35-010
  expression: "X is EOL in Y"
  category: eol_declaration
  function: end_of_life_stating
  speaker_role: presenter
  difficulty: 3
  context: "the 1A 4800 product is EOL in July 25"

# -- 회피·포장 (Hedging & Deflection) --
- id: m35-011
  expression: "Unfortunately currently we don't have plan to X. But we also reviewing Y."
  category: negation_but_review
  function: polite_refusal_with_review
  speaker_role: presenter
  difficulty: 5
  context: "Unfortunately currently we don't have plan to extend DDR4 including components and module. But we also reviewing how to deal our customer demand."
  note: 가장 중요한 회피 패턴 - 부정 + "But" + 검토

- id: m35-012
  expression: "after reviewing it then we can share it"
  category: review_promise
  function: soft_commitment
  speaker_role: presenter
  difficulty: 3
  context: "So, after reviewing it then we can share it"
  note: "we will share"이 아니라 "we can share" - 부드러운 약속

- id: m35-013
  expression: "So, it should be updated"
  category: error_admission
  function: chart_correction
  speaker_role: presenter
  difficulty: 3
  context: "So, it should be updated. So, measuring the cut in the middle of 2026 and DDR4 for DDR4"
  note: 차트 오류 인정 - 변명 없이 깔끔하게

- id: m35-014
  expression: "our X team doesn't own Y. There's another team that is owning those."
  category: boundary_stating
  function: responsibility_boundary
  speaker_role: presenter
  difficulty: 4
  context: "Again, ouRDIM, our Andes team doesn't own the components. There's anotheRDIM that is owning those."

- id: m35-015
  expression: "I don't know. Because I don't own X for them."
  category: honest_ignorance
  function: boundary_ignorance
  speaker_role: presenter
  difficulty: 3
  context: "I don't know. I don't know. Because I don't, again, I don't own the procurement for them."
  note: 이유 붙인 "I don't know" - 책임 경계 명시

- id: m35-016
  expression: "we are at least a couple of weeks ahead of X"
  category: timeline_advantage
  function: schedule_leverage
  speaker_role: presenter
  difficulty: 4
  context: "We are at least a couple of weeks ahead of Lenovo"
  note: 구체적 시차로 우위 주장

- id: m35-017
  expression: "we are going to receive a head of X"
  category: timeline_advantage
  function: early_access_stating
  speaker_role: presenter
  difficulty: 3
  context: "we are going to receive a head of a Lenovo"

# -- 정중한 도전 (Polite Challenge) --
- id: m35-018
  expression: "we hope you guys have some good news for us on last quantities on continuing support especially for X"
  category: eol_request
  function: polite_extension_request
  speaker_role: questioner
  difficulty: 5
  context: "we hope you guys have some good news for us on last quantities on continuing support especially for the component side of things"
  note: EOL 연장 요청 화법 - "good news"로 요구를 희망으로 포장

- id: m35-019
  expression: "we can't ship X without Y. So, no Z if we can't get Y."
  category: business_impact
  function: strong_leverage
  speaker_role: questioner
  difficulty: 5
  context: "we can't ship servers without the components. So, no DDR5 sales if we can't get DDR4 components."
  note: 가장 강력한 pushback - 비즈니스 임팩트 직접 명시

- id: m35-020
  expression: "Can I ask why that chart shows X if Y?"
  category: data_challenge
  function: inconsistency_probe
  speaker_role: questioner
  difficulty: 4
  context: "Can I ask why that chart shows into 2026 if Lenovo is not going to be extended?"

- id: m35-021
  expression: "Is that for other customers?"
  category: alternative_attribution
  function: answer_guiding
  speaker_role: questioner
  difficulty: 3
  context: "Is that for other customers?"
  note: 대답을 유도하는 짧은 후속 질문

- id: m35-022
  expression: "I would say this is X wide"
  category: industry_framing
  function: issue_escalation
  speaker_role: questioner
  difficulty: 4
  context: "I would say this is industry wide"

- id: m35-023
  expression: "this is something that's not unique to X"
  category: industry_framing
  function: shared_problem
  speaker_role: questioner
  difficulty: 4
  context: "And like I said, this is something that's not unique to Lenovo"

- id: m35-024
  expression: "I think you guys know who that is"
  category: implicit_reference
  function: unnamed_alliance
  speaker_role: questioner
  difficulty: 5
  context: "we have some large cloud customers. I think you guys know who that is that we build for"
  note: 이름 안 대고 암시 - 압박 전달 화법

- id: m35-025
  expression: "since we're reliant on a third party outside of you and us, it's problematic because we can't control it"
  category: third_party_constraint
  function: control_disclaim
  speaker_role: questioner
  difficulty: 5
  context: "since we're reliant on a third party outside of you and us, it's problematic because we can't control it"

- id: m35-026
  expression: "now that this has been designed in, it's very difficult for us OEMs to make that change"
  category: design_in_constraint
  function: technical_lockin
  speaker_role: questioner
  difficulty: 4
  context: "now that this has been designed in, it's very difficult for us OEMs to make that change"

- id: m35-027
  expression: "if we don't take it from you guys now, we're going to need X to try to accelerate Y"
  category: conditional_demand
  function: conditional_leverage
  speaker_role: questioner
  difficulty: 5
  context: "if we don't take it from you guys now, we're going to need support and responsiveness and everything on the component side for DDR5 to try to accelerate the plans of changing those BMCs"

- id: m35-028
  expression: "Would that be a correct understanding?"
  category: understanding_check
  function: polite_confirm
  speaker_role: questioner
  difficulty: 4
  context: "Would that be a correct understanding?"
  note: 자기 이해 명시 + 상대 확인 요구 - 가장 유용한 확인 화법

- id: m35-029
  expression: "So the current situation requiring X, applies to Y in common?"
  category: scope_confirm
  function: range_check
  speaker_role: questioner
  difficulty: 4
  context: "So the current situation requiring BMC, requiring DDR4, applies to Intel and AMD system in common?"

- id: m35-030
  expression: "Until when will you make the X by Y or Z?"
  category: timeline_probe
  function: end_date_inquiry
  speaker_role: questioner
  difficulty: 3
  context: "Until when will you make the DDR4 capable server by 2026 or 2027?"

- id: m35-031
  expression: "I guess I see you guys shifting X out through the end of Y"
  category: observation_stating
  function: pattern_observation
  speaker_role: questioner
  difficulty: 4
  context: "I guess I see you guys shifting DDR4 out through the end of 26"

# -- 협상·액션 (Negotiation & Action Items) --
- id: m35-032
  expression: "we want to verify that it is tested and approved with the necessary testing like a MIM is completed"
  category: verification_demand
  function: conditional_acceptance
  speaker_role: negotiator
  difficulty: 5
  context: "we want to verify that it is tested and approved with the necessary testing like a MIM is completed in the application system"
  note: 검증 조건 명시 - "tested and approved" + "necessary testing"

- id: m35-033
  expression: "I'd like to explain that one later on in another day"
  category: deferral
  function: separate_meeting_proposal
  speaker_role: presenter
  difficulty: 3
  context: "I'd like to explain that one later on in another day. I can explain it to Greg later on"
  note: 시간 부족 시 별도 회의 제안

- id: m35-034
  expression: "we are going to utilize X as a release"
  category: resource_plan
  function: dependency_stating
  speaker_role: presenter
  difficulty: 3
  context: "we are going to utilize AMD BIOS as a release"

- id: m35-035
  expression: "once the CS release from Hynix at the time of September, can you think that that is completed X?"
  category: timeline_check
  function: milestone_completion_check
  speaker_role: questioner
  difficulty: 4
  context: "So once the CS release from Hynix at the time of September, can you think that that is completed application testing in AMD CLB?"

- id: m35-036
  expression: "please let us know that we want to verify that X"
  category: verification_request
  function: double_request
  speaker_role: questioner
  difficulty: 4
  context: "please let us know that we want to verify that it is tested and approved"

# -- 스펙 Pushback (Spec Pushback) --
- id: m35-037
  expression: "One of the design point is the X is not meeting the Y"
  category: spec_pushback
  function: spec_mismatch
  speaker_role: questioner
  difficulty: 5
  context: "One of the design point is the command address signal is not meeting the AMD MBTG"
  note: 진행형 "is not meeting"으로 현재 미충족 강조

- id: m35-038
  expression: "there is some delay with the X"
  category: delay_stating
  function: delay_acknowledge
  speaker_role: questioner
  difficulty: 3
  context: "I was told that there is some delay with the CIB"

- id: m35-039
  expression: "The reason why I am asking is X"
  category: question_justification
  function: context_for_question
  speaker_role: questioner
  difficulty: 4
  context: "The reason why I am asking is the AMD Venus Agisa release note"
  note: 질문 전 이유 명시 - 근거 있는 도전

- id: m35-040
  expression: "my curiosity is that even X, how does Y?"
  category: curiosity_framing
  function: polite_probe
  speaker_role: questioner
  difficulty: 5
  context: "So my curiosity is that even the Agisa is releasing in September. How does the SK Hynix can test 8000 testing with 16GB and 32GB to FIA?"
  note: "curiosity"로 정중 도전

- id: m35-041
  expression: "At the time of X, Y is supported in Z"
  category: doc_reference
  function: official_note_cite
  speaker_role: questioner
  difficulty: 4
  context: "At the time of the 1x by 4, 8000 is supported in July and August"

- id: m35-042
  expression: "Just few of clouds guy"
  category: vague_attribution
  function: limited_adoption_stating
  speaker_role: presenter
  difficulty: 3
  context: "Just few of clouds guy" (re 7200 qualifying)

# -- 발화 채움 표현 (Discourse Markers) --
- id: m35-043
  expression: "Okay, let's get started"
  category: meeting_open
  function: start_signal
  speaker_role: facilitator
  difficulty: 2
  context: "Let's get started"

- id: m35-044
  expression: "We'd like to do short introduction"
  category: introduction_open
  function: round_robin_start
  speaker_role: facilitator
  difficulty: 2
  context: "We'd like to do short introduction"

- id: m35-045
  expression: "We have a timetable. We like to just start with X and then Y"
  category: agenda_stating
  function: agenda_outline
  speaker_role: facilitator
  difficulty: 3
  context: "We have a timetable. We like to just start with market outlook and then several road maps and then long term road map"

- id: m35-046
  expression: "I sent a separate one due to the limited time"
  category: time_constraint
  function: separate_handling
  speaker_role: facilitator
  difficulty: 3
  context: "I have not added the ECC using road map. I sent a separate one due to the limited time"

- id: m35-047
  expression: "Let me show the X side demand and supply and Y market outlook"
  category: presentation_intro
  function: topic_intro
  speaker_role: presenter
  difficulty: 3
  context: "Let me show the DLM side demand and supply and server market outlook"

- id: m35-048
  expression: "Move to the next slide"
  category: slide_transition
  function: next_slide
  speaker_role: presenter
  difficulty: 1
  context: "Okay. Move to the next slide."
  note: 단순 슬라이드 전환 - 자주 사용

- id: m35-049
  expression: "We still looking into the X but we didn't see Y"
  category: monitoring_stating
  function: ongoing_observation
  speaker_role: presenter
  difficulty: 4
  context: "we still looking into the tariff effect on the economy but we didn't see the capex cut by cut or reduction by CSP vendors"

- id: m35-050
  expression: "we need to keep watching how the circumstances are going to"
  category: ongoing_monitoring
  function: future_uncertainty
  speaker_role: presenter
  difficulty: 3
  context: "there are a lot of uncertainties but I need to keep watching how the circumstances are going to"

- id: m35-051
  expression: "That's the reason why we are coming here and wanting to hear about your plan"
  category: meeting_purpose
  function: intent_stating
  speaker_role: questioner
  difficulty: 3
  context: "the reason why we are coming here and wanting to hear about your plan"

- id: m35-052
  expression: "we are working on X design and manufacturing outside"
  category: cross_team_stating
  function: collaboration_status
  speaker_role: presenter
  difficulty: 3
  context: "we are working on AMD AMD CR design and manufacturing outside"
```

---

## 7. 발췌 지도 (Excerpt Map for Shadowing)

오디오: `repo/webex-audio/2025-07-16 08 21 54_EN_LenovoUSQTR-extracted.wav` (전사본 약 2,907단어, 회의 전체 길이는 더 길 수 있으나 전사본이 잘림)
추천 발췌 5구간 (월~금 순회용). 각 구간 1분 내외.

| # | 시간대(추정) | 내용 요약 | 학습 포인트 | shadowing 난이도 |
|:-:|:--|:---|:---|:--:|
| 1 | 도입부 (line 81-91) | DK Park "We have a timetable. We like to just start with..." 아젠다 + Chung Ha 발표 시작 | 회의 진행자 아젠다 화법 | ★★☆ |
| 2 | 시장 전망 (line 95-120) | Chung Ha "DLM demand is expected to grow..." + "supply paradigm is shifted" | 분기 리뷰 발표 화법 + 패러다임 선언 | ★★★ |
| 3 | DDR4 EOL pushback (line 135-145) | Nicky "we hope you guys have some good news..." + SK Hynix "Unfortunately currently we don't have plan..." | EOL 협상 - 정중 요청 + 정중 거절 | ★★★★ |
| 4 | 비즈니스 임팩트 (line 162-207) | Nicky "we can't ship servers without the components" + "industry wide" + "third party... can't control it" | 강한 pushback + 업계 격상 + 제3자 책임 | ★★★★★ |
| 5 | 타임라인 조정 (line 255-291) | Jason "The reason why I am asking..." + "my curiosity is that..." + "we want to verify that it is tested and approved" | 스펙 pushback + 타임라인 확인 + 검증 요구 | ★★★★ |

**사용법**: 
- 월: 발췌 1, 화: 발췌 2, ... 금: 발췌 5
- 일일 루틴(20분)의 ①②③④⑤⑥에 발췌를 넣어 사용
- 발췌 3, 4, 5가 가장 가치 높음 - EOL 협상, 강한 pushback, 스펙 도전이 밀집

---

## 8. 학습 포인트 (Audrey's Teaching Notes)

### Register (화체) 분석
이 회의는 **quarterly review + roadmap alignment + EOL negotiation** register다. 발표자(SK Hynix)가 분기 시장 전망과 로드맵을 발표하고, 고객(Lenovo)이 공급/EOL 이슈로 pushback하는 구조. 두 역할 모두 학습해야:
- **발표자 역할 (SK Hynix - Chung Ha, Theo Kim)**: 시장 프레이밍, 로드맵 명시, EOL 정중 거절 - 네가 분기 리뷰 발표할 때
- **질문자 역할 (Lenovo - Nicky, Jason)**: EOL pushback, 비즈니스 임팩트 명시, 스펙 도전 - 네가 파트너 로드맵 평가/협상할 때

### Pragmatics (화용론) 핵심
1. **"Unfortunately" + 부정 + "But" + 검토**: 영어 회의에서 "없다"고 말할 때, "Unfortunately currently we don't have plan. But we also reviewing." - 부정 앞에 유감, 부정 뒤에 대안. 이 3단 구조를 외워. 한국어 "안 됩니다, 그런데 검토해 보겠습니다"와 타이밍이 같지만, 영어는 "Unfortunately"로 시작해야 정중함이 전달.
2. **"we can't ship X without Y"**: 가장 강력한 비즈니스 pushback. "It would be difficult"가 아니라 "we can't ship" - 부정의 강도를 최대로. Nicky는 이걸로 DDR5 매출까지 연결시킨다. "no DDR5 sales if we can't get DDR4 components" - 하나의 부족이 다른 매출까지 차단된다는 레버리지.
3. **"this is something that's not unique to X"**: 개별 회사 이슈를 업계 전체 이슈로 격상. "우리만의 문제가 아니다"라고 하면, 공급자가 개별 대응이 아니라 업계 대응으로 받아들이게 됨. "I would say this is industry wide"로 격상.
4. **"Would that be a correct understanding?"**: 자기 이해를 명시하고 상대 확인을 요구. "Is that right?"보다 정중하고 "Do you agree?"보다 구체적. 긴 발언 후 이걸로 마무리하면, 발표자가 직접 확인/정정하게 됨.
5. **"my curiosity is that..."**: 질문을 "지적 호기심"으로 포장. "I want to know why"가 아니라 "my curiosity is that even X, how does Y?" - 정중한 도전 화법.

### 네가 당장 써야 할 Top 5
1. **"Unfortunately currently we don't have plan to X. But we also reviewing Y."** - 정중한 거절 + 검토 약속
2. **"we can't ship X without Y. So, no Z if we can't get Y."** - 강한 비즈니스 pushback
3. **"Would that be a correct understanding?"** - 정중한 확인 마무리
4. **"The reason why I am asking is X"** - 질문 전 이유 명시
5. **"we are at least a couple of weeks ahead of X"** - 타임라인 우위 주장

### 비교: 한국어 화법 vs 영어 화법
| 한국어 | 영어 (이 회의에서) | 차이 |
|:---|:---|:---|
| "안 됩니다, 검토해 보겠습니다" | "Unfortunately we don't have plan. But we also reviewing." | "Unfortunately"로 유감 선행 |
| "서버 출하 못 합니다" | "we can't ship servers without the components" | 직접적 부정 - 비즈니스 임팩트 명시 |
| "업계 공통 문제입니다" | "this is something that's not unique to Lenovo. This is industry wide." | "not unique to X"로 동병상련 |
| "제가 이해가 맞습니까?" | "Would that be a correct understanding?" | "correct understanding"으로 정중 확인 |
| "제가 질문하는 이유는..." | "The reason why I am asking is..." | 질문 전 근거 명시 |
| "다음에 따로 설명하겠습니다" | "I'd like to explain that one later on in another day" | "another day"로 별도 일정 제안 |
| "다른 팀 담당입니다" | "our team doesn't own X. There's another team that is owning those." | 소유권 경계 명시 |
| "우리가 더 빠릅니다" | "we are at least a couple of weeks ahead of X" | 구체적 시차로 우위 |

---

## 9. 이 교재 사용법

1. **매일 20분 루틴**: 7절 발췌 지도의 5구간을 월~금 순회
2. **표현 DB**: 6절의 52개 표현 중, 8절 Top 5부터 우선 숙지
3. **Audrey 금요일 교정**: 이 교재의 2절 회피 화법(부정+But+검토) + 3절 정중 도전(비즈니스 임팩트) 중심으로 dump 작성
4. **비교 학습**: 8절 한국어-영어 비교표로 화법 차이 체득
5. **Type B 특화**: 4절 협상·액션 화법을 가장 집중적으로 학습 - EOL 협상, 타임라인 조정, 스펙 pushback 패턴

---

*Textbook 35 - Lenovo US QTR (2025-07-16). 회의 유형 B (roadmap/supply alignment). 표현 DB 52개. 5개 발췌 구간. 작성: 2026-09-01. 전사본이 로드맵 중반에 잘려 있어 전체 회의는 더 길 수 있음.*
