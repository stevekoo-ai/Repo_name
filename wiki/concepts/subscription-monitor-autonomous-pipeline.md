---
title: 청약 모니터 autonomous 5단계 파이프라인
created: 2026-08-06
updated: 2026-08-06
tags: [subscription, automation, github-actions, pipeline, email]
---

`/c/*` 5분마다 GitHub Actions에서 도는 청약 모니터를 "조사 → 판단 → 보낼
메시지 작성 → 메일 본문 구성 → 발송"의 5단계 autonomous 파이프라인으로
고도화한 설계. **규칙 기반**(LLM in-the-loop 아님 — 결정론적, 토큰 비용 0,
Secret 추가 없음). 발송 정책은 **"의미있을 때 + 일일 요약"**.

사용자가 받는 일일 heartbeat 메일(예: "청약 모니터 정상 작동 중
(2026-08-05)")은 이 파이프라인의 DAILY_DIGEST 산출물이며, 이제 단순
"살아있다" 신호에서 **"오늘 조사 결과 요약(매물 N건, 우선순위 분포,
접수 임박 목록)"**으로 강화됐다.

## 배경 — 왜 고도화했나

기존 시스템(`collectors/subscription_monitor/`)은 이미 autonomous:
`subscription-monitor.yml`이 `*/5 * * * *` cron으로 5분마다 실행,
`fetch_and_render.py`가 data.go.kr API fetch + HTML 렌더, `alerts.py`가
키워드 매칭 시 Issue+email, 매일 1회 heartbeat, 장애/복구 알림. 그러나
두 가지 약점이 있었다:

1. **판단·메시지 작성이 단순 키워드 매칭** — "적절히 보낼 메시지를
   작성"이 템플릿 문자열 치환 수준이었다. 내 청약통장 조건(저축총액
   28,050,000원 · 249회 · 2005-11-03 가입)과 매물 조건을 대조해 "이 매물이
   나에게 실제 당첨 가능성 있는가"까지는 판단하지 않았다.
2. **매칭 없으면 24시간 침묵** — 사용자가 "이 조사는 꼭 내게 email로 결과를
   전달해 줘야 해!"라고 강조한 맥락. 새 매칭 없으면 heartbeat 1통/일 외엔
   아무것도 안 왔다.

## 5단계 파이프라인

| Step | 모듈 | 역할 |
|---|---|---|
| 1. 조사 | `fetch_and_render.py` | data.go.kr API fetch + 서울·경기 필터 (기존 유지) |
| 2. 판단 | `judge.py` (신설) | 매물별 판결: 자격·경쟁력·우선순위·권장행동 (규칙 엔진) |
| 3. 보낼 메시지 작성 | `compose.py` (신설) | 발송 이벤트 분류 + 발송 정책("의미있을 때 + 일일 요약") |
| 4. 메일 본문 구성 | `compose.py` | 이벤트별 결정론적 템플릿 (자연어, LLM 아님) |
| 5. 발송 | `alerts.py` (저수준만 남김) | Gmail SMTP + GitHub Issues API (기존 인프라 재사용) |

### Step 2 — 판단 규칙 엔진 (judge.py)

`docs/SUBSCRIPTION_SYSTEM.md`의 점수체계를 코드로 옮김. 내 청약통장은
모든 밴드 만점 → **40/40 만점** (가입 20년 8개월 → 15점, 249회 → 15점,
최고액 25만원 납입 → 10점). 판결 객체:

```
{id, name, region, eligible, match_keyword, competitiveness(HIGH/MED/LOW),
 score, days_to_open, priority(HIGH/MED/LOW), reason, recommended_action, is_newlywed, row}
```

판단 규칙 (결정론적):
- `match_keyword` 있거나 순차제 경쟁력 HIGH → HIGH 후보
- 접수 시작 D-1 도래 → 우선순위 1단계 상승 (접수 임박)
- 신혼희망타운 → 별도기준 캐비엣 → MED 상한 (HIGH 불가)
- 권장행동: HIGH→지원 강력 권장 / MED→검토 권장 / LOW→참고만

`judge.py`가 내 청약통장 상수(`MY_*`)의 단일 정보원. `fetch_and_render.py`는
이를 import. [[user-profile]]의 청약통장 표와 동기화 필요 시 양쪽 갱신.

### Step 3 — 발송 정책 (compose.py)

5개 발송 이벤트 (우선순위순):

| 이벤트 | 조건 | 발송 채널 | 즉시? |
|---|---|---|---|
| NEW_MATCH | 새 키워드 매칭 매물 (alerted_state로 중복 방지) | email + Issue | ✅ |
| PRIORITY_UP | 기존 매물이 HIGH로 승격 (접수 D-1 등) | email only | ✅ |
| OUTAGE | API 6회 연속(≈30분) 이상 | email + Issue | ✅ |
| RECOVERY | 장애 후 복구 | email only | ✅ |
| DAILY_DIGEST | 매일 1회, 09:00 KST 이후 첫 healthy 실행 | email only | 일 1회 |

DAILY_DIGEST가 핵심 — "조사 결과를 꼭 받는" 채널. 매칭이 0건이어도
오늘 조사 요약(전체 매물 N건, 우선순위 분포, 접수 임박 목록, 시스템 상태)을
발송. 기존 heartbeat의 "이 메일이 계속 오면 정상" 안내는 유지.

### 상태 파일 마이그레이션

- `alerted_state.json`: bare list `["id1","id2"]` → 객체 맵
  `{id: {priority, keyword, notified}}` (PRIORITY_UP 추적용). loader 하위호환
  (bare list 자동 읽기), writer는 항상 새 구조.
- `health_state.json`: 구조 유지, `last_heartbeat_date` 필드명 유지(하위호환).

### LLM in-the-loop 불가능성

사용자가 "네가(이 Claude 세션이) 2번(판단)을 해줄 수 있어?"라고 물었으나,
**불가능**: 5분 사이클은 GitHub Actions 클라우드 runner에서 혼자 실행.
이 Claude 세션은 이 대화창에서만 연결돼 있고 세션 종료 시 사라진다.
서버 사이드 LLM 판단을 autonomous로 돌리려면 Actions runner가 Claude API
호출(option 2)뿐 — 토큰 비용 + ANTHROPIC_API_KEY Secret + 결정론 상실.
따라서 **규칙 기반** 선택. "내가 연결 가능할 때"의 수동 보조는 이 세션
안에서만 가능, autonomous 사이클 자체는 규칙 기반이어야 함.

## 검증 (2026-08-06 로컬 단위 테스트)

가짜 row + send layer mock으로 5개 이벤트 경로 전부 검증:
- NEW_MATCH: 플랫폼시티 매물 → issue=True 발송 ✅
- DAILY_DIGEST: 같은 실행에서 요약 발송(issue=False) ✅
- 중복 방지: 같은 매물 재실행 시 NEW_MATCH 재발송 안 함, 같은 날 digest 재발송 안 함 ✅
- PRIORITY_UP: MED 매물이 D-1 도래로 HIGH 승격 시 email 발송 ✅
- OUTAGE: 6회 연속 실패 시 발송, outage_alerted 세트 ✅
- RECOVERY: 장애 후 복구 시 발송 ✅

## Sources

- `collectors/subscription_monitor/judge.py`, `compose.py`, `alerts.py`, `fetch_and_render.py`
- [docs/SUBSCRIPTION_SYSTEM.md](../../docs/SUBSCRIPTION_SYSTEM.md) — 점수체계 원본
- [사용자 프로필](../entities/user-profile.md) — 청약통장 상세 표 (judge.py 상수와 동기화)
- `.github/workflows/subscription-monitor.yml` — 5분 cron 트리거
- [메세지박스](../messagebox.md) 2026-08-06 게시 (🟡 CAUTION)
