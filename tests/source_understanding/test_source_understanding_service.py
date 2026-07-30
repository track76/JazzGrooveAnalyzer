import numpy as np

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.classifiers.dummy_instrument_classifier import (
    DummyInstrumentClassifier,
)
from jga.source_understanding.instrument_family import InstrumentFamily
from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)


def test_source_understanding_service_builds_observed_sources():
    stem = AudioStem(
        name="bass",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    stems = AudioStemCollection((stem,))

    service = SourceUnderstandingService(
        classifier=DummyInstrumentClassifier(),
    )

    observed = service.process(stems)

    assert len(observed) == 1
    assert observed[0].stem_id == "bass"
    assert observed[0].classification.family is InstrumentFamily.UNKNOWN
