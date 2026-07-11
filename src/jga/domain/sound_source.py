from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class SoundSource:
    """
    Represents a musical sound source.

    Examples:
    - Double Bass
    - Drum Kit
    - Piano
    - Saxophone
    """

    id: UUID
    name: str
    family: str
    description: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")

        if not self.family.strip():
            raise ValueError("family cannot be empty")