from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.sound_source import SoundSource
from jga.domain.source_understanding_result import (
    SourceUnderstandingResult,
)


class SourceUnderstandingService(ABC):
    """
    Produces semantic understanding of observed sound sources.

    Input:
        tuple[SoundSource, ...]

    Output:
        SourceUnderstandingResult
    """

    @abstractmethod
    def understand(
        self,
        sound_sources: tuple[SoundSource, ...],
    ) -> SourceUnderstandingResult:
        raise NotImplementedError
