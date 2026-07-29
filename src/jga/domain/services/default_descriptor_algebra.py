from __future__ import annotations

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.descriptor_set import DescriptorSet

from jga.domain.services.descriptor_algebra import DescriptorAlgebra
from jga.domain.services.descriptor_relation_builder import (
    DescriptorRelationBuilder,
)


class DefaultDescriptorAlgebra(DescriptorAlgebra):
    """
    Default implementation of Descriptor Algebra.

    Produces analytical structures from validated
    DescriptorSet objects.

    Current operations:
    - descriptor preservation
    - descriptor relation construction

    No mathematical transformation is applied without
    formal specification.
    """

    def __init__(self) -> None:

        self.relation_builder = (
            DescriptorRelationBuilder()
        )

    def analyze(
        self,
        descriptor_set: DescriptorSet,
    ) -> AnalyticalStructure:

        relations = (
            self.relation_builder.build(
                descriptor_set
            )
        )

        return AnalyticalStructure(
            source_descriptor_set=descriptor_set,
        )
