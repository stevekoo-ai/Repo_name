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
## Memory Hierarchy

Steve's Wiki maintains multiple memory layers.

Each layer serves a different purpose.

MessageBox
    ↓
log.md
    ↓
log-archive/
    ↓
Concepts
    ↓
Entities

---

### MessageBox

Active coordination memory.

Contains:

- warnings
- active notices
- coordination signals

Time horizon:

Hours to days.

---

### log.md

Working operational memory.

Contains:

- ongoing investigations
- implementation history
- system changes
- deployment records
- troubleshooting narratives
- recent discoveries

Time horizon:

Days to weeks.

log.md is not merely a log.

It is the current operational narrative of the system.

---

### log-archive/

Long-term operational memory.

Contains:

- historical incidents
- engineering decisions
- troubleshooting history
- operational evolution
- institution-level memory

Time horizon:

Months to years.

Archived logs remain part of the system's memory and should not be treated as obsolete information.

Before rediscovering a problem, agents should search historical operational memory.

---

### Concepts

Reusable intelligence.

Operational memory answers:

"What happened?"

Concepts answer:

"What did we learn?"

---

### Entities

Current state memory.

Entities answer:

"What do we currently know?"

---

## Logging

Logs are operational memory.

Archive rather than delete.

---

## Secrets

Secrets belong only in approved secret stores.

Never place credentials in wiki content.

---

