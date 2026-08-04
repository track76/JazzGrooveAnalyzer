from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.services.beat_period_estimator import (
    BeatPeriodEstimator,
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
    assert BeatPeriodEstimator() is not None


def test_estimate_requires_events():
    estimator = BeatPeriodEstimator()

    with pytest.raises(TypeError):
        estimator.estimate()


def test_less_than_two_events_returns_none():

    estimator = BeatPeriodEstimator()

    assert estimator.estimate(
        (
            make_event(1.000),
        )
    ) is None


def test_two_events_estimate_period():

    estimator = BeatPeriodEstimator()

    period = estimator.estimate(
        (
            make_event(1.000),
            make_event(1.500),
        )
    )

    assert period == 0.500


def test_estimate_average_period_from_multiple_events():

    estimator = BeatPeriodEstimator()

    period = estimator.estimate(
        (
            make_event(1.000),
            make_event(1.500),
            make_event(2.020),
            make_event(2.510),
        )
    )

    assert period == pytest.approx(
        (0.500 + 0.520 + 0.490) / 3,
    )
