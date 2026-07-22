from __future__ import annotations

from jga.domain.descriptor_relation import DescriptorRelation


class IdentityDescriptorOperator:
    """
    Identity Descriptor Operator.

    Input
    -----
    DescriptorRelation*

    Output
    ------
    DescriptorRelation*

    Preserved Invariants
    --------------------
    - immutability
    - provenance
    - descriptor identity
    """

    def apply(
        self,
        relations: tuple[DescriptorRelation, ...],
    ) -> tuple[DescriptorRelation, ...]:

        return relations

