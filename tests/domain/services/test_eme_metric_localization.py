from datetime import datetime
from decimal import Decimal
from uuid import NAMESPACE_URL, uuid4, uuid5

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.services.elementary_metric_event_association_service import (
    ElementaryMetricEventAssociationService,
)


def beat(index: int) -> BeatReference:
    timestamp = index * (10.0 / 13.0)
    return BeatReference(
        id=uuid5(NAMESPACE_URL, f"beat:{index}"),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
        exact_period_seconds=Decimal(10) / Decimal(13),
        exact_period_ratio="10/13",
    )


def event(timestamp: float, identity: str) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid5(NAMESPACE_URL, identity),
        contributor_id=uuid4(),
        sound_source_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
        supporting_pulse_candidate_ids=(uuid4(),),
    )


def test_multiple_events_in_one_quarter_remain_independently_localized():
    beats = (beat(0), beat(1), beat(2))
    events = (event(0.01, "a"), event(0.39, "b"))

    results = ElementaryMetricEventAssociationService().localize(events, beats)

    assert len(results) == len(events)
    assert all(item.outcome == "ASSOCIATED" for item in results)
    assert all(item.beat_reference_id == beats[0].id for item in results)
    assert tuple(item.elementary_metric_event_id for item in results) == tuple(
        item.id for item in events
    )
    assert results[0].normalized_phase == pytest.approx(0.013)
    assert results[1].normalized_phase == pytest.approx(0.507)


def test_identical_timestamps_preserve_distinct_event_identity():
    beats = (beat(0), beat(1))
    events = (event(0.2, "a"), event(0.2, "b"))

    results = ElementaryMetricEventAssociationService().localize(events, beats)

    assert len(results) == 2
    assert results[0].elementary_metric_event_id != results[1].elementary_metric_event_id
    assert results[0].normalized_phase == results[1].normalized_phase


def test_exact_reference_boundary_belongs_to_that_reference():
    beats = (beat(0), beat(1), beat(2))
    event_on_second = event(beats[1].timestamp, "boundary")

    result = ElementaryMetricEventAssociationService().localize(
        (event_on_second,), beats
    )[0]

    assert result.beat_reference_id == beats[1].id
    assert result.following_beat_reference_id == beats[2].id
    assert result.elapsed_seconds == 0.0
    assert result.normalized_phase == 0.0


def test_final_interval_localizes_without_following_in_scope_reference():
    beats = (beat(0), beat(1))
    final_event = event(beats[1].timestamp + 0.2, "final")

    result = ElementaryMetricEventAssociationService().localize(
        (final_event,), beats
    )[0]

    assert result.outcome == "ASSOCIATED"
    assert result.beat_reference_id == beats[1].id
    assert result.following_beat_reference_id is None
    assert result.normalized_phase == pytest.approx(0.26)
