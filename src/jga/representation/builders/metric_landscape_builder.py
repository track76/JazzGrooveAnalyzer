"""
Metric Landscape Builder.

Builds the scientific representation of one
complete musical performance.
"""

from jga.representation.metric_landscape import (
    MetricLandscape,
)


class MetricLandscapeBuilder:
    """
    Builds immutable MetricLandscape objects.
    """

    def build(
        self,
        metric_cluster_portraits: tuple = (),
    ) -> MetricLandscape:

        return MetricLandscape(
            metric_cluster_portraits=metric_cluster_portraits,
        )
