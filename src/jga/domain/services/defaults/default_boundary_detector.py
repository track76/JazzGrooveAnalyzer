from __future__ import annotations

from jga.domain.boundary_evidence import BoundaryEvidence
from jga.domain.services.boundary_detector import BoundaryDetector
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class DefaultBoundaryDetector(BoundaryDetector):
    """
    Initial implementation.

    Produces no boundaries.

    Scientific detection will be introduced
    incrementally in later iterations.
    """

    def detect(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BoundaryEvidence, ...]:
        return ()
