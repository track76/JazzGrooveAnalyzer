from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ElementaryMetricEvent:
    """
    One contributor's position relative to one reconstructed movement.

    It is an immutable Domain representation supported by observations; it
    is not itself a raw observation, onset, note, or transcription event.
    """

    id: UUID
    contributor_id: UUID
    timestamp: float
    confidence: float
    created_at: datetime

    beat_reference_id: UUID | None = None
    sound_source_id: UUID | None = None
    supporting_pulse_candidate_ids: tuple[UUID, ...] = ()
    association_rule: str = "legacy-unrecorded"
    temporal_scope: str = "unspecified"
    association_outcome: str = "ASSOCIATED"
    evidence_status: str = "UNRECORDED"

    def __post_init__(self) -> None:
        if self.timestamp < 0.0:
            raise ValueError("timestamp must be non-negative")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
