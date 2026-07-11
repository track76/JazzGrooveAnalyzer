from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse


def make_beat(index: int = 0) -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=index,
        timestamp=float(index),
        created_at=datetime.now(),
    )


def make_pulse(index: int = 0) -> Pulse:
    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=float(index),
        confidence=0.95,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=make_beat(index),
        events=(event,),
        created_at=datetime.now(),
    )

    return Pulse(
        id=uuid4(),
        index=index,
        cluster=cluster,
        timestamp=float(index),
        created_at=datetime.now(),
    )


def make_timeline() -> InternalMetricTimeline:
    return InternalMetricTimeline(
        id=uuid4(),
        pulses=(make_pulse(0),),
        created_at=datetime.now(),
    )


def test_create_valid_timeline():
    timeline = make_timeline()

    assert timeline.pulse_count == 1


def test_first_and_last_pulse():
    timeline = InternalMetricTimeline(
        id=uuid4(),
        pulses=(
            make_pulse(0),
            make_pulse(1),
            make_pulse(2),
        ),
        created_at=datetime.now(),
    )

    assert timeline.first_pulse.index == 0
    assert timeline.last_pulse.index == 2


def test_timeline_is_immutable():
    timeline = make_timeline()

    with pytest.raises(AttributeError):
        timeline.pulses = (make_pulse(0),)


def test_empty_timeline_raises():
    with pytest.raises(ValueError):
        InternalMetricTimeline(
            id=uuid4(),
            pulses=(),
            created_at=datetime.now(),
        )