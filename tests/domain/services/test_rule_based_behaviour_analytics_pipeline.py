from datetime import UTC, datetime
from uuid import uuid4

from jga.core.stability_curve import StabilityCurve

from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.services.rule_based_behaviour_analytics_pipeline import (
    RuleBasedBehaviourAnalyticsPipeline,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)


def test_rule_based_behaviour_analytics_pipeline_builds_result():

    observation = make_behaviour_observation()

    profile = BehaviourProfile(
        id=uuid4(),
        observations=(observation,),
        created_at=datetime.now(UTC),
    )

    pipeline = RuleBasedBehaviourAnalyticsPipeline()

    result = pipeline.analyze(
        profile,
        StabilityCurve(),
    )

    assert result is not None
    assert result.descriptor_set is not None
