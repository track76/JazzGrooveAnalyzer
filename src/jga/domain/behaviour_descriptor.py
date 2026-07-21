from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class BehaviourDescriptor:
    """
    Immutable Domain representation of one quantified Behaviour
    observation.

    This entity represents a quantified behavioural property without
    defining how the value has been computed.
    """

    id: UUID
    created_at: datetime
    name: str
    value: float
    provenance: str
