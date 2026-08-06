"""
Validation Dataset Builder.
"""

from collections.abc import Iterable

from jga.validation.models.validation_metadata import ValidationMetadata
from jga.validation.models.validation_record import ValidationRecord
from jga.validation.models.validation_source import ValidationSource
from jga.validation.validation_dataset import ValidationDataset


class ValidationDatasetBuilder:
    """
    Builds a ValidationDataset.
    """

    def build(
        self,
        observations: Iterable[ValidationRecord],
        source: ValidationSource | None = None,
        metadata: ValidationMetadata | None = None,
    ) -> ValidationDataset:
        return ValidationDataset(
            observations=tuple(observations),
            source=source,
            metadata=metadata,
        )
