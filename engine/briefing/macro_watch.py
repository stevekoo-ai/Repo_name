"""⑪ 경기·신용 경보 — 김영익 소장 거시 약세론의 두 시험대를 코드로 판정한다.

2026-10-20 사용자: "9월 산업활동동향(10월 말 발표)에서 선행지수가 두 달 연속
하락하는지, 하이일드 스프레드가 3.5%p를 넘는지 이거 트레이스해서 보고해."

- W1 선행지수 순환변동치(통계청, ECOS 901Y067/I16E) 두 달 연속 하락
- W2 미국 하이일드 스프레드(FRED BAMLH0A0HYM2) 3.5%p 초과
- W3 한국 "트리플 약세"(2026-10-21 오건영 단장): 최근 1개월 코스피↓·국고 10년↑·원화↓가
  동시에 — 경상수지 흑자국에서 셋이 같이 나오면 금융 시스템 위험 신호

데이터가 없거나 오래되면 R3대로 "판단 불가"이고 "안전"이 아니다.
판정은 근거이지 매매 지시가 아니다(R4).
"""
from __future__ import annotations

from datetime import date

HY_THRESHOLD = 3.5          # %p
HY_MAX_AGE_DAYS = 10        # FRED 일간, 며칠 지연 정상
TRIPLE = {"kospi_pct": -5.0, "kr10y_bp": 20.0, "usdkrw_pct": 2.0}   # 1개월 변화 기준
LEAD_MAX_AGE_DAYS = 100     # 월간, 날짜는 그달 1일·발표는 익월 말이라 정상 지연이 약 60~95일


def _rows(m: dict, key: str, as_of: date) -> list[tuple[str, float]]:
    return [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]


def evaluate(as_of: date, m: dict) -> list[dict]:
    out = []

    lead = _rows(m, "kr_leading_cycle", as_of)
    w1 = {"id": "W1", "name": "선행지수 순환변동치 2개월 연속 하락", "state": "판단 불가", "detail": "데이터 없음"}
    if len(lead) >= 3:
        (d2, v2), (d1, v1), (d0, v0) = lead[-3:]
        age = (as_of - date.fromisoformat(d0)).days
        peak_d, peak_v = max(lead[-24:], key=lambda r: r[1])
        streak = 0
        for (_, a), (_, b) in zip(reversed(lead[:-1]), reversed(lead[1:])):
            if b < a:
                streak += 1
            else:
                break
        detail = (f"{d0[:7]} {v0:.1f} (전월 {v1:.1f}, 전전월 {v2:.1f}) · 연속 하락 {streak}개월 · "
                  f"최근 2년 최고 {peak_v:.1f}({peak_d[:7]})")
        if age > LEAD_MAX_AGE_DAYS:
            w1.update(state="판단 불가", detail=detail + f" — 최신값이 {age}일 전(발표 지연 또는 수집 실패)")
        else:
            w1.update(state="🔴 점등" if streak >= 2 else ("🟡 1개월 하락" if streak == 1 else "🟢 미점등"),
                      detail=detail, streak=streak, latest=d0)
    out.append(w1)

    hy = _rows(m, "us_hy_oas", as_of)
    w2 = {"id": "W2", "name": f"미국 하이일드 스프레드 {HY_THRESHOLD}%p 초과", "state": "판단 불가", "detail": "데이터 없음"}
    if hy:
        d0, v0 = hy[-1]
        age = (as_of - date.fromisoformat(d0)).days
        prev3m = [v for d, v in hy if d <= date.fromordinal(date.fromisoformat(d0).toordinal() - 91).isoformat()]
        low1y = min(v for d, v in hy[-260:])
        detail = (f"{d0} {v0:.2f}%p (3개월 전 {prev3m[-1]:.2f}, 1년 최저 {low1y:.2f}) · "
                  f"경보선까지 {HY_THRESHOLD - v0:+.2f}%p")
        if age > HY_MAX_AGE_DAYS:
            w2.update(detail=detail + f" — 최신값이 {age}일 전")
        else:
            w2.update(state="🔴 점등" if v0 > HY_THRESHOLD else "🟢 미점등", detail=detail)
    out.append(w2)

    out.append(_triple(as_of, m))
    return out


def _chg(rows, as_of, days=30):
    rows = [(d, v) for d, v in rows if d <= as_of.isoformat()]
    if len(rows) < 2:
        return None
    d0, v0 = rows[-1]
    base = [v for d, v in rows if d <= date.fromordinal(date.fromisoformat(d0).toordinal() - days).isoformat()]
    if not base:
        return None
    return d0, base[-1], v0


def _triple(as_of: date, m: dict) -> dict:
    """W3 — 1개월 사이 코스피·국고10년·원/달러 세 다리가 모두 약세 방향으로 임계를 넘었나."""
    from engine.briefing import sentiment as S

    w3 = {"id": "W3", "name": "한국 트리플 약세(주가↓·금리↑·원화↓)", "state": "판단 불가", "detail": "데이터 없음"}
    k = _chg(S._daily_price("0001"), as_of)
    b = _chg(m.get("kr_treasury_10y", []), as_of)
    f = _chg(m.get("kr_usdkrw", []), as_of)
    if not (k and b and f):
        return w3
    kp = (k[2] / k[1] - 1) * 100
    bp = (b[2] - b[1]) * 100
    fp = (f[2] / f[1] - 1) * 100
    legs = [kp <= TRIPLE["kospi_pct"], bp >= TRIPLE["kr10y_bp"], fp >= TRIPLE["usdkrw_pct"]]
    detail = (f"1개월: 코스피 {kp:+.1f}%{'✔' if legs[0] else ''} · 국고10년 {bp:+.0f}bp{'✔' if legs[1] else ''} · "
              f"원/달러 {fp:+.1f}%{'✔' if legs[2] else ''} (임계 {TRIPLE['kospi_pct']:.0f}% / +{TRIPLE['kr10y_bp']:.0f}bp / "
              f"+{TRIPLE['usdkrw_pct']:.0f}%, 기준 {k[0]})")
    n = sum(legs)
    w3.update(state="🔴 점등" if n == 3 else (f"🟡 {n}/3" if n else "🟢 미점등"), detail=detail, legs=n)
    return w3


def render_markdown(results: list[dict]) -> str:
    lines = ["| 경보 | 상태 | 근거 |", "|---|---|---|"]
    for r in results:
        lines.append(f"| {r['id']} {r['name']} | {r['state']} | {r['detail']} |")
    lit = [r for r in results if r["state"].startswith("🔴")]
    lines.append("")
    if len(lit) >= 2:
        lines.append("> 🔴 **경보 2개 이상 점등 — 경기·신용·금융 시스템 위험이 겹쳤다.** "
                     "거시 약세론(김영익 10/20, 오건영 10/21 INGEST)의 근거가 강해졌다. 판단 근거이지 매매 지시가 아니다(R4).")
    elif lit:
        lines.append(f"> 🟠 **{lit[0]['id']} 점등.** 거시 약세론의 근거 하나가 확인됐다. 다른 하나는 아직이다.")
    else:
        lines.append("> 아직 점등된 경보 없음 — 거시 약세론의 시험대는 통과 전이다. "
                     "선행지수는 매월 말 산업활동동향(통계청) 발표 때 갱신된다.")
    return "\n".join(lines)
