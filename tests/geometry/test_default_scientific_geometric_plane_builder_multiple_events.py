import pytest

from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.metric_cluster import MetricCluster

from jga.geometry.builders import (
    DefaultScientificGeometricPlaneBuilder,
)


def test_multiple_events_preserve_metric_offset_sequence():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.000,
        created_at=datetime.now(),
    )

    event_1 = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=0.995,
        confidence=1.0,
        created_at=datetime.now(),
    )

    event_2 = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.010,
        confidence=1.0,
        created_at=datetime.now(),
    )

    event_3 = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.020,
        confidence=1.0,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(
            event_1,
            event_2,
            event_3,
        ),
        created_at=datetime.now(),
    )

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build(
        (cluster,)
    )

    coordinates = (
        plane.points[0]
        .coordinates
    )

    assert len(coordinates) == 3

    assert coordinates[0].value == pytest.approx(-5.0)
    assert coordinates[1].value == pytest.approx(10.0)
    assert coordinates[2].value == pytest.approx(20.0)
