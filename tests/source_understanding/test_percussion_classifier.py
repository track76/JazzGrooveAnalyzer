import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.classifiers.percussion_classifier import (
    PercussionClassifier,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


def test_percussion_classifier_returns_classification():

    classifier = PercussionClassifier()

    stem = AudioStem(
        name="drums",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    result = classifier.classify(stem)

    assert result.family == InstrumentFamily.UNKNOWN
    assert result.classifier_name == "PercussionClassifier"
    assert result.classifier_version == "0.1"
