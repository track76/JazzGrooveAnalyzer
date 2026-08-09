"""Item-selected execution of the approved scientific validation chain."""

from pathlib import Path

from jga.analysis_representation import (
    CompletedAnalysisMaterializer,
    MaterializationProvenance,
)
from jga.comparator import ScientificComparator
from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.scientific_validation_record import (
    ScientificValidationRecord,
    ScientificValidationRecordMaterializer,
)
from jga.validation_catalog.loaders import RepositoryValidationCatalogLoader


def execute_validation_item(
    *,
    repository_root: Path,
    validation_item_id: str,
    analysis_pipeline: AnalysisPipeline,
    materialization_provenance: MaterializationProvenance,
    comparator: ScientificComparator | None = None,
) -> ScientificValidationRecord:
    """Execute the existing immutable validation chain for one catalogue item."""
    catalogue = RepositoryValidationCatalogLoader().load(repository_root)
    item = catalogue.item(validation_item_id)

    completed_analysis = analysis_pipeline.analyze(
        (repository_root / item.mp3_recording.repository_path).as_posix()
    )
    analysis = CompletedAnalysisMaterializer().materialize(
        completed_analysis,
        materialization_provenance,
    )
    ground_truth = MusicXmlGroundTruthLoader(repository_root).load(
        Path(item.authoritative_musicxml.repository_path),
        repository_revision=item.authoritative_musicxml.repository_revision,
    )
    comparison = (comparator or ScientificComparator()).compare(
        item,
        analysis,
        ground_truth,
    )
    return ScientificValidationRecordMaterializer().materialize(
        comparison,
        analysis,
    )
