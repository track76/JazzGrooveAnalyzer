from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.feature_range_rule import (
    FeatureRangeRule,
)


def test_feature_range_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 700.0)

    result = FeatureRangeRule(
        feature=FeatureName.SPECTRAL_CENTROID,
        lower_bound=500.0,
        upper_bound=1000.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_feature_range_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 1500.0)

    result = FeatureRangeRule(
        feature=FeatureName.SPECTRAL_CENTROID,
        lower_bound=500.0,
        upper_bound=1000.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
