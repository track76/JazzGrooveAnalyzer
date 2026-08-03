"""
Metric Visualization Point.

Represents a metric domain event
mapped into visualization space.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricVisualizationPoint:
    """
    Point representation of metric data.
    """

    time: float

    value: float

    def is_valid(
        self,
    ) -> bool:
        """
        Checks point validity.
        """

        return (
            self.time >= 0.0
            and self.value is not None
        )
