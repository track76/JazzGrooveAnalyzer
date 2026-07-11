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
    confidence: float
    created_at: datetime

    def __post_init__(self) -> None:

        if self.timestamp < 0:
            raise ValueError("timestamp must be non-negative")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")