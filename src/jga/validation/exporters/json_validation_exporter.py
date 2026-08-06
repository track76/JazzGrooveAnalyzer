"""
JSON Validation Exporter.
"""

import json
from pathlib import Path

from jga.validation.exporters.validation_exporter import (
    ValidationExporter,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


class JsonValidationExporter(ValidationExporter):
    """
    Exports a ValidationDataset as JSON.

    No semantic interpretation is performed.
    """

    def export(
        self,
        dataset: ValidationDataset,
        destination: str,
    ) -> None:

        path = Path(destination)

        payload = {
            "observations": [
                {
                    "timestamp": observation.timestamp,
                    "observation_type": observation.observation_type,
                    "value": observation.value,
                    "source": observation.source,
                }
                for observation in dataset.observations
            ],
        }

        path.write_text(
            json.dumps(
                payload,
                indent=4,
            ),
            encoding="utf-8",
        )
