import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.chordal_classifier import (
    ChordalClassifier,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


def test_chordal_classifier_returns_classification():

    classifier = ChordalClassifier()

    stem = AudioStem(
        name="piano",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = classifier.classify(stem)

    assert result.family == InstrumentFamily.UNKNOWN
    assert result.classifier_name == "ChordalClassifier"
    assert result.classifier_version == "0.1"
