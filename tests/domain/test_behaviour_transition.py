import pytest

from jga.domain.behaviour_state import BehaviourState
from jga.domain.behaviour_transition import BehaviourTransition
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def trajectory():
    return BehaviourTrajectory()


def test_transition_duration():

    t = trajectory()

    a = BehaviourState(t, 0, 4)
    b = BehaviourState(t, 7, 10)

    transition = BehaviourTransition(a, b)

    assert transition.duration == 2


def test_overlapping_states_not_allowed():

    t = trajectory()

    a = BehaviourState(t, 0, 5)
    b = BehaviourState(t, 5, 8)

    with pytest.raises(ValueError):
        BehaviourTransition(a, b)


def test_reversed_states_not_allowed():

    t = trajectory()

    a = BehaviourState(t, 10, 15)
    b = BehaviourState(t, 4, 8)

    with pytest.raises(ValueError):
        BehaviourTransition(a, b)
