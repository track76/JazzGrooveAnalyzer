from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


class MusicalFunctionAssignmentService(ABC):
    """
    Assigns musical functions to detected sound sources.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
    ) -> tuple[SourceMusicalFunctionAssignment, ...]:
        ...
