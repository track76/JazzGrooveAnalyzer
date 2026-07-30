from dataclasses import dataclass

from jga.domain.behaviour_observation import BehaviourObservation


@dataclass(slots=True, frozen=True)
class BehaviourObservationCollection:

    observations: tuple[BehaviourObservation, ...]
