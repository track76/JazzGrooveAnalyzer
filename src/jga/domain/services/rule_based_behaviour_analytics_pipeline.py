from __future__ import annotations

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)
from jga.domain.behaviour_profile import BehaviourProfile

from jga.domain.services.behaviour_analytics_builder import (
    BehaviourAnalyticsBuilder,
)

from jga.domain.services.behaviour_quantification_builder import (
    BehaviourQuantificationBuilder,
)

from jga.domain.services.descriptor_set_builder import (
    DescriptorSetBuilder,
)

from jga.domain.services.behaviour_analytics_pipeline import (
    BehaviourAnalyticsPipeline,
)


class RuleBasedBehaviourAnalyticsPipeline(
    BehaviourAnalyticsPipeline,
):
    """
    Rule based implementation of Behaviour Analytics.

    Orchestrates:

        BehaviourProfile
              |
              v
        Behaviour Quantification
              |
              v
        DescriptorSet
              |
              v
        Behaviour Analytics

    No analytical algorithm is implemented here.
    """

    def __init__(
        self,
        quantifier: BehaviourQuantificationBuilder | None = None,
        descriptor_set_builder: DescriptorSetBuilder | None = None,
        analytics_builder: BehaviourAnalyticsBuilder | None = None,
    ) -> None:

        self._quantifier = (
            quantifier
            or BehaviourQuantificationBuilder()
        )

        self._descriptor_set_builder = (
            descriptor_set_builder
            or DescriptorSetBuilder()
        )

        self._analytics_builder = (
            analytics_builder
            or BehaviourAnalyticsBuilder()
        )

    def analyze(
        self,
        profile: BehaviourProfile,
    ) -> BehaviourAnalyticsResult:

        descriptors = self._quantifier.build(
            profile,
        )

        descriptor_set = (
            self._descriptor_set_builder.build(
                descriptors,
            )
        )

        return self._analytics_builder.build(
            descriptor_set,
        )
