from jga.domain.behaviour_distance import (
    BehaviourDistance,
)

from jga.domain.behaviour_distance_vector import (
    BehaviourDistanceVector,
)

from jga.domain.services.behaviour_distance_builder import (
    BehaviourDistanceBuilder,
)


def test_build_preserves_distance_dimensions():

    vector = BehaviourDistanceVector(
        physical=1.0,
        metric=2.0,
        stability=3.0,
        persistence=4.0,
        regularity=5.0,
    )

    distance = (
        BehaviourDistanceBuilder()
        .build(vector)
    )

    assert isinstance(
        distance,
        BehaviourDistance,
    )

    assert (
        distance.physical_distance_ms
        ==
        1.0
    )

    assert (
        distance.metric_distance
        ==
        2.0
    )
