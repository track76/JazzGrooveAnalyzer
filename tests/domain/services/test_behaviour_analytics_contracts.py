from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.descriptor_set_builder import (
    DescriptorSetBuilder,
)
from jga.domain.services.default_descriptor_algebra import (
    DefaultDescriptorAlgebra,
)
from jga.domain.services.behaviour_analytics_builder import (
    BehaviourAnalyticsBuilder,
)


def _descriptor(name: str) -> BehaviourDescriptor:
    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_descriptor_set_builder_preserves_cardinality():

    descriptors = (
        _descriptor("A"),
        _descriptor("B"),
        _descriptor("C"),
    )

    descriptor_set = DescriptorSetBuilder().build(
        descriptors
    )

    assert descriptor_set.size == 3


def test_descriptor_set_builder_preserves_identity():

    descriptors = (
        _descriptor("A"),
        _descriptor("B"),
    )

    descriptor_set = DescriptorSetBuilder().build(
        descriptors
    )

    assert descriptor_set.descriptors is descriptors


def test_default_descriptor_algebra_preserves_provenance():

    descriptor_set = DescriptorSetBuilder().build(
        (
            _descriptor("A"),
        )
    )

    analytical = DefaultDescriptorAlgebra().analyze(
        descriptor_set
    )

    assert (
        analytical.source_descriptor_set
        is descriptor_set
    )


def test_behaviour_analytics_builder_preserves_traceability():

    descriptor_set = DescriptorSetBuilder().build(
        (
            _descriptor("A"),
        )
    )

    result = BehaviourAnalyticsBuilder().build(
        descriptor_set
    )

    assert result.descriptor_set is descriptor_set

    assert (
        result.analytical_structure.source_descriptor_set
        is descriptor_set
    )
