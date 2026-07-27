from jga.geometry import GeometricPoint, ScientificCoordinate


def test_empty_point():
    point = GeometricPoint(())

    assert point.dimension == 0


def test_one_coordinate():
    point = GeometricPoint(
        (
            ScientificCoordinate(
                name="Metric Offset",
                value=5.0,
                unit="ms",
            ),
        )
    )

    assert point.dimension == 1


def test_two_coordinates():
    point = GeometricPoint(
        (
            ScientificCoordinate(
                name="Metric Offset",
                value=5.0,
                unit="ms",
            ),
            ScientificCoordinate(
                name="Future Coordinate",
                value=2.0,
                unit="unit",
            ),
        )
    )

    assert point.dimension == 2
