from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.audio_stem import AudioStem
from jga.domain.sound_source import SoundSource


class SourceIdentificationService(ABC):
    """
    Identifies the musical sound sources contained
    in a collection of separated audio stems.
    """

    @abstractmethod
    def identify(
        self,
        stems: tuple[AudioStem, ...],
    ) -> tuple[SoundSource, ...]:
        """
        Build the corresponding SoundSource objects.
        """
        ...