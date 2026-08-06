from pathlib import Path

from jga.validation.exporters.csv_validation_exporter import (
    CsvValidationExporter,
)
from jga.validation.models.validation_record import (
    ValidationRecord,
)
from jga.validation.services.validation_export_service import (
    ValidationExportService,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


def test_export_service_delegates_export(tmp_path: Path):

    dataset = ValidationDataset(
        observations=(
            ValidationRecord(
                timestamp=1.25,
                observation_type="PulseCandidate",
                value="0.82",
                source="Ride",
            ),
        ),
    )

    destination = tmp_path / "dataset.csv"

    ValidationExportService().export(
        dataset=dataset,
        exporter=CsvValidationExporter(),
        destination=str(destination),
    )

    assert destination.exists()
