"""
Metric Cluster Portrait Builder.

Builds immutable representation objects from validated
Domain entities.
"""

from jga.domain.metric_cluster import MetricCluster

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.builders.metric_point_builder import (
    MetricPointBuilder,
)


class MetricClusterPortraitBuilder:
    """
    Builds MetricClusterPortrait objects.

    No geometric measurements are performed here.
    """

    def __init__(self):
        self._metric_point_builder = MetricPointBuilder()

    def build(
        self,
        cluster: MetricCluster,
    ) -> MetricClusterPortrait:

        points = tuple(
            self._metric_point_builder.build_from_event(
                event,
                cluster.beat_reference,
            )
            for event in cluster.events
        )

        return MetricClusterPortrait(
            metric_cluster=cluster,
            points=points,
        )
