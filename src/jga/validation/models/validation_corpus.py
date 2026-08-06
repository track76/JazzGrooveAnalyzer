"""
Validation Corpus.
"""

from dataclasses import dataclass, field

from jga.validation.validation_dataset import ValidationDataset


@dataclass(frozen=True, slots=True)
class ValidationCorpus:
    """
    Collection of validation datasets obtained from
    multiple real recordings.
    """

    datasets: tuple[ValidationDataset, ...] = field(default_factory=tuple)

    def __len__(self) -> int:
        return len(self.datasets)

    @property
    def is_empty(self) -> bool:
        return len(self.datasets) == 0
