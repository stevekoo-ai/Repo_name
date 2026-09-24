"""브리핑 팩 — LLM이 **위키 대신 읽는** 크기 고정 컨텍스트.

## 왜 이게 필요한가

사용자가 겪은 두 실패:
  1. 위키·기존 리포트를 전부 넣기 → context 폭발 → 내용이 부실해짐
  2. 아주 간단히만 → 원하는 보고서가 아님

둘 다 같은 원인이다 — **선별 계층이 없어서** "전부 아니면 아무것도" 두 극단
밖에 없었다. 실측하면 이유가 분명하다:

    위키 268페이지 6.8MB   → 통째로 읽는 건 애초에 불가능
    리포트 1개 40,415자    → 약 27,000토큰. 이것만으로 예산이 날아간다
    digest 5개 약 4,000자  → 약 2,700토큰

그래서 이 모듈은 **크기가 고정된 팩**을 만든다. 위키가 500페이지가 돼도
팩 크기는 안 변한다 — 요약이 아니라 **선별**이기 때문이다. 오늘 안 고른
페이지는 잃는 게 아니라 다음에 고르면 된다.

## 규칙

- LLM은 `wiki/`를 직접 읽지 않는다. 이 팩만 읽는다.
- 팩의 모든 숫자는 **코드가 계산**한다. LLM이 만드는 건 서사와 판단뿐.
- 미수집은 "없음"으로 명시한다. 조용히 빼면 LLM이 있는 줄 알고 지어낸다(R3).
"""
from __future__ import annotations

import csv
import glob
import os
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
KST = timezone(timedelta(hours=9))

# macro-series.csv는 매일 자라고 과거분도 소급 백필된다 — 테스트가 이
# 실제 파일을 직접 읽으면 파일이 자랄 때마다 "특정 as_of 시점엔 지연이
# 있었다/없었다" 같은 시간에 종속된 단언이 깨진다. 모듈 상수로 빼서
# 테스트가 monkeypatch로 격리된 파일을 넣을 수 있게 한다(원장 격리와
# 같은 이유 — tests/test_briefing_context.py의 _isolated_ledger 참고).
MACRO_SERIES = REPO / "sources" / "macro-series.csv"

# 팩의 크기 상한(문자). 넘으면 잘라내고 잘렸다고 표기한다 —
# 조용히 넘치면 그날 리포트만 이상해지고 원인을 못 찾는다.
MAX_PACK_CHARS = 24_000

# digest 선별 개수. 늘리면 팩이 커지고 줄이면 맥락이 얇아진다.
DIGEST_SLOTS = 5

# 거시 수집이 이 시간(시간) 이상 전이면 "오늘 수집분 없음"으로 본다.
# 수집은 하루 1회라 20시간을 넘으면 그날 치가 아직 안 들어온 것이다.
STALE_COLLECTION_HOURS = 20


@dataclass
class Block:
    key: str
    title: str
    body: str
    chars: int = 0

    def __post_init__(self):
        self.chars = len(self.body)


@dataclass
class BriefingPack:
    slot: str                    # "AM" | "PM"
    as_of: datetime              # KST
    blocks: list[Block] = field(default_factory=list)

    @property
    def chars(self) -> int:
        return sum(b.chars for b in self.blocks)

    def render(self) -> str:
        head = (f"# 브리핑 팩 — {self.slot} ({self.as_of.strftime('%Y-%m-%d %H:%M')} KST)\n\n"
                f"> 이 파일은 코드가 생성했다. 여기 없는 숫자는 **없는 것이다** — "
                f"위키나 기억에서 끌어와 채우지 말 것.\n")
        parts = [head]
        for b in self.blocks:
            parts.append(f"\n## {b.title}\n\n{b.body}\n")
        out = "".join(parts)
        if len(out) > MAX_PACK_CHARS:
            out = out[:MAX_PACK_CHARS] + (
                f"\n\n⚠️ 팩이 상한({MAX_PACK_CHARS:,}자)을 넘어 잘렸다 — "
                "선별 규칙을 좁혀야 한다.\n")
        return out


# ─────────────────────────────────────────────────────────────
# 블록 ① 오늘의 실측 팩트시트
# ─────────────────────────────────────────────────────────────
def _series_map() -> dict[str, list[tuple[str, float]]]:
    path = MACRO_SERIES
    out: dict[str, list[tuple[str, float]]] = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                out.setdefault(r["series"], []).append((r["date"], float(r["value"])))
            except (ValueError, TypeError):
                continue
    for k in out:
        out[k].sort()
    return out


def _change(rows: list[tuple[str, float]], days: int) -> tuple[float, float, str] | None:
    """(최신값, 변화율%, 최신일). days 영업일 전 대비."""
    if len(rows) < 2:
        return None
    last_d, last_v = rows[-1]
    idx = max(0, len(rows) - 1 - days)
    prev_v = rows[idx][1]
    if prev_v == 0:
        return None
    return last_v, (last_v / prev_v - 1) * 100, last_d


# 팩트시트에 싣는 지표. (키, 표시명, 단위, 변화 표기 방식)
FACT_SERIES = [
    ("us_nasdaq", "나스닥", "", "pct"),
    ("us_sp500", "S&P500", "", "pct"),
    ("us_vix", "VIX", "", "level"),
    ("us_10y", "미 10년물", "%", "bp"),
    ("us_2y", "미 2년물", "%", "bp"),
    ("us_3m", "미 3개월물", "%", "bp"),
    ("us_hy_oas", "하이일드 스프레드", "%p", "bp"),
    ("us_dollar_index", "달러지수", "", "pct"),
    # 2026-09-18 추가. 위 DTWEXBGS(연준 26개국 무역가중)는 원천 발표가
    # 며칠 늦어 자주 ⚠️N일 지연이 뜬다 — 매일 나오는 ICE DXY를 나란히
    # 둬서 그날의 달러 방향을 어쨌든 볼 수 있게 한다. **대체가 아니다**:
    # 바스켓이 달라 값 자체가 다르므로(같은 날 118.21 vs 100.44) 라벨에
    # "참고"를 박아 둘을 섞어 읽지 않게 한다.
    ("us_dollar_index_dxy", "달러지수(DXY·참고)", "", "pct"),
    ("us_brent", "브렌트유", "$", "pct"),
    ("kr_usdkrw", "원/달러(ECOS)", "원", "pct"),
]


def collection_freshness(now: datetime | None = None) -> tuple[str | None, float | None]:
    """macro-series.csv를 **마지막으로 수집한 시각**과 그 경과 시간(시간 단위).

    ## 왜 데이터 날짜가 아니라 수집 시각인가

    팩 ①의 "⚠️N일 지연"은 **데이터 기준일**이 며칠 전인지를 잰다. 그건
    FRED가 늦게 발표해서일 수도 있고(정상), 우리가 수집을 못 해서일 수도
    있다(장애) — 둘이 구분되지 않는다.

    2026-09-14에 실제로 후자였다. 거시 수집(cron 22:10 UTC)이 GitHub
    Actions 큐 대기로 **매번 약 2시간씩 밀려** 00:00~00:15 UTC에 끝나는데,
    AM 브리핑은 (당시) 22:30 UTC에 돌았다. 완충이 20분뿐이라 **브리핑이
    항상 먼저 돌고 그날 수집분을 못 썼다** — 9/14 브리핑이 쓴 데이터는
    22시간 전 수집분이었고, 그날 수집은 브리핑 1시간 27분 뒤에 끝났다.

    이후 수집을 20:15 UTC로, 브리핑을 23:00 UTC(08:00 KST)로 옮겨 완충을
    2h45m으로 벌렸다. 다만 cron 조정은 GitHub 큐 사정이 바뀌면 다시
    깨지므로, **이 함수(상태 탐지)가 본선이고 cron은 보조**다.

    이걸 알면 LLM이 "숫자가 오래된 건 FRED 탓"이라고 오독하지 않고
    "오늘 수집분이 아직 없으니 직전 세션은 뉴스로 확인해야 한다"고
    행동할 수 있다(R1: 측정 > 추론).
    """
    p = MACRO_SERIES
    if not p.exists():
        return None, None
    latest = ""
    with p.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            f = r.get("fetched_at") or ""
            if f > latest:
                latest = f
    if not latest:
        return None, None
    try:
        t = datetime.fromisoformat(latest.replace("Z", "+00:00"))
    except ValueError:
        return latest, None
    now = now or datetime.now(timezone.utc)
    return latest, (now - t).total_seconds() / 3600


def build_fact_sheet(as_of: date) -> Block:
    m = _series_map()
    lines = ["| 지표 | 최신 | 1일 | 5일 | 기준일 |", "|---|---:|---:|---:|---|"]
    missing = []
    stale: list[tuple[str, int, str]] = []  # (label, age_days, last_date) — age>=3
    for key, label, unit, mode in FACT_SERIES:
        rows = [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]
        if len(rows) < 2:
            missing.append(label)
            continue
        last_v, d1, last_d = _change(rows, 1) or (None, None, None)
        _, d5, _ = _change(rows, 5) or (None, None, None)
        age = (as_of - date.fromisoformat(last_d)).days
        stale_mark = f" ⚠️{age}일 지연" if age >= 3 else ""
        if age >= 3:
            stale.append((label, age, last_d))

        def fmt(pct):
            if pct is None:
                return "—"
            if mode == "bp":
                return f"{pct * last_v / 100 * 100:+.0f}bp" if last_v else "—"
            if mode == "level":
                return f"{pct:+.1f}%"
            return f"{pct:+.2f}%"

        lines.append(f"| {label} | {last_v:,.2f}{unit} | {fmt(d1)} | {fmt(d5)} | {last_d}{stale_mark} |")
    body = "\n".join(lines)
    if missing:
        body += f"\n\n**미수집**: {', '.join(missing)} — 없는 것이므로 언급하지 말 것."

    if stale:
        # 2026-09-18 신설 — 사용자 지적: 지연된 지표를 뉴스 검색으로
        # 보정하는 "뉴스로 보정되는 칸"이 과거엔 사고가 났던 몇 개
        # 지표(10년물·브렌트유·원달러)에만 우연히 붙어 있었다. 그날그날
        # 실제로 지연된 지표가 다를 수 있으므로, ⚠️ 마크와 같은 나이
        # 기준(3일 이상)으로 매번 다시 계산해 빠짐없이 강제한다 —
        # 특정 지표를 하드코딩하지 않는다.
        body += ("\n\n**🔎 뉴스 교차검증 필수 목록** (하나도 빠짐없이 웹검색해서 "
                 "아래 '뉴스로 보정되는 칸' 표에 병기할 것 — 이 목록은 프롬프트의 "
                 "일반 검색 횟수 권장보다 우선한다. 오늘 지연된 지표가 몇 개든 "
                 "전부 확인한다):\n")
        for label, age, last_d in stale:
            body += f"- {label} ({last_d} 기준, {age}일 지연)\n"
        body += ("> ⚠️ 웹검색으로도 최신값을 못 찾으면 '검색함 → 최신값 확인 안 "
                 "됨(팩 값 유지)'으로 명시할 것 — 조용히 생략하지 말 것.")

    fetched, hours = collection_freshness()
    if hours is not None:
        if hours >= STALE_COLLECTION_HOURS:
            body += (f"\n\n🔴 **오늘 수집분이 아직 없다.** 거시 데이터의 마지막 수집은 "
                     f"`{fetched[:16]}` — **{hours:.0f}시간 전**이다.\n"
                     f"위 표의 '지연'은 FRED 발표 지연이 아니라 **수집이 안 된 탓일 수 있다.** "
                     f"직전 세션 수치는 표를 믿지 말고 **뉴스로 확인할 것.**\n"
                     f"(원인: 거시 수집 cron과 이 브리핑의 간격이 GitHub Actions 큐 지연보다 "
                     f"짧아 브리핑이 먼저 도는 경쟁 조건 — 2026-09-14 확인)")
        else:
            body += f"\n\n거시 수집: `{fetched[:16]}` ({hours:.0f}시간 전) — 최신."
    return Block("facts", "① 오늘의 실측 (macro-series.csv)", body)


def build_hynix_block(as_of: date) -> Block:
    """KIS 실측 — 하이닉스 시세·수급·신용·공매도·ADR."""
    def tail(name: str, n: int = 1) -> list[list[str]]:
        p = REPO / "sources" / f"{name}.csv"
        if not p.exists():
            return []
        with p.open(encoding="utf-8") as fh:
            rows = [r for r in csv.reader(fh) if r]
        body = [r for r in rows[1:] if r and r[0] <= as_of.isoformat()]
        return body[-n:]

    lines = []
    snap = tail("sk-hynix-price-snapshot")
    if snap:
        r = snap[-1]
        lines.append(f"- **종가** {r[0]}: {int(float(r[2])):,}원 "
                     f"({float(r[4]):+.2f}%), 외국인 보유율 {r[6]}%")
    flow = tail("sk-hynix-investor-flow", 5)
    if flow:
        try:
            frn = sum(float(r[5]) for r in flow) / 1e12
            org = sum(float(r[6]) for r in flow) / 1e12
            ind = sum(float(r[7]) for r in flow) / 1e12
            lines.append(f"- **최근 5거래일 순매수**: 외국인 {frn:+.2f}조 / "
                         f"기관 {org:+.2f}조 / 개인 {ind:+.2f}조")
        except (ValueError, IndexError):
            pass
    adr = tail("sk-hynix-adr-quote")
    if adr:
        r = adr[-1]
        lines.append(f"- **ADR** {r[0]}: ${r[2]} ({float(r[4]):+.2f}%) "
                     f"← 밤사이 미국 반응의 직접 지표")
    credit = tail("sk-hynix-credit-balance", 2)
    if len(credit) == 2:
        try:
            delta = float(credit[-1][2]) - float(credit[-2][2])
            lines.append(f"- **신용융자잔고** {credit[-1][0]}: "
                         f"{int(float(credit[-1][2])):,}주 ({delta:+,.0f})")
        except (ValueError, IndexError):
            pass
    if not lines:
        lines = ["- (KIS 수집 데이터 없음 — 브랜치가 main과 갈라졌는지 확인할 것)"]
    return Block("hynix", "② SK하이닉스 실측 (KIS)", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 블록 ③ 위키 digest 선별 — 이 팩의 핵심 아이디어
# ─────────────────────────────────────────────────────────────
def _load_digests() -> list[dict]:
    out = []
    for f in sorted(glob.glob(str(REPO / "data" / "wiki_digest" / "*.yaml"))):
        try:
            d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if d.get("one_line_summary"):
            d["slug"] = os.path.basename(f)[:-5]
            out.append(d)
    return out


def select_digests(as_of: date, triggers: set[str], slots: int = DIGEST_SLOTS) -> list[dict]:
    """오늘 읽힐 digest를 고른다 — **요약이 아니라 선별**이다.

    위키가 커져도 팩 크기가 안 커지는 이유가 여기 있다. 오늘 안 고른
    페이지는 잃는 게 아니라 다음에 고르면 된다.

    규칙(우선순위 순):
      1. 오늘 켜진 트리거에 대응하는 digest — 실제로 움직인 것
      2. 남는 자리는 **가장 오래 안 읽힌 순**으로 채운다(로테이션)

    2번이 없으면 조용한 축은 영원히 안 읽히고, 그 축이 조용히 썩는다.
    실제로 이 저장소의 monitoring 페이지 절반이 3주 이상 미갱신이었다.
    """
    digests = _load_digests()
    by_slug = {d["slug"]: d for d in digests}
    chosen: list[dict] = []

    for slug in TRIGGER_TO_DIGEST_ORDER:
        if slug in triggers and slug in by_slug and by_slug[slug] not in chosen:
            chosen.append(by_slug[slug])
        if len(chosen) >= slots:
            return chosen[:slots]

    # 로테이션 — as_of가 오래된 순
    rest = sorted((d for d in digests if d not in chosen),
                  key=lambda d: str(d.get("as_of", "")))
    chosen.extend(rest[: slots - len(chosen)])
    return chosen[:slots]


# 트리거 이름 = digest slug. 우선순위는 이 순서대로.
TRIGGER_TO_DIGEST_ORDER = [
    "ai-capex-slowdown",
    "fx-regime-score",
    "hbm-cycle-score",
    "sk-hynix-analyst-thesis-checkpoints",
    "market-cycles-leverage-risk",
    "panic-recovery-signals",
    "semiconductor-export-peak-recovery",
    "kospi-valuation-tracker",
    "macro-regime-history",
    "trump-midterm-tracker",
    "data-center-construction-vs-opposition",
    "situational-awareness-fund-liquidation",
    "sk-hynix-decision-tracker",
    "rate-outlook-scenario",
]


def detect_triggers(as_of: date) -> tuple[set[str], list[str]]:
    """오늘 무엇이 움직였나 → (digest 트리거 집합, 사람이 읽는 사유 목록).

    이 판정이 곧 §블록③의 선별 근거이자 §게이트의 입력이다."""
    fired: set[str] = set()
    why: list[str] = []
    m = _series_map()

    def rows(key):
        return [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]

    # FX 국면 — 경고가 켜졌거나 이격이 큰가
    try:
        from engine.fx.regime_score import calculate_frs, ma36_gap
        from engine.fx.transition import evaluate
        from collectors.manual import fetch_fx_risk_events
        ev = fetch_fx_risk_events()
        rep = evaluate(as_of, ev)
        if rep.count:
            fired.add("fx-regime-score")
            why.append(f"FX 전환 경고 {rep.count}/4 ({rep.trigger_kind.value})")
        g = ma36_gap(as_of)
        if g and abs(g[2]) >= 5:
            fired.add("fx-regime-score")
            why.append(f"원/달러 MA36 이격 {g[2]:+.1f}%")
    except Exception:
        pass

    # 하이닉스 급변
    snap = REPO / "sources" / "sk-hynix-price-snapshot.csv"
    if snap.exists():
        with snap.open(encoding="utf-8") as fh:
            body = [r for r in csv.reader(fh)][1:]
        body = [r for r in body if r and r[0] <= as_of.isoformat()]
        if body:
            try:
                chg = float(body[-1][4])
                if abs(chg) >= 3.0:
                    fired |= {"hbm-cycle-score", "sk-hynix-analyst-thesis-checkpoints"}
                    why.append(f"SK하이닉스 {chg:+.2f}%")
            except (ValueError, IndexError):
                pass

    # 미 장기금리 급등 — 국면 종료 트리거이자 장기채 경계
    r10 = rows("us_10y")
    if len(r10) > 20:
        chg = r10[-1][1] - r10[-21][1]
        if abs(chg) >= 0.25:
            fired.add("macro-regime-history")
            why.append(f"미 10년물 20일 {chg:+.2f}%p")

    # 위험선호 급변
    rv = rows("us_vix")
    if len(rv) > 5 and rv[-6][1]:
        chg = (rv[-1][1] / rv[-6][1] - 1) * 100
        if abs(chg) >= 20:
            fired |= {"market-cycles-leverage-risk", "panic-recovery-signals"}
            why.append(f"VIX 5일 {chg:+.0f}%")

    # 금리 전망 3대 시나리오 — 한은 기준금리 변동(디커플링 축 직접 증거)
    # 또는 FOMC/금통위가 임박했을 때(±3일) 켜진다. 2026-09-12
    # rate-outlook-scenarios-2026 참고.
    rb = rows("kr_base_rate")
    if len(rb) >= 2 and rb[-1][1] != rb[-2][1]:
        fired.add("rate-outlook-scenario")
        why.append(f"한국 기준금리 변동 {rb[-2][1]:.2f}→{rb[-1][1]:.2f}")
    try:
        from engine.briefing import calendar as C
        for ev in C.upcoming_events(as_of, horizon_days=3):
            if ev.get("type") in ("FOMC", "BOK"):
                fired.add("rate-outlook-scenario")
                why.append(f"{ev['date']} {ev['name']} 임박")
                break
    except Exception:
        pass

    return fired, why


def build_digest_block(as_of: date, triggers: set[str], why: list[str]) -> Block:
    chosen = select_digests(as_of, triggers)
    lines = []
    if why:
        lines.append(f"**오늘 켜진 신호**: {' · '.join(why)}\n")
    for d in chosen:
        age = ""
        try:
            days = (as_of - date.fromisoformat(str(d.get("as_of")))).days
            if days >= 7:
                age = f" ⚠️{days}일 전 판단"
        except (ValueError, TypeError):
            age = " ⚠️날짜 불명"
        lines.append(f"### {d.get('status_label', d['slug'])}{age}\n"
                     f"{str(d['one_line_summary']).strip()}\n"
                     f"→ `{d.get('monitoring_page', '')}`\n")
    return Block("digests", f"③ 위키 추적 신호 (선별 {len(chosen)}건)", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 블록 ④ 직전 브리핑의 결론만 / 블록 ⑤ 예측 원장
# ─────────────────────────────────────────────────────────────
BRIEF_DIR = REPO / "report" / "briefing"


def build_previous_block(as_of: date, slot: str) -> Block:
    """직전 브리핑의 **결론 섹션만**. 전문을 넣으면 예산이 날아간다
    (리포트 1개가 약 27,000토큰)."""
    if not BRIEF_DIR.exists():
        return Block("previous", "④ 직전 브리핑", "(이전 브리핑 없음 — 첫 발행)")
    files = sorted(BRIEF_DIR.glob("*.md"))
    files = [f for f in files if f.stem[:10] <= as_of.isoformat()]
    if not files:
        return Block("previous", "④ 직전 브리핑", "(이전 브리핑 없음 — 첫 발행)")
    text = files[-1].read_text(encoding="utf-8")
    marker = "## 결론"
    body = text.split(marker, 1)[1].strip() if marker in text else text[-800:]
    body = body[:1200]
    return Block("previous", f"④ 직전 브리핑 결론 ({files[-1].stem})", body)


def build_ledger_block(as_of: date) -> Block:
    from engine.briefing import ledger as L

    resolved = L.resolve_due(as_of)
    open_rows = L.open_predictions(as_of)
    sb = L.scoreboard()

    lines = []
    if resolved:
        lines.append("**오늘 채점된 예측** — 빗나간 게 있으면 왜 틀렸는지 쓰는 게 오늘의 핵심이다.\n")
        for r in resolved:
            mark = {"HIT": "✅", "MISS": "❌", "UNVERIFIABLE": "⚪"}.get(r.status, "?")
            lines.append(f"- {mark} `{r.id}` {r.claim} "
                         f"(기준 {r.check_key} {r.check_op} {r.check_value} / 실측 {r.result or '없음'})")
        lines.append("")
    else:
        lines.append("오늘 검증일이 도래한 예측: 없음\n")

    if open_rows:
        lines.append("**열린 예측**")
        for r in open_rows[:8]:
            lines.append(f"- `{r.id}` ({r.check_date} 검증) {r.claim}")
        lines.append("")

    acc = f"{sb['accuracy']:.0f}%" if sb["accuracy"] is not None else "—"
    lines.append(f"**누적**: 적중 {sb['hit']} / 빗나감 {sb['miss']} / "
                 f"채점불가 {sb['unverifiable']} / 열림 {sb['open']} → 적중률 {acc}")
    return Block("ledger", "⑤ 예측 원장", "\n".join(lines))


# ─────────────────────────────────────────────────────────────
# 게이트 — 조용한 날엔 조용히
# ─────────────────────────────────────────────────────────────
@dataclass
class Gate:
    publish: bool
    reasons: list[str]

    @property
    def verdict(self) -> str:
        return "발행" if self.publish else "조용한 날"


def evaluate_gate(as_of: date, triggers: set[str], why: list[str]) -> Gate:
    """LLM을 부르기 전에 **코드가** 발행 여부를 정한다.

    사용자가 Routine을 정지시킨 이유가 "대충 만드는데 토큰이 아깝다"였다.
    매일 억지로 뭔가 쓰게 하면 내용이 묽어지고 비용만 든다 — 쓸 게 있는
    날에만 쓰는 게 품질과 비용 양쪽에 낫다."""
    from engine.briefing import ledger as L

    reasons = list(why)
    if L.open_predictions(as_of):
        due = [r for r in L.open_predictions(as_of) if r.check_date <= as_of.isoformat()]
        if due:
            reasons.append(f"검증일 도래 예측 {len(due)}건")
    m = _series_map()
    for key, label in (("us_nasdaq", "나스닥"), ("kr_usdkrw", "원/달러")):
        rows = [(d, v) for d, v in m.get(key, []) if d <= as_of.isoformat()]
        if len(rows) >= 2 and rows[-2][1]:
            chg = (rows[-1][1] / rows[-2][1] - 1) * 100
            if abs(chg) >= 1.0:
                reasons.append(f"{label} 1일 {chg:+.2f}%")

    # 자금 조달 CDP 발동 / tranche 실행 기한 도래는 **무조건 발행**이다.
    #
    # 게이트의 원래 기준은 "오늘 시장이 움직였나"인데, CDP 중에는 몇 주에
    # 걸쳐 서서히 이탈하는 것이 있다(예: CDP2 us_10y ≤ 4.0). 그런 날은
    # 나스닥도 환율도 조용해서 게이트가 "조용한 날"로 닫히고, 그러면
    # 블록 ⑧이 통째로 발행되지 않아 경고가 사장님께 도달하지 못한다 —
    # "CDP를 계속 trace한다"가 그 순간 깨진다.
    # 실행 기한(DUE)도 같다. 조용한 날이라고 매도 기한을 놓치면 안 된다.
    try:
        from engine.execution import plan as EP
        est = EP.evaluate(as_of)
        for c in est.fired_cdps:
            reasons.append(f"CDP 발동: {c.id} {c.name}")
        for t in est.tranches:
            if t.state in ("DUE", "ACCELERATED"):
                reasons.append(f"매도 tranche {t.id} {t.state}")
        for c in est.checkpoints:
            if c.status == "MISS":
                reasons.append(f"판단 포스트 이탈: {c.id}")
    except Exception:
        # 실행 계획이 없거나 깨져도 브리핑 자체는 나가야 한다 —
        # 부가 기능이 본체를 막으면 안 된다.
        pass

    # 데이터 헬스 critical 이상도 같은 이유로 무조건 발행이다 — 조용한 날에
    # 하필 macro-series나 하이닉스 시세 수집이 죽으면, 그 사실 자체가
    # "오늘 브리핑에서 가장 중요한 내용"이다. 2026-09-15 사용자 요청
    # ("보고서가 항상 마음에 안들어!")에 대한 직접 대응.
    #
    # ⚠️ 단 `normalized:*`(data_freshness_audit 232개 시리즈 스윕)는
    # 제외한다 — 2026-09-15 최초 점검에서 이미 DEAD 22개가 발견됐는데,
    # 이건 오래전부터 죽어있던 장기 시리즈들이라(예: imf_* 622일 경과)
    # 매일 강제 발행하면 "조용한 날" 개념 자체가 영구히 사라진다. 브리핑이
    # 실제로 의존하는 핵심 소스(macro-series·하이닉스 시세·포트폴리오 등,
    # registry.SOURCES에 개별 등록된 것)만 이 게이트를 강제로 연다 — 그
    # 소스들은 매일 갱신이 정상이라 critical이 뜨는 것 자체가 진짜 이상이다.
    try:
        from engine.health import control
        if control.REPORT_JSON_PATH.exists():
            import json
            snap = json.loads(control.REPORT_JSON_PATH.read_text(encoding="utf-8"))
            crit = [s for s in snap.get("statuses", []) if s["state"] != "OK"
                   and s["severity"] == "critical" and not s["slug"].startswith("normalized:")]
            if crit:
                reasons.append(f"데이터 헬스 critical {len(crit)}건: "
                               + ", ".join(s["slug"] for s in crit[:3]))
    except Exception:
        pass

    return Gate(publish=bool(reasons), reasons=reasons)


# ─────────────────────────────────────────────────────────────
# 조립
# ─────────────────────────────────────────────────────────────
def build_calendar_block(as_of: date, slot: str) -> Block:
    """⑥ 거래 캘린더 — 휴장·시차를 코드가 판정해서 알려준다.

    LLM이 "왜 숫자가 오래됐는지"를 추측하지 않게 한다(R1). WEEKEND
    슬롯에서는 "다음주 예정 일정"이 이 블록을 대체한다(별도 함수)."""
    from engine.briefing import calendar as C

    gap = C.describe_trading_gap(as_of, slot)
    lines = [gap.text]

    # 필수 검색 체크리스트 — 2026-09-14 사고 이후 추가.
    # 그날 AM은 주말 갭을 스스로 알아채고 서두에 쓰기까지 했는데 검색은
    # 금요일 것만 했다. 인지와 행동이 따로 놀았다. 목록을 코드가 박아서
    # 프롬프트가 "전부 소화하라"만 하면 되게 만든다.
    lines.append("\n**🔎 이번 실행 필수 검색 항목** (하나도 빠뜨리지 말 것)")
    for q in C.required_searches(as_of, slot):
        lines.append(f"- {q}")
    lines.append("")
    lines.append("> ⚠️ **이 목록은 프롬프트의 '검색 3~5회면 충분, 과하게 돌지 말 것' "
                 "권장보다 우선한다.** 목록을 전부 소화한 뒤에 횟수를 따져라 — "
                 "8~12회까지는 정상이다.")
    lines.append("> ⚠️ 검색 결과가 없으면 **'미검색'이 아니라 '검색함 → 해당 없음'**으로 "
                 "구분해 적을 것. 안 찾은 것과 찾았는데 없는 것은 다르다.")
    lines.append("> ⚠️ **9체크포인트의 각 칸도 마찬가지다.** 검색하지 않은 칸에 "
                 "'해당 뉴스 없음'이라고 적지 마라 — 2026-09-14에 ③빅테크 CapEx 칸이 "
                 "정확히 그렇게 비어 있었고, 같은 날 코스피를 -3.26% 끌어내린 재료가 "
                 "바로 그 칸에 들어갈 것이었다.")

    events = C.upcoming_events(as_of, horizon_days=5)
    if events:
        lines.append("\n**5일 내 예정된 확정 일정**:")
        for e in events:
            lines.append(f"- {e['date']} {e.get('country', '')} {e['name']}")
    return Block("calendar", "⑥ 거래 캘린더 (휴장·시차)", "\n".join(lines))


def build_weekend_news_block(as_of: date) -> Block:
    """⑥ 주말 뉴스 스윕 — WEEKEND 슬롯 전용.

    2026-09-14 사고의 구조적 원인 중 하나. 주말엔 AM·PM이 돌지 않고,
    WEEKEND 슬롯은 설계상 "다음주 예정 일정" 안내라 **뉴스를 훑지 않았다.**
    그래서 주말에 터진 재료는 월요일 AM이 유일한 포착 지점이었는데,
    그 AM마저 휴장 갭 버그로 "정상 시차" 판정을 받았다 — 이중 공백.

    이 블록이 주말에도 뉴스를 훑게 한다."""
    from engine.briefing import calendar as C

    lines = ["주말엔 AM·PM 브리핑이 돌지 않는다. **주말 사이 터진 재료를 잡는 "
             "유일한 지점이 여기다** — 못 잡으면 월요일 개장 때 가격으로 먼저 만난다.",
             "", "**🔎 필수 검색 항목**"]
    for q in C.required_searches(as_of, "WEEKEND"):
        lines.append(f"- {q}")
    lines.append("- ⚠️ 없으면 **'검색함 → 해당 없음'**으로 적을 것(미검색과 구분).")
    return Block("weekend_news", "⑥ 주말 뉴스 스윕", "\n".join(lines))


def build_weekly_outlook_block(as_of: date) -> Block:
    """⑦ 다음주 예정 일정 — 주말(WEEKEND) 슬롯 전용.

    사용자 요청: "주말 보고서에는 다음주 어떤 일정들이 예정돼 있는지
    미리 알려달라 — 지표 발표 주기, 실적발표, 주요 선거, 지난 보고서에서
    확인된 이슈의 follow up." 이 함수가 그 네 가지를 조립한다."""
    from engine.briefing import calendar as C
    from engine.briefing import ledger as L

    lines = []

    confirmed = C.upcoming_events(as_of, horizon_days=9)
    if confirmed:
        lines.append("**확정 일정**")
        for e in confirmed:
            lines.append(f"- {e['date']} [{e.get('country','')}/{e.get('type','')}] {e['name']}")
            analog = C.historical_analog(e.get("type", ""))
            if analog:
                lines.append(f"  - 📜 과거 유사 사례(패턴 참고용, 확정 아님): {analog['note'].strip()}")
        lines.append("")

    patterns = C.pattern_events()
    if patterns:
        lines.append("**반복 패턴(정확한 날짜는 재확인 필요, 근사치)**")
        for e in patterns:
            lines.append(f"- {e['date']} [{e.get('country','')}] {e['name']} (추정)")
        lines.append("")

    due_next_week = [r for r in L.open_predictions(as_of)
                     if as_of.isoformat() < r.check_date <= (as_of + timedelta(days=9)).isoformat()]
    if due_next_week:
        lines.append("**다음주 검증일 도래 예측 (follow up 대상)**")
        for r in due_next_week:
            lines.append(f"- `{r.id}` ({r.check_date} 검증) {r.claim}")
        lines.append("")

    stale = sorted(
        (d for d in _load_digests()),
        key=lambda d: str(d.get("as_of", "")),
    )[:5]
    if stale:
        lines.append("**가장 오래 안 갱신된 위키 추적 축 (follow up 후보)**")
        for d in stale:
            lines.append(f"- {d.get('status_label', d['slug'])} (판단일 {d.get('as_of', '?')}) "
                        f"→ `{d.get('monitoring_page', '')}`")

    if not lines:
        lines = ["다음주 확정 일정 없음, follow up 대상 없음."]

    return Block("weekly_outlook", "⑦ 다음주 예정 일정 (주간 전망)", "\n".join(lines))


def _fmt_val(v: float | None) -> str:
    """실측값 표기. 지수표기(1.812e+06)는 사람이 못 읽으므로 막는다."""
    if v is None:
        return "값 없음"
    return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:g}"


def build_data_health_block() -> Block:
    """⓪ 데이터 헬스 — 이 브리핑이 딛고 선 데이터 자체가 멀쩡한지.

    사용자 요청(2026-09-15): "데이터 수집 블럭 정상 작동 중인지 센싱하고
    ... feedback이 있는 close-loop system을 만들자. 보고서가 항상 마음에
    안들어!" — 다른 블록이 아무리 정확해도 밑에 깔린 데이터가 죽어있으면
    전부 무의미하다. 그래서 이 블록이 **첫 번째**다.

    engine/health/control.py가 이미 만들어둔 스냅샷(`data/health/
    latest_report.json`)만 읽는다 — 브리핑이 열릴 때마다 58개+232개
    소스를 재검사하면 느리고, 헬스체크는 이미 2시간마다 별도로 돈다."""
    from engine.health import control

    if not control.REPORT_JSON_PATH.exists():
        return Block("data_health", "⓪ 데이터 헬스",
                     "헬스체크 스냅샷 없음 — data-health-check.yml이 아직 한 번도 안 돌았다.")

    import json
    data = json.loads(control.REPORT_JSON_PATH.read_text(encoding="utf-8"))
    statuses = data.get("statuses", [])
    bad = [s for s in statuses if s["state"] != "OK"]
    critical = [s for s in bad if s["severity"] == "critical"]

    lines = [f"점검 시각: {data.get('checked_at', '?')[:16]} "
             f"({len(statuses)}개 소스 중 {len(bad)}개 이상, critical {len(critical)}개)"]
    if critical:
        lines.append("\n🔴 **critical 등급 이상 — 아래 소스에 의존하는 판단은 신뢰하지 말 것**")
        for s in critical[:8]:
            lines.append(f"- **{s['slug']}** — {s['detail']}")
        if len(critical) > 8:
            lines.append(f"- ...외 {len(critical)-8}건, 전체는 data/health/latest_report.md 참고")
    elif bad:
        warn = [s for s in bad if s["severity"] != "critical"]
        lines.append(f"\n🟠 warning 등급 {len(warn)}건 (critical 없음) — "
                     f"{', '.join(s['slug'] for s in warn[:5])}"
                     + (f" 외 {len(warn)-5}건" if len(warn) > 5 else ""))
    else:
        lines.append("✅ 전 소스 정상")

    return Block("data_health", "⓪ 데이터 헬스", "\n".join(lines))


def build_style_directive_block() -> Block:
    """톤 지침 — "사실을 정확히 나열하는 글"과 "전문가 판단을 내리는 글"은
    다른 글이다.

    사용자 피드백(2026-09-16): "경제 전문가의 날카로운 분석이나 전망이
    전혀 없다." 실측해보니 자료·인용·자기검산은 이미 풍부한데, 확신에 찬
    스탠스는 문서 맨 끝 `## 결론`에서만, 그것도 헤지된 관찰 나열로
    나온다 — 8개 섹션을 다 읽어야 판단이 뭔지 나온다.

    Routine 프롬프트는 영구 세션에 묶여 있어 이 세션에서 직접 고칠 수
    없다(2026-08 `update_trigger` 확인 — persistent_session_id 바인딩된
    Routine의 프롬프트 수정은 거부됨). 그래서 다른 블록들과 같은 방식으로
    판 콘텐츠에 지침을 박는다 — 프롬프트가 이미 "여기 없는 숫자는 없는
    것"이라고 팩의 우선권을 인정하고 있으므로, 톤 지침도 같은 자리에서
    작동한다.
    """
    lines = [
        "**이 블록은 프롬프트의 일반적 톤 안내보다 우선한다.**",
        "",
        "1. **H1 제목 바로 다음, 첫 뉴스 섹션 이전에 `## 오늘의 판단` 절을 "
        "새로 쓸 것.** 3~5문장, **1인칭 확신 어조** — \"~일 수 있다/"
        "~로 보인다\" 대신 **\"~다/~로 본다/~로 판단한다\"**로 끝낸다.",
        "2. 이 절은 **문서 맨 끝 `## 결론`의 예고편이 아니라 그 자체로 "
        "완결된 판단**이어야 한다. 오늘 팩의 숫자 2~3개를 근거로 "
        "SK하이닉스·코스피 방향에 대해 **명시적 스탠스**(강세/약세/중립 "
        "중 하나, 며칠 지평인지 명시)를 밝히고, 그 스탠스를 뒤집을 조건 "
        "1개를 바로 다음 문장에 붙인다.",
        "3. **금지어**: 문장을 \"엇갈린다\", \"지켜봐야 한다\", "
        "\"단정하기 이르다\"로 끝내지 말 것. 근거가 얇으면 얇다고 쓰되, "
        "그래도 **오늘 시점 최선의 판단을 숫자로** 먼저 제시하고 헤지는 "
        "그 뒤에 조건절로 붙인다 — 헤지가 문장의 끝이 되면 안 된다.",
        "4. 나머지 섹션(사실관계·표·검산·예측 채점)은 지금처럼 "
        "정확성 우선으로 그대로 쓴다. 이 지침은 **추가**이지 대체가 아니다 "
        "— 사실을 왜곡하거나 확신을 지어내라는 뜻이 아니다.",
    ]
    return Block("style_directive", "톤 지침 (오늘의 판단 요구 — 2026-09-16)", "\n".join(lines))


def build_execution_block(as_of: date) -> Block:
    """⑧ 자금 조달 실행 계획 — 매도 tranche·판단 포스트·CDP 일일 점검.

    사용자 요청: "타임라인별로 어떻게 매도할지 전략을 세우고, 그 주장의
    근거가 실제로 잘 맞아가는지 판단 포스트를 세우고, Critical decision
    point가 발생하는지 계속 trace하는 daily 점검."

    이 블록은 **판정만** 한다 — 자동으로 팔지 않는다. 발동한 CDP는 맨 위로
    올려 LLM이 못 보고 지나치지 못하게 하고, 데이터를 못 구해 판정하지
    못한 CDP도 숨기지 않고 드러낸다(R3: 미수집은 판정이 아니다)."""
    from engine.execution import plan as EP

    try:
        st = EP.evaluate(as_of)
    except FileNotFoundError:
        return Block("execution", "⑧ 자금 조달 실행 계획", "계획 파일 없음 — 점검 생략")

    px = f"{st.price:,.0f}원" if st.price else "가격 미확인"
    lines = [
        f"**진행률 {st.progress_pct:.0f}%** — 목표 {st.target_krw:,}원 중 "
        f"{st.raised_krw:,}원 조달, 잔여 {st.remaining_krw:,}원"
        + (f" (현재가 {px} 기준 **{st.shares_remaining}주**)" if st.shares_remaining else ""),
    ]

    # 사전 경보를 CDP보다도 먼저 — CDP는 "이미 깨진 것", 이건 "곧 깨질 것"이라
    # 아직 손 쓸 시간이 있는 쪽이다. 사장님 요청(2026-09-22): "점검 포인트가
    # 나타나면 알 수 있도록 알람을 주고, 다음 판단 블록이 액션 아이템과
    # 플랜B를 가동해야 한다."
    ew_fired = st.fired_early_warnings
    if ew_fired:
        lines.append("\n🔔 **사전 경보 — 임계가 깨지기 전에 대응할 구간**")
        for w in ew_fired:
            mark = {"critical": "🔴", "warning": "🟠"}.get(w.severity, "⚪")
            esc = f" ⬆️승격({w.escalated_by} 🔴)" if w.escalated_by else ""
            lines.append(f"- {mark} **{w.id} {w.name}**{esc}")
            lines.append(f"  - 실측: {w.detail}")
            if w.linked:
                lines.append(f"  - 연결된 판정: {', '.join(w.linked)}")
            lines.append(f"  - **액션**: {w.action}")
            lines.append(f"  - **플랜B**: {w.plan_b}")
        lines.append("> ⚠️ 이 경보는 **오늘의 판단/결론 섹션에 반드시 반영할 것** — "
                     "블록 안에만 적고 넘어가면 사장님이 못 본다. 액션과 플랜B를 "
                     "그대로 옮기지 말고, 오늘 실측에 비춰 지금 해야 할 일로 "
                     "구체화해서 쓸 것.")
    unknown_ew = [w for w in st.early_warnings if w.fired is None]
    if unknown_ew:
        lines.append("⚠️ **판정 불가 사전경보**(데이터 없음): "
                     + ", ".join(f"{w.id}({w.detail})" for w in unknown_ew))

    # 발동한 CDP를 맨 위에 — 이걸 놓치면 이 블록의 존재 이유가 없다
    fired = st.fired_cdps
    if fired:
        lines.append("\n🚨 **Critical Decision Point 발동**")
        for c in fired:
            mark = {"critical": "🔴", "warning": "🟠", "opportunity": "🟢"}.get(c.severity, "⚪")
            lines.append(f"- {mark} **{c.id} {c.name}** — 실측 {_fmt_val(c.actual)} ({c.expected})")
            lines.append(f"  → {c.action}")
        lines.append("  ⚠️ 자동 실행하지 않는다. 사장님 판단이 필요한 지점이다.")
    else:
        lines.append("\nCDP: 발동 없음 " + ", ".join(
            f"{c.id}({_fmt_val(c.actual)})" for c in st.cdps if c.actual is not None))

    unknown = st.unknown_cdps
    if unknown:
        lines.append("⚠️ **판정 불가 CDP**(데이터 없음, 감시 사각지대): "
                     + ", ".join(f"{c.id} {c.expected}" for c in unknown))

    # 지금 행동이 필요한 tranche
    active = [t for t in st.tranches if t.state in ("OPEN", "DUE", "ACCELERATED")]
    if active:
        lines.append("\n**실행 창이 열린 tranche**")
        for t in active:
            sh = f"{t.shares_needed}주" if t.shares_needed else "주수 미산출"
            lines.append(f"- **{t.id} {t.name}** [{t.state}] {t.amount_krw:,}원 ≈ {sh} "
                         f"({t.window[0]}~{t.window[1]})")
            if t.note:
                lines.append(f"  {t.note}")
    else:
        nxt = next((t for t in st.tranches if t.state == "PENDING"), None)
        if nxt:
            lines.append(f"\n실행 창 없음 — 다음: **{nxt.id} {nxt.name}** "
                         f"({nxt.window[0]} 개시, {nxt.amount_krw:,}원)")

    # 가격 조건은 맞는데 차례가 아니라 대기 중인 tranche를 드러낸다.
    # 안 보여주면 CDP5("급등 — 조기 완료 기회")가 떴는데 열린 tranche는
    # 없는 상황에서 왜 그런지 사람이 알 수 없다.
    waiting = [t for t in st.tranches if t.state == "PENDING" and "앞당김 조건은 충족" in t.note]
    if waiting:
        lines.append("\n**앞당김 대기**(가격 조건 충족, 순서 대기 — 분할 전환 유지)")
        for t in waiting:
            lines.append(f"- {t.id} {t.name} — {t.note}")

    # 판단 포스트 — 채점된 것과 임박한 것
    scored = [c for c in st.checkpoints if c.status in ("HIT", "MISS", "UNKNOWN")]
    if scored:
        lines.append("\n**판단 포스트 채점**")
        for c in scored:
            icon = {"HIT": "✅", "MISS": "❌", "UNKNOWN": "❓"}[c.status]
            act = _fmt_val(c.actual)
            lines.append(f"- {icon} {c.id} ({c.date}) {c.thesis} — 실측 {act} / 기준 {c.expected}")
            if c.status == "MISS" and c.if_false:
                lines.append(f"  → 전제 이탈: {c.if_false}")
    pending = [c for c in st.checkpoints if c.status == "PENDING"]
    if pending:
        n = pending[0]
        d = (date.fromisoformat(n.date) - as_of).days
        lines.append(f"\n다음 판단 포스트: **{n.id}** D-{d} ({n.date}) — {n.thesis}")

    return Block("execution", "⑧ 자금 조달 실행 계획", "\n".join(lines))


def build_bottleneck_block(as_of: date) -> Block:
    """⑨ 병목 이동 추적 — 다음 병목 섹터 선제 매수 단계 판정.

    사용자 요청(2026-09-24): "다음 병목이 확정되기 전에 해당 섹터의
    대장주나 ETF를 매수하는 전략을 단계별로 구성하여 트레이스를 통해
    전망되는 방향에 따라 단계별 전략이 리포트에서 제안될 수 있도록."
    판정은 engine/bottleneck/rotation.py가 하고 여기선 그대로 싣는다."""
    from engine.bottleneck import rotation as BR

    title = "⑨ 병목 이동 추적 (다음 병목 선제 매수)"
    try:
        st = BR.evaluate(as_of)
    except FileNotFoundError:
        return Block("bottleneck", title, "설정 파일 없음 — 점검 생략")
    body = BR.render_markdown(st)
    if any(c.stage != c.stage_week_ago for c in st.candidates) or any(c.gap_krw > 0 or c.unwind for c in st.candidates):
        body += ("\n> ⚠️ 단계 변화·매수 제안·철회 검토가 있다 — **오늘의 판단/결론 섹션에 "
                 "반드시 반영할 것.** 제안 금액과 수단을 그대로 옮기지 말고, 오늘 시장 "
                 "움직임에 비춰 지금 실행할지(분할 여부 포함)를 판단해서 쓸 것.")
    return Block("bottleneck", title, body)


def build_pack(slot: str, as_of: date | None = None) -> tuple[BriefingPack, Gate]:
    now = datetime.now(KST)
    as_of = as_of or now.date()

    if slot == "WEEKEND":
        # 주말 전망은 "오늘 시장이 움직였나"로 게이트를 걸지 않는다 —
        # 주간 캘린더는 시장이 안 움직여도 매주 유효한 정보다.
        pack = BriefingPack(slot=slot, as_of=now, blocks=[
            build_data_health_block(),
            build_hynix_block(as_of),
            build_digest_block(as_of, *detect_triggers(as_of)),
            build_ledger_block(as_of),
            build_execution_block(as_of),
            build_bottleneck_block(as_of),
            build_weekend_news_block(as_of),
            build_weekly_outlook_block(as_of),
        ])
        return pack, Gate(publish=True, reasons=["주간 전망은 항상 발행"])

    triggers, why = detect_triggers(as_of)
    gate = evaluate_gate(as_of, triggers, why)
    pack = BriefingPack(slot=slot, as_of=now, blocks=[
        build_data_health_block(),
        build_style_directive_block(),
        build_fact_sheet(as_of),
        build_hynix_block(as_of),
        build_digest_block(as_of, triggers, why),
        build_previous_block(as_of, slot),
        build_ledger_block(as_of),
        build_calendar_block(as_of, slot),
        build_execution_block(as_of),
        build_bottleneck_block(as_of),
    ])
    return pack, gate
