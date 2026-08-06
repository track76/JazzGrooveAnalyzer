"""
Text Validation Exporter.
"""

from pathlib import Path

from jga.validation.exporters.validation_exporter import ValidationExporter
from jga.validation.validation_dataset import ValidationDataset


class TextValidationExporter(ValidationExporter):
    """
    Exports a ValidationDataset as plain text.

    No semantic interpretation is performed.
    """

    def export(
        self,
        dataset: ValidationDataset,
        destination: str,
    ) -> None:
        path = Path(destination)

        with path.open("w", encoding="utf-8") as fp:
            for observation in dataset.observations:
                fp.write(f"{observation}\n")
