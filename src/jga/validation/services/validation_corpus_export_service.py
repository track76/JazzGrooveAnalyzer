"""
Validation Corpus Export Service.
"""

from collections.abc import Iterable

from jga.validation.exporters.validation_exporter import ValidationExporter
from jga.validation.models.validation_corpus import ValidationCorpus


class ValidationCorpusExportService:
    """
    Exports every dataset contained in a ValidationCorpus.
    """

    def export(
        self,
        corpus: ValidationCorpus,
        exporter: ValidationExporter,
        destination_factory,
    ) -> None:
        for index, dataset in enumerate(corpus.datasets):
            exporter.export(
                dataset=dataset,
                destination=destination_factory(index),
            )
