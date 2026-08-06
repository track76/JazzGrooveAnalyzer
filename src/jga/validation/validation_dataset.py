"""
Validation Dataset.
"""

from dataclasses import dataclass, field

from jga.validation.models.validation_metadata import ValidationMetadata
from jga.validation.models.validation_record import ValidationRecord
from jga.validation.models.validation_source import ValidationSource


@dataclass(frozen=True, slots=True)
class ValidationDataset:
    """
    Scientific observational dataset.
    """

    observations: tuple[ValidationRecord, ...] = field(default_factory=tuple)
    source: ValidationSource | None = None
    metadata: ValidationMetadata | None = None

    def __len__(self) -> int:
        return len(self.observations)

    @property
    def is_empty(self) -> bool:
        return len(self.observations) == 0
