from datetime import datetime
from uuid import uuid4

from jga.domain.ensemble_profile import EnsembleProfile
from jga.domain.sound_source import SoundSource
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


class EnsembleUnderstandingService:
    """
    Translates observed sources into domain ensemble context.
    """

    def __init__(
        self,
        assignment_service=None,
    ):
        self._assignment_service = (
            assignment_service
            or RuleBasedMusicalFunctionAssignmentService()
        )

    def analyze(
        self,
        observed: ObservedSourceCollection,
    ) -> EnsembleProfile:

        sound_sources = tuple(
            SoundSource(
                id=uuid4(),
                name=source.stem_id,
                family=source.classification.family.value,
                description=None,
                created_at=datetime.now(),
            )
            for source in observed
        )

        assignment_result = (
            self._assignment_service.assign(
                sound_sources
            )
        )

        return EnsembleProfile(
            meter="4/4",
            estimated_bpm=120.0,
            pulse_start=0.0,
            sound_sources=sound_sources,
            musical_functions=(
                assignment_result.musical_functions
            ),
            source_function_assignments=(
                assignment_result.assignments
            ),
            metric_contributors=(),
            confidence=1.0,
        )
