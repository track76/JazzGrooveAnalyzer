from jga.domain.analytical_structure import (
    AnalyticalStructure,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)

from jga.domain.services.default_descriptor_algebra import (
    DefaultDescriptorAlgebra,
)

from tests.support.domain_objects import (
    make_behaviour_descriptor,
)


def test_descriptor_algebra_preserves_descriptor_set():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    result = (
        DefaultDescriptorAlgebra()
        .analyze(descriptor_set)
    )

    assert isinstance(
        result,
        AnalyticalStructure,
    )

    assert (
        result.source_descriptor_set
        ==
        descriptor_set
    )


def test_descriptor_algebra_does_not_modify_input():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    original = descriptor_set.descriptors

    DefaultDescriptorAlgebra().analyze(
        descriptor_set
    )

    assert (
        descriptor_set.descriptors
        ==
        original
    )


def test_descriptor_algebra_creates_descriptor_relations():

    descriptor = make_behaviour_descriptor()

    descriptor_set = DescriptorSet(
        descriptors=(descriptor,),
    )

    result = (
        DefaultDescriptorAlgebra()
        .analyze(descriptor_set)
    )

    assert (
        result.source_descriptor_set
        ==
        descriptor_set
    )
