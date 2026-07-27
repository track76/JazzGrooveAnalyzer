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


def test_metric_offset_becomes_x_coordinate():

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.010,
        confidence=1.0,
        created_at=datetime.now(),
    )

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.000,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(event,),
        created_at=datetime.now(),
    )

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build(
        (cluster,)
    )

    coordinate = (
        plane.points[0]
        .coordinates[0]
    )

    assert coordinate.name == "Metric Offset"
    assert coordinate.unit == "ms"
    assert coordinate.value == pytest.approx(10.0)
