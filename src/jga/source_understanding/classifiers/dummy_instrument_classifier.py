from __future__ import annotations

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import InstrumentClassification
from jga.source_understanding.instrument_classifier import InstrumentClassifier
from jga.source_understanding.instrument_family import InstrumentFamily


class DummyInstrumentClassifier(InstrumentClassifier):
    def classify(self, features: FeatureSet) -> InstrumentClassification:
        return InstrumentClassification(
            family=InstrumentFamily.UNKNOWN,
            instrument=None,
            confidence=0.0,
            classifier_name=self.__class__.__name__,
            classifier_version="0.1.0",
        )
