from abc import ABC

from jga.source_understanding.instrument_classifier import InstrumentClassifier


def test_instrument_classifier_is_abstract():
    assert issubclass(InstrumentClassifier, ABC)


def test_instrument_classifier_exposes_classify_method():
    assert hasattr(InstrumentClassifier, "classify")
