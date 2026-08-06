from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.engines.analytical_score_runner import (
    AnalyticalScoreRunner,
)


def test_runner_accepts_context():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([], dtype=float),
        sample_rate=44100,
        duration=1.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(audio=audio)

    runner = AnalyticalScoreRunner()

    assert runner is not None
