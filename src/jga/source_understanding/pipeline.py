from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.source_understanding_pipeline_result import (
    SourceUnderstandingPipelineResult,
)
from jga.source_understanding.services.ensemble_profile_builder import (
    EnsembleProfileBuilder,
)
from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)


class SourceUnderstandingPipeline:
    """
    Complete Source Understanding pipeline.

    AudioStemCollection
            │
            ▼
    ObservedSourceCollection
            │
            ▼
    EnsembleProfile
            │
            ▼
    SourceUnderstandingPipelineResult
    """

    def __init__(self) -> None:
        self._service = SourceUnderstandingService()
        self._builder = EnsembleProfileBuilder()

    def process(
        self,
        stems: AudioStemCollection,
    ) -> SourceUnderstandingPipelineResult:

        observed = self._service.process(stems)

        profile = self._builder.build(observed)

        return SourceUnderstandingPipelineResult(
            observed_sources=observed,
            ensemble_profile=profile,
        )
