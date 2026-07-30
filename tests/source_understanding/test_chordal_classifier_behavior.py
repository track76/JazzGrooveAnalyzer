from jga.source_understanding.classifiers.chordal_classifier import (
    ChordalClassifier,
)
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_chordal_classifier_identifies_chordal_features():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 700.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 500.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 1500.0)
    features.set(FeatureName.DURATION, 4.0)

    result = ChordalClassifier().classify(features)

    assert result.family is InstrumentFamily.CHORDAL
    assert result.confidence > 0.0
