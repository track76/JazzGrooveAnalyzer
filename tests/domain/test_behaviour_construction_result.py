
from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_construction_result import (
    BehaviourConstructionResult,
)


def test_behaviour_construction_result_contract_exists():

    result = BehaviourConstructionResult(
        behaviour_observations=(),
        behaviour_profile=None,
    )

    assert result is not None
    assert result.behaviour_observations == ()
    assert result.behaviour_profile is None
