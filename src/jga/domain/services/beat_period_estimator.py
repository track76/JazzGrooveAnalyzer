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

    Estimates the beat period from distinct temporal
    metric positions.

    Simultaneous events from different contributors
    represent the same metric instant and must not
    affect beat period estimation.
    """

    def estimate(
        self,
        events: tuple[ElementaryMetricEvent, ...],
    ) -> float | None:

        if len(events) < 2:
            return None

        timestamps = sorted(
            {
                event.timestamp
                for event in events
            }
        )

        if len(timestamps) < 2:
            return None

        intervals = [
            current - previous
            for previous, current in zip(
                timestamps,
                timestamps[1:],
            )
        ]

        period = (
            sum(intervals)
            /
            len(intervals)
        )

        # Avoid half-tempo reconstruction.
        if period > 0.8:
            period /= 2.0

        return period
