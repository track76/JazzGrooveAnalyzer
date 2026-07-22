from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.descriptor_relation_builder import (
    DescriptorRelationBuilder,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_descriptor_relation_builder():

    descriptors = (
        descriptor("A"),
        descriptor("B"),
        descriptor("C"),
    )

    descriptor_set = DescriptorSet(
        descriptors=descriptors,
    )

    relations = DescriptorRelationBuilder().build(
        descriptor_set
    )

    assert len(relations) == 1

    assert relations[0].descriptors == descriptors

