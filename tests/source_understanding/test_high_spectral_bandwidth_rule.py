from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.high_spectral_bandwidth_rule import (
    HighSpectralBandwidthRule,
)


def test_high_bandwidth_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 900.0)

    result = HighSpectralBandwidthRule(
        threshold=500.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_high_bandwidth_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 200.0)

    result = HighSpectralBandwidthRule(
        threshold=500.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
