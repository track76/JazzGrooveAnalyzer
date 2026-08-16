"""
Metric Point Builder.

Projects validated Domain events into immutable
Representation Layer MetricPoint objects.
"""

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.services.metric_offset_calculator import (
    MetricOffsetCalculator,
)

from jga.representation.metric_point import (
    MetricPoint,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


class MetricPointBuilder:
    """
    Builds immutable MetricPoint objects.
    """

    def __init__(self):

        self._offset_calculator = (
            MetricOffsetCalculator()
        )

    def build_from_event(
        self,
        event: ElementaryMetricEvent,
        beat_reference: BeatReference,
        following_beat_reference: BeatReference | None = None,
    ) -> MetricPoint:
        """
        Scientific projection of one validated
        ElementaryMetricEvent.
        """

        preceding = beat_reference
        nearest = preceding
        if following_beat_reference is not None and (
            abs(event.timestamp - following_beat_reference.timestamp)
            < abs(event.timestamp - preceding.timestamp)
        ):
            nearest = following_beat_reference

        offset = self._offset_calculator.compute(
            event,
            nearest,
        )
        elapsed = event.timestamp - preceding.timestamp
        period = (
            float(preceding.exact_period_seconds)
            if preceding.exact_period_seconds is not None
            else (
                following_beat_reference.timestamp - preceding.timestamp
                if following_beat_reference is not None
                else None
            )
        )
        phase = elapsed / period if period is not None and period > 0 else None

        return MetricPoint(
            event=event,
            beat_reference=nearest,
            coordinate=ScientificCoordinate(
                axis=(
                    METRIC_TEMPORAL_DISPLACEMENT_AXIS
                ),
                value=offset,
            ),
            beat_index=nearest.index,
            preceding_beat_reference=preceding,
            following_beat_reference=following_beat_reference,
            elapsed_from_preceding_seconds=elapsed,
            normalized_quarter_phase=phase,
        )
