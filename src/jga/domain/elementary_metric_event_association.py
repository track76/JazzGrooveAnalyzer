from dataclasses import dataclass
from typing import Literal
from uuid import UUID


AssociationOutcome = Literal["ASSOCIATED", "AMBIGUOUS", "NOT_PRODUCED"]


@dataclass(frozen=True, slots=True)
class ElementaryMetricEventAssociation:
    """Immutable result of associating observations with one movement."""

    beat_reference_id: UUID
    contributor_id: UUID
    sound_source_id: UUID
    supporting_pulse_candidate_ids: tuple[UUID, ...]
    timestamp: float | None
    confidence: float | None
    temporal_scope: str
    association_rule: str
    outcome: AssociationOutcome
