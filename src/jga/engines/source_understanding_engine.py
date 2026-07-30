from jga.runtime.analysis_context import AnalysisContext

from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)
from jga.source_understanding.services.ensemble_profile_builder import (
    EnsembleProfileBuilder,
)


class SourceUnderstandingEngine:

    def __init__(self):
        self._service = SourceUnderstandingService()
        self._builder = EnsembleProfileBuilder()

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        observed = self._service.process(
            context.audio_stems
        )

        context.observed_sources = observed

        context.ensemble_profile = (
            self._builder.build(observed)
        )

        return context
