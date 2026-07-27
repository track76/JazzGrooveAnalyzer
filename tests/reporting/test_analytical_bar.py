from jga.reporting.analytical_bar import AnalyticalBar


def test_analytical_bar_contains_temporal_boundaries():
    bar = AnalyticalBar(
        number=1,
        start_time_seconds=0.0,
        end_time_seconds=1.92,
        time_signature="4/4",
        internal_bpm=125.0,
        beats=(),
    )

    assert bar.number == 1
    assert bar.start_time_seconds == 0.0
    assert bar.end_time_seconds == 1.92
    assert bar.time_signature == "4/4"
    assert bar.internal_bpm == 125.0
    assert bar.beats == ()
