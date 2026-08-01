from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


def test_single_frame_produces_one_stable_region():

    frame = BehaviourObservationFrame(
        time=0.0,
        physical_offset_ms=0.0,
        metric_offset=0.0,
        internal_bpm=120.0,
        stability=1.0,
    )

    detector = StableRegionDetector()

    events = detector.detect(
        (frame,),
    )

    assert len(events) == 1

    event = events[0]

    assert event.start_time == 0.0
    assert event.end_time == 0.0
    assert event.event_type == "stable_region"
