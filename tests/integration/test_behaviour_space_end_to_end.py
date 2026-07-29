from jga.domain.descriptor_set import DescriptorSet

from jga.geometry.builders.descriptor_behaviour_space_builder import (
    DescriptorBehaviourSpaceBuilder,
)

from jga.domain.services.behaviour_space_comparison_builder import (
    BehaviourSpaceComparisonBuilder,
)

from jga.domain.services.behaviour_distance_builder import (
    BehaviourDistanceBuilder,
)

from jga.domain.behaviour_distance_vector import (
    BehaviourDistanceVector,
)

from tests.support.domain_objects import (
    make_behaviour_descriptor,
)


def test_behaviour_space_complete_flow():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    builder = DescriptorBehaviourSpaceBuilder()

    first_space = builder.build(
        descriptor_set
    )

    second_space = builder.build(
        descriptor_set
    )

    comparison = (
        BehaviourSpaceComparisonBuilder()
        .build(
            first_space,
            second_space,
        )
    )

    assert comparison.comparable


    vector = BehaviourDistanceVector(
        physical=0.0,
        metric=0.0,
        stability=0.0,
        persistence=0.0,
        regularity=0.0,
    )

    distance = (
        BehaviourDistanceBuilder()
        .build(vector)
    )

    assert distance.physical_distance_ms == 0.0
    assert distance.metric_distance == 0.0
