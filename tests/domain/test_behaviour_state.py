import pytest

from jga.domain.behaviour_state import BehaviourState
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def trajectory():
    return BehaviourTrajectory()


def test_duration():

    state = BehaviourState(
        trajectory=trajectory(),
        start_index=10,
        end_index=15,
    )

    assert state.duration == 6


def test_single_point_state():

    state = BehaviourState(
        trajectory=trajectory(),
        start_index=4,
        end_index=4,
    )

    assert state.duration == 1


def test_negative_start():

    with pytest.raises(ValueError):
        BehaviourState(
            trajectory=trajectory(),
            start_index=-1,
            end_index=4,
        )


def test_invalid_interval():

    with pytest.raises(ValueError):
        BehaviourState(
            trajectory=trajectory(),
            start_index=8,
            end_index=5,
        )
