from jga.geometry import ScientificCoordinate


def test_coordinate_creation():
    coordinate = ScientificCoordinate(
        name="Metric Offset",
        value=12.5,
        unit="ms",
    )

    assert coordinate.name == "Metric Offset"
    assert coordinate.value == 12.5
    assert coordinate.unit == "ms"


def test_coordinate_is_frozen():
    coordinate = ScientificCoordinate(
        name="Metric Offset",
        value=0.0,
        unit="ms",
    )

    try:
        coordinate.value = 10.0
        assert False
    except Exception:
        assert True


def test_two_equal_coordinates_are_equal():
    c1 = ScientificCoordinate(
        name="Metric Offset",
        value=8.0,
        unit="ms",
    )

    c2 = ScientificCoordinate(
        name="Metric Offset",
        value=8.0,
        unit="ms",
    )

    assert c1 == c2
