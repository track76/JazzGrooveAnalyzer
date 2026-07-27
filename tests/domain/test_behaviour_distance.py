from jga.domain.behaviour_distance import (
    BehaviourDistance,
)


def test_creation():

    distance = BehaviourDistance(
        physical_distance_ms=12.5,
        metric_distance=0.08,
        normalised_distance=0.11,
        confidence=1.0,
    )

    assert distance.physical_distance_ms == 12.5
    assert distance.metric_distance == 0.08
    assert distance.normalised_distance == 0.11
    assert distance.confidence == 1.0

