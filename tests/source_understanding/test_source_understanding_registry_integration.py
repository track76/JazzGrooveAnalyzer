import numpy as np

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.classifiers.default_classifier_registry import (
    DefaultClassifierRegistry,
)
from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)


def test_source_understanding_service_accepts_classifier_registry():

    stem = AudioStem(
        name="percussion",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    stems = AudioStemCollection((stem,))

    service = SourceUnderstandingService(
        classifier=DefaultClassifierRegistry(),
    )

    observed = service.process(stems)

    assert len(observed) == 1
