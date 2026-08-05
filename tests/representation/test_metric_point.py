from tests.support.domain_objects import make_elementary_metric_event

from jga.representation.metric_point import MetricPoint
from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)
from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


def test_metric_point_type_exists():
    assert MetricPoint is not None


def test_metric_point_preserves_eme_reference():

    eme = make_elementary_metric_event()

    coordinate = ScientificCoordinate(
        axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        value=0.0,
    )

    point = MetricPoint(
        event=eme,
        coordinate=coordinate,
        beat_index=0,
    )

    assert point.event is eme

    assert point.coordinate is coordinate

    assert point.coordinate.value == 0.0

    assert point.coordinate.axis is (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
    )

    assert point.coordinate.axis.unit == (
        "milliseconds"
    )

    assert point.coordinate.axis.dimension == (
        "metric_temporal_displacement"
    )


def test_metric_point_offset_compatibility_property():

    eme = make_elementary_metric_event()

    point = MetricPoint(
        event=eme,
        coordinate=ScientificCoordinate(
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            value=12.5,
        ),
    )

    assert point.offset_ms == 12.5
