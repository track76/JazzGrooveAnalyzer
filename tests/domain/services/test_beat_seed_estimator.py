from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.services.beat_seed_estimator import (
    BeatSeedEstimator,
)


def make_event(timestamp: float) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
    )


def test_estimator_can_be_instantiated():
    assert BeatSeedEstimator() is not None


def test_reconstruct_requires_events():
    estimator = BeatSeedEstimator()

    with pytest.raises(TypeError):
        estimator.estimate()


def test_empty_events_return_empty_tuple():
    estimator = BeatSeedEstimator()

    assert estimator.estimate(()) == ()


def test_single_event_returns_single_seed():

    estimator = BeatSeedEstimator()

    events = (
        make_event(1.250),
    )

    seeds = estimator.estimate(events)

    assert len(seeds) == 1

    assert seeds[0] == 1.250
