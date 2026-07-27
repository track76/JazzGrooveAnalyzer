"""
Metric Point Builder.

Projects validated Domain events into immutable
Representation Layer MetricPoint objects.
"""

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.representation.metric_point import (
    MetricPoint,
)


class MetricPointBuilder:
    """
    Builds immutable MetricPoint objects.
    """

    def build_from_event(
        self,
        event: ElementaryMetricEvent,
    ) -> MetricPoint:
        """
        Scientific projection of one validated
        ElementaryMetricEvent.

        The mathematical projection model will
        evolve in future milestones.

        The current implementation preserves
        complete scientific traceability.
        """

        return MetricPoint(
            event=event,
            offset_ms=0.0,
        )
