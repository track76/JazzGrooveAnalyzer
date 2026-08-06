from jga.core.metric_context import MetricContext
from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate
from jga.core.source_pulse_sequence import SourcePulseSequence

from jga.validation.builders.metric_context_validation_builder import (
    MetricContextValidationBuilder,
)


def test_builder_rejects_none():

    builder = MetricContextValidationBuilder()

    try:
        builder.build(None)
        assert False
    except ValueError:
        pass


def test_builder_creates_validation_record():

    context = MetricContext(
        source_pulse_sequences=(
            SourcePulseSequence(
                source=MetricSource(
                    name="Ride",
                    family="Percussion",
                ),
                pulse_candidates=[
                    PulseCandidate(
                        time=1.25,
                        strength=0.82,
                        confidence=0.97,
                    ),
                ],
            ),
        ),
        periodicity_segments=(),
        metric_segments=(),
    )

    records = (
        MetricContextValidationBuilder().build(
            context,
        )
    )

    assert len(records) == 1

    record = records[0]

    assert record.timestamp == 1.25
    assert record.observation_type == "PulseCandidate"
    assert record.value == "0.82"
    assert record.source == "Ride"
