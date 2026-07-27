from pathlib import Path

from jga.domain.audio_recording import (
    AudioRecording,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.reporting.builders.analytical_score_builder import (
    AnalyticalScoreBuilder,
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

    builder = AnalyticalScoreBuilder()

    score = builder.build(
        context,
    )

    assert score.title == "demo.wav"



def test_builder_populates_bars_from_reconstructed_measures():

    from jga.domain.reconstructed_measure import (
        ReconstructedMeasure,
    )


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


    builder = AnalyticalScoreBuilder()


    score = builder.build(
        context,
    )


    assert len(score.bars) == 2

    assert score.bars[0].number == 1

    assert score.bars[0].start_time_seconds == 0.0

    assert score.bars[1].end_time_seconds == 4.0
