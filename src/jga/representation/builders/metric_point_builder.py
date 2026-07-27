"""
Metric Point Builder.

Builds immutable MetricPoint objects from
Representation Layer inputs.
"""

from jga.representation.metric_point import (
    MetricPoint,
)


class MetricPointBuilder:
    """
    Builds immutable MetricPoint objects.
    """

    def build(
        self,
        x: float = 0.0,
        y: float = 0.0,
    ) -> MetricPoint:

        return MetricPoint(
            x=x,
            y=y,
        )
