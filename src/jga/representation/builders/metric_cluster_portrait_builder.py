"""
Metric Cluster Portrait Builder.

Builds immutable representation objects from validated
Domain entities.
"""

from jga.domain.metric_cluster import MetricCluster

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.metric_point import MetricPoint


class MetricClusterPortraitBuilder:
    """
    Builds MetricClusterPortrait objects.

    No geometric measurements are performed here.
    """

    def build(
        self,
        cluster: MetricCluster,
    ) -> MetricClusterPortrait:

        points = tuple(
            MetricPoint(
                event=event,
                offset_ms=0.0,
            )
            for event in cluster.events
        )

        return MetricClusterPortrait(
            metric_cluster=cluster,
            points=points,
        )
