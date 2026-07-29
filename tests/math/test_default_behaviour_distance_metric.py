from jga.domain.behaviour_distance import BehaviourDistance
from jga.math.defaults.default_behaviour_distance_metric import (
    DefaultBehaviourDistanceMetric,
)


def test_compute_returns_behaviour_distance():

    metric = DefaultBehaviourDistanceMetric()

    result = metric.compute(None, None)

    assert isinstance(result, BehaviourDistance)


def test_default_distance_is_neutral():

    metric = DefaultBehaviourDistanceMetric()

    result = metric.compute(None, None)

    assert result.physical_distance_ms == 0.0
    assert result.metric_distance == 0.0
    assert result.normalised_distance == 0.0
    assert result.confidence == 1.0
