from jga.core.stability_curve import StabilityCurve

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)

from jga.domain.services.behaviour_quantification_builder import (
    BehaviourQuantificationBuilder,
)

from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)


def test_quantification_builder_returns_descriptors():

    profile = BehaviourProfileBuilder().build(
        (
            make_behaviour_observation(),
        )
    )

    context = BehaviourQuantificationContext(
        behaviour_profile=profile,
        stability_curve=StabilityCurve(),
    )

    descriptors = (
        BehaviourQuantificationBuilder().build(context)
    )

    assert len(descriptors) == 4

    assert isinstance(
        descriptors[0],
        BehaviourDescriptor,
    )

    assert descriptors[0].name == "TemporalContinuity"

    assert descriptors[1].name == "BehaviourDensity"

    assert descriptors[2].name == "TemporalPersistence"

    assert descriptors[3].name == "MetricStability"
