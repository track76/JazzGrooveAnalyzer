from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.pulse_candidate import PulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.engines.periodicity_discovery import PeriodicityDiscovery
from jga.runtime.analysis_context import AnalysisContext


def make_context():
    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([]),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        format="wav",
    )
    return AnalysisContext(audio=audio)


def test_builds_one_periodicity_segment():

    context = make_context()

    context.source_pulse_sequences = [
        SourcePulseSequence(
            source_name="Ride",
            pulse_candidates=[
                PulseCandidate(time=0.0, strength=1.0),
                PulseCandidate(time=0.5, strength=1.0),
                PulseCandidate(time=1.0, strength=1.0),
            ],
        )
    ]

    engine = PeriodicityDiscovery()

    context = engine.process(context)

    assert len(context.periodicity_segments) == 1

    segment = context.periodicity_segments[0]

    assert segment.start_time == 0.0
    assert segment.end_time == 1.0
    assert segment.mean_interval == 0.5
    assert segment.source.name == "Ride"
