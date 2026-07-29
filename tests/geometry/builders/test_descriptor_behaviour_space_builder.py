from jga.geometry.builders.descriptor_behaviour_space_builder import (
    DescriptorBehaviourSpaceBuilder,
)

from jga.domain.descriptor_set import DescriptorSet

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)

from tests.support.domain_objects import (
    make_behaviour_descriptor,
)


def test_descriptor_set_builds_behaviour_space():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    space = (
        DescriptorBehaviourSpaceBuilder()
        .build(descriptor_set)
    )

    assert isinstance(
        space,
        ScientificBehaviourSpace,
    )

    assert space.trajectory_count == 1

    assert (
        space.first_trajectory.point_count
        ==
        1
    )

    assert (
        space.first_trajectory
        .first_point
        .coordinates[0]
        .value
        ==
        descriptor.value
    )
