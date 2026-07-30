from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.sound_source import SoundSource


class MusicalFunctionAssignmentService(ABC):
    """
    Assigns musical functions to detected sound sources.

    The result preserves both:
    - MusicalFunction definitions;
    - source/function relationships.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
    ) -> MusicalFunctionAssignmentResult:
        ...
