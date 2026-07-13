---
description: Health-check the wiki for drift, per CLAUDE.md
---

Follow the **Lint** workflow defined in `CLAUDE.md` exactly. Scope: $ARGUMENTS
(if empty, lint the entire `wiki/`).

Report findings as a list grouped by type (contradiction / stale claim /
orphaned page / missing cross-reference / broken link). Do not fix anything
automatically — wait for confirmation. Append one summary line to
`wiki/log.md`.
