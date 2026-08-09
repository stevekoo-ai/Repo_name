"""SK Hynix historical valuation band — P/E Z-score approximation + ERP.

Why this file exists (2026-08-09): a user-supplied external spec
(Project_SKH_Alpha_Prompt.md, authored by another AI — see
wiki/log.md 2026-08-09) proposed a standalone P/E-band + Equity Risk
Premium quant system fetching fresh data via yfinance/DART. That would
duplicate infrastructure this wiki already has (KIS API price/investor
flow, HBM Cycle Score, market-cycles-leverage-risk, the 4-layer
sk-hynix-investment-thesis decision engine) and risks producing a
second signal that disagrees with the first — the same problem this
wiki already has with 3 independently-run macro regime systems
(G/I/L, Investment Clock, PEOS US/KR) that reach different
conclusions and are deliberately NOT reconciled into one number.

So instead of a new pipeline, this module derives the two genuinely
new indicators (P/E Z-score, ERP) from data the wiki has already
verified, and exposes them for `engine/exporters/sk_hynix_decision.py`
to consume as a new "Layer 0: Valuation Band" gate.

## Why "divergence", not a literal P/E ratio

A literal P/E needs EPS, which needs shares outstanding. SK Hynix's
share count has moved materially in this window (2025 buyback +
cancellation ~2.1% of shares, 2026 ADR listing issuing new shares,
2026 buyback program ~40T KRW / ~2%+ of shares) and this repo has no
verified quarterly share-count series -- fabricating one would violate
the "don't invent numbers" principle documented across this wiki.

concepts/rally-justification-analysis.md already computed and verified
a **divergence gauge** instead:

    divergence(q) = log(price_index(q)) - log(operating_income_index(q))

Both indices are rebased to 24Q1=100, so share count cancels out of
the ratio (it's a fixed unknown constant on both sides in each
quarter, not something that needs to be known). This is a real
valuation-band signal — positive means price is running ahead of
operating income (getting more expensive), negative means the
opposite (getting cheaper) — already reviewed and cited across
multiple wiki pages. Treat this Z-score as **that** signal, not a
true P/E Z-score. It is directionally equivalent but not numerically
identical to a P/E ratio.

## Known limitation

Only 9-10 quarters of history exist (24Q1 onward — the wiki has no
earlier verified quarterly operating-income series). A standard P/E
band uses 5-10 YEARS (20-40 quarters). Treat this Z-score as
low-confidence / directional, not a precision signal, until more
history accumulates.
"""
from __future__ import annotations

import csv
import math
import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FUNDAMENTALS_CSV = REPO_ROOT / "sources" / "sk-hynix-quarterly-fundamentals.csv"
MACRO_SERIES_CSV = REPO_ROOT / "sources" / "macro-series.csv"

# Anchor for the one ERP snapshot this module can currently produce without
# a verified share-count series: the forward P/E already researched and
# cited in concepts/rally-justification-analysis.md ("2026년 선행 PER
# 약 6.8~6.9배", cross-checked against Micron's 10-11x in the same page).
FORWARD_PE_ANCHOR = 6.85
FORWARD_PE_ANCHOR_NOTE = (
    "concepts/rally-justification-analysis.md의 2026년 선행 PER 6.8~6.9배 "
    "실측 조사값(중간값). 발행주식수 미검증으로 이 모듈 자체 계산 아님."
)


@dataclass
class QuarterFundamental:
    quarter: str
    operating_income: float  # KRW billions
    close: float  # KRW


@dataclass
class ValuationBandReading:
    quarters_used: int
    divergence_series: list[tuple[str, float]]  # [(quarter, divergence), ...]
    latest_quarter: str
    latest_divergence: float
    mean_divergence: float
    std_divergence: float
    pe_zscore: float | None  # None if std is 0 or insufficient data
    band_label: str  # 저평가 / 중립 / 고평가
    erp_pct: float | None  # None if us_10y not yet collected
    erp_note: str
    caveats: list[str]


def _read_fundamentals() -> list[QuarterFundamental]:
    if not FUNDAMENTALS_CSV.exists():
        return []
    rows = []
    with FUNDAMENTALS_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(QuarterFundamental(
                quarter=r["quarter"],
                operating_income=float(r["operating_income_krw_bn"]),
                close=float(r["quarter_end_close_krw"]),
            ))
    return rows


def _latest_us_10y() -> float | None:
    """Read the most recent us_10y (FRED DGS10) value from macro-series.csv.
    Returns None if the series hasn't been collected yet (added 2026-08-09,
    first sync happens on the next macro-data-sync.yml run)."""
    if not MACRO_SERIES_CSV.exists():
        return None
    latest_date, latest_val = None, None
    with MACRO_SERIES_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("series") != "us_10y":
                continue
            if latest_date is None or r["date"] > latest_date:
                latest_date, latest_val = r["date"], float(r["value"])
    return latest_val


def compute_divergence_series(rows: list[QuarterFundamental]) -> list[tuple[str, float]]:
    """log10(price_index) - log10(oi_index), both rebased to first row = 100.

    ⚠ Uses log BASE 10, not natural log — verified by reproducing
    concepts/rally-justification-analysis.md's published table exactly
    (e.g. 24Q2: price_idx 129.2, oi_idx 189.3 -> log10(129.2/189.3) =
    -0.166, matching the wiki's published value; natural log gives
    -0.382, which does NOT match). Keep this consistent with that page
    if it's ever revised."""
    if not rows:
        return []
    base_oi = rows[0].operating_income
    base_price = rows[0].close
    out = []
    for r in rows:
        oi_idx = r.operating_income / base_oi * 100
        price_idx = r.close / base_price * 100
        divergence = math.log10(price_idx) - math.log10(oi_idx)
        out.append((r.quarter, divergence))
    return out


def compute_valuation_band() -> ValuationBandReading:
    rows = _read_fundamentals()
    caveats = [
        "P/E Z-score는 실제 P/E가 아니라 이격도(divergence = log 주가지수 - "
        "log 영업이익지수) 기반 근사 — 발행주식수 시계열 미검증으로 EPS 직접 "
        "계산 안 함(자사주 소각·ADR 신주발행으로 최근 2년간 주식수 변동 있었음).",
        f"샘플 {len(rows)}개 분기뿐 — 표준 밸류에이션 밴드(5~10년, 20~40분기) "
        "대비 부족, 방향성 참고용.",
    ]

    if len(rows) < 3:
        return ValuationBandReading(
            quarters_used=len(rows), divergence_series=[], latest_quarter="",
            latest_divergence=0.0, mean_divergence=0.0, std_divergence=0.0,
            pe_zscore=None, band_label="데이터 부족",
            erp_pct=None, erp_note="분기 데이터 3개 미만", caveats=caveats,
        )

    series = compute_divergence_series(rows)
    values = [v for _, v in series]
    mean_d = sum(values) / len(values)
    variance = sum((v - mean_d) ** 2 for v in values) / len(values)
    std_d = math.sqrt(variance)

    latest_q, latest_d = series[-1]
    pe_zscore = (latest_d - mean_d) / std_d if std_d > 0 else None

    if pe_zscore is None:
        band_label = "판정불가(표준편차 0)"
    elif pe_zscore <= -1.5:
        band_label = "저평가(Strong Buy Zone)"
    elif pe_zscore >= 1.5:
        band_label = "고평가(Sell Zone)"
    else:
        band_label = "중립"

    us_10y = _latest_us_10y()
    if us_10y is not None:
        earnings_yield = 1.0 / FORWARD_PE_ANCHOR * 100  # %
        erp_pct = earnings_yield - us_10y
        erp_note = (
            f"Earnings Yield {earnings_yield:.2f}%(선행PER {FORWARD_PE_ANCHOR}배 앵커) "
            f"- 미국10Y {us_10y:.2f}% = ERP {erp_pct:.2f}%p. "
            "⚠ 원화자산에 달러 무위험금리를 쓰는 방법론적 한계 있음(사용자 스펙 원안 "
            "그대로 채택 — 글로벌 반도체 밸류에이션 비교 관행)."
        )
    else:
        erp_pct = None
        erp_note = (
            "us_10y(FRED DGS10) 시리즈가 아직 수집되지 않음 — "
            "scripts/macro_data.py PRESETS에 2026-08-09 추가, "
            "macro-data-sync.yml 다음 실행(매일 07:10 KST)부터 자동 수집."
        )

    return ValuationBandReading(
        quarters_used=len(rows),
        divergence_series=series,
        latest_quarter=latest_q,
        latest_divergence=latest_d,
        mean_divergence=mean_d,
        std_divergence=std_d,
        pe_zscore=pe_zscore,
        band_label=band_label,
        erp_pct=erp_pct,
        erp_note=erp_note,
        caveats=caveats,
    )


if __name__ == "__main__":
    reading = compute_valuation_band()
    print(f"분기 수: {reading.quarters_used}")
    print(f"최신 분기: {reading.latest_quarter}, 이격도: {reading.latest_divergence:.4f}")
    print(f"평균: {reading.mean_divergence:.4f}, 표준편차: {reading.std_divergence:.4f}")
    print(f"P/E Z-score(근사): {reading.pe_zscore}")
    print(f"밴드: {reading.band_label}")
    print(f"ERP: {reading.erp_pct} ({reading.erp_note})")
    for c in reading.caveats:
        print(f"  ⚠ {c}")
