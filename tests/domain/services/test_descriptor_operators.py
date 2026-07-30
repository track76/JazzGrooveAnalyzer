from jga.domain.descriptor_relation import DescriptorRelation
from jga.domain.services.grouping_descriptor_operator import (
    GroupingDescriptorOperator,
)
from jga.domain.services.identity_descriptor_operator import (
    IdentityDescriptorOperator,
)
from jga.domain.services.ordering_descriptor_operator import (
    OrderingDescriptorOperator,
)
from jga.domain.services.selection_descriptor_operator import (
    SelectionDescriptorOperator,
)


def relation(size: int) -> DescriptorRelation:

    return DescriptorRelation(
        descriptors=tuple(object() for _ in range(size)),
    )


def test_identity_operator_preserves_sequence():

    relations = (
        relation(3),
        relation(1),
        relation(2),
    )

    result = IdentityDescriptorOperator().apply(
        relations
    )

    assert result is relations


def test_selection_operator_discards_empty_relations():

    relations = (
        relation(0),
        relation(2),
        relation(0),
        relation(1),
    )

    result = SelectionDescriptorOperator().apply(
        relations
    )

    assert len(result) == 2
    assert all(r.descriptors for r in result)


def test_ordering_operator_orders_by_cardinality():

    relations = (
        relation(3),
        relation(1),
        relation(4),
        relation(2),
    )

    result = OrderingDescriptorOperator().apply(
        relations
    )

    assert [
        len(r.descriptors)
        for r in result
    ] == [1, 2, 3, 4]


def test_grouping_operator_preserves_sequence():

    relations = (
        relation(2),
        relation(1),
    )

    result = GroupingDescriptorOperator().apply(
        relations
    )

    assert result is relations
