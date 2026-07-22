from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation

from jga.domain.services.identity_descriptor_operator import (
    IdentityDescriptorOperator,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_identity_descriptor_operator():

    relation = DescriptorRelation(
        descriptors=(
            descriptor("A"),
            descriptor("B"),
        ),
    )

    result = IdentityDescriptorOperator().apply(
        (relation,),
    )

    assert result == (relation,)

