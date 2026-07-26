"""
Representation Pipeline.

Transforms validated Domain representations into immutable
Representation Layer objects.
"""

from jga.domain.metric_cluster import MetricCluster

from jga.representation.builders.metric_cluster_portrait_builder import (
    MetricClusterPortraitBuilder,
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

    def run(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> RepresentationResult:

        portraits = tuple(
            self._portrait_builder.build(cluster)
            for cluster in metric_clusters
        )

        return RepresentationResult(
            metric_cluster_portraits=portraits,
        )
