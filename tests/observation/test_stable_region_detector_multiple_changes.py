from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


def test_multiple_changes_create_multiple_regions():

    detector = StableRegionDetector()

    frames = (
        BehaviourObservationFrame(
            time=0.0,
            physical_offset_ms=0.0,
            metric_offset=0.0,
            internal_bpm=120.0,
            stability=1.0,
        ),
        BehaviourObservationFrame(
            time=1.0,
            physical_offset_ms=0.0,
            metric_offset=0.0,
            internal_bpm=120.0,
            stability=1.0,
        ),
        BehaviourObservationFrame(
            time=2.0,
            physical_offset_ms=5.0,
            metric_offset=0.0,
            internal_bpm=120.0,
            stability=1.0,
        ),
        BehaviourObservationFrame(
            time=3.0,
            physical_offset_ms=10.0,
            metric_offset=0.0,
            internal_bpm=120.0,
            stability=1.0,
        ),
    )

    events = detector.detect(frames)

    assert len(events) == 3
