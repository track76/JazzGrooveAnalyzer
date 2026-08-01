from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


def test_change_creates_two_stable_regions():

    frame1 = BehaviourObservationFrame(
        time=0.0,
        physical_offset_ms=0.0,
        metric_offset=0.0,
        internal_bpm=120.0,
        stability=1.0,
    )

    frame2 = BehaviourObservationFrame(
        time=1.0,
        physical_offset_ms=0.0,
        metric_offset=0.0,
        internal_bpm=120.0,
        stability=1.0,
    )

    frame3 = BehaviourObservationFrame(
        time=2.0,
        physical_offset_ms=10.0,
        metric_offset=0.0,
        internal_bpm=120.0,
        stability=1.0,
    )

    detector = StableRegionDetector()

    events = detector.detect(
        (
            frame1,
            frame2,
            frame3,
        )
    )

    assert len(events) == 2

    assert events[0].start_time == 0.0
    assert events[0].end_time == 1.0

    assert events[1].start_time == 2.0
    assert events[1].end_time == 2.0
