from pathlib import Path

from jga.analysis_representation import MaterializationProvenance
from jga.comparator import ComparisonEvidenceState, ScientificComparator
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator
from jga.validation_execution import execute_validation_item


class FixedIdentities:
    def __init__(self) -> None:
        self._next = 0

    def __call__(self) -> str:
        self._next += 1
        return f"M93-ID-{self._next:02d}"


def test_executes_existing_scientific_chain_by_catalogue_item_identity():
    record = execute_validation_item(
        repository_root=Path("."),
        validation_item_id="VAL-001",
        analysis_pipeline=AnalysisPipeline(separator=DummyMultiStemSeparator()),
        materialization_provenance=MaterializationProvenance(
            analysis_execution_id="M93-VAL-001-EXECUTION",
            audio_content_id="VAL-001-MP3",
            source_revision="TEST-SOURCE-REVISION",
            pipeline_version="TEST-PIPELINE-VERSION",
            effective_configuration=(("separator", "dummy_multi_stem"),),
        ),
        comparator=ScientificComparator(identity_factory=FixedIdentities()),
    )

    assert record.validation_item_id == "VAL-001"
    assert record.ground_truth_id == "GT-VAL-001-v1"
    assert record.analysis_execution_id == "M93-VAL-001-EXECUTION"
    assert record.comparator_protocol_id == "JGA-COMPARATOR-001"
    assert record.comparator_schema_version == "1"
    assert {
        record.comparison_result.tempo.state,
        record.comparison_result.time_signature.state,
        record.comparison_result.sections.state,
        record.comparison_result.instrumentation.state,
    } == {ComparisonEvidenceState.NOT_PRODUCED}
