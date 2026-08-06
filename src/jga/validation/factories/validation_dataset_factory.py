"""
Validation Dataset Factory.
"""

from jga.validation.builders.validation_dataset_builder import (
    ValidationDatasetBuilder,
)
from jga.validation.models.validation_metadata import ValidationMetadata
from jga.validation.models.validation_record import ValidationRecord
from jga.validation.models.validation_source import ValidationSource
from jga.validation.validation_dataset import ValidationDataset


class ValidationDatasetFactory:
    """
    Entry point for creating ValidationDataset objects.

    Future pipeline integrations should use this factory.
    """

    def __init__(self) -> None:
        self._builder = ValidationDatasetBuilder()

    def create(
        self,
        observations: list[ValidationRecord],
        source: ValidationSource | None = None,
        metadata: ValidationMetadata | None = None,
    ) -> ValidationDataset:
        return self._builder.build(
            observations=observations,
            source=source,
            metadata=metadata,
        )
