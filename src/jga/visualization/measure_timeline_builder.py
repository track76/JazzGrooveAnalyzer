"""
Measure Timeline Builder.

Transforms analytical measures into
visualization timelines.
"""

from jga.visualization.measure import (
    Measure,
)

from jga.visualization.measure_timeline import (
    MeasureTimeline,
)


class MeasureTimelineBuilder:
    """
    Builds measure visualization timelines.
    """

    def build(
        self,
        measure: Measure,
    ) -> MeasureTimeline:

        beats = []
        offsets = []

        for event in measure.metric_events:

            beats.append(
                event.beat_index
            )

            offsets.append(
                event.offset_ms
            )

        return MeasureTimeline(
            measure_number=measure.number,
            beats=tuple(beats),
            offsets_ms=tuple(offsets),
        )
