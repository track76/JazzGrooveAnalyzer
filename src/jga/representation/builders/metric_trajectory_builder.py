"""
Metric Trajectory Builder.
"""

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)


class MetricTrajectoryBuilder:
    """
    Builds immutable MetricTrajectory objects.
    """

    def build(
        self,
        metric_points: tuple = (),
    ) -> MetricTrajectory:

        return MetricTrajectory(
            metric_points=metric_points,
        )
