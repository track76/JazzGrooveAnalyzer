from jga.source_understanding.classifiers.chordal_classifier import ChordalClassifier
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification


def test_chordal_classifier_returns_classification():
    classifier = ChordalClassifier()

    features = FeatureSet()
    features.set(FeatureName.RMS, 0.5)
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.1)
    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 80.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 300.0)
    features.set(FeatureName.DURATION, 1.0)

    result = classifier.classify(features)

    assert isinstance(result, InstrumentClassification)
