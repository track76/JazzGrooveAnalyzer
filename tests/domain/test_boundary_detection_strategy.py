import inspect

from jga.domain.services.boundary_detection_strategy import (
    BoundaryDetectionStrategy,
)


def test_strategy_is_abstract():

    assert inspect.isabstract(BoundaryDetectionStrategy)


def test_detect_method_exists():

    assert hasattr(
        BoundaryDetectionStrategy,
        "detect",
    )
