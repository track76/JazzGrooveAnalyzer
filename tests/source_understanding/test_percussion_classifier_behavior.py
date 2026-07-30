from jga.source_understanding.classifiers.percussion_classifier import (
    PercussionClassifier,
)
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_percussion_classifier_identifies_percussive_features():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 2000.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 1200.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 4000.0)
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.25)
    features.set(FeatureName.RMS, 0.8)
    features.set(FeatureName.DURATION, 0.3)

    result = PercussionClassifier().classify(features)

    assert result.family is InstrumentFamily.PERCUSSION
    assert result.confidence > 0.0
