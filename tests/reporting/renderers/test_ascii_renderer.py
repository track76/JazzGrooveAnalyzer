from jga.reporting.analytical_bar import AnalyticalBar
from jga.reporting.analytical_beat import AnalyticalBeat
from jga.reporting.analytical_cell import AnalyticalCell
from jga.reporting.analytical_score import AnalyticalScore
from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)


def test_renderer():

    cell = AnalyticalCell(
        instrument="Bass",
        beat=1,
        metric_cluster_id=1,
        absolute_time_seconds=0.0,
        internal_bpm=120.0,
        offset_ms=12.3,
        delta_ms=0.2,
        significant_change=False,
    )

    beat = AnalyticalBeat(
        number=1,
        cells=(cell,),
    )

    bar = AnalyticalBar(
        number=1,
        start_time_seconds=0.0,
        end_time_seconds=2.0,
        time_signature="4/4",
        internal_bpm=120.0,
        beats=(beat,),
    )

    score = AnalyticalScore(
        title="Test",
        artist="Unknown",
        bars=(bar,),
    )

    renderer = AnalyticalScoreAsciiRenderer()

    text = renderer.render(score)

    assert "BAR 1" in text
    assert "Bass" in text
    assert "+12.30" in text
