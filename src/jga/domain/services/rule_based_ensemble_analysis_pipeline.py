from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)
from jga.domain.sound_source import SoundSource
from jga.domain.services.ensemble_analysis_pipeline import (
    EnsembleAnalysisPipeline,
)
from jga.domain.services.metric_contributor_assignment_service import (
    MetricContributorAssignmentService,
)
from jga.domain.services.musical_function_assignment_service import (
    MusicalFunctionAssignmentService,
)


class RuleBasedEnsembleAnalysisPipeline(
    EnsembleAnalysisPipeline,
):
    """
    Performs semantic ensemble analysis starting from
    already identified Domain sound sources.
    """

    def __init__(
        self,
        function_assigner: MusicalFunctionAssignmentService,
        contributor_assigner: MetricContributorAssignmentService,
    ) -> None:

        self._function_assigner = function_assigner
        self._contributor_assigner = contributor_assigner

    def analyze(
        self,
        sound_sources: tuple[SoundSource, ...],
    ) -> EnsembleAnalysisResult:

        assignment_result = (
            self._function_assigner.assign(
                sound_sources,
            )
        )

        musical_functions = (
            assignment_result.musical_functions
        )

        source_function_assignments = (
            assignment_result.assignments
        )

        metric_contributors = (
            self._contributor_assigner.assign(
                sound_sources,
                assignment_result,
            )
        )

        return EnsembleAnalysisResult(
            sound_sources=sound_sources,
            musical_functions=musical_functions,
            source_function_assignments=(
                source_function_assignments
            ),
            metric_contributors=metric_contributors,
        )
