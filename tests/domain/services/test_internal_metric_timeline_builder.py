from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.services.internal_metric_timeline_builder import (
    InternalMetricTimelineBuilder,
)


def make_event(timestamp: float) -> ElementaryMetricEvent:

    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
    )


def make_pulse(
    timestamp: float,
    index: int = 0,
) -> Pulse:

    beat = BeatReference(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
    )

    cluster = MetricCluster(
        id=uuid4(),
        beat_reference=beat,
        events=(
            make_event(timestamp),
        ),
        created_at=datetime.now(),
    )

    return Pulse(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        cluster=cluster,
        created_at=datetime.now(),
    )


def test_builder_can_be_instantiated():

    assert InternalMetricTimelineBuilder() is not None


def test_build_requires_argument():

    builder = InternalMetricTimelineBuilder()

    with pytest.raises(TypeError):
        builder.build()


def test_empty_input_raises_value_error():

    builder = InternalMetricTimelineBuilder()

    with pytest.raises(ValueError):
        builder.build(())


def test_single_pulse_creates_timeline():

    builder = InternalMetricTimelineBuilder()

    pulse = make_pulse(
        timestamp=1.000,
        index=0,
    )

    timeline = builder.build((pulse,))

    assert len(timeline.pulses) == 1
    assert timeline.pulses[0] is pulse


def test_multiple_pulses_create_timeline():

    builder = InternalMetricTimelineBuilder()

    pulse1 = make_pulse(1.000, 1)
    pulse2 = make_pulse(2.000, 2)
    pulse3 = make_pulse(3.000, 3)

    timeline = builder.build(
        (
            pulse1,
            pulse2,
            pulse3,
        )
    )

    assert len(timeline.pulses) == 3

    assert timeline.pulses[0] is pulse1
    assert timeline.pulses[1] is pulse2
    assert timeline.pulses[2] is pulse3


def test_build_preserves_input_order():

    builder = InternalMetricTimelineBuilder()

    pulse3 = make_pulse(3.000, 3)
    pulse1 = make_pulse(1.000, 1)
    pulse2 = make_pulse(2.000, 2)

    timeline = builder.build(
        (
            pulse3,
            pulse1,
            pulse2,
        )
    )

    assert [pulse.index for pulse in timeline.pulses] == [
        3,
        1,
        2,
    ]


def test_build_large_number_of_pulses():

    builder = InternalMetricTimelineBuilder()

    pulses = tuple(
        make_pulse(
            float(i),
            i,
        )
        for i in range(100)
    )

    timeline = builder.build(pulses)

    assert len(timeline.pulses) == 100

    assert timeline.pulses[0].index == 0
    assert timeline.pulses[-1].index == 99

    assert timeline.pulses[0] is pulses[0]
    assert timeline.pulses[-1] is pulses[-1]

def test_none_pulse_raises_value_error():

    builder = InternalMetricTimelineBuilder()

    with pytest.raises(ValueError):
        builder.build((None,))


def test_non_pulse_object_raises_type_error():

    builder = InternalMetricTimelineBuilder()

    with pytest.raises(TypeError):
        builder.build(("not-a-pulse",))
