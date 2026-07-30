from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import InstrumentFamily


def test_instrument_classification_creation():
    classification = InstrumentClassification(
        family=InstrumentFamily.WIND,
        instrument="Tenor Saxophone",
        confidence=0.93,
        classifier_name="DummyClassifier",
        classifier_version="0.1.0",
    )

    assert classification.family is InstrumentFamily.WIND
    assert classification.instrument == "Tenor Saxophone"
    assert classification.confidence == 0.93
    assert classification.classifier_name == "DummyClassifier"
    assert classification.classifier_version == "0.1.0"


def test_instrument_can_be_unknown():
    classification = InstrumentClassification(
        family=InstrumentFamily.UNKNOWN,
        instrument=None,
        confidence=0.0,
        classifier_name="DummyClassifier",
        classifier_version="0.1.0",
    )

    assert classification.instrument is None
