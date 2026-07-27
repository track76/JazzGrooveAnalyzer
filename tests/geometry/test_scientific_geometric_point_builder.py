from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)


from jga.geometry.builders import (
    ScientificGeometricPointBuilder,
)


def test_builder_creates_two_dimensional_point():

    projection_input = ScientificProjectionInput(
        coordinates=(
            ScientificCoordinate(
                name="Metric Offset",
                value=12.0,
                unit="ms",
            ),
            ScientificCoordinate(
                name="Metric Stability",
                value=0.90,
                unit="score",
            ),
        )
    )

    builder = ScientificGeometricPointBuilder()

    point = builder.build(
        projection_input
    )

    assert isinstance(
        point,
        GeometricPoint,
    )

    assert len(
        point.coordinates
    ) == 2

    assert point.coordinates[0].name == "Metric Offset"
    assert point.coordinates[1].name == "Metric Stability"
