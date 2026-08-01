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


from jga.domain.behaviour_evolution_model import (
    BehaviourEvolutionModel,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


def test_scientific_report_builder_preserves_behaviour_evolution():

    result = BehaviourAnalyticsResult(
        descriptor_set=DescriptorSet(
            descriptors=(),
        ),
        analytical_structure=None,
    )

    evolution = BehaviourEvolutionModel(
        trajectory=BehaviourTrajectory()
    )

    report = ScientificReportBuilder().build(
        result,
        evolution_model=evolution,
    )

    assert report.behaviour_evolution == evolution

