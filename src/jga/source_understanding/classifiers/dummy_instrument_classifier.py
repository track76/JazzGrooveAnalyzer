from jga.source_understanding.instrument_classifier import (
    InstrumentClassifier,
)
from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import InstrumentFamily


class DummyInstrumentClassifier(InstrumentClassifier):
    """
    Default placeholder classifier.

    Always returns an unknown classification.
    """

    def classify(self, audio) -> InstrumentClassification:
        return InstrumentClassification(
            family=InstrumentFamily.UNKNOWN,
            instrument=None,
            confidence=0.0,
            classifier_name="DummyInstrumentClassifier",
            classifier_version="0.1.0",
        )
