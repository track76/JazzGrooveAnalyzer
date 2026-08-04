"""
Beat Seed Estimator.

Produces an initial sequence of beat seed timestamps
from observed ElementaryMetricEvents.

M70.2
"""

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)


class BeatSeedEstimator:
    """
    Initial deterministic implementation.

    One event produces one beat seed.
    """

    def estimate(
        self,
        events: tuple[ElementaryMetricEvent, ...],
    ) -> tuple[float, ...]:

        if not events:
            return ()

        return tuple(
            event.timestamp
            for event in events
        )
