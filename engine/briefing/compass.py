"""브리핑 나침반 — 새 세션에서도 이어지는 압축 누적 맥락 (wiki/concepts/briefing-compass.md).

상한은 여기서 강제한다. 넘으면 저장을 거부해 루틴이 곁가지를 쳐내게 만든다.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
COMPASS = REPO / "data" / "briefing" / "compass.yaml"

MAX_THREADS = 6
MAX_PRUNED = 10
MAX_RECENT = 3
MAX_FIELD = 120        # 스레드 필드 하나
MAX_LINE = 140         # pruned / recent 한 줄
MAX_RENDER = 2400      # 팩에 실리는 전체 글자


class CompassError(ValueError):
    pass


def load(path: Path | None = None) -> dict:
    return yaml.safe_load((path or COMPASS).read_text(encoding="utf-8")) or {}


def validate(c: dict) -> None:
    th = c.get("threads") or []
    if len(th) > MAX_THREADS:
        raise CompassError(f"스레드 {len(th)}개 — 상한 {MAX_THREADS}. 가치가 낮은 것을 prune하라")
    ids = [t["id"] for t in th]
    if len(ids) != len(set(ids)):
        raise CompassError("스레드 id 중복")
    for t in th:
        for k in ("question", "why", "status", "next_check"):
            if len(str(t.get(k, ""))) > MAX_FIELD:
                raise CompassError(f"{t['id']}.{k} {len(str(t[k]))}자 — 상한 {MAX_FIELD}. 더 압축하라")
    for key, cap in (("pruned", MAX_PRUNED), ("recent_conclusions", MAX_RECENT)):
        items = c.get(key) or []
        if len(items) > cap:
            raise CompassError(f"{key} {len(items)}개 — 상한 {cap}")
        for s in items:
            if len(s) > MAX_LINE:
                raise CompassError(f"{key} 한 줄 {len(s)}자 — 상한 {MAX_LINE}")
    if len(render(c)) > MAX_RENDER:
        raise CompassError(f"렌더 {len(render(c))}자 — 상한 {MAX_RENDER}")


def save(c: dict, path: Path | None = None) -> None:
    validate(c)
    (path or COMPASS).write_text(
        yaml.safe_dump(c, allow_unicode=True, sort_keys=False, width=100), encoding="utf-8")


def render(c: dict) -> str:
    lines = [f"**의도**: {str(c.get('mission', '')).strip()}", "", "**추적 중인 핵심 질문**"]
    for t in c.get("threads") or []:
        lines.append(f"- **{t['id']} {t['question']}** — {t['status']} "
                     f"(다음 확인: {t['next_check']}, 갱신 {t['updated']})")
    rec = c.get("recent_conclusions") or []
    if rec:
        lines += ["", "**최근 결론**"] + [f"- {r}" for r in rec]
    pr = c.get("pruned") or []
    if pr:
        lines += ["", "**쳐낸 곁가지 — 다시 끌어들이지 말 것**"] + [f"- {p}" for p in pr[-5:]]
    return "\n".join(lines)


# ── 루틴이 부르는 갱신 연산 ─────────────────────────────────────

def update(c: dict, tid: str, status: str, next_check: str | None, day: str) -> None:
    t = next((t for t in c["threads"] if t["id"] == tid), None)
    if t is None:
        raise CompassError(f"없는 스레드: {tid}")
    t["status"] = status
    if next_check:
        t["next_check"] = next_check
    t["updated"] = day


def add(c: dict, tid: str, question: str, why: str, status: str, next_check: str, day: str) -> None:
    c.setdefault("threads", []).append({"id": tid, "question": question, "why": why,
                                        "status": status, "next_check": next_check, "updated": day})


def prune(c: dict, tid: str, reason: str, day: str) -> None:
    t = next((t for t in c["threads"] if t["id"] == tid), None)
    if t is None:
        raise CompassError(f"없는 스레드: {tid}")
    c["threads"].remove(t)
    c.setdefault("pruned", []).append(f"{day} {t['question']} — {reason}"[:MAX_LINE])
    c["pruned"] = c["pruned"][-MAX_PRUNED:]


def conclude(c: dict, slot: str, text: str, day: str) -> None:
    c.setdefault("recent_conclusions", []).append(f"{day} {slot}: {text}"[:MAX_LINE])
    c["recent_conclusions"] = c["recent_conclusions"][-MAX_RECENT:]
