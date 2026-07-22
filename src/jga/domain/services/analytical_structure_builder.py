from __future__ import annotations

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.descriptor_relation import DescriptorRelation
from jga.domain.descriptor_set import DescriptorSet


class AnalyticalStructureBuilder:
    """
    Builds the final AnalyticalStructure from DescriptorRelation
    objects.

    Purpose
    -------
    Finalizes the mathematical layer.

    Input
    -----
    DescriptorRelation*

    Transformation
    --------------
    Creates the immutable AnalyticalStructure.

    Output
    ------
    AnalyticalStructure

    Preserved Invariants
    --------------------
    - provenance
    - descriptor identity
    - immutability
    """

    def build(
        self,
        relations: tuple[DescriptorRelation, ...],
    ) -> AnalyticalStructure:

        descriptors = tuple(
            descriptor
            for relation in relations
            for descriptor in relation.descriptors
        )

        return AnalyticalStructure(
            source_descriptor_set=DescriptorSet(
                descriptors=descriptors,
            ),
        )

