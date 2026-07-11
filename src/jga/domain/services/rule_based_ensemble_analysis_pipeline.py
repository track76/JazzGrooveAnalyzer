from jga.core.domain.audio_stem import AudioStem
from jga.core.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)
from jga.core.domain.services.ensemble_analysis_pipeline import (
    EnsembleAnalysisPipeline,
)
from jga.core.domain.services.metric_contributor_assignment_service import (
    MetricContributorAssignmentService,
)
from jga.core.domain.services.musical_function_assignment_service import (
    MusicalFunctionAssignmentService,
)
from jga.core.domain.services.source_identification_service import (
    SourceIdentificationService,
)


class RuleBasedEnsembleAnalysisPipeline(
    EnsembleAnalysisPipeline,
):

    def __init__(
        self,
        source_identifier: SourceIdentificationService,
        function_assigner: MusicalFunctionAssignmentService,
        contributor_assigner: MetricContributorAssignmentService,
    ) -> None:

        self._source_identifier = source_identifier
        self._function_assigner = function_assigner
        self._contributor_assigner = contributor_assigner

    def analyze(
        self,
        stems: tuple[AudioStem, ...],
    ) -> EnsembleAnalysisResult:

        sound_sources = self._source_identifier.identify(stems)

        musical_functions = self._function_assigner.assign(
            sound_sources,
        )

        metric_contributors = self._contributor_assigner.assign(
            sound_sources,
            musical_functions,
        )

        return EnsembleAnalysisResult(
            sound_sources=sound_sources,
            musical_functions=musical_functions,
            metric_contributors=metric_contributors,
        )