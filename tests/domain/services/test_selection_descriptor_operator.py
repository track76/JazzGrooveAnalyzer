from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation
from jga.domain.services.selection_descriptor_operator import (
    SelectionDescriptorOperator,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_selection_descriptor_operator():

    empty = DescriptorRelation()

    valid = DescriptorRelation(
        descriptors=(
            descriptor("A"),
        ),
    )

    result = SelectionDescriptorOperator().apply(
        (
            empty,
            valid,
        )
    )

    assert len(result) == 1
    assert result[0] is valid
