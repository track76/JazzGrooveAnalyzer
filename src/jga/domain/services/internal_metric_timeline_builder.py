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

        if not pulses:
            raise ValueError(
                "At least one Pulse is required to build an InternalMetricTimeline."
            )

        for pulse in pulses:
            if pulse is None:
                raise ValueError(
                    "Pulse sequence cannot contain None values."
                )

            if not isinstance(pulse, Pulse):
                raise TypeError(
                    "All elements must be Pulse instances."
                )

        return InternalMetricTimeline(
            id=uuid4(),
            pulses=pulses,
            created_at=datetime.now(),
        )
