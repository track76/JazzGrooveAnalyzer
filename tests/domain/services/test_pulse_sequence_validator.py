from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.services.pulse_sequence_validator import (
    PulseSequenceValidator,
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
    index: int,
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


def test_validator_can_be_instantiated():

    assert PulseSequenceValidator() is not None


def test_empty_sequence_raises_value_error():

    validator = PulseSequenceValidator()

    with pytest.raises(ValueError):
        validator.validate(())


def test_none_pulse_raises_value_error():

    validator = PulseSequenceValidator()

    with pytest.raises(ValueError):
        validator.validate((None,))


def test_non_pulse_object_raises_type_error():

    validator = PulseSequenceValidator()

    with pytest.raises(TypeError):
        validator.validate(("not-a-pulse",))


def test_valid_sequence_passes():

    validator = PulseSequenceValidator()

    validator.validate(
        (
            make_pulse(1.0, 0),
            make_pulse(2.0, 1),
        )
    )


def test_decreasing_timestamp_raises_value_error():

    validator = PulseSequenceValidator()

    with pytest.raises(ValueError):
        validator.validate(
            (
                make_pulse(2.0, 0),
                make_pulse(1.0, 1),
            )
        )
