"""
Validation Corpus Builder.
"""

from collections.abc import Iterable

from jga.validation.models.validation_corpus import ValidationCorpus
from jga.validation.validation_dataset import ValidationDataset


class ValidationCorpusBuilder:
    """
    Builds a ValidationCorpus from multiple ValidationDataset objects.
    """

    def build(
        self,
        datasets: Iterable[ValidationDataset],
    ) -> ValidationCorpus:
        return ValidationCorpus(
            datasets=tuple(datasets),
        )
