from unittest.mock import Mock

from jga.domain.behaviour_state import (
    BehaviourState,
)
from jga.domain.stable_region import (
    StableRegion,
)


def test_stable_region_exposes_state_properties():

    state = BehaviourState(
        trajectory=Mock(),
        start_index=10,
        end_index=14,
    )

    region = StableRegion(
        state=state,
    )

    assert region.start_index == 10
    assert region.end_index == 14
    assert region.duration == 5
