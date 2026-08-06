from jga.validation.models.validation_corpus import ValidationCorpus
from jga.validation.models.validation_run import ValidationRun


def test_validation_run():
    corpus = ValidationCorpus()

    run = ValidationRun(
        name="M78",
        corpus=corpus,
    )

    assert run.name == "M78"
    assert run.corpus is corpus
