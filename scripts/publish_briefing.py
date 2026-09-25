#!/usr/bin/env python3
"""브리핑 발행 — 마크다운을 HTML로 바꾸고 이메일로 보낸다.

    python3 scripts/publish_briefing.py --slot AM
    python3 scripts/publish_briefing.py --slot PM --date 2026-09-11 --no-email

## 토큰 비용 0

변환은 `engine/briefing/render_html.py`의 **순수 코드**다 — LLM을 부르지
않는다. Routine은 마크다운만 쓰고, 발행(HTML화·메일)은 이 스크립트가 맡는다.
LLM에게 HTML로 쓰게 하면 같은 내용에 출력 토큰을 두 번 내게 된다.

## 트랙 경계 (CLAUDE.md 최우선 정책)

브리핑은 **트랙 A**(거시·SK하이닉스 경제판단 리포트, 개인 자산 판단)라
email 발송이 명시적으로 허용된 범위다. 발송은 기존 `core/notify.py` 채널
(GitHub Secrets의 GMAIL_ADDRESS 등)만 쓰고, 2026-08-11에 제거된 회사망
우회 경로(dispatch/upload 계열)는 재사용하지 않는다.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import notify  # noqa: E402
from engine.briefing.render_html import render_briefing_html  # noqa: E402

BRIEF_DIR = Path(__file__).resolve().parents[1] / "report" / "briefing"

# 메일 첨부 상한. 브리핑은 보통 20KB 안쪽이라, 이 선을 넘으면 변환기
# 회귀를 의심하는 게 맞다(월간 리포트 쪽과 같은 방어).
MAX_HTML_BYTES = 2_000_000


def find_markdown(day: date, slot: str) -> Path | None:
    p = BRIEF_DIR / f"{day.isoformat()}-{slot}.md"
    return p if p.exists() else None


def _appendix(md: str, day: date) -> str:
    """코드가 판정한 체크포인트를 메일 끝에 원문 그대로 붙인다(토큰 0).

    2026-09-25 사용자: "어떤 보고서 경로로 내가 이 내용을 확인하게 되지?" —
    팩 블록은 브리핑 작성자가 본문에 옮겨야만 보였고, 신호가 꺼진 날은 생략될
    수 있었다. 부록은 작성자와 무관하게 항상 실린다. 상황 보고(notice)는 이미
    블록을 담고 있으므로 ⑩만 없을 때 붙인다."""
    from engine.briefing import context as X

    parts = []
    is_notice = "\nnotice: true" in md[:400]
    builders = [] if is_notice else [X.build_bottleneck_block]
    builders.append(X.build_midterm_block)
    for b in builders:
        try:
            blk = b(day)
            if is_notice and blk.title in md:
                continue
            parts.append(f"### {blk.title}\n\n{blk.body.strip()}\n")
        except Exception as exc:  # noqa: BLE001 — 부록 실패로 발송이 막히면 안 된다
            parts.append(f"### 부록 생성 실패\n\n({type(exc).__name__}: {exc})\n")
    if not parts:
        return ""
    return "\n\n---\n\n## 부록 — 자동 체크포인트 (코드 판정 원문)\n\n" + "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slot", choices=("AM", "PM", "WEEKEND"), required=True)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (기본: 오늘)")
    ap.add_argument("--no-email", action="store_true", help="HTML만 만들고 발송은 건너뜀")
    ap.add_argument("--allow-unconfigured", action="store_true",
                    help="알림 채널이 없어도 실패로 보지 않음(로컬 테스트용)")
    args = ap.parse_args()

    day = date.fromisoformat(args.date) if args.date else date.today()
    md_path = find_markdown(day, args.slot)
    if md_path is None:
        print(f"[error] {day} {args.slot} 브리핑 마크다운이 없습니다 ({BRIEF_DIR}/)",
              file=sys.stderr)
        return 1

    md = md_path.read_text(encoding="utf-8")
    html = render_briefing_html(md + _appendix(md, day))
    html_path = md_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    print(f"HTML: {html_path} ({len(html.encode()):,} bytes)")

    if len(html.encode()) > MAX_HTML_BYTES:
        print(f"[error] HTML이 상한({MAX_HTML_BYTES:,})을 넘습니다 — 변환기 회귀를 의심하십시오",
              file=sys.stderr)
        return 1

    if args.no_email:
        print("[skip] --no-email")
        return 0

    if not notify.is_configured():
        msg = ("알림 채널이 설정되지 않았습니다 "
               "(GMAIL_ADDRESS+GMAIL_APP_PASSWORD / SMTP_* / SLACK_WEBHOOK_URL 중 하나 필요)")
        if args.allow_unconfigured:
            print(f"[skip] {msg}")
            return 0
        print(f"[error] {msg}", file=sys.stderr)
        return 1

    label = {"AM": "아침", "PM": "저녁", "WEEKEND": "주간 전망"}[args.slot]
    subject = f"[PEOS {label} 브리핑] {day.isoformat()}"
    # 상황 보고(engine/briefing/notice.py)는 제목에서 바로 구분되게 — 정규
    # 브리핑이 없는 이유가 받은편지함 목록에서 보이도록.
    if "\nnotice: true" in md_path.read_text(encoding="utf-8")[:400]:
        subject = f"[PEOS 상황 보고] {day.isoformat()} {label} 브리핑 대체 — 정규 브리핑 미발행 사유 포함"
    try:
        notify.build_channel().send_document(subject, html, attachments=[html_path])
    except Exception as exc:  # noqa: BLE001 — 발송 실패는 조용히 넘기면 안 된다
        print(f"[error] 발송 실패: {exc}", file=sys.stderr)
        return 1
    print(f"발송 완료: {subject}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
