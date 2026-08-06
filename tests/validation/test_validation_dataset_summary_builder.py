from jga.validation.builders.validation_dataset_summary_builder import (
    ValidationDatasetSummaryBuilder,
)
from jga.validation.models.validation_metadata import (
    ValidationMetadata,
)
from jga.validation.validation_dataset import ValidationDataset


def test_summary_builder():
    dataset = ValidationDataset(
        metadata=ValidationMetadata(
            analysis_version="M78",
            sample_rate=44100,
            duration_seconds=10.5,
        ),
    )

    summary = ValidationDatasetSummaryBuilder().build(dataset)

    assert summary.observations == 0
    assert summary.sample_rate == 44100
    assert summary.duration_seconds == 10.5
