from jga.domain.metric_cluster import MetricCluster

from jga.domain.services.metric_offset_calculator import (
    MetricOffsetCalculator,
)

from jga.geometry.geometric_point import GeometricPoint

from jga.geometry.projectors import (
    MetricOffsetCoordinateProjector,
)

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)

from jga.interfaces.geometry import (
    ScientificGeometricPlaneBuilder,
)


class DefaultScientificGeometricPlaneBuilder(
    ScientificGeometricPlaneBuilder
):
    """
    Builds ScientificGeometricPlane from MetricClusters.

    The first scientific coordinate is:
    X = Metric Offset
    """

    def __init__(self) -> None:
        self._offset_calculator = (
            MetricOffsetCalculator()
        )

        self._offset_projector = (
            MetricOffsetCoordinateProjector()
        )

    def build(
        self,
        metric_clusters: tuple[MetricCluster, ...],
    ) -> ScientificGeometricPlane:

        points = []

        for cluster in metric_clusters:

            coordinates = []

            for event in cluster.events:

                offset = (
                    self._offset_calculator.compute(
                        event,
                        cluster.beat_reference,
                    )
                )

                coordinates.append(
                    self._offset_projector.project(
                        offset
                    )
                )

            points.append(
                GeometricPoint(
                    tuple(coordinates)
                )
            )

        return ScientificGeometricPlane(
            points=tuple(points)
        )
