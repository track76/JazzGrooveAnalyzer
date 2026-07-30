from abc import ABC
from typing import get_type_hints

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classifier import InstrumentClassifier


def test_classifier_is_abstract():
    assert issubclass(InstrumentClassifier, ABC)


def test_classifier_accepts_feature_set():
    annotations = get_type_hints(InstrumentClassifier.classify)
    assert annotations["features"] is FeatureSet
