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
