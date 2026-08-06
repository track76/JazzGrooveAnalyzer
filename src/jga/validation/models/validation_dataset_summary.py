"""
Validation Dataset Summary.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationDatasetSummary:
    """
    Summary of a ValidationDataset.

    Contains only observable statistics.
    """

    observations: int
    sample_rate: int
    duration_seconds: float
