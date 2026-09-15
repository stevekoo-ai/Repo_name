"""데이터 헬스 close-loop CLI — GitHub Actions와 로컬 양쪽에서 쓴다.

    python -m scripts.data_health_check                # 판정 + 제어(알림 포함)
    python -m scripts.data_health_check --no-alerts     # 판정만, 알림 생략(로컬 점검용)
    python -m scripts.data_health_check --check-only    # 상태 저장 없이 화면 출력만(디버깅용)

종료 코드: critical 소스가 하나라도 OK가 아니면 1 — GitHub Actions 스텝을
빨갛게 표시해 "이 저장소를 열어보게" 만든다(경고만 하고 아무도 안 여는
시스템은 없는 것과 같다).
"""
from __future__ import annotations

import argparse
import sys

from engine.health import control
from engine.health.check import check_all


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-alerts", action="store_true", help="알림 발송 생략")
    ap.add_argument("--check-only", action="store_true",
                    help="판정 결과만 출력하고 상태 파일·알림 건너뜀")
    args = ap.parse_args()

    if args.check_only:
        report = check_all()
        for s in report.statuses:
            if s.state == "OK":
                mark = "✅"
            elif s.state == "MISSING":
                mark = "⚪"
            else:
                mark = "🔴" if s.severity == "critical" else "🟠"
            print(f"{mark} {s.slug:32s} [{s.state:8s}/{s.severity:8s}] {s.detail}")
        print(f"\n{len(report.bad)}/{len(report.statuses)}개 이상")
        return 1 if report.critical_bad else 0

    result = control.run(send_alerts=not args.no_alerts)
    for f in result["fired"]:
        print(f"[fired] {f}")
    print(f"상태 저장: {control.STATE_PATH}")
    print(f"스냅샷: {control.REPORT_MD_PATH}")
    return 1 if result["report"].critical_bad else 0


if __name__ == "__main__":
    sys.exit(main())
