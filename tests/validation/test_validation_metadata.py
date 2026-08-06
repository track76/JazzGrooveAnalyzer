from jga.validation.models.validation_metadata import ValidationMetadata


def test_validation_metadata():
    metadata = ValidationMetadata(
        analysis_version="M78",
        sample_rate=44100,
        duration_seconds=195.42,
    )

    assert metadata.analysis_version == "M78"
    assert metadata.sample_rate == 44100
    assert metadata.duration_seconds == 195.42
    assert metadata.recording_date is None
