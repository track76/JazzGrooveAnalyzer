from jga.visualization.analytical_score import (
    AnalyticalScore,
)
from jga.visualization.analytical_score_builder import (
    AnalyticalScoreBuilder,
)


def test_builder_can_be_instantiated():

    assert AnalyticalScoreBuilder() is not None


def test_builder_exposes_build_method():

    builder = AnalyticalScoreBuilder()

    assert callable(builder.build)


def test_build_returns_analytical_score():

    builder = AnalyticalScoreBuilder()

    score = builder.build()

    assert isinstance(
        score,
        AnalyticalScore,
    )


def test_analytical_score_contains_recording_information():

    score = AnalyticalScoreBuilder().build()

    assert score.recording_title == ""
    assert score.time_signature == "4/4"
    assert score.average_bpm == 120.0
