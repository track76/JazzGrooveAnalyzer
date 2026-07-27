from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)


def test_creation():

    event = BehaviourChangeEvent(
        start_time=10.0,
        end_time=15.0,
        event_type="stable",
        intensity=0.0,
    )

    assert event.start_time == 10.0
    assert event.end_time == 15.0
    assert event.event_type == "stable"
    assert event.intensity == 0.0

