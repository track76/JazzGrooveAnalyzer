"""
Validation Run.
"""

from dataclasses import dataclass

from jga.validation.models.validation_corpus import ValidationCorpus


@dataclass(frozen=True, slots=True)
class ValidationRun:
    """
    Represents one scientific validation execution.
    """

    name: str
    corpus: ValidationCorpus
