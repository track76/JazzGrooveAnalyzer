"""
Tests for DummyMultiStemSeparator.
"""

from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_context import AnalysisContext
from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def _create_context() -> AnalysisContext:
    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.zeros(1024, dtype=float),
        sample_rate=44100,
        duration=1.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(audio=audio)
    context.processed_audio = np.zeros(1024, dtype=float)

    return context


def test_dummy_separator_creates_expected_audio_stems():
    context = _create_context()

    separator = DummyMultiStemSeparator()

    context = separator.process(context)

    assert context.audio_stems is not None
    assert len(context.audio_stems) == 7

    names = [stem.name for stem in context.audio_stems]

    assert names == [
        "Bass",
        "Piano",
        "Ride",
        "Hi-Hat",
        "Snare",
        "Kick",
        "Trumpet",
    ]


def test_dummy_separator_logs_runtime_event():
    context = _create_context()

    separator = DummyMultiStemSeparator()

    context = separator.process(context)

    event = context.log.entries[-1]

    assert event.event_id == "AUDIO_STEMS_CREATED"
    assert event.layer == "SEPARATION"
    assert event.component == "DummyMultiStemSeparator"
    assert event.metrics["stems"] == 7
