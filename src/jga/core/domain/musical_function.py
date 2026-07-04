from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class MusicalFunction:
    """
    Represents the musical role performed by a sound source
    during a specific time interval.
    """

    id: UUID
    name: str
    description: str | None
    is_metric: bool
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")