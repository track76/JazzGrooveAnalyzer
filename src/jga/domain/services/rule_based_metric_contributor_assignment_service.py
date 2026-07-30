from datetime import datetime
from uuid import uuid4

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function import MusicalFunction
from jga.domain.services.metric_contributor_assignment_service import (
    MetricContributorAssignmentService,
)
from jga.domain.sound_source import SoundSource
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


class RuleBasedMetricContributorAssignmentService(
    MetricContributorAssignmentService,
):

    def assign(
        self,
        sources: tuple[SoundSource, ...],
        assignments: tuple[
            SourceMusicalFunctionAssignment,
            ...
        ],
        functions: tuple[MusicalFunction, ...],
    ) -> tuple[MetricContributor, ...]:

        contributors: list[MetricContributor] = []

        functions_by_id = {
            function.id: function
            for function in functions
        }

        for source, assignment in zip(
            sources,
            assignments,
        ):

            function = functions_by_id.get(
                assignment.musical_function_id
            )

            if function is None:
                continue

            contributors.append(
                MetricContributor(
                    id=uuid4(),
                    sound_source_id=source.id,
                    musical_function_id=(
                        assignment.musical_function_id
                    ),
                    active=function.is_metric,
                    created_at=datetime.now(),
                )
            )

        return tuple(contributors)
