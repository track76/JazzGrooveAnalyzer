from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.ensemble_profile import EnsembleProfile
from jga.source_understanding.services.ensemble_profile_builder import (
    EnsembleProfileBuilder,
)
from jga.source_understanding.services.source_understanding_service import (
    SourceUnderstandingService,
)


class SourceUnderstandingPipeline:
    """
    Complete source understanding pipeline.

    AudioStemCollection
            │
            ▼
    ObservedSourceCollection
            │
            ▼
    EnsembleProfile
    """

    def __init__(self) -> None:
        self._service = SourceUnderstandingService()
        self._builder = EnsembleProfileBuilder()

    def process(
        self,
        stems: AudioStemCollection,
    ) -> EnsembleProfile:

        observed = self._service.process(stems)

        return self._builder.build(observed)
