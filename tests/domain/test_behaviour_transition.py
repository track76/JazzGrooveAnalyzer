from unittest.mock import Mock

from jga.domain.behaviour_state import (
    BehaviourState,
)
from jga.domain.behaviour_transition import (
    BehaviourTransition,
)


def test_behaviour_transition_duration():

    trajectory = Mock()

    source = BehaviourState(
        trajectory=trajectory,
        start_index=0,
        end_index=4,
    )

    target = BehaviourState(
        trajectory=trajectory,
        start_index=7,
        end_index=10,
    )

    transition = BehaviourTransition(
        source=source,
        target=target,
    )

    assert transition.duration == 2
