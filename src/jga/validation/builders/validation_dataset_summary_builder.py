"""
Validation Dataset Summary Builder.
"""

from jga.validation.models.validation_dataset_summary import (
    ValidationDatasetSummary,
)
from jga.validation.validation_dataset import ValidationDataset


class ValidationDatasetSummaryBuilder:
    """
    Builds a ValidationDatasetSummary.
    """

    def build(
        self,
        dataset: ValidationDataset,
    ) -> ValidationDatasetSummary:

        metadata = dataset.metadata

        assert metadata is not None

        return ValidationDatasetSummary(
            observations=len(dataset),
            sample_rate=metadata.sample_rate,
            duration_seconds=metadata.duration_seconds,
        )
