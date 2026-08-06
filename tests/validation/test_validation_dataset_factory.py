from jga.validation.factories.validation_dataset_factory import (
    ValidationDatasetFactory,
)
from jga.validation.models.validation_record import ValidationRecord


def test_factory_creates_dataset():
    factory = ValidationDatasetFactory()

    dataset = factory.create(
        observations=[
            ValidationRecord(
                timestamp=0.0,
                observation_type="TimingBehaviour",
                value="UNKNOWN",
                source="Bass",
            ),
        ],
    )

    assert len(dataset) == 1
