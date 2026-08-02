from jga.representation.scientific_axis import (
    ScientificAxis,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


def make_metric_temporal_displacement_axis():

    return ScientificAxis(
        identifier="metric_temporal_displacement",
        name="Metric Temporal Displacement",
        dimension="metric_temporal_displacement",
        unit="milliseconds",
        description=(
            "Temporal displacement between "
            "ElementaryMetricEvent and BeatReference"
        ),
    )


def test_scientific_coordinate_creation():

    axis = make_metric_temporal_displacement_axis()

    coordinate = ScientificCoordinate(
        axis=axis,
        value=10.5,
    )

    assert coordinate.value == 10.5

    assert coordinate.axis is axis


def test_scientific_coordinate_is_immutable():

    axis = make_metric_temporal_displacement_axis()

    coordinate = ScientificCoordinate(
        axis=axis,
        value=1.0,
    )

    try:
        coordinate.value = 2.0
        assert False
    except Exception:
        assert True
