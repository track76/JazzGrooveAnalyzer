from __future__ import annotations

from jga.domain.behaviour_distance import (
    BehaviourDistance,
)

from jga.domain.behaviour_distance_vector import (
    BehaviourDistanceVector,
)


class BehaviourDistanceBuilder:
    """
    Builds BehaviourDistance from a validated
    BehaviourDistanceVector.

    No mathematical aggregation is performed.
    The numerical formulation of distance belongs
    to future specifications.
    """

    def build(
        self,
        vector: BehaviourDistanceVector,
    ) -> BehaviourDistance:

        return BehaviourDistance(
            physical_distance_ms=vector.physical,
            metric_distance=vector.metric,
            normalised_distance=0.0,
            confidence=0.0,
        )
