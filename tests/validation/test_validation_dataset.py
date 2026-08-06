from jga.validation import ValidationDataset
from jga.validation.models.validation_metadata import ValidationMetadata
from jga.validation.models.validation_record import ValidationRecord


def test_empty_dataset():
    dataset = ValidationDataset()

    assert dataset.is_empty
    assert len(dataset) == 0
    assert dataset.metadata is None


def test_dataset_contains_observations():
    metadata = ValidationMetadata(
        analysis_version="M78",
        sample_rate=44100,
        duration_seconds=120.0,
    )

    dataset = ValidationDataset(
        observations=(
            ValidationRecord(
                timestamp=0.0,
                observation_type="TimingBehaviour",
                value="UNKNOWN",
                source="Bass",
            ),
        ),
        metadata=metadata,
    )

    assert not dataset.is_empty
    assert len(dataset) == 1
    assert dataset.metadata is metadata
