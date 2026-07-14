from engine.rule.engine import condition_matches, evaluate_indicator_rule


def test_condition_matches_gte_lte_between():
    assert condition_matches(5, {"gte": 5})
    assert not condition_matches(4.9, {"gte": 5})
    assert condition_matches(5, {"lte": 5})
    assert condition_matches(2, {"between": [0, 3]})
    assert not condition_matches(4, {"between": [0, 3]})


def test_evaluate_indicator_rule_positive_neutral_negative():
    rule_spec = {
        "field": "yoy",
        "positive": {"gte": 10.0},
        "neutral": {"between": [0.0, 10.0]},
        "negative": {"lt": 0.0},
    }
    assert evaluate_indicator_rule("exports", rule_spec, {"yoy": 24.7}).score == 1
    assert evaluate_indicator_rule("exports", rule_spec, {"yoy": 5.0}).score == 0
    assert evaluate_indicator_rule("exports", rule_spec, {"yoy": -2.0}).score == -1


def test_evaluate_indicator_rule_missing_field_is_unclassified():
    rule_spec = {"field": "yoy", "positive": {"gte": 10.0}, "neutral": {"between": [0, 10]}, "negative": {"lt": 0}}
    outcome = evaluate_indicator_rule("exports", rule_spec, {})
    assert outcome.score is None


def test_evaluate_indicator_rule_fallback_field():
    rule_spec = {
        "field": "qoq", "fallback_field": "yoy",
        "positive": {"gte": 3.0}, "neutral": {"between": [0.0, 2.9]}, "negative": {"lt": 0.0},
    }
    outcome = evaluate_indicator_rule("gdp", rule_spec, {"qoq": None, "yoy": 3.5})
    assert outcome.score == 1
    assert outcome.field_used == "yoy"
