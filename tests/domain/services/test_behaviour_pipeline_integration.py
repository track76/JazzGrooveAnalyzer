from jga.core.stability_curve import StabilityCurve

from jga.domain.services.behaviour_observation_builder import (
    BehaviourObservationBuilder,
)
from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)
from jga.domain.services.rule_based_behaviour_analytics_pipeline import (
    RuleBasedBehaviourAnalyticsPipeline,
)

from tests.support.domain_objects import (
    make_internal_metric_timeline,
)


def test_behaviour_pipeline_integration():

    timeline = make_internal_metric_timeline()

    observations = (
        BehaviourObservationBuilder().build(
            timeline,
        )
    )

    profile = (
        BehaviourProfileBuilder().build(
            observations,
        )
    )

    result = (
        RuleBasedBehaviourAnalyticsPipeline().analyze(
            profile,
            StabilityCurve(),
        )
    )

    assert result.descriptor_set is not None
    assert result.analytical_structure is not None
