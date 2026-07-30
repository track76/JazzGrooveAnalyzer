from jga.source_understanding.classifiers.wind_classifier import WindClassifier
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_wind_classifier_identifies_wind_like_features():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 900.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 600.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 1800.0)
    features.set(FeatureName.DURATION, 3.0)

    result = WindClassifier().classify(features)

    assert result.family is InstrumentFamily.WIND
    assert result.confidence > 0.0
