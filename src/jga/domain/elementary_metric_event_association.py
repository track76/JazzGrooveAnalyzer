from dataclasses import dataclass
from typing import Literal
from uuid import UUID


AssociationOutcome = Literal["ASSOCIATED", "AMBIGUOUS", "NOT_PRODUCED"]


@dataclass(frozen=True, slots=True)
class ElementaryMetricEventAssociation:
    """Immutable metric localization of one already-materialized EME."""

    beat_reference_id: UUID | None
    contributor_id: UUID
    sound_source_id: UUID
    supporting_pulse_candidate_ids: tuple[UUID, ...]
    timestamp: float | None
    confidence: float | None
    temporal_scope: str
    association_rule: str
    outcome: AssociationOutcome

    elementary_metric_event_id: UUID | None = None

    following_beat_reference_id: UUID | None = None

    elapsed_seconds: float | None = None

    normalized_phase: float | None = None
