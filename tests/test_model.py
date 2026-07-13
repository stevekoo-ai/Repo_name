import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from clock.model import compute_growth_signal, compute_inflation_signal, read_clock  # noqa: E402


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
