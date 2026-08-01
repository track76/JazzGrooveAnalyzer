from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)
from jga.domain.descriptor_set import DescriptorSet


def test_create_behaviour_analytics_result():

    descriptor_set = DescriptorSet(
        descriptors=(),
    )

    analytical_structure = AnalyticalStructure(
        source_descriptor_set=descriptor_set,
    )

    result = BehaviourAnalyticsResult(
        descriptor_set=descriptor_set,
        analytical_structure=analytical_structure,
    )

    assert result.descriptor_set is descriptor_set
    assert (
        result.analytical_structure
        is analytical_structure
    )
