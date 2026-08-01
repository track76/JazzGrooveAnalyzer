from jga.domain.scientific_report import (
    ScientificReport,
)

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)


class ScientificReportBuilder:
    """
    Builds a ScientificReport by aggregating
    already validated analytical results.

    No recomputation is performed.
    """

    def build(
        self,
        analytics_result: BehaviourAnalyticsResult,
        evolution_model=None,
    ) -> ScientificReport:

        evidence = None

        diagnostic = getattr(
            analytics_result,
            "behaviour_diagnostic_result",
            None,
        )

        if diagnostic is not None:
            evidence = (
                diagnostic.scientific_evidence
            )

        return ScientificReport(
            descriptor_set=(
                analytics_result.descriptor_set
            ),
            analytical_structure=(
                analytics_result.analytical_structure
            ),
            scientific_evidence=evidence,
            behaviour_evolution=evolution_model,
        )
