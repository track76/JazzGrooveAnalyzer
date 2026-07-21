from __future__ import annotations

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.descriptor_algebra import DescriptorAlgebra


class DefaultDescriptorAlgebra(DescriptorAlgebra):
    """
    Default implementation of Descriptor Algebra.

    Current implementation preserves the mathematical
    contract without introducing undefined operators.

    Future operations such as aggregation, comparison,
    normalization, correlation, similarity and clustering
    require formal mathematical specification.
    """

    def analyze(
        self,
        descriptor_set: DescriptorSet,
    ) -> AnalyticalStructure:

        return AnalyticalStructure(
            source_descriptor_set=descriptor_set,
        )
