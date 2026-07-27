from jga.domain.metric_cluster import MetricCluster
from jga.geometry.builders import (
    DefaultScientificGeometricPlaneBuilder,
)
from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)
from jga.interfaces.representation import (
    ScientificGeometryEngine,
)


class DefaultScientificGeometryEngine(
    ScientificGeometryEngine,
):
    """
    Default Geometry Engine.

    Converts Domain MetricClusters into a ScientificGeometricPlane.
    """

    def __init__(self) -> None:
        self._builder = DefaultScientificGeometricPlaneBuilder()

    def project(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> ScientificGeometricPlane:
        return self._builder.build(metric_clusters)
