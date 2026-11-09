from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class BassAttributionDecision(str, Enum):
    BASS = "BASS"
    NON_BASS = "NON_BASS"
    UNKNOWN = "UNKNOWN"


class CandidateInputRepresentation(str, Enum):
    FULL_MIX = "FULL_MIX"
    STEM = "STEM"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class BassCandidateAttribution:
    """Classification that retains candidate identity and observation lineage."""

    candidate_id: UUID
    source_id: UUID
    timestamp: float
    decision: BassAttributionDecision
    input_representation: CandidateInputRepresentation
    observation_index: int | None = None
    observation_provenance_id: str | None = None
