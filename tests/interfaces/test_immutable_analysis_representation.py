from inspect import isabstract

from jga.interfaces.validation import ImmutableAnalysisRepresentation


def test_immutable_analysis_representation_is_abstract_boundary():
    assert isabstract(ImmutableAnalysisRepresentation)


def test_immutable_analysis_representation_exposes_required_contract():
    required_members = {
        "analysis_execution_id",
        "audio_content_id",
        "audio_checksum",
        "source_revision",
        "pipeline_version",
        "schema_revision",
        "effective_configuration",
        "temporal_origin_seconds",
        "measurement_units",
        "output_completeness",
        "limitations",
        "content_fingerprint",
        "tempo",
        "time_signature",
        "sections",
        "instrumentation",
        "scientific_output",
    }

    assert required_members <= set(ImmutableAnalysisRepresentation.__abstractmethods__)


def test_immutable_analysis_representation_schema_revision():
    assert ImmutableAnalysisRepresentation.SCHEMA_REVISION == "1"
