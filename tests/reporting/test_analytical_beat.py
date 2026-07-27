from jga.reporting.analytical_beat import (
    AnalyticalBeat,
)


def test_creation():

    beat = AnalyticalBeat(

        number=1,

        timestamp_seconds=0.5,

        cells=(),

    )

    assert beat.number == 1

    assert beat.timestamp_seconds == 0.5

    assert beat.cells == ()
