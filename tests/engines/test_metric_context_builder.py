from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.metric_segment import MetricSegment
from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment
from jga.engines.metric_context_builder import MetricContextBuilder
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


def make_metric_segment():

    return MetricSegment(
        periodicity=PeriodicitySegment(
            source=MetricSource(
                name="Ride",
                family="Percussion",
            ),
            start_time=0.0,
            end_time=2.0,
            mean_interval=0.5,
            stability=0.95,
            confidence=0.90,
        ),
        confidence=0.90,
    )


def test_metric_context_builder_creates_observable_context():

    context = make_context()

    context.metric_segments = [
        make_metric_segment()
    ]

    builder = MetricContextBuilder()

    context = builder.process(context)

    assert context.metric_context is not None
    assert len(context.metric_context.metric_segments) == 1
