---
title: 다중 클라이언트 충돌 방지 운영 (모바일 + desktop)
created: 2026-08-03
updated: 2026-08-03
tags: [git, workflow, multi-client, conflict-prevention, ops, mobile]
---

모바일 Claude Code와 desktop Claude Code가 **같은** `stevekoo-ai/Repo_name.git`
서사 브랜치(`claude/ai-agent-impl-002tip`)에서 위키/코드를 동시에
갱신하는 환경의 충돌 방지 규칙. 두 클라이언트 모두 git을 직접
조작(commit/push)하므로, pull-before-write + 세션 마커 + 역할 분담
3축으로 충돌 창을 최소화한다. [CLAUDE.md 7-3/9-3 브랜치 전략](../CLAUDE.md)
의 운용 세부.

## 전제 (2026-08-03 확인)

- **두 클라이언트 모두 git 직접 조작** (모바일 Claude Code + desktop Claude Code)
- 같은 원격 `stevekoo-ai/Repo_name.git`, 서사 브랜치 `claude/ai-agent-impl-002tip`
- 같은 파일 풀(`wiki/`, `sources/`)을 편집 → 실질적 동시 편집 충돌 가능
- `main` 브랜치는 GitHub Actions 전용, 사람/에이전트 직접 커밋 금지
  ([CLAUDE.md 9-3](../CLAUDE.md))

## 가장 먼저: 기준선 확립 (1회성, desktop에서)

충돌 방지 규칙이 의미를 갖으려면 **양쪽이 같은 기준선 위에 있어야** 한다.
현재 desktop 로컬은 커밋 0개·리모트 미연결 상태이나 파일은 가득 — 즉
로컬과 GitHub이 조용히 분기(diverge)되어 있다. 이 상태에서 무심코
push/pull하면 한쪽 작업이 통째로 날아갈 수 있다.

절차:
1. remote 연결: `git remote add origin https://github.com/stevekoo-ai/Repo_name.git`
2. `git fetch origin`
3. remote HEAD와 로컬 파일의 **diff 분석** (어느 쪽이 더 최신인지, 양쪽에
   서로 없는 작업이 있는지)
4. 전략 선택:
   - (a) 로컬 = remote 최신 → remote 기준 reset 후 로컬 변경분만 patch
   - (b) 로컬에 remote 없는 신규 작업 → 로컬을 별도 branch로 커밋 후 merge
5. **이 작업 중 모바일에게 알려 push를 멈추게 함** (동시 push 경합 방지)

GitHub 인증은 자격 증명 관리자의 classic PAT(`ghp_`, push 권한 보유)로
이미 검증됨 → [사내 LLM 라우팅 페이지](claude-code-internal-routing.md)의
GitHub API 검증 섹션 참조.

## 핵심 메커니즘 5가지 (지속 운영)

### ① Pull-before-write + 즉시 push
모든 세션 **시작 시** `git fetch && git pull --rebase`. 작은 작업(ingest
하나, log 한 줄)이 끝나면 **즉시 push** — 다른 클라이언트가 다음 pull에서
바로 보게. 두 클라이언트가 동시 편집하는 시간창을 최소화한다. `--rebase`
핵심 — merge commit이 쌓여 위키 히스토리가 지저분해지는 걸 막는다.

### ② Append-only log.md (자동 병합)
`log.md`는 양쪽 모두 맨 아래에만 추가 ([CLAUDE.md 5](../CLAUDE.md) 규칙).
같은 줄만 아니면 git이 **다른 줄에 추가된 두 append를 자동 병합**.
진짜 충돌 위험은 `index.md`와 entities/concepts 페이지 동시 편집 — 이건
아래 ④로 회피.

### ③ 세션 인텐트 마커 (`.wiki/active-session.json`) — 가벼운 lock
세션 시작 시 자신의 작업 영역을 파일로 표시, 종료 시 제거. 상대 세션이
시작할 때 읽고 겹치면 **기다리거나 다른 파일 먼저**.

구조:
```json
{
  "client": "mobile | desktop",
  "session_id": "<고유 ID>",
  "started_utc": "<ISO 시각>",
  "scope": ["wiki/index.md", "wiki/entities/sk-hynix.md"],
  "note": "SK하이닉스 entity 대량 갱신 중"
}
```

규칙:
- 세션 시작: 파일 읽어 **활성 세션 목록** 확인 → 내 scope와 겹치는
  활성 세션이 있으면 (a) 그 세션이 끝날 때까지 대기, (b) 안 겹치는
  파일부터 먼저 처리
- 세션 종료: 자신의 entry 제거 후 push
- 무거운 lock이 아님 — "지금 이 파일 건드리는 중" 신호일 뿐, 강제력 없음
- 30분 이상 갱신 없는 entry는 죽은 세션으로 간주·무시 (stale 제거)

### ④ 큰 작업은 branch 격리
| 작업 유형 | 방식 |
|---|---|
| 모바일 대화형 ingest/query (위키 갱신) | 공유 브랜치에서 직접, 빠른 pull/push |
| desktop PEOS 코드 대량 변경, lint 전면 수정 | 별도 branch(`claude/peos-xxx`) → PR merge |

큰 작업 격리 시 "한창 코드 고치는데 모바일이 위키 밀어넣어 rebase 지옥"
방지. PR merge는 [CLAUDE.md 9-1](../CLAUDE.md)에 따라 사용자 승인 후.

### ⑤ Push 경합 실패 시 rebase 재시도
`git push`가 `rejected(fetch first)`면 rebase 후 최대 5회 재시도.
(log.md에 PR #23으로 추가한 GitHub Actions 재시도 로직과 동일 패턴)

## 역할 분담 (자연 충돌 최소화)

| 클라이언트 | 주 역할 | 주로 건드리는 파일 |
|---|---|---|
| **모바일** | 대화형 위키 갱신 (ingest/query) | `sources/*`, `wiki/summaries/*`, `wiki/log.md` |
| **desktop** | 깊은 분석, 코드, 대량 정리 | `scripts/`, `wiki/concepts/*`, `wiki/entities/*`, `.github/` |

역할이 겹치는 순간만 진짜 충돌 → 분담하면 대부분 자연 해소. `log.md`는
둘 다 append하지만 (②) 자동 병합되어 사실상 충돌 안 남.

## 충돌 실제 발생 시 복구

rebase 중 충돌이 나면:
1. `git status`로 충돌 파일 확인
2. `log.md` 충돌 → 양쪽 append 모두 보존 (두 섹션을 시간순 병합)
3. entity/concept 충돌 → **최신 날짜/내용 기준으로 한쪽 채택**, 다른 쪽
   내용은 해당 페이지 하단에 "대안 서술"로 보존하거나 log에 기록 후 폐기
4. `index.md` 충돌 → 줄 단위 병합 (두 클라이언트가 같은 페이지 줄을
   동시에 고쳤을 때만 수동, 보통은 서로 다른 줄이라 자동 병합)
5. 해결 후 `git rebase --continue` → push

절대 `git push -f` (force)로 덮어쓰지 않는다 — 상대 작업 통째로 날아감.

## Sources

- 2026-08-03 사용자 대화: 모바일+desktop 동시 운영 충돌 방지 전략 논의
  (모바일도 git 직접 조작 확인, 세션 마커 도입 합의)
- [CLAUDE.md 7-3 브랜치 분리, 9-3 브랜치 전략](../CLAUDE.md)
- [사내 LLM 라우팅 & GitHub API 검증](claude-code-internal-routing.md)
- [wiki/log.md 2026-08-03 PR #23 재시도 로직 선례](../log.md)
