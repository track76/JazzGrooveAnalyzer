import numpy as np

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.pipeline import (
    SourceUnderstandingPipeline,
)


def test_pipeline_builds_ensemble_profile():

    stems = AudioStemCollection(
        (
            AudioStem(
                name="mix",
                signal=np.zeros(1024),
                sample_rate=44100,
            ),
        )
    )

    pipeline = SourceUnderstandingPipeline()

    result = pipeline.process(stems)

    assert len(result.observed_sources) == 1
    assert result.ensemble_profile.size == 1
