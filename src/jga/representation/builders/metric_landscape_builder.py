"""
Metric Landscape Builder.

Builds the scientific representation of one
complete musical performance.
"""

from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.metric_trajectory import (
    MetricTrajectory,
)


class MetricLandscapeBuilder:
    """
    Builds immutable MetricLandscape objects.
    """

    def build(
        self,
        metric_cluster_portraits: tuple = (),
        metric_trajectory: MetricTrajectory | None = None,
    ) -> MetricLandscape:

        return MetricLandscape(
            metric_trajectory=metric_trajectory,
            metric_cluster_portraits=metric_cluster_portraits,
        )
