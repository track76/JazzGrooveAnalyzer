from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.metric_segment import MetricSegment
from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment

from jga.engines.metric_cluster_builder import MetricClusterBuilder
from jga.runtime.analysis_context import AnalysisContext


def make_segment(start, end, interval, stability):

    source = MetricSource(
        name="Ride",
        family="Percussion",
    )

    periodicity = PeriodicitySegment(
        source=source,
        start_time=start,
        end_time=end,
        mean_interval=interval,
        stability=stability,
        confidence=1.0,
    )

    return MetricSegment(
        periodicity=periodicity,
        confidence=1.0,
    )


def test_similar_segments_are_grouped():

    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([]),
        sample_rate=44100,
        duration=10.0,
        channels=1,
        format="wav",
    )

    context = AnalysisContext(audio=audio)

    context.metric_segments = [
        make_segment(0.0, 2.0, 0.500, 0.92),
        make_segment(2.0, 4.0, 0.501, 0.91),
    ]

    builder = MetricClusterBuilder()

    context = builder.process(context)

    assert len(context.metric_clusters) == 1
