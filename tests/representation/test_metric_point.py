from tests.support.domain_objects import make_elementary_metric_event

from jga.representation.metric_point import MetricPoint
from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


def test_metric_point_type_exists():
    assert MetricPoint is not None


def test_metric_point_preserves_eme_reference():

    eme = make_elementary_metric_event()

    coordinate = ScientificCoordinate(
        value=0.0,
        unit="milliseconds",
        dimension="metric_temporal_displacement",
    )

    point = MetricPoint(
        event=eme,
        coordinate=coordinate,
    )

    assert point.event is eme

    assert point.coordinate is coordinate

    assert point.coordinate.value == 0.0
    assert point.coordinate.unit == "milliseconds"
    assert point.coordinate.dimension == (
        "metric_temporal_displacement"
    )


def test_metric_point_offset_compatibility_property():

    eme = make_elementary_metric_event()

    point = MetricPoint(
        event=eme,
        coordinate=ScientificCoordinate(
            value=12.5,
            unit="milliseconds",
            dimension="metric_temporal_displacement",
        ),
    )

    assert point.offset_ms == 12.5
