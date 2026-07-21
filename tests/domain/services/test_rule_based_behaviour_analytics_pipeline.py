from datetime import UTC, datetime
from uuid import uuid4

from tests.support.domain_objects import (
    make_behaviour_observation,
)

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)

from jga.domain.behaviour_profile import (
    BehaviourProfile,
)

from jga.domain.services.rule_based_behaviour_analytics_pipeline import (
    RuleBasedBehaviourAnalyticsPipeline,
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
    )

    assert isinstance(
        result,
        BehaviourAnalyticsResult,
    )

    assert result.analytical_structure is not None
