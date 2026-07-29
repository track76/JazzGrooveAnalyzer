from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint

from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)

from jga.domain.services.metric_stability_descriptor_builder import (
    MetricStabilityDescriptorBuilder,
)

from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)


def test_metric_stability_descriptor_uses_stability_curve():

    profile = BehaviourProfileBuilder().build(
        (
            make_behaviour_observation(),
        )
    )

    curve = StabilityCurve(
        points=[
            StabilityPoint(
                time=0.0,
                score=0.8,
                window_size=4,
            ),
            StabilityPoint(
                time=1.0,
                score=1.0,
                window_size=4,
            ),
        ]
    )

    context = BehaviourQuantificationContext(
        behaviour_profile=profile,
        stability_curve=curve,
    )

    descriptor = (
        MetricStabilityDescriptorBuilder()
        .build(context)
    )

    assert descriptor.name == "MetricStability"

    assert descriptor.value == 0.9
