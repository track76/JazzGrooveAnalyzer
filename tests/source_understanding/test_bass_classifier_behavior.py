from jga.source_understanding.classifiers.bass_classifier import BassClassifier
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_bass_classifier_identifies_bass_like_features():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 250.0)
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.03)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 120.0)
    features.set(FeatureName.RMS, 0.7)
    features.set(FeatureName.DURATION, 2.0)

    result = BassClassifier().classify(features)

    assert result.family is InstrumentFamily.BASS
    assert result.confidence > 0.0
