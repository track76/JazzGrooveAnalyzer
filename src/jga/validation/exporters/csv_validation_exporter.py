"""
CSV Validation Exporter.
"""

from pathlib import Path

from jga.validation.exporters.validation_exporter import (
    ValidationExporter,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


class CsvValidationExporter(ValidationExporter):
    """
    Exports a ValidationDataset as CSV.

    No semantic interpretation is performed.
    """

    def export(
        self,
        dataset: ValidationDataset,
        destination: str,
    ) -> None:

        path = Path(destination)

        with path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            fp.write(
                "timestamp,observation_type,value,source\n"
            )

            for observation in dataset.observations:

                fp.write(
                    f"{observation.timestamp},"
                    f"{observation.observation_type},"
                    f"{observation.value},"
                    f"{observation.source}\n"
                )
