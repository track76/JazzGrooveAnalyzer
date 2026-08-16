from dataclasses import FrozenInstanceError
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
from jga.interfaces.scientific_value_origin import ScientificValueOrigin
from jga.interfaces.validation import AnalysisOutputState
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


MP3_PATH = "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
MP3_SHA256 = "d358d1bca5144ea1dabee4d970fa5deabf81a209922481a77db0f01bd8bdbbbb"


@pytest.fixture(scope="module")
def completed_analysis():
    return AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(MP3_PATH)


def provenance(execution_id: str = "ANALYSIS-VAL-001-TEST"):
    return MaterializationProvenance(
        analysis_execution_id=execution_id,
        audio_content_id="VAL-001-MP3",
        source_revision="TEST-SOURCE-REVISION",
        pipeline_version="TEST-PIPELINE-VERSION",
        effective_configuration=(("separator", "dummy_multi_stem"),),
    )


def declared_reference() -> DeclaredMetricReference:
    return DeclaredMetricReference(
        beats_per_minute=Decimal("78"),
        beat_unit="quarter",
        provenance=MetricReferenceProvenance(
            source_id="GT-VAL-001-v1",
            source_kind="authoritative controlled-source context",
            source_sha256=(
                "809a6ef276c4c3b9042c71d40a71763d"
                "cbf90d47e654e784af371eb53d073778"
            ),
            temporal_scope="complete controlled performance",
        ),
    )


def declared_meter() -> DeclaredMeter:
    return DeclaredMeter(4, 4, declared_reference().provenance)


def test_materializes_real_completed_analysis_with_provenance(completed_analysis):
    result = CompletedAnalysisMaterializer().materialize(
        completed_analysis,
        provenance(),
    )

    assert result.analysis_execution_id == "ANALYSIS-VAL-001-TEST"
    assert result.audio_content_id == "VAL-001-MP3"
    assert result.audio_checksum == MP3_SHA256
    assert result.source_revision == "TEST-SOURCE-REVISION"
    assert result.pipeline_version == "TEST-PIPELINE-VERSION"
    assert result.schema_revision == "1"
    assert result.temporal_origin_seconds == 0.0
    assert result.effective_configuration == (("separator", "dummy_multi_stem"),)


def test_unapproved_pipeline_defaults_are_not_materialized(completed_analysis):
    result = CompletedAnalysisMaterializer().materialize(
        completed_analysis,
        provenance(),
    )

    outputs = (
        result.tempo,
        result.time_signature,
        result.sections,
        result.instrumentation,
    )
    assert all(output.state is AnalysisOutputState.NOT_PRODUCED for output in outputs)
    assert all(output.value is None for output in outputs)
    assert result.output_completeness == (
        ("instrumentation", "NOT_PRODUCED"),
        ("sections", "NOT_PRODUCED"),
        ("tempo", "NOT_PRODUCED"),
        ("time_signature", "NOT_PRODUCED"),
    )
    assert len(result.limitations) == 4


def test_materialization_is_deeply_immutable(completed_analysis):
    result = CompletedAnalysisMaterializer().materialize(
        completed_analysis,
        provenance(),
    )

    with pytest.raises(FrozenInstanceError):
        result.pipeline_version = "changed"
    with pytest.raises(FrozenInstanceError):
        result.tempo.value = None
    assert isinstance(result.effective_configuration, tuple)
    assert isinstance(result.measurement_units, tuple)
    assert isinstance(result.limitations, tuple)


def test_content_fingerprint_is_deterministic_and_execution_independent(
    completed_analysis,
):
    materializer = CompletedAnalysisMaterializer()
    first = materializer.materialize(completed_analysis, provenance("EXECUTION-1"))
    second = materializer.materialize(completed_analysis, provenance("EXECUTION-2"))

    assert first.analysis_execution_id != second.analysis_execution_id
    assert first.content_fingerprint == second.content_fingerprint


def test_scientific_output_exposes_only_the_approved_scope(completed_analysis):
    result = CompletedAnalysisMaterializer().materialize(
        completed_analysis,
        provenance(),
    )

    assert result.scientific_output("tempo") is result.tempo
    with pytest.raises(KeyError):
        result.scientific_output("ground_truth")


def test_declared_tempo_is_materialized_with_origin_and_provenance():
    completed = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(
        MP3_PATH,
        declared_metric_reference=declared_reference(),
    )

    result = CompletedAnalysisMaterializer().materialize(
        completed,
        provenance(),
    )

    assert result.tempo.state is AnalysisOutputState.PRESENT
    assert result.tempo.value.beats_per_minute == Decimal("78")
    assert result.tempo.value.beat_unit == "quarter"
    assert result.tempo.origin is ScientificValueOrigin.DECLARED
    assert result.tempo.provenance.source_id == "GT-VAL-001-v1"
    assert result.tempo.provenance.source_kind == (
        "authoritative controlled-source context"
    )
    assert any(
        "autonomous BPM inference is deferred" in limitation
        for limitation in result.limitations
    )


def test_declared_meter_is_materialized_with_origin_and_provenance():
    completed = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(
        MP3_PATH,
        declared_meter=declared_meter(),
    )

    result = CompletedAnalysisMaterializer().materialize(
        completed,
        provenance(),
    )

    assert result.time_signature.state is AnalysisOutputState.PRESENT
    assert result.time_signature.value.beats == 4
    assert result.time_signature.value.beat_type == 4
    assert result.time_signature.origin is ScientificValueOrigin.DECLARED
    assert result.time_signature.provenance.source_id == "GT-VAL-001-v1"
    assert "autonomous meter recognition is deferred" in result.limitations[-1]
