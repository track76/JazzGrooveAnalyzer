from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from jga.domain.metric_contributor import MetricContributor
from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.services.metric_contributor_assignment_service import (
    MetricContributorAssignmentService,
)
from jga.domain.sound_source import SoundSource


class RuleBasedMetricContributorAssignmentService(
    MetricContributorAssignmentService,
):

    def assign(
        self,
        sources: tuple[SoundSource, ...],
        assignment_result: MusicalFunctionAssignmentResult,
    ) -> tuple[MetricContributor, ...]:

        contributors: list[MetricContributor] = []

        functions_by_id = {
            function.id: function
            for function in assignment_result.musical_functions
        }

        for source, assignment in zip(
            sources,
            assignment_result.assignments,
        ):

            function = functions_by_id.get(
                assignment.musical_function_id
            )

            if function is None:
                continue

            contributors.append(
                MetricContributor(
                    id=uuid5(
                        NAMESPACE_URL,
                        ":".join(
                            (
                                "metric-contributor/v1",
                                str(source.id),
                                function.name,
                                str(function.is_metric),
                            )
                        ),
                    ),
                    sound_source_id=source.id,
                    musical_function_id=(
                        assignment.musical_function_id
                    ),
                    active=function.is_metric,
                    created_at=datetime.now(),
                )
            )

        return tuple(contributors)
