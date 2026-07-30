from datetime import datetime
from uuid import uuid4

from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_assign_bass_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="bass",
        description=None,
        created_at=datetime.now(),
    )

    assignments = service.assign((source,))

    assert len(assignments) == 1

    assignment = assignments[0]

    assert isinstance(
        assignment,
        SourceMusicalFunctionAssignment,
    )

    assert assignment.sound_source_id == source.id
    assert assignment.confidence > 0.0
    assert assignment.rationale is not None


def test_assign_unknown_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="accordion",
        family="unknown",
        description=None,
        created_at=datetime.now(),
    )

    assignments = service.assign((source,))

    assert len(assignments) == 1

    assignment = assignments[0]

    assert isinstance(
        assignment,
        SourceMusicalFunctionAssignment,
    )

    assert assignment.confidence > 0.0
