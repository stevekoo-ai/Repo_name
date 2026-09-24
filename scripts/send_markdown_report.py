#!/usr/bin/env python3
"""마크다운 보고서를 HTML로 바꿔 메일로 보낸다 — 텍스트로 나가던 보고서들의 공용 발송기.

2026-09-24 사용자: "SK하이닉스 자동 리포트가 내 gmail로 전달이 안되고 있는데?!
모든 보고서들이 정확히 html로 변환되어 제시간에 gmail로 발송되고 있는지 확인하라."

조사 결과 SK하이닉스 리포트만 dawidd6/action-send-mail로 **보낸사람 주소 없이**
("SK하이닉스 자동 리포트 봇") 마크다운 원문을 보내고 있었다. Gmail은 헤더가 부실한
자기→자기 메일을 250 OK로 받아놓고 조용히 버린다는 게 이미 확인된 사실이다
(core/notify.py 주석). 그래서 발송은 From·Date·Message-ID를 제대로 붙이는
core.notify로 통일하고, HTML은 브리핑에서 검증된 render_briefing_html을 재사용한다.

    python -m scripts.send_markdown_report --file /tmp/report.md --subject "[SK하이닉스 자동 리포트] ..."

설정된 채널로 발송이 실패하면 0이 아닌 코드로 끝난다 — 워크플로의 실패 알림이
그걸 보고 뜬다(조용한 실패 방지).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from core import notify  # noqa: E402
from engine.briefing.render_html import render_briefing_html  # noqa: E402


def build_html(md: str, subject: str) -> str:
    return render_briefing_html(md, title=subject)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="보낼 마크다운 파일")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--save-html", default=None, help="렌더링한 HTML을 이 경로에도 저장")
    ap.add_argument("--allow-unconfigured", action="store_true",
                    help="채널 미설정이면 성공으로 간주(로컬 점검용)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        print(f"[error] 보낼 보고서가 없거나 비어 있음: {path}", file=sys.stderr)
        return 1
    html = build_html(path.read_text(encoding="utf-8"), args.subject)
    if args.save_html:
        Path(args.save_html).write_text(html, encoding="utf-8")

    if not notify.is_configured():
        msg = "메일 채널 미설정(GMAIL_ADDRESS/GMAIL_APP_PASSWORD 없음)"
        if args.allow_unconfigured:
            print(f"[skip] {msg}")
            return 0
        print(f"[error] {msg}", file=sys.stderr)
        return 1
    try:
        notify.build_channel().send_document(args.subject, html, attachments=[])
    except Exception as exc:  # noqa: BLE001 — 발송 실패는 반드시 드러낸다
        print(f"[error] 발송 실패: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"[ok] HTML 발송 완료 — {args.subject} ({len(html):,}자)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
