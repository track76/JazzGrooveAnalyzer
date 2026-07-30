from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function import MusicalFunction
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


class MetricContributorAssignmentService(ABC):
    """
    Determines which sound sources actively contribute
    to the ensemble metric structure.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
        assignments: tuple[
            SourceMusicalFunctionAssignment,
            ...
        ],
        functions: tuple[MusicalFunction, ...],
    ) -> tuple[MetricContributor, ...]:
        ...
