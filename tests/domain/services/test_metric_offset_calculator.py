from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)
from jga.domain.services.metric_offset_calculator import (
    MetricOffsetCalculator,
)


def test_zero_offset():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=10.0,
        created_at=datetime.now(),
    )

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=10.0,
        confidence=1.0,
        created_at=datetime.now(),
    )

    calculator = MetricOffsetCalculator()

    assert calculator.compute(event, beat) == pytest.approx(0.0)


def test_positive_offset():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=10.000,
        created_at=datetime.now(),
    )

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=10.012,
        confidence=1.0,
        created_at=datetime.now(),
    )

    calculator = MetricOffsetCalculator()

    assert calculator.compute(event, beat) == pytest.approx(12.0)


def test_negative_offset():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=10.000,
        created_at=datetime.now(),
    )

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=9.992,
        confidence=1.0,
        created_at=datetime.now(),
    )

    calculator = MetricOffsetCalculator()

    assert calculator.compute(event, beat) == pytest.approx(-8.0)


from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)


def test_offset_is_computed_against_projected_beat():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.500,
        created_at=datetime.now(),
    )

    event = ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=1.530,
        confidence=1.0,
        created_at=datetime.now(),
    )

    offset = MetricOffsetCalculator().compute(
        event,
        beat,
    )

    assert offset == pytest.approx(30.0)
