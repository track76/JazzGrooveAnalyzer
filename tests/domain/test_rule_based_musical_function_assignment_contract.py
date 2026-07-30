from datetime import datetime
from uuid import uuid4

from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)


def test_rule_based_service_returns_assignments():

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="bass",
        description=None,
        created_at=datetime.now(),
    )

    service = RuleBasedMusicalFunctionAssignmentService()

    result = service.assign((source,))

    assert len(result) == 1

    assignment = result[0]

    assert isinstance(
        assignment,
        SourceMusicalFunctionAssignment,
    )

    assert assignment.sound_source_id == source.id
    assert assignment.confidence > 0.0
    assert assignment.rationale is not None
