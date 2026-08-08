# Operating System

## Synchronization

- Read MessageBox first
- Pull before write
- Prefer append over overwrite
- Assume concurrent agents exist

---

## Communication

MessageBox contains active coordination signals.

Categories:

- HALT
- CAUTION
- INFO

---

## Source Control

- Pull before write
- No force push
- Preserve auditability

---

## Runtime Safety

Never disrupt:

- active agents
- active reports
- active workflows

Safety takes priority over cleanup.

---

## Logging

Logs are operational memory.

Archive rather than delete.

---

## Secrets

Secrets belong only in approved secret stores.

Never place credentials in wiki content.
