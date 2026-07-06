from datetime import datetime
from uuid import uuid4

from jga.core.domain.metric_contributor import MetricContributor
from jga.core.domain.musical_function import MusicalFunction
from jga.core.domain.services.metric_contributor_assignment_service import (
    MetricContributorAssignmentService,
)
from jga.core.domain.sound_source import SoundSource


class RuleBasedMetricContributorAssignmentService(
    MetricContributorAssignmentService,
):

    def assign(
        self,
        sources: tuple[SoundSource, ...],
        functions: tuple[MusicalFunction, ...],
    ) -> tuple[MetricContributor, ...]:

        contributors: list[MetricContributor] = []

        for source, function in zip(sources, functions):

            contributors.append(
                MetricContributor(
                    id=uuid4(),
                    sound_source_id=source.id,
                    musical_function_id=function.id,
                    active=function.is_metric,
                    created_at=datetime.now(),
                )
            )

        return tuple(contributors)