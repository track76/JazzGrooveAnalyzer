from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent


class BeatReferenceBuilder:
    """
    Builds BeatReference objects from ordered ElementaryMetricEvents.
    """

    def build(
        self,
        events: tuple[ElementaryMetricEvent, ...],
    ) -> tuple[BeatReference, ...]:

        if not events:
            return ()

        return tuple(
            BeatReference(
                id=uuid4(),
                index=index,
                timestamp=event.timestamp,
                created_at=datetime.now(),
            )
            for index, event in enumerate(events)
        )
