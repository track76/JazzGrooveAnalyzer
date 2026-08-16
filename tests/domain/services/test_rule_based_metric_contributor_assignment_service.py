from datetime import datetime
from uuid import uuid4

from jga.domain.musical_function import MusicalFunction
from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_metric_contributors_follow_metric_functions():

    source = SoundSource(
        id=uuid4(),
        name="Double Bass",
        family="Strings",
        description=None,
        created_at=datetime.now(),
    )

    function = MusicalFunction(
        id=uuid4(),
        name="Pulse",
        description=None,
        is_metric=True,
        created_at=datetime.now(),
    )

    assignment = SourceMusicalFunctionAssignment(
        id=uuid4(),
        sound_source_id=source.id,
        musical_function_id=function.id,
        confidence=1.0,
        rationale=None,
        created_at=datetime.now(),
    )

    assignment_result = MusicalFunctionAssignmentResult(
        musical_functions=(function,),
        assignments=(assignment,),
    )

    service = RuleBasedMetricContributorAssignmentService()

    contributors = service.assign(
        (source,),
        assignment_result,
    )

    assert len(contributors) == 1

    contributor = contributors[0]

    assert contributor.sound_source_id == source.id
    assert contributor.musical_function_id == function.id
    assert contributor.active is True

    replay = service.assign(
        (source,),
        assignment_result,
    )

    assert replay[0].id == contributor.id
