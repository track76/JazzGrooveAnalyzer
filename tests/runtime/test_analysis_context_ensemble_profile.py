from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.source_understanding.ensemble_profile import (
    EnsembleProfile,
)


def test_analysis_context_stores_ensemble_profile():

    context = AnalysisContext(
        audio=AudioFile(
            path=Path("dummy.wav"),
            raw_audio=np.zeros(1),
            sample_rate=44100,
            duration=0.0,
            channels=1,
            format="wav",
        ),
    )

    profile = EnsembleProfile(
        families=(),
        confidence=1.0,
    )

    context.ensemble_profile = profile

    assert context.ensemble_profile is profile
