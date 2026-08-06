from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_real_audio_creates_analytical_score():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert context.analytical_score is not None

    assert len(
        context.analytical_score.measures
    ) >= 0
