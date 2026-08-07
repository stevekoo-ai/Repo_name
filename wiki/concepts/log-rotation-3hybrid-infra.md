---
title: 로그 로테이션 3인 하이브리드 자동화 — 인프라
created: 2026-08-07
updated: 2026-08-07
tags: [ops, automation, log-rotation, github-actions, infra]
---

# 로그 로테이션 3인 하이브리드 자동화 — 인프라

`wiki/log.md`가 3주 만에 193KB까지 커져 토큰 비용·context 한계 요인이
된 것을 해결하기 위한 자동 회전 인프라. 매일 자정 직후 어제 항목을
일자별 아카이브로 잘라내 log.md를 당일 중심으로 작게 유지한다.

> **설계·규칙·graceful degradation 표는 [CLAUDE.md](../../CLAUDE.md)
> "Log rotation" 섹션에 전부 있음.** 이 페이지는 그 인프라의
> **산출물(파일)·배포 상태·실행 이력**을 추적하는 운영 페이지다.

## 3층 구조 (각 층의 역할)

| 층 | 실행 주체 | 시각 | 산출물 | 상태 |
|---|---|---|---|---|
| GitHub Actions | `log-rotate.yml`(main) → `log_rotate.py` | 00:20 KST 매일 | `log-archive/YYYY-MM/YYYY-MM-DD.md` + 월말 월 아카이브 병합 | ✅ 배포 완료 (2026-08-07 실증) |
| Windows Task Scheduler | `log_summarize_routine.bat` → `claude -p`(GLM) | 00:40 KST 매일 | `log.md` `## 당월 요약` 2~3줄 갱신 + Contents API PUT | ❌ 미등록 (schtasks 등록 필요) |
| Live session | 세션 시작 시 `wc -c > 50KB` | on-demand | 정성/복구 + 즉시 cut | 부분 (이번 세션에서 72KB 초과 안 건드림) |

## 산출물 파일 목록

### GitHub 층 (✅ main + 서사 브랜치 양쪽 배포 완료)
- `.github/workflows/log-rotate.yml` — schedule `20 15 * * *`(=00:20 KST),
  `workflow_dispatch`(수동 실행, `target_date` 입력 optional). 서사
  브랜치 checkout → cut → Bot commit/push. main에 있어야 schedule 발화.
- `scripts/log_rotate.py` — deterministic 회전 로직(순수 Python, LLM 없음).
  dry-run/실 cut/월병합 지원. idempotent(아카이브 존재 시 skip).

### Windows 층 (❌ 로컬만, schtasks 미등록)
- `scripts/log_summarize_routine.bat` — 3단계(git pull → `claude -p`
  GLM 요약 → Contents API PUT). 00:40 KST.
- `scripts/run_log_summarize_bounded.ps1` — `claude -p` 래퍼(시간 제한).
- `scripts/upload_log_summary.py` — log.md 단일 파일 Contents API PUT.
- `prompts/log-summarize-headless.txt` — 헤드리스 요약 프롬프트.

### 배포 보조 (이번 세션 신설)
- `scripts/push_log_rotate_to_main.py` — main에 rotation 파일 PUT
  (3가지 함정 적용).
- `scripts/push_log_rotate_to_narrative.py` — 서사 브랜치에 PUT.

## 배포 이력 (2026-08-07)

| 단계 | 결과 |
|---|---|
| 진단 | rotation 파일 6종 전부 untracked(한 번도 commit 안 됨). log-rotate.yml main 없음 → schedule 발화 0회 |
| main 배포 | Contents API PUT 성공: log-rotate.yml(9889eba), log_rotate.py(c6d8a19) |
| 첫 run(31152276405) | **실패** — 서사 브랜치 checkout 시 log_rotate.py 없어 FileNotFoundError |
| 서사 배포 | 스크립트 4종 PUT: f9f7b78/c62a95e/efafba/f1f60d |
| 두 번째 run(31153363185) | **성공** — Bot commit cbf80c2, `2026-08-06.md` 생성, log.md 72KB→25KB |

**핵심 교훈:** workflow 파일과 그 workflow가 실행하는 스크립트는
**같은 브랜치**(특히 checkout 대상 브랜치)에 있어야 한다. schedule은
default branch(main)에 workflow 파일이 있어야 발화하지만, checkout하는
브랜치에 스크립트가 없으면 runner가 FileNotFoundError로 죽는다. →
**main과 서사 브랜치 양쪽에 스크립트를 두어야** schedule 발화(main)와
실행(서사 checkout)이 모두 성립.

## 아카이브 구조 (실제)

```
wiki/log-archive/
  2026-07.md                  ← 완료월 cold archive (mobile 2026-08-04 수동 cut)
  2026-08-early.md            ← 🟡 규칙 밖 임시 파일 (8/1~8/5, dispatch 용량 회피용 수동 cut)
  2026-08/
    2026-08-06.md             ← ✅ workflow가 처음 만든 정식 일일 아카이브 (cbf80c2)
```

> `2026-08-early.md`는 3인 하이브리드 도입 전, 회사망 dispatch 용량
> 한계 회피용으로 수동 잘라낸 임시 파일. 규칙상 2-tier(월 아카이브 +
> 일일 폴더)에 없는 파일이므로, 다음 정리 시 정식 구조로 통합하거나
> 규칙에 "과도기 임시 파일 허용"을 한 줄 추가해야 (미해결).

## 미구현 (사용자 액션 대기)

1. **Windows Task Scheduler 등록** — `log_summarize_routine.bat`를
   schtasks로 00:40 KST 매일 등록. 등록 안 되면 `## 당월 요약`/`## 직전월
   요약` 섹션이 계속 빈 상태로 남음(GitHub 층 cut은 정상 작동해도).
2. **`2026-08-early.md` 처리 결정** — 임시 파일을 정식 구조로 통합할지
   규칙 보완할지.
3. **log.md 중복 항목 정리** — 8/4·8/6 항목이 multi-client 동시 편집으로
   중복되어 있는 것 정리(현재 cut 후라 8/6은 아카이브로, 8/4는 여전히
   log.md에 2개).

## Sources

- [CLAUDE.md](../../CLAUDE.md) "Log rotation" 섹션 — 설계·규칙·degradation 표
- [회사망 GitHub API 우회 push — 코드 작성 시 필수 함정 3종](corp-github-api-push-gotchas.md) — 배포 스크립트의 3가지 함정 적용 근거
- [메세지박스](../messagebox.md) 2026-08-07T13:50Z 항목 — 도입 게시
- 2026-08-07 실증: main 배포 → 첫 run 실패 → 서사 배포 → 두 번째 run 성공(commit cbf80c2)
