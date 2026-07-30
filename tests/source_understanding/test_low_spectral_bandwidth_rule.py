from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.low_spectral_bandwidth_rule import (
    LowSpectralBandwidthRule,
)


def test_low_bandwidth_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 180.0)

    result = LowSpectralBandwidthRule(
        threshold=250.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_low_bandwidth_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 600.0)

    result = LowSpectralBandwidthRule(
        threshold=250.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
