from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.elementary_metric_event import ElementaryMetricEvent


def make_event() -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.234,
        confidence=0.95,
        created_at=datetime.now(),
    )


def test_create_valid_event():
    event = make_event()

    assert event.timestamp == 1.234
    assert event.confidence == 0.95


def test_is_immutable():
    event = make_event()

    with pytest.raises(AttributeError):
        event.timestamp = 2.0


def test_negative_timestamp_raises():
    with pytest.raises(ValueError):
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=-1.0,
            confidence=0.9,
            created_at=datetime.now(),
        )


def test_confidence_below_zero_raises():
    with pytest.raises(ValueError):
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=1.0,
            confidence=-0.1,
            created_at=datetime.now(),
        )


def test_confidence_above_one_raises():
    with pytest.raises(ValueError):
        ElementaryMetricEvent(
            id=uuid4(),
            contributor_id=uuid4(),
            timestamp=1.0,
            confidence=1.1,
            created_at=datetime.now(),
        )