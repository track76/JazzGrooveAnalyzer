from jga.reporting.builders.analytical_bar_builder import (
    AnalyticalBarBuilder,
)


def test_build():

    builder = AnalyticalBarBuilder()

    bar = builder.build(

        number=1,

        time_seconds=0.0,

        time_signature="4/4",

        internal_bpm=120.0,

    )

    assert bar.number == 1

    assert bar.internal_bpm == 120.0

    assert len(bar.beats) == 0

