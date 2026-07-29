from jga.domain.services.defaults.default_boundary_detector import (
    DefaultBoundaryDetector,
)


def test_detector_returns_tuple():

    detector = DefaultBoundaryDetector()

    result = detector.detect(None)

    assert isinstance(result, tuple)


def test_detector_initially_returns_no_boundaries():

    detector = DefaultBoundaryDetector()

    assert detector.detect(None) == ()
