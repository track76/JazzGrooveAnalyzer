from datetime import datetime
from uuid import uuid4

from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.domain.sound_source import SoundSource


def test_assign_bass_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="bass",
        description=None,
        created_at=datetime.now(),
    )

    result = service.assign((source,))

    assert isinstance(
        result,
        MusicalFunctionAssignmentResult,
    )

    assert len(result.assignments) == 1

    assert len(result.musical_functions) == 1

    assert (
        result.musical_functions[0].name
        == "Walking Bass"
    )

    assert (
        result.musical_functions[0].is_metric
        is True
    )


def test_assign_unknown_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="accordion",
        family="unknown",
        description=None,
        created_at=datetime.now(),
    )

    result = service.assign((source,))

    assert len(result.assignments) == 1

    assert (
        result.musical_functions[0].name
        == "Unknown"
    )

    assert (
        result.musical_functions[0].is_metric
        is False
    )
