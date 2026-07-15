---
description: Ingest a source into the wiki, following the schema in CLAUDE.md
---

Follow the **Ingest** workflow defined in `CLAUDE.md` exactly, for this source:

$ARGUMENTS

If that looks like a path under `sources/`, read it. If it doesn't match an
existing file, treat the whole argument as inline source text: save it to a
new file under `sources/` with a sensible filename first, then proceed.

When done, report which wiki pages were created vs. updated, and confirm
`wiki/index.md` and `wiki/log.md` were updated.
