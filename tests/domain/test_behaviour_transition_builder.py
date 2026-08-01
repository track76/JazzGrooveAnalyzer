
from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.domain.behaviour_transition import (
    BehaviourTransition,
)

from jga.domain.services.behaviour_transition_builder import (
    BehaviourTransitionBuilder,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


def test_empty_states_return_no_transitions():

    result = (
        BehaviourTransitionBuilder()
        .build(())
    )

    assert result == ()


def test_two_states_create_one_transition():

    trajectory = BehaviourTrajectory()

    first = BehaviourState(
        trajectory=trajectory,
        start_index=0,
        end_index=2,
    )

    second = BehaviourState(
        trajectory=trajectory,
        start_index=5,
        end_index=8,
    )

    result = (
        BehaviourTransitionBuilder()
        .build(
            (
                first,
                second,
            )
        )
    )

    assert len(result) == 1

    assert isinstance(
        result[0],
        BehaviourTransition,
    )

    assert result[0].source == first
    assert result[0].target == second

