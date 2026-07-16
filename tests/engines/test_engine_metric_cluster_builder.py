from jga.core.metric_cluster import MetricCluster
from jga.core.metric_segment import MetricSegment
from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment

from jga.engines.metric_cluster_builder import MetricClusterBuilder
from jga.runtime.analysis_context import AnalysisContext
from jga.core.audio_file import AudioFile
from pathlib import Path

import numpy as np

def test_single_metric_segment_produces_one_cluster():

    source = MetricSource(
        name="Ride",
        family="Percussion",
    )

    periodicity = PeriodicitySegment(
        source=source,
        start_time=0.0,
        end_time=4.0,
        mean_interval=0.50,
        stability=0.95,
        confidence=0.90,
    )

    segment = MetricSegment(
        periodicity=periodicity,
        confidence=0.90,
    )


    audio = AudioFile(
        path=Path("dummy.wav"),
        raw_audio=np.array([]),
        sample_rate=44100,
        duration=4.0,
        channels=1,
        format="wav",
    )


    context = AnalysisContext(audio=audio)
    context.metric_segments = [segment]

    builder = MetricClusterBuilder()

    context = builder.process(context)

    assert len(context.metric_clusters) == 1

    cluster = context.metric_clusters[0]

    assert isinstance(cluster, MetricCluster)

    assert cluster.start_time == 0.0
    assert cluster.end_time == 4.0
