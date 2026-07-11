from __future__ import annotations

from abc import ABC, abstractmethod

from jga.core.domain.musical_function import MusicalFunction
from jga.core.domain.sound_source import SoundSource


class MusicalFunctionAssignmentService(ABC):
    """
    Assigns a musical function to each detected sound source.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
    ) -> tuple[MusicalFunction, ...]:
        ...