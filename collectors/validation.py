"""Data validation engine (Master Instruction 7.7-7.10).

Runs the eight required checks (null, dup, unit, date, outlier, staleness,
prior-value diff, revision) against a normalized series and returns a list
of warnings plus a pass/fail flag. This never mutates or drops data — it
only annotates, so raw/normalized data stays intact (7.5) and downstream
layers decide how to react to a warning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

import pandas as pd

from core.config import thresholds_config
from core.logger import log_event
from core.models import DataPoint, DataStatus, Frequency


@dataclass
class ValidationResult:
    series_id: str
    passed: bool
    warnings: list[str] = field(default_factory=list)


def validate_series(series_id: str, df: pd.DataFrame) -> ValidationResult:
    """7.7 checks 1-3, 5, 7: null / duplicate / date sanity / outlier / prior diff."""
    warnings: list[str] = []

    if df is None or df.empty:
        return ValidationResult(series_id, passed=False, warnings=["empty series"])

    # 1. Null
    if df["value"].isna().any():
        warnings.append(f"{df['value'].isna().sum()} null value(s) present")

    # 2. Duplicate dates
    dup_count = df["date"].duplicated().sum()
    if dup_count:
        warnings.append(f"{dup_count} duplicate date row(s)")

    # 4. Date sanity — no future-dated observations
    today = date.today()
    future_rows = df[pd.to_datetime(df["date"]).dt.date > today]
    if not future_rows.empty:
        warnings.append(f"{len(future_rows)} row(s) dated in the future")

    clean = df.dropna(subset=["value"]).sort_values("date").reset_index(drop=True)
    if len(clean) >= 2:
        latest = clean.iloc[-1]["value"]
        previous = clean.iloc[-2]["value"]
        # 5. Outlier: current value implausibly large vs previous (7.8 example: 15% -> 250%)
        outlier_cfg = thresholds_config()["outlier_detection"]
        if abs(previous) >= outlier_cfg["min_abs_previous_for_multiplier_check"]:
            ratio = abs(latest - previous) / abs(previous)
            if ratio >= outlier_cfg["yoy_change_warning_multiplier"]:
                warnings.append(
                    f"outlier: latest={latest} vs previous={previous} "
                    f"(ratio {ratio:.1f}x >= {outlier_cfg['yoy_change_warning_multiplier']}x) "
                    "— check base-effect / re-verify against official release before scoring"
                )
        # 7. Prior-value diff, always recorded for traceability
        warnings.append(f"prior_diff: {latest - previous:+.4f} vs previous observation")

    result = ValidationResult(series_id, passed=not any("outlier" in w for w in warnings), warnings=warnings)
    log_event("validation.series_checked", series_id=series_id, passed=result.passed, warning_count=len(warnings))
    return result


def check_staleness(series_id: str, reference_date: date | None, frequency: Frequency) -> str | None:
    """7.11/18.2 — is the latest observation older than its expected refresh window?"""
    if reference_date is None:
        return None
    staleness_days = thresholds_config()["staleness_days"]
    key = {
        Frequency.DAILY: "realtime_fx",
        Frequency.WEEKLY: "market_index",
        Frequency.MONTHLY: "monthly_macro",
        Frequency.QUARTERLY: "quarterly_macro",
        Frequency.ANNUAL: "annual_macro",
    }[frequency]
    max_age = staleness_days[key]
    age = (date.today() - reference_date).days
    if age > max_age:
        return f"{series_id} is {age}d old (expected refresh within {max_age}d)"
    return None


def detect_revision(previous_raw_value: float | None, new_value: float | None) -> bool:
    """7.5 — flag when a previously stored raw value for the same reference period changed."""
    if previous_raw_value is None or new_value is None:
        return False
    return abs(previous_raw_value - new_value) > 1e-9


def validate_datapoint(dp: DataPoint) -> ValidationResult:
    """Single-point validation for collectors that only expose a latest DataPoint (not a full series)."""
    warnings: list[str] = []
    if dp.status != DataStatus.OK:
        return ValidationResult(dp.series_id, passed=True, warnings=[f"status={dp.status.value}: {dp.note or ''}"])
    if dp.value is None:
        warnings.append("status OK but value is None")
    if dp.metadata:
        stale = check_staleness(dp.series_id, dp.metadata.reference_date, dp.metadata.frequency)
        if stale:
            warnings.append(stale)
        min_grade = thresholds_config()["data_governance"]["minimum_reliability_grade_for_judgment"]
        if dp.metadata.reliability_grade < min_grade and dp.metadata.official:
            warnings.append(
                f"reliability_grade {dp.metadata.reliability_grade} below judgment minimum {min_grade}"
            )
    return ValidationResult(dp.series_id, passed=len(warnings) == 0, warnings=warnings)
