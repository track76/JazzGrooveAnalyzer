"""
Metric Visualization Series.

Represents a temporal sequence
of metric visualization points.
"""

from dataclasses import dataclass, field

from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)


@dataclass(frozen=True, slots=True)
class MetricVisualizationSeries:
    """
    Series of metric visualization points.
    """

    points: tuple[MetricVisualizationPoint, ...] = field(
        default_factory=tuple,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks series validity.
        """

        return all(
            point.is_valid()
            for point in self.points
        )
