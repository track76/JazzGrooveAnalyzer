from jga.visualization.metric_event import (
    MetricEvent,
)


def test_metric_event_can_be_created():

    event = MetricEvent(
        beat_index=2,
        offset_ms=-8.5,
    )

    assert event.beat_index == 2

    assert event.offset_ms == -8.5
