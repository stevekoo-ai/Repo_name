import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from clock.model import build_full_history, compute_growth_signal, compute_inflation_signal, read_clock  # noqa: E402


def _monthly_series(values: list[float], start: str = "2023-01-01") -> pd.DataFrame:
    dates = pd.date_range(start=start, periods=len(values), freq="MS")
    return pd.DataFrame({"date": dates, "value": values})


def _series_for(growth_rising: bool, inflation_rising: bool) -> dict[str, pd.DataFrame]:
    # 16 months of growth data; last 3-month change controls the signal.
    growth_vals = [100.0] * 13 + ([100, 101, 102] if growth_rising else [100, 99, 98])
    growth = _monthly_series(growth_vals)

    # CPI level series long enough for YoY (13 months) + 3-month momentum on YoY (needs 16 months).
    base_cpi = 100.0
    cpi_vals = [base_cpi * (1.02 ** (i / 12)) for i in range(16)]
    if inflation_rising:
        cpi_vals[-1] *= 1.01
        cpi_vals[-2] *= 1.005
    else:
        cpi_vals[-1] *= 0.99
        cpi_vals[-2] *= 0.995
    cpi = _monthly_series(cpi_vals)

    return {
        "growth_primary": growth,
        "inflation_primary": cpi,
    }


def test_all_four_quadrants_map_to_expected_phase():
    expected = {
        (True, False): "Recovery",
        (True, True): "Overheat",
        (False, True): "Stagflation",
        (False, False): "Reflation",
    }
    for (growth_rising, inflation_rising), phase_name in expected.items():
        series = _series_for(growth_rising, inflation_rising)
        reading = read_clock(series)
        assert reading.phase["name"] == phase_name, (growth_rising, inflation_rising, reading.phase)


def test_growth_signal_uses_3month_momentum():
    series = _series_for(True, True)
    signal = compute_growth_signal(series)
    assert signal.label == "rising"
    assert signal.change > 0


def test_inflation_signal_reflects_yoy_acceleration():
    series = _series_for(True, True)
    signal = compute_inflation_signal(series)
    assert signal.label == "rising"


def test_build_full_history_backfills_every_overlapping_month():
    # 4 years of growth (sinusoidal-ish via cumulative steps) and steadily
    # rising CPI so YoY momentum flips sign partway through.
    n = 48
    dates = pd.date_range("2020-01-01", periods=n, freq="MS")
    growth_vals = [100 + 5 * ((-1) ** (i // 6)) * (i % 6) for i in range(n)]
    growth = pd.DataFrame({"date": dates, "value": growth_vals})

    cpi_vals = [100 * (1.02 ** (i / 12)) * (1 + 0.01 * (i % 5)) for i in range(n)]
    cpi = pd.DataFrame({"date": dates, "value": cpi_vals})

    series = {"growth_primary": growth, "inflation_primary": cpi}
    full = build_full_history(series)

    # Growth needs 3 months lookback, inflation needs 12 (YoY) + 3 (momentum) = 15.
    assert len(full) == n - 15
    assert set(full["phase"].unique()) <= {"Reflation", "Recovery", "Overheat", "Stagflation"}
    assert list(full.columns) == [
        "data_asof", "growth_value", "growth_change_3m", "growth_signal",
        "inflation_yoy", "inflation_change_3m", "inflation_signal",
        "phase", "asset", "core_cpi_yoy", "yield_curve_10y2y", "unemployment_rate",
    ]

    # The last row of the full history must match what read_clock() reports.
    reading = read_clock(series)
    last = full.iloc[-1]
    assert reading.phase["name"] == last["phase"]
    assert reading.growth.value == last["growth_value"]
    assert reading.inflation.value == last["inflation_yoy"]
