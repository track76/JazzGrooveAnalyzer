from datetime import datetime
from uuid import uuid4

from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_source_musical_function_assignment_creation():

    assignment = SourceMusicalFunctionAssignment(
        id=uuid4(),
        sound_source_id=uuid4(),
        musical_function_id=uuid4(),
        confidence=0.8,
        rationale="metric foundation",
        created_at=datetime.now(),
    )

    assert assignment.confidence == 0.8
    assert assignment.rationale == "metric foundation"


def test_source_musical_function_assignment_requires_valid_confidence():

    try:
        SourceMusicalFunctionAssignment(
            id=uuid4(),
            sound_source_id=uuid4(),
            musical_function_id=uuid4(),
            confidence=1.5,
            rationale=None,
            created_at=datetime.now(),
        )

    except ValueError:
        return

    assert False
