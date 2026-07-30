from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class SourceMusicalFunctionAssignment:
    """
    Represents the relationship between a SoundSource
    and a MusicalFunction inside an ensemble context.
    """

    id: UUID

    sound_source_id: UUID

    musical_function_id: UUID

    confidence: float

    rationale: str | None

    created_at: datetime

    def __post_init__(self) -> None:

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )
