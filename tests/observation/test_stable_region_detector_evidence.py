from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


def test_stable_region_detector_preserves_evidence():

    frames = (
        BehaviourObservationFrame(
            time=0.0,
            physical_offset_ms=1.0,
            metric_offset=0.1,
            internal_bpm=120.0,
            stability=0.9,
        ),
        BehaviourObservationFrame(
            time=1.0,
            physical_offset_ms=2.0,
            metric_offset=0.2,
            internal_bpm=120.5,
            stability=0.8,
        ),
    )

    detector = StableRegionDetector()

    result = detector.detect(frames)

    evidence = result.evidences

    assert len(evidence) == 1
    assert evidence[0].physical_offset_delta_ms == 1.0
