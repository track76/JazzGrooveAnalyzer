"""
Metric Event Inspector.

Builds detailed analytical information
for one MetricEvent.
"""

from jga.visualization.metric_event_detail import (
    MetricEventDetail,
)


class MetricEventInspector:
    """
    Creates detailed views of metric events.
    """

    def inspect(
        self,
        event,
        measure_number: int,
        bpm: float,
    ) -> MetricEventDetail:

        return MetricEventDetail(
            source_name=event.source_name,

            measure_number=measure_number,

            theoretical_position=(
                event.theoretical_position
            ),

            observed_position=(
                event.beat_index
            ),

            beat_position=(
                event.theoretical_position
            ),

            offset_ms=(
                event.offset_ms
            ),

            bpm=bpm,
        )
