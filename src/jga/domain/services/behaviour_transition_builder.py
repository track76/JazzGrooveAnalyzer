
from __future__ import annotations

from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.domain.behaviour_transition import (
    BehaviourTransition,
)


class BehaviourTransitionBuilder:
    """
    Builds BehaviourTransition objects from an ordered
    sequence of BehaviourStates.

    The builder preserves the temporal ordering already
    established by the state segmentation layer.
    """

    def build(
        self,
        states: tuple[BehaviourState, ...],
    ) -> tuple[BehaviourTransition, ...]:

        if len(states) < 2:
            return ()

        transitions = []

        for index in range(
            len(states) - 1
        ):
            transitions.append(
                BehaviourTransition(
                    source=states[index],
                    target=states[index + 1],
                )
            )

        return tuple(transitions)

