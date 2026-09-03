---
title: "Customer-Meetings Intelligence — 2-tier 구조 운영 패턴"
created: 2026-08-11
updated: 2026-08-11
tags: [cxl, customer-meeting, concept, methodology, 2-tier, intelligence, pattern]
---

# Customer-Meetings Intelligence — 2-tier 구조 운영 패턴

> 1차 현장 인텔리전스(미팅 발언)를 보존·축적·정제하는 재사용 가능한 운영 개념.
> 2026-01-15~08-11 11개 미팅 수집 과정에서 발견된 패턴을 일반화.
> 구조 규칙은 [customer-meetings/README.md](../customer-meetings/README.md),
> 전문·교차표는 [customer-meetings/index.md](../customer-meetings/index.md),
> thread 현재 상태는 [monitoring/customer-meetings-thread-tracker-status.md](../monitoring/customer-meetings-thread-tracker-status.md),
> 이벤트 기록은 [summaries/customer-meetings-overview-2026-01-15-to-08-11.md](../summaries/customer-meetings-overview-2026-01-15-to-08-11.md).

---

## 핵심 문제

고객·파트너 미팅은 **many-to-many** — 한 미팅에 여러 상대방이 동시 발언하고,
한 상대방이 여러 미팅에 걸쳐 등장. 단일 평면 구조(미팅별 파일만)에선:
- 상대방별 누적 관계 상태를 볼 수 없음
- 교차 thread(여러 미팅에 걸친 주제)가 분산되어 놓침
- 새 미팅이 기존 결론을 번복할 때 정정 이력이 묻힘

---

## 해결: 2-tier 구조

```
customer-meetings/
├─ meetings/   ← 미팅별(날짜키, 변경 불가, 전문) — 단일 출처
└─ by-customer/ ← 상대방별 누적(현재 상태 + 모든 미팅 이력) — 축적
```

- **meetings/** = 한 미팅의 전체 맥락(여러 상대방 동시 발언)을 보존. **단일 출처**.
- **by-customer/** = 한 상대방의 모든 미팅을 누적. 현재 관계 상태 + 핵심 팩트 + 미팅 이력(역순).
- 같은 사실이 양쪽에 나오되, **전문은 meetings/가 단일 출처**, by-customer/는 요약+상태.

### relation 분류
- **customer**: 구매 고객 (8명: Lenovo·Google·IBM·AWS·HPE·Oracle·NVIDIA·MSFT·Dell)
- **partner**: 협력 파트너 (11명: Marvell·Xcena·Xconn·Liqid·Intel·AMD·Qualcomm·ScaleFlux·Panmnesia·Primemas·Penguin)
- **competitor**: 추적 경쟁사 (5명: Montage·Broadcom·Micron·Samsung·Kioxia)
- 한 미팅에 여러 relation 섞여도 각각 by-customer 파일로 분리.

---

## 발견된 운영 패턴 (재사용 가능)

### 패턴 1: 시계열 누적 정제 (Self-correcting Accumulation)

새 미팅이 기존 "기원/최초" 결론을 번복하는 패턴. 더 이른 미팅이 발견될 때마다 기원이 재정립.

**KV Cache thread 사례 (정정 4회)**:
| 회차 | 기원 결론 | 계기 |
|------|----------|------|
| 1차 | MSFT 04-30 | 최초 ingest |
| 2차 | NVIDIA 03-12 | 더 이른 미팅 |
| 3차 | AWS 02-10 + NVIDIA 03-12 두 축 | 더 이른 자사 발의 |
| 4차 | + IBM 02-06 독립 인지 (3출처) | 더 이른 고객 인지 |

**일반화**:
- "X의 기원/최초" 결론은 **가장 이른 현재 알려진 기록**일 뿐. 새 미팅이 번복 가능.
- 정정 이력을 thread 기록에 **명시적으로 추적**("정정 이력: A→B→C") — 묻히지 않게.
- 2-tier 구조가 이를 가능케 함: meetings/ 단일 출처 + by-customer/ 누적 = 새 미팅 추가 시 기존 결론 재검증 용이.

**적용 조건**: 같은 주제가 2개+ 미팅에 걸쳐 등장할 때. 단일 미팅엔 미적용.

### 패턴 2: 플랫폼 교차 (Platform Cross-axis)

동일 기술 플랫폼이 서로 다른 관점(CXL vs DRAM, 고객A vs 고객B)에서 교차 등장.

**사례**:
- **AMD Venice**: Google 02-05(DRAM, MRD 필수, EVT 진행) ↔ HPE 02-12(CXL, Post-Launch) — 동일 플랫폼 다른 메모리 페이즈
- **Intel DMR**: Google 02-05(DRAM, 48→64GB) ↔ Intel 08-11(CXL, Co-enabling) — DRAM 선행→CXL 확장

**일반화**:
- 한 플랫폼이 두 관점에서 등장하면, 각 관점의 **진행 단계(EVT/DVT/GA/Post-Launch)** 가 다를 수 있음.
- by-customer/ 양쪽에 교차검증 노트로 연결 — 한쪽만 보면 플랫폼 전체 타이밍을 놓침.
- 간접 등장(AMD·Intel이 Google 미팅에서 언급만)도 by-customer 이력에 추가 — 직접 미팅 아님 명시.

**적용 조건**: 동일 플랫폼/제품이 2개+ 미팅에 걸쳐 다른 관점에서 언급될 때.

### 패턴 3: 교차 thread 발견 (Cross-meeting Thread)

여러 미팅에 걸쳐 같은 주제가 반복 등장 → 단일 미팅엔 안 보이는 패턴이 미팅 간 비교에서 드러남.

**사례 (11개 미팅에서 16개 thread 발견)**:
- TCO/가격: 7고객 공통 (Lenovo 가장 직접적 cost 장벽 → Oracle 엄격 → IBM $/GB 명목)
- 폼팩터: 7-way (고객별 제약이 다름 — Oracle AIC 큼, AWS 1DPC, IBM 시계열 분리)
- IMDB/Memory sharing: 4고객 공통 use case

**일반화**:
- thread는 customer-meetings/index.md §3(교차검증)에 누적 — 단일 미팅 관점엔 안 보임.
- thread별로 "가장 이른 언급 / 가장 직접적 / 가장 엄격" 등 **특성 부여** — 단순 나열 아님.
- 새 미팅 ingest 시 기존 thread 갱신 + 신규 thread 탐지.

**적용 조건**: 3개+ 미팅 수집 후. 1-2개에선 thread 미성숙.

### 패턴 4: 분류 범위 확장 (Scope Discovery)

미팅 분류 체계가 실제 자료 유입에 따라 확장됨.

**사례**: 9개 CXL 미팅 후 Google 10번째로 **첫 비-CXL(DRAM)** 미팅 추가 → README 범위가 CXL+DRAM 모두 커버함 확인.

**일반화**:
- 분류 구조(meetings/+by-customer/)를 **주제(CXL)에 묶지 말고 관계(고객·파트너 미팅)에 묶기** — 주제 확장 대응.
- "첫 X" 미팅(첫 비-CXL, 첫 partner 단독 등) 발견 시 분류 범위 재확인.

---

## DRAFT 연결 (CXL 상품기획 12장)

by-customer/ 핵심 팩트는 DRAFT 챕터로 연결:
- 3장 컨트롤러·4장 풀링·5장 CPU/GPU·6장 AI 패브릭·7장 Main Memory·9장 KV offload·11장 시장 인텔리전스·12장 상품기획
- ★★★/★★/★ 영향도 표기. DRAFT 본문 반영은 정규 .md 경로 복구 후 일괄.
- DRAFT 장 매핑은 [cxl-fullstack-7layer-framework.md](cxl-fullstack-7layer-framework.md) 7레이어와 정렬.

---

## 데이터 한계 공개 원칙

- 1차 미팅 발언 = **단일 출처**. 외부 교차검증 미수행 명시.
- 추정(M사=Micron 등)은 확정 전 "(추정)" 명시, 확정 시 정정.
- 원문 표기 변형(Pamnesia/famfs 등)은 정정 시 "(FAMS→famfs 정정)" 식으로 추적 가능 명시.
- 상대방 직책 미기재 cases는 발언 부분 매핑만, 개별 직책 비매핑 명시.

---

## Local-only 정책

- github push 안 함. 모든 파일 local working tree에만. (CLAUDE.md 최우선 정책 준수)
- push 필요 시 사용자 확인 후.

---

## 적용 대상 (향후 미팅)

본 개념은 **새 미팅 ingest 시마다 적용**:
1. 원문 → sources/ (immutable)
2. 전문 → meetings/YYYY-MM-DD-<slug>.md
3. 등장 상대방 전부 → by-customer/<customer>.md 갱신 (이력 append + 현재 상태)
4. index.md §3 교차검증 갱신 (기존 thread + 신규 thread)
5. 시계열 누적 정제 패턴 발동 시 정정 이력 명시
6. 플랫폼 교차 발견 시 양쪽 by-customer에 교차 노트
7. summaries/·monitoring/ 갱신 (이벤트 기록·thread 상태)
8. wiki/index.md + wiki/log.md 갱신

---

## Sources

- 11개 미팅 수집 (2026-01-15 ~ 2026-08-11): [customer-meetings/](../customer-meetings/)
- 구조 규칙: [customer-meetings/README.md](../customer-meetings/README.md)
- CXL 상품기획 핸드오프: [cxl-product-planning-session-handoff.md](cxl-product-planning-session-handoff.md)
- 7레이어 프레임워크: [cxl-fullstack-7layer-framework.md](cxl-fullstack-7layer-framework.md)
- Concept Lifecycle: [concept-lifecycle.md](../architecture/concept-lifecycle.md) (Creation/Merge/Archive rules)
