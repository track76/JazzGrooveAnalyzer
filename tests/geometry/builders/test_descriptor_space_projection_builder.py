from jga.geometry.builders.descriptor_space_projection_builder import (
    DescriptorSpaceProjectionBuilder,
)

from jga.domain.descriptor_set import DescriptorSet

from tests.support.domain_objects import (
    make_behaviour_descriptor,
)


def test_descriptor_projection_preserves_values():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    result = (
        DescriptorSpaceProjectionBuilder()
        .build(descriptor_set)
    )

    assert len(result.coordinates) == 1

    assert (
        result.coordinates[0].name
        ==
        descriptor.name
    )

    assert (
        result.coordinates[0].value
        ==
        descriptor.value
    )
