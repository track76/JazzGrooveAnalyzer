from unittest.mock import Mock

import pytest

from jga.domain.behaviour_state import (
    BehaviourState,
)
from jga.domain.behaviour_transition import (
    BehaviourTransition,
)


def test_overlapping_states_are_rejected():

    trajectory = Mock()

    source = BehaviourState(
        trajectory=trajectory,
        start_index=0,
        end_index=5,
    )

    target = BehaviourState(
        trajectory=trajectory,
        start_index=5,
        end_index=8,
    )

    with pytest.raises(ValueError):

        BehaviourTransition(
            source=source,
            target=target,
        )


def test_target_before_source_is_rejected():

    trajectory = Mock()

    source = BehaviourState(
        trajectory=trajectory,
        start_index=10,
        end_index=12,
    )

    target = BehaviourState(
        trajectory=trajectory,
        start_index=8,
        end_index=9,
    )

    with pytest.raises(ValueError):

        BehaviourTransition(
            source=source,
            target=target,
        )
