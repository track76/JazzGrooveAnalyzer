from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID


@dataclass(slots=True)
class AudioStem:
    """
    Represents an audio stem extracted from an audio recording.

    An AudioStem is a domain entity that models a separated audio source.
    It does not contain any DSP or source-separation logic.
    """

    id: UUID
    recording_id: UUID
    name: str
    audio_path: Path
    sample_rate: int
    duration: float
    channels: int
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name cannot be empty")

        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be greater than zero")

        if self.duration <= 0:
            raise ValueError("duration must be greater than zero")

        if self.channels <= 0:
            raise ValueError("channels must be greater than zero")