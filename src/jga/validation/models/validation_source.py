"""
Validation Source.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationSource:
    """
    Identifies the origin of a validation dataset.
    """

    recording_id: str
    recording_name: str
    performer: str
