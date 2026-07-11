from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference


def test_create_valid_beat_reference():

    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=0.000,
        created_at=datetime.now(),
    )

    assert beat.index == 0
    assert beat.timestamp == 0.000


def test_is_immutable():

    beat = BeatReference(
        id=uuid4(),
        index=1,
        timestamp=1.000,
        created_at=datetime.now(),
    )

    with pytest.raises(Exception):
        beat.index = 10


def test_negative_index_raises():

    with pytest.raises(ValueError):
        BeatReference(
            id=uuid4(),
            index=-1,
            timestamp=0.000,
            created_at=datetime.now(),
        )


def test_negative_timestamp_raises():

    with pytest.raises(ValueError):
        BeatReference(
            id=uuid4(),
            index=0,
            timestamp=-0.001,
            created_at=datetime.now(),
        )