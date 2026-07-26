from tests.support.domain_objects import make_elementary_metric_event

from jga.representation.metric_point import MetricPoint


def test_metric_point_type_exists():
    assert MetricPoint is not None


def test_metric_point_preserves_eme_reference():

    eme = make_elementary_metric_event()

    point = MetricPoint(
        event=eme,
        offset_ms=0.0,
    )

    assert point.event is eme
    assert point.offset_ms == 0.0
