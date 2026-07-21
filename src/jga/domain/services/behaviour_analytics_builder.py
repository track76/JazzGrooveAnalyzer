from __future__ import annotations

from jga.domain.behaviour_analytics_result import BehaviourAnalyticsResult
from jga.domain.descriptor_set import DescriptorSet
from jga.domain.services.default_descriptor_algebra import (
    DefaultDescriptorAlgebra,
)
from jga.domain.services.descriptor_algebra import DescriptorAlgebra


class BehaviourAnalyticsBuilder:
    """
    Orchestrates Behaviour Analytics.

    The builder delegates mathematical operations
    to Descriptor Algebra and wraps the resulting
    AnalyticalStructure into a BehaviourAnalyticsResult.
    """

    def __init__(
        self,
        algebra: DescriptorAlgebra | None = None,
    ) -> None:

        self._algebra = algebra or DefaultDescriptorAlgebra()

    def build(
        self,
        descriptor_set: DescriptorSet,
    ) -> BehaviourAnalyticsResult:

        analytical_structure = self._algebra.analyze(
            descriptor_set
        )

        return BehaviourAnalyticsResult(
            descriptor_set=descriptor_set,
            analytical_structure=analytical_structure,
        )
