from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.low_spectral_rolloff_rule import (
    LowSpectralRolloffRule,
)


def test_low_rolloff_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_ROLLOFF, 250.0)

    result = LowSpectralRolloffRule(
        threshold=300.0,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_low_rolloff_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.SPECTRAL_ROLLOFF, 600.0)

    result = LowSpectralRolloffRule(
        threshold=300.0,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
