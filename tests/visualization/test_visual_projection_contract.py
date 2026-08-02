from tests.support.domain_objects import (
    make_elementary_metric_event,
)

from jga.representation.metric_point import (
    MetricPoint,
)

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)

from jga.visualization.visual_point import (
    VisualPoint,
)


def test_visual_projection_preserves_metric_value():

    metric_point = MetricPoint(
        event=make_elementary_metric_event(),
        coordinate=ScientificCoordinate(
            value=12.5,
            axis=(
                METRIC_TEMPORAL_DISPLACEMENT_AXIS
            ),
        ),
    )

    visual_point = VisualPoint(
        x=0.0,
        y=metric_point.coordinate.value,
    )

    assert (
        visual_point.y
        ==
        metric_point.coordinate.value
    )


def test_visual_projection_does_not_modify_scientific_object():

    metric_point = MetricPoint(
        event=make_elementary_metric_event(),
        coordinate=ScientificCoordinate(
            value=-4.0,
            axis=(
                METRIC_TEMPORAL_DISPLACEMENT_AXIS
            ),
        ),
    )

    visual_point = VisualPoint(
        x=1.0,
        y=metric_point.coordinate.value,
    )

    assert metric_point.coordinate.value == -4.0

    assert visual_point.y == -4.0
