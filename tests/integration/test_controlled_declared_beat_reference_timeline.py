from decimal import Decimal

from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.interfaces.scientific_value_origin import ScientificValueOrigin
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


DRUM_WAV = "recordings/validation/stems/drums.wav"
MUSICXML_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"
DRUM_SHA256 = "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd"


def test_authoritative_controlled_asset_has_one_exact_declared_quarter_timeline():
    tempo_authority = MetricReferenceProvenance(
        "GT-VAL-001-v1",
        "authoritative controlled-source MusicXML",
        MUSICXML_SHA256,
        "complete controlled performance",
    )
    asset_authority = MetricReferenceProvenance(
        "CED-VAL-001-drums-wav",
        "authoritative controlled audio asset",
        DRUM_SHA256,
        "complete controlled performance",
    )
    reference = DeclaredMetricReference(Decimal("78"), "quarter", tempo_authority)
    phase = DeclaredQuarterPhaseOrigin(Decimal("0"), asset_authority)
    scope = DeclaredAnalysisScope(
        Decimal("0"),
        Decimal(1865728) / Decimal(44100),
        DRUM_SHA256,
        asset_authority,
    )

    context = AnalysisPipeline().analyze(
        DRUM_WAV,
        declared_metric_reference=reference,
        declared_quarter_phase_origin=phase,
        declared_analysis_scope=scope,
    )
    beats = context.beat_references

    assert reference.period_seconds == Decimal("60") / Decimal("78")
    assert len(beats) == 55
    assert beats[0].exact_timestamp_ratio == "0/1"
    assert beats[-1].exact_timestamp_ratio == "540/13"
    assert all(beat.timestamp < float(scope.end_seconds) for beat in beats)
    assert tuple(beat.index for beat in beats) == tuple(range(55))
    assert all(beat.epistemic_status is ScientificValueOrigin.DECLARED for beat in beats)
    assert all(beat.tempo_provenance is tempo_authority for beat in beats)
    assert all(beat.phase_origin_provenance is asset_authority for beat in beats)
    assert all(beat.numeric_temporal_scope is scope for beat in beats)
