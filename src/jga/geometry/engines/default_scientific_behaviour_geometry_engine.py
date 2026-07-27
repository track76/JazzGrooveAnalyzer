from jga.core.stability_curve import StabilityCurve
from jga.domain.metric_cluster import MetricCluster

from jga.geometry.builders import (
    ScientificGeometricPointBuilder,
    DefaultScientificGeometricProjectionBuilder,
)

from jga.geometry.projections import (
    DefaultMetricBehaviourProjection,
)

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


class DefaultScientificBehaviourGeometryEngine:
    """
    Builds a ScientificGeometricPlane from
    temporal musical behaviour observations.
    """

    def __init__(self):

        self.projection = (
            DefaultMetricBehaviourProjection()
        )

        self.point_builder = (
            ScientificGeometricPointBuilder()
        )

        self.plane_builder = (
            DefaultScientificGeometricProjectionBuilder()
        )

    def project(
        self,
        metric_clusters: tuple[MetricCluster, ...],
        stability_curve: StabilityCurve,
    ) -> ScientificGeometricPlane:

        points = []

        for cluster in metric_clusters:

            for event in cluster.events:

                projection_input = (
                    self.projection.project(
                        event,
                        cluster.beat_reference,
                        stability_curve,
                    )
                )

                point = (
                    self.point_builder.build(
                        projection_input,
                    )
                )

                points.append(point)

        return self.plane_builder.build(
            tuple(points)
        )
