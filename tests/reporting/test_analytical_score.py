from jga.reporting.analytical_bar import (
    AnalyticalBar,
)

from jga.reporting.analytical_beat import (
    AnalyticalBeat,
)

from jga.reporting.analytical_cell import (
    AnalyticalCell,
)

from jga.reporting.analytical_score import (
    AnalyticalScore,
)


def test_creation():

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

        artist="Test",

        bars=(bar,),

    )

    assert (
        score
        .bars[0]
        .beats[0]
        .cells[0]
        .offset_ms
        == 12.3
    )
