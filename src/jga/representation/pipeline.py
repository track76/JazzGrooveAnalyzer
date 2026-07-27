"""
Representation Pipeline.

Transforms validated Domain representations into immutable
Representation Layer objects.
"""

from jga.domain.metric_cluster import MetricCluster

from jga.representation.builders.metric_cluster_portrait_builder import (
    MetricClusterPortraitBuilder,
)
from jga.representation.builders.metric_landscape_builder import (
    MetricLandscapeBuilder,
)
from jga.representation.builders.metric_point_builder import (
    MetricPointBuilder,
)
from jga.representation.builders.metric_trajectory_builder import (
    MetricTrajectoryBuilder,
)
from jga.representation.representation_result import (
    RepresentationResult,
)


class RepresentationPipeline:
    """
    Executes the Representation Layer.
    """

    def __init__(self):

        self._portrait_builder = (
            MetricClusterPortraitBuilder()
        )

        self._landscape_builder = (
            MetricLandscapeBuilder()
        )

        self._trajectory_builder = (
            MetricTrajectoryBuilder()
        )

        self._metric_point_builder = (
            MetricPointBuilder()
        )

    def run(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> RepresentationResult:

        portraits = tuple(
            self._portrait_builder.build(cluster)
            for cluster in metric_clusters
        )

        metric_points = tuple(
            self._metric_point_builder.build_from_event(
                event,
                cluster.beat_reference,
            )
            for cluster in metric_clusters
            for event in cluster.events
        )

        trajectory = self._trajectory_builder.build(
            metric_points=metric_points,
        )

        landscape = self._landscape_builder.build(
            metric_cluster_portraits=portraits,
            metric_trajectory=trajectory,
        )

        return RepresentationResult(
            metric_landscape=landscape,
        )
