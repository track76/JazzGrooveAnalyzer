import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.classifier_registry import (
    ClassifierRegistry,
)

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)

from jga.source_understanding.instrument_classifier import (
    InstrumentClassifier,
)

from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


class LowConfidenceClassifier(InstrumentClassifier):

    def classify(self, stem):
        return InstrumentClassification(
            family=InstrumentFamily.UNKNOWN,
            instrument=None,
            confidence=0.20,
            classifier_name="low",
            classifier_version="1.0",
        )


class HighConfidenceClassifier(InstrumentClassifier):

    def classify(self, stem):
        return InstrumentClassification(
            family=InstrumentFamily.BASS,
            instrument="Double Bass",
            confidence=0.95,
            classifier_name="high",
            classifier_version="1.0",
        )


def test_registry_returns_highest_confidence():

    registry = ClassifierRegistry(
        [
            LowConfidenceClassifier(),
            HighConfidenceClassifier(),
        ]
    )

    stem = AudioStem(
        name="bass",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = registry.classify(stem)

    assert result.family == InstrumentFamily.BASS
    assert result.instrument == "Double Bass"
    assert result.confidence == 0.95
