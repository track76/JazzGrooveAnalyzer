from unittest.mock import Mock

from jga.domain.behaviour_state import (
    BehaviourState,
)


def test_behaviour_state_duration():

    trajectory = Mock()

    state = BehaviourState(
        trajectory=trajectory,
        start_index=10,
        end_index=14,
    )

    assert state.duration == 5
