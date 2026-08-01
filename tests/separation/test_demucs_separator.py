
from pathlib import Path

import numpy as np
import pytest

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.demucs_separator import (
    DemucsSeparator,
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


def test_demucs_separator_requires_backend():

    context = make_context()

    with pytest.raises(RuntimeError):

        DemucsSeparator().process(
            context
        )
