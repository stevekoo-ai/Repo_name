"""Correlate MOTIE monthly export growth against SK Hynix price and KOSPI.

WHY YoY, NOT LEVELS
────────────────────
The user's claim to check was "수출입동향 수치와 하이닉스 주가, 코스피 주가간에
상관관계를 보인다" — but naively correlating a growth RATE (수출 %YoY) against
a price LEVEL (원화 주가, 지수 포인트) is close to guaranteed to look
"significant" for the wrong reason: both trend upward over a multi-year
uptrend/cycle, so almost any two upward-trending series correlate strongly
without one causing or tracking the other (spurious correlation from a
shared trend). This repo has already paid for treating a coincidence as a
signal once (the fabricated US-KR rate spread published from an 8-year-old
observation) — the fix here is methodological: convert price and the index
to YoY% themselves before correlating, so all four series are the same kind
of quantity (a growth rate) and a high correlation actually means the rates
moved together, not just that both happened to rise.

INPUTS (all real, no estimates)
────────────────────────────────
  data/normalized/motie_total_exports_yoy.csv          (date, value) %YoY
  data/normalized/motie_semiconductor_exports_yoy.csv   (date, value) %YoY
  sources/monthly-price-history.csv                     (date, code, label,
                                                           close, ...) — via
    `python -m scripts.investor_flow monthly-history --code 000660 ...`
    `python -m scripts.investor_flow monthly-history --code 0001 --is-index`
  Price/index YoY% is derived here (close_m / close_{m-12} - 1) * 100 — it is
  not itself a stored series, so a short price history simply yields fewer
  YoY points rather than an error.

OUTPUTS
────────
  monitoring/exports-price-correlation.md   pairwise correlation table + a
                                             stated sample size for every
                                             pair (a correlation without n is
                                             not trustworthy — see 한계 절)
  monitoring/exports-price-correlation.png  the most-correlated pair,
                                             z-score normalized onto one
                                             chart so different units (a
                                             %YoY vs a %YoY) sit on a
                                             comparable scale

Run:
  python -m scripts.correlation_analysis
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
NORMALIZED = REPO_ROOT / "data" / "normalized"
MONTHLY_PRICE_CSV = REPO_ROOT / "sources" / "monthly-price-history.csv"
OUT_DIR = REPO_ROOT / "monitoring"
OUT_MD = OUT_DIR / "exports-price-correlation.md"
OUT_PNG = OUT_DIR / "exports-price-correlation.png"

# 표본이 이보다 적으면 상관계수를 표에는 싣되 "신뢰 불가"로 명시한다 —
# 조용히 숫자만 보여주면 n=3짜리 상관계수도 확신처럼 읽힌다.
MIN_TRUSTWORTHY_N = 6

SERIES_LABELS = {
    "total_exports_yoy": "총수출 (%YoY)",
    "semi_exports_yoy": "반도체수출 (%YoY)",
    "hynix_price_yoy": "SK하이닉스 주가 (%YoY)",
    "kospi_yoy": "코스피 지수 (%YoY)",
}

# matplotlib on a bare ubuntu-latest Actions runner only has DejaVu Sans
# (no CJK glyphs) — Hangul in the PNG renders as missing-glyph boxes. The
# markdown table above doesn't have this problem (plain UTF-8 text, no font
# dependency), so only the chart needs an ASCII fallback.
SERIES_LABELS_CHART = {
    "total_exports_yoy": "Total exports (%YoY)",
    "semi_exports_yoy": "Semiconductor exports (%YoY)",
    "hynix_price_yoy": "SK Hynix price (%YoY)",
    "kospi_yoy": "KOSPI index (%YoY)",
}


def _load_motie(series_id: str) -> pd.Series:
    path = NORMALIZED / f"{series_id}.csv"
    if not path.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["value"].sort_index()


def _load_price_yoy(code: str) -> pd.Series:
    """Monthly close -> %YoY. Requires a close roughly 12 months earlier to
    exist in the same file — with less than a year of KIS history this
    returns an empty series rather than guessing, which is correct: no
    fabricated YoY belongs in a "grade 5 official" comparison."""
    if not MONTHLY_PRICE_CSV.exists():
        return pd.Series(dtype=float)
    df = pd.read_csv(MONTHLY_PRICE_CSV)
    df = df[df["code"].astype(str) == str(code)].copy()
    if df.empty:
        return pd.Series(dtype=float)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    # Normalize each observation onto the first-of-month so it lines up with
    # MOTIE's monthly index regardless of which day-of-month KIS reports.
    df["month"] = df["date"].values.astype("datetime64[M]")
    close = df.set_index("month")["close"]

    yoy = {}
    for month, price in close.items():
        prior_month = month - pd.DateOffset(years=1)
        if prior_month in close.index:
            prior = close.loc[prior_month]
            if prior:
                yoy[month] = (price / prior - 1) * 100
    return pd.Series(yoy, dtype=float).sort_index()


def build_dataset() -> pd.DataFrame:
    series = {
        "total_exports_yoy": _load_motie("motie_total_exports_yoy"),
        "semi_exports_yoy": _load_motie("motie_semiconductor_exports_yoy"),
        "hynix_price_yoy": _load_price_yoy("000660"),
        "kospi_yoy": _load_price_yoy("0001"),
    }
    df = pd.DataFrame(series)
    df.index.name = "month"
    return df


def pairwise_correlations(df: pd.DataFrame) -> list[dict]:
    cols = list(df.columns)
    out = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            pair = df[[a, b]].dropna()
            n = len(pair)
            r = pair[a].corr(pair[b]) if n >= 2 else float("nan")
            out.append({"a": a, "b": b, "r": r, "n": n})
    out.sort(key=lambda row: (row["r"] is not None and not pd.isna(row["r"]), abs(row["r"]) if not pd.isna(row["r"]) else -1), reverse=True)
    return out


def render_markdown(df: pd.DataFrame, pairs: list[dict]) -> str:
    lines = [
        "# 수출입동향 × SK하이닉스 × 코스피 상관관계",
        "",
        f"자동 생성 — `python -m scripts.correlation_analysis` "
        f"(source: data/normalized/motie_*.csv, sources/monthly-price-history.csv)",
        "",
        "모든 값은 %YoY로 통일해 비교했다 — 성장률(수출)과 가격 수준(주가)을",
        "그대로 맞대면 둘 다 장기 우상향이라 원인 없이도 높은 상관계수가",
        "나오기 쉽다(추세 공유로 인한 가짜 상관). 4개 지표를 전부 같은",
        "종류(YoY 증가율)로 바꾼 뒤에야 비교가 의미를 가진다.",
        "",
        "## 표본 데이터",
        "",
        "| 월 | " + " | ".join(SERIES_LABELS.values()) + " |",
        "|---|" + "---|" * len(SERIES_LABELS),
    ]
    # reindex rather than raw column access — a caller (or a test) may pass a
    # frame missing a metric entirely (e.g. no price data collected yet);
    # that should render as "—" for every month, not crash the whole report.
    df_full = df.reindex(columns=list(SERIES_LABELS))
    for month, row in df_full.iterrows():
        cells = [f"{row[c]:.1f}" if pd.notna(row[c]) else "—" for c in SERIES_LABELS]
        lines.append(f"| {month.strftime('%Y-%m')} | " + " | ".join(cells) + " |")

    lines += ["", "## 쌍별 상관계수 (Pearson r, 표본 많은/상관 높은 순)", "",
              "| 지표 A | 지표 B | r | n | 비고 |", "|---|---|---|---|---|"]
    for p in pairs:
        r = p["r"]
        r_str = f"{r:+.2f}" if pd.notna(r) else "계산불가"
        note = "" if pd.isna(r) else ("⚠ n<6 — 표본 부족, 신뢰 불가" if p["n"] < MIN_TRUSTWORTHY_N else "")
        lines.append(f"| {SERIES_LABELS[p['a']]} | {SERIES_LABELS[p['b']]} | {r_str} | {p['n']} | {note} |")

    no_price_data = all(pd.isna(p["r"]) for p in pairs
                         if "hynix_price_yoy" in (p["a"], p["b"]) or "kospi_yoy" in (p["a"], p["b"]))
    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    lines += ["", "## 해석"]
    if no_price_data:
        lines.append(
            "**가격 데이터가 아직 없다** — `sources/monthly-price-history.csv`가 "
            "비어 있어 수출-주가/지수 상관은 전부 계산 불가(n=0). "
            "`python -m scripts.investor_flow monthly-history --code 000660 ...`와 "
            "`--code 0001 --is-index`를 실행해 KIS 월봉을 채운 뒤 이 스크립트를 "
            "다시 돌리면 채워진다. 아래는 그때까지 계산 가능한 두 수출 지표 "
            "간의 참고용 상관일 뿐, 사용자가 물은 '수출-주가 상관관계'가 아니다."
        )
    if trustworthy:
        top = trustworthy[0]
        lines.append(
            f"표본이 {MIN_TRUSTWORTHY_N}개월 이상인 쌍 중 가장 강한 상관: "
            f"**{SERIES_LABELS[top['a']]} ↔ {SERIES_LABELS[top['b']]}** "
            f"(r={top['r']:+.2f}, n={top['n']}). 아래 차트 참고."
        )
    else:
        best = pairs[0] if pairs else None
        if best and pd.notna(best["r"]):
            lines.append(
                f"현재 모든 쌍이 표본 {MIN_TRUSTWORTHY_N}개월 미만이다 — 가장 높은 "
                f"상관(r={best['r']:+.2f}, n={best['n']})조차 결론을 내리기엔 이르다. "
                f"KIS 월봉 이력이 쌓일수록(매월 자동 갱신) n이 늘어나고 신뢰도가 오른다."
            )
        else:
            lines.append("아직 두 지표를 겹쳐볼 수 있는 달이 없다 — 월봉 이력이 더 필요하다.")
    lines.append(
        "\n**한계**: 수출입동향은 4개월분(2026-04~07)뿐이라 표본이 원천적으로 "
        "작다 — 상관계수가 높게 나와도 우연일 가능성을 배제할 수 없다. n이 "
        "10 미만이면 방향성 참고 이상으로 쓰지 말 것."
    )
    return "\n".join(lines) + "\n"


def render_chart(df: pd.DataFrame, top_pair: dict | None) -> None:
    if top_pair is None:
        return
    a, b = top_pair["a"], top_pair["b"]
    pair = df[[a, b]].dropna()
    if pair.empty:
        return
    z = (pair - pair.mean()) / pair.std(ddof=0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(z.index, z[a], marker="o", linewidth=2, color="#2a78d6", label=SERIES_LABELS_CHART[a])
    ax.plot(z.index, z[b], marker="o", linewidth=2, color="#eb6834", label=SERIES_LABELS_CHART[b])
    ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
    ax.set_title(f"{SERIES_LABELS_CHART[a]} vs {SERIES_LABELS_CHART[b]}  (r={top_pair['r']:+.2f}, n={top_pair['n']})")
    ax.set_ylabel("z-score (mean 0, std 1)")
    ax.set_xlabel("month")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)


def main() -> int:
    df = build_dataset()
    if df.dropna(how="all").empty:
        print("입력 데이터가 전혀 없습니다 — motie exports.yaml과 "
              "sources/monthly-price-history.csv를 먼저 채우세요.", file=sys.stderr)
        return 1

    pairs = pairwise_correlations(df)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(df, pairs), encoding="utf-8")

    trustworthy = [p for p in pairs if pd.notna(p["r"]) and p["n"] >= MIN_TRUSTWORTHY_N]
    top_pair = trustworthy[0] if trustworthy else (pairs[0] if pairs and pd.notna(pairs[0]["r"]) else None)
    render_chart(df, top_pair)

    print(f"{len(pairs)}개 쌍 계산 완료 → {OUT_MD}")
    if OUT_PNG.exists():
        print(f"차트 저장 → {OUT_PNG}")
    for p in pairs:
        r_str = f"{p['r']:+.2f}" if pd.notna(p["r"]) else "N/A"
        print(f"  {p['a']:<18} x {p['b']:<18} r={r_str} n={p['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
