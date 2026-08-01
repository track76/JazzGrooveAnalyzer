
from __future__ import annotations

from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


class DefaultBehaviourStateSegmenter:
    """
    Default conservative BehaviourState segmenter.

    Current scientific implementation:
    the complete trajectory is considered
    one coherent behavioural state.

    Future versions will introduce
    scientifically defined transition criteria.
    """

    def segment(
        self,
        trajectory: BehaviourTrajectory,
    ) -> tuple[BehaviourState, ...]:

        if trajectory.is_empty:
            return ()

        return (
            BehaviourState(
                trajectory=trajectory,
                start_index=0,
                end_index=trajectory.point_count - 1,
            ),
        )

