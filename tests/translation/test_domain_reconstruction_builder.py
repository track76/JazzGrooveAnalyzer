
from jga.translation.domain_reconstruction_builder import (
    DefaultDomainReconstructionBuilder,
)
from jga.domain.declared_meter import DeclaredMeter
from jga.domain.declared_metric_reference import MetricReferenceProvenance
from jga.translation.domain_reconstruction_input import DomainReconstructionInput


def test_domain_reconstruction_builder_exists():

    builder = DefaultDomainReconstructionBuilder()

    assert builder is not None


from jga.domain.services.beat_reconstruction_engine import (
    BeatReconstructionEngine,
)


def test_builder_uses_beat_reconstruction_engine():

    builder = DefaultDomainReconstructionBuilder()

    assert isinstance(
        builder.beat_builder,
        BeatReconstructionEngine,
    )


def test_declared_meter_becomes_domain_signature_without_changing_its_evidence():
    declared_meter = DeclaredMeter(
        4,
        4,
        MetricReferenceProvenance(
            source_id="CONTROLLED-CONTEXT-TEST",
            source_kind="authoritative_controlled_source_context",
            source_sha256="a" * 64,
            temporal_scope="complete_recording",
        ),
    )
    reconstruction_input = DomainReconstructionInput(
        sound_sources=(),
        metric_context=object(),
        metric_contributors=(),
        domain_pulse_candidates=(),
        ensemble_metric_events=(),
        declared_meter=declared_meter,
    )

    result = DefaultDomainReconstructionBuilder().build(reconstruction_input)

    assert result.internal_metric_signature.numerator == 4
    assert result.internal_metric_signature.denominator == 4
    assert result.internal_metric_signature.pulses_per_beat == 4
    assert not hasattr(declared_meter, "pulses_per_beat")
