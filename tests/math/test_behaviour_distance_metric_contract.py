import inspect

from jga.math.behaviour_distance_metric import (
    BehaviourDistanceMetric,
)


def test_behaviour_distance_metric_is_abstract():

    assert inspect.isabstract(
        BehaviourDistanceMetric,
    )


def test_compute_method_exists():

    assert hasattr(
        BehaviourDistanceMetric,
        "compute",
    )
