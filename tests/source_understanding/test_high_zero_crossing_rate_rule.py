from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.high_zero_crossing_rate_rule import (
    HighZeroCrossingRateRule,
)


def test_high_zero_crossing_rate_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.20)

    result = HighZeroCrossingRateRule(
        threshold=0.10,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_high_zero_crossing_rate_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.02)

    result = HighZeroCrossingRateRule(
        threshold=0.10,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
