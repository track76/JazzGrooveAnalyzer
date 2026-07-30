import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.voice_classifier import (
    VoiceClassifier,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


def test_voice_classifier_returns_classification():

    classifier = VoiceClassifier()

    stem = AudioStem(
        name="voice",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = classifier.classify(stem)

    assert result.family == InstrumentFamily.UNKNOWN
    assert result.classifier_name == "VoiceClassifier"
    assert result.classifier_version == "0.1"
