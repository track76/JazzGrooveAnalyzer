
from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.null_separator import NullSeparator


def make_context():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([0.1, 0.2, 0.3]),
        sample_rate=44100,
        duration=1.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(
        audio=audio
    )

    context.processed_audio = np.array(
        [0.1, 0.2, 0.3]
    )

    return context


def test_separator_creates_audio_stem_collection():

    context = make_context()

    result = NullSeparator().process(
        context
    )

    assert result.audio_stems is not None

    assert len(result.audio_stems) == 1

    stem = result.audio_stems[0]

    assert stem.name == "Mix"

    assert stem.sample_rate == 44100

    assert stem.source == "NullSeparator"

    assert np.array_equal(
        stem.signal,
        context.processed_audio,
    )
