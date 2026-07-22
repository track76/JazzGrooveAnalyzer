from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation

from datetime import UTC, datetime
from uuid import uuid4


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_descriptor_relation():

    d1 = descriptor("A")
    d2 = descriptor("B")

    relation = DescriptorRelation(
        descriptors=(d1, d2),
    )

    assert len(relation.descriptors) == 2

    assert relation.descriptors[0] is d1

    assert relation.descriptors[1] is d2

