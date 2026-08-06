from pathlib import Path

from jga.validation.exporters.csv_validation_exporter import (
    CsvValidationExporter,
)
from jga.validation.models.validation_corpus import ValidationCorpus
from jga.validation.services.validation_corpus_export_service import (
    ValidationCorpusExportService,
)
from jga.validation.validation_dataset import ValidationDataset


def test_export_all_datasets(tmp_path: Path):
    corpus = ValidationCorpus(
        datasets=(
            ValidationDataset(),
            ValidationDataset(),
        )
    )

    ValidationCorpusExportService().export(
        corpus=corpus,
        exporter=CsvValidationExporter(),
        destination_factory=lambda i: str(tmp_path / f"dataset_{i}.csv"),
    )

    assert (tmp_path / "dataset_0.csv").exists()
    assert (tmp_path / "dataset_1.csv").exists()
