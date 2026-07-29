from jga.domain.descriptor_relation import (
    DescriptorRelation,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)

from jga.domain.services.descriptor_relation_builder import (
    DescriptorRelationBuilder,
)

from tests.support.domain_objects import (
    make_behaviour_descriptor,
)


def test_descriptor_relation_preserves_descriptors():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    relations = (
        DescriptorRelationBuilder()
        .build(descriptor_set)
    )

    assert len(relations) == 1

    assert isinstance(
        relations[0],
        DescriptorRelation,
    )

    assert (
        relations[0].descriptors
        ==
        descriptor_set.descriptors
    )


def test_descriptor_relation_is_immutable():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    relation = (
        DescriptorRelationBuilder()
        .build(descriptor_set)[0]
    )

    assert relation.descriptors[0] == descriptor
