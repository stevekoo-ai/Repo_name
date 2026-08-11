---
title: Log 운영 정책 — 다중 Agent 공유 규칙
created: 2026-08-07
updated: 2026-08-11
tags: [ops, log-rotation, multi-agent, policy, must-read]
---

# Log 운영 정책 — 다중 Agent 공유 규칙

> **모든 Agent(모바일·데스크톱·제3의 AI 채널)이 `wiki/log.md`를 쓸 때
> 반드시 지킬 운영 정책.** 세션 시작 시 이 페이지를 한 번 읽을 것.
> log 회전(과거 항목 cut·요약 갱신)은 3층 자동화가 하므로 **Agent는
> 회전을 건드리지 않고 `## 당일 log` 맨 아래에만 append**하면 된다.
> 이 페이지가 log 운영 규칙·회전 설계·degradation 표의 **단일 출처**다
> (CLAUDE.md의 Startup Protocol line 4 "Review operational context
> (log.md ...)"가 여기로 연결된다).

## TL;DR (3줄)

1. **log는 append-only.** `## 당일 log` 맨 아래에만 한 줄 append. 같은
   줄만 아니면 git이 자동 병합하므로 동시 편집 충돌 안 남.
2. **회전(과거 항목 cut)은 자동화가 한다. Agent가 직접 cut/수정/삭제 금지.**
3. **요약 섹션(`## 당월 요약`/`## 직전월 요약`)도 자동화가 갱신. 건드리지 마라.**

## log.md 3-tier 구조 (누가 갱신하는가)

```
# Log
[header + rotation note]
## 직전월 요약 (YYYY-MM)        ← 자동화(Windows 층, 월초 승격). Agent 건드리지 마라.
## 당월 요약 (YYYY-MM) — 진행중  ← 자동화(Windows 층, 매일 1줄). Agent 건드리지 마라.
## 당일 log (append-only)       ← Agent가 맨 아래에만 append.
2026-08-07 09:50 KST — QUERY ...
```

| 섹션 | 누가 갱신 | Agent가 해도 되는가 |
|------|----------|-------------------|
| `## 직전월 요약` | Windows 층 LLM (월초 자동 승격) | ❌ 건드리지 마라 |
| `## 당월 요약` | Windows 층 LLM (매일 어제 아카이브 2~3줄) | ❌ 건드리지 마라 |
| `## 당일 log` | **Agent** (맨 아래 append) + GitHub 층 (과거 날짜 cut) | ✅ 맨 아래에만 append |

**핵심**: Agent가 log를 쓴다는 건 `## 당일 log` 맨 아래에 한 줄 추가하는
것만 의미한다. 나머지 섹션은 자동화가 관리.

## Agent가 log 쓸 때 지켜야 할 규칙 (핵심 6)

### R1: `## 당일 log` 맨 아래에만 한 줄 append

log.md는 append-only. 한 줄 형식:
```
YYYY-MM-DD HH:MM KST — TYPE 동사(객체) → 결과(생성/갱신 파일, PR, 결론)
```
- TYPE: `INGEST`/`QUERY`/`CODE`/`ANALYSIS`/`REPORT`/`CHECK`/`CORRECTION`/`SYNC`/`LINT`/`ROTATE`
- 같은 줄만 아니면 git이 다른 줄의 append를 자동 병합 → 동시 편집 충돌 안 남.
- **절대 중간 항목을 삽입/수정/삭제하지 마라.** append는 맨 아래만.

### R2: 과거 날짜 항목 cut/수정/삭제 금지

회전(cut)은 GitHub Actions 층이 매일 00:20 KST에 어제 항목을 아카이브로
이관. Agent가 직접 과거 항목을 지우면 자동화와 충돌하고 데이터 손실 발생.
- 오늘 항목이 아닌 `^YYYY-MM-DD` 항목은 그대로 둘 것.
- "log.md가 너무 크다"고 판단해 수동 cut 금지 → 자동화가 알아서.

### R3: 요약 섹션(`## 당월 요약`/`## 직전월 요약`) 건드리지 마라

이 섹션은 Windows 층 LLM(claude -p → 사내 GLM)이 매일 00:40 KST에
어제 아카이브 기반으로 2~3줄 서술 요약을 갱신(idempotent — 같은 날짜 줄 교체).
Agent가 직접 요약 줄을 쓰거나 지우면 다음 자동 실행이 덮어쓰거나 충돌.

### R4: 회전 전 load-bearing 확인 (log.md 외 페이지 아카이브 시)

log.md 외 페이지(예: concept/entity 페이지의 표·행)의 과거 행을
아카이브할 땐, 그 사실이 다른 곳에 중복됐는지 먼저 grep으로 확인:
1. `grep -r "그 행의 핵심 사실" wiki/` — 다른 페이지가 의존하는가?
2. 그 행의 사실이 다른 "현재 상태" prose 섹션에 이미 restated됐는가?
3. 한 곳에만 있다면 → 1줄 요약을 prose 섹션에 먼저 fold한 뒤 cut,
   또는 한 로테이션 더 보존.
- log.md 자체 회전엔 이 확인 불필요(순수 일기라 age=staleness).

### R5: 한 줄 형식 준수 + KST 시각

- 시각은 KST(UTC+9). `TZ=Asia/Seoul date '+%Y-%m-%d %H:%M %Z'`로 확보.
- 한 이벤트 = 한 줄. 여러 줄 쓰지 마라 (병합·가독성·로테이션 단위).
- 결과는 구체적으로: `created entities/foo.md`, `updated concepts/bar.md`,
  `PR #52`, 파일 크기, 결론 한 줄.

### R6: 동시 실행 Agent 고려

- 세션 시작 시 `git fetch origin && git checkout claude/ai-agent-impl-002tip
  && git pull --rebase` (서사 브랜치로 전환 + 동기화).
- `wiki/messagebox.md` 가장 먼저 읽기. 🔴 HALT 있으면 해당 작업 끝날 때까지
  sync 대기. 🟡 CAUTION이면 pull 먼저. 🟦 INFO면 읽고 진행.
- 큰 변화(기준선 재정렬·브랜치 구조 변경·대량 리팩터·스키마 변경)는
  messagebox에 게시. 작은 log 한 줄은 게시 불필요.
- `git push -f`(force) 절대 금지 — 상대 작업 통째로 날아감.

## 3층 자동화가 무엇을 하는지 (Agent가 알아야 할 만큼만)

| 층 | 실행 주체 | 시각 | 하는 일 | 상태 |
|---|---|---|---|---|
| GitHub Actions | `log-rotate.yml`(main) → `log_rotate.py` | 00:20 KST 매일 | 어제 항목 cut → 일자별 아카이브 이관 + 월말 월 아카이브 병합 | ✅ 배포·실증 완료 |
| Windows Task Scheduler | `log_summarize_routine.bat` → `claude -p`(GLM, 무료) | 00:40 KST 매일 | 어제 아카이브 2~3줄 한국어 서술 요약 → log.md `## 당월 요약` 갱신 (로컬) | ✅ 등록 완료·자동 실행 중 (8/8~8/10 실증) |
| Live session | 세션 시작 시 `wc -c log.md > 50000` | on-demand | 정성/복구 + 즉시 cut(안전망) | 부분 (best-effort) |

> **Windows 층 비고 (2026-08-10 실측)**: `log_summarize_routine.bat` +
> `run_log_summarize_bounded.ps1` + `.claude/prompts/log-summarize.md` 는
> 완성됐고, `schtasks /TN LogSummarize /SC DAILY /ST 00:40` 등록 완료.
> **8/8·8/9·8/10 매일 00:40 KST 자동 실행 실증**(`.claude/logs/log-summary-2026MMDD-004005.log`,
> `claude -p` rc=0, 64~191s 정상 응답). 빈 stdout 해결(`--append-system-prompt-file`
> 주입)도 자동 실행에 적용됨. 3층 전부 가동 중 — Agent는 회전·요약 갱신
> 건드리지 말고 `## 당일 log` 맨 아래만 append.
> (이전 "schtasks 미등록" 기술은 2026-08-10 정정 — Git Bash MSYS 경로
> 변환으로 schtasks query가 실패한 것을 미등록으로 오해한 것.)

**graceful degradation** (모든 작업 idempotent — 누가 먼저 돌든/겹치든 결과 동일):

| 상황 | GitHub | Windows | 결과 |
|---|---|---|---|
| 노트북 OFF(주말/공휴일) | cut OK | 안 돔 | 크기 제어 OK, 그날 요약 생략(전문은 아카이브에) |
| GitHub 지연/누락 | 안 돔 | 자체 cut + 요약 | 완전 커버 |
| 둘 다 다운 | — | — | log.md +~17KB/일, 다음 run의 idempotent cut가 catch-up |
| 자폭(daemon self-restart) | 면역 | 면역(OS 레벨) | 둘 다 생존 |

## 아카이브 구조 (2-tier)

```
wiki/log-archive/
  YYYY-MM.md                  ← 완료월 cold archive (GitHub 층이 월초 병합)
  YYYY-MM/
    YYYY-MM-DD.md             ← 당월 과거 일자 (GitHub 층이 매일 cut)
```

- 오늘 항목은 `## 당일 log`에 살아있고, **내일 자정에** GitHub 층이
  오늘을 "어제"로 인식해 `YYYY-MM/YYYY-MM-DD.md`로 cut.
- 과거 history 찾는 순서: log.md `## 직전월 요약` → `## 당월 요약` →
  `log-archive/YYYY-MM/YYYY-MM-DD.md` → `log-archive/YYYY-MM.md`.

## "자동화가 돌고 있는지" 확인하는 4곳

| 보는 곳 | 돌고 있으면 | 안 돌고 있으면 |
|---------|-----------|--------------|
| GitHub 리포 Actions 탭 → `Log Rotate` 워크플로우 | 매일 15:20 UTC run ✅ | run 없음 |
| `wiki/log-archive/YYYY-MM/` | 어제 날짜 .md 있음 | 없음 |
| `wiki/log.md` `## 당월 요약` | 날짜 줄 매일 증가 | 멈춤 |
| `.claude/logs/log-summary-latest.log` | 오늘 시각 + "routine end" | 옛날 시각 |

가장 빠른 한 줄 확인 (Windows 층):
```
type C:\Users\2053437\.claude\logs\log-summary-latest.log
```

## 금지 사항

- `git push -f`(force) — 상대 작업 통째로 날아감.
- `sources/` 파일 수정/삭제 (immutable, 새 파일만 추가).
- `## 당일 log` 과거 날짜 항목 직접 cut/수정/삭제 (자동화가 함).
- `## 당월 요약`/`## 직전월 요약` 섹션 직접 갱신 (Windows 층 LLM이 함).
- messagebox 🔴 HALT 무시.
- 빈 stdout 재발 — 헤드리스 `claude -p` 래퍼 짤 때 `--append-system-prompt-file`
  필수 (사내 GLM 라우팅 시 system prompt 주입이 응답 생성의 실질적 트리거).
- 좁은 타임아웃(예: 90초)으로 무거운 headless 작업 테스트 — 타임아웃 분기 발동 →
  process sweep 위험. 상세는 [concurrent-agent-aware-coding.md](concurrent-agent-aware-coding.md).

## Sources

- [로그 로테이션 3인 하이브리드 자동화 — 인프라](log-rotation-3hybrid-infra.md) — 산출물·배포 이력·실행 추적 (이 페이지의 운영 규칙과 한 쌍)
- [다중 클라이언트 충돌 방지 운영](multi-client-conflict-prevention.md) — 동시 편집·messagebox·브랜치 규칙
- [동시 실행 Agent 고려 코딩](concurrent-agent-aware-coding.md) — process kill/sweep 금지, 고아 남기기
- 2026-08-10 실측: `schtasks /query` 로 `LogSummarize` 작업 부재 확인 → Windows 층 자동 등록 미완료 상태 기록 근거
