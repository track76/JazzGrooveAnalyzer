from __future__ import annotations

from abc import ABC, abstractmethod

from jga.core.domain.audio_stem import AudioStem
from jga.core.domain.pulse_candidate import PulseCandidate


class PulseCandidateExtractor(ABC):
    """
    Extracts pulse candidates from a single audio stem.
    """

    @abstractmethod
    def extract(
        self,
        stem: AudioStem,
    ) -> tuple[PulseCandidate, ...]:
        ...