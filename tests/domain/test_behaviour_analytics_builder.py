from datetime import UTC, datetime
from uuid import uuid4

from jga.domain.behaviour_analytics_result import BehaviourAnalyticsResult
from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.behaviour_analytics_builder import BehaviourAnalyticsBuilder


def test_behaviour_analytics_builder_returns_result():

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

    builder = BehaviourAnalyticsBuilder()

    result = builder.build(descriptor_set)

    assert isinstance(result, BehaviourAnalyticsResult)
    assert result.descriptor_set is descriptor_set
