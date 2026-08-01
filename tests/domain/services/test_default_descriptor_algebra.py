from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.default_descriptor_algebra import (
    DefaultDescriptorAlgebra,
)


def test_default_descriptor_algebra_returns_structure():

    algebra = DefaultDescriptorAlgebra()

    descriptor_set = DescriptorSet(
        descriptors=(),
    )

    result = algebra.analyze(
        descriptor_set,
    )

    assert (
        result.source_descriptor_set
        is descriptor_set
    )
