"""
Validation Export Service.
"""

from jga.validation.validation_dataset import ValidationDataset
from jga.validation.exporters.validation_exporter import ValidationExporter


class ValidationExportService:
    """
    Delegates dataset export to a ValidationExporter.
    """

    def export(
        self,
        dataset: ValidationDataset,
        exporter: ValidationExporter,
        destination: str,
    ) -> None:
        exporter.export(dataset, destination)
