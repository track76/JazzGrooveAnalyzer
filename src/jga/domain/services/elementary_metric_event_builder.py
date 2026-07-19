from datetime import datetime
from uuid import uuid4

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate
from jga.domain.services.metric_contributor_resolver import (
    MetricContributorResolver,
)


class ElementaryMetricEventBuilder:
    """
    Builds ElementaryMetricEvent objects from
    Domain PulseCandidate objects.

    The contributor identity is resolved through
    MetricContributorResolver.
    """

    def __init__(self) -> None:

        self._resolver = MetricContributorResolver()

    def build(
        self,
        pulse_candidates: tuple[PulseCandidate, ...],
        contributors: tuple[MetricContributor, ...],
    ) -> tuple[ElementaryMetricEvent, ...]:

        if not pulse_candidates:
            return ()

        if contributors is None:
            raise ValueError(
                "contributors cannot be None."
            )

        events = []

        for candidate in pulse_candidates:

            contributor = self._resolver.resolve(
                candidate.sound_source_id,
                contributors,
            )

            events.append(
                ElementaryMetricEvent(
                    id=uuid4(),
                    contributor_id=contributor.id,
                    timestamp=candidate.timestamp,
                    confidence=candidate.confidence,
                    created_at=datetime.now(),
                )
            )

        return tuple(events)
