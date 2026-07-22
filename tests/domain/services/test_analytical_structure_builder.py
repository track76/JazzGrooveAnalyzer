from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_relation import DescriptorRelation
from jga.domain.services.analytical_structure_builder import (
    AnalyticalStructureBuilder,
)


def descriptor(name: str):

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_analytical_structure_builder():

    relation = DescriptorRelation(
        descriptors=(
            descriptor("A"),
            descriptor("B"),
        ),
    )

    analytical = AnalyticalStructureBuilder().build(
        (relation,),
    )

    assert len(
        analytical.source_descriptor_set.descriptors
    ) == 2

