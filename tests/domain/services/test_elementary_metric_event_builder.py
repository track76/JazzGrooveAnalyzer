from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate
from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)


def create_candidate_and_contributor():

    source_id = uuid4()

    candidate = PulseCandidate(
        id=uuid4(),
        sound_source_id=source_id,
        timestamp=1.25,
        confidence=0.9,
        created_at=datetime.now(),
    )

    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=source_id,
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )

    return candidate, contributor


def test_builder_can_be_instantiated():

    builder = ElementaryMetricEventBuilder()

    assert builder is not None


def test_build_requires_arguments():

    builder = ElementaryMetricEventBuilder()

    with pytest.raises(TypeError):
        builder.build()


def test_build_returns_empty_tuple():

    builder = ElementaryMetricEventBuilder()

    events = builder.build(
        (),
        (),
    )

    assert events == ()


def test_build_resolves_metric_contributor():

    builder = ElementaryMetricEventBuilder()

    candidate, contributor = create_candidate_and_contributor()

    events = builder.build(
        (candidate,),
        (contributor,),
    )

    assert len(events) == 1

    event = events[0]

    assert event.timestamp == candidate.timestamp
    assert event.confidence == candidate.confidence
    assert event.contributor_id == contributor.id


def test_build_multiple_events():

    builder = ElementaryMetricEventBuilder()

    candidate, contributor = create_candidate_and_contributor()

    candidates = tuple(
        PulseCandidate(
            id=uuid4(),
            sound_source_id=contributor.sound_source_id,
            timestamp=float(i),
            confidence=1.0,
            created_at=datetime.now(),
        )
        for i in range(5)
    )

    events = builder.build(
        candidates,
        (contributor,),
    )

    assert len(events) == 5
