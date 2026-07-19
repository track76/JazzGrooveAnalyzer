from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.internal_metric_timeline import InternalMetricTimeline
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.services.internal_metric_timeline_reconstructor import (
    InternalMetricTimelineReconstructor,
)


def make_event(timestamp: float) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
    )


def make_pulse(timestamp: float, index: int) -> Pulse:
    beat = BeatReference(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(make_event(timestamp),),
        created_at=datetime.now(),
    )

    return Pulse(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        cluster=cluster,
        created_at=datetime.now(),
    )


def test_reconstructor_can_be_instantiated():

    assert InternalMetricTimelineReconstructor() is not None


def test_reconstruct_returns_internal_metric_timeline():

    reconstructor = InternalMetricTimelineReconstructor()

    timeline = reconstructor.reconstruct(
        (
            make_pulse(1.0, 0),
            make_pulse(2.0, 1),
        )
    )

    assert isinstance(
        timeline,
        InternalMetricTimeline,
    )


def test_invalid_sequence_raises_value_error():

    reconstructor = InternalMetricTimelineReconstructor()

    with pytest.raises(ValueError):
        reconstructor.reconstruct(())


def test_projection_preserves_pulse_identity():

    reconstructor = InternalMetricTimelineReconstructor()

    pulse1 = make_pulse(1.0, 0)
    pulse2 = make_pulse(2.0, 1)

    timeline = reconstructor.reconstruct(
        (
            pulse1,
            pulse2,
        )
    )

    assert timeline.pulses[0] is pulse1
    assert timeline.pulses[1] is pulse2


def test_projection_returns_new_tuple():

    reconstructor = InternalMetricTimelineReconstructor()

    pulses = (
        make_pulse(1.0, 0),
        make_pulse(2.0, 1),
    )

    projected = reconstructor._project(pulses)

    assert projected is pulses
