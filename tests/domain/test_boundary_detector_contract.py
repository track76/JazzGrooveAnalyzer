import inspect

from jga.domain.services.boundary_detector import (
    BoundaryDetector,
)


def test_boundary_detector_is_abstract():

    assert inspect.isabstract(BoundaryDetector)


def test_detect_method_exists():

    assert hasattr(
        BoundaryDetector,
        "detect",
    )
