---
name: session-start-checklist
description: 세션 시작 시 반드시 읽을 운영 규칙 · 환경 제약 · 실행 절차 총정리 — 모든 Agent가 이 파일을 먼저 읽고 시작
---

# Session Start Checklist — 세션 시작必读 규칙

> **이 파일이 세션 시작의 단일 출처 (SSOT) 이다.** 모든 Agent는 세션 시작 시 이 파일을 먼저 읽는다.

---

## 🚨 0. MessageBox 확인 (최우선)

`wiki/messagebox.md`를 **가장 먼저** 읽는다.

| 코드 | 의미 | 행동 |
|---|---|---|
| **🔴 HALT** | HALT | **작업 중단** — 다른 Agent나 사람이 기준선 재정렬 중 |
| **🟡 CAUTION** | CAUTION | 읽고 신중 진행 — pull 먼저 하거나 주의 필요 |
| **🟦 INFO** | INFO | 읽고 진행 — 참고용 |
| **없음** | — | 진행 |

**왜?** 누군가 작업 중인 파일을 건드리면 동시 실행 충돌 발생.

---

## 1. 실행 환경 제약 (환경에 따라 무조건 지키기)

### 1.1 Git Bash vs CMD.exe
| 작업 | 허용 | 금지 |
|---|---|---|
| `.bat` 실행 | ✅ CMD.exe / Task Scheduler | ❌ Git Bash |
| `.ps1` 실행 | ✅ PowerShell | ❌ Git Bash |
| `claude -p` 실행 | ✅ CMD.exe / Task Scheduler | ❌ Git Bash |
| 파일 읽기 / git 명령 | ✅ Git Bash / CMD 모두 OK | — |

**규칙**: Windows 환경에서 headless claude 실행은 **반드시 bat/ps1 wrapper를 통해** 실행. Git Bash는 git/파일 읽기만 사용.

### 1.2 bat 파일 작성 규칙
- **모든 줄을 ASCII 영문으로** — bat 내 한글은 CMD 파싱 에러 발생
- **`if/else`는 flat 구조** — 중첩 금지 (goto 라벨 패턴 사용)
- **`pause`**: 수동 실행용에는 추가, Task Scheduler 자동 실행용에는 금지

### 1.3 bat 파일 `if/else` 패턴
```bat
if %RC% equ 0 goto :SUCCESS
if %RC% equ 124 goto :TIMEOUT
goto :FAIL

:SUCCESS
echo OK
goto :DONE

:TIMEOUT
echo TIMEOUT
goto :DONE

:FAIL
echo FAIL

:DONE
```

### 1.4 `file://` 프로토콜 UTF-8 강제
```html
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta charset="utf-8">
```
`<meta http-equiv="Content-Type">`을 `<meta charset>` **앞에** 배치. `file://` 프로토콜에서도 동작.

---

## 2. 웹 검색 — WebSearch/WebFetch 금지

| 도구 | 상태 | 우회 방법 |
|---|---|---|
| `WebSearch` | ❌ 400 Bad Request | `python search.py` |
| `WebFetch` | ❌ 400 Bad Request | `python search.py` |
| `Bash(dispatch.sh)` | ❌ 회사망 우회 금지 | 사용 금지 |
| `python search.py` | ✅ DuckDuckGo 직접 | 권장 |

**규칙**: 모든 검색은 `python search.py "검색어"` 만으로 수행. 병렬 실행 금지 (순차적).

**allowedTools 설정 예시**:
```
'--allowedTools', 'Read Grep Glob Write Edit Bash(python search.py *)'
'--disallowedTools', 'WebSearch WebFetch Bash(dispatch.sh)'
```

---

## 3. 모델명 — `--model` alias 명시

`claude -p` 실행 시 항상 `--model` alias 명시. 직접 모델명 사용 금지.

| 설정 | alias | 직접 모델명 |
|---|---|---|
| Opus | `opus` | GLM-5.2 |
| Sonnet | `sonnet` | gemma-4-31B-it |
| Haiku | `haiku` | Qwen3.6-35B-A3B |

**규칙**: `--model haiku` (alias 사용). `--model Qwen3.6-35B-A3B` 금지 → 400 Bad Request.

---

## 4. 보고서 자동화 실행 패턴

### bat + PS wrapper 구조
```
run_cxl_daily.bat (CMD, ASCII만)
  ├── [1/2] git fetch + pull --rebase
  └── [2/2] claude -p via run_cxl_claude_bounded.ps1
        ├── [Console]::OutputEncoding = UTF8
        ├── --model haiku (alias)
        ├── allowedTools: search.py only
        ├── stdout: sidecar 5초 폴링 → CMD 실시간 출력
        ├── heartbeat: 30초 주기
        └── 완료: CMD 창에 큰 박스 메시지 (Write-Host)
```

### 핵심 규칙
1. **PS wrapper 시작 라인에 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`** — Write-Output 모자이크 방지 (P9)
2. **stdout 실시간 CMD 출력** — sidecar 파일 5초 폴링
3. **heartbeat 30초 주기** — claude 활동 중에는 heartbeat 없이 stdout만 표시
4. **`--model haiku` alias 명시** — 직접 모델명 금지
5. **bat 파일 ASCII만** — 한글은 PS wrapper `Write-Host`에서 처리
6. **bat `if/else` flat 구조** — goto 라벨 패턴
7. **search.py 순차 실행** — 병렬 금지 (메모리 안전)

---

## 5. GitHub / 위키 sync 규칙

### 5.1 기본 원칙
- **한 방향으로만 pull** — push 금지 (최우선 정책)
- **stash-protected pull** — unstaged wiki 파일 stash → pull → pop
- **append-only log** — `wiki/log.md`는 `## 당일 log` 맨 아래에만 append

### 5.2 충돌 방지
- **git push -f 절대 금지** — 상대 작업 통째로 날아감
- **동시 편집** — 같은 파일을 두 Agent가 수정하면 충돌
- **큰 작업** — 별도 branch 격리 후 merge

### 5.3 push 금지
- Track B (회사 업무): GitHub push / email 발송 **전면 금지**
- Track A (개인 투자): 정상 GitHub Actions 시크릿 통한 발송만 허용

---

## 6. 다른 Agent 안전

`wiki/concepts/concurrent-agent-aware-coding.md` — 코드 작성 시 반드시 적용.

**핵심**: 프로세스 kill 매칭 좁히기 (PID/CreationDate), sweep보다 고아를 남기는 쪽이 안전.

---

## 7. Concept 수정 규칙

`wiki/concepts/concept-lifecycle-maturity.md` — Concept 수정의 정당성 4조건 (AND rule):

1. 3회 이상 반복 관찰
2. 기존 가정 위반
3. 신변수 발견
4. 통계적 유의성

**규칙**: 이 4조건 모두 만족할 때만 Concept 수정.

---

## 8. 세션 시작 체크리스트 요약

```
□ 1. wiki/messagebox.md 읽기 (HALT/CAUTION/INFO 확인)
□ 2. wiki/concepts/session-start-checklist.md 읽기 (이 파일)
□ 3. CLAUDE.md 최상단 정책 읽기 (트랙 A/B, 작업 실행 프로토콜)
□ 4. wiki/concepts/log-operating-policy.md 읽기 (R1-R6)
□ 5. 실행 환경 확인: Git Bash → CMD.exe, bat/ps1 wrapper 사용
□ 6. settings.json 확인: CLAUDE_CODE_MAX_OUTPUT_TOKENS = 64000
□ 7. search.py 사용 (WebSearch/WebFetch 금지)
□ 8. --model haiku 명시
□ 9. git pull (stash-protected)
□ 10. 작업 시작
```

---

## 관련 문서

| 문서 | 설명 |
|---|---|
| [log-operating-policy.md](log-operating-policy.md) | R1-R6 log 운영 규칙 |
| [multi-terminal-wiki-sync-design.md](multi-terminal-wiki-sync-design.md) | 다중 터미널 위키 동기화 |
| [automation-strategy-and-delivery-boundary.md](automation-strategy-and-delivery-boundary.md) | 트랙 A/B 경계 |
| [concurrent-agent-aware-coding.md](concurrent-agent-aware-coding.md) | 동시 실행 Agent 안전 |
| [multi-client-conflict-prevention.md](multi-client-conflict-prevention.md) | 충돌 방지 git 규칙 |
| [concept-lifecycle-maturity.md](concept-lifecycle-maturity.md) | Concept 수정 4조건 |
| [report-generation-lessons-learned-2026-08-20.md](report-generation-lessons-learned-2026-08-20.md) | 보고서 생성 Lessons Learned |
| [cmd-bounded-report-execution-pattern-2026-08-21.md](cmd-bounded-report-execution-pattern-2026-08-21.md) | bat/PS wrapper 패턴 |
| [headless-claude-autonomous-cycle.md](headless-claude-autonomous-cycle.md) | 자동화 사이클 아키텍처 |
