from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext


def test_analysis_context_validation_dataset_defaults_to_none():
    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([], dtype=float),
        sample_rate=44100,
        duration=0.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(audio=audio)

    assert context.validation_dataset is None
