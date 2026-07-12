from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)


def test_builder_can_be_instantiated():
    builder = ElementaryMetricEventBuilder()

    assert builder is not None


def test_build_requires_argument():
    builder = ElementaryMetricEventBuilder()

    with pytest.raises(TypeError):
        builder.build()


def test_build_returns_empty_tuple_when_no_intervals():
    builder = ElementaryMetricEventBuilder()

    events = builder.build(())

    assert events == ()
from datetime import datetime
from uuid import uuid4

from jga.domain.pulse_candidate import PulseCandidate


def test_build_creates_one_event():

    builder = ElementaryMetricEventBuilder()

    candidate = PulseCandidate(
        id=uuid4(),
        sound_source_id=uuid4(),
        timestamp=1.25,
        confidence=0.9,
        created_at=datetime.now(),
    )

    events = builder.build((candidate,))

    assert len(events) == 1

    event = events[0]

    assert event.timestamp == candidate.timestamp
    assert event.confidence == candidate.confidence
    assert event.contributor_id == candidate.sound_source_id


def test_build_creates_multiple_events():

    builder = ElementaryMetricEventBuilder()

    candidates = tuple(
        PulseCandidate(
            id=uuid4(),
            sound_source_id=uuid4(),
            timestamp=float(i),
            confidence=1.0,
            created_at=datetime.now(),
        )
        for i in range(5)
    )

    events = builder.build(candidates)

    assert len(events) == 5
