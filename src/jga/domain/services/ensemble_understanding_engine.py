from abc import ABC, abstractmethod

from jga.domain.audio_recording import AudioRecording
from jga.domain.ensemble_profile import EnsembleProfile


class EnsembleUnderstandingEngine(ABC):
    """
    Level A0 engine.

    Produces a complete EnsembleProfile starting
    from an AudioRecording.
    """

    @abstractmethod
    def analyze(
        self,
        recording: AudioRecording,
    ) -> EnsembleProfile:
        ...