from datetime import datetime
from uuid import uuid4

from jga.domain.musical_function import MusicalFunction
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_assign_metric_contributor():

    service = RuleBasedMetricContributorAssignmentService()

    source = SoundSource(
        id=uuid4(),
        name="bass",
        family="strings",
        description=None,
        created_at=datetime.now(),
    )

    function = MusicalFunction(
        id=uuid4(),
        name="Walking Bass",
        description=None,
        is_metric=True,
        created_at=datetime.now(),
    )

    assignment = SourceMusicalFunctionAssignment(
        id=uuid4(),
        sound_source_id=source.id,
        musical_function_id=function.id,
        confidence=0.9,
        rationale="bass provides metric foundation",
        created_at=datetime.now(),
    )

    contributors = service.assign(
        (source,),
        (assignment,),
        (function,),
    )

    assert len(contributors) == 1
    assert contributors[0].active is True
    assert contributors[0].sound_source_id == source.id
    assert contributors[0].musical_function_id == function.id
