from jga.source_understanding.classifiers.dummy_instrument_classifier import (
    DummyInstrumentClassifier,
)
from jga.source_understanding.instrument_family import InstrumentFamily


def test_dummy_classifier_returns_unknown_classification():
    classifier = DummyInstrumentClassifier()

    classification = classifier.classify(audio=None)

    assert classification.family is InstrumentFamily.UNKNOWN
    assert classification.instrument is None
    assert classification.confidence == 0.0
    assert classification.classifier_name == "DummyInstrumentClassifier"
