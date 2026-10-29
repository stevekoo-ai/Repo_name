"""⑫ 시나리오 점검 — 오늘 어느 길 위에 있나, 그 길이면 무엇을 하나(2026-10-28).

2026-10-28 사용자: "누가 맞는지를 알아가는 것은 의미가 없다. 누구의 시나리오를 따라갈 때
결과나 action item이 뭔지를 정리하고 실제 진행 방향에 따라 대응 전략을 제시하는 것이다."
→ wiki/concepts/scenario-action-playbook.md 의 S1~S4 확인 신호를 자동으로 재고, 우세 시나리오와
그때의 행동을 한 줄로 낸다.

- 우선순위: S4(거시 쇼크) > S3(사이클 꺾임) > S1(슈퍼사이클, 신호 2개 이상) > S2(박스권).
  신호가 섞이면 더 보수적인 쪽 — 주거 자금은 날짜가 있다.
- 데이터가 없으면 그 신호는 "판단 불가"이고 "미충족(안전)"이 아니다(R3).
- 판정은 근거이지 매매 지시가 아니다(R4). 행동 문구는 사용자가 승인한 플레이북 원문.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SOURCES = REPO / "sources"

# 2026-10-28 사용자 승인 T1 조정안(wiki/monitoring/housing-funding-execution-status.md)
DEFER_START = "2026-10-28"      # 연기분 12주 추적 시작일(이날 종가부터 최고가 갱신)
DEFER_DEADLINE = "2026-11-13"
DEFER_FLOOR = 1_341_000         # 실적 전 10/27 종가 — 아래면 서프라이즈 효과 소멸
DEFER_TRAIL = 0.08              # 연기 후 최고 종가 대비 하락폭
BOX = (1_300_000, 1_500_000)

ACTIONS = {
    "S4": "주거 자금만 일정 앞당김(T2·T3), 쓸 날짜 없는 몫은 매도하지 않음, 인도 추가 중단",
    "S3": "연기분 12주 즉시 매도, T2·T3 앞당김(전세안이면 더 서두름), 분산 즉시, 인도 추가 중단",
    "S1": "연기분 12주는 11/13까지 보유 후 그 안에서 매도, T2는 11월 중순 이후, 분산은 천천히 계속, 인도 1/3씩",
    "S2": "연기분 12주는 11/13에 매도, T2는 11월 안에 2~3회 분할, 분산 실행 적기(DC·ISA·IRP 안에서 교체)",
    "S1/S2": "공통 행동만 — T1 13주는 늦어도 11/3 장 마감까지(선거 전), 집 형태(전세/월세)는 11/4 전 결정, 추가 매수 없음",
}


def _last(rows, as_of):
    rows = [(d, v) for d, v in rows if d <= as_of.isoformat()]
    return rows[-1] if rows else None


def _first_series(m, names, as_of):
    """같은 지표의 여러 원천 중 as_of 기준 가장 최신 값을 쓴다(신선도 쌍둥이)."""
    best = None
    for n in names:
        r = _last(m.get(n, []), as_of)
        if r and (best is None or r[0] > best[0]):
            best = r
    return best


def load_hynix_closes() -> list[tuple[str, float]]:
    p = SOURCES / "sk-hynix-price-snapshot.csv"
    out = {}
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            try:
                out[r["date"]] = float(r["price"])
            except (ValueError, KeyError):
                continue
    return sorted(out.items())


def load_foreign_flows() -> list[tuple[str, float]]:
    p = SOURCES / "sk-hynix-investor-flow.csv"
    out = {}
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if r.get("ticker") == "000660" and r.get("foreign_net_krw"):
                out[r["date"]] = float(r["foreign_net_krw"])
    return sorted(out.items())


def load_breadth() -> list[tuple[str, int, int]]:
    p = SOURCES / "kr-index-quote.csv"
    out = {}
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if r.get("index_code") == "0001":
                try:
                    a, d = int(r["advancers"]), int(r["decliners"])
                except (ValueError, KeyError):
                    continue
                if a + d:            # 휴장일 0:0 행은 건너뛴다
                    out[r["date"]] = (a, d)
    return [(k, *v) for k, v in sorted(out.items())]


def _sig(name, ok, detail):
    """ok: True(충족) / False(미충족) / None(판단 불가)."""
    return {"name": name, "ok": ok, "detail": detail}


def evaluate(as_of: date, m: dict, closes: list, flows: list, breadth: list, watch: list) -> dict:
    iso = as_of.isoformat()
    closes = [(d, v) for d, v in closes if d <= iso]
    flows = [(d, v) for d, v in flows if d <= iso]
    breadth = [r for r in breadth if r[0] <= iso]
    w = {r["id"]: r for r in watch}

    y10 = _first_series(m, ["us_10y_yf", "us_10y"], as_of)
    brent = _first_series(m, ["us_brent_futures", "us_brent"], as_of)
    vix = _first_series(m, ["us_vix_yf", "us_vix"], as_of)
    last = closes[-1] if closes else None

    # ---- S1: 2개 이상 ----
    s1 = []
    if len(flows) >= 3:
        f3 = flows[-3:]
        s1.append(_sig("외국인 3일 연속 순매수", all(v > 0 for _, v in f3),
                       " / ".join(f"{d[5:]} {v/1e8:+,.0f}억" for d, v in f3)))
    else:
        s1.append(_sig("외국인 3일 연속 순매수", None, "수급 자료 부족"))
    s1.append(_sig("미 10년물 ≤ 4.8%", None if not y10 else y10[1] <= 4.8,
                   "자료 없음" if not y10 else f"{y10[1]:.2f}% ({y10[0][5:]})"))
    s1.append(_sig("브렌트 < 100달러", None if not brent else brent[1] < 100,
                   "자료 없음" if not brent else f"${brent[1]:.1f} ({brent[0][5:]})"))
    if len(breadth) >= 3:
        b3 = breadth[-3:]
        s1.append(_sig("코스피 상승 종목 > 하락 3일", all(a > d for _, a, d in b3),
                       " / ".join(f"{dd[5:]} {a}:{d}" for dd, a, d in b3)))
    else:
        s1.append(_sig("코스피 상승 종목 > 하락 3일", None, "자료 부족"))

    # ---- S3: 하나라도 ----
    s3 = []
    if last:
        s3.append(_sig(f"하이닉스 종가 < {DEFER_FLOOR:,}", last[1] < DEFER_FLOOR, f"{last[1]:,.0f} ({last[0][5:]})"))
        since = [v for d, v in closes if d >= DEFER_START]
        if since and iso <= DEFER_DEADLINE:
            pk = max(since)
            s3.append(_sig(f"연기 후 최고 종가 대비 −{DEFER_TRAIL:.0%}", last[1] <= pk * (1 - DEFER_TRAIL),
                           f"최고 {pk:,.0f} → 기준선 {pk*(1-DEFER_TRAIL):,.0f}"))
    else:
        s3.append(_sig(f"하이닉스 종가 < {DEFER_FLOOR:,}", None, "시세 없음"))
    for wid, label in (("W2", "하이일드 스프레드 > 3.5%p"), ("W1", "선행지수 2개월 연속 하락")):
        r = w.get(wid)
        if not r or r["state"] == "판단 불가":
            s3.append(_sig(label, None, "판단 불가(⑪)"))
        else:
            s3.append(_sig(label, r["state"].startswith("🔴"), r["state"]))

    # ---- S4: 하나라도 ----
    s4 = [
        _sig("미 10년물 ≥ 5.3%", None if not y10 else y10[1] >= 5.3, "자료 없음" if not y10 else f"{y10[1]:.2f}%"),
        _sig("브렌트 ≥ 120달러", None if not brent else brent[1] >= 120, "자료 없음" if not brent else f"${brent[1]:.1f}"),
        _sig("VIX ≥ 30", None if not vix else vix[1] >= 30, "자료 없음" if not vix else f"{vix[1]:.1f}"),
    ]

    # ---- S2 ----
    box_days = 0
    for _, v in reversed(closes):
        if BOX[0] <= v <= BOX[1]:
            box_days += 1
        else:
            break
    s2 = [_sig(f"{BOX[0]:,}~{BOX[1]:,} 박스 10거래일 이상", (box_days >= 10) if last else None,
               f"연속 {box_days}거래일")]

    hit = lambda sigs: sum(1 for s in sigs if s["ok"] is True)
    if hit(s4):
        dom = "S4"
    elif hit(s3):
        dom = "S3"
    elif hit(s1) >= 2:
        dom = "S1"
    elif hit(s2):
        dom = "S2"
    else:
        dom = "S1/S2"
    return {"dominant": dom, "action": ACTIONS[dom], "S1": s1, "S2": s2, "S3": s3, "S4": s4,
            "unknown": sum(1 for g in (s1, s2, s3, s4) for s in g if s["ok"] is None)}


LABEL = {"S1": "S1 AI 슈퍼사이클 지속(2개 이상)", "S2": "S2 박스권", "S3": "S3 사이클 꺾임(하나라도)",
         "S4": "S4 거시 쇼크(하나라도)"}
NAME = {"S1": "AI 슈퍼사이클 지속", "S2": "박스권", "S3": "사이클 꺾임", "S4": "거시 쇼크",
        "S1/S2": "S1·S2 사이(판정 대기)"}


def render_markdown(res: dict) -> str:
    mark = {True: "✅", False: "—", None: "판단 불가"}
    lines = [f"**우세 시나리오: {res['dominant']} {NAME[res['dominant']]}** → {res['action']}", "",
             "| 시나리오 | 신호 | 상태 | 근거 |", "|---|---|---|---|"]
    for k in ("S4", "S3", "S1", "S2"):
        for s in res[k]:
            lines.append(f"| {LABEL[k]} | {s['name']} | {mark[s['ok']]} | {s['detail']} |")
    lines += ["", "> 수동 확인 신호(자동 수집 없음): 고객 재고·주문 조정 언급, D램 계약가, 빅테크 CapEx, "
              "깜짝 인상·다회 인상 발언, 선거 결과(교착/블루/레드). 판정은 근거이지 매매 지시가 아니다(R4). "
              "플레이북: wiki/concepts/scenario-action-playbook.md"]
    if res["unknown"]:
        lines.append(f"> 판단 불가 신호 {res['unknown']}개 — '안전'으로 읽지 말 것(R3).")
    return "\n".join(lines)


def collect(as_of: date, m: dict) -> dict:
    from engine.briefing import macro_watch as MW
    try:
        watch = MW.evaluate(as_of, m)
    except Exception:  # noqa: BLE001 — ⑪ 실패가 ⑫를 막지 않게
        watch = []
    return evaluate(as_of, m, load_hynix_closes(), load_foreign_flows(), load_breadth(), watch)
