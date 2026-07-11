from datetime import datetime
from uuid import uuid4

from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.pulse import Pulse


class InternalMetricTimelineBuilder:
    """Builds an InternalMetricTimeline from Pulse objects."""

    def build(
        self,
        pulses: tuple[Pulse, ...],
    ) -> InternalMetricTimeline:

        return InternalMetricTimeline(
            id=uuid4(),
            pulses=pulses,
            created_at=datetime.now(),
        )