"""
Metric Landscape Visualization Adapter.

Connects Representation Layer geometry
to Visualization Layer objects.
"""

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


class MetricLandscapeVisualizationAdapter:
    """
    Adapts MetricLandscape into visual objects.
    """

    def adapt(
        self,
        landscape: MetricLandscape,
    ) -> VisualTrajectory:
        """
        Converts scientific metric points into
        visual points.

        X:
            temporal ordering

        Y:
            scientific metric displacement
        """

        if landscape.metric_trajectory is None:
            return VisualTrajectory()

        points = tuple(
            VisualPoint(
                x=float(index),
                y=metric_point.coordinate.value,
                time=metric_point.event.timestamp,
            )
            for index, metric_point in enumerate(
                landscape.metric_trajectory.metric_points
            )
        )

        return VisualTrajectory(
            points=points,
        )
