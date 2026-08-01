from jga.domain.services.scientific_report_builder import (
    ScientificReportBuilder,
)

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)


def test_scientific_report_builder():

    result = BehaviourAnalyticsResult(
        descriptor_set=DescriptorSet(
            descriptors=(),
        ),
        analytical_structure=None,
    )

    report = ScientificReportBuilder().build(
        result
    )

    assert report.descriptor_set == (
        result.descriptor_set
    )
