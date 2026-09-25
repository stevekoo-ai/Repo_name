#!/usr/bin/env python3
"""브리핑 나침반 갱신 CLI — 루틴은 보고서를 쓴 뒤 이것으로만 나침반을 고친다.

    python3 scripts/compass.py show
    python3 scripts/compass.py conclude --slot AM --text "오늘 결론 한 줄"
    python3 scripts/compass.py update --id T1 --status "새 판단 한 줄" [--next-check "10/15"]
    python3 scripts/compass.py add --id T7 --question ... --why ... --status ... --next-check ...
    python3 scripts/compass.py prune --id T3 --reason "왜 더 볼 가치가 없나"

상한(스레드 6개·필드 120자 등)을 넘으면 저장을 거부한다 — 먼저 prune하라.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.briefing import compass as C  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show")
    p = sub.add_parser("conclude"); p.add_argument("--slot", required=True); p.add_argument("--text", required=True)
    p = sub.add_parser("update"); p.add_argument("--id", required=True); p.add_argument("--status", required=True)
    p.add_argument("--next-check")
    p = sub.add_parser("add")
    for k in ("--id", "--question", "--why", "--status", "--next-check"):
        p.add_argument(k, required=True)
    p = sub.add_parser("prune"); p.add_argument("--id", required=True); p.add_argument("--reason", required=True)
    a = ap.parse_args()

    day = datetime.now(timezone(timedelta(hours=9))).date().isoformat()
    c = C.load()
    try:
        if a.cmd == "show":
            print(C.render(c)); return 0
        if a.cmd == "conclude":
            C.conclude(c, a.slot, a.text, day)
        elif a.cmd == "update":
            C.update(c, a.id, a.status, a.next_check, day)
        elif a.cmd == "add":
            C.add(c, a.id, a.question, a.why, a.status, a.next_check, day)
        elif a.cmd == "prune":
            C.prune(c, a.id, a.reason, day)
        C.save(c)
    except C.CompassError as e:
        print(f"[거부] {e}", file=sys.stderr)
        return 1
    print(f"[ok] 나침반 {a.cmd} 저장 ({len(C.render(c))}자)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
