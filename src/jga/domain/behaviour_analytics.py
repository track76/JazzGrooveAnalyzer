from dataclasses import dataclass

from jga.domain.behaviour_profile import BehaviourProfile


@dataclass(slots=True, frozen=True)
class BehaviourAnalytics:
    """
    Root aggregate for Behaviour Analytics.
    """

    profile: BehaviourProfile
