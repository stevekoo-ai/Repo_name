"""PEOS data collectors: Official First (Master Instruction 7.1).

Each collector module fetches one official source, writes an immutable
Level-1 raw snapshot (7.5), and returns a normalized (date, value) series
for the indicator layer. On failure, collectors retry, then fall back to
cache, then report DataStatus.PENDING/SOURCE_ERROR rather than guessing
(7.9, 19.2) — they never silently reuse a stale prior value as if it were
current.
"""
