# Repo_name

An implementation of Andrej Karpathy's ["LLM Wiki" pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
instead of re-deriving answers from raw sources on every query, an LLM
incrementally builds and maintains a persistent, interlinked markdown wiki.
You curate sources and ask questions; the agent does the bookkeeping.

## Layout

- `sources/` — raw, immutable inputs you add (articles, notes, transcripts...)
- `wiki/` — the LLM-maintained knowledge base (summaries, entities, concepts,
  plus `index.md` and `log.md`)
- `CLAUDE.md` — the schema: structure, conventions, and the three workflows
  below

## Usage (with Claude Code)

- `/ingest <path under sources/ or pasted text>` — fold a new source into the
  wiki, updating existing pages where they overlap and creating new ones only
  when nothing fits
- `/query <question>` — answer from the wiki, citing which page(s) support
  each claim
- `/lint` — health-check the wiki for contradictions, stale claims, orphaned
  pages, and missing cross-references

See `CLAUDE.md` for the full schema these commands follow.
