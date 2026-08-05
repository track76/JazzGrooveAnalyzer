
from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


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


def test_dummy_multi_stem_separator_creates_multiple_stems():

    context = make_context()

    result = (
        DummyMultiStemSeparator()
        .process(context)
    )

    assert result.audio_stems is not None

    assert len(result.audio_stems) == 4

    names = tuple(
        stem.name
        for stem in result.audio_stems
    )

    assert names == (
        "Double Bass",
        "Piano",
        "Drums",
        "Trumpet",
    )

    for stem in result.audio_stems:

        assert stem.sample_rate == 44100

        assert (
            stem.source
            == "DummyMultiStemSeparator"
        )

        assert stem.confidence == 0.5

        assert np.array_equal(
            stem.signal,
            context.processed_audio,
        )
