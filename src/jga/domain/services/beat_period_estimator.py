"""
Beat Period Estimator.

Estimates the initial beat period from observed
ElementaryMetricEvents.

M70.3
"""

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)


class BeatPeriodEstimator:
    """
    Initial deterministic implementation.

    Estimates the beat period from the average
    temporal distance between consecutive events.
    """

    def estimate(
        self,
        events: tuple[ElementaryMetricEvent, ...],
    ) -> float | None:

        if len(events) < 2:
            return None

        intervals = [
            current.timestamp - previous.timestamp
            for previous, current in zip(
                events,
                events[1:],
            )
        ]

        period = (
            sum(intervals)
            /
            len(intervals)
        )

        # Avoid half-tempo reconstruction.
        # Beat period should remain in a musical
        # pulse range.
        if period > 0.8:
            period /= 2.0

        return period
