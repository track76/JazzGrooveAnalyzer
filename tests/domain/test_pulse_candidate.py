from datetime import datetime
from uuid import uuid4

import pytest

from jga.core.domain.pulse_candidate import PulseCandidate


def test_create_valid_pulse_candidate():

    candidate = PulseCandidate(
        id=uuid4(),
        sound_source_id=uuid4(),
        timestamp=1.25,
        confidence=0.95,
        created_at=datetime.now(),
    )

    assert candidate.timestamp == 1.25
    assert candidate.confidence == 0.95


def test_is_immutable():

    candidate = PulseCandidate(
        id=uuid4(),
        sound_source_id=uuid4(),
        timestamp=1.0,
        confidence=0.9,
        created_at=datetime.now(),
    )

    with pytest.raises(AttributeError):
        candidate.timestamp = 2.0


def test_negative_timestamp_raises():

    with pytest.raises(ValueError):
        PulseCandidate(
            id=uuid4(),
            sound_source_id=uuid4(),
            timestamp=-1.0,
            confidence=0.9,
            created_at=datetime.now(),
        )


def test_confidence_below_zero_raises():

    with pytest.raises(ValueError):
        PulseCandidate(
            id=uuid4(),
            sound_source_id=uuid4(),
            timestamp=1.0,
            confidence=-0.1,
            created_at=datetime.now(),
        )


def test_confidence_above_one_raises():

    with pytest.raises(ValueError):
        PulseCandidate(
            id=uuid4(),
            sound_source_id=uuid4(),
            timestamp=1.0,
            confidence=1.1,
            created_at=datetime.now(),
        )