from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.behaviour_analytics_builder import (
    BehaviourAnalyticsBuilder,
)


def test_behaviour_analytics_builder_returns_result():

    builder = BehaviourAnalyticsBuilder()

    descriptor_set = DescriptorSet(
        descriptors=(),
    )

    result = builder.build(
        descriptor_set
    )

    assert result.descriptor_set is descriptor_set
    assert result.analytical_structure is not None
