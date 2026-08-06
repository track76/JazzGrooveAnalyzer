"""
Validation Session.
"""

from dataclasses import dataclass

from jga.validation.validation_dataset import ValidationDataset


@dataclass(frozen=True, slots=True)
class ValidationSession:
    """
    Groups the dataset produced during a scientific validation run.
    """

    dataset: ValidationDataset
