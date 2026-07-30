from jga.source_understanding.classifiers.default_classifier_registry import (
    DefaultClassifierRegistry,
)
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet


def test_registry_classifies_feature_set():

    registry = DefaultClassifierRegistry()

    features = FeatureSet()

    features.set(
        FeatureName.SPECTRAL_CENTROID,
        2000.0,
    )

    features.set(
        FeatureName.SPECTRAL_BANDWIDTH,
        1000.0,
    )

    features.set(
        FeatureName.SPECTRAL_ROLLOFF,
        3000.0,
    )

    features.set(
        FeatureName.ZERO_CROSSING_RATE,
        0.2,
    )

    features.set(
        FeatureName.RMS,
        0.8,
    )

    features.set(
        FeatureName.DURATION,
        0.3,
    )

    result = registry.classify(features)

    assert result is not None
    assert result.confidence >= 0.0
