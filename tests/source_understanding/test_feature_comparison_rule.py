from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.comparison_operator import ComparisonOperator
from jga.source_understanding.rules.feature_comparison_rule import (
    FeatureComparisonRule,
)


def test_less_equal_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)

    result = FeatureComparisonRule(
        feature=FeatureName.SPECTRAL_CENTROID,
        operator=ComparisonOperator.LESS_EQUAL,
        threshold=300.0,
    ).evaluate(features)

    assert result.satisfied


def test_less_equal_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 800.0)

    result = FeatureComparisonRule(
        feature=FeatureName.SPECTRAL_CENTROID,
        operator=ComparisonOperator.LESS_EQUAL,
        threshold=300.0,
    ).evaluate(features)

    assert not result.satisfied
