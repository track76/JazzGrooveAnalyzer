from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.engines.analytical_groove_score_renderer_runner import (
    AnalyticalGrooveScoreRendererRunner,
)


def test_renderer_runner_requires_score():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([], dtype=float),
        sample_rate=44100,
        duration=1.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(
        audio=audio,
    )

    runner = AnalyticalGrooveScoreRendererRunner()

    try:
        runner.render_first_measure(context)
    except ValueError:
        assert True
        return

    assert False
