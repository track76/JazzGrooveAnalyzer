from jga.domain.services.temporal_persistence_descriptor_builder import (
    TemporalPersistenceDescriptorBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_observation,
)


def test_temporal_persistence_descriptor():

    observation = make_behaviour_observation()

    descriptor = (
        TemporalPersistenceDescriptorBuilder()
        .build(observation)
    )

    assert descriptor.name == "TemporalPersistence"

    assert descriptor.value == 1.0
