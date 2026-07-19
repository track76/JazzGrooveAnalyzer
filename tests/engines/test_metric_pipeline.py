from pathlib import Path

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.pulse_candidate import PulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.core.metric_source import MetricSource

from jga.engines.periodicity_discovery import PeriodicityDiscovery
from jga.engines.metric_segment_builder import MetricSegmentBuilder
from jga.engines.metric_cluster_builder import MetricClusterBuilder

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


def test_metric_pipeline_end_to_end():

    context = make_context()

    context.source_pulse_sequences = [
        SourcePulseSequence(
            source=MetricSource(
                name="Ride",
                family="Unknown",
            ),
            pulse_candidates=[
                PulseCandidate(time=0.0, strength=1.0),
                PulseCandidate(time=0.5, strength=1.0),
                PulseCandidate(time=1.0, strength=1.0),
            ],
        )
    ]

    context = PeriodicityDiscovery().process(context)

    assert len(context.periodicity_segments) == 1

    context = MetricSegmentBuilder().process(context)

    assert len(context.metric_segments) == 1

    context = MetricClusterBuilder().process(context)

    assert len(context.metric_clusters) == 1
