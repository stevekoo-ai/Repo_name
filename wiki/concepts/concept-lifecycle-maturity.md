---
title: Concept Lifecycle Maturity — Change Justification Framework
created: 2026-08-08
updated: 2026-08-08
tags: [governance, concept-discipline, decision-framework, operations]
---

## The 4-Stage Lifecycle

| Stage | Definition | Wiki Action | Evidence Required |
|---|---|---|---|
| **Event** | 일회성 사건 ("X 발표했다") | Entity 업데이트만 | timestamp 고정 |
| **State Change** | 주체의 상태 변화 ("X의 상태: A→B") | Entity 수정 | 전후 상태 명시 |
| **Pattern** | 반복되는 현상 | Concept 검토 대기 | 3회+ 동일 타입 |
| **Concept** | 보편적 이론/틀 | Concept 수정 가능 | 크로스도메인 적용 가능 |

## Concept Change Justification — 4 Conditions (AND rule)

✅ **ALL must be true to justify Concept modification:**

- [ ] **Repetition**: 3회 이상의 동일 타입 Event 관찰
- [ ] **Assumption Violation**: 기존 Concept의 전제가 증거로 부정됨
- [ ] **New Variable**: 이전에 알려지지 않은 인과관계 발견
- [ ] **Statistical Significance**: 독립적 반복 (동일 도메인만 아님)

❌ **Do NOT modify Concept if:**
- Single event only (1회)
- Same company/entity only (반복성 부족)
- Existing Concept이 이미 설명 가능
- Time window 부족 (< 1 month data)

## Quick Decision Tree

```
새로운 Event 발생?
  ↓
이게 처음인가? (1회)
  → YES: Entity 업데이트만 + Watch List 추가
  → NO: 3회 이상인가?
    → YES: 기존 Concept의 가정이 깨졌나?
      → YES: Concept 검토 시작
      → NO: 새로운 변수가 있나?
        → YES: Concept 검토 시작
        → NO: 관찰 계속 (아직 통계적 유의성 부족)
    → NO (2회): 관찰 단계 계속
```

## Case Study: SK Hynix HBM4 Supply Confirmed (2026-08-08)

**Diagnosis:**

| Check | Result | Reasoning |
|---|---|---|
| Stage? | Event + State Change ✓ | "공급 확정 발표" + "SK하이닉스 상태: 미정→확정" |
| Repetition? | 1회만 ✗ | SK하이닉스만 발표, CXMT/Samsung 미확인 |
| Pattern? | No ✗ | 3회 미만 |
| Assumption Violated? | Unknown | "공급 확대 → leverage 감소" 가설 미검증 |
| Concept Change Justified? | **NO** ✗ | 모든 조건 불충족 |

**Action Taken:**
- ✅ Entity (sk-hynix.md): "HBM4: 공급 확정 [2026-08-08]" 추가
- ✅ Watch List: hbm-cycle-score.md 관찰 섹션에 기록
- ❌ Concept 수정 금지

**Next Trigger for Review:**
1. CXMT HBM4 공급 공표 시 (2회 감지) — watch 계속
2. 삼성 HBM4 신호 시 (3회 감지) → hbm-cycle-score.md 검토 가능
3. 공급 확대 → 신용잔고 회복 상관관계 검증 시 → market-cycles-leverage-risk.md 검토 가능

## Application Examples

**Example 1 — Concept Change (Justified)**
```
Event: 신용잔고 역전 신호 3회 반복 (8/1, 8/3, 8/5)
  → Pattern 확인
  → "신용잔고 역전은 찐반등 선행신호" 검증됨
  → panic-recovery-signals.md 수정 정당화 ✅
```

**Example 2 — Concept Change (Not Justified)**
```
Event: SK하이닉스 HBM4 공급 확정 (1회)
  → State Change 확인
  → 반복성 부족 + 가정 미검증
  → Concept 수정 비정당화 ✗
  → Watch List에 추가, 다음 반복 대기
```

## References
- [Concept vs Entity 경계](../concepts/entity-concept-boundaries.md) (향후 작성)
- [Pattern Recognition 임계값](../concepts/pattern-recognition-thresholds.md) (향후 작성)
- Parent: [wiki/concepts](../concepts/) 

## Sources
- 2026-08-08 Session: Concept Lifecycle 원칙 수립 과정에서 도출
