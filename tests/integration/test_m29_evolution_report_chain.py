
from jga.domain.behaviour_evolution_model import (
    BehaviourEvolutionModel,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)

from jga.domain.services.scientific_report_builder import (
    ScientificReportBuilder,
)


def test_m29_evolution_reaches_scientific_report():

    evolution = BehaviourEvolutionModel(
        trajectory=BehaviourTrajectory()
    )

    analytics_result = BehaviourAnalyticsResult(
        descriptor_set=DescriptorSet(
            descriptors=(),
        ),
        analytical_structure=None,
    )

    report = ScientificReportBuilder().build(
        analytics_result,
        evolution_model=evolution,
    )

    assert report.behaviour_evolution is evolution

