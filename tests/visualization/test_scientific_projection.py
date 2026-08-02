from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from jga.visualization.scientific_projection import (
    ScientificProjection,
)


def test_projection_preserves_scientific_coordinate():

    coordinate = ScientificCoordinate(
        value=10.0,
        axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
    )

    projection = ScientificProjection(
        coordinate=coordinate,
        visual_value=10.0,
    )

    assert (
        projection.coordinate
        is coordinate
    )


def test_projection_is_immutable():

    projection = ScientificProjection(
        coordinate=ScientificCoordinate(
            value=0.0,
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        ),
        visual_value=0.0,
    )

    try:
        projection.visual_value = 1.0
        assert False
    except Exception:
        assert True
