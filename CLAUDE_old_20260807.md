# Wiki schema

This repo implements the "LLM Wiki" pattern (see
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of
re-deriving answers from raw sources on every query, an LLM incrementally
builds and maintains a persistent, interlinked markdown wiki that synthesizes
what's in the sources. You (the human) curate sources and ask questions; the
LLM does the bookkeeping.

## Layers

1. `sources/` — raw, immutable inputs (articles, notes, transcripts, papers,
   whatever). Never edit or delete files here as part of a wiki workflow. Add
   new sources as new files.
2. `wiki/` — the LLM-maintained knowledge base. Everything here can be
   regenerated from `sources/` in principle, but treat it as durable: it
   embodies synthesis work that's expensive to redo.
3. This file — the schema. It defines structure, conventions, and workflows.
   Update it yourself when the wiki's shape needs to change; the agent
   should not restructure the schema unprompted.

## Wiki structure

```
wiki/
  index.md            content-oriented catalog: every page, one line each
  log.md              chronological, append-only event log (current month only — see rotation below)
  log-archive/         log.md rotated out by month: YYYY-MM.md, cold storage
  summaries/           one page per ingested source, distilled
  entities/            one page per recurring person/org/product/thing
  concepts/            one page per recurring idea/topic/theme
```

Only create a new top-level folder under `wiki/` if an existing one clearly
doesn't fit — don't fragment the taxonomy further than this.

## Page conventions

- Filenames: kebab-case, `.md`.
- Every page starts with frontmatter:
  ```
  ---
  title: <Title>
  created: <YYYY-MM-DD>
  updated: <YYYY-MM-DD>
  tags: [tag1, tag2]
  ---
  ```
- Body is distilled prose an LLM would actually want to re-read later — not a
  dump of the source. Preserve exact quotes, numbers, or dates only where
  precision matters.
- Every page ends with a `## Sources` section listing the `sources/` files
  (and/or other wiki pages) it was derived from.
- Cross-link liberally using standard relative markdown links, e.g.
  `[Some Entity](../entities/some-entity.md)`. When you update a page, check
  whether pages it now relates to should link back.

## index.md conventions

One line per wiki page, grouped by folder:
```
### entities
- [Some Entity](entities/some-entity.md) — one-line summary

### concepts
- [Some Concept](concepts/some-concept.md) — one-line summary
```

## log.md conventions

Append-only, newest entry at the bottom. One line per event:
```
YYYY-MM-DD HH:MM UTC — INGEST sources/foo.md → created entities/foo.md, updated concepts/bar.md
YYYY-MM-DD HH:MM UTC — QUERY "question text" → cited entities/foo.md, concepts/bar.md
YYYY-MM-DD HH:MM UTC — LINT → 2 issues found (see report)
```

### Log rotation (3인 하이브리드 자동화 — 2026-08-07 개정, 2026-08-04 도입)

`log.md` grew to 193KB / 225 lines in its first 3 weeks (3x/day automated
routines + ad-hoc queries, never pruned) — expensive to read every session
and a real contributor to hitting context limits. The first cut at
2026-08-04 was a monthly manual cut. As of 2026-08-07 this is fully
automated via a **3-way collaboration** (GitHub Actions + Windows Task
Scheduler + live Claude session), each covering the others' gaps:

- **GitHub Actions (`log-rotate.yml`, 00:20 KST daily, on `main`)** — the
  always-on backbone. Deterministic Python (`scripts/log_rotate.py`, no
  LLM): cuts yesterday's (KST) entries from `log.md` into
  `wiki/log-archive/YYYY-MM/YYYY-MM-DD.md` and pushes (runner is on GitHub
  infra → no 73KB corp-net limit; large monthly archives go up here too).
  On the 1st of each month it also consolidates the previous month's daily
  archive folder into `wiki/log-archive/YYYY-MM.md` and deletes the daily
  files. Idempotent (archive already exists → skip cut), so GitHub's
  documented schedule delays/drops are safe: a late or missed run just
  runs again the next day and catches up. Immune to the local-daemon
  self-restart ("자폭") problem — GitHub schedule runs on GitHub infra,
  outside the local daemon's blast radius.
- **Windows Task Scheduler (`scripts/log_summarize_routine.bat`, 00:40 KST
  daily, laptop ON assumed)** — the free-LLM layer. After pulling the cut
  the GitHub layer made, `claude -p` routes to the corp GLM gateway ($0,
  no personal API cost) and writes a 2~3-line Korean prose summary of
  yesterday's archive into `log.md`'s `## 당월 요약 (YYYY-MM)` section
  (idempotent: same-day re-run replaces that day's line). On the 1st it
  also promotes last month's summary to `## 직전월 요약 (YYYY-MM)` as a
  "this month's key shifts" 10~15-line narrative, and starts a fresh
  `## 당월 요약` for the new month. Uploads `log.md` via Contents API PUT
  (<73KB after cut → corp-net safe). If the GitHub layer didn't run, this
  layer does its own fallback cut directly from `log.md`.
- **Live Claude session** — quality + recovery. On session start, if
  `wc -c wiki/log.md > 50000`, run the cut immediately (safety net if both
  auto layers missed). Optionally promote a stub summary line to richer
  prose. Fix either auto layer when present. This is best-effort, not
  load-bearing — the system works without any session present.

**Graceful degradation** (all operations idempotent — who runs first or
whether runs overlap doesn't matter, results are the same):

| situation | GitHub | Windows | result |
|---|---|---|---|
| laptop OFF (weekend/holiday) | cut OK | doesn't run | size control OK, that day's prose summary skipped (full text still in archive) |
| GitHub delayed/dropped | doesn't run | own cut + summary | fully covered |
| both down | — | — | log.md +~17KB/day, next run's idempotent cut catches up (safe) |
| 자폭 (daemon self-restart) | immune | immune (OS-level) | both survive |

**`log.md` structure (3 tiers):**
```
# Log
[header + rotation note]
## 직전월 요약 (YYYY-MM)   ← narrative, ~10-15 lines (Windows layer, month-start)
## 당월 요약 (YYYY-MM) — 진행중   ← one 2-3 line entry per day (Windows layer, daily)
## 당일 log (append-only)   ← raw dated entries, today + any not-yet-cut days
2026-08-07 09:50 KST — QUERY ...
```
The `## 당일 log` section (raw `^YYYY-MM-DD` entries) is append-only and
**never edited by rotation** — rotation only *moves* whole past days out
to archive and *writes/updates* the two summary sections. Live sessions
still append to the bottom as before.

**Archive structure (2 tiers):**
- `wiki/log-archive/YYYY-MM.md` — completed-month cold archive (GitHub
  layer consolidates the daily folder into this at month start).
- `wiki/log-archive/YYYY-MM/YYYY-MM-DD.md` — current month's past days
  (GitHub layer cuts here daily). Folder is deleted after consolidation.

Looking for old history: check `log.md`'s `## 직전월 요약` first (narrative
summary), then `## 당월 요약` (current month's daily summaries), then
`log-archive/YYYY-MM/YYYY-MM-DD.md` (that day's full entries), then
`log-archive/YYYY-MM.md` (consolidated month).

**What this does *not* change:** still append-only, still one line per
event, still every ingest/query/lint. The 3-tier summary is a
size/rotation optimization + context-preservation layer on top of the
same log. Multi-client note: the daily cut is per-day-idempotent and runs
in a low-activity window (00:20~00:40 KST), so it doesn't conflict with
the append-only auto-merge property the
[multi-client-conflict-prevention.md](wiki/concepts/multi-client-conflict-prevention.md)
doc relies on for concurrent sessions.

**Before rotating any page other than `log.md` (2026-08-04 refinement, user
feedback):** a pure calendar-month cut is too blunt on its own — age isn't
the same as irrelevance. Before archiving a table/section's old rows,
check whether they're still load-bearing:

1. Grep the rest of the wiki (including the file's own still-live prose
   sections) for anything that cites or depends on the specific old
   entries being cut — table rows in this wiki have no per-row anchors, so
   in practice this means checking whether the *fact* in that row is only
   ever stated there, or whether it's already been promoted into a durable
   "current state" prose section elsewhere on the page (checkpoints.md's
   "핵심 체크포인트", macro-regime-history.md's "0."/"4." sections, etc.
   already work this way — dated tables are an audit trail, not the
   only copy of the finding).
2. If a fact is *only* in the row about to be archived and nothing else
   currently cites or restates it, don't just cut it — either fold a
   one-line durable summary into the relevant prose section first (so the
   knowledge survives the cut even if the row's full detail goes cold),
   or leave that row live one more rotation cycle.
3. Report what you checked, not just what you cut — e.g. "verified 0
   pages link to a specific archived row; the facts in it are already
   restated in section X" — so this stays auditable rather than assumed.

This is why `log.md`'s own rotation doesn't need this extra check — it's
a pure chronological diary with no "current state" duplicate elsewhere by
design, so age and staleness are the same thing there. That's not true for
concept/entity pages, which mix a changelog-shaped table with durable
prose that the changelog feeds into.

## Workflows

### Ingest (`/ingest <path-or-text>`)

1. Read this file if you haven't already this session.
2. Read the source. If the argument names a file under `sources/`, read it;
   otherwise treat the argument as inline source text and save it to
   `sources/` first (pick a sensible filename) before proceeding.
3. Read `wiki/index.md` and grep `wiki/` for topics the source touches.
4. Prefer updating an existing page over creating a new one when the source
   adds to something already covered. Only create a new page when nothing
   existing fits — don't create near-duplicate pages.
5. Update every cross-reference the change touches, in both directions.
6. Update `wiki/index.md` and append one line to `wiki/log.md`.
7. Report which pages were created vs. updated.

### Query (`/query <question>`, and ordinary conversation)

Applies to explicit `/query` calls and to any conversational question or
discussion in the session — not just slash-command invocations. Every such
exchange must leave a trace in the wiki; nothing gets discussed and then
lost. No need to ask permission first — record, then move on.

1. Read `wiki/index.md` and grep `wiki/` for pages relevant to the question.
2. Answer the question, citing which wiki page(s) support each claim.
3. **Always record the exchange — recording is mandatory, never optional.**
   Judge how much it matters and size the write-up accordingly:
   - Important/new/insight-bearing: write a proper entry into the relevant
     existing page (new page only if nothing fits) — include the reasoning
     or insight behind it, not just the bare fact, cross-linked as usual.
   - Minor, a repeat, or adds nothing new: a brief note is enough (a short
     line on the relevant page, or just the `log.md` entry if there's truly
     nothing page-worthy) — don't skip it, just don't over-write it.
   - Write first; don't wait for the user to confirm before recording.
4. Append one line to `wiki/log.md` describing what happened either way.

### Lint (`/lint`)

1. Walk every page under `wiki/`.
2. Flag: contradictions between pages, claims no longer supported by any
   source, orphaned pages (not reachable from `index.md`), missing
   cross-references (two pages clearly about the same thing that don't link
   to each other), and broken links.
3. Report findings as a list; don't auto-fix without confirmation.
4. Append one line to `wiki/log.md` summarizing the count of issues found.

---

## 운영 규칙 (Operating Principles)

### 동기화 & 메세지박스 (Sync & Message Box)

한 저장소를 mobile과 desktop 두 Claude Code 클라이언트가 동시에 git
직접 조작하므로, 충돌 방지를 위해 다음 규칙을 따른다. 상세 설계는
[wiki/concepts/multi-client-conflict-prevention.md](wiki/concepts/multi-client-conflict-prevention.md).

1. **세션 시작 시 / GitHub 동기화(push/pull) 전, 반드시
   `wiki/messagebox.md`를 가장 먼저 읽는다.** 활성 🔴 HALT 메시지가
   있으면 해당 작업이 끝날 때까지 sync를 대기한다. 🟡 CAUTION이면
   pull 먼저. 🟦 INFO는 읽고 진행.
2. **큰 변화를 줄 때 메세지박스에 게시한다** — 기준선 재정렬, 브랜치
   구조 변경, 대량 코드 리팩터, 위키 스키마 변경 등. "누가/언제 무슨
   변화/모바일이 뭘 먼저 읽어야 하는지"를 서술하고 만료 시각을 표기.
   작은 ingest/log 한 줄은 게시할 필요 없다.
3. **메세지박스는 현재 유효한 공지만** — 내용이 상대에게 전달되면
   작성자가 다음 메시지로 교체. log.md처럼 무한히 쌓지 않는다.
4. **매 세션 시작 시 `git fetch && git pull --rebase`** — 동시 편집
   시간창을 최소화. 작은 작업은 끝나자마자 즉시 push.
5. **`log.md`는 맨 아래에만 append** (이미 5번 규칙) — 같은 줄만
   아니면 git이 다른 줄의 append를 자동 병합하므로 사실상 충돌 안 남.
6. **큰 작업은 별도 branch에서** — 공유 서사 브랜치에서 코드 대량
   변경하면 모바일 위키 작업과 rebase 지옥이 생기니 격리 후 PR merge.
7. **절대 `git push -f`(force) 금지** — 상대 작업이 통째로 날아간다.

### 브랜치 전략 (Branch Strategy)

- **`main`**: GitHub Actions 자동 수집 + 리포트 생성. 사람/에이전트
  직접 커밋 금지. **default branch로 유지** (워크플로우가 main에서
  돌고 main에 push하도록 짜여 있으므로 변경 금지).
- **`claude/ai-agent-impl-002tip`**: 위키/엔티티/컨셉 정리 및 서사.
  mobile·desktop 모두 여기서 작업.
- **세션 시작 시 반드시 서사 브랜치로 checkout**:
  `git fetch origin && git checkout claude/ai-agent-impl-002tip`.
  default가 main이라 clone/pull 시 main을 받으므로, 모바일은 매
  세션 시작 시 명시적으로 서사 브랜치로 전환해야 이번 작업
  (messagebox·운영 섹션·concept)을 볼 수 있다. [messagebox](wiki/messagebox.md) 참조.
- 두 브랜치가 갈라져 있을 경우, 데이터 참조 시 반드시 브랜치 확인.
- wiki/log.md의 마지막 항목을 기준으로 브랜치 동기화 필요.

### 시크릿 관리 (Secrets)

- 시크릿 값은 GitHub Secrets에만 저장, 코드/위키/채팅에 노출 금지.
- GitHub 인증 토큰(PAT)은 Git 자격 증명 관리자에 보관 — 코드에
  절대 평문 기재 금지. 토큰 추출/설정 절차는
  [wiki/concepts/claude-code-internal-routing.md](wiki/concepts/claude-code-internal-routing.md).

### 커밋 원칙 (Commit)

- 사용자 명시적 승인 전까지 커밋하지 않음.
- 파일 추가 시 `git add -A` 대신 개별 파일 명시적 추가.
- pre-commit hook 실패 시 새 커밋 생성 (amend 금지).
- 커밋 메시지 끝에 `Co-Authored-By: Claude <noreply@anthropic.com>`.

### 코드 작성 품질 (Code Quality Protocol)

- **🔴 최상위 상위 규칙 — 동시 실행 중인 다른 Agent를 고려하라 (가장 먼저 적용)**:
  코드가 **동시에 실행 중일 수 있는 다른 프로세스를 죽이거나 방해하지
  않도록** 작성한다. 특히 headless 자동화 스크립트(`claude -p` 래퍼,
  스케줄러, bat/ps1 루틴)에서 `taskkill`/`Stop-Process`/`Get-CimInstance
  Win32_Process`로 프로세스를 정리(sweep)할 때, 매칭 조건이 **좁아야**
  한다 — generic keyword(`'claude'`, `'node'`) 부분 문자열 매칭만으로는
  **사용자의 live interactive Claude Code 세션과 다른 Agent의 진행 중
  작업까지 `taskkill /F`로 통째로 강제 종료**한다 (2026-08-07 실제 사건:
  래퍼 타임아웃 sweep이 interactive 창을 죽임 → 대화 컨텍스트 상실,
  되돌릴 불가). 안전장치: (1) spawn한 PID 직접 추적, (2) CreationDate
  시간 창(내 job 시작 이후만 타겟 — interactive 세션은 그 전부터 존재해
  자동 제외), (3) headless 고유 시그니처로 좁히기. **sweep이 위험하면
  sweep 자체를 빼고 `Stop-Job`만 남겨라** — 고아 자식 프로세스가 남는
  것이 다른 Agent 작업을 죽이는 것보다 안전하다. 좁은 타임아웃(예: 90초)
  으로 무거운 headless 작업을 테스트하지 마라 (타임아웃 분기 발동 →
  sweep 위험). git 동시 편집 충돌([multi-client-conflict-prevention](wiki/concepts/multi-client-conflict-prevention.md))과는
  **다른 프로세스 레이어** 규칙. 상세·체크리스트는
  [wiki/concepts/concurrent-agent-aware-coding.md](wiki/concepts/concurrent-agent-aware-coding.md).
  API 오류(아래 cross-check)보다 **먼저** 적용 — 치명도가 더 높다.
- **코드 작성 전 반드시 cross-check 수행**: 외부 라이브러리 API, 파라미터명, 설정파일 키 이름 등은 **실제 documentation/소스 코드를 먼저 읽고** 작성 — 기억이나 추측으로 코드 생성 금지.
- **Double/triple check 원칙**:
  1. 첫 번째: `Glob`/`Grep`으로 관련 파일 구조 확인
  2. 두 번째: `Read`로 API/파라미터명/유사 패턴 확인
  3. 세 번째: `WebFetch`로 외부 문서 (예: GitHub Actions action param, npm package API 등) 검증
  4. 검증 완료 전까지 코드 작성 시작 금지
- **Cross-check subfunction 패턴**: 검증이 필요한 작업은 반드시 별도 단계로 분리. 예:
  ```
  Step A: WebFetch("https://github.com/owner/action/docs", "What are all valid 'with' parameters?")
  Step B: Grep("**/*.yml", parameter_name)로 프로젝트 내 사용 패턴 확인
  Step C: 검증 완료 후 코드 작성
  ```
  검증 단계 없이 바로 코드 생성하는 것은 절대 금지.
- **에러 발생 시**: "틀릴 수 있다"는 가정으로 접근. "이렇게 하면 된다"가 아닌 "문서에 이렇게 나온다"로 결론 서술.

### 중간 단계 작업 — 진단형 테스트 스크립트 (Intermediate Task Protocol)

상호 사용자가 "어떻게 하면 될까?", "어떤 문제가 있는지 확인해줘", "이걸 해보려고 하는데" 같은 **중간 단계의 질문**을 했을 때, 부분적인 스크립트나 단계별 테스트 → 실패 → 수정 → 재시도 사이클은 절대 금지.

- **모든 케이스를 cover하는 정교한 diagnostic 스크립트**를 한 번에 작성해서 제공해야 함. 실패하면 그 원인을 설명하고 **수정된 전체 스크립트**를 재제공.
- 스크립트는 다음을 포함해야 함:
  1. **환경 진단** — OS, Python 버전, PATH, 접근 가능한 툴 목록
  2. **파일/리소스 존재 확인** — 모든 대상 파일, 키, API endpoint 검증
  3. **네트워크/연결성 테스트** — SSL 모드별 폴백, timeout 설정
  4. **에러별 분기 처리** — 401/403/409/422/429 등 HTTP status code별 자동 대응
  5. **대체 경로 폴백** — 주요 경로 실패 시 자동 fallback (예: credential manager → clipboard → pat.txt → 수동 입력)
  6. **최종 요약 리포트** — 성공/실패, 원인이면 원인명, 다음 액션 제안
- **최종 결론이 나야 종료**: 성공했거나 원인이 명확히 특정되어야 종료. "어쩌면 될지도 모른다"로 끝내면 안 됨.

### 시간대 (Timezone)

- 모든 시간 기준: KST(UTC+9). 금융 데이터 기준일은 거래일 기준.
- 비대칭 휴장 구간 주의: 한국 휴장 중 미국 장시간 운영.
