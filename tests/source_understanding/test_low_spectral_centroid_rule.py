from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.low_spectral_centroid_rule import (
    LowSpectralCentroidRule,
)


def test_low_spectral_centroid_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)

    result = LowSpectralCentroidRule(threshold=300.0).evaluate(features)

    assert result.satisfied
    assert result.confidence == 1.0


def test_low_spectral_centroid_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_CENTROID, 1200.0)

    result = LowSpectralCentroidRule(threshold=300.0).evaluate(features)

    assert not result.satisfied
