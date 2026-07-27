from jga.domain.metric_cluster import MetricCluster
from jga.geometry.geometric_point import GeometricPoint
from jga.geometry.scientific_geometric_plane import ScientificGeometricPlane
from jga.interfaces.geometry import ScientificGeometricPlaneBuilder


class DefaultScientificGeometricPlaneBuilder(
    ScientificGeometricPlaneBuilder
):
    """
    Default implementation of the ScientificGeometricPlaneBuilder.

    Temporary implementation.

    Geometry integration with the Representation Pipeline will be introduced
    in a later milestone.
    """

    def build(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> ScientificGeometricPlane:
        return ScientificGeometricPlane(
            points=tuple(
                GeometricPoint(())
                for _ in metric_clusters
            )
        )
