from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.rules.high_rms_rule import HighRMSRule


def test_high_rms_rule_is_satisfied():
    features = FeatureSet()
    features.set(FeatureName.RMS, 0.8)

    result = HighRMSRule(
        threshold=0.5,
    ).evaluate(features)

    assert result.satisfied
    assert result.confidence > 0.0


def test_high_rms_rule_is_not_satisfied():
    features = FeatureSet()
    features.set(FeatureName.RMS, 0.1)

    result = HighRMSRule(
        threshold=0.5,
    ).evaluate(features)

    assert not result.satisfied
    assert result.confidence == 0.0
