from jga.visualization.metric_event import (
    MetricEvent,
)


def test_metric_event_can_be_created():

    event = MetricEvent(
        source_name="Double Bass",
        beat_index=2,
        absolute_time_seconds=0.482,
        offset_ms=-8.5,
    )

    assert event.source_name == "Double Bass"

    assert event.beat_index == 2

    assert event.absolute_time_seconds == 0.482

    assert event.offset_ms == -8.5
