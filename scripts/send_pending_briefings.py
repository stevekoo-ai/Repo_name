#!/usr/bin/env python3
"""아직 발송하지 않은 브리핑(정규·상황 보고)을 전부, 한 번씩만 보낸다.

2026-09-24 발견한 두 가지 사고를 동시에 막는다:
  ① "가장 최근 파일 1개만" 보내던 구조 — 9/22 아침 브리핑이 9/23 아침과 한
     push로 올라오자 9/22분은 영영 발송되지 않았다.
  ② 같은 push에 워크플로가 두 번 떠서 9/23 저녁 브리핑이 2통 나갔다.

발송 장부: report/briefing/sent.log (한 줄에 "YYYY-MM-DD-SLOT"). 발송에 성공한
것만 기록하고, 호출자(briefing-email.yml)가 커밋한다. 동시 실행은 워크플로의
concurrency(대기열)로 직렬화되고, 각 실행은 최신 main을 받은 뒤 장부를 읽는다.

    python3 scripts/send_pending_briefings.py            # 최근 3일 미발송분 전부
    python3 scripts/send_pending_briefings.py --lookback-days 7
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BRIEF_DIR = REPO / "report" / "briefing"
SENT_LOG = BRIEF_DIR / "sent.log"
KST = timezone(timedelta(hours=9))
_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-(AM|PM|WEEKEND)\.md$")


def sent_keys() -> set[str]:
    if not SENT_LOG.exists():
        return set()
    return {ln.strip() for ln in SENT_LOG.read_text(encoding="utf-8").splitlines() if ln.strip()}


def pending(today: date, lookback_days: int) -> list[tuple[str, str, str]]:
    done = sent_keys()
    out = []
    for p in sorted(BRIEF_DIR.glob("*.md")):
        m = _NAME.match(p.name)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        key = briefing_key(p)
        if key in done or (today - d).days > lookback_days:
            continue
        out.append((m.group(1), m.group(2), key))
    return out


def briefing_key(path: Path) -> str:
    """상황 보고(frontmatter notice: true)는 ':notice'를 붙여 따로 기록한다 —
    워치독이 상황 보고를 보낸 뒤 루틴이 늦게 정규 브리핑을 올리면 그것도
    보내야 하기 때문이다(같은 키면 장부 때문에 조용히 누락된다)."""
    head = path.read_text(encoding="utf-8")[:400]
    return path.stem + (":notice" if "\nnotice: true" in head else "")


def mark_sent(key: str) -> None:
    with SENT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(key + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lookback-days", type=int, default=3)
    args = ap.parse_args()

    today = datetime.now(KST).date()
    todo = pending(today, args.lookback_days)
    if not todo:
        print("미발송 브리핑 없음")
        return 0
    failed = []
    for day, slot, key in todo:
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "publish_briefing.py"),
                            "--slot", slot, "--date", day], cwd=REPO)
        if r.returncode == 0:
            mark_sent(key)
            print(f"✓ 발송·기록: {key}")
        else:
            failed.append(f"{day}-{slot}")
    if failed:
        print(f"::error::발송 실패: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
