"""BLS(미국 노동·물가) + IMF WEO(전망) 정기 수집.

2026-09-07 신설. 두 소스 다 이날 만들어진 수집기(collectors/bls.py,
collectors/imf.py)를 돌려 data/normalized/에 쌓는 게 전부다 — 리포트
파이프라인(engine/report/payload.py)은 네트워크를 쓰지 않고 이 정규화
CSV만 읽으므로, 실제 API 호출은 여기서만 일어난다.

주기: 주 1회로 충분하다. BLS는 월간 지표(발표도 월 1회)이고 IMF WEO는
연 2회(4월·10월) 갱신이다. 매일 돌리면 BLS 키리스 한도(일 25회)를 태우고
IMF datamapper에도 불필요한 부하만 준다.

실패해도 종료코드 0 — 이 저장소의 원칙대로 수집 실패가 파이프라인을
멈추지 않는다. 대신 무엇이 실패했는지 표준출력에 남겨 워크플로 로그에서
보이게 한다(조용한 실패 방지 — 2026-09-07에 부동산 수집이 한 달간
"success"를 찍으며 죽어 있었던 사고의 교훈).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    ok_count = fail_count = 0

    print("=== BLS (미국 고용·물가) ===", flush=True)
    try:
        from collectors import bls
        results = bls.fetch_all()   # 8개 시리즈를 한 번의 호출로 — 키리스 한도 절약
        for key, dp in sorted(results.items()):
            status = getattr(dp, "status", "?")
            value = getattr(dp, "value", None)
            if value is None:
                fail_count += 1
                print(f"  ✗ {key}: {status} — {getattr(dp, 'note', '')}")
            else:
                ok_count += 1
                ref = getattr(getattr(dp, "metadata", None), "reference_date", "?")
                print(f"  ✓ {key}: {value} ({ref})")
    except Exception as exc:
        fail_count += 1
        print(f"  ✗ BLS 전체 실패: {type(exc).__name__}: {exc}")

    print("\n=== IMF WEO (전망 포함) ===", flush=True)
    try:
        from collectors import imf
        for country in imf.COUNTRIES:
            for series_key in imf.IMF_SERIES:
                try:
                    dp = imf.fetch_series(series_key, country)
                except Exception as exc:
                    fail_count += 1
                    print(f"  ✗ {series_key}/{country}: {type(exc).__name__}: {exc}")
                    continue
                value = getattr(dp, "value", None)
                if value is None:
                    fail_count += 1
                    print(f"  ✗ {series_key}/{country}: {getattr(dp, 'status', '?')}")
                else:
                    ok_count += 1
                    fc = imf.forecast_rows(series_key, country)
                    ref = getattr(getattr(dp, "metadata", None), "reference_date", "?")
                    print(f"  ✓ {series_key}/{country}: {value} (실측 {ref}, 전망 {len(fc)}년치)")
    except Exception as exc:
        fail_count += 1
        print(f"  ✗ IMF 전체 실패: {type(exc).__name__}: {exc}")

    print(f"\n집계: 성공 {ok_count}건, 실패 {fail_count}건", flush=True)
    if ok_count == 0:
        # 하나도 못 가져왔으면 그건 진짜 문제다 — 워크플로가 알아채게 한다.
        print("::warning::BLS/IMF 수집에서 단 한 건도 성공하지 못했다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
