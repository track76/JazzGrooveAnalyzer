from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from jga.domain.audio_stem import AudioStem


def test_create_valid_audio_stem():
    stem = AudioStem(
        id=uuid4(),
        recording_id=uuid4(),
        name="Double Bass",
        audio_path=Path("bass.wav"),
        sample_rate=44100,
        duration=120.0,
        channels=1,
        created_at=datetime.now(),
    )

    assert stem.name == "Double Bass"
    assert stem.sample_rate == 44100
    assert stem.duration == 120.0
    assert stem.channels == 1


def test_empty_name_raises():
    with pytest.raises(ValueError):
        AudioStem(
            id=uuid4(),
            recording_id=uuid4(),
            name="",
            audio_path=Path("bass.wav"),
            sample_rate=44100,
            duration=120.0,
            channels=1,
            created_at=datetime.now(),
        )


def test_negative_duration_raises():
    with pytest.raises(ValueError):
        AudioStem(
            id=uuid4(),
            recording_id=uuid4(),
            name="Bass",
            audio_path=Path("bass.wav"),
            sample_rate=44100,
            duration=-1.0,
            channels=1,
            created_at=datetime.now(),
        )


def test_zero_sample_rate_raises():
    with pytest.raises(ValueError):
        AudioStem(
            id=uuid4(),
            recording_id=uuid4(),
            name="Bass",
            audio_path=Path("bass.wav"),
            sample_rate=0,
            duration=120.0,
            channels=1,
            created_at=datetime.now(),
        )


def test_zero_channels_raises():
    with pytest.raises(ValueError):
        AudioStem(
            id=uuid4(),
            recording_id=uuid4(),
            name="Bass",
            audio_path=Path("bass.wav"),
            sample_rate=44100,
            duration=120.0,
            channels=0,
            created_at=datetime.now(),
        )