from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_dummy_multi_stem_separator_creates_sources():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([]),
        sample_rate=44100,
        duration=1.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(
        audio=audio,
        processed_audio=np.array([]),
    )

    DummyMultiStemSeparator().process(
        context
    )

    assert len(
        context.audio_stems
    ) == 5
