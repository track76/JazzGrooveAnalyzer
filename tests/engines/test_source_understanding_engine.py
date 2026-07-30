from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.engines.source_understanding_engine import (
    SourceUnderstandingEngine,
)
from jga.runtime.analysis_context import AnalysisContext


def test_source_understanding_engine_updates_context():
    context = AnalysisContext(
        audio=AudioFile(
            path=Path("dummy.wav"),
            raw_audio=np.zeros(1024),
            sample_rate=44100,
            duration=1.0,
            channels=1,
            format="wav",
        )
    )

    context.audio_stems = AudioStemCollection(
        (
            AudioStem(
                name="mix",
                signal=np.zeros(1024),
                sample_rate=44100,
            ),
        )
    )

    engine = SourceUnderstandingEngine()

    engine.process(context)

    assert context.observed_sources is not None
    assert context.ensemble_profile is not None
    assert context.ensemble_profile.size == 1
