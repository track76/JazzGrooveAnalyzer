from jga.domain.services.behaviour_density_descriptor_builder import (
    BehaviourDensityDescriptorBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)


def test_behaviour_density_descriptor():

    observation = make_behaviour_observation()

    descriptor = (
        BehaviourDensityDescriptorBuilder()
        .build(observation)
    )

    assert descriptor.name == "BehaviourDensity"

    assert descriptor.value == 1.0
