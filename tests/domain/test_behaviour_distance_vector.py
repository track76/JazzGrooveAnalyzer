from jga.domain.behaviour_distance_vector import (
    BehaviourDistanceVector,
)


def test_creation():

    vector = BehaviourDistanceVector(
        physical=1.0,
        metric=2.0,
        stability=3.0,
        persistence=4.0,
        regularity=5.0,
    )

    assert vector.physical == 1.0
    assert vector.metric == 2.0
    assert vector.stability == 3.0
    assert vector.persistence == 4.0
    assert vector.regularity == 5.0

