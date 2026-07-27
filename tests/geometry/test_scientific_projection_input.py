from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


def test_projection_input_contains_coordinates():

    coordinate = ScientificCoordinate(
        name="Metric Offset",
        value=10.0,
        unit="ms",
    )

    projection_input = ScientificProjectionInput(
        coordinates=(coordinate,)
    )

    assert len(
        projection_input.coordinates
    ) == 1
