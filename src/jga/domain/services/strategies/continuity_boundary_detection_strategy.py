from __future__ import annotations

from jga.domain.boundary_evidence import BoundaryEvidence
from jga.domain.services.boundary_detection_strategy import (
    BoundaryDetectionStrategy,
)
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class ContinuityBoundaryDetectionStrategy(
    BoundaryDetectionStrategy,
):
    """
    First scientific implementation.

    This initial version assumes that the analysed
    BehaviourTrajectory is fully continuous and
    therefore produces no boundaries.

    Subsequent iterations will introduce observable
    continuity analysis.
    """

    def detect(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BoundaryEvidence, ...]:
        return ()
