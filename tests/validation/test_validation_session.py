from jga.validation import (
    ValidationDataset,
    ValidationSession,
)


def test_validation_session_contains_dataset():
    dataset = ValidationDataset(
        observations=("A",),
    )

    session = ValidationSession(dataset=dataset)

    assert session.dataset is dataset
