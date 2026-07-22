from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.services.behaviour_analytics_builder import (
    BehaviourAnalyticsBuilder,
)
from jga.domain.services.descriptor_set_builder import (
    DescriptorSetBuilder,
)


def _descriptor(name: str) -> BehaviourDescriptor:

    return BehaviourDescriptor(
        id=uuid4(),
        created_at=datetime.now(UTC),
        name=name,
        value=1.0,
        provenance="pytest",
    )


def test_descriptor_set_preserved():

    descriptor_set = DescriptorSetBuilder().build(
        (
            _descriptor("A"),
            _descriptor("B"),
        )
    )

    result = BehaviourAnalyticsBuilder().build(
        descriptor_set
    )

    assert result.descriptor_set is descriptor_set


def test_analytical_structure_exists():

    descriptor_set = DescriptorSetBuilder().build(
        (
            _descriptor("A"),
        )
    )

    result = BehaviourAnalyticsBuilder().build(
        descriptor_set
    )

    assert result.analytical_structure is not None


def test_descriptor_content_preserved():

    descriptor_set = DescriptorSetBuilder().build(
        (
            _descriptor("A"),
            _descriptor("B"),
        )
    )

    result = BehaviourAnalyticsBuilder().build(
        descriptor_set
    )

    assert (
        result.analytical_structure.source_descriptor_set.descriptors
        ==
        descriptor_set.descriptors
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
        result.analytical_structure.source_descriptor_set.descriptors
        ==
        descriptor_set.descriptors
    )

