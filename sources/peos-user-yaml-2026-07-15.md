# PEOS config/user.yaml, config/portfolio.yaml 발췌 (2026-07-15)

이 저장소에는 이 위키(Wiki) 패턴과는 별개로 **PEOS (Personal Economic Operating System)** 라는
시스템이 같은 날 다른 세션에 의해 구축되어 `main`에 merge되어 있었다. PEOS는 기계가 읽는
`config/user.yaml`(성향/전략), `config/portfolio.yaml`(보유자산)을 단일 정보원으로 여러 엔진
(`engine/personal/*.py`)이 참조하는 구조다. 위키의 `entities/user-profile.md`가 "가입일 불일치
확인중"으로 남겨뒀던 문제를 이 소스로 교차검증한다.

## config/user.yaml → housing 섹션 (발췌)

```yaml
housing:
  target_type: public_sale
  target_complex: "플랫폼시티 공공분양"
  status: waiting_for_announcement
  preferred_size: "84m2+"
  income_cap_preference: none
  priority_regions: ["세종 플랫폼시티"]
  subscription_account_start: "2005-11-03"  # REAL — 국민은행, config/portfolio.yaml subscription_savings와 동일
  subscription_priority_strategy: "저축총액(납입총액) 기준 경쟁 — 85㎡ 초과 일반공급, 소득제한 없는 84㎡ 이상 우선"
  moveout_deadline: "2027-02-22"       # 현 거주지 전세 계약 만료일(갱신청구권 이미 사용) — 입주 전 임시 거주 필요
```

## config/portfolio.yaml → subscription_savings 섹션 (발췌, 전문)

```yaml
subscription_savings:
  bank: "국민은행"
  account_start: "2005-11-03"
  balance_krw: 28050000
  monthly_contribution_krw: 250000        # 납입인정 최고금액
  contribution_count: 249                 # 2026-07 납입분까지 누적 회차
  contribution_count_as_of: "2026-07"
  max_recognized_payment: true
  rate_increased_from: "2024-11"          # 229회차부터 25만원으로 상향
```

이 수치(은행/가입일/잔액/월납입액/누적회차/상향시점)는
`sources/subscription-savings-account-2026-07-15.md`(청약통장 상세, 2026-07-15 확인분)와
필드 단위로 완전히 일치한다. 즉 가입일은 **2005-11-03**으로 두 개의 독립적으로 관리되는
시스템(위키의 원본 사용자 소스 vs PEOS의 config)에서 교차 확인됨 — 최초 위키 소스
(`user-profile-2026-07-13.md`)에 적힌 "2008-11"은 사용자의 부정확한 초기 기억이었던 것으로 정리한다.

참고: `config/portfolio.yaml` 파일 상단 주석은 "cash/bonds/subscription_savings below are still
EXAMPLE placeholders"라고 되어 있는데, 실제 `subscription_savings` 값은 위 대조 결과로 볼 때 EXAMPLE이
아니라 실제 값으로 보인다 — PEOS 쪽 문서가 갱신되지 않은 것으로 추정(이 위키에서 직접 고치지 않음,
PEOS 쪽 세션에서 정리 필요).

## config/user.yaml → investment_style 섹션 (발췌)

```yaml
investment_style:
  horizon: long_term
  macro_driven: true
  cycle_driven: true
  data_driven: true
  risk_tolerance: medium
  rebalancing_rule: "분기 1회 점검, Investment Environment Score 20점 이상 변동 시 리밸런싱 검토"
```

## Sources
- `config/user.yaml` (repo root, PEOS)
- `config/portfolio.yaml` (repo root, PEOS)
