from __future__ import annotations

from abc import ABC, abstractmethod

from jga.core.domain.metric_contributor import MetricContributor
from jga.core.domain.musical_function import MusicalFunction
from jga.core.domain.sound_source import SoundSource


class MetricContributorAssignmentService(ABC):
    """
    Determines which sound sources actively contribute
    to the ensemble metric structure.
    """

    @abstractmethod
    def assign(
        self,
        sources: tuple[SoundSource, ...],
        functions: tuple[MusicalFunction, ...],
    ) -> tuple[MetricContributor, ...]:
        ...