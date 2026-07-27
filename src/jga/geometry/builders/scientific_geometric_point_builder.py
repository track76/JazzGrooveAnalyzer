from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)


class ScientificGeometricPointBuilder:
    """
    Builds a GeometricPoint from validated
    scientific coordinates.

    No scientific computation is performed here.
    Coordinates are preserved unchanged.
    """

    def build(
        self,
        projection_input: ScientificProjectionInput,
    ) -> GeometricPoint:

        return GeometricPoint(
            projection_input.coordinates
        )
