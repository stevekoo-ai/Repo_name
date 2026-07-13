"""Data acquisition for the Investment Clock model.

All series are pulled from FRED's public CSV export endpoint
(https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES_ID>), which does
not require an API key. This keeps the pipeline runnable with zero
credentials in GitHub Actions.

If FRED ever requires a key or blocks anonymous CSV pulls, set the
FRED_API_KEY env var and switch USE_FRED_API=1; see fetch_series() below for
the fallback path already wired in.
"""
from __future__ import annotations

import io
import os
from dataclasses import dataclass

import pandas as pd
import requests

FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
FRED_API_URL = "https://api.stlouisfed.org/fred/series/observations"

# Series used by the model. Keep IDs centralized so swapping a proxy is a
# one-line change.
SERIES = {
    "growth_primary": "USALOLITOAASTSAM",  # OECD CLI, US, amplitude adjusted
    "growth_fallback": "INDPRO",  # Industrial Production Index
    "inflation_primary": "CPIAUCSL",  # CPI, all urban consumers, NSA
    "inflation_confirm": "CPILFESL",  # Core CPI (ex food & energy)
    "context_yield_curve": "T10Y2Y",  # 10y-2y treasury spread (context only)
    "context_unemployment": "UNRATE",  # context only
}

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; investment-clock-agent/1.0; "
        "+https://github.com)"
    )
}


@dataclass
class SeriesResult:
    series_id: str
    frame: pd.DataFrame  # columns: date, value


def fetch_series(series_id: str, timeout: int = 20) -> SeriesResult:
    """Fetch one FRED series as a tidy (date, value) DataFrame.

    Tries the anonymous CSV export first. Falls back to the official REST
    API if FRED_API_KEY is set and the CSV pull fails or returns no data.
    """
    frame = _fetch_csv(series_id, timeout)
    if frame is None or frame.empty:
        api_key = os.environ.get("FRED_API_KEY")
        if api_key:
            frame = _fetch_api(series_id, api_key, timeout)
    if frame is None or frame.empty:
        raise RuntimeError(f"Could not fetch FRED series '{series_id}'")
    return SeriesResult(series_id=series_id, frame=frame)


def _fetch_csv(series_id: str, timeout: int) -> pd.DataFrame | None:
    try:
        resp = requests.get(
            FRED_CSV_URL, params={"id": series_id}, headers=_HEADERS, timeout=timeout
        )
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
    except Exception:
        return None
    if df.empty:
        return None
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"]).reset_index(drop=True)


def _fetch_api(series_id: str, api_key: str, timeout: int) -> pd.DataFrame | None:
    try:
        resp = requests.get(
            FRED_API_URL,
            params={
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        obs = resp.json().get("observations", [])
    except Exception:
        return None
    if not obs:
        return None
    df = pd.DataFrame(obs)[["date", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["value"]).reset_index(drop=True)


def fetch_all() -> dict[str, pd.DataFrame]:
    """Fetch every series the model needs, keyed by the logical name in SERIES."""
    out: dict[str, pd.DataFrame] = {}
    for name, series_id in SERIES.items():
        try:
            out[name] = fetch_series(series_id).frame
        except RuntimeError as exc:
            if name in ("growth_primary", "inflation_primary"):
                raise
            print(f"[warn] optional series '{name}' ({series_id}) unavailable: {exc}")
    return out
