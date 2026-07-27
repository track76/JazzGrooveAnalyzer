from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)


def test_creation():

    event = BehaviourChangeEvent(
        start_time=0.0,
        end_time=2.5,
        event_type="stable",
        intensity=0.0,
    )

    assert event.start_time == 0.0
    assert event.end_time == 2.5
    assert event.event_type == "stable"
    assert event.intensity == 0.0
