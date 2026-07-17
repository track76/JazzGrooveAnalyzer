from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment
from jga.engines.metric_segment_builder import MetricSegmentBuilder
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


def test_builds_metric_segment_from_periodicity_segment():

    context = make_context()

    context.periodicity_segments = [
        PeriodicitySegment(
            source=MetricSource(
                name="Ride",
                family="Percussion",
            ),
            start_time=0.0,
            end_time=2.0,
            mean_interval=0.5,
            stability=0.95,
            confidence=0.90,
        )
    ]

    builder = MetricSegmentBuilder()

    context = builder.process(context)

    assert len(context.metric_segments) == 1

    segment = context.metric_segments[0]

    assert segment.periodicity is context.periodicity_segments[0]
    assert segment.confidence == 0.90
    assert segment.duration == 2.0
