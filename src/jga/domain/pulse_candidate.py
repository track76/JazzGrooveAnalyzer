from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PulseCandidate:
    """
    Represents one candidate temporal event that may
    contribute to the estimation of the ensemble pulse.

    A PulseCandidate is not necessarily a beat.
    """

    id: UUID
    sound_source_id: UUID
    timestamp: float
    strength: float
    confidence: float
    created_at: datetime

    observation_index: int | None = None

    observation_provenance_id: str | None = None

    def __post_init__(self) -> None:

        if self.timestamp < 0:
            raise ValueError("timestamp must be non-negative")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

        if self.observation_index is not None and self.observation_index < 0:
            raise ValueError("observation_index must be non-negative")
