from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.sound_source import SoundSource


class MetricContributorAssignmentService(ABC):
    """
    Determines which sound sources actively contribute
    to the ensemble metric structure.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
        assignment_result: MusicalFunctionAssignmentResult,
    ) -> tuple[MetricContributor, ...]:
        ...
