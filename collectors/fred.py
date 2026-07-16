"""FRED collector — keyless CSV endpoint, official REST API as fallback.

Used for US/global Core-10 inputs (NFP, unemployment, CPI comparisons) and
folds in the existing macro-investment-clock series (OECD CLI, CPI,
Treasury spread) as the composite input to the `us_global` Core-10
indicator (Master Instruction 11.4 (10), README fold-in decision).
"""
from __future__ import annotations

import io
import os
from datetime import date

import pandas as pd
import requests

from core import cache as cache_mod
from core.config import api_config, get_api_key
from core.models import DataPoint, DataStatus, Frequency, Metadata
from . import base

FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
FRED_API_URL = "https://api.stlouisfed.org/fred/series/observations"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; peos-agent/1.0; +https://github.com)"}

# Series used to build the US/Global composite (11.4 item 10) and cross-checks.
SERIES = {
    "us_cpi": "CPIAUCSL",
    "us_core_cpi": "CPILFESL",
    "us_unemployment": "UNRATE",
    "us_nonfarm_payroll": "PAYEMS",
    "us_yield_curve_10y2y": "T10Y2Y",
    "us_10y_treasury": "DGS10",      # 10-Year Treasury Constant Maturity Rate
    "us_2y_treasury": "DGS2",        # 2-Year Treasury Constant Maturity Rate
    "us_oecd_cli": "USALOLITOAASTSAM",
    "us_industrial_production": "INDPRO",
    "us_dollar_index": "DTWEXBGS",   # Trade Weighted US Dollar Index: Broad, Goods and Services
    "us_fed_funds_rate": "FEDFUNDS",

    # US Core Macro set (engine/macro/indicators_us.py) — the "big picture"
    # the KR Core-10 is compared against. cpi/unemployment/industrial_production
    # /yield_curve above are reused directly; these four fill the rest.
    "us_gdp_qoq": "A191RL1Q225SBEA",   # Real GDP, % change from preceding period, annualized
    "us_ppi": "PPIACO",                # Producer Price Index by Commodity: All Commodities
    "us_retail_sales": "RSAFS",        # Advance Retail Sales: Retail Trade and Food Services
    "us_trade_balance": "BOPGSTB",     # Trade Balance: Goods and Services, Balance of Payments Basis

    # Korea series mirrored from OECD Main Economic Indicators, used as a
    # fallback when kosis.kr is unreachable (collectors/kosis.py has been
    # observed to intermittently time out from GitHub Actions IPs — see
    # engine/macro/indicators.py's fallback wiring). fred.stlouisfed.org has
    # never failed in any observed run, unlike ECOS/KOSIS, so this is a
    # meaningfully more reliable path when the primary source is down.
    "kr_cpi_oecd": "KORCPIALLMINMEI",              # CPI, total, index (OECD)
    "kr_industrial_production_oecd": "KORPROINDMISMEI",  # Industrial production volume, index (OECD)
    "kr_unemployment_oecd": "LRHUTTTTKRM156S",     # Unemployment rate, %, 15+ (OECD)
    "kr_retail_sales_mom_oecd": "KORSLRTTO01GPSAM",  # Retail trade volume, MoM % change SA (OECD) — already a growth rate, not a level
}


def _fetch_csv(series_id: str, timeout: int = 20) -> pd.DataFrame | None:
    resp = requests.get(FRED_CSV_URL, params={"id": series_id}, headers=_HEADERS, timeout=timeout)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    if df.empty:
        return None
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"]).reset_index(drop=True)


def _fetch_api(series_id: str, api_key: str, timeout: int = 20) -> pd.DataFrame | None:
    resp = requests.get(
        FRED_API_URL,
        params={"series_id": series_id, "api_key": api_key, "file_type": "json"},
        timeout=timeout,
    )
    resp.raise_for_status()
    obs = resp.json().get("observations", [])
    if not obs:
        return None
    df = pd.DataFrame(obs)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"]).reset_index(drop=True)


def fetch_series(series_key: str, ttl_seconds: int | None = None) -> DataPoint:
    """Fetch one named FRED series (see SERIES), cache it, store raw+normalized, return the latest DataPoint."""
    series_id = SERIES[series_key]
    ttl = ttl_seconds or api_config()["cache_ttl_seconds"]["monthly_macro"]

    cached = cache_mod.get(f"fred:{series_id}", ttl)
    if cached is not None:
        df = pd.DataFrame(cached)
        df["date"] = pd.to_datetime(df["date"])
    else:
        df = base.retry(lambda: _fetch_csv(series_id), label=f"fred:{series_id}:csv")
        if df is None or df.empty:
            api_key = get_api_key("fred")
            if api_key:
                df = base.retry(lambda: _fetch_api(series_id, api_key), label=f"fred:{series_id}:api")

        if df is None or df.empty:
            stale = cache_mod.get_stale(f"fred:{series_id}")
            if stale:
                df = pd.DataFrame(stale)
                df["date"] = pd.to_datetime(df["date"])
            else:
                return DataPoint(series_id=series_key, status=DataStatus.SOURCE_ERROR,
                                  note="FRED unreachable and no cache available")
        else:
            cache_mod.set(f"fred:{series_id}", df.assign(date=df["date"].dt.strftime("%Y-%m-%d")).to_dict("records"))

    base.write_raw("fred", series_key, df.tail(24).to_dict("records"))
    rows = [{"date": d.strftime("%Y-%m-%d"), "value": v} for d, v in zip(df["date"], df["value"])]
    base.append_normalized(f"fred_{series_key}", rows)

    latest = df.sort_values("date").iloc[-1]
    metadata = Metadata(
        source="FRED",
        unit="index/percent",
        frequency=Frequency.MONTHLY,
        reliability_grade=5,
        official=True,
        reference_date=latest["date"].date(),
        confidence=90.0,
    )
    return DataPoint(series_id=series_key, status=DataStatus.OK, value=float(latest["value"]), metadata=metadata)


def fetch_all() -> dict[str, DataPoint]:
    return {key: fetch_series(key) for key in SERIES}
