from jga.representation.metric_point import MetricPoint
from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)
from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)
from jga.visualization.visual_point import (
    VisualPoint,
)

from tests.factories.elementary_metric_event_factory import (
    make_elementary_metric_event,
)


def test_visual_projection_preserves_metric_value():

    metric_point = MetricPoint(
        event=make_elementary_metric_event(
            timestamp=0.0,
        ),
        coordinate=ScientificCoordinate(
            value=12.5,
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        ),
    )

    visual_point = VisualPoint(
        x=0.0,
        y=metric_point.coordinate.value,
        time=metric_point.event.timestamp,
    )

    assert visual_point.y == 12.5


def test_visual_projection_does_not_modify_scientific_object():

    metric_point = MetricPoint(
        event=make_elementary_metric_event(
            timestamp=1.0,
        ),
        coordinate=ScientificCoordinate(
            value=-4.0,
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        ),
    )

    visual_point = VisualPoint(
        x=1.0,
        y=metric_point.coordinate.value,
        time=metric_point.event.timestamp,
    )

    assert metric_point.coordinate.value == -4.0
    assert visual_point.y == -4.0
