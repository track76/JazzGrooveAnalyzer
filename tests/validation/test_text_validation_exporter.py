from pathlib import Path

from jga.validation import ValidationDataset
from jga.validation.exporters.text_validation_exporter import (
    TextValidationExporter,
)


def test_text_export(tmp_path: Path):
    dataset = ValidationDataset(
        observations=("A", "B", "C"),
    )

    destination = tmp_path / "dataset.txt"

    TextValidationExporter().export(dataset, str(destination))

    assert destination.exists()

    content = destination.read_text().splitlines()

    assert content == ["A", "B", "C"]
