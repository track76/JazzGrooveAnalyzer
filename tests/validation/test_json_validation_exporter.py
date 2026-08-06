from pathlib import Path
import json

from jga.validation.exporters.json_validation_exporter import (
    JsonValidationExporter,
)
from jga.validation.models.validation_record import (
    ValidationRecord,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


def test_json_export(tmp_path: Path):

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

    destination = tmp_path / "dataset.json"

    JsonValidationExporter().export(
        dataset,
        str(destination),
    )

    payload = json.loads(
        destination.read_text(
            encoding="utf-8",
        )
    )

    assert len(payload["observations"]) == 1

    observation = payload["observations"][0]

    assert observation["timestamp"] == 1.25
    assert observation["observation_type"] == "PulseCandidate"
    assert observation["value"] == "0.82"
    assert observation["source"] == "Ride"
