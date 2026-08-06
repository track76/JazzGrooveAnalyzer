from jga.validation.models.validation_record import ValidationRecord


def test_validation_record_creation():
    record = ValidationRecord(
        timestamp=1.25,
        observation_type="TimingBehaviour",
        value="UNKNOWN",
        source="Bass",
    )

    assert record.timestamp == 1.25
    assert record.observation_type == "TimingBehaviour"
    assert record.value == "UNKNOWN"
    assert record.source == "Bass"
