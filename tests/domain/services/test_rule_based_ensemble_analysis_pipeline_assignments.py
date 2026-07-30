from datetime import datetime
from pathlib import Path
from uuid import uuid4

from jga.domain.audio_stem import AudioStem
from jga.domain.services.rule_based_ensemble_analysis_pipeline import (
    RuleBasedEnsembleAnalysisPipeline,
)
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.domain.services.source_identification_service import (
    SourceIdentificationService,
)
from jga.domain.sound_source import SoundSource


class DummySourceIdentifier(SourceIdentificationService):

    def identify(
        self,
        stems,
    ):
        return (
            SoundSource(
                id=uuid4(),
                name="bass",
                family="bass",
                description=None,
                created_at=datetime.now(),
            ),
        )


def test_pipeline_returns_source_function_assignments():

    pipeline = RuleBasedEnsembleAnalysisPipeline(
        source_identifier=DummySourceIdentifier(),
        function_assigner=(
            RuleBasedMusicalFunctionAssignmentService()
        ),
        contributor_assigner=(
            RuleBasedMetricContributorAssignmentService()
        ),
    )

    result = pipeline.analyze(
        (
            AudioStem(
                id=uuid4(),
                recording_id=uuid4(),
                name="bass",
                audio_path=Path("bass.wav"),
                sample_rate=44100,
                duration=10.0,
                channels=1,
                created_at=datetime.now(),
            ),
        )
    )

    assert len(
        result.source_function_assignments
    ) == 1
