"""Scientific validation catalogue loader boundary."""

from abc import ABC, abstractmethod
from pathlib import Path

from jga.validation_catalog.models import ValidationCatalog


class ValidationCatalogLoader(ABC):
    """Loads a catalogue without analysis, Ground Truth generation or comparison."""

    @abstractmethod
    def load(self, repository_root: Path) -> ValidationCatalog:
        """Verify catalogue assets and return their immutable bindings."""
        raise NotImplementedError
