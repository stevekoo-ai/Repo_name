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
  log.md              chronological, append-only event log
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

### 시간대 (Timezone)

- 모든 시간 기준: KST(UTC+9). 금융 데이터 기준일은 거래일 기준.
- 비대칭 휴장 구간 주의: 한국 휴장 중 미국 장시간 운영.
