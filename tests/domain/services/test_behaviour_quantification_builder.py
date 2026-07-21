from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.services.behaviour_quantification_builder import (
    BehaviourQuantificationBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)
from jga.domain.services.behaviour_profile_builder import (
    BehaviourProfileBuilder,
)


def test_quantification_builder_returns_descriptors():

    observation = make_behaviour_observation()

    profile = BehaviourProfileBuilder().build(
        (observation,),
    )

    descriptors = (
        BehaviourQuantificationBuilder().build(profile)
    )

    assert len(descriptors) == 1

    assert isinstance(
        descriptors[0],
        BehaviourDescriptor,
    )

    assert descriptors[0].name == "TemporalContinuity"

    assert descriptors[0].value == 1.0

