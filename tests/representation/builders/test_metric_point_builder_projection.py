from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from tests.support.domain_objects import (
    make_elementary_metric_event,
)

from jga.representation.builders.metric_point_builder import (
    MetricPointBuilder,
)


def test_metric_point_builder_projects_event():

    event = make_elementary_metric_event()

    beat_reference = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=event.timestamp,
        created_at=datetime.now(),
    )

    point = (
        MetricPointBuilder()
        .build_from_event(
            event,
            beat_reference,
        )
    )

    assert point.event is event
    assert point.offset_ms == 0.0
