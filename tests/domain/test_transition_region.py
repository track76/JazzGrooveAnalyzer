from jga.domain.behaviour_state import BehaviourState
from jga.domain.behaviour_transition import BehaviourTransition
from jga.domain.transition_region import TransitionRegion
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def trajectory():
    return BehaviourTrajectory()


def test_transition_region():

    t = trajectory()

    a = BehaviourState(
        trajectory=t,
        start_index=0,
        end_index=4,
    )

    b = BehaviourState(
        trajectory=t,
        start_index=7,
        end_index=10,
    )

    transition = BehaviourTransition(a, b)

    region = TransitionRegion(transition)

    assert region.start_index == 5
    assert region.end_index == 6
    assert region.duration == 2
    assert region.transition is transition
