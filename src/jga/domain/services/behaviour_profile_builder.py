from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_observation import BehaviourObservation
from jga.domain.behaviour_profile import BehaviourProfile


class BehaviourProfileBuilder:
    """
    Builds the canonical BehaviourProfile from BehaviourObservation objects.
    """

    def build(
        self,
        observations: tuple[BehaviourObservation, ...],
    ) -> BehaviourProfile:

        return BehaviourProfile(
            id=uuid4(),
            observations=observations,
            created_at=datetime.now(),
        )
