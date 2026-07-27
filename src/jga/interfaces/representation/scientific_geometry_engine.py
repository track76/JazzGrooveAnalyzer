from abc import ABC, abstractmethod

from jga.domain.metric_cluster import MetricCluster
from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


class ScientificGeometryEngine(ABC):
    """
    Produces a ScientificGeometricPlane from Domain MetricClusters.
    """

    @abstractmethod
    def project(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> ScientificGeometricPlane:
        ...
