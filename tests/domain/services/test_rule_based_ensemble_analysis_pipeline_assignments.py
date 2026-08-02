from datetime import datetime
from uuid import uuid4

from jga.domain.services.rule_based_ensemble_analysis_pipeline import (
    RuleBasedEnsembleAnalysisPipeline,
)
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.domain.sound_source import SoundSource


def test_pipeline_returns_source_function_assignments():

    pipeline = RuleBasedEnsembleAnalysisPipeline(
        function_assigner=(
            RuleBasedMusicalFunctionAssignmentService()
        ),
        contributor_assigner=(
            RuleBasedMetricContributorAssignmentService()
        ),
    )

    sound_sources = (
        SoundSource(
            id=uuid4(),
            name="bass",
            family="bass",
            description=None,
            created_at=datetime.now(),
        ),
    )

    result = pipeline.analyze(sound_sources)

    assert len(
        result.source_function_assignments
    ) == 1
