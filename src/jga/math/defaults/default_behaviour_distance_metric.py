from __future__ import annotations

from jga.domain.behaviour_distance import BehaviourDistance
from jga.domain.behaviour_observation import BehaviourObservation
from jga.math.behaviour_distance_metric import (
    BehaviourDistanceMetric,
)


class DefaultBehaviourDistanceMetric(
    BehaviourDistanceMetric,
):
    """
    Reference implementation.

    Produces the neutral BehaviourDistance used as the
    mathematical baseline for M8.
    """

    def compute(
        self,
        first: BehaviourObservation,
        second: BehaviourObservation,
    ) -> BehaviourDistance:

        return BehaviourDistance(
            physical_distance_ms=0.0,
            metric_distance=0.0,
            normalised_distance=0.0,
            confidence=1.0,
        )
