from jga.observation.stable_region_detector import (
    StableRegionDetector,
)


def test_empty_sequence_returns_no_events():

    detector = StableRegionDetector()

    events = detector.detect(())

    assert events == ()
