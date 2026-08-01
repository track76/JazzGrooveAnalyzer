from unittest.mock import Mock

import pytest

from jga.domain.behaviour_state import (
    BehaviourState,
)


def test_negative_start_index_is_rejected():

    with pytest.raises(ValueError):

        BehaviourState(
            trajectory=Mock(),
            start_index=-1,
            end_index=0,
        )


def test_end_before_start_is_rejected():

    with pytest.raises(ValueError):

        BehaviourState(
            trajectory=Mock(),
            start_index=5,
            end_index=4,
        )
