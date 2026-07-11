from jga.core.domain.audio_recording import AudioRecording
from jga.core.domain.ensemble_profile import EnsembleProfile
from jga.core.domain.services.ensemble_understanding_engine import (
    EnsembleUnderstandingEngine,
)


class DummyEnsembleUnderstandingEngine(
    EnsembleUnderstandingEngine,
):

    def analyze(
        self,
        recording: AudioRecording,
    ) -> EnsembleProfile:

        return EnsembleProfile(
            meter="4/4",
            estimated_bpm=120.0,
            pulse_start=0.0,
            sound_sources=[],
            musical_functions=[],
            metric_contributors=[],
            confidence=1.0,
        )