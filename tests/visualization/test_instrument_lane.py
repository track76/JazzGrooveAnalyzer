from jga.visualization.instrument_lane import (
    InstrumentLane,
)


def test_instrument_lane_can_be_created():

    lane = InstrumentLane(
        name="Bass",
    )

    assert lane.name == "Bass"

from jga.visualization.metric_event import (
    MetricEvent,
)


def test_instrument_lane_contains_metric_events():

    events = (
        MetricEvent(
            beat_index=2,
            offset_ms=-8.0,
        ),
    )

    lane = InstrumentLane(
        name="Bass",
        metric_events=events,
    )

    assert lane.metric_events == events
