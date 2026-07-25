"""Generic YAML-driven rule evaluator (Master Instruction 10).

Rules are never hardcoded in engine code (10.1) — every indicator's
positive/neutral/negative thresholds live in config/rules.yaml (10.2) and
are evaluated here through a small condition grammar:

    { gte: x }            value >= x
    { lte: x }             value <= x
    { gt: x }               value > x
    { lt: x }               value < x
    { between: [lo, hi] }   lo <= value <= hi

Adding a new indicator or domain rule means adding YAML, not touching this
module (24.1/24.2).
"""
from __future__ import annotations

from dataclasses import dataclass

from core.logger import log_event


def condition_matches(value: float, condition: dict) -> bool:
    if "gte" in condition and not value >= condition["gte"]:
        return False
    if "lte" in condition and not value <= condition["lte"]:
        return False
    if "gt" in condition and not value > condition["gt"]:
        return False
    if "lt" in condition and not value < condition["lt"]:
        return False
    if "between" in condition:
        lo, hi = condition["between"]
        if not (lo <= value <= hi):
            return False
    return True


@dataclass
class RuleOutcome:
    score: int | None  # -1 / 0 / +1, or None if unclassified
    matched_band: str | None  # "positive" | "neutral" | "negative" | None
    value_used: float | None
    field_used: str | None


def evaluate_indicator_rule(indicator_key: str, rule_spec: dict, fields: dict[str, float | None]) -> RuleOutcome:
    """Evaluate one Core-10-style rule (10.2 shape) against computed fields.

    `fields` holds the indicator's computed values keyed by field name
    (e.g. {"qoq": 0.9, "yoy": 3.1}); `rule_spec['field']` picks which one to
    score, falling back to `rule_spec['fallback_field']` if the primary is
    missing.
    """
    field = rule_spec.get("field")
    value = fields.get(field) if field else None
    field_used = field
    if value is None and rule_spec.get("fallback_field"):
        field_used = rule_spec["fallback_field"]
        value = fields.get(field_used)

    if value is None:
        log_event("rule.unclassified", level="warning", indicator=indicator_key, reason="no usable field value")
        return RuleOutcome(score=None, matched_band=None, value_used=None, field_used=field_used)

    for band, score in (("positive", 1), ("negative", -1), ("neutral", 0)):
        cond = rule_spec.get(band)
        if cond and condition_matches(value, cond):
            log_event("rule.applied", indicator=indicator_key, band=band, score=score,
                      field=field_used, value=value)
            return RuleOutcome(score=score, matched_band=band, value_used=value, field_used=field_used)

    log_event("rule.unclassified", level="warning", indicator=indicator_key, field=field_used, value=value)
    return RuleOutcome(score=None, matched_band=None, value_used=value, field_used=field_used)
