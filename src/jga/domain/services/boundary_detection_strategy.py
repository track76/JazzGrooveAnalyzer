from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.boundary_evidence import BoundaryEvidence
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class BoundaryDetectionStrategy(ABC):
    """
    Scientific strategy for detecting behavioural
    discontinuities.
    """

    @abstractmethod
    def detect(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BoundaryEvidence, ...]:
        raise NotImplementedError
