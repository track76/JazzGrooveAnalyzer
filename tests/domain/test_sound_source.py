from datetime import datetime
from uuid import uuid4

import pytest

from jga.core.domain.sound_source import SoundSource


def test_create_valid_sound_source():
    source = SoundSource(
        id=uuid4(),
        name="Double Bass",
        family="Strings",
        description="Jazz double bass",
        created_at=datetime.now(),
    )

    assert source.name == "Double Bass"
    assert source.family == "Strings"
    assert source.description == "Jazz double bass"


def test_empty_name_raises():
    with pytest.raises(ValueError):
        SoundSource(
            id=uuid4(),
            name="",
            family="Strings",
            description=None,
            created_at=datetime.now(),
        )


def test_empty_family_raises():
    with pytest.raises(ValueError):
        SoundSource(
            id=uuid4(),
            name="Double Bass",
            family="",
            description=None,
            created_at=datetime.now(),
        )