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
다른 결정 엔진(`sk_hynix_decision.py`, `real_estate_decision.py`)과 동일한
"@dataclass 결과 + compute_X(payload) 함수" 패턴을 그대로 따른다.

**2026-09-02 이관**: 사용자 요청("PEOS가 아니라 하루 한번 보내는 청약
리포트에 내용을 추가해줘" + "PEOS는 너무 무거워서 좀 나눠야해")에 따라
PEOS(`engine/report/payload.py`/`markdown.py`)에서 완전히 분리해
`engine/report/subscription_report.py`(별도 daily "청약 리포트")로 옮겼다.
이 리포트는 거시 엔진(ECOS/KOSIS/FRED)도 CCI도 SK하이닉스 실측도 import하지
않는다 — `_subscription_concerns_section()`이
`.github/workflows/subscription-daily-report.yml`(07:10 KST)을 통해 매일
렌더링되고, `scripts/send_subscription_report_email.py`가 발송한다. 이 이관
전엔 PEOS 3.5절에 있었으나, 실제 PEOS 이메일은 `markdown.py`가 아니라
`html_new.py`로 렌더링돼서 이 섹션이 한 번도 실제 이메일에 나타난 적이
없었다는 것도 이번에 확인됐다 — 별도 리포트로 분리하면서 그 드리프트
문제 자체가 해소됐다(html_new.py를 동기화할 필요가 없어짐).

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

## 이 리포트가 담는 것 (2026-09-02 기준)

"청약 리포트"는 이 우려사항 추적만이 아니라 부동산 실거래가 동향(국토교통부,
아파트/연립다세대/오피스텔 매매 + 아파트 전월세)도 함께 담는다 — 둘 다
청약 의사결정에 실제로 쓰이지만 거시경제 판단(PEOS)과는 무관해 같은 자리로
옮겼다. `engine/report/subscription_report.py`가 두 부분을 한 markdown으로
조립하고, 매매/전세 동향의 원 구현(각 `_*_trend()` 함수)은 원래 markdown.py에
있던 것을 그대로 옮겨왔다 — PEOS의 `real_estate_decision`(WAIT/ENTER 진입
판단)은 거시 신호와 결합돼 있어 PEOS에 남았고, 이 리포트에는 순수 시세
데이터만 있다.

## 알려진 한계 (2026-09-01 기준)

- `data/manual_inputs/subscription_notices.yaml`은 수동 입력 파일이라
  실제 공고 등록과 시차가 있을 수 있음 — `subscription-monitor.yml`(5~30분
  주기 자동 감시)이 이 파일보다 먼저 새 공고를 알아챌 수 있으므로, 항목
  2(플랫폼시티)는 `alerted_state.json` 키워드 매칭도 함께 본다(공고
  상세는 몰라도 "뭔가 떴다"는 조기신호로 REVISE 단계 부여).
- 자금조달 갭(항목 5)은 분양가 확정 전까지 구조적으로 WATCH만 가능 —
  이건 결함이 아니라 7.9 원칙의 의도된 결과.
