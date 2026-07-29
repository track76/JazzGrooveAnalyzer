from jga.domain.behaviour_state import BehaviourState
from jga.domain.stable_region import StableRegion
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def trajectory():
    return BehaviourTrajectory()


def test_region_exposes_state_interval():

    state = BehaviourState(
        trajectory=trajectory(),
        start_index=12,
        end_index=20,
    )

    region = StableRegion(state)

    assert region.start_index == 12
    assert region.end_index == 20
    assert region.duration == 9
    assert region.state is state
