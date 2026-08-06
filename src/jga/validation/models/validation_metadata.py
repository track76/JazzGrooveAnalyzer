"""
Validation Metadata.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationMetadata:
    """
    Scientific metadata describing a validation dataset.
    """

    analysis_version: str
    sample_rate: int
    duration_seconds: float
    recording_date: str | None = None
