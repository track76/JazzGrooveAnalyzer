from jga.validation.models.validation_source import ValidationSource


def test_validation_source():
    source = ValidationSource(
        recording_id="001",
        recording_name="Autumn Leaves",
        performer="Bill Evans Trio",
    )

    assert source.recording_id == "001"
    assert source.recording_name == "Autumn Leaves"
    assert source.performer == "Bill Evans Trio"
