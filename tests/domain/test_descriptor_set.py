from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet


def test_descriptor_set_contains_descriptors():

    descriptor = BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name="temporal_continuity",
        value=0.95,
        provenance="unit-test",
    )

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    assert descriptor_set.size == 1
    assert tuple(descriptor_set) == (descriptor,)
