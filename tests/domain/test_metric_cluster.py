from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster


def make_event() -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.0,
        confidence=0.95,
        created_at=datetime.now(),
    )


def make_beat() -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.0,
        created_at=datetime.now(),
    )


def make_cluster() -> MetricCluster:
    return MetricCluster(
        id=uuid4(),
        beat_reference=make_beat(),
        events=(make_event(),),
        created_at=datetime.now(),
    )


def test_create_valid_cluster():
    cluster = make_cluster()

    assert cluster.size == 1
    assert cluster.beat_reference is not None


def test_multiple_events():
    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=make_beat(),
        events=(
            make_event(),
            make_event(),
            make_event(),
        ),
        created_at=datetime.now(),
    )

    assert cluster.size == 3


def test_cluster_is_immutable():
    cluster = make_cluster()

    with pytest.raises(AttributeError):
        cluster.events = (make_event(),)


def test_empty_cluster_raises():
    with pytest.raises(ValueError):
        MetricCluster(
            id=uuid4(),
            beat_reference=make_beat(),
            events=(),
            created_at=datetime.now(),
        )