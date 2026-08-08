"""Ground Truth loader boundary."""

from abc import ABC, abstractmethod
from pathlib import Path

from jga.ground_truth.models import GroundTruth


class GroundTruthLoader(ABC):
    """Constructs Ground Truth from an authoritative symbolic source."""

    @abstractmethod
    def load(
        self,
        source: Path,
        repository_revision: str | None = None,
    ) -> GroundTruth:
        """Read the source and return an immutable Ground Truth model."""
        raise NotImplementedError
