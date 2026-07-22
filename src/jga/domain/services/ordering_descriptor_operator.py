from __future__ import annotations

from jga.domain.descriptor_relation import DescriptorRelation


class OrderingDescriptorOperator:
    """
    Deterministic ordering operator.

    Orders DescriptorRelation objects by descriptor cardinality.
    """

    def apply(
        self,
        relations: tuple[DescriptorRelation, ...],
    ) -> tuple[DescriptorRelation, ...]:

        return tuple(
            sorted(
                relations,
                key=lambda relation: len(
                    relation.descriptors
                ),
            )
        )

