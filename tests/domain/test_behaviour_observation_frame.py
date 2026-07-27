from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)


def test_creation():

    frame = BehaviourObservationFrame(
        time=0.0,
        physical_offset_ms=12.0,
        metric_offset=0.04,
        internal_bpm=120.0,
        stability=0.98,
    )

    assert frame.time == 0.0
    assert frame.physical_offset_ms == 12.0
    assert frame.metric_offset == 0.04
    assert frame.internal_bpm == 120.0
    assert frame.stability == 0.98

