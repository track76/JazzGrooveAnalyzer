from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.short_duration_rule import ShortDurationRule


def test_short_duration_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.DURATION, 0.5)

    result = ShortDurationRule(
        threshold=1.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_short_duration_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.DURATION, 3.0)

    result = ShortDurationRule(
        threshold=1.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
