from __future__ import annotations

from jga.domain.behaviour_analytics_result import BehaviourAnalyticsResult
from jga.domain.descriptor_set import DescriptorSet

from jga.domain.services.analytical_structure_builder import (
    AnalyticalStructureBuilder,
)
from jga.domain.services.descriptor_relation_builder import (
    DescriptorRelationBuilder,
)
from jga.domain.services.identity_descriptor_operator import (
    IdentityDescriptorOperator,
)
from jga.domain.services.selection_descriptor_operator import (
    SelectionDescriptorOperator,
)
from jga.domain.services.ordering_descriptor_operator import (
    OrderingDescriptorOperator,
)
from jga.domain.services.grouping_descriptor_operator import (
    GroupingDescriptorOperator,
)


class BehaviourAnalyticsBuilder:
    """
    Behaviour Analytics orchestration.

    Pipeline

        DescriptorSet
              ↓
        DescriptorRelationBuilder
              ↓
        IdentityOperator
              ↓
        SelectionOperator
              ↓
        OrderingOperator
              ↓
        GroupingOperator
              ↓
        AnalyticalStructureBuilder
              ↓
        BehaviourAnalyticsResult
    """

    def __init__(self) -> None:

        self._relation_builder = (
            DescriptorRelationBuilder()
        )

        self._identity = (
            IdentityDescriptorOperator()
        )

        self._selection = (
            SelectionDescriptorOperator()
        )

        self._ordering = (
            OrderingDescriptorOperator()
        )

        self._grouping = (
            GroupingDescriptorOperator()
        )

        self._builder = (
            AnalyticalStructureBuilder()
        )

    def build(
        self,
        descriptor_set: DescriptorSet,
    ) -> BehaviourAnalyticsResult:

        relations = self._relation_builder.build(
            descriptor_set
        )

        relations = self._identity.apply(
            relations
        )

        relations = self._selection.apply(
            relations
        )

        relations = self._ordering.apply(
            relations
        )

        relations = self._grouping.apply(
            relations
        )

        analytical = self._builder.build(
            relations
        )

        return BehaviourAnalyticsResult(
            descriptor_set=descriptor_set,
            analytical_structure=analytical,
        )

