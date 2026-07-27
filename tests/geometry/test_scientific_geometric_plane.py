from jga.geometry import (
    GeometricPoint,
    ScientificCoordinate,
    ScientificGeometricPlane,
)


def test_empty_plane():
    plane = ScientificGeometricPlane(())

    assert plane.size == 0


def test_plane_with_one_point():
    point = GeometricPoint(
        (
            ScientificCoordinate(
                name="Metric Offset",
                value=10.0,
                unit="ms",
            ),
        )
    )

    plane = ScientificGeometricPlane((point,))

    assert plane.size == 1


def test_plane_with_two_points():
    point = GeometricPoint(
        (
            ScientificCoordinate(
                name="Metric Offset",
                value=10.0,
                unit="ms",
            ),
        )
    )

    plane = ScientificGeometricPlane(
        (
            point,
            point,
        )
    )

    assert plane.size == 2
