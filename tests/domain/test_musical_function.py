from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.musical_function import MusicalFunction


def test_create_valid_musical_function():
    function = MusicalFunction(
        id=uuid4(),
        name="Walking Bass",
        description="Primary metric accompaniment",
        is_metric=True,
        created_at=datetime.now(),
    )

    assert function.name == "Walking Bass"
    assert function.is_metric is True


def test_metric_flag_false():
    function = MusicalFunction(
        id=uuid4(),
        name="Solo",
        description="Improvised solo",
        is_metric=False,
        created_at=datetime.now(),
    )

    assert function.is_metric is False


def test_empty_name_raises():
    with pytest.raises(ValueError):
        MusicalFunction(
            id=uuid4(),
            name="",
            description=None,
            is_metric=True,
            created_at=datetime.now(),
        )