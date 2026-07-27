from tests.support.domain_objects import (
    make_elementary_metric_event,
)

from jga.representation.builders.metric_point_builder import (
    MetricPointBuilder,
)


def test_metric_point_builder_projects_event():

    event = make_elementary_metric_event()

    point = (
        MetricPointBuilder()
        .build_from_event(event)
    )

    assert point.event is event
    assert point.offset_ms == 0.0
