from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class MetricContributor:
    """
    Represents a sound source that contributes to the
    construction of the Internal Metric Timeline.
    """

    id: UUID
    sound_source_id: UUID
    musical_function_id: UUID
    active: bool
    created_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.active, bool):
            raise TypeError("active must be a boolean")