from __future__ import annotations

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)
from jga.domain.behaviour_state import (
    BehaviourState,
)
from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


class BehaviourStateBuilder:
    """
    Builds BehaviourState objects from contiguous
    BehaviourObservationFrame intervals.

    No scientific interpretation is performed here.
    """

    def build(
        self,
        frames: tuple[
            BehaviourObservationFrame,
            ...
        ],
        start_index: int,
        end_index: int,
    ) -> BehaviourState:

        return BehaviourState(
            trajectory=BehaviourTrajectory(),
            start_index=start_index,
            end_index=end_index,
        )
