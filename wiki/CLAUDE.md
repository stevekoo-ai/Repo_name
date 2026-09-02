# LLM Wiki — 운영 지침

> **최우선 원칙**: 모든 코드는 기존에 성공한 이력이 있는지 먼저 확인하고, 성공된 것을 재사용하는 것을 원칙으로 한다.
> **2026-08-11 최우선 정책**: GitHub download(GET) → 로컬 HTML 보고서 생성까지만 허용. GitHub push → email 전달은 금지. 상세는 [CLAUDE.md](../CLAUDE.md) 최상단 정책 블록 참조.

This repo implements the "LLM Wiki" pattern (See
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of
re-deriving answers from raw sources on every query, an LLM incrementally
builds and maintains a persistent, interlinked markdown wiki that synthesizes
what's in the sources. You (the human) curates sources and ask questions; the
LLM does the bookkeeping.

---

## 1. Layers

1. `sources/` — raw, immutable inputs (articles, notes, transcripts, papers,
   whatever). Never edit or delete files here as part of a wiki workflow. Add
   new sources as new files. CSV 자동 수집 파일도 여기 포함.
2. `wiki/` — the LLM-maintained knowledge base. Everything here can be
   regenerated from `sources/` in principle, but treat it as durable: it
   embodies synthesis work that's expensive to redo.
3. This file — the schema. It defines structure, conventions, and workflows.
   Update it yourself when the wiki's shape needs to change; the agent
   should not restructure the schema unprompted.

---

## 2. Wiki structure

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

---

## 3. Page conventions

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

---

## 4. index.md conventions

One line per wiki page, grouped by folder:
```
### entities

- [Some Entity](entities/some-entity.md) — one-line summary

### concepts

- [Some Concept](concepts/some-concept.md) — one-line summary
```

---

## 5. log.md conventions

Append-only, newest entry at the bottom. One line per event:
```
YYYY-MM-DD HH:MM UTC — INGEST sources/foo.md → created entities/foo.md, updated concepts/bar.md
YYYY-MM-DD HH:MM UTC — QUERY "question text" → cited entities/foo.md, concepts/bar.md
YYYY-MM-DD HH:MM UTC — LINT → 2 issues found (see report)
```

---

## 6. Workflows

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

### Query (`/query <question>`)

1. Read `wiki/index.md` and grep `wiki/` for pages relevant to the question.
2. Answer the question, citing which wiki page(s) support each claim.
3. If the answer surfaces something worth keeping that isn't already in the
   wiki, propose filing it back in — don't write it in without saying so.
4. Append one line to `wiki/log.md`.

### Lint (`/lint`)

1. Walk every page under `wiki/`.
2. Flag: contradictions between pages, claims no longer supported by any
   source, orphaned pages (not reachable from `index.md`), missing
   cross-references (two pages clearly about the same thing that don't link
   to each other), and broken links.
3. Report findings as a list; don't auto-fix without confirmation.
4. Append one line to `wiki/log.md` summarizing the count of issues found.

---

## 7. 대화 운영 원칙 (Conversation Operating Principles)

### 7-1. 법칙 우선순위
1. **사용자의 직접적 지시**가 최우선 (GitHub 커밋 금지, 읽기 전용 모드 등)
2. **CLAUDE.md**가 두 번째 (위키 스키마, 워크플로 정의)
3. **`.github/commands/*.md`** 커스텀 명령 (ingest, query, lint)
4. **기존 코드/설정**이 세 번째 (daily_report.py, 워크플로우 YAML)
5. LLM의 일반적 판단은 가장 낮은 우선순위

### 7-2. 데이터 출처 우선순위
- **KIS API 자동 수집 CSV** > 사용자 제공 스크린샷/데이터 > 웹검색 결과
- CSV의 `fetched_at` 타임스탬프 기준으로 가장 최근 데이터를 사용
- 같은 날짜에 중복 데이터가 있을 경우, `fetched_at` 기준 최신 행 선택 (github-data-pipeline-cautions.md 2-2 참조)

### 7-3. 브랜치 분리 원칙
- GitHub Actions 워크플로는 **main 브랜치**에서만 실행
- 위키/리포트 서사는 **claude/ai-agent-impl-002tip 브랜치**에서 관리
- 두 브랜치가 갈라져 있을 경우, 데이터 참조 시 반드시 브랜치 확인 필요
- (github-data-pipeline-cautions.md 1-1 참조)

### 7-4. 보고서 버저닝
- HTML 리포트는 **overwrite하면 안 됨**
- 파일명에 **날짜와 시간**을 포함: `sk-hynix-web-report-YYYY-MM-DD-HHMM.html`
- 새 데이터가 들어오면 **새 파일**로 생성, 기존 파일 보존
- 버전 태그: `<span class="version-tag">vN (데이터 기준일)</span>`

### 7-5. 데이터 정확성
- **실측 우선 원칙**: 차트 스크린샷 > 웹 검색 요약 > 추정치
- KSD 보유율(결제 기준)은 KRX 매매동향(체결 기준)과 **T+2 시차** 존재
- "체결↔결제 시차" 가설이 의심될 때는 보류 후 다음 영업일 확인

### 7-6. 작업 실행 프로토콜 (Task Execution Protocol)
1. **모든 작업 전에 계획을 먼저 세운다** — 어떤 작업을 시작하기 전에
   수행할 단계를 먼저 정리한다. 계획 없이 즉시 실행하지 않는다.
2. **현재 어떤 작업을 하고 있는지 표시한다** — 진행 중에 항상
   지금 수행 중인 단계가 무엇인지 명시한다 (todo/진행 상태 표시).
3. **각 계획이 완료되면 완료 메시지를 보낸다** — 단위 작업이 끝날
   때마다 완료 사실을 명시적으로 알린다. 한꺼번에 몰아서 보고하지 않는다.

---

## 8. 데이터 파이프라인 & 자동화 (Data Pipeline & Automation)

### 8-1. GitHub Actions 스케줄
- **07:00, 10:00, 19:00 KST** — SK하이닉스 일간 리포트 수집
- **19:10 KST** — 포트폴리오 보유 현황 동기화
- **매일 01:06 KST** — 간헐적 추가 수집 (자동 보고서용)

### 8-2. CSV 데이터 파일
| 파일 | 설명 | 업데이트 주기 |
|---|---|---|
| `sk-hynix-price-snapshot.csv` | 종가, 외국인 보유율, 250일 고가 대비 | 일일 |
| `sk-hynix-investor-flow.csv` | 투자자별 순매수 (외국인/기관/개인) | 일일 |
| `sk-hynix-adr-quote.csv` | ADR 가격, 등락 | 일일 |

### 8-3. KIS API 충돌 방지
- 기존 워크플로 간 스케줄 충돌 시 **토큰 재발급 403 오류** 발생
- 새 워크플로 작성 시 `kis_get_token()` 함수 공유 캐시 재사용
- 시크릿은 GitHub Secrets에서만 접근, 코드에 절대 노출 금지

---

## 9. GitHub 운영 규칙 (GitHub Operations)

### 9-1. 커밋 원칙
- **사용자 명시적 승인 전까지 커밋하지 않음**
- 커밋 시에는 `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>` 포함
- 파일 추가 시 `git add -A` 대신 **개별 파일 명시적 추가**
- pre-commit hook 실패 시 **새 커밋 생성** (amend 금지)

### 9-2. 시크릿 관리
- **시크릿 값은 GitHub Secrets에만 저장**, 코드/위키에 노출 금지
- 시크릿 이름만 `.claude/commands/ingest.md`나 설정 파일에 기록
- GMAIL_ADDRESS, GMAIL_APP_PASSWORD, KIS_* 시크릿은 기존 워크플로가 이미 등록 완료

### 9-3. 브랜치 전략
- **main**: GitHub Actions 자동 수집 + 리포트 생성
- **claude/ai-agent-impl-002tip**: 위키/엔티티/컨셉 정리 및 서사
- wiki/log.md의 마지막 항목을 기준으로 브랜치 동기화 필요

---

## 10. 시간대 & 스케줄

- **모든 시간 기준: KST (UTC+9)**
- 금융 데이터 기준일은 **거래일 기준** (한국 시간 기준 당일 종가)
- 미국 장정과의 시간 차이: NYSE/Nasdaq 09:30~16:00 (한국 22:30~05:00 다음날)
- **비대칭 휴장 구간**: 한국 휴장 중 미국 장시간 운영 → 7/17(제헌절) 누락 사건 주의

---

## 11. 용어 정의

| 용어 | 정의 |
|---|---|
| **체결 기준** | KRX 매매동향의 당일 거래 데이터 (외국인 순매도 -13.06조 원 등) |
| **결제 기준** | KSD 보유율 = 체결 후 T+2 결제 시점의 실제 보유량 |
| **ADR 프리미엄** | `(ADR - (주가/10/환율)) / (주가/10/환율)` |
| **HBM Cycle Score** | 6축 종합점수(0~100) + 4개 붕괴조건. 80점+=강세, 60~80=경계, 60점 미만=사이클 꺾임 |
| **LTA** | Long-Term Agreement, 가격 상한선 없는 장기 공급 계약 |

---

> **이 파일은 LLM Wiki의 운영 지칙입니다. 새로운 운영 규칙이 필요하면 언제든지 직접 수정하세요.**
<!-- cloude-code-toolbox:mcp-skills-awareness-begin -->

### MCP & Skills awareness (Cloude Code ToolBox)

_Last synced: 2026-08-24T08:25:30.643Z._

- **Full report:** `.claude/cloude-code-toolbox-mcp-skills-awareness.md` in this workspace (auto-overwritten on each scan). Use it as ground truth for configured servers and skill folders.
- **MCP:** For **live tools** in Claude Code, enable the matching server via `/mcp`. Servers are configured in `~/.claude.json` (user) and `.mcp.json` (project).
- **When the user’s task matches a server** (e.g. Confluence work and a **Confluence** / **Atlassian** MCP is listed), **prefer that server id** and plan on tool use—not only file search.
- **Skills:** Folders below contain `SKILL.md`; attach or cite paths in chat when relevant.

#### Workspace MCP

- `c:\Users\2053437\wiki\.mcp.json` _(workspace: wiki)_ — _file missing_

_No active workspace servers in mcp.json._

#### User MCP

- `C:\Users\2053437\.claude.json` — _no servers defined_

_No active user-scoped servers in mcp.json._

#### Project skills

_None found (or no workspace open)._

#### User skills

_None found._

<!-- cloude-code-toolbox:mcp-skills-awareness-end -->
