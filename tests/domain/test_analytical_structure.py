from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet


def test_analytical_structure_preserves_descriptor_provenance():

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

    analytical_structure = AnalyticalStructure(
        source_descriptor_set=descriptor_set,
    )

    assert analytical_structure.source_descriptor_set is descriptor_set
