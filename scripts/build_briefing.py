#!/usr/bin/env python3
"""브리핑 팩 생성 CLI — Routine이 이걸 실행하고 결과 파일만 읽는다.

    python3 scripts/build_briefing.py --slot AM
    python3 scripts/build_briefing.py --slot PM --as-of 2026-09-11

출력: data/briefing/pack_<slot>.md  (매번 덮어씀 — 팩은 그 시점의 스냅샷이고
이력은 report/briefing/에 남는 발행물이 담당한다)

종료 코드로 게이트 결과를 알린다:
  0 = 발행할 것이 있다
  10 = 정규 브리핑을 쓰지 않는 날(조용한 날·한국 휴장). 이때 코드가
       report/briefing/<날짜>-<SLOT>.md에 '상황 보고'를 이미 써 둔다 —
       Routine은 새로 쓰지 않고 그 파일을 발행(커밋·push)만 한다.
       (2026-09-24, 조용한 미발행 금지 — wiki/concepts/report-delivery-policy.md)
"""
import argparse
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.briefing.context import build_pack  # noqa: E402

QUIET_EXIT = 10


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slot", choices=("AM", "PM", "WEEKEND"), required=True)
    ap.add_argument("--as-of", help="YYYY-MM-DD (기본: 오늘 KST)")
    ap.add_argument("--out", help="출력 경로 (기본: data/briefing/pack_<slot>.md)")
    args = ap.parse_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    pack, gate = build_pack(args.slot, as_of)

    out = Path(args.out) if args.out else (
        Path(__file__).resolve().parents[1] / "data" / "briefing" / f"pack_{args.slot}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(pack.render(), encoding="utf-8")

    print(f"팩: {out} ({pack.chars:,}자, 약 {pack.chars // 1.5:,.0f}토큰)")
    for b in pack.blocks:
        print(f"  {b.title} — {b.chars:,}자")
    print(f"게이트: {gate.verdict}")
    for r in gate.reasons:
        print(f"  · {r}")

    # 2026-09-24 — 조용한 날·휴장일에도 "아무것도 안 보내고 끝"은 금지다
    # (wiki/concepts/report-delivery-policy.md). 정규 브리핑 대신 코드가
    # 상황 보고를 써 둔다. 종료코드 10은 그대로 — Routine은 새로 쓰지 않고
    # 이 파일을 발행(HTML 변환·커밋·push)만 한다.
    from engine.briefing import notice as N
    day = as_of or datetime.now(timezone(timedelta(hours=9))).date()
    reason = N.skip_reason(args.slot, day, gate)
    if reason:
        path = N.write_notice(args.slot, day, reason)
        print(f"상황 보고 작성: {path}")
        print(f"  사유: {reason}")
        return QUIET_EXIT
    return 0


if __name__ == "__main__":
    sys.exit(main())
