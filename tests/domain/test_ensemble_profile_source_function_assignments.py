from datetime import datetime
from uuid import uuid4

from jga.domain.ensemble_profile import EnsembleProfile
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_ensemble_profile_contains_source_function_assignments():

    assignment = SourceMusicalFunctionAssignment(
        id=uuid4(),
        sound_source_id=uuid4(),
        musical_function_id=uuid4(),
        confidence=0.9,
        rationale="bass provides metric foundation",
        created_at=datetime.now(),
    )

    profile = EnsembleProfile(
        meter="4/4",
        estimated_bpm=120.0,
        pulse_start=0.0,
        sound_sources=(),
        musical_functions=(),
        source_function_assignments=(assignment,),
        metric_contributors=(),
        confidence=0.9,
    )

    assert len(profile.source_function_assignments) == 1
    assert (
        profile.source_function_assignments[0]
        is assignment
    )
