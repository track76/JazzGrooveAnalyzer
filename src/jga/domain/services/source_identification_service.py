from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.audio_stem import AudioStem
from jga.domain.sound_source import SoundSource


class SourceIdentificationService(ABC):
    """
    Transforms observed AudioStems into SoundSources.

    Input:
        tuple[AudioStem, ...]

    Output:
        tuple[SoundSource, ...]
    """

    @abstractmethod
    def identify(
        self,
        audio_stems: tuple[AudioStem, ...],
    ) -> tuple[SoundSource, ...]:
        raise NotImplementedError
