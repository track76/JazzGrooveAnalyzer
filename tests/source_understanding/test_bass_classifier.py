import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.bass_classifier import (
    BassClassifier,
)

from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


def test_bass_classifier_returns_classification():

    classifier = BassClassifier()

    stem = AudioStem(
        name="bass",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = classifier.classify(stem)

    assert result.family == InstrumentFamily.UNKNOWN
    assert result.classifier_name == "BassClassifier"
    assert result.classifier_version == "0.1"
