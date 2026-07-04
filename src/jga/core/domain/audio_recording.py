from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class AudioRecording:
    """
    Aggregate Root representing one analysed audio recording.
    """

    id: UUID
    path: Path
    sample_rate: int
    channels: int
    duration_seconds: float

    @classmethod
    def create(
        cls,
        path: Path,
        sample_rate: int,
        channels: int,
        duration_seconds: float,
    ) -> "AudioRecording":
        return cls(
            id=uuid4(),
            path=path,
            sample_rate=sample_rate,
            channels=channels,
            duration_seconds=duration_seconds,
        )