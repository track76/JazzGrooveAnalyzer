"""
Validation Report Builder.
"""

from jga.validation.builders.validation_dataset_summary_builder import (
    ValidationDatasetSummaryBuilder,
)
from jga.validation.models.validation_report import (
    ValidationReport,
)
from jga.validation.validation_dataset import ValidationDataset


class ValidationReportBuilder:
    """
    Builds a ValidationReport from a ValidationDataset.
    """

    def __init__(self) -> None:
        self._summary_builder = (
            ValidationDatasetSummaryBuilder()
        )

    def build(
        self,
        dataset: ValidationDataset,
    ) -> ValidationReport:

        return ValidationReport(
            summary=self._summary_builder.build(
                dataset,
            ),
        )
