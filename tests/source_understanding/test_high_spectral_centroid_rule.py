from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.high_spectral_centroid_rule import (
    HighSpectralCentroidRule,
)


def test_high_centroid_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 1200.0)

    result = HighSpectralCentroidRule(
        threshold=1000.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_high_centroid_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 300.0)

    result = HighSpectralCentroidRule(
        threshold=1000.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
