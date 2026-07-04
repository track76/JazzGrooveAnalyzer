from datetime import datetime
from uuid import uuid4

import pytest

from jga.core.domain.beat_reference import BeatReference
from jga.core.domain.elementary_metric_event import ElementaryMetricEvent
from jga.core.domain.metric_cluster import MetricCluster
from jga.core.domain.pulse import Pulse


def make_beat() -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.0,
        created_at=datetime.now(),
    )


def make_cluster() -> MetricCluster:
    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.0,
        confidence=0.95,
        created_at=datetime.now(),
    )

    return MetricCluster(
        id=uuid4(),
        beat_reference=make_beat(),
        events=(event,),
        created_at=datetime.now(),
    )


def make_pulse() -> Pulse:
    return Pulse(
        id=uuid4(),
        index=0,
        cluster=make_cluster(),
        timestamp=1.0,
        created_at=datetime.now(),
    )


def test_create_valid_pulse():
    pulse = make_pulse()

    assert pulse.index == 0
    assert pulse.timestamp == 1.0


def test_pulse_is_immutable():
    pulse = make_pulse()

    with pytest.raises(AttributeError):
        pulse.index = 10


def test_negative_index_raises():
    with pytest.raises(ValueError):
        Pulse(
            id=uuid4(),
            index=-1,
            cluster=make_cluster(),
            timestamp=1.0,
            created_at=datetime.now(),
        )


def test_negative_timestamp_raises():
    with pytest.raises(ValueError):
        Pulse(
            id=uuid4(),
            index=0,
            cluster=make_cluster(),
            timestamp=-0.5,
            created_at=datetime.now(),
        )