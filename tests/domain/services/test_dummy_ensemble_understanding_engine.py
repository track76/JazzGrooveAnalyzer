from pathlib import Path

from jga.domain.audio_recording import AudioRecording
from jga.domain.services.dummy_ensemble_understanding_engine import (
    DummyEnsembleUnderstandingEngine,
)


def test_dummy_engine():

    engine = DummyEnsembleUnderstandingEngine()

    recording = AudioRecording.create(
        path=Path("dummy.wav"),
        sample_rate=44100,
        channels=2,
        duration_seconds=10.0,
    )

    profile = engine.analyze(recording)

    assert profile.meter == "4/4"