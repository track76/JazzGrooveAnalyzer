from jga.geometry.builders import (
    DefaultScientificGeometricProjectionBuilder,
)

from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


def test_builder_creates_plane_from_points():

    point = GeometricPoint(
        coordinates=()
    )

    builder = DefaultScientificGeometricProjectionBuilder()

    plane = builder.build(
        (point,)
    )

    assert isinstance(
        plane,
        ScientificGeometricPlane,
    )

    assert plane.size == 1
