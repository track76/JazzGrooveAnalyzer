from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.analytical_structure_builder import (
    AnalyticalStructureBuilder,
)


def test_analytical_structure_builder_preserves_descriptor_set():

    builder = AnalyticalStructureBuilder()

    result = builder.build(
        (),
    )

    assert isinstance(
        result.source_descriptor_set,
        DescriptorSet,
    )

    assert (
        result.source_descriptor_set.descriptors
        == ()
    )
