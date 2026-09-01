# 청약 우려사항 Daily 추적 프레임워크

**신설**: 2026-09-01. **사용자 요청 원문**: "너는 정보를 취득하면 항상 나를
바라봐야해. 내가 현재 우려하는 것들에 대해서 그 정보들이 진행되고 있는
방향을 분석해서 긴급하게 처리해야하는지 전략을 수정해야하는지를 알려주는
daily보고서가 되어야하는거야."

## 왜 이게 필요했나

이전까지 이 세션은 정보(공공분양 소득요건 규칙, LH청약플러스 실전검증,
전국 표본 확대 등)를 취득할 때마다 그 정보 자체의 정확성만 검증하고
끝냈다. 사용자가 "내가 청약하려고하는 타겟이 뭔지 말해봐"로 지적한 것처럼,
정보 취득이 실제 목표(용인 플랫폼시티 청약, 원천동 청약)와 연결되지 않은
채 표류할 수 있다는 게 드러났다. 이 프레임워크는 **모든 새 정보를 사용자가
이미 밝힌 5개 우려사항의 렌즈로 걸러서, 매일 "오늘 뭘 해야 하나"를 3단계로
답하는** 상시 계층을 만든다.

## 구현 위치

`engine/exporters/subscription_concern_tracker.py` — `compute_subscription_concerns(payload)`.
`engine/report/payload.py`가 매일 리포트 payload 빌드 시 자동 호출
(`payload["subscription_concerns"]`), `engine/report/markdown.py`의
`_subscription_concerns_section()`이 PEOS 일일 리포트 3.5절로 렌더링.
다른 결정 엔진(`sk_hynix_decision.py`, `real_estate_decision.py`)과 동일한
"@dataclass 결과 + compute_X(payload) 함수" 패턴을 그대로 따른다.

## 3단계 긴급도

- 🔴 **긴급**: 오늘 실행 가능한 조치가 있고 지연 비용이 큼(예: 전세만료
  D-90 이내, 플랫폼시티가 실제로 민영 분류로 확정).
- 🟡 **전략재검토**: 지금 당장 행동은 아니지만 기존 전제를 다시 계산해야
  함(예: 새 후보지가 통학권 밖, 6개월 이내 임시거주 계획 필요).
- 🟢 **관망**: 전제가 그대로 유지됨 — 조용히 넘어감(매일 같은 경보를
  반복하지 않는다).

## 추적 중인 5개 우려사항 (2026-09-01 최초 등록)

1. **소득제한 특별공급 배제 위험** — `config/user.yaml`의
   `income_cap_preference: none` + `subscription_priority_strategy`(저축총액
   기준, 85㎡ 초과 일반공급/소득제한 없는 84㎡ 이상 우선)가 실제 규칙과
   맞는지. `income_analysis.py`(LH청약플러스 실전검증)로 "60㎡ 초과 일반공급
   = 소득 무관"이 확인된 상태 — 이 전제가 계속 유효한지 매 공고마다 재확인.
2. **플랫폼시티 민영 분류 위험** — 역사적으로 라온프라이빗 아르디에·
   e편한세상 용인역 플랫폼시티 모두 민영 분류였음. 민영으로 확정되면 이
   저장소의 국민주택 소득요건 프레임워크(public-housing-income-requirement-framework.md)
   자체가 적용 안 되므로 완전히 다른 전략(청약저축 순위제)이 필요 — 그
   전환점을 놓치지 않는 게 이 항목의 핵심.
3. **전세 계약 만료 임박** — `moveout_deadline`(2027-02-22, 갱신청구권
   이미 소진 — 재연장 불가). D-90/D-180 경계로 긴급도 승격.
4. **자녀 통학거리 제약** — 등록된 후보 공고(`data/manual_inputs/subscription_notices.yaml`)
   중 현재 거주지(용인 수지구, 문정중·풍천초) 밖 지역이 있으면 전략재검토.
5. **자금조달 갭 & 경쟁률 불확실성** — 분양가·경쟁률이 확정되기 전엔 갭
   숫자를 만들어내지 않음(Master Instruction 7.9). 공고 확정 시
   `engine/personal/housing.py`의 `funding_gap_krw` 로직이 자동 재계산.

## 새 우려사항을 추가하는 법

사용자가 새로운 우려를 명시적으로 밝히면 (a) 이 문서에 6번째 항목으로
append, (b) `subscription_concern_tracker.py`에 `_check_<name>()` 함수를
추가(다른 5개와 동일한 `ConcernItem(name, urgency, status, recommendation,
detail)` 반환 시그니처), (c) `compute_subscription_concerns()`의 concerns
리스트에 연결, (d) 단위테스트(`tests/test_subscription_concern_tracker.py`)에
경계 케이스 추가. 우려사항을 다른 세션의 판단만으로 제거하지 않는다 —
사용자가 "이제 이건 신경 안 써도 된다"고 명시할 때만 제거.

## 알려진 한계 (2026-09-01 기준)

- `data/manual_inputs/subscription_notices.yaml`은 수동 입력 파일이라
  실제 공고 등록과 시차가 있을 수 있음 — `subscription-monitor.yml`(5~30분
  주기 자동 감시)이 이 파일보다 먼저 새 공고를 알아챌 수 있으므로, 항목
  2(플랫폼시티)는 `alerted_state.json` 키워드 매칭도 함께 본다(공고
  상세는 몰라도 "뭔가 떴다"는 조기신호로 REVISE 단계 부여).
- 자금조달 갭(항목 5)은 분양가 확정 전까지 구조적으로 WATCH만 가능 —
  이건 결함이 아니라 7.9 원칙의 의도된 결과.
