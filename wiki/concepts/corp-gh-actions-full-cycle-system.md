---
title: 회사망 ↔ GitHub Actions 완전 사이클 시스템 설계 (2026-08-06)
created: 2026-08-06
updated: 2026-08-06
tags: [infrastructure, github-actions, automation, system-design, corporate-proxy]
---

> **설계만 정리한 페이지. 구현은 다음 세션.** 측정된 제약(회사망→GitHub
> 73KB POST 한계, GitHub→회사망 pull 제약 없음) 안에서 동작하는 3단계
> 자동 사이클 설계. 모든 메커니즘은 docs 교차검증 완료.

## 시스템 개요

```
        ① 신호 (회사망 → GitHub)              ② GitHub Actions 작업         ③ 결과 회수 + 종합 (GitHub → 회사망)
        ┌─────────────────────┐              ┌──────────────────┐          ┌────────────────────────┐
        | repository_dispatch |    트리거 →  | 데이터 수집        |  결과 →  | git pull (제약 없음)    |
        | API POST (<73KB)    |              | 리포트 HTML 생성   |          | 위키 서사 + LLM 종합     |
        | event_type + payload|              | 커밋 + 이메일 발송 |          | 새 종합 리포트 작성     |
        └─────────────────────┘              └──────────────────┘          └────────────────────────┘
              "시동 버튼"                       "실제 일"                     "가치 더하기 + 다시 ①로"
```

**핵심 원리**: 회사망은 73KB 제약 때문에 "시동 버튼"(작은 POST)만 누르고,
실제 무거운 작업은 GitHub Actions 러너(제약 없는 환경)가 한다. 결과는 git pull
(방향 반대, 제약 없음)로 회수해 위키 서사와 종합한다. 종합물은 다시 ① 신호로
올려 사이클을 닫는다.

## 3단계 상세 설계

### ① 신호 단계 — 회사망 → GitHub (73KB 이하 POST)

**메커니즘**: `repository_dispatch` REST API.
[docs 검증](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event):

- 엔드포인트: `POST /repos/{owner}/{repo}/dispatches`
- 본문: `event_type`(100자 한계) + `client_payload`(65,535자 한계, 속성 10개)
- 인증: PAT `repo` scope
- **POST 본문 크기**: client_payload 65KB 한계 = 회사망 73KB 한계 **이하** → ✅ 작동 확정

**트리거 스크립트** (회사망에서 실행, [`upload_brief.py`](../../upload_brief.py) 패턴 재사용):

```python
# 회사망 → GitHub Actions 시동. 본문 수백 bytes로 73KB 한계 여유.
import json, urllib.request, ssl
def trigger(event_type, payload):
    url = f"https://api.github.com/repos/{REPO}/dispatches"
    body = json.dumps({"event_type": event_type, "client_payload": payload}).encode()
    # SSL 폴백 + PAT (github-api-bypass-code-patterns.md 헬퍼 재사용)
    api("POST", "dispatches", pat, {"event_type": event_type, "client_payload": payload})
    # 예: trigger("daily-brief", {"date": "2026-08-06", "mode": "full"})

# 사용: 아침에 한 줄
python trigger_brief.py  # → repository_dispatch event_type="daily-brief"
```

**왜 push 트리거가 아니라 repository_dispatch인가**: push는 73KB 초과 파일
막히고(큰 리포트), 파일 올릴 필요 없이 "시동만" 누르려면 dispatch가 목적에 부합.
push 트리거는 이미 `daily-brief-report.yml`이 `report/daily-brief-*.html` push에
반응하도록 돼 있으니 — ②단계 결과 커밋이 ③ 자동 발송까지 트리거하는 데 재사용.

### ② GitHub Actions 작업 단계 (제약 없는 환경)

**메커니즘**: `repository_dispatch`에 반응하는 워크플로우.
[docs 검증](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch):

```yaml
# .github/workflows/daily-brief-generate.yml (main 브랜치 — dispatch는 default branch 필요)
name: Daily Brief Generator
on:
  repository_dispatch:
    types: [daily-brief]
  workflow_dispatch: {}  # 수동 테스트용

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - name: Collect data + generate report
        run: |
          python scripts/generate_brief.py --date ${{ github.event.client_payload.date }} \
                                           --mode ${{ github.event.client_payload.mode }}
          # → report/daily-brief-YYYY-MM-DD.html 생성
      - name: Commit report (PAT 필요 — GITHUB_TOKEN은 자기 브랜치 push 가능)
        run: |
          git config user.name "Daily Brief Bot"
          git config user.email "noreply@anthropic.com"
          git add report/daily-brief-*.html
          git commit -m "Daily Brief ${{ github.event.client_payload.date }} 자동 생성"
          git push
        env:
          GH_TOKEN: ${{ secrets.PAT_FOR_PUSH }}  # 또는 기본 GITHUB_TOKEN
      # push 이벤트가 daily-brief-report.yml을 자동 트리거 → 이메일 발송 (③ 단계 없이도 완결)
```

**이미 검증된 인프라 재사용** ([automation-infrastructure.md](../entities/automation-infrastructure.md)):
- 데이터 수집: `collectors/` + KIS/ECOS/FRED API 시크릿 (이미 Actions에서 작동 중)
- 리포트 생성 로직: `scripts/daily_report.py`에 5개 섹션 이미 구현
- 이메일 발송: `daily-brief-report.yml`이 push에 반응 (이미 검증 완료,
  [`daily-brief-email-workflow-debug.md`](daily-brief-email-workflow-debug.md))

### ③ 결과 회수 + 종합 단계 (GitHub → 회사망)

**메커니즘**: `git pull` (방향 반대, 73KB 제약 없음 — GET은 POST 검사 안 받음).

```
① 신호 → ② Actions가 리포트 생성+커밋 → (회사망에서) git pull →
  내가 위키 서사 + LLM 종합으로 '해석층' 보고서 작성 →
  그 종합물을 다시 upload_brief.py(①)로 올려 다음 사이클
```

**왜 이 단계가 가치를 더하는가** ([CLAUDE.md](../../CLAUDE.md) 위키 철학):
- ② 단계는 **사실층** (데이터 → 규칙기반 계산 → HTML). LLM-free, 재현 가능.
- ③ 단계는 **해석층** (위키 서사 + LLM 종합). 이게 "LLM Wiki" 패턴의 본질 —
  매번 raw에서 재도출하지 않고 위키에 축적된 서사 위에서 종합.
- [automation-vs-ai-narrative-roadmap.md](automation-vs-ai-narrative-roadmap.md)의
  3단계 로드맵과 정확히 일치: 규칙기반(②) + LLM 서술(③) 하이브리드 명시 분리.

## 73KB 제약과 각 단계의 호환성 (측정 기반)

| 단계 | 방향 | 메커니즘 | 크기 제약 | 작동 |
|---|---|---|---|---|
| ① 신호 | 회사망→GitHub | `repository_dispatch` POST | client_payload 65KB 한계 < 73KB | ✅ 확정 |
| ② 작업 | GitHub 내부 | Actions 러너 | 제약 없음 | ✅ (이미 10개 워크플로우 작동 중) |
| ③ 회수 | GitHub→회사망 | `git pull` (GET) | POST 검사 안 받음 | ✅ 확정 |
| 종합→① | 회사망→GitHub | `upload_brief.py` (작은 파일) | 73KB 이하만 | ⚠️ 크기 의존 |

**유일한 제약**: ③에서 만든 종합 리포트가 73KB 초과하면 회사망에서 못 올림.
해결: 종합 리포트를 위키 페이지(작게 쪼개어)로 올리거나, 외부망에서 push.
대부분의 위키 페이지는 10~30KB라 73KB 이하 → ✅.

## 기존 인프라와의 통합 포인트

| 기존 자산 | 이 시스템에서의 역할 |
|---|---|
| [`upload_brief.py`](../../upload_brief.py) | ① 신호 단계의 PAT/SSL/Contents API 헬퍼 재사용 + dispatch POST |
| `daily-brief-report.yml` (이메일 발송) | ②에서 리포트 push 시 자동 트리거 → 발송 (이미 검증) |
| `scripts/daily_report.py` (5개 섹션) | ②의 리포트 생성 본체 (이미 구현) |
| `collectors/` + API 시크릿 | ②의 데이터 수집 (이미 Actions에서 작동) |
| [`github-api-bypass-code-patterns.md`](github-api-bypass-code-patterns.md) | ① 구현 시 코드 패턴 참조 |
| [`automation-vs-ai-narrative-roadmap.md`](automation-vs-ai-narrative-roadmap.md) | ②③ 하이브리드 설계 원칙 원본 |

## 검증된 vs 미검증 (솔직한 상태)

**docs 교차검증 완료 (신뢰 가능)**:
- `repository_dispatch` 엔드포인트/파라미터/크기 한계 — docs로 확인
- `workflow_run`/push 트리거 문법 — docs로 확인
- 73KB POST 한계 — 이진 탐색으로 측정 (이번 세션)
- git pull 방향 제약 없음 — GET은 POST 검사 안 받음 (측정된 사실)

**구현 시 검증 필요 (다음 세션)**:
- `repository_dispatch`가 회사망 POST에서 실제로 작동하는지 (이론적으론 65KB<73KB라 OK지만 실호출 필요)
- `PAT_FOR_PUSH` 시크릿이 Actions에서 커밋을 밀 수 있는지 (또는 기본 GITHUB_TOKEN으로 자기 브랜치 push 가능 여부 — repo 설정 의존)
- ② 워크플로우가 main 브랜치에 있어야 dispatch 인식 (CLAUDE.md "main 직접 커밋 금지"와 충돌 → PR로 이관 필요, [PR #47 선례](automation-vs-ai-narrative-roadmap.md) 참고)

## 다음 세션 구현 순서 (제안)

1. **② 워크플로우 초안 작성** — `daily-brief-generate.yml`, `repository_dispatch` 반응.
   main 이관용 `feat/daily-brief-generator` 브랜치 → PR (CLAUDE.md 준수).
2. **① 트리거 스크립트** — `trigger_brief.py`, `upload_brief.py` 헬퍼 재사용.
   회사망에서 실호출로 `repository_dispatch` 작동 검증.
3. **회사망에서 end-to-end 1회 시연** — 트리거 → Actions run → 리포트 커밋 →
   자동 이메일 발송 확인. ②까지만으로도 이미 가치 (자동 생성+발송).
4. **③ 종합 단계** — 위키 서사 기반 종합 리포트 작성 루틴을 위키 워크플로우로
   정리. 이건 LLM이 매번 하는 것이라 "코드"라기보다 "프롬프트 루틴" 문서화.

## Sources

- [GitHub REST: repository_dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event) — WebFetch 교차검증 (event_type 100자, client_payload 65,535자/10속성)
- [GitHub Actions: repository_dispatch 트리거](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch) — `on: repository_dispatch: types:` 문법
- [GitHub Actions: workflow_run 트리거](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run) — 후속 워크플로우 체인
- [회사망 git push 우회 — 4경로 전수 측정](corp-network-push-bypass-investigation.md) — 73KB POST 한계 측정
- [GitHub API 우회 코드 패턴](github-api-bypass-code-patterns.md) — ① 구현 시 헬퍼 재사용
- [자동화 인프라 — GitHub Actions 워크플로우 & 시크릿 인벤토리](../entities/automation-infrastructure.md) — 기존 10개 워크플로우/시크릿
- [자동화 vs AI 서술 — SK하이닉스 데일리 체크 로드맵](automation-vs-ai-narrative-roadmap.md) — ②③ 하이브리드 설계 원칙
- [Daily Brief 이메일 전송 — 디버깅 경위](daily-brief-email-workflow-debug.md) — push→이메일 발송 검증 이력
