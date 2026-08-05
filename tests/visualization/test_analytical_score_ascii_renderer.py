from jga.visualization.analytical_score import (
    AnalyticalScore,
)
from jga.visualization.ascii_analytical_score_renderer import (
    AsciiAnalyticalScoreRenderer,
)


def test_renderer_can_be_instantiated():

    assert AsciiAnalyticalScoreRenderer() is not None


def test_renderer_returns_text():

    score = AnalyticalScore(
        recording_title="I Fall In Love Too Easily",
        artist="Chet Baker",
        time_signature="4/4",
        average_bpm=124.0,
        sections=(),
        measures=(),
        instrument_lanes=(),
    )

    text = AsciiAnalyticalScoreRenderer().render(
        score,
    )

    assert isinstance(
        text,
        str,
    )
