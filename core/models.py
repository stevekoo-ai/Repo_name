"""Shared data models for PEOS.

These are the common currency passed between layers (Collect -> Validate ->
Transform -> Analyze -> Score -> Report -> Recommend, Master Instruction
6.2) so every engine speaks the same shape.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class DataStatus(str, Enum):
    """7.9: missing data is never guessed — it is explicitly tagged."""

    OK = "ok"
    PENDING = "pending"
    NOT_RELEASED = "not_released"
    SOURCE_ERROR = "source_error"


class RevisionStage(str, Enum):
    INITIAL = "initial"
    REVISED = "revised"
    FINAL = "final"


class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


@dataclass
class Metadata:
    """7.6 metadata schema — attached to every data point PEOS stores."""

    source: str
    unit: str
    frequency: Frequency
    reliability_grade: int  # 1-5, see 7.2
    official: bool
    release_date: date | None = None
    reference_date: date | None = None
    last_updated: datetime = field(default_factory=lambda: datetime.utcnow())
    confidence: float = 0.0
    revision_stage: RevisionStage = RevisionStage.INITIAL

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "unit": self.unit,
            "frequency": self.frequency.value,
            "reliability_grade": self.reliability_grade,
            "official": self.official,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "reference_date": self.reference_date.isoformat() if self.reference_date else None,
            "last_updated": self.last_updated.isoformat(),
            "confidence": self.confidence,
            "revision_stage": self.revision_stage.value,
        }


@dataclass
class DataPoint:
    """One observation: a series id, a value (or None if not available), status, metadata."""

    series_id: str
    status: DataStatus
    value: float | None = None
    metadata: Metadata | None = None
    note: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def is_usable(self) -> bool:
        return self.status == DataStatus.OK and self.value is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "status": self.status.value,
            "value": self.value,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "note": self.note,
        }


@dataclass
class TrendPoint:
    """A computed trend over one lookback window (1M/3M/6M/12M/3Y/5Y, 9.3)."""

    window: str  # "1m" | "3m" | "6m" | "12m" | "3y" | "5y"
    change: float | None
    direction: str | None = None  # "up" | "down" | "flat"


@dataclass
class IndicatorReading:
    """A named economic indicator's current value + trend set + rule score."""

    name: str
    value: float | None
    status: DataStatus
    trends: dict[str, TrendPoint] = field(default_factory=dict)
    score: float | None = None  # -1 / 0 / +1 per rule engine
    weight: float = 1.0
    label: str | None = None
    source: str | None = None
    reference_date: date | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def weighted_score(self) -> float:
        if self.score is None:
            return 0.0
        return self.score * self.weight


def score_to_stars(score: float, max_score: float = 100.0) -> str:
    """Convert a 0-100 score to a 1-5 star rating (Master Instruction 14.3)."""
    pct = max(0.0, min(1.0, score / max_score)) * 100
    if pct >= 85:
        return "★★★★★"
    if pct >= 70:
        return "★★★★☆"
    if pct >= 55:
        return "★★★☆☆"
    if pct >= 40:
        return "★★☆☆☆"
    return "★☆☆☆☆"


def action_priority_stars(score: float) -> str:
    """15.4 action-priority star mapping (same bands, distinct semantic use)."""
    return score_to_stars(score)
