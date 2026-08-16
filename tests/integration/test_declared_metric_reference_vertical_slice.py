from decimal import Decimal

import pytest

from jga.analysis_representation import (
    CompletedAnalysisMaterializer,
    MaterializationProvenance,
)
from jga.domain.declared_metric_reference import (
    DeclaredMetricReference,
    MetricReferenceProvenance,
)
from jga.domain.declared_meter import DeclaredMeter
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.interfaces.scientific_value_origin import ScientificValueOrigin
from jga.interfaces.validation import AnalysisOutputState
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator
from jga.visualization.ascii_analytical_score_renderer import (
    AsciiAnalyticalScoreRenderer,
)


MP3_PATH = "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
SOURCE_SHA256 = "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778"


def declared_reference() -> DeclaredMetricReference:
    return DeclaredMetricReference(
        beats_per_minute=Decimal("78"),
        beat_unit="quarter",
        provenance=MetricReferenceProvenance(
            source_id="GT-VAL-001-v1",
            source_kind="authoritative controlled-source context",
            source_sha256=SOURCE_SHA256,
            temporal_scope="complete controlled performance",
        ),
    )


def declared_meter() -> DeclaredMeter:
    return DeclaredMeter(4, 4, declared_reference().provenance)


def declared_timeline_context():
    provenance = declared_reference().provenance
    return (
        DeclaredQuarterPhaseOrigin(Decimal("0"), provenance),
        DeclaredAnalysisScope(
            Decimal("0"), Decimal("42.24"), SOURCE_SHA256, provenance
        ),
    )


@pytest.fixture(scope="module")
def analyses():
    pipeline = AnalysisPipeline(separator=DummyMultiStemSeparator())
    observed_only = pipeline.analyze(MP3_PATH)
    phase, scope = declared_timeline_context()
    declared = pipeline.analyze(
        MP3_PATH,
        declared_metric_reference=declared_reference(),
        declared_quarter_phase_origin=phase,
        declared_analysis_scope=scope,
        declared_meter=declared_meter(),
    )
    return observed_only, declared


def test_declared_context_does_not_change_core_observation(analyses):
    observed_only, declared = analyses

    assert declared.pulse_candidates == observed_only.pulse_candidates
    assert (
        declared.candidate_period_population
        == observed_only.candidate_period_population
    )


def test_declared_reference_controls_domain_timeline_and_measures(analyses):
    _, declared = analyses

    assert declared.declared_metric_reference.origin is ScientificValueOrigin.DECLARED
    assert len(declared.beat_references) > 1
    assert declared.beat_references[1].timestamp - declared.beat_references[0].timestamp == pytest.approx(
        60.0 / 78.0
    )
    assert declared.reconstructed_measures
    assert all(measure.internal_bpm == 78.0 for measure in declared.reconstructed_measures)
    assert all(
        measure.declared_metric_reference is declared.declared_metric_reference
        for measure in declared.reconstructed_measures
    )
    assert all(
        measure.declared_meter is declared.declared_meter
        for measure in declared.reconstructed_measures
    )


def test_immutable_and_report_outputs_label_reference_as_declared(analyses):
    _, declared = analyses
    materialized = CompletedAnalysisMaterializer().materialize(
        declared,
        MaterializationProvenance(
            analysis_execution_id="ANALYSIS-VAL-001-DECLARED-TEST",
            audio_content_id="VAL-001-MP3",
            source_revision="TEST-SOURCE-REVISION",
            pipeline_version="TEST-PIPELINE-VERSION",
            effective_configuration=(("metric_reference", "DECLARED"),),
        ),
    )

    assert materialized.tempo.state is AnalysisOutputState.PRESENT
    assert materialized.tempo.origin is ScientificValueOrigin.DECLARED
    assert materialized.tempo.provenance.source_id == "GT-VAL-001-v1"
    assert materialized.time_signature.state is AnalysisOutputState.PRESENT
    assert materialized.time_signature.value.beats == 4
    assert materialized.time_signature.value.beat_type == 4
    assert materialized.time_signature.origin is ScientificValueOrigin.DECLARED
    assert materialized.time_signature.provenance.source_id == "GT-VAL-001-v1"
    rendered = AsciiAnalyticalScoreRenderer().render(declared.analytical_score)
    assert "Meter (DECLARED) : 4/4" in rendered
    assert "Meter source: GT-VAL-001-v1" in rendered
    assert "Metric reference (DECLARED) : 78.0 quarter BPM" in rendered
    assert "Metric reference source: GT-VAL-001-v1" in rendered
    assert "detected" not in rendered.lower()
    assert "inferred" not in rendered.lower()


def test_declared_tempo_and_meter_are_independent():
    pipeline = AnalysisPipeline(separator=DummyMultiStemSeparator())
    phase, scope = declared_timeline_context()
    tempo_only = pipeline.analyze(
        MP3_PATH,
        declared_metric_reference=declared_reference(),
        declared_quarter_phase_origin=phase,
        declared_analysis_scope=scope,
    )
    meter_only = pipeline.analyze(
        MP3_PATH,
        declared_meter=declared_meter(),
    )

    tempo_only_output = CompletedAnalysisMaterializer().materialize(
        tempo_only,
        MaterializationProvenance(
            analysis_execution_id="TEMPO-ONLY",
            audio_content_id="VAL-001-MP3",
            source_revision="TEST",
            pipeline_version="TEST",
        ),
    )
    meter_only_output = CompletedAnalysisMaterializer().materialize(
        meter_only,
        MaterializationProvenance(
            analysis_execution_id="METER-ONLY",
            audio_content_id="VAL-001-MP3",
            source_revision="TEST",
            pipeline_version="TEST",
        ),
    )

    assert tempo_only_output.tempo.state is AnalysisOutputState.PRESENT
    assert tempo_only_output.time_signature.state is AnalysisOutputState.NOT_PRODUCED
    assert meter_only_output.tempo.state is AnalysisOutputState.NOT_PRODUCED
    assert meter_only_output.time_signature.state is AnalysisOutputState.PRESENT
    assert tempo_only.analytical_score.time_signature == "NOT_PRODUCED"
