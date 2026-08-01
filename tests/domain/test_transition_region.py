from unittest.mock import Mock

from jga.domain.behaviour_state import (
    BehaviourState,
)
from jga.domain.behaviour_transition import (
    BehaviourTransition,
)
from jga.domain.transition_region import (
    TransitionRegion,
)


def test_transition_region_exposes_transition_properties():

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

    region = TransitionRegion(
        transition=transition,
    )

    assert region.start_index == 5
    assert region.end_index == 6
    assert region.duration == 2
