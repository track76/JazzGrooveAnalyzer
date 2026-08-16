from uuid import uuid4

import pytest

from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate as CorePulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.engines.domain_pulse_candidate_adapter import (
    DomainPulseCandidateAdapter,
)


def test_adapter_preserves_strength_exactly_and_immutably():
    source_id = uuid4()
    observed_strength = 0.12345678901234568
    sequence = SourcePulseSequence(
        source=MetricSource(
            name="bass",
            family="strings",
            source_id=source_id,
        ),
        pulse_candidates=[
            CorePulseCandidate(
                time=1.25,
                strength=observed_strength,
                confidence=0.9,
            )
        ],
    )

    result = DomainPulseCandidateAdapter().convert((sequence,))

    assert len(result) == 1
    assert result[0].strength == observed_strength
    assert result[0].strength.hex() == observed_strength.hex()

    with pytest.raises(AttributeError):
        result[0].strength = 1.0


def test_adapter_identity_is_deterministic_and_scope_bound():
    source_id = uuid4()
    sequence = SourcePulseSequence(
        source=MetricSource("piano", "strings", source_id=source_id),
        pulse_candidates=[CorePulseCandidate(time=1.25, strength=0.5)],
    )
    adapter = DomainPulseCandidateAdapter()

    first = adapter.convert((sequence,), "asset-a")
    second = adapter.convert((sequence,), "asset-a")
    other_asset = adapter.convert((sequence,), "asset-b")

    assert first[0].id == second[0].id
    assert first[0].id != other_asset[0].id
    assert first[0].observation_index == 0
    assert first[0].observation_provenance_id == "asset-a"
