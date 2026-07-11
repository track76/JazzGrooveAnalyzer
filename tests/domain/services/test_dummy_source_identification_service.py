from datetime import datetime
from pathlib import Path
from uuid import uuid4

from jga.domain.audio_stem import AudioStem
from jga.domain.services.dummy_source_identification_service import (
    DummySourceIdentificationService,
)


def test_identify_creates_sound_source():

    service = DummySourceIdentificationService()

    stem = AudioStem(
        id=uuid4(),
        recording_id=uuid4(),
        name="bass",
        audio_path=Path("bass.wav"),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        created_at=datetime.now(),
    )

    sources = service.identify((stem,))

    assert len(sources) == 1
    assert sources[0].name == "bass"
    assert sources[0].family == "unknown"