import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.wind_classifier import (
    WindClassifier,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


def test_wind_classifier_returns_classification():

    classifier = WindClassifier()

    stem = AudioStem(
        name="wind",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = classifier.classify(stem)

    assert result.family == InstrumentFamily.UNKNOWN
    assert result.classifier_name == "WindClassifier"
    assert result.classifier_version == "0.1"
