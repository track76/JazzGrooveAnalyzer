from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.behaviour_distance import BehaviourDistance
from jga.domain.behaviour_observation import BehaviourObservation


class BehaviourDistanceMetric(ABC):
    """
    Mathematical metric computing the scientific
    distance between two BehaviourObservations.
    """

    @abstractmethod
    def compute(
        self,
        first: BehaviourObservation,
        second: BehaviourObservation,
    ) -> BehaviourDistance:
        """
        Compute the scientific BehaviourDistance
        between two observations.
        """
        raise NotImplementedError
