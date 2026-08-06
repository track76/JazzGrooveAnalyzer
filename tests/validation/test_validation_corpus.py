from jga.validation.models.validation_corpus import ValidationCorpus
from jga.validation.validation_dataset import ValidationDataset


def test_empty_corpus():
    corpus = ValidationCorpus()

    assert corpus.is_empty
    assert len(corpus) == 0


def test_corpus_contains_datasets():
    dataset = ValidationDataset()

    corpus = ValidationCorpus(
        datasets=(dataset,),
    )

    assert not corpus.is_empty
    assert len(corpus) == 1
