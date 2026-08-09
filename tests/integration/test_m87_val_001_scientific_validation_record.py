from pathlib import Path

from jga.analysis_representation import (
    CompletedAnalysisMaterializer,
    MaterializationProvenance,
)
from jga.comparator import ComparisonEvidenceState, ScientificComparator
from jga.ground_truth.loaders.musicxml_ground_truth_loader import (
    MusicXmlGroundTruthLoader,
)
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.scientific_validation_record import ScientificValidationRecordMaterializer
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator
from jga.validation_catalog.loaders.repository_validation_catalog_loader import (
    RepositoryValidationCatalogLoader,
)


def test_m87_val_001_complete_scientific_validation_record():
    repository_root = Path(".")
    validation_item = RepositoryValidationCatalogLoader().load(
        repository_root
    ).items[0]
    ground_truth = MusicXmlGroundTruthLoader().load(
        Path(validation_item.authoritative_musicxml.repository_path)
    )
    context = AnalysisPipeline(separator=DummyMultiStemSeparator()).analyze(
        validation_item.mp3_recording.repository_path
    )
    analysis = CompletedAnalysisMaterializer().materialize(
        context,
        MaterializationProvenance(
            analysis_execution_id="M87-VAL-001-EXECUTION",
            audio_content_id="VAL-001-MP3",
            source_revision="TEST-SOURCE-REVISION",
            pipeline_version="TEST-PIPELINE-VERSION",
            effective_configuration=(("separator", "dummy_multi_stem"),),
        ),
    )
    comparison = ScientificComparator().compare(
        validation_item,
        analysis,
        ground_truth,
    )
    record = ScientificValidationRecordMaterializer().materialize(
        comparison,
        analysis,
    )

    assert record.validation_item_id == validation_item.validation_item_id
    assert record.ground_truth_id == ground_truth.ground_truth_id
    assert record.analysis_execution_id == analysis.analysis_execution_id
    assert record.input_provenance == comparison.provenance
    assert record.comparison_result == comparison
    assert record.limitations == analysis.limitations
    assert {
        record.comparison_result.tempo.state,
        record.comparison_result.time_signature.state,
        record.comparison_result.sections.state,
        record.comparison_result.instrumentation.state,
    } == {ComparisonEvidenceState.NOT_PRODUCED}

    repeated = ScientificValidationRecordMaterializer().materialize(
        comparison,
        analysis,
    )
    assert repeated == record
