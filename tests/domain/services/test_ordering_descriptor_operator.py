from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation

from jga.domain.services.ordering_descriptor_operator import (
    OrderingDescriptorOperator,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_ordering_descriptor_operator():

    small = DescriptorRelation(
        descriptors=(
            descriptor("A"),
        ),
    )

    large = DescriptorRelation(
        descriptors=(
            descriptor("A"),
            descriptor("B"),
        ),
    )

    result = OrderingDescriptorOperator().apply(
        (
            large,
            small,
        )
    )

    assert result[0] is small
    assert result[1] is large

