from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation

from jga.domain.services.grouping_descriptor_operator import (
    GroupingDescriptorOperator,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_grouping_descriptor_operator():

    d1 = descriptor("A")
    d2 = descriptor("B")
    d3 = descriptor("C")

    relations = (
        DescriptorRelation(
            descriptors=(d1, d2),
        ),
        DescriptorRelation(
            descriptors=(d3,),
        ),
    )

    result = GroupingDescriptorOperator().apply(
        relations,
    )

    assert result == relations

