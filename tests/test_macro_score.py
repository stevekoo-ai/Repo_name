from core.models import DataStatus, IndicatorReading
from engine.macro import score as score_mod


def _reading(name, s, weight=1.0):
    return IndicatorReading(name=name, value=1.0, status=DataStatus.OK, score=s, weight=weight)


def test_compute_scores_raw_and_weighted():
    readings = {
        "a": _reading("a", 1, weight=1.0),
        "b": _reading("b", 1, weight=1.5),
        "c": _reading("c", -1, weight=1.0),
        "d": IndicatorReading(name="d", value=None, status=DataStatus.PENDING, score=None),
    }
    result = score_mod.compute_scores(readings)
    assert result["raw_score"] == 1  # 1 + 1 - 1
    assert result["weighted_score"] == 1.5  # 1*1 + 1*1.5 - 1*1
    assert result["scored_count"] == 3
    assert result["total_count"] == 4
    assert result["coverage_pct"] == 75.0


def test_score_band_boundaries():
    assert score_mod.score_band(10)[0] == "strong_expansion"
    assert score_mod.score_band(7)[0] == "strong_expansion"
    assert score_mod.score_band(5)[0] == "expansion"
    assert score_mod.score_band(2)[0] == "unbalanced_expansion"
    assert score_mod.score_band(0)[0] == "early_slowdown"
    assert score_mod.score_band(-2)[0] == "slowdown"
    assert score_mod.score_band(-7)[0] == "recession_warning"
