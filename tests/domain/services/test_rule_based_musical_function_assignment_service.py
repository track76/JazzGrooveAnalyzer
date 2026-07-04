from datetime import datetime
from uuid import uuid4

from jga.core.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)
from jga.core.domain.sound_source import SoundSource


def test_assign_bass_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="strings",
        description=None,
        created_at=datetime.now(),
    )

    functions = service.assign((source,))

    assert len(functions) == 1
    assert functions[0].name == "Walking Bass"
    assert functions[0].is_metric is True


def test_assign_unknown_function():

    service = RuleBasedMusicalFunctionAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="accordion",
        family="unknown",
        description=None,
        created_at=datetime.now(),
    )

    functions = service.assign((source,))

    assert len(functions) == 1
    assert functions[0].name == "Unknown"
    assert functions[0].is_metric is False