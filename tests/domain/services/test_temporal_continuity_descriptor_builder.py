from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.services.temporal_continuity_descriptor_builder import (
    TemporalContinuityDescriptorBuilder,
)

from tests.support.domain_objects import make_behaviour_observation


def test_builder_returns_behaviour_descriptor():
    observation = make_behaviour_observation()

    builder = TemporalContinuityDescriptorBuilder()

    descriptor = builder.build(observation)

    assert isinstance(descriptor, BehaviourDescriptor)
    assert descriptor.name == "TemporalContinuity"
