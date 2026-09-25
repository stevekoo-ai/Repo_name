"""중간선거 대통령 레버 체크포인트 자동 판정 — 브리핑 ⑩ 블록.

2026-09-25 사용자 요청으로 트럼프 트래커에 "레버가 유권자 지갑에 닿았나(L1)"와
"선거 후 청구서(L3)" 체크포인트를 만들었고(wiki/concepts/trump-midterm-tracker.md),
그중 FRED로 매일 잡히는 것을 여기서 규칙으로 판정한다. 임계값은 위키 표와 같다.

- 값이 없거나 오래됐으면 판정하지 않는다(R3 — 판정 불가를 드러낸다).
- "지속" 조건이 있는 신호는 최근 N개 관측치가 모두 조건을 만족해야 켠다.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

ACTIVE_UNTIL = date(2026, 12, 11)  # 12/11 CR 만료까지 — 선거 후 청구서 창 포함

# (id, 층, series, 설명, 방향, 임계, 연속 관측치 수, 신호 의미, 최대 허용 지연일)
CHECKS = [
    ("L1-gas", "L1 지갑", "us_gasoline", "휘발유 전국 평균", "<", 4.00, 2,
     "$4.00 아래 2주 = 종전·유가 레버가 주유소까지 전달", 14),
    ("L1-mortgage", "L1 지갑", "us_mortgage_30y", "30년 모기지", "<", 6.5, 2,
     "6.5% 아래 2주 = 금리 레버 부활", 14),
    ("L1-brent", "L1 지갑", "us_brent", "브렌트유", "<", 85.0, 5,
     "$85 아래 1주 안착 = 종전 레버 1차 반응", 10),
    ("L3-30y", "L3 청구서", "us_30y", "30년물 국채금리", ">", 5.5, 3,
     "5.5% 돌파 3일 = 채권 자경단(재정 신뢰 이탈)", 7),
    ("L3-hy", "L3 청구서", "us_hy_oas", "하이일드 스프레드", ">", 5.0, 3,
     "5%p 돌파 = 위험회피 확산", 7),
]
# 방향만 보는 추세 지표: (id, 층, series, 설명, 비교 관측치 수, 해석)
TRENDS = [
    ("L1-mich", "L1 지갑", "us_mich_infl_1y", "미시간대 1년 기대인플레", 1,
     "하락 = 체감물가 개선 / 상승 = 악화 (FRED 공개가 약 2개월 늦다)", 100),
    ("L3-5y5y", "L3 청구서", "us_5y5y_infl", "5년 뒤 5년 기대인플레", 20,
     "20일 +0.25%p 이상 급등 = 연준 신뢰 훼손 경고", 7),
    ("L1-tga", "L1 지갑", "us_tga", "재무부 현금잔고(TGA, 백만달러)", 4,
     "4주 감소 = 재정 지출이 풀리는 중(집행 앞당김 단서)", 14),
]


@dataclass
class LeverCheck:
    id: str
    layer: str
    label: str
    ok: bool | None
    detail: str
    meaning: str


def _recent(series: list[tuple[str, float]], as_of: date, max_age: int):
    rows = [(d, v) for d, v in series if d <= as_of.isoformat()]
    if not rows or (as_of - date.fromisoformat(rows[-1][0])).days > max_age:
        return None
    return rows


def evaluate(as_of: date, series_map: dict) -> list[LeverCheck]:
    out = []
    for cid, layer, key, label, op, thr, n, meaning, max_age in CHECKS:
        rows = _recent(series_map.get(key, []), as_of, max_age)
        if not rows or len(rows) < n:
            out.append(LeverCheck(cid, layer, label, None, "데이터 없음/지연 — 판정 불가", meaning))
            continue
        last = [v for _, v in rows[-n:]]
        hit = all((v < thr) if op == "<" else (v > thr) for v in last)
        out.append(LeverCheck(cid, layer, label, hit,
                              f"{rows[-1][1]:,.2f} ({rows[-1][0]}), 기준 {op} {thr} × 최근 {n}회", meaning))
    for cid, layer, key, label, lag, meaning, max_age in TRENDS:
        rows = _recent(series_map.get(key, []), as_of, max_age)
        if not rows or len(rows) <= lag:
            out.append(LeverCheck(cid, layer, label, None, "데이터 없음/지연 — 판정 불가", meaning))
            continue
        cur, prev = rows[-1][1], rows[-1 - lag][1]
        chg = cur - prev
        if cid == "L3-5y5y":
            flag = chg >= 0.25          # 경고가 켜짐
        elif cid == "L1-tga":
            flag = chg < 0               # 지출이 풀리는 중
        else:
            flag = chg < 0               # 기대인플레 하락 = 개선
        out.append(LeverCheck(cid, layer, label, flag,
                              f"{cur:,.2f} ({rows[-1][0]}), {lag}관측 전 대비 {chg:+.2f}", meaning))
    return out


_ICON = {True: "🔔", False: "·", None: "❓"}


def render_markdown(checks: list[LeverCheck], as_of: date) -> str:
    d = (date(2026, 11, 3) - as_of).days
    lines = [f"선거까지 D-{d} (11/3). 🔔 = 신호 켜짐, · = 아직, ❓ = 판정 불가. "
             "레버 전체 판단은 wiki/concepts/trump-midterm-tracker.md 참고."]
    for c in checks:
        lines.append(f"- {_ICON[c.ok]} **{c.layer} · {c.label}** — {c.detail}  \n  ↳ {c.meaning}")
    on = [c for c in checks if c.ok]
    if on:
        lines.append("> ⚠️ 켜진 신호가 있다 — 오늘의 판단/결론에 반영할 것: "
                     + ", ".join(f"{c.label}" for c in on))
    return "\n".join(lines)
