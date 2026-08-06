from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.metric_context import MetricContext
from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.engines.validation_dataset_runner import (
    ValidationDatasetRunner,
)


def test_runner_creates_dataset():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([], dtype=float),
        sample_rate=44100,
        duration=12.5,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(audio=audio)

    context.metric_context = MetricContext(
        source_pulse_sequences=(
            SourcePulseSequence(
                source=MetricSource(
                    name="Ride",
                    family="Percussion",
                ),
                pulse_candidates=[
                    PulseCandidate(
                        time=1.25,
                        strength=0.82,
                        confidence=0.97,
                    ),
                ],
            ),
        ),
        periodicity_segments=(),
        metric_segments=(),
    )

    ValidationDatasetRunner().run(context)

    dataset = context.validation_dataset

    assert dataset is not None
    assert dataset.metadata.sample_rate == 44100
    assert dataset.source.recording_name == "dummy.wav"
    assert len(dataset.observations) == 1

    record = dataset.observations[0]

    assert record.timestamp == 1.25
    assert record.source == "Ride"
