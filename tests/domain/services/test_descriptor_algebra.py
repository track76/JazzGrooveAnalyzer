from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.default_descriptor_algebra import (
    DefaultDescriptorAlgebra,
)


def test_descriptor_algebra_returns_analytical_structure():

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

    algebra = DefaultDescriptorAlgebra()

    result = algebra.analyze(descriptor_set)

    assert isinstance(result, AnalyticalStructure)
    assert result.source_descriptor_set is descriptor_set
