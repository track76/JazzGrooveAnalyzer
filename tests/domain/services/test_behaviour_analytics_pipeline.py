from datetime import UTC, datetime
from uuid import uuid4

from tests.support.domain_objects import (
    make_behaviour_observation,
)

from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.services.behaviour_analytics_pipeline import (
    BehaviourAnalyticsPipeline,
)


def test_behaviour_analytics_pipeline_contract_exists():

    observation = make_behaviour_observation()

    profile = BehaviourProfile(
        id=uuid4(),
        observations=(observation,),
        created_at=datetime.now(UTC),
    )

    assert profile is not None
    assert isinstance(
        BehaviourAnalyticsPipeline,
        type,
    )
