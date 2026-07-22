from __future__ import annotations

from jga.domain.descriptor_relation import DescriptorRelation


class SelectionDescriptorOperator:
    """
    Deterministic selection operator.

    Input
    -----
    DescriptorRelation*

    Transformation
    --------------
    Selects DescriptorRelation objects satisfying a deterministic
    predicate.

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

        return tuple(
            relation
            for relation in relations
            if relation.descriptors
        )
