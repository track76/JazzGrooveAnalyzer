from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


def test_scientific_coordinate_creation():

    coordinate = ScientificCoordinate(
        value=10.5,
        unit="milliseconds",
        dimension="metric_temporal_displacement",
    )

    assert coordinate.value == 10.5
    assert coordinate.unit == "milliseconds"
    assert coordinate.dimension == (
        "metric_temporal_displacement"
    )


def test_scientific_coordinate_is_immutable():

    coordinate = ScientificCoordinate(
        value=1.0,
        unit="milliseconds",
        dimension="metric_temporal_displacement",
    )

    try:
        coordinate.value = 2.0
        assert False
    except Exception:
        assert True
