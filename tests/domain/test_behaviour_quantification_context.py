from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)

from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)

from jga.core.stability_curve import StabilityCurve


def test_behaviour_quantification_context_requires_valid_inputs():

    profile = BehaviourProfileBuilder().build(
        (
            make_behaviour_observation(),
        )
    )

    context = BehaviourQuantificationContext(
        behaviour_profile=profile,
        stability_curve=StabilityCurve(),
    )

    assert context.behaviour_profile == profile
    assert context.stability_curve is not None
