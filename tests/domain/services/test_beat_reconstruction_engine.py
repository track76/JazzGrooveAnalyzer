from decimal import Decimal
from uuid import uuid4

import pytest

from jga.core.ensemble_metric_event import EnsembleMetricEvent
from jga.core.metric_contribution import MetricContribution
from jga.core.metric_source import MetricSource
from jga.domain.services.beat_reconstruction_engine import BeatReconstructionEngine
from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)


def ensemble_event(timestamp, candidate_id):
    source_id = uuid4()
    return EnsembleMetricEvent(
        start_time=timestamp,
        end_time=timestamp,
        beat_time=timestamp,
        contributions=[
            MetricContribution(
                source=MetricSource("source", "test", source_id=source_id),
                event_time=timestamp,
                pulse_candidate_id=candidate_id,
                sound_source_id=source_id,
            )
        ],
        confidence=1.0,
    )


def test_empty_pre_eme_evidence_produces_no_movement():
    assert BeatReconstructionEngine().reconstruct(()) == ()


def test_reconstruction_uses_pre_eme_consensus_and_preserves_lineage():
    candidate_id = uuid4()
    beats = BeatReconstructionEngine().reconstruct(
        (ensemble_event(1.25, candidate_id),)
    )

    assert len(beats) == 1
    assert beats[0].timestamp == 1.25
    assert beats[0].supporting_pulse_candidate_ids == (candidate_id,)
    assert beats[0].reconstruction_rule == "ensemble-consensus-anchor/v1"


def test_reconstruction_is_ordered_and_has_deterministic_identity():
    candidate_ids = (uuid4(), uuid4())
    evidence = (
        ensemble_event(2.0, candidate_ids[1]),
        ensemble_event(1.0, candidate_ids[0]),
    )

    first = BeatReconstructionEngine().reconstruct(evidence)
    second = BeatReconstructionEngine().reconstruct(evidence)

    assert tuple(beat.timestamp for beat in first) == (1.0, 2.0)
    assert tuple(beat.id for beat in first) == tuple(beat.id for beat in second)


def declared_context():
    checksum = "a" * 64
    provenance = MetricReferenceProvenance(
        "controlled-asset", "authoritative test context", checksum, "complete asset"
    )
    return (
        DeclaredMetricReference(Decimal("78"), "quarter", provenance),
        DeclaredQuarterPhaseOrigin(Decimal("0"), provenance),
        DeclaredAnalysisScope(Decimal("0"), Decimal("42.30675736961451"), checksum, provenance),
    )


def test_declared_timeline_is_exact_scoped_and_density_independent():
    reference, phase, scope = declared_context()
    engine = BeatReconstructionEngine()
    empty = engine.reconstruct((), reference, phase, scope)
    dense = engine.reconstruct(
        (ensemble_event(1.2, uuid4()), ensemble_event(1.3, uuid4())),
        reference,
        phase,
        scope,
    )

    assert len(empty) == len(dense) == 55
    assert empty[0].exact_timestamp_ratio == "0/1"
    assert empty[-1].exact_timestamp_ratio == "540/13"
    assert tuple(item.id for item in empty) == tuple(item.id for item in dense)
    assert tuple(item.timestamp for item in empty) == tuple(item.timestamp for item in dense)
    assert all(item.timestamp < float(scope.end_seconds) for item in empty)
    assert all(item.numeric_temporal_scope is scope for item in empty)


def test_declared_rate_without_phase_and_scope_is_rejected():
    reference, _, _ = declared_context()
    with pytest.raises(ValueError, match="phase origin and numeric scope"):
        BeatReconstructionEngine().reconstruct((), reference)
