from pathlib import Path

from jga.domain.audio_recording import (
    AudioRecording,
)

from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)

from jga.reporting.builders.analytical_score_builder import (
    AnalyticalScoreBuilder,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)


def test_builder():

    recording = AudioRecording.create(
        path=Path("demo.wav"),
        sample_rate=44100,
        channels=2,
        duration_seconds=0.0,
    )

    context = AnalysisContext(
        audio=recording,
    )

    score = AnalyticalScoreBuilder().build(
        context,
    )

    assert score.recording_title == "demo.wav"


def test_builder_populates_measures_from_reconstructed_measures():

    recording = AudioRecording.create(
        path=Path("demo.wav"),
        sample_rate=44100,
        channels=2,
        duration_seconds=10.0,
    )

    context = AnalysisContext(
        audio=recording,
        reconstructed_measures=(
            ReconstructedMeasure(
                number=1,
                time_signature="4/4",
                internal_bpm=120.0,
                start_time_seconds=0.0,
                end_time_seconds=2.0,
                beat_references=(),
                metric_clusters=(),
            ),
            ReconstructedMeasure(
                number=2,
                time_signature="4/4",
                internal_bpm=120.0,
                start_time_seconds=2.0,
                end_time_seconds=4.0,
                beat_references=(),
                metric_clusters=(),
            ),
        ),
    )

    score = AnalyticalScoreBuilder().build(
        context,
    )

    assert len(score.measures) == 2

    assert score.measures[0].number == 1

    assert score.measures[0].start_time_seconds == 0.0

    assert score.measures[1].start_time_seconds == 2.0
