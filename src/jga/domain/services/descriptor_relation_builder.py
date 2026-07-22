from __future__ import annotations

from jga.domain.descriptor_relation import DescriptorRelation
from jga.domain.descriptor_set import DescriptorSet


class DescriptorRelationBuilder:
    """
    Builds mathematical DescriptorRelation objects.

    Purpose
    -------
    Formalize mathematical relations from DescriptorSet.

    Current implementation creates one global relation
    preserving the complete DescriptorSet.

    Future versions will generate multiple mathematically
    defined relations according to Descriptor Algebra.
    """

    def build(
        self,
        descriptor_set: DescriptorSet,
    ) -> tuple[DescriptorRelation, ...]:

        return (
            DescriptorRelation(
                descriptors=descriptor_set.descriptors,
            ),
        )

