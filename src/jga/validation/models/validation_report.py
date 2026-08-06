"""
Validation Report.
"""

from dataclasses import dataclass

from jga.validation.models.validation_dataset_summary import (
    ValidationDatasetSummary,
)


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """
    Scientific report generated from a ValidationDataset.
    """

    summary: ValidationDatasetSummary
