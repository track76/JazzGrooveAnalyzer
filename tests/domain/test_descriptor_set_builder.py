from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.descriptor_set_builder import DescriptorSetBuilder


def test_descriptor_set_builder_returns_descriptor_set():

    descriptor = BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name="temporal_continuity",
        value=0.95,
        provenance="unit-test",
    )

    builder = DescriptorSetBuilder()

    result = builder.build((descriptor,))

    assert isinstance(result, DescriptorSet)
    assert result.size == 1
