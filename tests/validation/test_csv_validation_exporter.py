from pathlib import Path

from jga.validation.exporters.csv_validation_exporter import (
    CsvValidationExporter,
)
from jga.validation.models.validation_record import (
    ValidationRecord,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


def test_csv_export(tmp_path: Path):

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

    CsvValidationExporter().export(
        dataset,
        str(destination),
    )

    content = destination.read_text()

    assert "timestamp,observation_type,value,source" in content
    assert "1.25,PulseCandidate,0.82,Ride" in content
