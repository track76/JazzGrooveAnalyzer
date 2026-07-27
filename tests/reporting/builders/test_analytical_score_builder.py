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

