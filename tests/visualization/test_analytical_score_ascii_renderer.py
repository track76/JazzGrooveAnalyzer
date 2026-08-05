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


def test_renderer_shows_real_metric_events():

    from jga.visualization.analytical_score import AnalyticalScore
    from jga.visualization.instrument_lane import InstrumentLane
    from jga.visualization.metric_event import MetricEvent
    from jga.visualization.ascii_analytical_score_renderer import (
        AsciiAnalyticalScoreRenderer,
    )

    event = MetricEvent(
        source_name="Double Bass",
        beat_index=1,
        absolute_time_seconds=0.482,
        offset_ms=-8.0,
    )

    score = AnalyticalScore(
        recording_title="Test",
        artist="Test",
        time_signature="4/4",
        average_bpm=124.0,
        sections=(),
        measures=(),
        instrument_lanes=(
            InstrumentLane(
                name="Double Bass",
                metric_events=(event,),
            ),
        ),
    )

    output = AsciiAnalyticalScoreRenderer().render(score)

    assert "Double Bass" in output
    assert "-8.0" in output

