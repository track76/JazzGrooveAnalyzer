from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from jga.visualization.scientific_projection import (
    ScientificProjection,
)

from jga.visualization.scientific_projection_engine import (
    ScientificProjectionEngine,
)


def test_engine_projects_scientific_projection():

    coordinate = ScientificCoordinate(
        value=5.0,
        axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
    )

    projection = ScientificProjection(
        coordinate=coordinate,
        visual_value=5.0,
    )

    point = (
        ScientificProjectionEngine()
        .project(projection)
    )

    assert point.x == 5.0
    assert point.y == 5.0
