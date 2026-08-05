from jga.visualization.measure import (
    Measure,
)

from jga.visualization.metric_event import (
    MetricEvent,
)

from jga.visualization.measure_timeline_builder import (
    MeasureTimelineBuilder,
)


def test_measure_timeline_normalizes_beats():

    measure = Measure(
        number=26,
        time_signature="4/4",
        bpm=120.0,
        metric_events=(
            MetricEvent(
                source_name="Mix",
                beat_index=100,
                absolute_time_seconds=99.834,
                offset_ms=6.4,
            ),
            MetricEvent(
                source_name="Mix",
                beat_index=101,
                absolute_time_seconds=100.090,
                offset_ms=-9.2,
            ),
        ),
    )

    timeline = (
        MeasureTimelineBuilder()
        .build(measure)
    )

    assert timeline.measure_number == 26
    assert timeline.beats == (100, 101)
    assert timeline.offsets_ms == (6.4, -9.2)
