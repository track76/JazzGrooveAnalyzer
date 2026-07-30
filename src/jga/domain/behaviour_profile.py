from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from jga.domain.behaviour_observation import BehaviourObservation


@dataclass(slots=True, frozen=True)
class BehaviourProfile:
    """
    Immutable collection of behaviour observations describing
    the quantified behaviour of an ensemble.
    """

    id: UUID
    observations: tuple[BehaviourObservation, ...]
    created_at: datetime

    @property
    def observation_count(self) -> int:
        return len(self.observations)
