from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)

from jga.interfaces.geometry import (
    ScientificGeometricProjectionBuilder,
)


class DefaultScientificGeometricProjectionBuilder(
    ScientificGeometricProjectionBuilder
):
    """
    Builds a ScientificGeometricPlane from
    validated geometric points.
    """

    def build(
        self,
        points: tuple[GeometricPoint, ...],
    ) -> ScientificGeometricPlane:

        return ScientificGeometricPlane(
            points=points
        )
