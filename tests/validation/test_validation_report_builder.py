from jga.validation.builders.validation_report_builder import (
    ValidationReportBuilder,
)
from jga.validation.models.validation_metadata import (
    ValidationMetadata,
)
from jga.validation.validation_dataset import (
    ValidationDataset,
)


def test_validation_report_builder():
    dataset = ValidationDataset(
        metadata=ValidationMetadata(
            analysis_version="M78",
            sample_rate=44100,
            duration_seconds=12.5,
        ),
    )

    report = ValidationReportBuilder().build(
        dataset,
    )

    assert report.summary.observations == 0
    assert report.summary.sample_rate == 44100
    assert report.summary.duration_seconds == 12.5
