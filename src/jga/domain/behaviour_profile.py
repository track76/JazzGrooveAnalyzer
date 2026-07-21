from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.behaviour_observation import BehaviourObservation


@dataclass(frozen=True, slots=True)
class BehaviourProfile:
    """
    Canonical behavioural representation produced by M5.
    """

    id: UUID
    observations: tuple[BehaviourObservation, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        if len(self.observations) == 0:
            raise ValueError(
                "BehaviourProfile must contain at least one BehaviourObservation"
            )

    @property
    def observation_count(self) -> int:
        return len(self.observations)
