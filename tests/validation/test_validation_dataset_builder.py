from jga.validation import ValidationDataset, ValidationDatasetBuilder
from jga.validation.models.validation_metadata import ValidationMetadata
from jga.validation.models.validation_record import ValidationRecord
from jga.validation.models.validation_source import ValidationSource


def test_builder_returns_validation_dataset():
    builder = ValidationDatasetBuilder()

    source = ValidationSource(
        recording_id="001",
        recording_name="Autumn Leaves",
        performer="Bill Evans Trio",
    )

    metadata = ValidationMetadata(
        analysis_version="M78",
        sample_rate=44100,
        duration_seconds=120.0,
    )

    records = (
        ValidationRecord(
            timestamp=0.0,
            observation_type="TimingBehaviour",
            value="UNKNOWN",
            source="Bass",
        ),
    )

    dataset = builder.build(
        observations=records,
        source=source,
        metadata=metadata,
    )

    assert isinstance(dataset, ValidationDataset)
    assert dataset.source is source
    assert dataset.metadata is metadata
    assert len(dataset) == 1
