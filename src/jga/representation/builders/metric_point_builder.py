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
    ) -> MetricPoint:
        """
        Scientific projection of one validated
        ElementaryMetricEvent.
        """

        offset = self._offset_calculator.compute(
            event,
            beat_reference,
        )

        return MetricPoint(
            event=event,
            beat_reference=beat_reference,
            coordinate=ScientificCoordinate(
                axis=(
                    METRIC_TEMPORAL_DISPLACEMENT_AXIS
                ),
                value=offset,
            ),
            beat_index=beat_reference.index,
        )
