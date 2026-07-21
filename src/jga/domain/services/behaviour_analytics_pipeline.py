from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)


class BehaviourAnalyticsPipeline(ABC):
    """
    Behaviour Analytics pipeline contract.

    Input
    -----
    BehaviourProfile

    Output
    ------
    BehaviourAnalyticsResult

    The pipeline orchestrates the transition:

        BehaviourProfile
              |
              v
        BehaviourQuantification
              |
              v
        DescriptorSet
              |
              v
        BehaviourAnalytics
              |
              v
        BehaviourAnalyticsResult

    No analytical computation is performed here.
    """

    @abstractmethod
    def analyze(
        self,
        profile: BehaviourProfile,
    ) -> BehaviourAnalyticsResult:
        ...
