from datetime import datetime
from uuid import UUID

from jga.domain.behaviour_descriptor import BehaviourDescriptor


def test_behaviour_descriptor_creation():
    descriptor = BehaviourDescriptor(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        created_at=datetime(2026, 1, 1),
        name="TemporalStability",
        value=0.85,
        provenance="BehaviourObservation"
    )

    assert descriptor.name == "TemporalStability"
    assert descriptor.value == 0.85
    assert descriptor.provenance == "BehaviourObservation"


def test_behaviour_descriptor_is_immutable():
    descriptor = BehaviourDescriptor(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        created_at=datetime(2026, 1, 1),
        name="TemporalStability",
        value=0.85,
        provenance="BehaviourObservation"
    )

    try:
        descriptor.value = 0.90
        immutable = False
    except Exception:
        immutable = True

    assert immutable
