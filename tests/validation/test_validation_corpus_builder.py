from jga.validation.builders.validation_corpus_builder import (
    ValidationCorpusBuilder,
)
from jga.validation.models.validation_corpus import ValidationCorpus
from jga.validation.validation_dataset import ValidationDataset


def test_builder_returns_validation_corpus():
    builder = ValidationCorpusBuilder()

    corpus = builder.build(
        (
            ValidationDataset(),
            ValidationDataset(),
        )
    )

    assert isinstance(corpus, ValidationCorpus)
    assert len(corpus) == 2
