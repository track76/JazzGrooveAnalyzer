from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.boundary_evidence import BoundaryEvidence
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class BoundaryDetector(ABC):
    """
    Detects observable behavioural discontinuities
    along one BehaviourTrajectory.
    """

    @abstractmethod
    def detect(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BoundaryEvidence, ...]:
        """
        Detect validated boundary evidence.

        Returned evidence must

        - preserve temporal ordering
        - be reproducible
        - be derived exclusively from observable data
        """
        raise NotImplementedError
