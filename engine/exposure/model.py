"""Position & Exposure Model — the layer the report was missing.

WHY THIS EXISTS (read before changing anything here)
────────────────────────────────────────────────────
Everything else in this repo answers "what is the economy doing?".
The user's two actual decisions are:

    1. SK하이닉스를 계속 들고 갈 것인가
    2. 집을 언제 살 것인가

Neither of those is a macro question. They are *exposure* questions, and
they are the SAME question — the cash for the house is locked inside the
stock. Until 2026-08-10 the two decision engines
(engine/exporters/sk_hynix_decision.py, real_estate_decision.py) ran side
by side and never exchanged a single value, so the report could be fully
"green" and still not answer either one.

This module computes that missing layer. Three properties matter:

  • It needs NO network. It reads config/portfolio.yaml only. On a day when
    every collector fails (see the 2026-08-10 run: 10/10 KR indicators
    carried forward, US 8/8), THIS SECTION IS STILL VALID. That is the
    point — it is the part of the report that always works.

  • It never invents a price. Market value is computed only for tickers
    with a price in KNOWN_PRICES; everything else is reported at cost
    basis and labelled as such. A missing price is stated, not guessed.

  • It counts *effective* exposure, not just the brokerage line. The user
    works at SK하이닉스, so salary/PS and the IRP/DC balance move with the
    same memory cycle as the shares. And the concentration is sector-wide:
    삼성전자·제주반도체·SOL AI반도체소부장·ACE AI반도체TOP3 are all the
    same bet.

WHAT TO DO NEXT (for whoever picks this up)
───────────────────────────────────────────
The honest gap here is `KNOWN_PRICES`. Wire a real quote source (KIS API —
see wiki/concepts/kis-api-reference.md) and market values become live.
Until then cost-basis numbers are correct and clearly labelled, which is
the right failure mode. Do NOT paper over it by defaulting price to
avg_price silently.

2026-08-27 update — that quote source now exists and is wired in:
sk-hynix-daily-report.yml has been fetching a live KIS price into
sources/sk-hynix-price-snapshot.csv 3x/day since 2026-07-28, but this
module kept reading the one-time hardcoded KNOWN_PRICES value (stuck at the
2026-08-07 snapshot) instead. `_load_live_price()` below reads that CSV's
latest row — still no network call (it's a file this repo already commits
daily), so the "always valid with zero collectors running" property is
unchanged. KNOWN_PRICES stays as the fallback for tickers with no such CSV.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from core.config import portfolio_config, user_profile

REPO_ROOT = Path(__file__).resolve().parents[2]

# Last verified market prices. Each entry MUST carry its observation date and
# source — an undated price is how stale numbers turn into fake precision.
# Anything absent here is reported at cost basis instead.
KNOWN_PRICES: dict[str, dict] = {
    "000660.KS": {
        "price": 1436000,
        "as_of": "2026-08-07",
        "source": "사용자 제보 장중 스냅샷 (종가 아님)",
    },
}

# Buckets that move with the same underlying cycle as the user's employer.
SEMI_SECTORS = {"semiconductor_memory", "semiconductor"}
SEMI_ETF_BUCKETS = {"semiconductor"}

EMPLOYER_TICKER = "000660.KS"

# Tickers with a locally-collected live-price CSV (KIS API via
# sk-hynix-daily-report.yml, 3x/day) — maps to (csv_path, plain ticker value
# used in that CSV's "ticker" column, since the CSV doesn't carry the
# ".KS" suffix config/portfolio.yaml uses). Add an entry here whenever a new
# holding gets a real collector; anything absent falls back to KNOWN_PRICES.
LIVE_PRICE_CSV: dict[str, tuple[Path, str]] = {
    "000660.KS": (REPO_ROOT / "sources" / "sk-hynix-price-snapshot.csv", "000660"),
}


def _load_live_price(ticker: str) -> dict | None:
    """Latest row from the daily-collected KIS snapshot CSV for `ticker`, or
    None. Never raises and never guesses — a missing file, an empty file, or
    a malformed row all just fall through to KNOWN_PRICES (or cost basis),
    same as the "never invent a price" rule above."""
    entry = LIVE_PRICE_CSV.get(ticker)
    if not entry:
        return None
    path, plain_ticker = entry
    if not path.exists():
        return None
    try:
        with path.open(newline="", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r.get("ticker") == plain_ticker]
        if not rows:
            return None
        latest = rows[-1]  # collector upserts one row per date, in date order
        return {
            "price": int(float(latest["price"])),
            "as_of": latest["date"],
            "source": "KIS API 실시간 스냅샷 (sk-hynix-daily-report.yml)",
        }
    except (KeyError, ValueError, OSError):
        return None


@dataclass
class Holding:
    name: str
    ticker: str
    quantity: int
    avg_price: float
    cost: float
    market_value: float | None      # None when no verified price exists
    price_as_of: str | None
    is_semi: bool
    locked_qty: int = 0
    lock_until: str | None = None

    @property
    def valued(self) -> float:
        """Best available value — market when verified, else cost basis."""
        return self.market_value if self.market_value is not None else self.cost

    @property
    def sellable_qty(self) -> int:
        return self.quantity - self.locked_qty


@dataclass
class ExposureModel:
    as_of: str
    holdings: list[Holding]
    cash_krw: float
    retirement_krw: float                # IRP+DC 현금성 잔고만
    retirement_total_krw: float = 0.0     # IRP+DC 전체 평가액(현금성+펀드) — 주택 특별중도인출 후보

    total_cost: float = 0.0
    total_valued: float = 0.0
    priced_coverage_pct: float = 0.0     # % of portfolio with a verified price

    semi_valued: float = 0.0
    semi_pct: float = 0.0
    employer_valued: float = 0.0
    employer_pct: float = 0.0

    locked_valued: float = 0.0
    liquid_valued: float = 0.0
    deployable_cash: float = 0.0         # available RIGHT NOW (cash + liquid stock)

    # 2026-09-02 추가 — 사용자 지적: "부동산 가용 현금에 현재 전세금 포함해야
    # 하는 거 아니냐?". deployable_cash와 의도적으로 분리한다 — 전세보증금은
    # moveout_deadline(계약 만료)이 와야 돌려받는 돈이라 "지금 당장" 쓸 수
    # 있는 현금이 아니다. 다만 다음 집 계약도 통상 그 시점 전후로 이뤄지므로
    # 주택 진입 총 자금 계산에는 포함해야 맞다 — 그래서 별도 필드로 만들어
    # "지금 가용"과 "전세 회수 시점 기준 총 가용"을 구분해서 보여준다.
    jeonse_deposit_krw: float = 0.0
    jeonse_deposit_available_from: str | None = None
    housing_entry_funds_total: float = 0.0   # deployable_cash + jeonse_deposit_krw

    notes: list[str] = field(default_factory=list)


def _semi(sector: str | None, bucket: str | None) -> bool:
    return (sector in SEMI_SECTORS) or (bucket in SEMI_ETF_BUCKETS)


def build_exposure_model() -> ExposureModel:
    cfg = portfolio_config()
    holdings: list[Holding] = []

    for row in (cfg.get("stocks") or []) + (cfg.get("etf") or []):
        ticker = str(row.get("ticker", ""))
        qty = int(row.get("quantity") or 0)
        avg = float(row.get("avg_price") or 0)
        cost = qty * avg

        quote = _load_live_price(ticker) or KNOWN_PRICES.get(ticker)
        mv = qty * quote["price"] if quote else None

        lockups = row.get("lockups") or []
        locked_qty = sum(int(l.get("quantity") or 0) for l in lockups)
        lock_until = next((l.get("lock_until") for l in lockups if l.get("lock_until")), None)

        holdings.append(Holding(
            name=row.get("name") or ticker,
            ticker=ticker,
            quantity=qty,
            avg_price=avg,
            cost=cost,
            market_value=mv,
            price_as_of=quote["as_of"] if quote else None,
            is_semi=_semi(row.get("sector"), row.get("bucket")),
            locked_qty=locked_qty,
            lock_until=lock_until,
        ))

    cash = float((cfg.get("cash") or {}).get("krw") or 0)

    # 2026-09-02 — retirement_krw는 계좌 안의 "현금성 잔고"만이다(투자된 펀드
    # 평가액은 안 셈). retirement_total_krw는 IRP/DC 계좌 전체 평가액(현금성 +
    # 보유 펀드 평가액 전부)이다 — 사용자 지적: "ISA계좌와 IRP 그리고 DC계좌도
    # 주택 마련에 사용될 수 있다" — 소득세법 시행령상 무주택자의 주택구입·
    # 전세자금 목적 중도인출이 IRP/DC 둘 다 허용 사유에 해당하므로, 현금성
    # 잔고만이 아니라 계좌 전체가 주택 자금 후보다(단, 일반 매도와 달리
    # 사유 증빙이 필요한 특별 중도인출 — housing_entry_funds_total에서
    # 별도로 표시한다).
    retirement = 0.0
    retirement_total = 0.0
    for acct in (cfg.get("retirement_accounts") or {}).values():
        if isinstance(acct, dict):
            cash_like = float(acct.get("cash_like_balance_krw") or 0)
            retirement += cash_like
            holdings_value = sum(float(h.get("valuation_krw") or 0) for h in (acct.get("holdings") or []))
            retirement_total += cash_like + holdings_value

    m = ExposureModel(
        as_of=date.today().isoformat(),
        holdings=holdings,
        cash_krw=cash,
        retirement_krw=retirement,
    )
    m.retirement_total_krw = retirement_total

    m.total_cost = sum(h.cost for h in holdings)
    m.total_valued = sum(h.valued for h in holdings)
    priced = sum(h.valued for h in holdings if h.market_value is not None)
    m.priced_coverage_pct = (priced / m.total_valued * 100) if m.total_valued else 0.0

    m.semi_valued = sum(h.valued for h in holdings if h.is_semi)
    m.semi_pct = (m.semi_valued / m.total_valued * 100) if m.total_valued else 0.0

    emp = next((h for h in holdings if h.ticker == EMPLOYER_TICKER), None)
    if emp:
        m.employer_valued = emp.valued
        m.employer_pct = (emp.valued / m.total_valued * 100) if m.total_valued else 0.0
        per_share = emp.valued / emp.quantity if emp.quantity else 0
        m.locked_valued = emp.locked_qty * per_share
        m.liquid_valued = m.total_valued - m.locked_valued
    else:
        m.liquid_valued = m.total_valued

    # THE COUPLING: this is the number the real-estate decision actually
    # depends on and never received.
    m.deployable_cash = m.cash_krw + m.liquid_valued

    # 2026-09-02 추가 — 현재 전세보증금은 지금 당장 가용은 아니지만(계약 만료
    # 시점에 회수), 다음 집 계약도 통상 그 시점 전후로 이뤄지므로 주택 진입
    # 총 자금엔 포함해야 한다. user.yaml에 없으면(사용자가 아직 임대가 아니거나
    # 미입력) 0으로 조용히 빠진다 — 지어내지 않는다.
    housing = user_profile().get("housing", {})
    m.jeonse_deposit_krw = float(housing.get("current_jeonse_deposit_krw") or 0)
    m.jeonse_deposit_available_from = housing.get("moveout_deadline")
    # retirement_total_krw(IRP+DC 전체 평가액)도 포함 — 소득세법 시행령상
    # 무주택자의 주택구입·전세자금 목적 중도인출이 IRP/DC 둘 다 허용 사유다.
    m.housing_entry_funds_total = m.deployable_cash + m.jeonse_deposit_krw + m.retirement_total_krw

    if m.priced_coverage_pct < 99:
        m.notes.append(
            f"검증된 시세가 있는 자산은 평가액의 {m.priced_coverage_pct:.0f}%뿐 — "
            f"나머지는 매수원가 기준입니다. 시세 연동(KIS API) 전까지 비중(%)은 근사치입니다."
        )
    if emp and emp.price_as_of:
        quote = _load_live_price(EMPLOYER_TICKER) or KNOWN_PRICES.get(EMPLOYER_TICKER)
        if quote:
            m.notes.append(
                f"{emp.name} 기준가 {quote['price']:,}원은 {emp.price_as_of} {quote['source']}."
            )
    m.notes.append(
        "급여·성과급(PS)과 퇴직연금이 같은 회사·같은 메모리 사이클에 연동됩니다. "
        "실질 집중도는 아래 지분율보다 높습니다."
    )
    if m.jeonse_deposit_krw:
        m.notes.append(
            f"주택 진입 총 가용({m.housing_entry_funds_total:,.0f}원)에는 현재 거주지 "
            f"전세보증금 {m.jeonse_deposit_krw:,.0f}원이 포함돼 있습니다 — "
            f"{m.jeonse_deposit_available_from or '계약 만료일 미입력'}에 계약이 끝나야 실제로 "
            "회수되는 돈이라 지금 당장 쓸 수 있는 현금은 아닙니다."
        )
    if m.retirement_total_krw:
        m.notes.append(
            f"주택 진입 총 가용에는 IRP·DC 퇴직연금 전체 평가액 {m.retirement_total_krw:,.0f}원도 "
            "포함돼 있습니다 — 무주택자의 주택구입·전세자금 목적 중도인출 사유에 해당하지만, "
            "일반 주식 매도와 달리 사유 증빙·신청 절차가 필요한 특별 인출이라 즉시 현금화되지 않습니다."
        )
    return m
