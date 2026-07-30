import numpy as np

from jga.source_understanding.classifiers.bass_classifier import BassClassifier
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification


def test_bass_classifier_returns_classification():

    classifier = BassClassifier()

    features = FeatureSet()

    features.set(FeatureName.RMS, 0.5)
    features.set(FeatureName.ZERO_CROSSING_RATE, 0.1)
    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 80.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 300.0)
    features.set(FeatureName.DURATION, 1.0)

    result = classifier.classify(features)

    assert isinstance(result, InstrumentClassification)
