from jga.domain.services.strategies.continuity_boundary_detection_strategy import (
    ContinuityBoundaryDetectionStrategy,
)


def test_strategy_returns_tuple():

    strategy = ContinuityBoundaryDetectionStrategy()

    result = strategy.detect(None)

    assert isinstance(result, tuple)


def test_initial_strategy_returns_no_boundaries():

    strategy = ContinuityBoundaryDetectionStrategy()

    assert strategy.detect(None) == ()
