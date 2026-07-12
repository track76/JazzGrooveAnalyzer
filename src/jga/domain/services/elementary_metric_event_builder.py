from datetime import datetime
from uuid import uuid4

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.pulse_candidate import PulseCandidate


class ElementaryMetricEventBuilder:
    """
    Builds ElementaryMetricEvent objects from PulseCandidate objects.
    """

    def build(
        self,
        pulse_candidates: tuple[PulseCandidate, ...],
    ) -> tuple[ElementaryMetricEvent, ...]:

        if not pulse_candidates:
            return ()

        events = []

        for candidate in pulse_candidates:

            events.append(
                ElementaryMetricEvent(
                    id=uuid4(),
                    contributor_id=candidate.sound_source_id,
                    timestamp=candidate.timestamp,
                    confidence=candidate.confidence,
                    created_at=datetime.now(),
                )
            )

        return tuple(events)
