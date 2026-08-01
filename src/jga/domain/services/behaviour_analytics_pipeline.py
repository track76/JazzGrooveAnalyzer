from __future__ import annotations

from abc import ABC, abstractmethod

from jga.core.stability_curve import StabilityCurve
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
    StabilityCurve

    Output
    ------
    BehaviourAnalyticsResult
    """

    @abstractmethod
    def analyze(
        self,
        profile: BehaviourProfile,
        stability_curve: StabilityCurve,
    ) -> BehaviourAnalyticsResult:
        ...
