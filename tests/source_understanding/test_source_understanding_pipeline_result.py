from jga.source_understanding.ensemble_profile import (
    EnsembleProfile,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)
from jga.source_understanding.source_understanding_pipeline_result import (
    SourceUnderstandingPipelineResult,
)


def test_pipeline_result_creation():

    result = SourceUnderstandingPipelineResult(
        observed_sources=ObservedSourceCollection(tuple()),
        ensemble_profile=EnsembleProfile(
            families=tuple(),
            confidence=0.0,
        ),
    )

    assert len(result.observed_sources) == 0
    assert result.ensemble_profile.size == 0
